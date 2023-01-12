""" Module.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class ModuleBuilder(gegede.builder.Builder):
    """ Class to build Module geometry.

    """

    def configure(self,**kwargs):

        # Material definitons

        self.Material   = 'Air'

        # Subbuilders
        self.Bucket_builder         = self.get_builder('Bucket')
        self.Flange_builder         = self.get_builder('Flange')
        self.HVFeedThrough_builder  = self.get_builder('HVFeedThrough')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Flange_builder.halfDimension['dx'],
                                'dy':   self.Bucket_builder.halfDimension['dy']+self.Flange_builder.halfDimension['dy'],
                                'dz':   self.Flange_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ModuleBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Build Bucket
        pos = [Q('0cm'),-self.halfDimension['dy']+self.Bucket_builder.halfDimension['dy'],Q('0cm')]

        Bucket_lv = self.Bucket_builder.get_volume()

        Bucket_pos = geom.structure.Position(self.Bucket_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Bucket_pla = geom.structure.Placement(self.Bucket_builder.name+'_pla',
                                                volume=Bucket_lv,
                                                pos=Bucket_pos)

        main_lv.placements.append(Bucket_pla.name)

        # Build Flange
        pos = [Q('0cm'),-self.halfDimension['dy']+2*self.Bucket_builder.halfDimension['dy']+self.Flange_builder.halfDimension['dy'],Q('0cm')]

        Flange_lv = self.Flange_builder.get_volume()

        Flange_pos = geom.structure.Position(self.Flange_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        Flange_pla = geom.structure.Placement(self.Flange_builder.name+'_pla',
                                                volume=Flange_lv,
                                                pos=Flange_pos)

        main_lv.placements.append(Flange_pla.name)

        # Build HVFeedThrough
        pos = [Q('0cm'),-self.halfDimension['dy']+self.HVFeedThrough_builder.halfDimension['dz'],Q('0cm')]

        rot = [Q('90.0deg'),Q('0.0deg'),Q('0.0deg')]

        HVFeedThrough_lv = self.HVFeedThrough_builder.get_volume()

        HVFeedThrough_pos = geom.structure.Position(self.HVFeedThrough_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        HVFeedThrough_rot = geom.structure.Rotation(self.HVFeedThrough_builder.name+'_rot',
                                                rot[0],rot[1],rot[2])

        HVFeedThrough_pla = geom.structure.Placement(self.HVFeedThrough_builder.name+'_pla',
                                                volume=HVFeedThrough_lv,
                                                pos=HVFeedThrough_pos,
                                                rot=HVFeedThrough_rot)

        #main_lv.placements.append(HVFeedThrough_pla.name)

