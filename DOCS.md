# Home Assistant Add-on: SNMP server

## Installation

From the supervisor add-on store, add the following repository:

https://github.com/darthsebulba04/hassio-addons

Then, in the new list of add-ons, install `SNMP Server`

## How to use

1. Set the `community` option, e.g. `public`.
2. Set the port under network, e.g. `161`.
3. Save the add-on configuration by clicking the "SAVE" button.
4. Start the add-on.

## Configuration

Example add-on configuration (EcoFlow mode):

```yaml
community: public
location: Home
name: RPi
email: rpi@me.com
ecoflow_ups_mode: true
ecoflow_device_id: d32156
```

### Option: `ecoflow_ups_mode`

Enable device-id driven UPS mapping generation for `ha-ef-ble` entities.

### Option: `ecoflow_device_id`

Single EcoFlow device id (for example `d32156`). This is used to build entity IDs such as `sensor.ef_d32156_output_power`.

### Option: `ups_oid_mappings`

Advanced JSON override list. Use this if you need to override/extend generated mappings. In EcoFlow mode, manual entries win on OID conflicts.

### Option: `enable_ups_oid_mapping`

Legacy/manual mode. Enables manual mapping without EcoFlow auto-generation.

### Option: `expose_sensors`

Enable/disable automatic HA entity exposure through generated `extend` OIDs.

### Option: `sensors_to_expose`

Filter entity IDs for auto-generated `extend` OIDs. Supports comma-separated wildcards.

## EcoFlow auto-generated UPS OIDs

When enabled, the add-on generates practical UPS-MIB mappings under `.1.3.6.1.2.1.33`:

- `1.3.6.1.2.1.33.1.1.2.0` => static model string
- `1.3.6.1.2.1.33.1.1.5.0` => static device name string
- `1.3.6.1.2.1.33.1.2.4.0` => battery level percent
- `1.3.6.1.2.1.33.1.4.1.0` => output source (normal vs battery from plug state)
- `1.3.6.1.2.1.33.1.4.4.1.4.1` => output power

Plug state behavior is mapped as requested:

- plug `on` => normal line (`OL` behavior)
- plug `off` => on battery (`OB` behavior)

## Support

In case you've found a bug, please [open an issue on my GitHub][issue].

[issue]: https://github.com/darthsebulba04/hassio-snmpd/issues
[repository]: https://github.com/darthsebulba04/hassio-snmpd/
