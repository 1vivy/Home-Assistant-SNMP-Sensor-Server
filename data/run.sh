#!/usr/bin/with-contenv bashio

bashio::log.info "Preparing SNMP Sensor Server, please wait.."
CONFIG="/etc/snmp/snmpd.conf"
UPS_MAPPING_FILE="/tmp/ups-oid-mappings.json"

{
	echo "com2sec readonly default $(bashio::config 'community')"
	echo "syslocation $(bashio::config 'location')"
	echo "syscontact $(bashio::config 'name') <$(bashio::config 'email')>"
	echo "group MyROGroup v2c readonly"
	echo "view all included .1 80"
	echo "access MyROGroup ''      any       noauth    exact  all    none   none"
} > "${CONFIG}"


if bashio::var.true "$(bashio::config 'expose_sensors')" || bashio::var.true "$(bashio::config 'enable_ups_oid_mapping')"; then
	apk add py3-requests
fi

if bashio::var.true "$(bashio::config 'expose_sensors')"; then
	bashio::log.info "Generating OID for HA sensors.."
	OUTPUT=$(python3 snmpd-configurator.py "${CONFIG}" "$(bashio::config 'expose_sensors_OID_base')" "$(bashio::config 'sensors_to_expose')")
	bashio::log.info "${OUTPUT}"
fi

if bashio::var.true "$(bashio::config 'enable_ups_oid_mapping')"; then
	bashio::log.info "Configuring manual UPS OID mappings.."
	UPS_OID_MAPPINGS_RAW="$(bashio::config 'ups_oid_mappings')"
	if python3 - "$UPS_OID_MAPPINGS_RAW" "$UPS_MAPPING_FILE" <<'PY'
import json
import sys

mappings_raw = sys.argv[1]
output_path = sys.argv[2]

if not mappings_raw.strip():
    parsed = []
else:
    parsed = json.loads(mappings_raw)

if not isinstance(parsed, list):
    raise ValueError("ups_oid_mappings must be a JSON array")

for index, item in enumerate(parsed, start=1):
    if not isinstance(item, dict):
        raise ValueError(f"mapping #{index} is not an object")
    if "oid" not in item or "entity_id" not in item:
        raise ValueError(f"mapping #{index} requires oid and entity_id")

with open(output_path, "w", encoding="utf-8") as handle:
    json.dump(parsed, handle)

print(f"Loaded {len(parsed)} UPS mapping entries")
PY
	then
		echo "pass .1.3.6.1.2.1.33 python3 /ups-snmp-pass.py" >> "${CONFIG}"
		export UPS_OID_MAPPINGS_FILE="${UPS_MAPPING_FILE}"
	else
		bashio::log.error "Invalid ups_oid_mappings configuration. Skipping UPS OID mapping support."
	fi
fi

bashio::log.info "Listening SNMP Sensor Server..."
exec /usr/sbin/snmpd \
	-c "${CONFIG}" \
	-f \
	< /dev/null
