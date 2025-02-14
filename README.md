# Dune-ND-GGD

This is a tool to build proposal geometries for DUNE near detector.

dunendggd is based on [GeGeDe](https://github.com/brettviren/gegede) and started out as [gyang9/dunendggd](https://github.com/gyang9/dunendggd).

# Setup

## Installing dunendggd

This package can be installed as user using `pip`:

```bash
pip install -e .
```

Or if you do not have pip on your system and do not want to install it:

```bash
python setup.py develop --user
```

With root privileges:
```bash
python setup.py develop
```

Don't forget to check your variable `PATH`:
```bash
export PATH=~/.local/bin/:${PATH}
```

# Building default geometries

The default geometries are defined in the `Makefile`. To build them just invoke
```bash
make prod
```

Have a look in the `Makefile` to see what kind of geometries are defined there.

Hint: The `nosand` geometries build much, _much_ faster than the geometries
including the `sand` detector.

# Quick Visualization
To do a quick check or your geometry file you can use ROOT-CERN:
```bash
root -l 'geoDisplay.C("example.gdml")'
```

# Online Visualization

You can also use the JSROOT webpage on https://dune.github.io/dunendggd/ to
visualize a geometry. That page should already contain the default geometries
from the last CI test, but you can also upload root files containing geometries
yourself. You can use the `gdml2root.C` macro to convert gdml files to root
files.

# Checking for overlaps

You can use the following macro to check a generated geometries for overlaps:

```
root -q -b "checkOverlaps.C(\"geometry.gdml\", 0)"
root -q -b "checkOverlaps.C(\"geometry.gdml\", 1)"
```

The last argument determines the algorithm used for the check. You should run
both to be sure that there really are no overlaps.

# Checking geometry positions

The macro `locateVolume.C` can be used to check positions of volumes in the
global coordinate system:

```
$ root -b -q 'locateVolume.C("nd_hall_with_lar_tms_sand.gdml", "volWorld/rockBox_lv_0/volDetEnclosure_0/volTMS_0/thinlayervol_0/thinvolTMS_0")'
   ------------------------------------------------------------------
  | Welcome to ROOT 6.30/04                        https://root.cern |
  | (c) 1995-2024, The ROOT Team; conception: R. Brun, F. Rademakers |
  | Built for linuxx8664gcc on Feb 03 2024, 23:12:12                 |
  | From tags/v6-30-04@v6-30-04                                      |
  | With c++ (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0                   |
  | Try '.help'/'.?', '.demo', '.license', '.credits', '.quit'/'.q'  |
   ------------------------------------------------------------------


Processing locateVolume.C("nd_hall_with_lar_tms_sand.gdml", "volWorld/rockBox_lv_0/volDetEnclosure_0/volTMS_0/thinlayervol_0/thinvolTMS_0")...
== Loading Geometry ==
== Switching to volume path: volWorld/rockBox_lv_0/volDetEnclosure_0/volTMS_0/thinlayervol_0/thinvolTMS_0 ==
== Volume information ==
== Volume: thinvolTMS type TGeoVolume positioned 2 times
*** Shape boxTMS: TGeoBBox ***
    dX =    87.45000
    dY =   251.10000
    dZ =     0.75000
    origin: x=    0.00000 y=    0.00000 z=    0.00000
Mixture SteelTMS    Aeff=55.7025 Zeff=25.938 rho=7.85 radlen=1.7654 intlen=16.9869 index=41
   Element #0 : C  Z=  6.00 A= 12.01 w= 0.000
   Element #1 : FE  Z= 26.00 A= 55.84 w= 0.995
   Element #2 : SI  Z= 14.00 A= 28.09 w= 0.004
== Node information ==
OBJ: TGeoNodeMatrix	thinvolTMS_0
== Matrix information ==
matrix global_5 - tr=1  rot=1  refl=0  scl=0 shr=0 reg=0 own=0
  1.000000    0.000000    0.000000    Tx = -264.350000
  0.000000    1.000000    0.000000    Ty = -135.223000
  0.000000    0.000000    1.000000    Tz = 1139.550000
```

The Volume information tells us the shape and size of the volume, as well as
its material. The matrix information tells us the rotation and translation of
the volume in the global coordinate system.

You can use any of the visualisation methods above to browse the geometry and
find the paths to the volumes you want to inspect.

Currently this does _not_ work copies of volumes ending with `#<some_number>`.

# Contact
- **dunendggd:** Package managers
  - Lukas Koch
  - Mathew Muether
- **GeGeDe:**
  - Brett Viren
