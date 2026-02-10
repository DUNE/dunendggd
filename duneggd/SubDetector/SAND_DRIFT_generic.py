import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q
import time

class GenericDRIFTBuilder(gegede.builder.Builder):
    
    def configure(self,
                # sand inner volume info
                configuration = None,tracker_configuration=None, nBarrelModules = None, halfDimension = None, Material = None, GRAINThickness = None, 
                clearenceECALGRAIN = None, clearenceGRAINTracker = None, clearenceTrackerECAL = None, clearanceStations = None,
                # station commons
                frameThickness = None, frameMaterial = None, driftGas = None, MylarThickness=None,
                # tracker stations
                stationDict = None,
                **kwds):
        
            # Non-STT info: clearances and ECAL modules
            self.configuration              = configuration
            self.tracker_configuration      = tracker_configuration
            self.nBarrelModules             = nBarrelModules
            self.rotAngle                   = 0.5 * Q('360deg') / self.nBarrelModules
            self.halfDimension, self.Material = ( halfDimension, Material )
            self.kloeVesselRadius           = self.halfDimension['rmax'] #= Q('2m')
            self.kloeVesselHalfDx           = self.halfDimension['dz'] #= Q('1.69m')
            self.GRAINThickness             = GRAINThickness
            self.clearenceECALGRAIN         = clearenceECALGRAIN
            self.clearenceGRAINTracker      = clearenceGRAINTracker
            
            self.clearenceTrackerECAL       = clearenceTrackerECAL
            self.clearanceStations          = clearanceStations

            # station common info (assumed to be constant)
            self.frameThickness             = frameThickness
            self.frameMaterial              = frameMaterial
            self.driftGas                   = driftGas
            self.MylarThickness             = MylarThickness
            
            # station info dictionary (reasonably station-wise customisable parameters)
            self.stationDict                = stationDict

    def init(self):

            # self.GetModThickness            = lambda mod_type : self.targetThickness[mod_type] + self.NofDriftModules * self.DriftModuleThickness + (self.NofDriftModules + 1) * self.MylarThickness

            # self.ModThickness               = {"CMod" : self.GetModThickness("CMod"), "C3H6Mod" : self.GetModThickness("C3H6Mod"), "TrkMod" : self.GetModThickness("TrkMod")}

            # self.SuperModThickness          = self.ModThickness["CMod"] + self.ModThickness["C3H6Mod"] * self.nofC3H6ModAfterCMod# + self.clearenceSupermods 

            self.TrackerAvailableRadius     = self.kloeVesselRadius - self.clearenceTrackerECAL
            
            self.Space4Tracker              = self.kloeVesselRadius * 2 - self.GRAINThickness - self.clearenceECALGRAIN - self.clearenceGRAINTracker - self.clearenceTrackerECAL

            # self.nofSuperMods               = int((self.Space4Tracker / (self.SuperModThickness + self.clearenceSupermods)).to_base_units().magnitude)

            self.PrintRecap()

    def PrintRecap(self):   

            print("")
            print("*"*20 + f" INNERVOLUME CONFIGURATION {self.configuration}" +" "+"*"*20)
            print("*"*20 + f" TRACKER CONFIGURATION {self.tracker_configuration}" +" "+"*"*20)
            print("")
            print("_"*20+" INNERVOLUME INFO "+"_"*20)
            print("")
            print("SAND radius                    | "+str(self.kloeVesselRadius))
            print("SAND half Dx                   | "+str(self.kloeVesselHalfDx))
            print("GRAINThickness                 | "+str(self.GRAINThickness))
            print("clearance GRAIN-ECAL           | "+str(self.clearenceECALGRAIN))
            print("clearance GRAIN-tracker        | "+str(self.clearenceGRAINTracker))
            print("clearance tracker-ECAL         | "+str(self.clearenceTrackerECAL))
            print("clearance stations            | "+str(self.clearanceStations))
            print("Space 4 Tracker                | "+str(self.Space4Tracker))
            print("")


    def construct(self, geom):

        self.init()

        main_lv = self.constructTracker(geom)

        self.add_volume( main_lv )
        
        
    def constructTracker(self, geom):

        whole_shape         = geom.shapes.PolyhedraRegular("whole_shape_for_tracker", numsides = self.nBarrelModules, rmin = Q('0cm'), rmax = self.kloeVesselRadius , dz = self.kloeVesselHalfDx, sphi = self.rotAngle)

        upstream_shape      = geom.shapes.Box("upstream_shape_for_tracker", dx = (self.GRAINThickness + self.clearenceECALGRAIN + self.clearenceGRAINTracker)*0.5, dy = self.kloeVesselRadius, dz = self.kloeVesselHalfDx )

        upstream_shape_pos  = geom.structure.Position("upstream_shape_pos_for_tracker", - self.kloeVesselRadius + 0.5 * self.GRAINThickness + self.clearenceECALGRAIN, Q('0m'), Q('0m'))

        tracker_shape       = geom.shapes.Boolean("tracker_shape", type='subtraction', first = whole_shape, second = upstream_shape, rot='noRotate', pos=upstream_shape_pos)

        main_lv             = geom.structure.Volume('SANDtracker',   material=self.Material, shape=tracker_shape)

        print((f"Building {main_lv.name}"))

        self.FillTracker(geom, main_lv)

        return main_lv
    

    def FillTracker(self, geom, volume):

        self.constructTrackingStations(geom, volume)

        print("")
        # print something here, maybe
        print("")
        
        
    def constructTrackingStations(self, geom, volume):

        running_x =  -self.kloeVesselRadius + self.clearenceECALGRAIN + self.GRAINThickness + self.clearenceGRAINTracker#TODO: start from the GRAIN-side

        for idx, station_cfg in enumerate(self.stationDict):

            station_lv, station_thick = self.constructStation(geom, running_x, station_cfg,label = "s_"+str(idx))

            self.placeSubVolume(geom, volume, station_lv, pos_x = running_x + station_thick/2, label = str(idx))

            running_x += (station_thick + self.clearanceStations) #TODO: start from the GRAIN-side

            # self.WiresCounter["Tracker"] += self.WiresCounter["SuperMod"] 
            

    def constructStation(self, geom, running_x, station_cfg, chamberThickness=None, half_thickness=None,half_length=None, name = "station", label = ""):
        # build station main shape
        print("")
        print(f"Building station s_{label}")

        # self.WiresCounter["SuperMod"] = 0
        # TODO: temporarily assume only modules with targets when computing the thickness
        if chamberThickness == None : chamberThickness = station_cfg["n_views"]*station_cfg["view_thickness"] + self.MylarThickness
        if half_thickness == None : half_thickness = (station_cfg["tgt_thickness"]+chamberThickness)/2
        if half_length    == None : half_length    = self.kloeVesselHalfDx

        half_heigth    = self.getHalfHeight(abs(running_x))

        station_name  = label #TODO: review the name of the variables label is more of an index

        station_lv    = self.constructBox(geom, station_name, half_thickness, half_heigth, half_length)

        # build station subvolumes : frame and views(planes)

        frame_lv       = self.constructFrame(geom, half_thickness, half_heigth, half_length, label = label)
        # place the frame subvolume in the station logical volume 
        self.placeSubVolume(geom, station_lv, frame_lv)
        
        view_half_height            = half_heigth - self.frameThickness
        view_half_length            = half_length - self.frameThickness

        inner_station_lv            = self.constructBox(geom, label+"_in", half_thickness, view_half_height, view_half_length)
        
        tgt_string = "c" if station_cfg["tgt_material"] == 'Graphite' else "pp"

        target_lv                   = self.constructBox(geom, label+"_t_"+tgt_string, station_cfg["tgt_thickness"]/2, view_half_height, view_half_length, material=station_cfg["tgt_material"])

        DriftChamber_lv             = self.constructBox(geom, label+"_ch", chamberThickness/2, view_half_height, view_half_length) #TODO: review the need for a DriftChamber logical volume

        self.FillDriftChamber(geom, DriftChamber_lv, label, station_cfg) # updates self.WiresCounter["DriftChamber"]

        self.placeSubVolume(geom, inner_station_lv, target_lv, pos_x =- half_thickness + station_cfg["tgt_thickness"]/2)

        self.placeSubVolume(geom, inner_station_lv, DriftChamber_lv, pos_x = - half_thickness + station_cfg["tgt_thickness"] + chamberThickness/2)
        
        # place the inner station volume within the station
        self.placeSubVolume(geom, station_lv, inner_station_lv)
        

        print("")
        print(f"station dimensions : thickness {half_thickness*2}, heigth {half_heigth*2}, lenght {half_length*2}")

        return station_lv, half_thickness*2

    def constructFrame(self, geom, half_thickness, half_heigth, half_length, label = ""):

        name = label+"_fr"

        outer_box  = geom.shapes.Box(name+"_out_shape", dx = half_thickness, dy = half_heigth, dz = half_length)

        inner_box  = geom.shapes.Box(name+"_in_shape", dx = half_thickness, dy = half_heigth - self.frameThickness, dz = half_length - self.frameThickness)

        shape      = geom.shapes.Boolean(name+"_shape", type = "subtraction", first = outer_box, second = inner_box, rot='noRotate')

        frame_lv   = geom.structure.Volume(name, material = self.frameMaterial, shape = shape) 

        return frame_lv
    
    
    def FillDriftChamber(self, geom, DriftChamber_lv, label, station_cfg):

        half_dx, half_h, half_l     = geom.get_shape(DriftChamber_lv.shape)[1:]
        view_thickness = station_cfg["view_thickness"]

        MylarPlane_lv               = self.constructBox(geom, label+"_m", self.MylarThickness/2, half_h, half_l, "Mylar")

        running_x                   = - half_dx + self.MylarThickness/2
        
        for i in range(station_cfg["n_views"]):

            self.placeSubVolume(geom, DriftChamber_lv, MylarPlane_lv, pos_x = running_x, label = "_"+str(i))
            
            running_x += view_thickness/2


            view_lv = self.constructBox(geom, label+"_v_"+str(i), (view_thickness - self.MylarThickness)/2, half_h, half_l, self.driftGas)

            view_lv.params.append(("SensDet","DriftVolume"))

            self.placeSubVolume(geom, DriftChamber_lv, view_lv, pos_x = running_x, label = "_"+str(i))

            running_x           += view_thickness/2

        self.placeSubVolume(geom, DriftChamber_lv, MylarPlane_lv, pos_x = running_x, label = "_"+str(station_cfg["n_views"]+1))


    def constructBox(self, geom, name, half_thickness, half_heigth, half_length, material="Air35C"):
        
        box_shape = geom.shapes.Box(name+"_shape", dx = half_thickness, dy = half_heigth, dz = half_length)
        box       = geom.structure.Volume(name, material = material, shape = box_shape)
        return box

    
    def placeSubVolume(self, geom, volume, subvolume, pos_x=Q("0mm"), pos_y=Q("0mm"), pos_z=Q("0mm"), rot_x=Q("0deg"), rot_y=Q("0deg"), rot_z=Q("0deg"), label=""):

        name     = subvolume.name + label
        position = geom.structure.Position(name + "_pos", pos_x, pos_y, pos_z)
        rotation = geom.structure.Rotation(name + "_rot", rot_x, rot_y, rot_z)
        place    = geom.structure.Placement(name + "_place", volume = subvolume.name, pos = position.name, rot = rotation.name)

        volume.placements.append(place.name)
        
        
    def getHalfHeight(self,dis2c):

        theta   = math.pi*2/self.nBarrelModules
        d       = self.TrackerAvailableRadius*math.tan(theta/2)
        if dis2c<d:
            return self.TrackerAvailableRadius
        projectedDis = d
        HalfHeight   = self.TrackerAvailableRadius

        for i in range(1,int(self.nBarrelModules/4)):
            projectedDisPre = projectedDis
            projectedDis   += 2 * d * math.cos(i * theta)
            if dis2c<projectedDis:
                return HalfHeight-(dis2c-projectedDisPre)*math.tan(i*theta)
            else:
                HalfHeight-=2*d*math.sin(i*theta)