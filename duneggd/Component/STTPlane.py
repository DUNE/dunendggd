#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q


class STTPlaneBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, NElements=None,
                    BeginGap=None, InsideGap=None, Rotation=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.NElements, self.BeginGap = ( NElements, BeginGap )
        self.InsideGap, self.Rotation  = ( InsideGap, Rotation )
        pass

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        self.add_volume( main_lv )

        # definition local rotation
        rotation = ltools.getRotation( self, geom )

        InsideGap = ltools.getInsideGap( self )

        if self.NElements != None:
            # get sub-builders and its logic volume
            sb = self.get_builder()
            sb_lv = sb.get_volume()
            sb_dim = ltools.getShapeDimensions( sb_lv, geom )

#            TranspV = [1,0,0] #MAK: not used

            # initial position, particular case
            pos = [-main_hDim[0]+sb_dim[0]*0.5, Q('0m'), Q('0m')]
            print(( "STTPlane sb_dim[]= "+str(sb_dim)))
            for elem in range(self.NElements):
                pos = [ sb_dim[0]*0.5+pos[0], pos[1]-math.pow(-1,elem+1)*sb_dim[0]*math.sqrt(3)*0.5, pos[2] ]
                sb_pos = geom.structure.Position(self.name+sb_lv.name+str(elem)+'_pos',
                                                    pos[0], pos[1], pos[2])
                sb_pla = geom.structure.Placement(self.name+sb_lv.name+str(elem)+'_pla',
                                                    volume=sb_lv, pos=sb_pos, rot =rotation)
                main_lv.placements.append(sb_pla.name)
                pos = [ sb_dim[0]*0.5+pos[0], pos[1]+math.pow(-1,elem+1)*sb_dim[0]*math.sqrt(3)*0.5, pos[2] ]
