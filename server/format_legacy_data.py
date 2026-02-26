import argparse
import json
import os
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import MetaData, Table, create_engine, inspect, select


ROLE_MAP = {
    "office": "technician",
    "fridge_tech": "technician",
    "washer_tech": "technician",
    "dryer_range_tech": "technician",
    "inventory": "technician",
}

CATEGORY_MAP = {
    "fridge": "refrigerator",
    "washer": "washer",
    "dryer": "dryer",
    "range": "range",
    "microwave": "microwave",
    "water_heater": "water_heater",
    "stackable": "laundry_tower",
    "dishwasher": "dishwasher",
}

CONDITION_MAP = {
    "NEW": "new",
    "USED": "used",
    "Scratch and Dent": "scratch_and_dent",
}

VENDOR_MAP = {
    "pasadena": "pasadena",
    "baton_rouge": "baton_rouge",
    "alexandria": "alexandria",
    "stines_lc": "stines",
    "stines_jn": "stines",
    "scrappers": "scrappers",
    "viking": "viking",
    "unknown": "unknown",
}

STATUS_MAP = {
    "in_progress": "in_progress",
    "completed": "completed",
    "trashed": "trashed",
    "archived": "archived",
    "exported": "archived",
}


def _to_iso(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        return value
    raise ValueError(f"Unsupported date value type: {type(value)}")


def _event_type_for(to_status, from_status):
    if to_status == "completed":
        return "completed"
    if to_status == "trashed":
        return "trashed"
    if to_status == "archived":
        return "archived"
    if to_status == "in_progress":
        if from_status in {"completed", "trashed", "archived"}:
            return "reopened"
        return "initiated"
    return "initiated"


def _first_valid_user_id(users):
    return users[0]["id"] if users else None


def _read_legacy_tables(engine):
    metadata = MetaData()
    insp = inspect(engine)
    table_names = set(insp.get_table_names())

    if "users" not in table_names or "machines" not in table_names:
        raise RuntimeError(
            "Source database is missing required tables 'users' and/or 'machines'. "
            "If this is your legacy rehearsal DB, seed/create legacy tables first."
        )

    users_table = Table("users", metadata, autoload_with=engine)
    machines_table = Table("machines", metadata, autoload_with=engine)

    notes_source = "notes" if "notes" in table_names else "machine_notes" if "machine_notes" in table_names else None
    history_source = "machine_status_history" if "machine_status_history" in table_names else None

    if notes_source is None:
        raise RuntimeError(
            "No note table found. Expected either 'notes' (legacy) or 'machine_notes' (new)."
        )

    notes_table = Table(notes_source, metadata, autoload_with=engine)
    history_table = (
        Table(history_source, metadata, autoload_with=engine) if history_source else None
    )

    work_orders_table = (
        Table("work_orders", metadata, autoload_with=engine) if "work_orders" in table_names else None
    )
    work_order_events_table = (
        Table("work_order_events", metadata, autoload_with=engine)
        if "work_order_events" in table_names
        else None
    )

    with engine.connect() as conn:
        users = conn.execute(select(users_table)).mappings().all()
        machines = conn.execute(select(machines_table)).mappings().all()
        notes = conn.execute(select(notes_table)).mappings().all()
        history = (
            conn.execute(select(history_table)).mappings().all()
            if history_table is not None
            else []
        )
        work_orders = (
            conn.execute(select(work_orders_table)).mappings().all()
            if work_orders_table is not None
            else []
        )
        work_order_events = (
            conn.execute(select(work_order_events_table)).mappings().all()
            if work_order_events_table is not None
            else []
        )

    return (
        users,
        machines,
        notes,
        history,
        work_orders,
        work_order_events,
        {"notes": notes_source, "history": history_source},
    )


def _transform_users(legacy_users):
    users = []
    for u in legacy_users:
        role_raw = u.get("role")
        if role_raw in {"admin", "technician"}:
            role = role_raw
        else:
            is_admin = bool(u.get("is_admin"))
            role = "admin" if is_admin else ROLE_MAP.get(role_raw, "technician")
        users.append(
            {
                "id": u["id"],
                "first_name": u["first_name"],
                "last_name": u["last_name"],
                "email": u["email"],
                "password_hash": u["password_hash"],
                "role": role,
            }
        )
    users.sort(key=lambda r: r["id"])
    return users


def _transform_machines(legacy_machines):
    machines = []
    warnings = []

    for m in legacy_machines:
        category = m.get("category") or CATEGORY_MAP.get(m.get("type_of"))
        condition = m.get("condition")
        if condition in {"new", "used", "scratch_and_dent"}:
            mapped_condition = condition
        else:
            mapped_condition = CONDITION_MAP.get(condition)
        vendor = m.get("vendor")
        if vendor in {"pasadena", "baton_rouge", "college_station", "alexandria", "stines", "scrappers", "viking", "unknown"}:
            mapped_vendor = vendor
        else:
            mapped_vendor = VENDOR_MAP.get(vendor, "unknown")

        if category is None:
            warnings.append(
                f"Machine {m.get('id')}: unknown type_of={m.get('type_of')}; defaulted to 'refrigerator'."
            )
            category = "refrigerator"

        if mapped_condition is None:
            warnings.append(
                f"Machine {m.get('id')}: unknown condition={m.get('condition')}; defaulted to 'used'."
            )
            mapped_condition = "used"

        machines.append(
            {
                "id": m["id"],
                "brand": m["brand"],
                "model": m["model"],
                "serial": m["serial"],
                "category": category,
                "form_factor": m.get("form_factor") or m.get("style"),
                "color": m["color"],
                "condition": mapped_condition,
                "vendor": mapped_vendor,
            }
        )

    machines.sort(key=lambda r: r["id"])
    return machines, warnings


def _transform_work_orders(legacy_machines, user_ids):
    work_orders = []
    warnings = []

    for m in legacy_machines:
        mapped_status = m.get("current_status") or STATUS_MAP.get(m.get("status"), "in_progress")
        initiated_by = m.get("technician_id")
        if initiated_by not in user_ids:
            warnings.append(
                f"Machine {m.get('id')}: technician_id={m.get('technician_id')} not found; using fallback."
            )
            initiated_by = min(user_ids) if user_ids else None

        closed_on = None
        if mapped_status == "completed":
            closed_on = _to_iso(m.get("completed_on") or m.get("closed_on"))
        elif mapped_status == "trashed":
            closed_on = _to_iso(m.get("trashed_on") or m.get("closed_on"))

        archived_on = _to_iso(m.get("exported_on") or m.get("archived_on")) if mapped_status == "archived" else None

        work_orders.append(
            {
                "id": m["id"],
                "machine_id": m["id"],
                "initiated_on": _to_iso(m.get("started_on") or m.get("initiated_on")),
                "initiated_by": initiated_by,
                "current_status": mapped_status,
                "closed_on": closed_on,
                "archived_on": archived_on,
            }
        )

    work_orders.sort(key=lambda r: r["id"])
    return work_orders, warnings


def _transform_work_order_events(legacy_machines, legacy_history, work_orders, user_ids):
    machine_by_id = {m["id"]: m for m in legacy_machines}
    work_order_by_machine = {wo["machine_id"]: wo for wo in work_orders}
    history_by_machine = defaultdict(list)
    warnings = []

    for h in legacy_history:
        history_by_machine[h["machine_id"]].append(h)

    for machine_id in history_by_machine:
        history_by_machine[machine_id].sort(
            key=lambda r: (_to_iso(r.get("changed_on")) or "", r.get("id") or 0)
        )

    events = []
    seen = set()
    event_id = 1

    def append_event(event):
        nonlocal event_id
        key = (
            event["work_order_id"],
            event["machine_id"],
            event["event_type"],
            event["from_status"],
            event["to_status"],
            event["event_date"],
            event["technician_id"],
        )
        if key in seen:
            return
        seen.add(key)
        event["id"] = event_id
        event_id += 1
        events.append(event)

    for machine_id, wo in work_order_by_machine.items():
        machine = machine_by_id[machine_id]
        initiated_by = wo["initiated_by"]
        if initiated_by not in user_ids:
            initiated_by = min(user_ids) if user_ids else None

        append_event(
            {
                "work_order_id": wo["id"],
                "machine_id": machine_id,
                "event_type": "initiated",
                "from_status": None,
                "to_status": "in_progress",
                "event_date": wo["initiated_on"],
                "technician_id": initiated_by,
                "reason": "default",
            }
        )

        for h in history_by_machine.get(machine_id, []):
            to_status = STATUS_MAP.get(h.get("status"))
            from_status = STATUS_MAP.get(h.get("prev_status"))
            if to_status is None:
                warnings.append(
                    f"History {h.get('id')}: unknown status={h.get('status')}; skipped."
                )
                continue
            tech_id = h.get("changed_by")
            if tech_id not in user_ids:
                tech_id = initiated_by
            append_event(
                {
                    "work_order_id": wo["id"],
                    "machine_id": machine_id,
                    "event_type": _event_type_for(to_status, from_status),
                    "from_status": from_status,
                    "to_status": to_status,
                    "event_date": _to_iso(h.get("changed_on")),
                    "technician_id": tech_id,
                    "reason": "default",
                }
            )

        current_status = wo["current_status"]
        if current_status in {"completed", "trashed", "archived"}:
            terminal_date = wo["closed_on"] or wo["archived_on"]
            append_event(
                {
                    "work_order_id": wo["id"],
                    "machine_id": machine_id,
                    "event_type": _event_type_for(current_status, "in_progress"),
                    "from_status": "in_progress",
                    "to_status": current_status,
                    "event_date": terminal_date or wo["initiated_on"],
                    "technician_id": initiated_by,
                    "reason": "default",
                }
            )

    events.sort(key=lambda r: (r["event_date"] or "", r["id"]))
    for idx, event in enumerate(events, start=1):
        event["id"] = idx
    return events, warnings


def _transform_notes(legacy_notes, legacy_machines, user_ids):
    machine_ids = {m["id"] for m in legacy_machines}
    machine_tech = {m["id"]: m.get("technician_id") for m in legacy_machines}
    fallback_user_id = min(user_ids) if user_ids else None

    notes = []
    warnings = []
    skipped = 0

    for n in legacy_notes:
        machine_id = n.get("machine_id")
        if machine_id not in machine_ids:
            skipped += 1
            continue

        technician_id = n.get("user_id") or n.get("technician_id")
        if technician_id not in user_ids:
            technician_id = machine_tech.get(machine_id)
        if technician_id not in user_ids:
            technician_id = fallback_user_id
        if technician_id is None:
            skipped += 1
            continue

        content = (n.get("content") or "").strip()
        if not content:
            skipped += 1
            continue

        notes.append(
            {
                "id": n["id"],
                "content": content,
                "added_on": _to_iso(n.get("date") or n.get("added_on")),
                "technician_id": technician_id,
                "machine_id": machine_id,
            }
        )

    if skipped:
        warnings.append(f"Skipped {skipped} legacy note rows due to missing required fields/FKs.")

    notes.sort(key=lambda r: r["id"])
    return notes, warnings


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def _normalize_existing_work_orders(rows, user_ids, machine_ids):
    work_orders = []
    for row in rows:
        initiated_by = row.get("initiated_by")
        if initiated_by not in user_ids:
            initiated_by = min(user_ids) if user_ids else None
        machine_id = row.get("machine_id")
        if machine_id not in machine_ids:
            continue
        work_orders.append(
            {
                "id": row["id"],
                "machine_id": machine_id,
                "initiated_on": _to_iso(row.get("initiated_on")),
                "initiated_by": initiated_by,
                "current_status": row.get("current_status"),
                "closed_on": _to_iso(row.get("closed_on")),
                "archived_on": _to_iso(row.get("archived_on")),
            }
        )
    work_orders.sort(key=lambda r: r["id"])
    return work_orders


def _normalize_existing_work_order_events(rows, work_order_ids, machine_ids, user_ids):
    events = []
    for row in rows:
        if row.get("work_order_id") not in work_order_ids:
            continue
        if row.get("machine_id") not in machine_ids:
            continue
        technician_id = row.get("technician_id")
        if technician_id not in user_ids:
            technician_id = min(user_ids) if user_ids else None
        events.append(
            {
                "id": row["id"],
                "work_order_id": row["work_order_id"],
                "machine_id": row["machine_id"],
                "event_type": row.get("event_type"),
                "from_status": row.get("from_status"),
                "to_status": row.get("to_status"),
                "event_date": _to_iso(row.get("event_date")),
                "technician_id": technician_id,
                "reason": row.get("reason") or "default",
            }
        )
    events.sort(key=lambda r: (r["event_date"] or "", r["id"]))
    return events


def format_legacy_data(database_uri, output_dir):
    engine = create_engine(database_uri)
    (
        legacy_users,
        legacy_machines,
        legacy_notes,
        legacy_history,
        existing_work_orders,
        existing_work_order_events,
        source_tables,
    ) = _read_legacy_tables(engine)

    users = _transform_users(legacy_users)
    user_ids = {u["id"] for u in users}

    machines, machine_warnings = _transform_machines(legacy_machines)
    is_legacy_machines = bool(legacy_machines) and "type_of" in legacy_machines[0]
    if is_legacy_machines:
        work_orders, wo_warnings = _transform_work_orders(legacy_machines, user_ids)
        work_order_events, event_warnings = _transform_work_order_events(
            legacy_machines, legacy_history, work_orders, user_ids
        )
    else:
        machine_ids = {m["id"] for m in machines}
        work_orders = _normalize_existing_work_orders(existing_work_orders, user_ids, machine_ids)
        work_order_ids = {wo["id"] for wo in work_orders}
        work_order_events = _normalize_existing_work_order_events(
            existing_work_order_events, work_order_ids, machine_ids, user_ids
        )
        wo_warnings = []
        event_warnings = []
    machine_notes, note_warnings = _transform_notes(legacy_notes, legacy_machines, user_ids)

    payload = {
        "users": users,
        "machines": machines,
        "work_orders": work_orders,
        "work_order_events": work_order_events,
        "machine_notes": machine_notes,
    }

    output_root = Path(output_dir)
    _write_json(output_root / "users.json", users)
    _write_json(output_root / "machines.json", machines)
    _write_json(output_root / "work_orders.json", work_orders)
    _write_json(output_root / "work_order_events.json", work_order_events)
    _write_json(output_root / "machine_notes.json", machine_notes)
    _write_json(output_root / "migration_payload.json", payload)

    warnings = machine_warnings + wo_warnings + event_warnings + note_warnings
    summary = {
        "legacy_counts": {
            "users": len(legacy_users),
            "machines": len(legacy_machines),
            "notes": len(legacy_notes),
            "machine_status_history": len(legacy_history),
        },
        "source_tables": source_tables,
        "formatted_counts": {key: len(value) for key, value in payload.items()},
        "warnings": warnings,
        "output_dir": str(output_root.resolve()),
    }
    _write_json(output_root / "summary.json", summary)
    return summary


def main():
    load_dotenv(Path(__file__).resolve().parent / ".env")
    parser = argparse.ArgumentParser(
        description="Format legacy models.py table data into insert-ready payloads for new model schema."
    )
    parser.add_argument(
        "--database-uri",
        default=os.getenv("LEGACY_DATABASE_URI") or os.getenv("DATABASE_URI"),
        help="SQLAlchemy DB URI for the legacy dataset. Defaults to LEGACY_DATABASE_URI, then DATABASE_URI.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parent / "migration_output"),
        help="Directory where transformed JSON payloads will be written.",
    )
    args = parser.parse_args()

    if not args.database_uri:
        raise SystemExit("Missing database URI. Pass --database-uri or set DATABASE_URI in environment/.env.")

    summary = format_legacy_data(args.database_uri, args.output_dir)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
