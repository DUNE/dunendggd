.PHONY: clean all prod tms tms_nosand gar garlite empty sandopt

# Default
prod: tms tms_drift1

# Other options
all:  tms tms_drift1 tms_nosand gar_nosand garlite_nosand empty sandopt

tms: nd_hall_with_lar_tms_sand_stt1.gdml \
	anti_fiducial_nd_hall_with_lar_tms_sand_stt1.gdml

tms_drift1: nd_hall_with_lar_tms_sand_drift1.gdml \
	anti_fiducial_nd_hall_with_lar_tms_sand_drift1.gdml

tms_nosand: nd_hall_with_lar_tms_nosand.gdml

gar_nosand: nd_hall_with_lar_gar_nosand.gdml

garlite_nosand: nd_hall_with_lar_garlite_nosand.gdml

empty: nd_hall_no_dets.gdml

sandopt: SAND_opt3_STT1.gdml \
	SAND_opt3_DRIFT1.gdml \
	only_SAND_STT_Initial.gdml

lar_only: nd_hall_with_lar_only.gdml

clean:
	rm *.gdml

%.gdml:
	gegede-cli $^ -w World -o $@

nd_hall_with_lar_tms_sand_stt1.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume_LAr_TMS_SAND.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/ND_CraneRailStruct1.cfg \
	duneggd/Config/ND_CraneRailStruct2.cfg \
	duneggd/Config/ND_HallwayStruct.cfg \
	duneggd/Config/ND_CryoStruct.cfg \
	duneggd/Config/SAND_MAGNET.cfg \
	duneggd/Config/SAND_INNERVOLOPT3.cfg \
	duneggd/Config/SAND_ECAL.cfg \
	duneggd/Config/SAND_STT/STT1.cfg \
	duneggd/Config/SAND_GRAIN.cfg \
	duneggd/Config/TMS.cfg \
	duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	duneggd/Config/ArgonCube/ArgonCubeDetector.cfg

anti_fiducial_nd_hall_with_lar_tms_sand_stt1.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume_LAr_TMS_SAND.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/ND_CraneRailStruct1.cfg \
	duneggd/Config/ND_CraneRailStruct2.cfg \
	duneggd/Config/ND_HallwayStruct.cfg \
	duneggd/Config/ND_CryoStruct.cfg \
	duneggd/Config/SAND_MAGNET.cfg \
	duneggd/Config/SAND_INNERVOLOPT3.cfg \
	duneggd/Config/SAND_ECAL.cfg \
	duneggd/Config/SAND_STT/STT1.cfg \
	duneggd/Config/SAND_GRAIN.cfg \
	duneggd/Config/TMS.cfg \
	duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	duneggd/Config/ArgonCube/ArgonCubeDetectorNoActive.cfg

nd_hall_with_lar_tms_sand_drift1.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume_LAr_TMS_SAND.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/ND_CraneRailStruct1.cfg \
	duneggd/Config/ND_CraneRailStruct2.cfg \
	duneggd/Config/ND_HallwayStruct.cfg \
	duneggd/Config/ND_CryoStruct.cfg \
	duneggd/Config/SAND_MAGNET.cfg \
	duneggd/Config/SAND_INNERVOLOPTDRIFT1.cfg \
	duneggd/Config/SAND_ECAL.cfg \
	duneggd/Config/SAND_DRIFT_CHAMBER/DRIFT1.cfg \
	duneggd/Config/SAND_GRAIN.cfg \
	duneggd/Config/TMS.cfg \
	duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	duneggd/Config/ArgonCube/ArgonCubeDetector.cfg

anti_fiducial_nd_hall_with_lar_tms_sand_drift1.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume_LAr_TMS_SAND.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/ND_CraneRailStruct1.cfg \
	duneggd/Config/ND_CraneRailStruct2.cfg \
	duneggd/Config/ND_HallwayStruct.cfg \
	duneggd/Config/ND_CryoStruct.cfg \
	duneggd/Config/SAND_MAGNET.cfg \
	duneggd/Config/SAND_INNERVOLOPTDRIFT1.cfg \
	duneggd/Config/SAND_ECAL.cfg \
	duneggd/Config/SAND_DRIFT_CHAMBER/DRIFT1.cfg \
	duneggd/Config/SAND_GRAIN.cfg \
	duneggd/Config/TMS.cfg \
	duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	duneggd/Config/ArgonCube/ArgonCubeDetectorNoActive.cfg

