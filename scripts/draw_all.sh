#!/bin/bash
scriptname=draw_geometry.py

# Get python to use
if which root-framework.pyroot 1>/dev/null 2>/dev/null
then
    # Use SNAP package root if available
    PYTHON=root-framework.pyroot
else
    # Default to `python`
    PYTHON=python
fi

if [[ $# -eq 0 ]] || [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
  echo "Usage ./draw_all.sh --filename <gdml file> + any additional args"
  echo "Automatically draws all default views"
  echo "Here's the output of $PYTHON $scriptname --help:"
  $PYTHON $scriptname --help
  exit 0
fi

xargs <<EOF -I {} -P $(nproc) $PYTHON $scriptname --view {} $@
xz_zoom
yz_zoom
sand_top
sand_side
lar_side
lar_top
rock_top
rock_side
tms_side
tms_top
xz
xz_wide
yz
yz_wide
EOF
