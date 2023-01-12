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
           duneggd/Config/SAND_STT.cfg \
           duneggd/Config/SAND_GRAIN.cfg \
           duneggd/Config/TMS.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           -w World -o nd_hall_with_lar_tms_sand.gdml
fi

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
           duneggd/Config/SAND_STT.cfg \
           duneggd/Config/SAND_GRAIN.cfg \
           duneggd/Config/TMS.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetectorNoActive.cfg \
           -w World -o anti_fiducial_nd_hall_with_lar_tms_sand.gdml
fi



####################################################################### start of miniProduction area

# full hall with detectors for mini-production version 1. 
#There are three versions : 
#  1. LAr + GAr     (+ SAND), 
#  2. LAr + GArLite (+ SAND), 
#  3. LAr + TMS     (+ SAND)

if [ $option = "all" -o $option = "miniproduction1_gar" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/ND_ElevatorStruct.cfg \
           duneggd/Config/KLOE_with_3DST.cfg \
           duneggd/Config/KLOEEMCALO.cfg \
           duneggd/Config/ND_CraneRailStruct1.cfg \
           duneggd/Config/ND_CraneRailStruct2.cfg \
           duneggd/Config/ND_HallwayStruct.cfg \
           duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ND-GAr/ND-GAr-SPYv3_noTPC.cfg \
	   duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           -w World -o nd_hall_with_lar_gar_sand.gdml
fi

if [ $option = "all" -o $option = "miniproduction1_gar_nosand" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume_No_KLOE.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/ND_ElevatorStruct.cfg \
           duneggd/Config/ND_CraneRailStruct1.cfg \
           duneggd/Config/ND_CraneRailStruct2.cfg \
           duneggd/Config/ND_HallwayStruct.cfg \
           duneggd/Config/ND_CryoStruct.cfg \
           duneggd/Config/ND-GAr/ND-GAr-SPYv3_noTPC.cfg \
           duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           -w World -o nd_hall_with_lar_gar_nosand.gdml
fi

if [ $option = "all" -o $option = "miniproduction1_garlite" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/ND_ElevatorStruct.cfg \
           duneggd/Config/KLOE_with_3DST.cfg \
           duneggd/Config/KLOEEMCALO.cfg \
           duneggd/Config/ND_CraneRailStruct1.cfg \
           duneggd/Config/ND_CraneRailStruct2.cfg \
           duneggd/Config/ND_HallwayStruct.cfg \
           duneggd/Config/ND_CryoStruct.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           duneggd/Config/ND-GAr-Lite/MPD_Temporary_SPY_v3_IntegratedMuID.cfg \
           -w World -o nd_hall_with_lar_garlite_sand.gdml
fi

if [ $option = "all" -o $option = "miniproduction1_garlite_nosand" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume_No_KLOE.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/ND_ElevatorStruct.cfg \
           duneggd/Config/ND_CraneRailStruct1.cfg \
           duneggd/Config/ND_CraneRailStruct2.cfg \
           duneggd/Config/ND_HallwayStruct.cfg \
           duneggd/Config/ND_CryoStruct.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           duneggd/Config/ND-GAr-Lite/MPD_Temporary_SPY_v3_IntegratedMuID.cfg \
           -w World -o nd_hall_with_lar_garlite_nosand.gdml
fi

if [ $option = "all" -o $option = "miniproduction1_tms" ];
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
           duneggd/Config/SAND_STT.cfg \
           duneggd/Config/SAND_GRAIN.cfg \
           duneggd/Config/TMS.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           -w World -o nd_hall_with_lar_tms_sand.gdml
fi

if [ $option = "all" -o $option = "miniproduction1_tms_nosand" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume_LAr_TMS_noSAND.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/ND_ElevatorStruct.cfg \
           duneggd/Config/ND_CraneRailStruct1.cfg \
           duneggd/Config/ND_CraneRailStruct2.cfg \
           duneggd/Config/ND_HallwayStruct.cfg \
           duneggd/Config/ND_CryoStruct.cfg \
           duneggd/Config/TMS.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           -w World -o nd_hall_with_lar_tms_nosand.gdml
fi

#################################################################### end of miniProduction area

# build the full hall
if [ $option = "all" -o $option = "full" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/MPD_Concept_SPY_v2_IntegratedMuID.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   -w World -o nd_hall_with_dets.gdml
fi

if [ $option = "all" -o $option = "3DST_STT" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/ND_ElevatorStruct.cfg \
           duneggd/Config/KLOE_with_3DST_STT.cfg \
           duneggd/Config/KLOEEMCALO.cfg \
           duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
           duneggd/Config/ND_CraneRailStruct1.cfg \
           duneggd/Config/ND_CraneRailStruct2.cfg \
           duneggd/Config/ND_HallwayStruct.cfg \
           duneggd/Config/ND_CryoStruct.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           -w World -o nd_hall_with_3DST_STT.gdml
fi

# build a hall with no detectors
if [ $option = "all" -o $option = "empty" ];
then

gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_NoDets.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   -w World -o nd_hall_no_dets.gdml
fi

if [ $option = "all" -o $option = "lar" ];
then
# build a hall with only LAr
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_Only_LAr.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   -w World -o nd_hall_only_lar.gdml
fi
# anti-fiducial LAr
if [ $option = "all" -o $option = "lar_antifid" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_Only_LAr.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetectorNoActive.cfg \
	   -w World -o nd_hall_lar_antifid.gdml
fi

# MPD only
if [ $option = "all" -o $option = "mpd" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_Only_MPD.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   -w World -o nd_hall_only_mpd.gdml
fi

# MPD anti-fiducial
if [ $option = "all" -o $option = "mpd_antifid" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_Only_MPD.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/ND-GAr/ND-GAr-SPYv3_noTPC.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   -w World -o nd_hall_only_mpd_antifid.gdml
fi


# KLOE only
if [ $option = "all" -o $option = "kloe" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_Only_KLOE.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   -w World -o nd_hall_only_kloe.gdml
fi

# KLOE filled with STT
if [ $option = "all" -o $option = "kloe_sttonly" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume_Only_KLOE.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/ND_ElevatorStruct.cfg \
           duneggd/Config/KLOE_STTFULL.cfg \
           duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
           duneggd/Config/ND_CraneRailStruct1.cfg \
           duneggd/Config/ND_CraneRailStruct2.cfg \
           duneggd/Config/ND_HallwayStruct.cfg \
           duneggd/Config/ND_CryoStruct.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           -w World -o nd_hall_kloe_sttonly.gdml
fi

# KLOE filled with STT and LAr target
if [ $option = "all" -o $option = "kloe_sttlar" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume_Only_KLOE.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/KLOE_STTLAR.cfg \
           duneggd/Config/STTLAR.cfg \
           duneggd/Config/KLOEEMCALO.cfg \
           -w World -o nd_hall_kloe_sttLAr.gdml
fi

# SAND OPT 1
if [ $option = "sand_opt1" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/ND_ElevatorStruct.cfg \
           duneggd/Config/SAND_MAGNET.cfg \
           duneggd/Config/SAND_INNERVOLOPT1.cfg \
           duneggd/Config/SAND_ECAL.cfg \
           duneggd/Config/SAND_STT.cfg \
           duneggd/Config/SAND_GRAIN.cfg \
           duneggd/Config/ND_CraneRailStruct1.cfg \
           duneggd/Config/ND_CraneRailStruct2.cfg \
           duneggd/Config/ND_HallwayStruct.cfg \
           duneggd/Config/ND_CryoStruct.cfg \
           duneggd/Config/ND-GAr/ND-GAr-SPYv3_noTPC.cfg \
           duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           -w World -o SAND_opt1.gdml
fi

# SAND OPT 2
if [ $option = "all" -o $option = "sand_opt2" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/ND_ElevatorStruct.cfg \
           duneggd/Config/SAND_MAGNET.cfg \
           duneggd/Config/SAND_INNERVOLOPT2.cfg \
           duneggd/Config/SAND_ECAL.cfg \
           duneggd/Config/SAND_STT.cfg \
           duneggd/Config/SAND_GRAIN.cfg \
           duneggd/Config/ND_CraneRailStruct1.cfg \
           duneggd/Config/ND_CraneRailStruct2.cfg \
           duneggd/Config/ND_HallwayStruct.cfg \
           duneggd/Config/ND_CryoStruct.cfg \
           duneggd/Config/ND-GAr/ND-GAr-SPYv3_noTPC.cfg \
           duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           -w World -o SAND_opt2.gdml
fi

# KLOE anti-fiducial
if [ $option = "all" -o $option = "kloe_antifid" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_Only_KLOE.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_No_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   -w World -o nd_hall_only_kloe_antifid.gdml
fi

# LAr and MPD (No KLOE)
if [ $option = "all" -o $option = "lar_mpd" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_No_KLOE.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   -w World -o nd_hall_lar_mpd.gdml
fi

# LAr and MPD anti-fiducial (for MPD)
if [ $option = "all" -o $option = "lar_mpd_antifid" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
	   duneggd/Config/ND_Hall_Air_Volume_No_KLOE.cfg \
	   duneggd/Config/ND_Hall_Rock.cfg \
	   duneggd/Config/ND_ElevatorStruct.cfg \
	   duneggd/Config/KLOE_with_3DST.cfg \
	   duneggd/Config/KLOEEMCALO.cfg \
	   duneggd/Config/ND-GAr/ND-GAr-SPYv3_noTPC.cfg \
	   duneggd/Config/ND_CraneRailStruct1.cfg \
	   duneggd/Config/ND_CraneRailStruct2.cfg \
	   duneggd/Config/ND_HallwayStruct.cfg \
	   duneggd/Config/ND_CryoStruct.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	   -w World -o nd_hall_lar_mpd_antifid.gdml
fi

# LAr and TMS (No KLOE)
if [ $option = "all" -o $option = "lar_tms" ];
then
gegede-cli duneggd/Config/WORLDggd.cfg \
           duneggd/Config/ND_Hall_Air_Volume_LAr_TMS.cfg \
           duneggd/Config/ND_Hall_Rock.cfg \
           duneggd/Config/ND_ElevatorStruct.cfg \
           duneggd/Config/KLOE_with_3DST.cfg \
           duneggd/Config/KLOEEMCALO.cfg \
           duneggd/Config/TMS.cfg \
           duneggd/Config/ND_CraneRailStruct1.cfg \
           duneggd/Config/ND_CraneRailStruct2.cfg \
           duneggd/Config/ND_HallwayStruct.cfg \
           duneggd/Config/ND_CryoStruct.cfg \
           duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
           duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
           -w World -o nd_hall_lar_tms.gdml
fi

