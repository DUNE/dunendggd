scriptname=draw_geometry.py
if [[ $# -eq 0 ]] || [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
  echo "Usage ./draw_all.sh --filename <gdml file> + any additional args"
  echo "Automatically draws all default views"
  echo "Here's the output of python $scriptname --help:"
  python $scriptname --help
  exit 0
fi
python $scriptname --view xz_zoom $@
python $scriptname --view yz_zoom $@
python $scriptname --view sand_top $@
python $scriptname --view sand_side $@
python $scriptname --view lar_side $@
python $scriptname --view lar_top $@
python $scriptname --view rock_top $@
python $scriptname --view rock_side $@
python $scriptname --view tms_side $@
python $scriptname --view tms_top $@
python $scriptname --view xz $@
python $scriptname --view xz_wide $@
python $scriptname --view yz $@
python $scriptname --view yz_wide $@
