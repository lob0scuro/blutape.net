import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import MetaData, Table, create_engine, delete, insert


TABLE_ORDER = [
    "users",
    "machines",
    "work_orders",
    "work_order_events",
    "machine_notes",
]


def _read_rows(input_dir: Path, table_name: str):
    path = input_dir / f"{table_name}.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a JSON array.")
    return payload


def _load_tables(engine):
    metadata = MetaData()
    tables = {}
    for name in TABLE_ORDER:
        tables[name] = Table(name, metadata, autoload_with=engine)
    return tables


def load_payload(database_uri: str, input_dir: str, dry_run: bool = False, clear_first: bool = False):
    engine = create_engine(database_uri)
    input_path = Path(input_dir)
    tables = _load_tables(engine)
    payloads = {name: _read_rows(input_path, name) for name in TABLE_ORDER}

    summary = {
        "input_dir": str(input_path.resolve()),
        "dry_run": dry_run,
        "clear_first": clear_first,
        "loaded_counts": {name: len(payloads[name]) for name in TABLE_ORDER},
    }

    if dry_run:
        return summary

    with engine.begin() as conn:
        if clear_first:
            for name in reversed(TABLE_ORDER):
                conn.execute(delete(tables[name]))

        for name in TABLE_ORDER:
            rows = payloads[name]
            if rows:
                conn.execute(insert(tables[name]), rows)

    return summary


def main():
    load_dotenv(Path(__file__).resolve().parent / ".env")

    parser = argparse.ArgumentParser(
        description="Load formatted migration JSON payloads into new schema tables in FK-safe order."
    )
    parser.add_argument(
        "--database-uri",
        default=os.getenv("DATABASE_URI"),
        help="Target SQLAlchemy DB URI. Defaults to DATABASE_URI env var.",
    )
    parser.add_argument(
        "--input-dir",
        default=str(Path(__file__).resolve().parent / "migration_output"),
        help="Directory containing users.json, machines.json, work_orders.json, work_order_events.json, machine_notes.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and report counts only; no inserts/deletes.",
    )
    parser.add_argument(
        "--clear-first",
        action="store_true",
        help="Delete existing rows from target tables before inserting payloads.",
    )
    args = parser.parse_args()

    if not args.database_uri:
        raise SystemExit("Missing database URI. Pass --database-uri or set DATABASE_URI in environment/.env.")

    summary = load_payload(
        database_uri=args.database_uri,
        input_dir=args.input_dir,
        dry_run=args.dry_run,
        clear_first=args.clear_first,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
