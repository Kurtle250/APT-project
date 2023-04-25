#!/bin/bash

# Example usage: ./entrypoint-wrap.sh -s <schema-file>
# Example usage: ./entrypoint-wrap.sh -s "/start/run/schema_decoder.cql"

export SEPARATOR="***************************************************************"

# Accepted args for user to pass
usage() {
  echo "${SEPARATOR}"
  echo "--(usage)-- Arguments"
  echo "-s 'path/to/schema.cql' "
  echo "--(usage)-- Example "
  echo "RUN      $0 -s '/start/run/schema_decoder.cql'"
  echo "HELP     $0 -h"
  echo ""
}

while getopts 's:h' option
do
  case "${option}" in
    s) SCHEMA_FILE=${OPTARG};;
    h) usage
    exit 1;;
   esac
done

if test -f "$SCHEMA_FILE"
then
  echo "--(info)-- Loading schema file: ${SCHEMA_FILE} "
else
  echo ""
  echo "--(error)-- Invalid argument: $0 -s ${SCHEMA_FILE}"
  echo ""
  usage;
  exit 1;
fi

# Load in database schemas as a background task
until CONFIGURE_DB_SCHEMA=$(cqlsh -u cassandra -p cassandra -f "${SCHEMA_FILE}"); do
    sleep 0.5
done &

# Postpone docker build until schemas are available to other docker containers (I.E background tasks are completed)
until echo "$CONFIGURE_DB_SCHEMA" | cqlsh; do
  echo "--(info)-- Waiting until schema has loaded into Cassandra: (${SCHEMA_FILE})"
  sleep 2
done &

exec /docker-entrypoint.sh "cassandra" "-f"
