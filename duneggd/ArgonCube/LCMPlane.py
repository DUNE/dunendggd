""" LCMPlane.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class LCMPlaneBuilder(gegede.builder.Builder):
    """ Class to build LCMPlane geometry.

    """

    def configure(self,LCM_pitch,N_LCM,**kwargs):

        # Read dimensions form config file
        self.LCM_pitch              = LCM_pitch
        self.N_LCM                  = int(N_LCM)

        # Material definitons
        self.Material               = 'LAr'

        # Subbuilders
        self.LCM_builder            = self.get_builder('LCM')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension      = { 'dx':   self.LCM_builder.halfDimension['dx'],

                                    'dy':   self.LCM_builder.halfDimension['dy']+self.LCM_pitch*(self.N_LCM-1),

                                    'dz':   self.LCM_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('LCMPlaneBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Build ArCLight Array
        for i in range(self.N_LCM):
                pos = [Q('0cm'),-self.halfDimension['dy']+self.LCM_builder.halfDimension['dy']+i*2*self.LCM_pitch,Q('0cm')]

                LCM_lv = self.LCM_builder.get_volume()

                LCM_pos = geom.structure.Position(self.LCM_builder.name+'_pos_'+str(i),
                                                    pos[0],pos[1],pos[2])

                LCM_pla = geom.structure.Placement(self.LCM_builder.name+'_pla_'+str(i),
                                                        volume=LCM_lv,
                                                        pos=LCM_pos,
                                                        copynumber=i)

                main_lv.placements.append(LCM_pla.name)

