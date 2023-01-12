# Dune-ND-GGD

This is a tool to build proposal geometries for DUNE near detector.

dunendggd is based on [GeGeDe](https://github.com/brettviren/gegede) and started out as [gyang9/dunendggd](https://github.com/gyang9/dunendggd).

# Setup

## Prerequisites

This package requires `gegede`.
Unfortunately, the latest version of `gegede` which supports Python 3 [is _not_ on PyPI](https://github.com/brettviren/gegede/issues/18) yet.
This means we have to install a suitable version directly from GitHub:

```bash
pip install git+https://github.com/brettviren/gegede.git@86ca28190516a23203cd883aafb0548a61664ceb
```

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

# Example
To run an example containing basic detectors, you could process like:
```bash
gegede-cli duneggd/Config/PRIMggd_example.cfg duneggd/Config/DETENCLOSURE-prim-only.cfg duneggd/Config/WORLDggd.cfg -w World -o example.gdml
```

To run a full example containing surrounded magnet
```bash
gegede-cli duneggd/Config/PRIMggd_example.cfg duneggd/Config/SECggd_example.cfg duneggd/Config/DETENCLOSURE.cfg duneggd/Config/WORLDggd.cfg -w World -o full_example.gdml
```

# Quick Visualization
To do a quick check or your geometry file you can use ROOT-CERN:
```bash
root -l 'geoDisplay.C("example.gdml")'
```

# Contact
- **dunendggd:** Package managers
  - Lukas Koch
  - Mathew Muether
- **GeGeDe:**
  - Brett Viren
