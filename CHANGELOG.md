# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to a modified version of [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Geometry releases will be tagged as `Descriptive_tag_v_X.Y.Z`.

## TMS geometry update from CDR to PDR

- Switch to 50 thin, 34 thick and 8 double thick steel planes with less material overburden in the y dimension
- Change the dimension of scintillator bars, the amount of bars per module and the number of modules per layer
- Introducing horizontal layer(X), currently in a vXuvXuv pattern with the first two layers being in front of the steel, while between the rest there is one layer of steel each in between
- Increasing the air gap size
- Double first layer of scintillator before the first layer of thin steel. There is also a layer of scintillator after the last layer of steel now

## [Unreleased]

- Nothing

## [TDR_Production_geometry_v_1.1.0]

### Changed

- Bump gegede to version 0.8.0
- Define default geometries in Makefile instead of bash script
- Implementation of the C-shaped volumes of the SAND ECAL Endcaps
- Change the NDLAr SensDet name from `TPCActive_shape` and `volTPCActive` to avoid inconsistency between prototype gdml and downstream configuration confusion
- Add ND-LAr only gdml configuration

### Removed

- Removed old gdml files from repo.
- Default geometry definitions that did not build (missing KLOE cfg file)

### Added
- Updated with standalone build of initial and complete STT configurations. `only_SAND_STT_Initial.gdml` `only_SAND_STT_Complete.gdml`
- generate complete ND geo with SAND provided with a Drift Chamber using target `sand_opt3_DRIFT1.gdml`

## [TDR_Production_geometry_v_1.0.3]

### Fixed

- Fixed use of TGeoManager::Import in scripts.

### Changed

- Changed drift length and ND gaps to reflect ND CAD gap lengths.
- `checkOverlaps.C` now takes an optional argument to choose the overlap checking method.
- CI now runs both types of overlap checks.

## [TDR_Production_geometry_v_1.0.2]

### Fixed

- Fixed Overlaps in TMS geometry.

### Changed
- `checkOverlaps.C` now uses sampling method.

## [TDR_Production_geometry_v_1.0.1]

### Changed

- Added production gdml with no LArActive to build script

## [TDR_Production_geometry_v_1.0]

### Changed

- Update `build_hall.sh` to build production geom with prod option
