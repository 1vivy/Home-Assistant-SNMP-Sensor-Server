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

if bashio::var.true "$(bashio::config 'expose_sensors')" || \
	bashio::var.true "$(bashio::config 'enable_ups_oid_mapping')" || \
	bashio::var.true "$(bashio::config 'ecoflow_ups_mode')"; then
	apk add py3-requests
fi

if bashio::var.true "$(bashio::config 'expose_sensors')"; then
	bashio::log.info "Generating OID for HA sensors.."
	OUTPUT=$(python3 snmpd-configurator.py "${CONFIG}" "$(bashio::config 'expose_sensors_OID_base')" "$(bashio::config 'sensors_to_expose')")
	bashio::log.info "${OUTPUT}"
fi

UPS_ENABLED=false
if bashio::var.true "$(bashio::config 'ecoflow_ups_mode')"; then
	bashio::log.info "Generating EcoFlow UPS mappings from device id.."
	ECOFLOW_DEVICE_ID="$(bashio::config 'ecoflow_device_id')"
	UPS_OID_MAPPINGS_RAW="$(bashio::config 'ups_oid_mappings')"
	if OUTPUT=$(python3 /generate-ecoflow-ups-mappings.py "${ECOFLOW_DEVICE_ID}" "${UPS_OID_MAPPINGS_RAW}" "${UPS_MAPPING_FILE}" 2>&1); then
		bashio::log.info "${OUTPUT}"
		UPS_ENABLED=true
	else
		bashio::log.error "Unable to generate EcoFlow UPS mappings: ${OUTPUT}"
	fi
elif bashio::var.true "$(bashio::config 'enable_ups_oid_mapping')"; then
	bashio::log.info "Configuring manual UPS OID mappings.."
	UPS_OID_MAPPINGS_RAW="$(bashio::config 'ups_oid_mappings')"
	if OUTPUT=$(python3 - "${UPS_OID_MAPPINGS_RAW}" "${UPS_MAPPING_FILE}" <<'PY' 2>&1
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
    if "oid" not in item:
        raise ValueError(f"mapping #{index} requires oid")
    if "entity_id" not in item and "entity_ids" not in item and "static_value" not in item:
        raise ValueError(f"mapping #{index} requires one of entity_id/entity_ids/static_value")

with open(output_path, "w", encoding="utf-8") as handle:
    json.dump(parsed, handle)

print(f"Loaded {len(parsed)} UPS mapping entries")
PY
	); then
		bashio::log.info "${OUTPUT}"
		UPS_ENABLED=true
	else
		bashio::log.error "Invalid ups_oid_mappings configuration. ${OUTPUT}"
	fi
fi

if [ "${UPS_ENABLED}" = "true" ]; then
	echo "pass .1.3.6.1.2.1.33 python3 /ups-snmp-pass.py" >> "${CONFIG}"
	export UPS_OID_MAPPINGS_FILE="${UPS_MAPPING_FILE}"
fi

bashio::log.info "Listening SNMP Sensor Server..."
exec /usr/sbin/snmpd \
	-c "${CONFIG}" \
	-f \
	< /dev/null
