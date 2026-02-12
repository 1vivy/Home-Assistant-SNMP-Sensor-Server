# Home Assistant Add-on: SNMP server

## Installation

From the supervisor add-on store, add the following repository:

https://github.com/darthsebulba04/hassio-addons

Then, in the new list of add-ons, install `SNMP Server`

## How to use

1. Set the `community` option, eg, `public`. Fill in the other options if you wish.
2. Set the port under network, eg, `161`.
3. Save the add-on configuration by clicking the "SAVE" button.
4. Start the add-on.

## Configuration

The SNMP server add-on can be changed to your likings. This section
covers each configuration option.

Example add-on configuration:

```yaml
community: public
location: Home
name: RPi
email: rpi@me.com
expose_sensors: true
sensors_to_expose: sensor.ef_*
enable_ups_oid_mapping: true
ups_oid_mappings: >-
  [{"oid":"1.3.6.1.2.1.33.1.2.4.0","entity_id":"sensor.ef_d32156_battery_level","snmp_type":"integer"}]
```

### Option: `community`

The community your SNMP monitor is looking for, e.g. `public`.

### Option: `location`

The SNMP location, e.g. `Home`.

### Option: `name`

The SNMP contact name, e.g. `RPi`.

### Option: `email`

The SNMP contact email address.

### Option: `expose_sensors`

Enable/disable automatic HA entity exposure through generated `extend` OIDs.

### Option: `expose_sensors_OID_base`

Reserved for compatibility with previous versions.

### Option: `sensors_to_expose`

Filter entity IDs for auto-generated `extend` OIDs. Supports comma-separated wildcards.

### Option: `enable_ups_oid_mapping`

Enables manual mapping of HA entities to UPS-MIB OIDs under `.1.3.6.1.2.1.33`.

### Option: `ups_oid_mappings`

JSON array with one object per mapped OID:

- `oid` (required)
- `entity_id` (required)
- `snmp_type` (optional; default `string`)
- `value_map` (optional object for enum translation)
- `scale` and `offset` (optional numeric transforms)
- `default_value` (optional fallback for unknown/unavailable)

## Support

In case you've found a bug, please [open an issue on my GitHub][issue].

[issue]: https://github.com/darthsebulba04/hassio-snmpd/issues
[repository]: https://github.com/darthsebulba04/hassio-snmpd/
