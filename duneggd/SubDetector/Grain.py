import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class GrainBuilder(gegede.builder.Builder):

    def configure( self, configuration=None, 
                  ExtVesselThickness = None, ExtVesselHeight = None, ExtVesselLength = None, 
                  CarbonFiberThickness = None, HoneycombThickness = None, SteelThickness = None, EndcapThickness = None,
                  LArThickness = None, LArHeight = None, LArLength = None, 
                  **kwds):
        
        self.configuration          = configuration
        
        self.ExtVesselThickness     = ExtVesselThickness
        self.ExtVesselHeight        = ExtVesselHeight
        self.ExtVesselLength        = ExtVesselLength
        
        self.CarbonFiberThickness   = CarbonFiberThickness
        self.HoneycombThickness     = HoneycombThickness
        self.SteelThickness         = SteelThickness

        self.EndcapThickness        = EndcapThickness
        
        self.LArThickness           = LArThickness
        self.LArHeight              = LArHeight
        self.LArLength              = LArLength

        self.VacuumThicknessX       = self.ExtVesselThickness/2 - self.CarbonFiberThickness*2 - self.HoneycombThickness - (self.LArThickness/2 + self.SteelThickness)
        self.VacuumThicknessY       = self.ExtVesselThickness/2 - self.CarbonFiberThickness*2 - self.HoneycombThickness - (self.LArHeight/2 + self.SteelThickness)
        self.VacuumThicknessZ       = self.ExtVesselThickness/2 - self.CarbonFiberThickness*2 - self.HoneycombThickness - (self.LArLength/2 + self.SteelThickness)
    

    def construct(self, geom):
        print("constructing GRAIN")
        GRAIN_lv = self.constructGRAIN(geom)
        self.add_volume(GRAIN_lv)
    
    def constructGRAIN(self,geom):

        GRAIN_lv = self.constructElTube(geom, "GRAIN_lv",       self.ExtVesselThickness/2, self.ExtVesselHeight/2, self.ExtVesselLength/2)

        ExtVessel_CF1_lv   = self.construcElTubeShell(geom, "GRAIN_Ext_vessel_outer_layer_lv",  self.ExtVesselThickness/2, 
                                                                                                self.ExtVesselHeight/2, 
                                                                                                self.ExtVesselLength/2, 
                                                                                                material_thickness = self.CarbonFiberThickness, 
                                                                                                material = "Carbon_fiber")
        
        ExtVessel_Honey_lv = self.construcElTubeShell(geom, "GRAIN_Honeycomb_layer_lv",         self.ExtVesselThickness/2 - self.CarbonFiberThickness, 
                                                                                                self.ExtVesselHeight/2    - self.CarbonFiberThickness, 
                                                                                                self.ExtVesselLength/2    - self.CarbonFiberThickness, 
                                                                                                material_thickness = self.HoneycombThickness,
                                                                                                material = "Vacuum_cryo")
        
        ExtVessel_CF2_lv   = self.construcElTubeShell(geom, "GRAIN_Ext_vessel_inner_layer_lv",  self.ExtVesselThickness/2 - self.CarbonFiberThickness - self.HoneycombThickness, 
                                                                                                self.ExtVesselHeight/2    - self.CarbonFiberThickness - self.HoneycombThickness, 
                                                                                                self.ExtVesselLength/2    - self.CarbonFiberThickness - self.HoneycombThickness, 
                                                                                                material_thickness = self.CarbonFiberThickness, 
                                                                                                material = "Carbon_fiber")
        
        vacuum_lv          = self.construcElTubeShell(geom, "GRAIN_gap_between_vessels_lv",     self.ExtVesselThickness/2 - self.CarbonFiberThickness*2 - self.HoneycombThickness, 
                                                                                                self.ExtVesselHeight/2    - self.CarbonFiberThickness*2 - self.HoneycombThickness, 
                                                                                                self.ExtVesselLength/2    - self.CarbonFiberThickness*2 - self.HoneycombThickness, 
                                                                                                material_thickness = (self.VacuumThicknessX, self.VacuumThicknessY, self.VacuumThicknessZ), 
                                                                                                material = "Vacuum_cryo")
        
        InnerVessel_lv     = self.construcElTubeShell(geom, "GRAIN_inner_vessel_lv",            self.LArThickness/2 + self.SteelThickness,
                                                                                                self.LArHeight/2    + self.SteelThickness,
                                                                                                self.LArLength/2    + self.EndcapThickness,
                                                                                                material_thickness = (self.SteelThickness, self.SteelThickness, self.EndcapThickness),
                                                                                                material = "Steel")   
        
        LAr_lv             = self.constructElTube(geom,     "GRAIN_LAr_lv",                     self.LArThickness/2, 
                                                                                                self.LArHeight/2, 
                                                                                                self.LArLength/2, 
                                                                                                material = "LAr")      

        LAr_lv.params.append(("SensDet", 'LArHit'))

        self.placeSubVolume(geom, GRAIN_lv, ExtVessel_CF1_lv)
        self.placeSubVolume(geom, GRAIN_lv, ExtVessel_Honey_lv)
        self.placeSubVolume(geom, GRAIN_lv, ExtVessel_CF2_lv)
        self.placeSubVolume(geom, GRAIN_lv, vacuum_lv)
        self.placeSubVolume(geom, GRAIN_lv, InnerVessel_lv)
        self.placeSubVolume(geom, GRAIN_lv, LAr_lv)

        return GRAIN_lv


    def construcElTubeShell(self, geom, name, half_thickness, half_heigth, half_length, material_thickness, material="Air35C"):

        if type(material_thickness)==type(Q("0mm")):
            material_thickness_x, material_thickness_y, material_thickness_z = material_thickness, material_thickness, material_thickness
        else:
            material_thickness_x, material_thickness_y, material_thickness_z = material_thickness[0], material_thickness[1], material_thickness[2]

        outer_eltube    = geom.shapes.EllipticalTube(name + "_out", dx = half_thickness, dy = half_heigth, dz = half_length)
        inner_eltube    = geom.shapes.EllipticalTube(name + "_in",  dx = half_thickness - material_thickness_x, dy = half_heigth - material_thickness_y, dz = half_length - material_thickness_z)
        shape           = geom.shapes.Boolean(name+"_shape", type = "subtraction", first = outer_eltube, second = inner_eltube, rot='noRotate')
        tube_shell_lv   = geom.structure.Volume(name, material = material, shape = shape)
        return tube_shell_lv

    def constructElTube(self, geom, name, half_thickness, half_heigth, half_length, material="Air35C"):

        tube_shape = geom.shapes.EllipticalTube(name+"_shape", dx = half_thickness, dy = half_heigth, dz = half_length)
        tube       = geom.structure.Volume(name, material = material, shape = tube_shape)
        return tube

    
    def placeSubVolume(self, geom, volume, subvolume, pos_x=Q("0mm"), pos_y=Q("0mm"), pos_z=Q("0mm"), rot_x=Q("0deg"), rot_y=Q("0deg"), rot_z=Q("0deg"), label=""):

        name     = subvolume.name + label
        position = geom.structure.Position(name + "_pos", pos_x, pos_y, pos_z)
        rotation = geom.structure.Rotation(name + "_rot", rot_x, rot_y, rot_z)
        place    = geom.structure.Placement(name + "_place", volume = subvolume.name, pos = position.name, rot = rotation.name)
        
        volume.placements.append(place.name)
