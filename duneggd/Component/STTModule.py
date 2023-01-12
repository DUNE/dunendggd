#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q


class STTModuleBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, NElements=None,
                   centerPlane1=None, centerPlane2=None,
                   rotationPlane1=None, rotationPlane2=None , 
                   radiators=False, radiatorOffset=None,
                   radiator1HalfDimension=None, radiator2HalfDimension=None,
                   **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.NElements=NElements
        self.centerPlane1, self.centerPlane2 = (centerPlane1,centerPlane2)
        self.rotationPlane1, self.rotationPlane2 = (rotationPlane1,rotationPlane2)
        self.radiators=radiators
        self.radiatorOffset=radiatorOffset
        self.radiator1HalfDimension=radiator1HalfDimension
        self.radiator2HalfDimension=radiator2HalfDimension

        pass

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # main volume
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        print( "STTModule::construct()")
        print(( "  main_lv = "+ main_lv.name))
        self.add_volume( main_lv )

        # Straw Plane 1
        plane1_builder=self.get_builder("STTPlane1")
        print(( "plane1_builder="+str(plane1_builder)))
        plane1_lv=plane1_builder.get_volume()
        plane1_pos=geom.structure.Position(self.name+'_Plane1_pos',
                                           self.centerPlane1[0],self.centerPlane1[1],self.centerPlane1[2])
        plane1_rot=geom.structure.Rotation(self.name+'_Plane1_rot',
                                           self.rotationPlane1[0],self.rotationPlane1[1],self.rotationPlane1[2])
        plane1_pla=geom.structure.Placement(self.name+'_Plane1_pla',volume=plane1_lv, pos=plane1_pos, rot=plane1_rot) 

        main_lv.placements.append(plane1_pla.name)

        # Straw Plane 2
        plane2_builder=self.get_builder("STTPlane2")
        print(( "plane2_builder="+str(plane2_builder)))
        plane2_lv=plane2_builder.get_volume()
        plane2_pos=geom.structure.Position(self.name+'_Plane2_pos',
                                           self.centerPlane2[0],self.centerPlane2[1],self.centerPlane2[2])
        plane2_rot=geom.structure.Rotation(self.name+'_Plane2_rot',
                                           self.rotationPlane2[0],self.rotationPlane2[1],self.rotationPlane2[2])
        plane2_pla=geom.structure.Placement(self.name+'_Plane2_pla',volume=plane2_lv, pos=plane2_pos, rot=plane2_rot) 

        main_lv.placements.append(plane2_pla.name)
        
        # build the 4 radiators
        if self.radiators:
            # center of the radiator modules along y
            radiator_position=[ [self.centerPlane1[0],self.centerPlane1[1]-self.radiatorOffset,self.centerPlane1[2]],
                                [self.centerPlane1[0],self.centerPlane1[1]+self.radiatorOffset,self.centerPlane1[2]],
                                [self.centerPlane2[0],self.centerPlane2[1]-self.radiatorOffset,self.centerPlane2[2]],
                                [self.centerPlane2[0],self.centerPlane2[1]+self.radiatorOffset,self.centerPlane2[2]]
                                ]
            radiator_rotation=[ [self.rotationPlane1[0],self.rotationPlane1[1],self.rotationPlane1[2]],
                                [self.rotationPlane1[0],self.rotationPlane1[1],self.rotationPlane1[2]],
                                [self.rotationPlane2[0],self.rotationPlane2[1],self.rotationPlane2[2]],
                                [self.rotationPlane2[0],self.rotationPlane2[1],self.rotationPlane2[2]]
                                ]
            radiator_hd=[ self.radiator1HalfDimension, self.radiator1HalfDimension,
                          self.radiator2HalfDimension, self.radiator2HalfDimension 
                          ]
            radiator_name= ['1A','1B','2A','2B']
            for pos,rot,hd,rname in zip(radiator_position,radiator_rotation,radiator_hd,radiator_name):
                basename='STTModule_Radiator_'+rname
                rad_shape=geom.shapes.Box(basename,hd[0],hd[1],hd[2])
                rad_lv=geom.structure.Volume(basename+"_vol",material="RadiatorBlend",shape=rad_shape)
                rad_pos=geom.structure.Position(basename+"_pos",pos[0],pos[1],pos[2])
                rad_rot=geom.structure.Rotation(basename+"_rot",rot[0],rot[1],rot[2])
                rad_pla=geom.structure.Placement(basename+"_pla",volume=rad_lv,pos=rad_pos,rot=rad_rot)
                main_lv.placements.append(rad_pla.name)
        
