<br />
<center>
  <a href="https://github.com/PecceG2/StudioLED">
    <img src="https://raw.githubusercontent.com/PecceG2/Home-Assistant-SNMP-Sensor-Server/main/icon.png" alt="Logo" width="80" height="80">
  </a>

<p align="center">
  <h3 align="center">Home Assistant SNMP Sensor Server</h3>


  <img align="center">
    HA Add-on to expose the different sensors, entities and objects via SNMP automatically.</br>
    It provides monitoring of the system, hardware and HA integrations via external monitoring software like LibreNMS or Nagios.
    <br />
    <br />
    <a href="https://github.com/PecceG2/"><strong>View my projects »</strong></a>
    <br />
    <br />
    <a href="https://github.com/PecceG2/Home-Assistant-SNMP-Sensor-Server/issues">Report a Bug</a>
    ·
    <a href="https://github.com/PecceG2/Home-Assistant-SNMP-Sensor-Server/blob/master/LICENSE.md">View License</a>
    ·
    <a href="https://github.com/PecceG2/Home-Assistant-SNMP-Sensor-Server/issues">Request Feature</a>
  </p>
</p>

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield] ![Supports armhf Architecture][armhf-shield] ![Supports armv7 Architecture][armv7-shield] ![Supports i386 Architecture][i386-shield]

</center>

**Installation**
---

1. In your HA panel, go to `Configuration` -> `Add-ons, Backup & supervisor`.
2. In the lower right corner, click on `Add-on Store` button.
3. Go to the `three dots` on the top right screen and open `Repositories`.
4. Copy and paste this link in Add box, and press "Add" button:
`https://github.com/PecceG2/Home-Assistant-SNMP-Sensor-Server`
5. Close Add-on pop-up, refresh the page with F5 and go to `Configuration` -> `Add-ons, Backup & supervisor`.
6. Find "SNMP Sensor Server" add-on and install it.

**Configuration and usage**
---

### Auto-generated sensor OIDs

The add-on can auto-generate OIDs for Home Assistant entities using `extend` entries (legacy behavior).

### EcoFlow UPS mode (intended usage with ha-ef-ble)

This repository is now optimized for `ha-ef-ble` usage.

When `ecoflow_ups_mode` is enabled, you only provide one device id (example: `d32156`) and the add-on auto-generates practical UPS-MIB mappings under `.1.3.6.1.2.1.33`.

```yaml
ecoflow_ups_mode: true
ecoflow_device_id: d32156
```

Auto-mapped OIDs include:

- `1.3.6.1.2.1.33.1.1.2.0` (`upsIdentModel`) static `EcoFlow BLE`
- `1.3.6.1.2.1.33.1.1.5.0` (`upsIdentName`) static `EcoFlow <device_id>`
- `1.3.6.1.2.1.33.1.2.4.0` (`upsEstimatedChargeRemaining`) from `sensor.ef_<id>_battery_level` (fallback `main_battery_level`)
- `1.3.6.1.2.1.33.1.4.1.0` (`upsOutputSource`) from plug state (`on` => normal/OL, `off` => battery/OB)
- `1.3.6.1.2.1.33.1.4.4.1.4.1` (`upsOutputPower`) from `sensor.ef_<id>_output_power`

### Manual UPS OID mapping (advanced override)

`ups_oid_mappings` remains available for custom OIDs and manual overrides. If `ecoflow_ups_mode` is enabled, manual entries override auto-generated entries by OID.

<br />

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg

This is a modification of the original [darthsebulba04 project](https://github.com/darthsebulba04/hassio-snmpd/) under the MIT license to add sensor functionality and HA control via SNMP.
