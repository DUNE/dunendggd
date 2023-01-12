""" Detector.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class DetectorBuilder(gegede.builder.Builder):
    """ Class to build Detector geometry.

    """

    def configure(self,N_ModuleX,N_ModuleZ,**kwargs):

        # Read dimensions form config file

        # Material definitons

        self.Material   = 'Air'
        self.N_ModuleX  = N_ModuleX
        self.N_ModuleZ  = N_ModuleZ

        # Subbuilders
        self.Module_builder         = self.get_builder('Module')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Module_builder.halfDimension['dx']*self.N_ModuleX,
                                'dy':   self.Module_builder.halfDimension['dy'],
                                'dz':   self.Module_builder.halfDimension['dz']*self.N_ModuleZ}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('DetectorBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Build Module
        for i in range(self.N_ModuleX):
            for j in range(self.N_ModuleZ):
                pos = [-self.halfDimension['dx']+(2*i+1)*self.Module_builder.halfDimension['dx'],Q('0cm'),-self.halfDimension['dz']+(2*j+1)*self.Module_builder.halfDimension['dz']]

                Module_lv = self.Module_builder.get_volume()

                Module_pos = geom.structure.Position(self.Module_builder.name+'_pos_'+str(i)+'.'+str(j),
                                                        pos[0],pos[1],pos[2])

                Module_pla = geom.structure.Placement(self.Module_builder.name+'_pla_'+str(i)+'.'+str(j),
                                                        volume=Module_lv,
                                                        pos=Module_pos,
                                                        copynumber=2*j+i)

                main_lv.placements.append(Module_pla.name)

