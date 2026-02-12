# Changelog

## 1.5.0

- Added manual UPS OID mapping support (`enable_ups_oid_mapping` + `ups_oid_mappings`) to bind Home Assistant entities directly to UPS-MIB OIDs.
- Added value conversion options for mapped OIDs (`value_map`, `scale`, `offset`, and `default_value`) to support cases like EcoFlow plug state to `OL/OB`.
- Kept existing automatic sensor OID generation behavior for backwards compatibility.

## 1.0

- Initial release
