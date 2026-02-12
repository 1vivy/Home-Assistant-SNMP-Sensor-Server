#!/usr/bin/python3

import json
import os
import sys


def build_mappings(device_id):
    base_sensor = f"sensor.ef_{device_id}_"
    base_binary = f"binary_sensor.ef_{device_id}_"

    # Designed for ha-ef-ble naming with practical fallbacks.
    return [
        {
            "oid": "1.3.6.1.2.1.33.1.1.2.0",
            "snmp_type": "string",
            "static_value": "EcoFlow BLE",
        },
        {
            "oid": "1.3.6.1.2.1.33.1.1.5.0",
            "snmp_type": "string",
            "static_value": f"EcoFlow {device_id}",
        },
        {
            "oid": "1.3.6.1.2.1.33.1.2.4.0",
            "entity_ids": [
                f"{base_sensor}battery_level",
                f"{base_sensor}main_battery_level",
            ],
            "snmp_type": "integer",
            "default_value": 0,
        },
        {
            "oid": "1.3.6.1.2.1.33.1.4.1.0",
            "entity_ids": [
                f"{base_binary}plug",
                f"{base_binary}plugged_in_ac",
            ],
            "snmp_type": "integer",
            "value_map": {
                "on": 3,
                "off": 5,
                "true": 3,
                "false": 5,
            },
            "default_value": 2,
        },
        {
            "oid": "1.3.6.1.2.1.33.1.4.4.1.4.1",
            "entity_id": f"{base_sensor}output_power",
            "snmp_type": "integer",
            "default_value": 0,
        },
    ]


def merge_manual_overrides(auto_mappings, manual_mappings):
    by_oid = {str(item["oid"]): item for item in auto_mappings}
    for item in manual_mappings:
        by_oid[str(item["oid"])] = item
    merged = list(by_oid.values())
    merged.sort(key=lambda item: tuple(int(part) for part in str(item["oid"]).strip(".").split(".")))
    return merged


def main():
    if len(sys.argv) != 4:
        raise SystemExit("Usage: generate-ecoflow-ups-mappings.py <device_id> <manual_json> <output_file>")

    device_id = sys.argv[1].strip().lower()
    manual_raw = sys.argv[2]
    output_file = sys.argv[3]

    if not device_id:
        raise ValueError("ecoflow_device_id must not be empty when ecoflow_ups_mode is enabled")

    if manual_raw.strip():
        manual_mappings = json.loads(manual_raw)
    else:
        manual_mappings = []

    if not isinstance(manual_mappings, list):
        raise ValueError("ups_oid_mappings must be a JSON array")

    auto_mappings = build_mappings(device_id)
    merged = merge_manual_overrides(auto_mappings, manual_mappings)

    with open(output_file, "w", encoding="utf-8") as handle:
        json.dump(merged, handle)

    print(f"Generated {len(merged)} UPS mappings for EcoFlow device {device_id}")


if __name__ == "__main__":
    main()
