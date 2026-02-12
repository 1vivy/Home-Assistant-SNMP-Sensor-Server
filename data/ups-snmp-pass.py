#!/usr/bin/python3

import json
import os
import sys
from requests import get

SUPERVISOR_TOKEN = os.environ.get("SUPERVISOR_TOKEN", "")
MAPPING_FILE = os.environ.get("UPS_OID_MAPPINGS_FILE", "/tmp/ups-oid-mappings.json")
HA_STATES_URL = "http://supervisor/core/api/states/"


TYPE_ALIASES = {
    "int": "integer",
    "integer": "integer",
    "gauge": "gauge",
    "counter": "counter",
    "timeticks": "timeticks",
    "str": "string",
    "string": "string",
}

NUMERIC_TYPES = {"integer", "gauge", "counter", "timeticks"}


def parse_oid(oid_str):
    oid_str = oid_str.strip()
    if oid_str.startswith("."):
        oid_str = oid_str[1:]
    return tuple(int(part) for part in oid_str.split(".") if part)


def format_oid(oid_parts):
    return "." + ".".join(str(part) for part in oid_parts)


def load_mappings():
    with open(MAPPING_FILE, "r", encoding="utf-8") as handle:
        raw_mappings = json.load(handle)

    parsed = []
    for mapping in raw_mappings:
        oid = parse_oid(str(mapping["oid"]))
        snmp_type = TYPE_ALIASES.get(str(mapping.get("snmp_type", "string")).lower())
        if not snmp_type:
            continue

        if "entity_ids" in mapping and isinstance(mapping["entity_ids"], list):
            entity_ids = [str(entity_id) for entity_id in mapping["entity_ids"] if str(entity_id).strip()]
        elif "entity_id" in mapping:
            entity_ids = [str(mapping["entity_id"])]
        else:
            entity_ids = []

        parsed.append(
            {
                "oid": oid,
                "entity_ids": entity_ids,
                "snmp_type": snmp_type,
                "scale": float(mapping.get("scale", 1)),
                "offset": float(mapping.get("offset", 0)),
                "value_map": mapping.get("value_map", {}),
                "default_value": mapping.get("default_value"),
                "static_value": mapping.get("static_value"),
            }
        )

    parsed.sort(key=lambda item: item["oid"])
    return parsed


def normalize_numeric(value):
    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"on", "true", "plugged_in", "plugged in"}:
            return 1.0
        if normalized in {"off", "false", "unplugged", "not plugged in"}:
            return 0.0
        return float(value)

    raise ValueError("Value is not numeric")


def resolve_value(mapping, raw_state):
    state_key = str(raw_state)
    value_map = mapping.get("value_map") or {}

    if state_key in value_map:
        value = value_map[state_key]
    else:
        lowered = state_key.lower()
        value = value_map.get(lowered, raw_state)

    if value in (None, "unknown", "unavailable") and mapping.get("default_value") is not None:
        value = mapping["default_value"]

    if mapping["snmp_type"] in NUMERIC_TYPES:
        value = normalize_numeric(value)
        value = value * mapping["scale"] + mapping["offset"]
        return str(int(round(value)))

    return str(value)


def fetch_state(entity_id):
    response = get(
        HA_STATES_URL + entity_id,
        headers={
            "Authorization": "Bearer " + SUPERVISOR_TOKEN,
            "content-type": "application/json",
        },
        timeout=10,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Unable to fetch state for {entity_id}: {response.status_code}")

    payload = response.json()
    return payload.get("state")


def fetch_first_state(entity_ids):
    last_error = None
    for entity_id in entity_ids:
        try:
            return fetch_state(entity_id)
        except Exception as error:  # noqa: PERF203
            last_error = error
    if last_error:
        raise last_error
    raise RuntimeError("No entity IDs configured")


def find_getnext(mappings, oid):
    for mapping in mappings:
        if mapping["oid"] > oid:
            return mapping
    return None


def output_mapping(mapping):
    if mapping.get("static_value") is not None:
        value = mapping["static_value"]
    else:
        try:
            raw_state = fetch_first_state(mapping["entity_ids"])
        except Exception:
            if mapping.get("default_value") is None:
                raise
            raw_state = mapping["default_value"]

        value = resolve_value(mapping, raw_state)

    print(format_oid(mapping["oid"]))
    print(mapping["snmp_type"])
    print(value)


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in {"-g", "-n"}:
        sys.exit(1)

    mappings = load_mappings()
    if not mappings:
        sys.exit(0)

    command = sys.argv[1]
    request_oid = parse_oid(sys.argv[2])

    if command == "-g":
        selected = next((item for item in mappings if item["oid"] == request_oid), None)
    else:
        selected = find_getnext(mappings, request_oid)

    if not selected:
        sys.exit(0)

    output_mapping(selected)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # SNMP pass scripts should fail silently from snmpd's perspective.
        sys.exit(0)
