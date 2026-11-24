import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class GrainBuilder(gegede.builder.Builder):

    def configure( self, configuration=None, 
                  ExtVesselThickness = None, ExtVesselHeight = None, ExtVesselLength = None, 
                  CarbonFiberThickness = None, HoneycombThickness = None, SteelThickness = None, EndcapThickness = None,
                  InEndcapRingThickness = None, InEndcapRingLength = None, LArThickness = None, LArHeight = None, LArLength = None, 
                  **kwds):
        
        self.configuration          = configuration
        
        self.ExtVesselThickness     = ExtVesselThickness
        self.ExtVesselHeight        = ExtVesselHeight
        self.ExtVesselLength        = ExtVesselLength
        
        self.CarbonFiberThickness   = CarbonFiberThickness
        self.HoneycombThickness     = HoneycombThickness
        self.SteelThickness         = SteelThickness

        self.EndcapThickness        = EndcapThickness
        self.InEndcapRingThickness  = InEndcapRingThickness
        self.InEndcapRingLength     = InEndcapRingLength
        
        self.LArThickness           = LArThickness
        self.LArHeight              = LArHeight
        self.LArLength              = LArLength

        self.VacuumThicknessX       = self.ExtVesselThickness/2 - self.CarbonFiberThickness*2 - self.HoneycombThickness - (self.LArThickness/2 + self.SteelThickness)
        self.VacuumThicknessY       = self.ExtVesselHeight/2 - self.CarbonFiberThickness*2 - self.HoneycombThickness - (self.LArHeight/2 + self.SteelThickness)
        self.VacuumThicknessZ       = self.ExtVesselLength/2 - self.CarbonFiberThickness*2 - self.HoneycombThickness - (self.LArLength/2 + self.EndcapThickness)
    

    def construct(self, geom):
        print("constructing GRAIN")
        GRAIN_lv = self.constructGRAIN(geom)
        self.add_volume(GRAIN_lv)
    
    def constructGRAIN(self,geom):

        GRAIN_lv, _ = self.constructElTube(geom, "GRAIN_lv",       self.ExtVesselThickness/2, self.ExtVesselHeight/2, self.ExtVesselLength/2)

        ExtVessel_CF1_lv, _   = self.constructElTubeShell(geom, "GRAIN_Ext_vessel_outer_layer_lv",  self.ExtVesselThickness/2, 
                                                                                                self.ExtVesselHeight/2, 
                                                                                                self.ExtVesselLength/2, 
                                                                                                material_thickness = self.CarbonFiberThickness, 
                                                                                                material = "Carbon_fiber")
        
        ExtVessel_Honey_lv, _ = self.constructElTubeShell(geom, "GRAIN_Honeycomb_layer_lv",         self.ExtVesselThickness/2 - self.CarbonFiberThickness, 
                                                                                                self.ExtVesselHeight/2    - self.CarbonFiberThickness, 
                                                                                                self.ExtVesselLength/2    - self.CarbonFiberThickness, 
                                                                                                material_thickness = self.HoneycombThickness,
                                                                                                material = "Vacuum_cryo")
        
        ExtVessel_CF2_lv, _   = self.constructElTubeShell(geom, "GRAIN_Ext_vessel_inner_layer_lv",  self.ExtVesselThickness/2 - self.CarbonFiberThickness - self.HoneycombThickness, 
                                                                                                self.ExtVesselHeight/2    - self.CarbonFiberThickness - self.HoneycombThickness, 
                                                                                                self.ExtVesselLength/2    - self.CarbonFiberThickness - self.HoneycombThickness, 
                                                                                                material_thickness = self.CarbonFiberThickness, 
                                                                                                material = "Carbon_fiber")
        # construct the complex InnerVessel shape and volume in a dedicated function
        InnerVessel_lv, InnerVessel_shape = self.constructInnerVessel(geom)
        # return the LAr shape and volume 
        LAr_lv, LAr_shape            = self.constructElTube(geom,     "GRAIN_LAr_lv",           self.LArThickness/2, 
                                                                                                self.LArHeight/2, 
                                                                                                self.LArLength/2, 
                                                                                                material = "LAr")     
        # subtract InnerVessel_shape and LAr_shape from an ElTubeShape to define the vacuum volume
        vacuum_lv          = self.constructVacuum(geom, InnerVessel_shape, LAr_shape)

        LAr_lv.params.append(("SensDet", 'LArHit'))

        self.placeSubVolume(geom, GRAIN_lv, ExtVessel_CF1_lv)
        self.placeSubVolume(geom, GRAIN_lv, ExtVessel_Honey_lv)
        self.placeSubVolume(geom, GRAIN_lv, ExtVessel_CF2_lv)
        self.placeSubVolume(geom, GRAIN_lv, vacuum_lv)
        self.placeSubVolume(geom, GRAIN_lv, InnerVessel_lv)
        self.placeSubVolume(geom, GRAIN_lv, LAr_lv)
        
        return GRAIN_lv

    def constructElTubeShellShape(self, geom, name, hx, hy, hz, tx, ty, tz):
        outer = geom.shapes.EllipticalTube(name + "_out", dx=hx,      dy=hy,      dz=hz)
        inner = geom.shapes.EllipticalTube(name + "_in",  dx=hx - tx, dy=hy - ty, dz=hz - tz)
        return geom.shapes.Boolean(name + "_shape", type="subtraction", first=outer, second=inner, rot='noRotate')

    def constructElTubeShell(self, geom, name, half_thickness, half_heigth, half_length, material_thickness, material="Air35C"):

        if type(material_thickness)==type(Q("0mm")):
            material_thickness_x, material_thickness_y, material_thickness_z = material_thickness, material_thickness, material_thickness
        else:
            material_thickness_x, material_thickness_y, material_thickness_z = material_thickness[0], material_thickness[1], material_thickness[2]
        
        tube_shell_shape           = self.constructElTubeShellShape(geom, name, hx = half_thickness, hy = half_heigth, hz = half_length, 
                                                                tx = material_thickness_x, 
                                                                ty = material_thickness_y, 
                                                                tz = material_thickness_z)
        tube_shell_lv   = geom.structure.Volume(name, material = material, shape = tube_shell_shape)
        return tube_shell_lv, tube_shell_shape
    
    def constructElTubeShape(self, geom, name, half_thickness, half_heigth, half_length):
        return geom.shapes.EllipticalTube(name + "_shape", dx=half_thickness, dy=half_heigth, dz=half_length)

    def constructElTube(self, geom, name, half_thickness, half_heigth, half_length, material="Air35C"):

        tube_shape = self.constructElTubeShape(geom, name, half_thickness, half_heigth, half_length)
        tube       = geom.structure.Volume(name, material = material, shape = tube_shape)
        return tube, tube_shape
    
    def constructInnerVessel(self, geom):
        """Inner steel vessel: elliptical shell + two off-centre end-cap rings, merged into one volume + other stuff"""
        vessel_shape = self.constructElTubeShellShape(geom, "GRAIN_inner_vessel",
                self.LArThickness/2 + self.SteelThickness,
                self.LArHeight/2    + self.SteelThickness,
                self.LArLength/2    + self.EndcapThickness,
                self.SteelThickness, self.SteelThickness, self.EndcapThickness)

        ring_shape = self.constructElTubeShellShape(geom, "InEndcapRing",
                self.LArThickness/2 + self.SteelThickness + self.InEndcapRingThickness,
                self.LArHeight/2    + self.SteelThickness + self.InEndcapRingThickness,
                self.InEndcapRingLength/2,
                self.InEndcapRingThickness, self.InEndcapRingThickness, Q("0mm"))

        ring_dz = self.LArLength/2 + self.EndcapThickness - self.InEndcapRingLength/2
        # define the endcap ring shapes
        pos_p = geom.structure.Position("InEndcapRing_pos_p", Q("0mm"), Q("0mm"),  ring_dz)
        pos_m = geom.structure.Position("InEndcapRing_pos_m", Q("0mm"), Q("0mm"), -ring_dz)
        u1 = geom.shapes.Boolean("GRAIN_inner_vessel_u1", type="union",
                                first=vessel_shape, second=ring_shape, pos=pos_p, rot='noRotate')
        u2 = geom.shapes.Boolean("GRAIN_inner_vessel_u2", type="union",
                                first=u1, second=ring_shape, pos=pos_m, rot='noRotate')
        # return both subvolume and shape (the latter to be subtracted to the vacuum volume)
        inner_vessel_lv = geom.structure.Volume("GRAIN_inner_vessel_lv", material="Steel", shape=u2)
        return inner_vessel_lv, u2
    
    def constructVacuum(self, geom, InnerVesselShape, LAr_shape):
        gap_outer = self.constructElTubeShape(geom, "GRAIN_gap_between_vessels_out",
                        self.ExtVesselThickness/2 - self.CarbonFiberThickness*2 - self.HoneycombThickness,
                        self.ExtVesselHeight/2    - self.CarbonFiberThickness*2 - self.HoneycombThickness,
                        self.ExtVesselLength/2    - self.CarbonFiberThickness*2 - self.HoneycombThickness)
        gap_s1 = geom.shapes.Boolean("GRAIN_gap_s1", type="subtraction",
                                    first=gap_outer, second=InnerVesselShape, rot='noRotate')
        gap_s2 = geom.shapes.Boolean("GRAIN_gap_s2", type="subtraction",
                                    first=gap_s1, second=LAr_shape, rot='noRotate')
        vacuum_lv = geom.structure.Volume("GRAIN_gap_between_vessels_lv", material="Vacuum_cryo", shape=gap_s2)
        return vacuum_lv
    
    def placeSubVolume(self, geom, volume, subvolume, pos_x=Q("0mm"), pos_y=Q("0mm"), pos_z=Q("0mm"), rot_x=Q("0deg"), rot_y=Q("0deg"), rot_z=Q("0deg"), label=""):

        name     = subvolume.name + label
        position = geom.structure.Position(name + "_pos", pos_x, pos_y, pos_z)
        rotation = geom.structure.Rotation(name + "_rot", rot_x, rot_y, rot_z)
        place    = geom.structure.Placement(name + "_place", volume = subvolume.name, pos = position.name, rot = rotation.name)
        
        volume.placements.append(place.name)
