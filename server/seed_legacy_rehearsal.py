import argparse
import os
import random
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    delete,
    insert,
)


LEGACY_ROLES = ["office", "fridge_tech", "washer_tech", "dryer_range_tech", "inventory"]
TYPES = ["fridge", "washer", "dryer", "range", "microwave", "water_heater", "stackable", "dishwasher"]
CONDITIONS = ["NEW", "USED", "Scratch and Dent"]
VENDORS = ["pasadena", "baton_rouge", "alexandria", "stines_lc", "stines_jn", "scrappers", "viking", "unknown"]
BRANDS = ["Whirlpool", "LG", "Samsung", "GE", "Maytag", "Frigidaire", "Bosch", "KitchenAid"]
COLORS = ["white", "black", "stainless", "silver", "slate"]
STYLES = ["top-load", "front-load", "side-by-side", "french-door", "gas", "electric", "countertop", "standard"]
STATUSES = ["in_progress", "completed", "trashed", "archived", "exported"]


def _legacy_tables(metadata: MetaData):
    users = Table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("first_name", String(50), nullable=False),
        Column("last_name", String(50), nullable=False),
        Column("role", String(50), nullable=False),
        Column("is_admin", Boolean, nullable=False, default=False),
        Column("email", String(150), nullable=False, unique=True),
        Column("password_hash", String(255), nullable=False),
    )

    machines = Table(
        "machines",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("brand", String(50), nullable=False),
        Column("type_of", String(50), nullable=False),
        Column("model", String(100), nullable=False),
        Column("serial", String(150), nullable=False, unique=True),
        Column("style", String(50), nullable=False),
        Column("color", String(50), nullable=False),
        Column("condition", String(50), nullable=False),
        Column("vendor", String(50), nullable=True),
        Column("status", String(50), nullable=False),
        Column("started_on", Date, nullable=False),
        Column("completed_on", Date, nullable=True),
        Column("trashed_on", Date, nullable=True),
        Column("exported_on", Date, nullable=True),
        Column("technician_id", Integer, ForeignKey("users.id"), nullable=False),
    )

    notes = Table(
        "notes",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("content", Text, nullable=True),
        Column("date", Date, nullable=False),
        Column("user_id", Integer, ForeignKey("users.id"), nullable=True),
        Column("machine_id", Integer, ForeignKey("machines.id"), nullable=True),
    )

    history = Table(
        "machine_status_history",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("machine_id", Integer, ForeignKey("machines.id"), nullable=False),
        Column("status", String(50), nullable=False),
        Column("prev_status", String(50), nullable=False),
        Column("changed_on", Date, nullable=False),
        Column("changed_by", Integer, ForeignKey("users.id"), nullable=True),
    )
    return users, machines, notes, history


