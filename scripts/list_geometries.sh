#!/usr/bin/env bash
# Print the GDML files that a make target (default: prod) will build, one per line.
#
# The generic build rule is `gegede-cli <configs> -w World -o <output>.gdml`, so a
# dry run of make reveals every geometry that would be generated.
#
# Usage: scripts/list_geometries.sh [make-target ...]
set -euo pipefail

if [ "$#" -eq 0 ]; then
  set -- prod
fi

make -n -B "$@" 2>/dev/null \
  | grep -oE -- '-o [^ ]+\.gdml' \
  | awk '{ print $2 }' \
  | sort -u