nd_hall_with_lar_only.gdml: duneggd/Config/WORLDggd.cfg \
        duneggd/Config/ND_Hall_Air_Volume_Only_LArDet.cfg \
        duneggd/Config/ND_Hall_Rock.cfg \
        duneggd/Config/ND_CryoStruct.cfg \
        duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
        duneggd/Config/ArgonCube/ArgonCubeDetector.cfg

nd_hall_with_lar_tms_nosand.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume_LAr_TMS_noSAND.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/ND_CraneRailStruct1.cfg \
	duneggd/Config/ND_CraneRailStruct2.cfg \
	duneggd/Config/ND_HallwayStruct.cfg \
	duneggd/Config/ND_CryoStruct.cfg \
	duneggd/Config/TMS.cfg \
	duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	duneggd/Config/ArgonCube/ArgonCubeDetector.cfg

nd_hall_with_lar_gar_nosand.gdml: duneggd/Config/WORLDggd.cfg \
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
	duneggd/Config/ArgonCube/ArgonCubeDetector.cfg

nd_hall_with_lar_garlite_nosand.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume_No_KLOE.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/ND_CraneRailStruct1.cfg \
	duneggd/Config/ND_CraneRailStruct2.cfg \
	duneggd/Config/ND_HallwayStruct.cfg \
	duneggd/Config/ND_CryoStruct.cfg \
	duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
	duneggd/Config/ND-GAr-Lite/MPD_Temporary_SPY_v3_IntegratedMuID.cfg

SAND_opt1_STT1.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/SAND_MAGNET.cfg \
	duneggd/Config/SAND_INNERVOLOPT1.cfg \
	duneggd/Config/SAND_ECAL.cfg \
	duneggd/Config/SAND_STT/STT1.cfg \
	duneggd/Config/SAND_GRAIN.cfg \
	duneggd/Config/ND_CraneRailStruct1.cfg \
	duneggd/Config/ND_CraneRailStruct2.cfg \
	duneggd/Config/ND_HallwayStruct.cfg \
	duneggd/Config/ND_CryoStruct.cfg \
	duneggd/Config/ND-GAr/ND-GAr-SPYv3_noTPC.cfg \
	duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
	duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	duneggd/Config/ArgonCube/ArgonCubeDetector.cfg

SAND_opt2_STT1.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/SAND_MAGNET.cfg \
	duneggd/Config/SAND_INNERVOLOPT2.cfg \
	duneggd/Config/SAND_ECAL.cfg \
	duneggd/Config/SAND_STT/STT1.cfg \
	duneggd/Config/SAND_GRAIN.cfg \
	duneggd/Config/ND_CraneRailStruct1.cfg \
	duneggd/Config/ND_CraneRailStruct2.cfg \
	duneggd/Config/ND_HallwayStruct.cfg \
	duneggd/Config/ND_CryoStruct.cfg \
	duneggd/Config/ND-GAr/ND-GAr-SPYv3_noTPC.cfg \
	duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
	duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	duneggd/Config/ArgonCube/ArgonCubeDetector.cfg

SAND_opt2_STT3.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/SAND_MAGNET.cfg \
	duneggd/Config/SAND_INNERVOLOPT2.cfg \
	duneggd/Config/SAND_ECAL.cfg \
	duneggd/Config/SAND_STT/STT3.cfg \
	duneggd/Config/SAND_GRAIN.cfg \
	duneggd/Config/ND_CraneRailStruct1.cfg \
	duneggd/Config/ND_CraneRailStruct2.cfg \
	duneggd/Config/ND_HallwayStruct.cfg \
	duneggd/Config/ND_CryoStruct.cfg \
	duneggd/Config/ND-GAr/ND-GAr-SPYv3_noTPC.cfg \
	duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
	duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	duneggd/Config/ArgonCube/ArgonCubeDetector.cfg

