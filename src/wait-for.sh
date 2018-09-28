#!/bin/bash

set -e

url="$1"
shift
cmd="$@"

until wget -O- "$url"; do
  >&2 echo "URL is unavailable - sleeping"
  sleep 1
done

>&2 echo "URL is up - executing command"
exec $cmd
