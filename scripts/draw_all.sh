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
$PYTHON $scriptname --view xz_zoom $@
$PYTHON $scriptname --view yz_zoom $@
$PYTHON $scriptname --view sand_top $@
$PYTHON $scriptname --view sand_side $@
$PYTHON $scriptname --view lar_side $@
$PYTHON $scriptname --view lar_top $@
$PYTHON $scriptname --view rock_top $@
$PYTHON $scriptname --view rock_side $@
$PYTHON $scriptname --view tms_side $@
$PYTHON $scriptname --view tms_top $@
$PYTHON $scriptname --view xz $@
$PYTHON $scriptname --view xz_wide $@
$PYTHON $scriptname --view yz $@
$PYTHON $scriptname --view yz_wide $@
