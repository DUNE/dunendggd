# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to a modified version of [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Geometry releases will be tagged as `Descriptive_tag_v_X.Y.Z`.
-Standard method and sampling method have been integrated to overlaps of geometry.
## [Unreleased]

## Fixed

- Fixed use of TGeoManager::Import in scripts.

## [TDR_Production_geometry_v_1.0.2]

## Fixed

- Fixed Overlaps in TMS geometry.

## Changed
- `checkOverlaps.C` now uses sampling method.
- `checkOverlaps.C` now takes an optional argument to choose the overlap checking method. 

## [TDR_Production_geometry_v_1.0.1]

### Changed

- Added production gdml with no LArActive to build script

## [TDR_Production_geometry_v_1.0]

### Changed

- Update `build_hall.sh` to build production geom with prod option
