#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q
import numpy as np

class ContainerBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, positions=None, **kwds ):
        self.positions = positions

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # container
        cont_lv=geom.structure.Volume( "vol"+self.name, material=None, shape=None )
        self.add_volume( cont_lv )

        # we will handle the connections, inlets, legs seperately
        sbs = self.get_builders()

        # place the first components
        for i, (sb, pos) in enumerate(zip(sbs, self.positions)):
            sb_lv = sb.get_volume()
            sb_pos = geom.structure.Position(self.name+sb_lv.name+'_pos',
                                             pos[0], pos[1], pos[2])     
            sb_rot = geom.structure.Rotation(self.name+sb_lv.name+'_rot',
                                             '0.0deg', '0.0deg', '0.0deg')                            
            sb_pla = geom.structure.Placement(self.name+sb_lv.name+'_pla',
                                              volume=sb_lv, pos=sb_pos, rot=sb_rot)
            cont_lv.placements.append(sb_pla.name)