SAND_opt3_STT1.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/SAND_MAGNET.cfg \
	duneggd/Config/SAND_INNERVOLOPT3.cfg \
	duneggd/Config/SAND_ECAL.cfg \
	duneggd/Config/SAND_STT/STT1.cfg \
	duneggd/Config/SAND_GRAIN.cfg \
	duneggd/Config/ND_CraneRailStruct1.cfg \
	duneggd/Config/ND_CraneRailStruct2.cfg \
	duneggd/Config/ND_HallwayStruct.cfg \
	duneggd/Config/ND_CryoStruct.cfg \
	duneggd/Config/ND-GAr/ND-GAr-SPYv3_noTPC.cfg \
	duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
	duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	duneggd/Config/ArgonCube/ArgonCubeDetector.cfg


SAND_opt3_DRIFT1.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/SAND_MAGNET.cfg \
	duneggd/Config/SAND_INNERVOLOPTDRIFT1.cfg \
	duneggd/Config/SAND_ECAL.cfg \
	duneggd/Config/SAND_DRIFT_CHAMBER/DRIFT1.cfg \
	duneggd/Config/SAND_GRAIN.cfg \
	duneggd/Config/ND_CraneRailStruct1.cfg \
	duneggd/Config/ND_CraneRailStruct2.cfg \
	duneggd/Config/ND_HallwayStruct.cfg \
	duneggd/Config/ND_CryoStruct.cfg \
	duneggd/Config/ND-GAr/ND-GAr-SPYv3_noTPC.cfg \
	duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
	duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
	duneggd/Config/ArgonCube/ArgonCubeDetector.cfg

only_SAND_DRIFT.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume_Only_SAND.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/SAND_MAGNET.cfg \
	duneggd/Config/SAND_INNERVOLOPTDRIFT1.cfg \
	duneggd/Config/SAND_ECAL.cfg \
	duneggd/Config/SAND_DRIFT_CHAMBER/DRIFT1.cfg \
	duneggd/Config/SAND_GRAIN.cfg

only_SAND_STT_Initial.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume_Only_SAND.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/SAND_MAGNET.cfg \
	duneggd/Config/SAND_INNERVOLOPT_BackupSTT.cfg \
	duneggd/Config/SAND_ECAL.cfg \
	duneggd/Config/SAND_STT/STT_Backup.cfg \
	duneggd/Config/SAND_GRAIN.cfg 

only_SAND_STT_Complete.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume_Only_SAND.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/SAND_MAGNET.cfg \
	duneggd/Config/SAND_INNERVOLOPT_DefaultSTT.cfg \
	duneggd/Config/SAND_ECAL.cfg \
	duneggd/Config/SAND_STT/STT_Default.cfg \
	duneggd/Config/SAND_GRAIN.cfg 


OUTPUT_DIR ?= ./
GENERIC_DRIFT_STATIONS_CFG ?= duneggd/Config/SAND_DRIFT_CHAMBER/TEST_DRIFT_STATIONS.cfg
only_SAND_DRIFT_GENERIC.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume_Only_SAND.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/SAND_MAGNET.cfg \
	duneggd/Config/SAND_INNERVOLOPTDRIFT1.cfg \
	duneggd/Config/SAND_ECAL.cfg \
	$(GENERIC_DRIFT_STATIONS_CFG) \
	duneggd/Config/SAND_DRIFT_CHAMBER/DRIFT_generic.cfg \
	duneggd/Config/SAND_GRAIN.cfg
	gegede-cli -o $(OUTPUT_DIR)/$@ $^


nd_hall_no_dets.gdml: duneggd/Config/WORLDggd.cfg \
	duneggd/Config/ND_Hall_Air_Volume_NoDets.cfg \
	duneggd/Config/ND_Hall_Rock.cfg \
	duneggd/Config/ND_ElevatorStruct.cfg \
	duneggd/Config/ND_CraneRailStruct1.cfg \
	duneggd/Config/ND_CraneRailStruct2.cfg \
	duneggd/Config/ND_HallwayStruct.cfg \
	duneggd/Config/ND_CryoStruct.cfg

nd_hall_with_lar_tms_sand_old_window.gdml: duneggd/Config/WORLDggd.cfg \
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
	duneggd/Config/ArgonCube/ArgonCubeCryostatOldWindow.cfg \
	duneggd/Config/ArgonCube/ArgonCubeDetector.cfg
