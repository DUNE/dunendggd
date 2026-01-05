""" InnerDetector.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class InnerDetectorBuilder(gegede.builder.Builder):
    """ Class to build InnerDetector geometry.

    """

    def configure(self, Side='both', **kwargs):

        # Material definitons
        self.Material           = 'G10'

        self.Side = Side

        # Subbuilders
        self.HalfDetector_builder = self.get_builder('HalfDetector')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   2*self.HalfDetector_builder.halfDimension['dx'],
                                'dy':   self.HalfDetector_builder.halfDimension['dy'],
                                'dz':   self.HalfDetector_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('InnerDetectorBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Build HalfDetector L
        if self.Side in ['left', 'both']:
            pos = [-self.HalfDetector_builder.halfDimension['dx'],Q('0cm'),Q('0cm')]

            HalfDetector_lv = self.HalfDetector_builder.get_volume()

            HalfDetector_pos = geom.structure.Position(self.HalfDetector_builder.name+'_pos_L',
                                                    pos[0],pos[1],pos[2])

            HalfDetector_pla = geom.structure.Placement(self.HalfDetector_builder.name+'_pla_L',
                                                    volume=HalfDetector_lv,
                                                    pos=HalfDetector_pos,
                                                    copynumber=0)

            main_lv.placements.append(HalfDetector_pla.name)

        # Build HalfDetector R
        if self.Side in ['right', 'both']:
            pos = [self.HalfDetector_builder.halfDimension['dx'],Q('0cm'),Q('0cm')]

            HalfDetector_lv = self.HalfDetector_builder.get_volume()

            HalfDetector_pos = geom.structure.Position(self.HalfDetector_builder.name+'_pos_R',
                                                    pos[0],pos[1],pos[2])

            rot = [Q('0.0deg'),Q('180.0deg'),Q('0.0deg')]

            HalfDetector_rot = geom.structure.Rotation(self.HalfDetector_builder.name+'_rot',
                                                    rot[0],rot[1],rot[2])

            HalfDetector_pla = geom.structure.Placement(self.HalfDetector_builder.name+'_pla_R',
                                                    volume=HalfDetector_lv,
                                                    pos=HalfDetector_pos,
                                                    rot=HalfDetector_rot,
                                                    copynumber=1)

            main_lv.placements.append(HalfDetector_pla.name)
