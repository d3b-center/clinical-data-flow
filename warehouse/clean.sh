#! /bin/bash

set -eo pipefail

docker-compose down
rm -rf "$WAREHOUSE_DATA"
rm -rf "$MB_DATA"
