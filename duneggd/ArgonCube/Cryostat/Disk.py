#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q
import numpy as np


class DiskBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dz=None, rmin=None, rmax=None,
                    Material=None, **kwds ):
        self.rmin, self.rmax, self.dz= (rmin, rmax, dz)
        self.Material = Material

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        disk_shape = geom.shapes.Tubs( self.name+'Disk', rmin=self.rmin, rmax=self.rmax, dz=self.dz)
        disk_lv = geom.structure.Volume( "vol"+disk_shape.name, material=self.Material, shape=disk_shape )
        
        self.add_volume( disk_lv )      
