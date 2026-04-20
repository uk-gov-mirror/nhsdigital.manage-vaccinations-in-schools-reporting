#!/bin/sh

set -euo pipefail

CONTAINER_IP=$(wget -qO- https://checkip.amazonaws.com)

export ROOT_URL=http://${CONTAINER_IP}:4000/reports
echo "ROOT_URL=${ROOT_URL}"
