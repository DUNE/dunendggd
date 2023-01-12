#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q


class KLOESTTBuilder(gegede.builder.Builder):

    def configure( self, halfDimension=None, Material=None, nModules=None,
                   gap=None, startingOffset=None, modWidth=None, modRot=None, **kwds):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.nModules=nModules
        self.gap=gap
        self.startingOffset=startingOffset
        self.modWidth=modWidth
        self.modRot=modRot
        pass

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # main volume
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        print( "KLOESTT::construct()")
        print(( "  main_lv = "+ main_lv.name))
        self.add_volume( main_lv )

        rot=[Q("0deg"),Q("0deg"),Q("0deg")]
        if self.modRot!=None:
            rot=self.modRot

        mod_builder=self.get_builder("STTModule")
        mod_lv=mod_builder.get_volume()
        # build modules starting from -z edge of KLOESTT
        # startingOffset moves us away from the edge (e.g., to center the array of modules in z)
        startz=-main_hDim[2]+self.startingOffset
        for imod in range(self.nModules):
            loc=[Q("0cm"),Q("0cm"),startz+(self.modWidth+self.gap)*(imod+0.5)]
            basename=self.name+'_'+mod_lv.name+'_'+str(imod)
            print(( "Placing STTModule " + basename+" at "+str(loc)))
            mod_pos=geom.structure.Position(basename+'_pos',loc[0],loc[1],loc[2])
            mod_rot=geom.structure.Rotation(basename+'_rot',rot[0],rot[1],rot[2])
            mod_pla=geom.structure.Placement(basename+'_pla',volume=mod_lv,pos=mod_pos,rot=mod_rot)
            main_lv.placements.append(mod_pla.name)



