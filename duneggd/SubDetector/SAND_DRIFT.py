import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q
import time

class DRIFTBuilder(gegede.builder.Builder):

    def configure(self, 
                # sand inner volume info
                configuration = None,tracker_configuration=None, nBarrelModules = None, halfDimension = None, Material = None, GRAINThickness = None, 
                clearenceECALGRAIN = None, clearenceGRAINTracker = None, clearenceTrackerECAL = None, clearenceSupermods = None,
                # tracker
                nofUpstreamTrkMod = None, nofDownstreamTrkMod = None, nofC3H6ModAfterCMod = None,
                # tracker module
                frameThickness = None, frameMaterial = None, targetThickness = None, MylarThickness = None, NofDriftModules = None, DriftModulesWireAngles = None, DriftChamberGas = None, DriftModuleThickness = None,
                # module wire
                FieldWireRadius = None, SignalWireRadius = None, WireMaterial = None, WireAngle = None, WireWireDistance = None,
                **kwds):

            # sand inner volume info
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
            self.clearenceSupermods         = clearenceSupermods

            # tracker
            self.nofUpstreamTrkMod          = nofUpstreamTrkMod
            self.nofDownstreamTrkMod        = nofDownstreamTrkMod
            self.nofC3H6ModAfterCMod        = nofC3H6ModAfterCMod

            # tracker module
            self.frameThickness             = frameThickness
            self.frameMaterial              = frameMaterial
            self.targetThickness            = targetThickness
            self.MylarThickness             = MylarThickness
            self.NofDriftModules            = NofDriftModules
            self.DriftModulesWireAngles     = DriftModulesWireAngles
            self.DriftChamberGas            = DriftChamberGas
            self.DriftModuleThickness       = DriftModuleThickness
            self.DriftChamberThickness      = self.NofDriftModules * self.DriftModuleThickness + (self.NofDriftModules + 1) * self.MylarThickness

            # module wire
            self.FieldWireRadius            = FieldWireRadius
            self.SignalWireRadius           = SignalWireRadius
            self.WireMaterial               = WireMaterial
            self.WireAngle                  = WireAngle
            self.WireWireDistance           = WireWireDistance

    def init(self):

            self.GetModThickness            = lambda mod_type : self.targetThickness[mod_type] + self.NofDriftModules * self.DriftModuleThickness + (self.NofDriftModules + 1) * self.MylarThickness

            self.ModThickness               = {"CMod" : self.GetModThickness("CMod"), "C3H6Mod" : self.GetModThickness("C3H6Mod"), "TrkMod" : self.GetModThickness("TrkMod")}

            self.SuperModThickness          = self.ModThickness["CMod"] + self.ModThickness["C3H6Mod"] * self.nofC3H6ModAfterCMod# + self.clearenceSupermods 

            self.Space4Tracker              = self.kloeVesselRadius * 2 - self.GRAINThickness - self.clearenceECALGRAIN - self.clearenceGRAINTracker - self.clearenceTrackerECAL

            self.nofSuperMods               = int((self.Space4Tracker / (self.SuperModThickness + self.clearenceSupermods)).to_base_units().magnitude)

            self.nofSymMods                 = 3

            self.nofExtraMods               = 2

            self.WiresCounter               = {"Tracker":0, "SuperMod":0, "DriftChamber":0, "DriftModule":0}

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
            print("clearance SuperMods            | "+str(self.clearenceSupermods))
            print("Space 4 Tracker                | "+str(self.Space4Tracker))
            print("")
            print("_"*20+" MODULE INFO "+"_"*20)
            print("")
            print("trkMod       Thickness         | "+str(self.ModThickness["TrkMod"]))
            print("C3H6Mod      Thickness         | "+str(self.ModThickness["C3H6Mod"]))
            print("CMod         Thickness         | "+str(self.ModThickness["CMod"]))
            print("SuperMod     Thickness         | "+str(self.SuperModThickness))
            print("")
            print("")
            print(f"nof supermodules               | {self.nofSuperMods}")
            print("")
            print("_"*60)

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

        self.constructExtraMod(geom, volume)

        self.costructSymSuperMod(geom, volume)

        print("")
        print(f"{volume.name} nof wires built {self.WiresCounter['Tracker']}")
        print("")

    def constructExtraMod(self, geom, volume):

        running_x = self.kloeVesselRadius - self.clearenceTrackerECAL

        for i in range(self.nofExtraMods):

            extraMod_lv = self.constructSuperMod(geom, running_x, label = "_X"+str(i))

            self.placeSubVolume(geom, volume, extraMod_lv, pos_x = running_x - self.SuperModThickness/2, label = str(i))

            running_x -= (self.SuperModThickness + self.clearenceSupermods)

            self.WiresCounter["Tracker"] += self.WiresCounter["SuperMod"] 

    def costructSymSuperMod(self, geom, volume):

        running_x = self.kloeVesselRadius - self.clearenceTrackerECAL - (self.SuperModThickness + self.clearenceSupermods) * self.nofExtraMods

        supermod_label = ["C", "B", "A"]
        step           = [5,3,1]

        for i in range(self.nofSymMods):

            SuperMod_lv = self.constructSuperMod(geom, abs(running_x), label = "_"+supermod_label[i])

            self.placeSubVolume(geom, volume, SuperMod_lv, pos_x = running_x - self.SuperModThickness/2, label = str(i)+"dw")

            print(f"placing SuperMod {supermod_label[i]} up")

            self.placeSubVolume(geom, volume, SuperMod_lv, pos_x = running_x - self.SuperModThickness/2 - (self.SuperModThickness + self.clearenceSupermods)*step[i], label = str(i)+"up")

            print(f"placing SuperMod {supermod_label[i]} dw")

            if i == 0 : 
                tracking_lv = self.constructTrackingMod(geom, volume,abs(running_x))
                half_tracking_thickness = geom.get_shape(tracking_lv.shape)[1]
                self.placeSubVolume(geom, volume, tracking_lv, pos_x = running_x - self.SuperModThickness - (self.SuperModThickness + self.clearenceSupermods)*step[i] - half_tracking_thickness, label = "Trk")

            running_x -= (self.SuperModThickness + self.clearenceSupermods)

            self.WiresCounter["Tracker"] += self.WiresCounter["SuperMod"] * 2

    def constructTrackingMod(self, geom, volume, running_x):

        nofDriftMods = 2

        half_heigth  = self.getHalfHeight(running_x)

        thickness    = nofDriftMods * self.DriftModuleThickness + (nofDriftMods + 1) * self.MylarThickness

        tracking_lv  = self.constructBox(geom, "Trk", thickness/2, half_heigth,self.kloeVesselHalfDx)

        frame_lv     = self.constructFrame(geom, thickness/2, half_heigth, self.kloeVesselHalfDx, label = "Trk")

        drift_lv     = self.constructBox(geom, "TrkDrift", thickness/2, half_heigth - self.frameThickness, self.kloeVesselHalfDx - self.frameThickness)

        self.FillDriftChamber(geom, drift_lv,"C", nofDriftModules = nofDriftMods, wireAngles = [Q("0deg"),Q("90deg")])

        self.placeSubVolume(geom, tracking_lv, frame_lv)
        self.placeSubVolume(geom, tracking_lv, drift_lv)

        return tracking_lv

    def constructSuperMod(self, geom, running_x, half_thickness = None, half_length = None, nofC3H6 = None, name = "SuperMod", label = ""):
        # build SuperMod main shape
        print("")
        print(f"Building SuperMod{label}")

        self.WiresCounter["SuperMod"] = 0

        if half_thickness == None : half_thickness = self.SuperModThickness/2
        if half_length    == None : half_length    = self.kloeVesselHalfDx
        if nofC3H6        == None : nofC3H6        = self.nofC3H6ModAfterCMod

        half_heigth    = self.getHalfHeight(abs(running_x))

        SuperMod_name  = name + label

        SuperMod_lv    = self.constructBox(geom, SuperMod_name, half_thickness, half_heigth, half_length)

        # build SuperMod subvolumes : CMod, C3H6Mod, Frame

        frame_lv       = self.constructFrame(geom, half_thickness, half_heigth, half_length, label = label)

        CMod_lv        = self.constructMod(geom, "C", half_heigth - self.frameThickness, label = label)

        self.WiresCounter["SuperMod"] += self.WiresCounter["DriftChamber"] 

        C3H6Mod_lv     = self.constructMod(geom, "C3H6", half_heigth - self.frameThickness, label = label)

        self.WiresCounter["SuperMod"] += self.WiresCounter["DriftChamber"] * nofC3H6 
        # place subvolumes in SuperMod

        self.placeSubVolume(geom, SuperMod_lv, frame_lv)

        self.placeSubVolume(geom, SuperMod_lv, CMod_lv, pos_x = - half_thickness + self.ModThickness["CMod"]/2)

        for i in range(nofC3H6):

            pos_x =  - half_thickness + self.ModThickness["CMod"] + self.ModThickness["C3H6Mod"] * (0.5 + i)

            self.placeSubVolume(geom, SuperMod_lv, C3H6Mod_lv, pos_x = pos_x, label=str(i))

        print("")
        print(f"supermodule dimensions : thickness {half_thickness*2}, heigth {half_heigth*2}, lenght {half_length*2}")
        print(f"{SuperMod_lv.name} nof wires {self.WiresCounter['SuperMod']}")

        return SuperMod_lv

    def constructFrame(self, geom, half_thickness, half_heigth, half_length, label = ""):

        name = "Frame"+label

        outer_box  = geom.shapes.Box(name+"_out_shape", dx = half_thickness, dy = half_heigth, dz = half_length)

        inner_box  = geom.shapes.Box(name+"_in_shape", dx = half_thickness, dy = half_heigth - self.frameThickness, dz = half_length - self.frameThickness)

        shape      = geom.shapes.Boolean(name+"_shape", type = "subtraction", first = outer_box, second = inner_box, rot='noRotate')

        frame_lv   = geom.structure.Volume(name, material = self.frameMaterial, shape = shape) 

        return frame_lv
 
    def constructMod(self, geom, target_type, half_heigth, label = ""):

        self.WiresCounter["DriftChamber"] = 0

        half_thickness, half_length = self.ModThickness[target_type+"Mod"]/2, self.kloeVesselHalfDx - self.frameThickness

        target_material = "Graphite" if target_type == 'C' else "C3H6"

        mod_lv                      = self.constructBox(geom, target_type+"Mod"+label, half_thickness, half_heigth, half_length)

        target_lv                   = self.constructBox(geom, target_type+"Target"+label, self.targetThickness[target_type+"Mod"]/2, half_heigth, half_length, material=target_material)

        DriftChamber_lv             = self.constructBox(geom, target_type+"DriftChamber"+label, self.DriftChamberThickness/2, half_heigth, half_length)

        self.FillDriftChamber(geom, DriftChamber_lv, target_type, label) # updates self.WiresCounter["DriftChamber"]

        self.placeSubVolume(geom, mod_lv, target_lv, pos_x = - half_thickness + self.targetThickness[target_type+"Mod"]/2)

        self.placeSubVolume(geom, mod_lv, DriftChamber_lv, pos_x = - half_thickness + self.targetThickness[target_type+"Mod"] + self.DriftChamberThickness/2)

        return mod_lv

    def FillDriftChamber(self, geom, DriftChamber_lv, target_type, label="", nofDriftModules = None, wireAngles = None, DriftChamberGas = None):

        if nofDriftModules == None: nofDriftModules = self.NofDriftModules
        if wireAngles      == None: wireAngles      = self.DriftModulesWireAngles
        if DriftChamberGas == None: DriftChamberGas = self.DriftChamberGas[target_type+"Mod"]

        half_dx, half_h, half_l     = geom.get_shape(DriftChamber_lv.shape)[1:]

        MylarPlane_lv               = self.constructBox(geom, target_type+"Mylar"+label, self.MylarThickness/2, half_h, half_l, "Mylar")

        running_x                   = - half_dx

        for i in range(nofDriftModules):

            running_x += self.MylarThickness/2

            self.placeSubVolume(geom, DriftChamber_lv, MylarPlane_lv, pos_x = running_x, label = "_"+str(i))

            running_x += self.MylarThickness/2 + self.DriftModuleThickness/2

            if wireAngles[i] == Q("90deg"):

                DriftModule_lv       = self.constructBox(geom, target_type+"DriftModule_"+str(i)+label, self.DriftModuleThickness/2, half_l, half_h, DriftChamberGas)
                rot_x = Q("90deg")
            else:
                DriftModule_lv       = self.constructBox(geom, target_type+"DriftModule_"+str(i)+label, self.DriftModuleThickness/2, half_h, half_l, DriftChamberGas)
                rot_x = Q("0deg")

            DriftModule_lv.params.append(("SensDet","DriftVolume"))

            self.FillDriftModule(geom, DriftModule_lv, module_number = i)

            self.WiresCounter["DriftChamber"] += self.WiresCounter["DriftModule"]

            self.placeSubVolume(geom, DriftChamber_lv, DriftModule_lv, pos_x = running_x, rot_x = rot_x, label = "_"+str(i))

            running_x           += self.DriftModuleThickness/2

        running_x           += self.MylarThickness/2

        self.placeSubVolume(geom, DriftChamber_lv, MylarPlane_lv, pos_x = running_x, label = "_"+str(self.NofDriftModules+1))

    def FillDriftModule(self, geom, DriftModule_lv, module_number):

        half_dx, half_h, half_l = geom.get_shape(DriftModule_lv.shape)[1:]

        staggered               = (module_number%2)

        FieldWire_lv            = self.constructWire(geom, DriftModule_lv.name, half_l*2, "F")

        SignalWire_lv           = self.constructWire(geom, DriftModule_lv.name, half_l*2, "S")

        wire_index, running_wire = 0, FieldWire_lv

        running_y = half_h - 1.5*(self.WireWireDistance + self.FieldWireRadius) if staggered else half_h - (self.WireWireDistance + self.FieldWireRadius)

        while(running_y > - half_h):

            self.placeSubVolume(geom, DriftModule_lv, running_wire, pos_y = running_y, label = "_" + str(wire_index).zfill(3))

            wire_index += 1

            running_wire = (FieldWire_lv,SignalWire_lv)[wire_index % 2]

            running_y -= (self.WireWireDistance + self.FieldWireRadius + self.SignalWireRadius)

        self.WiresCounter["DriftModule"] = wire_index + 1

    def constructWire(self, geom, base_name, length, wire_type):

        wire_name           = base_name+"_"+wire_type+"wire"
        r                   = self.SignalWireRadius if wire_type=="S" else self.FieldWireRadius
        wire_shape          = geom.shapes.Tubs(wire_name+"_shape", rmin = Q("0mm"), rmax = r, dz=length/2)
        wire_lv             = geom.structure.Volume(wire_name, material = self.WireMaterial, shape = wire_shape)
        # print(wire_type+"wire length : "+str(length))

        return wire_lv

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
        d       = self.kloeVesselRadius*math.tan(theta/2)
        if dis2c<d:
            return self.kloeVesselRadius
        projectedDis = d
        HalfHeight   = self.kloeVesselRadius

        for i in range(1,int(self.nBarrelModules/4)):
            projectedDisPre = projectedDis
            projectedDis   += 2 * d * math.cos(i * theta)
            if dis2c<projectedDis:
                return HalfHeight-(dis2c-projectedDisPre)*math.tan(i*theta)
            else:
                HalfHeight-=2*d*math.sin(i*theta)