# Changelog

## 1.6.0

- Added `ecoflow_ups_mode` and `ecoflow_device_id` so a single EcoFlow device id can auto-generate UPS-MIB mappings for ha-ef-ble entities.
- Added auto-generated mappings for practical UPS fields: device identity, charge remaining, output source (OL/OB behavior from plug state), and output power.
- Added support for `entity_ids` fallbacks and `static_value` in UPS mapping entries to handle model differences.
- Kept manual `ups_oid_mappings` support as an override mechanism when custom OIDs are needed.

## 1.5.0

- Added manual UPS OID mapping support (`enable_ups_oid_mapping` + `ups_oid_mappings`) to bind Home Assistant entities directly to UPS-MIB OIDs.
- Added value conversion options for mapped OIDs (`value_map`, `scale`, `offset`, and `default_value`) to support cases like EcoFlow plug state to `OL/OB`.
- Kept existing automatic sensor OID generation behavior for backwards compatibility.

## 1.0

- Initial release
