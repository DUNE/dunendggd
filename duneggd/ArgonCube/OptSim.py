""" OptSim.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class OptSimBuilder(gegede.builder.Builder):
    """ Class to build OptSim geometry.

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
        self.Kapton_dd      = Q('0.025mm')/2

        self.LAr_Material           = 'LAr'
        self.Bracket_Material       = 'G10'
        self.Kapton_Material        = 'Kapton'

        # Material definitons
        self.Material               = 'G10'

        # Subbuilders
        self.TPC_builder            = self.get_builder('TPC')
        self.OpticalDetL_builder    = self.TPC_builder.get_builder('OpticalDetL')
        self.OpticalDetR_builder    = self.TPC_builder.get_builder('OpticalDetR')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Fieldcage_dx+self.Cathode_dx/2,
                                'dy':   self.Fieldcage_dy,
                                'dz':   self.Fieldcage_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('OptSimBuilder::construct()')
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

        # Construct Capton Volume
        Kapton_shape = geom.shapes.Box('Kapton_shape',
                                        dx = self.Fieldcage_dx-self.Cathode_dx/2+self.Kapton_dd,
                                        dy = self.Fieldcage_dy-self.Fieldcage_dd*2+self.Kapton_dd*2,
                                        dz = self.Fieldcage_dz-self.Fieldcage_dd*2+self.Kapton_dd*2)

        Kapton_lv = geom.structure.Volume('volKapton',
                                        material=self.Kapton_Material,
                                        shape=Kapton_shape)

        # Place Capton Volume inside Fieldcage volume
        pos = [self.Kapton_dd,Q('0cm'),Q('0cm')]

        Kapton_pos = geom.structure.Position('Kapton_pos',
                                                pos[0],pos[1],pos[2])

        Kapton_pla = geom.structure.Placement('Kapton_pla',
                                                volume=Kapton_lv,
                                                pos=Kapton_pos)

        Fieldcage_lv.placements.append(Kapton_pla.name)

        # Construct LAr Volume
        LAr_shape = geom.shapes.Box('LAr_shape',
                                        dx = self.Fieldcage_dx-self.Cathode_dx/2,
                                        dy = self.Fieldcage_dy-self.Fieldcage_dd*2,
                                        dz = self.Fieldcage_dz-self.Fieldcage_dd*2)

        LAr_lv = geom.structure.Volume('volLAr',
                                        material=self.LAr_Material,
                                        shape=LAr_shape)

        # Place LAr Volume inside Fieldcage volume
        pos = [-self.Kapton_dd,Q('0cm'),Q('0cm')]

        LAr_pos = geom.structure.Position('LAr_pos',
                                                pos[0],pos[1],pos[2])

        LAr_pla = geom.structure.Placement('LAr_pla',
                                                volume=LAr_lv,
                                                pos=LAr_pos)

        Kapton_lv.placements.append(LAr_pla.name)

        # Build TPC
        pos = [self.Fieldcage_dx-self.TPC_builder.halfDimension['dx']-self.Cathode_dx/2,Q('0cm'),Q('0cm')]

        TPC_lv = self.TPC_builder.get_volume()

        TPC_pos = geom.structure.Position(self.TPC_builder.name+'_pos',
                                            pos[0],pos[1],pos[2])

        TPC_pla = geom.structure.Placement(self.TPC_builder.name+'_pla',
                                                volume=TPC_lv,
                                                pos=TPC_pos)

        LAr_lv.placements.append(TPC_pla.name)

        # Build OpticalDet R
        pos = [self.Fieldcage_dx-self.TPC_builder.halfDimension['dx']*2-self.Cathode_dx/2+self.OpticalDetR_builder.halfDimension['dx'],Q('0cm'),-self.TPC_builder.halfDimension['dz']-self.OpticalDetR_builder.halfDimension['dz']]

        OpticalDetR_lv = self.OpticalDetR_builder.get_volume()

        OpticalDetR_pos = geom.structure.Position(self.OpticalDetR_builder.name+'_pos_R',
                                                pos[0],pos[1],pos[2])

        OpticalDetR_pla = geom.structure.Placement(self.OpticalDetR_builder.name+'_pla_R',
                                                volume=OpticalDetR_lv,
                                                pos=OpticalDetR_pos,
                                                copynumber=0)

        LAr_lv.placements.append(OpticalDetR_pla.name)

        # Build OpticalDet L
        pos = [self.Fieldcage_dx-self.TPC_builder.halfDimension['dx']*2-self.Cathode_dx/2+self.OpticalDetL_builder.halfDimension['dx'],Q('0cm'),+self.TPC_builder.halfDimension['dz']+self.OpticalDetL_builder.halfDimension['dz']]

        OpticalDetL_lv = self.OpticalDetL_builder.get_volume()

        OpticalDetL_pos = geom.structure.Position(self.OpticalDetL_builder.name+'_pos_L',
                                                pos[0],pos[1],pos[2])

        rot = [Q('180.0deg'),Q('0.0deg'),Q('0.0deg')]

        OpticalDetL_rot = geom.structure.Rotation(self.OpticalDetL_builder.name+'_rot',
                                                rot[0],rot[1],rot[2])

        OpticalDetL_pla = geom.structure.Placement(self.OpticalDetL_builder.name+'_pla_L',
                                                volume=OpticalDetL_lv,
                                                pos=OpticalDetL_pos,
                                                rot=OpticalDetL_rot,
                                                copynumber=1)

        LAr_lv.placements.append(OpticalDetL_pla.name)

        # Construct Bracket Volume
        Bracket_shape = geom.shapes.Box('Bracket_shape',
                                        dx = self.Bracket_dx,
                                        dy = self.Bracket_dy,
                                        dz = self.OpticalDetL_builder.halfDimension['dz'])

        Bracket_lv = geom.structure.Volume('volBracket',
                                        material=self.Bracket_Material,
                                        shape=Bracket_shape)

        # Place Bracket Volume L inside Fieldcage volume
        pos = [self.Fieldcage_dx-self.Cathode_dx/2-self.Bracket_dx,Q('0cm'),-self.Fieldcage_dz+self.Fieldcage_dd*2+self.OpticalDetL_builder.halfDimension['dz']]

        Bracket_pos = geom.structure.Position('Bracket_pos_L',
                                                pos[0],pos[1],pos[2])

        Bracket_pla = geom.structure.Placement('Bracket_pla_L',
                                                volume=Bracket_lv,
                                                pos=Bracket_pos)

        LAr_lv.placements.append(Bracket_pla.name)

        # Place Bracket Volume R inside Fieldcage volume
        pos = [self.Fieldcage_dx-self.Cathode_dx/2-self.Bracket_dx,Q('0cm'),self.Fieldcage_dz-self.Fieldcage_dd*2-self.OpticalDetL_builder.halfDimension['dz']]

        Bracket_pos = geom.structure.Position('Bracket_pos_R',
                                                pos[0],pos[1],pos[2])

        Bracket_pla = geom.structure.Placement('Bracket_pla_R',
                                                volume=Bracket_lv,
                                                pos=Bracket_pos)

        LAr_lv.placements.append(Bracket_pla.name)

