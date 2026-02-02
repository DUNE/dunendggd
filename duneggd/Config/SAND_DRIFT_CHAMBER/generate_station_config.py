import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q
import time

import argparse
import configparser

__CONFIG__ = "/storage/gpfs_data/neutrino/users/alrugger/Software/dunendggd/duneggd/Config"

def fill_uniform_from_CCH2_tgt_ratio(Space4Tracker,gen_cfg,**kwargs):
    print("\n>Generating with: fill_uniform_from_CCH2_tgt_ratio")
    
    station_lst = []
    idx = 0
    
    running_z = Q("0.0mm")
    
    while running_z < Space4Tracker:
        if idx % (gen_cfg["n_CH2_after_C"]+1) == 0:
            station_lst.append({"tgt_material" : "Graphite", "tgt_thickness":gen_cfg["C_tgt_thickness"], "n_views":gen_cfg["n_views"], "view_thickness":gen_cfg["view_thickness"]})
            running_z += gen_cfg["C_tgt_thickness"] + gen_cfg["n_views"] * gen_cfg["view_thickness"] + gen_cfg["clearanceStations"]
        else:
            station_lst.append({"tgt_material" : "C3H6", "tgt_thickness":gen_cfg["CH2_tgt_thickness"], "n_views":gen_cfg["n_views"], "view_thickness":gen_cfg["view_thickness"]})
            running_z += gen_cfg["CH2_tgt_thickness"] + gen_cfg["n_views"] * gen_cfg["view_thickness"] + gen_cfg["clearanceStations"]
        idx += 1
    return station_lst
       
    


def serialize_obj_to_cfg(obj):
    if isinstance(obj, Q): # find Q-type objects
        return f"Q('{obj.magnitude}{obj.units}')"
    elif isinstance(obj, dict):
        return "{" + ", ".join(
            f"'{k}': {serialize_obj_to_cfg(v)}" for k, v in obj.items()
        ) + "}"
    elif isinstance(obj, list):
        return "[" + ", ".join(serialize_obj_to_cfg(v) for v in obj) + "]" # unpack lists and dictionaries
    elif isinstance(obj, str):
        return repr(obj)
    else:
        return repr(obj)


def parse_script_args():
    # read the JSON config. file
    parser = argparse.ArgumentParser(
        description="Parse the Drift Chamber station configuration file"
    )
    parser.add_argument(
        "--config",
        required=False,
        type=str,
        help="Path to the parser config. file",
        default="station_gen_config.cfg"
    )
    parser.add_argument(
        "--save_path",
        required=False,
        type=str,
        help="Path to the parser config. file",
        default="."
    )
    print("> Parsed arguments", flush=True)
    return parser.parse_args()

if __name__ == "__main__":
    
    # pass the Q in the configuration files as gegede quantities
    namespace = {"Q": Q}
    # set a dictionary of generation options --> add new options here
    gen_mode_dict = {"fill_uniform_from_CCH2_tgt_ratio": fill_uniform_from_CCH2_tgt_ratio}
    
    # Read the generation algorithm configuration file
    args = parse_script_args()
    gen_cfg_file = args.config
    cfg_save_path = args.save_path
    print(f"> Generating station config from: {gen_cfg_file}")
    gen_config = configparser.ConfigParser()
    gen_config.read(gen_cfg_file)
    gen_config = gen_config["STATION_GEN_CFG"]
    
    gen_mode            = eval(gen_config["gen_mode"])
    
    # Read the opt3 configuration clearances (this should reasonably remain fixed)
    innervol_config = configparser.ConfigParser()
    innervol_config.read(f"{__CONFIG__}/SAND_INNERVOLOPTDRIFT1.cfg")
    innervol_config = innervol_config["SANDINNERVOLUME"]
    
    halfDimension = eval(innervol_config["halfDimension"],namespace)
    kloeVesselRadius           = halfDimension['rmax'] 
    kloeVesselHalfDx           = halfDimension['dz'] 
    GRAINThickness             = eval(innervol_config["GRAINThickness"],namespace)
    clearanceECALGRAIN         = eval(innervol_config["clearenceECALGRAIN"],namespace)
    clearanceGRAINTracker      = eval(innervol_config["clearenceGRAINTracker"],namespace)
    clearanceTrackerECAL       = eval(innervol_config["clearenceTrackerECAL"],namespace)
    
    print("\n>Inner volume parameters:")
    print(f" kloeVesselRadius: {kloeVesselRadius}")
    print(f" kloeVesselHalfDx: {kloeVesselHalfDx}")
    print(f" GRAINThickness: {GRAINThickness}")
    print(f" clearanceECALGRAIN: {clearanceECALGRAIN}")
    print(f" clearanceGRAINTracker: {clearanceGRAINTracker}")
    print(f" clearanceTrackerECAL: {clearanceTrackerECAL}")
    print("\n>Generation parameters")
    print(f" gen_mode: {gen_mode['name']}")
    print(f" clearanceStations: {gen_mode['clearanceStations']}")
    
    # compute the space available for the tracker along z
    Space4Tracker  = kloeVesselRadius * 2 - GRAINThickness - clearanceECALGRAIN - clearanceGRAINTracker - clearanceTrackerECAL
    print(f"\n>Length available for the tracker stations: {Space4Tracker}")
    
    # Run the generation
    stations_dict = gen_mode_dict[gen_mode['name']](Space4Tracker, gen_mode)
    
    # Save the configuration file
    station_config = configparser.ConfigParser()
    station_config["SAND_GENERIC_DRIFT_STATIONS"]={"clearanceStations": serialize_obj_to_cfg(gen_mode["clearanceStations"]), "stationDict": serialize_obj_to_cfg(stations_dict)}
    with open(f"{cfg_save_path}/TEST_DRIFT_STATIONS.cfg", "w") as f:
        station_config.write(f)
    
    