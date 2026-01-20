#!/usr/bin/env python3

from gegede import Quantity as Q
from gegede.builder import Builder
from duneggd.LocalTools.materialdefinition import define_materials


class GCWorldBuilder(Builder):
    def configure(self, halfDimension={}, **kwds):
        self.halfDimension = halfDimension

    def construct(self, geom):
        define_materials(geom)

        worldBox = geom.shapes.Box(self.name,
                                   dx=self.halfDimension['dx'],
                                   dy=self.halfDimension['dy'],
                                   dz=self.halfDimension['dz'])
        worldVol = geom.structure.Volume(
            'vol'+self.name, material='Vac', shape=worldBox)
        self.add_volume(worldVol)

        tpcName = 'TPCActive'
        tpcBox = geom.shapes.Box(tpcName,
                                 dx=0.5*self.halfDimension['dx'],
                                 dy=self.halfDimension['dy'],
                                 dz=self.halfDimension['dz'])
        tpcVol = geom.structure.Volume(
            'vol'+tpcName, material='LAr', shape=tpcBox,
            params=[('SensDet', 'vol'+tpcName)])

        tpcPos = geom.structure.Position(
            tpcVol.name+'_pos', 0.5*self.halfDimension['dx'], Q('0m'), Q('0m'))
        tpcPla = geom.structure.Placement(
            tpcVol.name+'_pla', volume=tpcVol, pos=tpcPos)
        worldVol.placements.append(tpcPla.name)
