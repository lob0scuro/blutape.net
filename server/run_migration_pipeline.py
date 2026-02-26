import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from format_legacy_data import format_legacy_data
from load_migration_payload import load_payload


TARGET_TABLES = [
    "users",
    "machines",
    "work_orders",
    "work_order_events",
    "machine_notes",
]


def _missing_tables(database_uri: str, required_tables: list[str]):
    engine = create_engine(database_uri)
    with engine.connect() as conn:
        existing = {
            row[0]
            for row in conn.execute(
                text(
                    "SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema = DATABASE()"
                )
            )
        }
    return [table for table in required_tables if table not in existing]


def _parse_mysql_uri(uri: str):
    parsed = urlparse(uri)
    if parsed.scheme.split("+")[0] != "mysql":
        raise ValueError(f"Only MySQL URIs are supported for backup. Got scheme: {parsed.scheme}")
    db = (parsed.path or "").lstrip("/")
    if not db:
        raise ValueError("Database name is missing in URI path.")
    return {
        "host": parsed.hostname or "127.0.0.1",
        "port": parsed.port or 3306,
        "user": parsed.username or "",
        "password": parsed.password or "",
        "database": db,
    }


def _run_backup(new_database_uri: str, backup_path: Path):
    cfg = _parse_mysql_uri(new_database_uri)
    backup_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "mysqldump",
        "-h",
        cfg["host"],
        "-P",
        str(cfg["port"]),
        "-u",
        cfg["user"],
        "--single-transaction",
        "--quick",
        "--routines",
        "--triggers",
        cfg["database"],
    ]

    env = os.environ.copy()
    if cfg["password"]:
        env["MYSQL_PWD"] = cfg["password"]

    with open(backup_path, "w", encoding="utf-8") as handle:
        result = subprocess.run(cmd, stdout=handle, stderr=subprocess.PIPE, text=True, env=env)
    if result.returncode != 0:
        raise RuntimeError(f"Backup failed: {result.stderr.strip()}")


def _table_counts(database_uri: str):
    counts = {}
    engine = create_engine(database_uri)
    with engine.connect() as conn:
        for table in TARGET_TABLES:
            counts[table] = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()
    return counts


def run_pipeline(
    legacy_database_uri: str,
    new_database_uri: str,
    output_dir: str,
    backup_file: str | None,
    skip_backup: bool,
    execute_load: bool,
):
    output_path = Path(output_dir)

    summary = {
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "legacy_database_uri": legacy_database_uri,
        "new_database_uri": new_database_uri,
        "output_dir": str(output_path.resolve()),
        "steps": {},
    }

    missing_target = _missing_tables(new_database_uri, TARGET_TABLES)
    if missing_target:
        raise RuntimeError(
            "Target database is not on new schema. Missing tables: "
            + ", ".join(missing_target)
        )

    if not skip_backup:
        backup_path = (
            Path(backup_file)
            if backup_file
            else Path(__file__).resolve().parent
            / "backups"
            / f"pre_migration_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        )
        _run_backup(new_database_uri, backup_path)
        summary["steps"]["backup"] = {"status": "ok", "backup_file": str(backup_path.resolve())}
    else:
        summary["steps"]["backup"] = {"status": "skipped"}

    format_summary = format_legacy_data(legacy_database_uri, str(output_path))
    summary["steps"]["format"] = format_summary

    dry_run_summary = load_payload(
        database_uri=new_database_uri,
        input_dir=str(output_path),
        dry_run=True,
        clear_first=False,
    )
    summary["steps"]["dry_run"] = dry_run_summary

    if execute_load:
        load_summary = load_payload(
            database_uri=new_database_uri,
            input_dir=str(output_path),
            dry_run=False,
            clear_first=True,
        )
        summary["steps"]["load"] = load_summary
        summary["steps"]["verify_counts"] = _table_counts(new_database_uri)
    else:
        summary["steps"]["load"] = {"status": "skipped", "reason": "Use --execute-load to perform real inserts."}

    summary["finished_at"] = datetime.now().isoformat(timespec="seconds")
    return summary


def main():
    load_dotenv(Path(__file__).resolve().parent / ".env")
    parser = argparse.ArgumentParser(
        description="Run full migration pipeline: backup new DB, format legacy data, dry-run load, optional real load + verify."
    )
    parser.add_argument(
        "--legacy-database-uri",
        default=os.getenv("LEGACY_DATABASE_URI"),
        help="Legacy DB URI (source). Defaults to LEGACY_DATABASE_URI from .env.",
    )
    parser.add_argument(
        "--new-database-uri",
        default=os.getenv("DATABASE_URI"),
        help="New DB URI (target). Defaults to DATABASE_URI from .env.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parent / "migration_output_prod"),
        help="Output directory for formatted payload files.",
    )
    parser.add_argument(
        "--backup-file",
        default=None,
        help="Optional explicit backup .sql path for pre-migration backup.",
    )
    parser.add_argument(
        "--skip-backup",
        action="store_true",
        help="Skip pre-migration backup step (not recommended in production).",
    )
    parser.add_argument(
        "--execute-load",
        action="store_true",
        help="Perform real load with clear-first. Without this, script only backs up + formats + dry-runs.",
    )
    args = parser.parse_args()

    if not args.legacy_database_uri:
        raise SystemExit("Missing legacy DB URI. Set LEGACY_DATABASE_URI or pass --legacy-database-uri.")
    if not args.new_database_uri:
        raise SystemExit("Missing new DB URI. Set DATABASE_URI or pass --new-database-uri.")

    result = run_pipeline(
        legacy_database_uri=args.legacy_database_uri,
        new_database_uri=args.new_database_uri,
        output_dir=args.output_dir,
        backup_file=args.backup_file,
        skip_backup=args.skip_backup,
        execute_load=args.execute_load,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}", file=sys.stderr)
        raise
