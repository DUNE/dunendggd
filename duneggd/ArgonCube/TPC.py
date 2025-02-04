""" TPC.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class TPCBuilder(gegede.builder.Builder):
    """ Class to build TPC geometry.

    """

    def configure(self,Drift_Length,**kwargs):

        # Read dimensions form config file
        self.Drift_Length       = Drift_Length

        # Material definitons
        self.Material           = 'LAr'

        # Subbuilders
        self.OpticalDet_builder = self.get_builder('OpticalDet')
        self.TPCPlane_builder   = self.OpticalDet_builder.get_builder('TPCPlane')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Drift_Length
                                        +self.TPCPlane_builder.halfDimension['dx'],

                                'dy':   self.TPCPlane_builder.halfDimension['dy'],
                                'dz':   self.TPCPlane_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('TPCBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Build TPCPlane
        pos = [-self.Drift_Length,Q('0mm'),Q('0mm')]

        TPCPlane_lv = self.TPCPlane_builder.get_volume()

        TPCPlane_pos = geom.structure.Position(self.TPCPlane_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        TPCPlane_pla = geom.structure.Placement(self.TPCPlane_builder.name+'_pla',
                                                volume=TPCPlane_lv,
                                                pos=TPCPlane_pos)

        main_lv.placements.append(TPCPlane_pla.name)

        # Construct TPCActive
        TPCActive_shape = geom.shapes.Box('TPCActive_shape',
                                        dx =    self.Drift_Length,
                                        dy =    self.TPCPlane_builder.halfDimension['dy'],
                                        dz =    self.TPCPlane_builder.halfDimension['dz'])

        TPCActive_lv = geom.structure.Volume('volTPCActive',
                                        material=self.Material,
                                        shape=TPCActive_shape)

        TPCActive_lv.params.append(("SensDet","TPCActive_shape"))
        TPCActive_lv.params.append(("EField","(500.0 V/cm, 0.0 V/cm, 0.0 V/cm)"))

        # Place TPCActive
        pos = [self.TPCPlane_builder.halfDimension['dx'],Q('0cm'),Q('0cm')]

        TPCActive_pos = geom.structure.Position('TPCActive_pos',
                                                pos[0],pos[1],pos[2])

        TPCActive_pla = geom.structure.Placement('TPCActive_pla',
                                                volume=TPCActive_lv,
                                                pos=TPCActive_pos)

        main_lv.placements.append(TPCActive_pla.name)

        # Place E-Field
        #TPCActive_lv.params.append(("EField",self.EField))
