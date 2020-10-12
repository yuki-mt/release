#!/bin/bash
set -eu

cd `dirname $0`/..

docker exec <container_name> conda env export -n base > conda.yaml
