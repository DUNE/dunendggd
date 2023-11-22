#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
import math
from gegede import Quantity as Q

class DriftChamberModuleBuilder(gegede.builder.Builder):
    
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, moduleDx=None, moduleHeight=None,
                        NofDriftModules=None, DriftModulesWireAngles=None,
                        frameThickness=None,
                        targetThickness=None, targetMaterial=None, MylarThickness=None,
                        DriftModuleThickness=None, DriftChamberGas=None,
                        FieldWireRadius=None, SignalWireRadius=None, WireMaterial=None,WireAngle=None,WireWireDistance=None,
                        **kwds):

        self.moduleDx               = moduleDx
        self.moduleHeight           = moduleHeight
        self.NofDriftModules        = NofDriftModules
        self.DriftModulesWireAngles = DriftModulesWireAngles
        self.DriftChamberGas        = DriftChamberGas
        self.DriftModuleThickness   = DriftModuleThickness

        self.frameThickness         = frameThickness

        self.targetThickness        = targetThickness
        self.targetMaterial         = targetMaterial
        self.MylarThickness         = MylarThickness
        
        self.DriftChamberThickness  = self.DriftModuleThickness * self.NofDriftModules + self.MylarThickness*(self.NofDriftModules + 1)
        self.moduleThickness        = self.targetThickness + self.DriftChamberThickness

        self.FieldWireRadius        = FieldWireRadius
        self.SignalWireRadius       = SignalWireRadius
        self.WireMaterial           = WireMaterial
        self.WireAngle              = WireAngle
        self.WireWireDistance       = WireWireDistance

    def construct(self, geom):
        print("DriftChamberModuleBuilder::construct()")
        materials.define_materials(geom)
        main_lv = self.constructModule(geom)
        self.add_volume(main_lv)
        # print(type(main_lv))
        # print("volume added")
    
    def constructModule(self,geom):

        main_lv          = self.constructBox(geom, "prototype", self.moduleThickness/2, self.moduleHeight/2, self.moduleDx/2, "Air35C")

        frame_lv         = self.constructFrame(geom, "frame", self.moduleHeight/2, self.moduleDx/2)
        
        target_lv        = self.constructBox(geom, "target", self.targetThickness/2, self.moduleHeight/2 - self.frameThickness, self.moduleDx/2 - self.frameThickness, self.targetMaterial)
        
        drift_chamber_lv = self.constructBox(geom, "drift_volume", self.DriftChamberThickness/2, self.moduleHeight/2 - self.frameThickness, self.moduleDx/2 - self.frameThickness, "Air35C") 

        self.FillDriftChamber(geom, drift_chamber_lv)

        self.PlaceSubVolume(geom, main_lv, frame_lv)

        self.PlaceSubVolume(geom, main_lv, target_lv, pos_x = -self.moduleThickness/2 + self.targetThickness/2)
        
        self.PlaceSubVolume(geom, main_lv, drift_chamber_lv, pos_x = -self.moduleThickness/2 + self.targetThickness + self.DriftChamberThickness/2)
        
        return main_lv

    def FillDriftChamber(self,geom, drift_volume):

        half_dx, half_h, half_l     = geom.get_shape(drift_volume.shape)[1:]

        MylarPlane_lv               = self.constructBox(geom, drift_volume.name + "_mylar", self.MylarThickness/2, half_h, half_l, "Mylar")

        running_x                   = - half_dx

        for i in range(self.NofDriftModules):
            
            running_x           += self.MylarThickness/2

            self.PlaceSubVolume(geom, drift_volume, MylarPlane_lv, pos_x = running_x, label = "_"+str(i))
 
            running_x           += self.MylarThickness/2 + self.DriftModuleThickness/2
            
            if self.DriftModulesWireAngles[i] == Q("90deg"):
                DriftModule_lv       = self.constructBox(geom, "drift_module"+str(i), self.DriftModuleThickness/2, half_l, half_h, self.DriftChamberGas)
                rot_x = Q("90deg")
            else:
                DriftModule_lv       = self.constructBox(geom, "drift_module"+str(i), self.DriftModuleThickness/2, half_h, half_l, self.DriftChamberGas)
                rot_x = Q("0deg")

            self.FillDriftModule(geom, DriftModule_lv)

            self.PlaceSubVolume(geom, drift_volume, DriftModule_lv, pos_x = running_x, rot_x = rot_x, label = "_"+str(i))

            running_x           += self.DriftModuleThickness/2

        running_x           += self.MylarThickness/2

        self.PlaceSubVolume(geom, drift_volume, MylarPlane_lv, pos_x = running_x, label = "_"+str(self.NofDriftModules+1))

    
    def FillDriftModule(self, geom, drift_module):
        
        half_dx, half_h, half_l = geom.get_shape(drift_module.shape)[1:]

        module_number           = int(drift_module.name[-1])
        
        staggered               = (module_number%2)
        
        print(" ")
        print("drift module : "+drift_module.name)
        print("module height : "+str(half_h*2))
        print("module length : "+str(half_l*2))

        FieldWire_lv            = self.constructWire(geom, drift_module.name, half_l*2, Q("0deg"), "F")
        SignalWire_lv           = self.constructWire(geom, drift_module.name, half_l*2, Q("0deg"), "S")

        wire_index, nof_wires, running_wire = 0, 0, FieldWire_lv
        
        running_y = half_h - 1.5*(self.WireWireDistance + self.FieldWireRadius) if staggered else half_h - (self.WireWireDistance + self.FieldWireRadius)
        
        while(running_y > - half_h):

            self.PlaceSubVolume(geom, drift_module, running_wire, pos_y = running_y, label = "_" + str(wire_index).zfill(3))
            nof_wires  += 1
            wire_index += 1

            running_wire = (FieldWire_lv,SignalWire_lv)[wire_index % 2]

            running_y -= (self.WireWireDistance + self.FieldWireRadius + self.SignalWireRadius)

        print("nof_wires build : "+str(nof_wires))
        print(" ")
    
    def constructWire(self, geom, base_name, length, wire_angle, wire_type):

        wire_name           = base_name+"_"+wire_type+"wire"
        r                   = self.SignalWireRadius if wire_type=="S" else self.FieldWireRadius
        wire_shape          = geom.shapes.Tubs(wire_name+"_shape", rmin = Q("0mm"), rmax = r, dz=length/2)
        wire_lv             = geom.structure.Volume(wire_name, material = self.WireMaterial, shape = wire_shape)
        print(wire_type+"wire length : "+str(length))

        return wire_lv
    
    def constructBox(self, geom, name, half_thickness, half_heigth, half_length, material):
        
        box_shape = geom.shapes.Box(name+"_shape", dx = half_thickness, dy = half_heigth, dz = half_length)
        box       = geom.structure.Volume(name, material = material, shape = box_shape)
        return box
    
    def constructFrame(self, geom, name, half_h, half_l):
        outer_box  = geom.shapes.Box(name + "_out_shape", dx = self.moduleThickness/2, dy = half_h, dz = half_l)
        inner_box  = geom.shapes.Box(name + "_in_shape", dx = self.moduleThickness/2, dy = half_h - self.frameThickness, dz = half_l - self.frameThickness)

        shape = geom.shapes.Boolean(name+"_shape", type = "subtraction", first = outer_box, second = inner_box, rot='noRotate')

        frame = geom.structure.Volume(name, material = "carbonComposite", shape = shape)
        return frame 

    
    def PlaceSubVolume(self, geom, volume, subvolume, pos_x=Q("0mm"), pos_y=Q("0mm"), pos_z=Q("0mm"), rot_x=Q("0deg"), rot_y=Q("0deg"), rot_z=Q("0deg"), label=""):

        name = subvolume.name + label
        position = geom.structure.Position(name + "_pos", pos_x, pos_y, pos_z)
        rotation = geom.structure.Rotation(name + "_rot", rot_x, rot_y, rot_z)
        place    = geom.structure.Placement(name + "_place", volume = subvolume.name, pos = position.name, rot = rotation.name)
        
        volume.placements.append(place.name)
    
