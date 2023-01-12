""" HalfDetector.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class HalfDetectorBuilder(gegede.builder.Builder):
    """ Class to build HalfDetector geometry.

    """

    def configure(self,Fieldcage_dimension,Bracket_dimension,Cathode_dx,**kwargs):

        # Read dimensions form config file
        self.Fieldcage_dx   = Fieldcage_dimension['dx']
        self.Fieldcage_dy   = Fieldcage_dimension['dy']
        self.Fieldcage_dz   = Fieldcage_dimension['dz']
        self.Fieldcage_dd   = Fieldcage_dimension['dd']

        self.Bracket_dx     = Bracket_dimension['dx']
        self.Bracket_dy     = Bracket_dimension['dy']

        self.Cathode_dx     = Cathode_dx

        # Material definitons
        self.LAr_Material           = 'LAr'
        self.Bracket_Material       = 'G10'

        self.Material               = 'G10'

        # Subbuilders
        self.TPC_builder            = self.get_builder('TPC')
        self.OpticalDet_builder     = self.TPC_builder.get_builder('OpticalDet')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Fieldcage_dx,
                                'dy':   self.Fieldcage_dy,
                                'dz':   self.Fieldcage_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('HalfDetectorBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Construct Fieldcage
        Fieldcage_shape = geom.shapes.Box('Fieldcage_shape',
                                        dx = self.halfDimension['dx'],
                                        dy = self.halfDimension['dy'],
                                        dz = self.halfDimension['dz'])

        Fieldcage_lv = geom.structure.Volume('volFieldcage',
                                        material=self.Material,
                                        shape=Fieldcage_shape)

        # Place Fieldcage
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        Fieldcage_pos = geom.structure.Position('Fieldcage_pos',
                                                pos[0],pos[1],pos[2])

        Fieldcage_pla = geom.structure.Placement('Fieldcage_pla',
                                                volume=Fieldcage_lv,
                                                pos=Fieldcage_pos)

        main_lv.placements.append(Fieldcage_pla.name)

        # Construct LAr Volume
        LAr_shape = geom.shapes.Box('LAr_shape',
                                        dx = self.Fieldcage_dx-self.Cathode_dx/2,
                                        dy = self.Fieldcage_dy-self.Fieldcage_dd*2,
                                        dz = self.Fieldcage_dz-self.Fieldcage_dd*2)

        LAr_lv = geom.structure.Volume('volLAr',
                                        material=self.LAr_Material,
                                        shape=LAr_shape)

        # Place LAr Volume inside Fieldcage volume
        pos = [-self.Cathode_dx/2,Q('0cm'),Q('0cm')]

        LAr_pos = geom.structure.Position('LAr_pos',
                                                pos[0],pos[1],pos[2])

        LAr_pla = geom.structure.Placement('LAr_pla',
                                                volume=LAr_lv,
                                                pos=LAr_pos)

        Fieldcage_lv.placements.append(LAr_pla.name)

        # Build TPC
        pos = [
            self.Fieldcage_dx-self.TPC_builder.halfDimension['dx']-self.Cathode_dx/2,
            Q('0cm'),
            Q('0cm')
        ]

        TPC_lv = self.TPC_builder.get_volume()

        TPC_pos = geom.structure.Position(self.TPC_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        TPC_pla = geom.structure.Placement(self.TPC_builder.name+'_pla',
                                                volume=TPC_lv,
                                                pos=TPC_pos)

        LAr_lv.placements.append(TPC_pla.name)

        # Build OpticalDets and Brackets
        OpticalDet_lv = self.OpticalDet_builder.get_volume()
        OpticalDet_rot_R = geom.structure.Rotation(self.OpticalDet_builder.name+'_rot',
                                                 Q('180.0deg'),Q('0.0deg'),Q('0.0deg'))

        Bracket_shape = geom.shapes.Box('Bracket_shape',
                                        dx = self.Bracket_dx,
                                        dy = self.Bracket_dy,
                                        dz = self.OpticalDet_builder.halfDimension['dz'])

        Bracket_lv = geom.structure.Volume('volBracket',
                                        material=self.Bracket_Material,
                                        shape=Bracket_shape)

        for side, sign in (('L', -1), ('R', 1)):
            # OpticalDet
            pos = [
                self.Fieldcage_dx-self.TPC_builder.halfDimension['dx']*2-self.Cathode_dx/2+self.OpticalDet_builder.halfDimension['dx'],
                Q('0cm'),
                sign*(self.TPC_builder.halfDimension['dz']+self.OpticalDet_builder.halfDimension['dz'])
            ]

            OpticalDet_pos = geom.structure.Position(self.OpticalDet_builder.name+'_pos_'+side,
                                                    pos[0],pos[1],pos[2])

            OpticalDet_rot = OpticalDet_rot_R if side == 'R' else None

            OpticalDet_pla = geom.structure.Placement(self.OpticalDet_builder.name+'_pla_'+side,
                                                    volume=OpticalDet_lv,
                                                    pos=OpticalDet_pos,
                                                    rot=OpticalDet_rot)

            LAr_lv.placements.append(OpticalDet_pla.name)

            # Bracket
            pos = [
                self.Fieldcage_dx-self.Cathode_dx/2-self.Bracket_dx,
                Q('0cm'),
                sign*(self.Fieldcage_dz-self.Fieldcage_dd*2-self.OpticalDet_builder.halfDimension['dz'])
            ]

            Bracket_pos = geom.structure.Position('Bracket_pos_'+side,
                                                    pos[0],pos[1],pos[2])

            Bracket_pla = geom.structure.Placement('Bracket_pla_'+side,
                                                    volume=Bracket_lv,
                                                    pos=Bracket_pos)

            #LAr_lv.placements.append(Bracket_pla.name)