def seed_legacy_rehearsal(database_uri: str, machine_count: int = 1200, user_count: int = 12, seed: int = 42, reset: bool = True):
    rng = random.Random(seed)
    engine = create_engine(database_uri)
    metadata = MetaData()
    users, machines, notes, history = _legacy_tables(metadata)

    with engine.begin() as conn:
        if reset:
            metadata.drop_all(conn, checkfirst=True)
        metadata.create_all(conn, checkfirst=True)

        for table in [history, notes, machines, users]:
            conn.execute(delete(table))

        user_rows = []
        for i in range(1, user_count + 1):
            is_admin = i == 1
            user_rows.append(
                {
                    "id": i,
                    "first_name": f"Tech{i}",
                    "last_name": "User",
                    "role": "office" if is_admin else LEGACY_ROLES[(i - 1) % len(LEGACY_ROLES)],
                    "is_admin": is_admin,
                    "email": f"tech{i}@example.local",
                    "password_hash": "pbkdf2:sha256:placeholder",
                }
            )
        conn.execute(insert(users), user_rows)

        machine_rows = []
        note_rows = []
        history_rows = []
        note_id = 1
        history_id = 1
        today = date.today()

        for i in range(1, machine_count + 1):
            tech_id = rng.randint(1, user_count)
            started_on = today - timedelta(days=rng.randint(30, 365))
            status = rng.choices(STATUSES, weights=[35, 30, 20, 10, 5], k=1)[0]

            completed_on = None
            trashed_on = None
            exported_on = None

            if status == "completed":
                completed_on = started_on + timedelta(days=rng.randint(1, 30))
            elif status == "trashed":
                trashed_on = started_on + timedelta(days=rng.randint(1, 30))
            elif status in {"archived", "exported"}:
                completed_on = started_on + timedelta(days=rng.randint(1, 20))
                exported_on = completed_on + timedelta(days=rng.randint(1, 30))

            machine_rows.append(
                {
                    "id": i,
                    "brand": rng.choice(BRANDS),
                    "type_of": rng.choice(TYPES),
                    "model": f"MODEL-{rng.randint(1000, 9999)}",
                    "serial": f"SER-{i:06d}-{rng.randint(100,999)}",
                    "style": rng.choice(STYLES),
                    "color": rng.choice(COLORS),
                    "condition": rng.choices(CONDITIONS, weights=[20, 60, 20], k=1)[0],
                    "vendor": rng.choice(VENDORS),
                    "status": status,
                    "started_on": started_on,
                    "completed_on": completed_on,
                    "trashed_on": trashed_on,
                    "exported_on": exported_on,
                    "technician_id": tech_id,
                }
            )

            if status in {"completed", "trashed", "archived", "exported"}:
                to_status = "completed" if status in {"archived", "exported"} else status
                changed_on = completed_on or trashed_on or exported_on or started_on
                history_rows.append(
                    {
                        "id": history_id,
                        "machine_id": i,
                        "status": to_status,
                        "prev_status": "in_progress",
                        "changed_on": changed_on,
                        "changed_by": tech_id,
                    }
                )
                history_id += 1

                if status in {"archived", "exported"}:
                    history_rows.append(
                        {
                            "id": history_id,
                            "machine_id": i,
                            "status": "archived",
                            "prev_status": "completed",
                            "changed_on": exported_on or changed_on,
                            "changed_by": tech_id,
                        }
                    )
                    history_id += 1

            note_total = rng.randint(0, 2)
            for _ in range(note_total):
                note_rows.append(
                    {
                        "id": note_id,
                        "content": f"Legacy rehearsal note {note_id} for machine {i}",
                        "date": started_on + timedelta(days=rng.randint(0, 10)),
                        "user_id": tech_id,
                        "machine_id": i,
                    }
                )
                note_id += 1

        conn.execute(insert(machines), machine_rows)
        if note_rows:
            conn.execute(insert(notes), note_rows)
        if history_rows:
            conn.execute(insert(history), history_rows)

    return {
        "database_uri": database_uri,
        "seed": seed,
        "counts": {
            "users": len(user_rows),
            "machines": len(machine_rows),
            "notes": len(note_rows),
            "machine_status_history": len(history_rows),
        },
    }


def main():
    load_dotenv(Path(__file__).resolve().parent / ".env")
    parser = argparse.ArgumentParser(description="Seed legacy-schema rehearsal data into a local MySQL database.")
    parser.add_argument(
        "--database-uri",
        default=os.getenv("LEGACY_DATABASE_URI"),
        help="Target legacy DB URI. Defaults to LEGACY_DATABASE_URI from .env.",
    )
    parser.add_argument("--machines", type=int, default=1200, help="Number of legacy machines to generate.")
    parser.add_argument("--users", type=int, default=12, help="Number of legacy users to generate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for deterministic data generation.")
    parser.add_argument(
        "--no-reset",
        action="store_true",
        help="Do not drop/recreate legacy tables; still clears table contents before insert.",
    )
    args = parser.parse_args()

    if not args.database_uri:
        raise SystemExit("Missing database URI. Set LEGACY_DATABASE_URI in server/.env or pass --database-uri.")

    result = seed_legacy_rehearsal(
        database_uri=args.database_uri,
        machine_count=args.machines,
        user_count=args.users,
        seed=args.seed,
        reset=not args.no_reset,
    )
    print(result)


if __name__ == "__main__":
    main()
