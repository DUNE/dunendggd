""" HVFeedThrough.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class HVFeedThroughBuilder(gegede.builder.Builder):
    """ Class to build HVFeedThrough geometry.

    """

    def configure(self,Insulation_dimension,Core_rmax,**kwargs):

        # Read dimensions form config file
        self.Insulation_rmin        = Insulation_dimension['rmin']
        self.Insulation_rmax        = Insulation_dimension['rmax']
        self.Insulation_dz          = Insulation_dimension['dz']

        self.Core_rmax              = Core_rmax

        # Material definitons
        self.Insulation_Material    = 'PVT'
        self.Core_Material          = 'Copper'

        self.Material               = 'Air'

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'rmin': self.Insulation_rmin,
                                'rmax': self.Insulation_rmax,
                                'dz':   self.Insulation_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Tubs')
        print('HVFeedThroughBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Construct Insulation Volume
        Insulation_shape = geom.shapes.Tubs('Insulation_shape',
                                        rmin = self.halfDimension['rmin'],
                                        rmax = self.halfDimension['rmax'],
                                        dz = self.halfDimension['dz'])

        Insulation_lv = geom.structure.Volume('volInsulation',
                                        material=self.Insulation_Material,
                                        shape=Insulation_shape)

        # Place Insulation Volume inside HVFeedThrough volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        Insulation_pos = geom.structure.Position('Insulation_pos',
                                                pos[0],pos[1],pos[2])

        Insulation_pla = geom.structure.Placement('Insulation_pla',
                                                volume=Insulation_lv,
                                                pos=Insulation_pos)

        main_lv.placements.append(Insulation_pla.name)

        # Construct Core Volume
        Core_shape = geom.shapes.Tubs('Core_shape',
                                        rmin = Q('0mm'),
                                        rmax = self.Core_rmax,
                                        dz = self.halfDimension['dz'])

        Core_lv = geom.structure.Volume('volCore',
                                        material=self.Core_Material,
                                        shape=Core_shape)

        # Place Core Volume inside HVFeedThrough volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        Core_pos = geom.structure.Position('Core_pos',
                                                pos[0],pos[1],pos[2])

        Core_pla = geom.structure.Placement('Core_pla',
                                                volume=Core_lv,
                                                pos=Core_pos)

        main_lv.placements.append(Core_pla.name)

