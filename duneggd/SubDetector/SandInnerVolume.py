import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class SandInnerVolumeBuilder(gegede.builder.Builder):
    def configure( self, halfDimension=None, Material=None, nBarrelModules=None, GRAINThickness=None, clearenceECALGRAIN=None, clearenceGRAINTracker=None, clearenceTrackerECAL=None,**kwds):
        self.halfDimension = halfDimension
        self.Material =      Material
        self.kloeVesselRadius       = self.halfDimension['rmax']
        self.kloeVesselHalfDx       = self.halfDimension['dz']
        self.nBarrelModules         = nBarrelModules
        self.rotAngle               = 0.5 * Q('360deg') / self.nBarrelModules
        self.GRAINThickness         = GRAINThickness

        self.clearenceECALGRAIN     = clearenceECALGRAIN
        self.clearenceGRAINTracker  = clearenceGRAINTracker
        self.clearenceTrackerECAL   = clearenceTrackerECAL

    def construct(self,geom):
        sand_inner_volume_shape = geom.shapes.PolyhedraRegular("sand_inner_volume_shape",numsides=self.nBarrelModules, rmin=Q('0cm'), rmax=self.kloeVesselRadius , dz=self.kloeVesselHalfDx, sphi=self.rotAngle)
        #sand_inner_volume_shape = geom.shapes.Tubs("sand_inner_volume_shape", rmin = Q("0mm"), rmax = self.kloeVesselRadius, dz=self.kloeVesselHalfDx/2)
        main_lv                 = geom.structure.Volume('sand_inner_volume',   material=self.Material, shape=sand_inner_volume_shape)
        self.add_volume( main_lv )
        self.build_tracker(main_lv, geom)
        self.build_grain(main_lv, geom)

    def build_tracker(self, main_lv, geom):
        # if "STT" not in self.builders:
        #     print("STT builder not found")
        #     return  
        if "STT" in self.builders:
            print("STT builder found")
            tracker_builder=self.get_builder("STT")
        elif "SAND_TRACKER" in self.builders:
            tracker_builder=self.get_builder("SAND_TRACKER")
        else:
            print("no SAND tracker found")
            return
        
        
        tracker_lv=tracker_builder.get_volume()

        tracker_position = geom.structure.Position(
                'tracker_position', Q('0m'), Q('0m'), Q('0m'))

        tracker_rotation = geom.structure.Rotation(
                'tracker_rotation', Q('0deg'), Q('180deg'), Q('0deg'))

        tracker_placement = geom.structure.Placement('tracker_place',
                                                  volume=tracker_lv,
                                                  pos=tracker_position,
                                                  rot=tracker_rotation)

        main_lv.placements.append(tracker_placement.name) 

    def build_grain(self, main_lv, geom):
        if "GRAIN" not in self.builders:
            print("GRAIN builder not found")
            return        

        grain_builder=self.get_builder("GRAIN")
        grain_lv=grain_builder.get_volume()
        
        grain_position = geom.structure.Position("grain_position",
                                      self.kloeVesselRadius - 0.5*self.GRAINThickness - self.clearenceECALGRAIN,
                                      Q('0mm'),
                                      Q('0mm'))

        grain_rotation = geom.structure.Rotation(
                'grain_rotation', Q('0deg'), Q('0deg'), Q('0deg'))

        grain_placement = geom.structure.Placement('grain_place',
                                                  volume=grain_lv,
                                                  pos=grain_position,
                                                  rot=grain_rotation)
        main_lv.placements.append(grain_placement.name) 
        