""" Backplate.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class BackplateBuilder(gegede.builder.Builder):
    """ Class to build Backplate geometry.

    """

    def configure(self,Backplate_dimension,Backplate_Gap,Backplate_btm_off,**kwargs):

        # Read dimensions form config file
        self.Backplate_dx           = Backplate_dimension['dx']
        self.Backplate_dy           = Backplate_dimension['dy']
        self.Backplate_dz           = Backplate_dimension['dz']

        self.Backplate_Gap_dy       = Backplate_Gap['dy']
        self.Backplate_Gap_dz       = Backplate_Gap['dz']

        self.Backplate_btm_off      = Backplate_btm_off

        # Material definitons
        self.Gap_Material   = 'LAr'

        self.Material       = 'G10'

        # Subbuilders
        self.TPC_builder        = self.get_builder('TPC')
        self.OpticalDet_builder = self.TPC_builder.get_builder('OpticalDet')
        self.TPCPlane_builder   = self.OpticalDet_builder.get_builder('TPCPlane')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.Backplate_top_off = self.Backplate_dy-self.TPCPlane_builder.halfDimension['dy']-self.Backplate_btm_off

        self.N_Gap = self.TPCPlane_builder.N_UnitsY

        self.halfDimension  = { 'dx':   self.Backplate_dx,
                                'dy':   self.Backplate_dy,
                                'dz':   self.Backplate_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('BackplateBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Construct Backplate Gap Volume
        BackplateGap_shape = geom.shapes.Box('BackplateGap_shape',
                                        dx = self.Backplate_dx,
                                        dy = self.Backplate_Gap_dy,
                                        dz = self.Backplate_Gap_dz)

        BackplateGap_lv = geom.structure.Volume('volBackplateGap',
                                        material=self.Gap_Material,
                                        shape=BackplateGap_shape)

        # Place Backplate Gap Volume inside Backplate volume
        for i in range(2):
            for j in range(self.N_Gap):
                pos = [Q('0cm'),self.TPCPlane_builder.halfDimension['dy']/self.N_Gap*(3-2*j)-self.Backplate_top_off+self.Backplate_btm_off,(-1)**i*(self.Backplate_dz-self.Backplate_Gap_dz)]

                BackplateGap_pos = geom.structure.Position('BackplateGap_pos_'+str(i*self.N_Gap+j),
                                                        pos[0],pos[1],pos[2])

                BackplateGap_pla = geom.structure.Placement('BackplateGap_pla_'+str(i*self.N_Gap+j),
                                                        volume=BackplateGap_lv,
                                                        pos=BackplateGap_pos)

                main_lv.placements.append(BackplateGap_pla.name)

