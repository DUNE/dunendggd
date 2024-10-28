#! /bin/bash

# use the first argument to indicate what we should build
# if no argument build everything
option=$1

if [ -z $option ];
then
  option="prod"
fi


####################################################################### start of Production area
# full hall with detectors for mini-production version 1. 

###FULL HALL
if [ $option = "all" -o $option = "prod" -o $option = "production1_tms" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_Only_LAr.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           -w World -o nd_hall_only_lar.gdml
fi



# duneggd/Config/TMS.cfg \

: '
## No active LAR (Anti-fiducial)
if [ $option = "all" -o $option = "prod" -o $option = "production1_tms" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume_LAr_TMS_SAND.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/ND_ElevatorStruct.cfg \
           duneggd/Config/ND_CraneRailStruct1.cfg \
           duneggd/Config/ND_CraneRailStruct2.cfg \
           duneggd/Config/ND_HallwayStruct.cfg \
           duneggd/Config/ND_CryoStruct.cfg \
           duneggd/Config/SAND_MAGNET.cfg \
           duneggd/Config/SAND_INNERVOLOPT2.cfg \
           duneggd/Config/SAND_ECAL.cfg \
           duneggd/Config/SAND_STT/STT1.cfg \
           duneggd/Config/SAND_GRAIN.cfg \
           duneggd/Config/TMS.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetectorNoActive.cfg \
           -w World -o anti_fiducial_nd_hall_with_lar_tms_sand.gdml
fi

'
