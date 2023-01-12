""" Pillow.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class PillowBuilder(gegede.builder.Builder):
    """ Class to build Pillow geometry.

    """

    def configure(self,Pillow_dimension,PillowSide_dimension,PillowBottom_dy,AngleBarTop_dimension,AngleBarSide_dimension,Angle_Length,Angle_dd,N_Angle,G10_dz,**kwargs):

        # Read dimensions form config file
        self.PillowSide_dx      = PillowSide_dimension['dx']
        self.PillowSide_dy      = PillowSide_dimension['dy']
        self.PillowSide_dz      = PillowSide_dimension['dz']
        self.PillowSide_dd      = PillowSide_dimension['dd']

        self.PillowBottom_dy    = PillowBottom_dy

        self.AngleBarTop_dx     = AngleBarTop_dimension['dx']
        self.AngleBarTop_dy     = AngleBarTop_dimension['dy']
        self.AngleBarTop_dz     = AngleBarTop_dimension['dz']
        self.AngleBarTop_gap    = AngleBarTop_dimension['gap']

        self.AngleBarSide_dx    = AngleBarSide_dimension['dx']
        self.AngleBarSide_dy    = AngleBarSide_dimension['dy']
        self.AngleBarSide_dz    = AngleBarSide_dimension['dz']

        self.Angle_Length       = Angle_Length
        self.Angle_dd           = Angle_dd
        self.N_Angle            = N_Angle
        self.Angle_gap          = (self.AngleBarTop_dz-self.Angle_Length*self.N_Angle)/(self.N_Angle-1)

        self.G10_dz             = G10_dz

        self.Pillow_dx          = Pillow_dimension['dx']
        self.Pillow_dy          = self.PillowSide_dy+self.AngleBarTop_dy+self.AngleBarTop_dx
        self.Pillow_dz          = Pillow_dimension['dz']

        # Material definitons
        self.Pillow_Material    = 'Steel'
        self.Vacuum_Material    = 'Vac'
        self.G10_Material       = 'G10'

        self.Material           = 'GAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Pillow_dx,
                                'dy':   self.Pillow_dy,
                                'dz':   self.Pillow_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('PillowBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Construct Pillow Side Volume
        PillowSide_shape = geom.shapes.Box('PillowSide_shape',
                                        dx = self.PillowSide_dx,
                                        dy = self.PillowSide_dy,
                                        dz = self.PillowSide_dz)

        PillowSide_lv = geom.structure.Volume('volPillowSide',
                                        material=self.Pillow_Material,
                                        shape=PillowSide_shape)

        # Place Pillow Side Volume inside Pillow volume
        pos = [Q('0cm'),self.Pillow_dy-self.PillowSide_dy,Q('0cm')]

        PillowSide_pos = geom.structure.Position('PillowSide_pos',
                                                pos[0],pos[1],pos[2])

        PillowSide_pla = geom.structure.Placement('PillowSide_pla',
                                                volume=PillowSide_lv,
                                                pos=PillowSide_pos)

        main_lv.placements.append(PillowSide_pla.name)

        # Construct Pillow Cavity Volume
        PillowCavity_shape = geom.shapes.Box('PillowCavity_shape',
                                        dx = self.PillowSide_dx-2*self.PillowSide_dd,
                                        dy = self.PillowSide_dy-self.PillowBottom_dy,
                                        dz = self.PillowSide_dz-2*self.PillowSide_dd)

        PillowCavity_lv = geom.structure.Volume('volPillowCavity',
                                        material=self.Vacuum_Material,
                                        shape=PillowCavity_shape)

        # Place Pillow Cavity Volume inside Pillow Side volume
        pos = [Q('0cm'),self.PillowBottom_dy,Q('0cm')]

        PillowCavity_pos = geom.structure.Position('PillowCavity_pos',
                                                pos[0],pos[1],pos[2])

        PillowCavity_pla = geom.structure.Placement('PillowCavity_pla',
                                                volume=PillowCavity_lv,
                                                pos=PillowCavity_pos)

        PillowSide_lv.placements.append(PillowCavity_pla.name)

        # Construct Angle Bar Top Volume
        AngleBarTop_shape = geom.shapes.Box('AngleBarTop_shape',
                                        dx = self.AngleBarTop_dx,
                                        dy = self.AngleBarTop_dy,
                                        dz = self.AngleBarTop_dz)

        AngleBarTop_lv = geom.structure.Volume('volAngleBarTop',
                                        material=self.Pillow_Material,
                                        shape=AngleBarTop_shape)

        # Place Angle Bar Top L Volume inside Pillow volume
        pos = [-self.AngleBarTop_gap-self.AngleBarTop_dx,self.Pillow_dy-2*self.PillowSide_dy-self.AngleBarTop_dy,Q('0cm')]

        AngleBarTop_L_pos = geom.structure.Position('AngleBarTop_L_pos',
                                                pos[0],pos[1],pos[2])

        AngleBarTop_L_pla = geom.structure.Placement('AngleBarTop_L_pla',
                                                volume=AngleBarTop_lv,
                                                pos=AngleBarTop_L_pos)

        main_lv.placements.append(AngleBarTop_L_pla.name)

        # Place Angle Bar Top R Volume inside Pillow volume
        pos = [self.AngleBarTop_gap+self.AngleBarTop_dx,self.Pillow_dy-2*self.PillowSide_dy-self.AngleBarTop_dy,Q('0cm')]

        rot = [Q('0.0deg'),Q('180.0deg'),Q('0.0deg')]

        AngleBarTop_R_rot = geom.structure.Rotation('AngleBarTop_R_rot',
                                                rot[0],rot[1],rot[2])

        AngleBarTop_R_pos = geom.structure.Position('AngleBarTop_R_pos',
                                                pos[0],pos[1],pos[2])

        AngleBarTop_R_pla = geom.structure.Placement('AngleBarTop_R_pla',
                                                volume=AngleBarTop_lv,
                                                pos=AngleBarTop_R_pos,
                                                rot=AngleBarTop_R_rot)

        main_lv.placements.append(AngleBarTop_R_pla.name)

        # Construct Angle Base Volume
        AngleBase_shape = geom.shapes.Box('AngleBase_shape',
                                        dx = self.AngleBarTop_dx,
                                        dy = self.Angle_dd,
                                        dz = self.Angle_Length)

        AngleBase_lv = geom.structure.Volume('volAngleBase',
                                        material=self.Pillow_Material,
                                        shape=AngleBase_shape)

        # Place Angle Base Volume inside Pillow volume
        for i in range(2):
            for j in range(self.N_Angle):
                pos = [(-1)**i*(self.AngleBarTop_gap+AngleBase_shape[1]),self.Pillow_dy-2*self.PillowSide_dy-2*self.AngleBarTop_dy-self.Angle_dd,-(self.N_Angle-1-2*j)*self.Angle_Length-(self.N_Angle-1-2*j)*self.Angle_gap]

                AngleBase_pos = geom.structure.Position('AngleBase_pos_'+str(i*self.N_Angle+j),
                                                        pos[0],pos[1],pos[2])

                AngleBase_pla = geom.structure.Placement('AngleBase_pla_'+str(i*self.N_Angle+j),
                                                        volume=AngleBase_lv,
                                                        pos=AngleBase_pos)

                main_lv.placements.append(AngleBase_pla.name)

        # Construct Angle Side Volume
        AngleSide_shape = geom.shapes.Box('AngleSide_shape',
                                        dx = self.Angle_dd,
                                        dy = self.AngleBarTop_dx-self.Angle_dd,
                                        dz = self.Angle_Length)

        AngleSide_lv = geom.structure.Volume('volAngleSide',
                                        material=self.Pillow_Material,
                                        shape=AngleSide_shape)

        # Place Angle Side Volume inside Pillow volume
        for i in range(2):
            for j in range(self.N_Angle):
                pos = [(-1)**i*(self.AngleBarTop_gap+2*self.AngleBarTop_dx-AngleSide_shape[1]),self.Pillow_dy-2*self.PillowSide_dy-2*self.AngleBarTop_dy-2*self.Angle_dd-AngleSide_shape[2],-(self.N_Angle-1-2*j)*self.Angle_Length-(self.N_Angle-1-2*j)*self.Angle_gap]

                AngleSide_pos = geom.structure.Position('AngleSide_pos_'+str(i*self.N_Angle+j),
                                                        pos[0],pos[1],pos[2])

                AngleSide_pla = geom.structure.Placement('AngleSide_pla_'+str(i*self.N_Angle+j),
                                                        volume=AngleSide_lv,
                                                        pos=AngleSide_pos)

                main_lv.placements.append(AngleSide_pla.name)

        # Construct Angle Bar Side Volume
        AngleBarSide_shape = geom.shapes.Box('AngleBarSide_shape',
                                        dx = self.AngleBarSide_dx,
                                        dy = self.AngleBarSide_dy,
                                        dz = self.AngleBarSide_dz)

        AngleBarSide_lv = geom.structure.Volume('volAngleBarSide',
                                        material=self.Pillow_Material,
                                        shape=AngleBarSide_shape)

        # Place Angle Bar Side Volume inside Pillow volume
        for i in range(2):
            pos = [(-1)**i*(self.AngleBarTop_gap+2*self.AngleBarTop_dx+3*self.AngleBarSide_dx),self.Pillow_dy-2*self.PillowSide_dy-2*self.AngleBarTop_dy-2*self.Angle_dd-2*AngleSide_shape[2]+self.AngleBarSide_dy,Q('0cm')]

            AngleBarSide_pos = geom.structure.Position('AngleBarSide_pos_'+str(i*self.N_Angle+j),
                                                    pos[0],pos[1],pos[2])

            AngleBarSide_pla = geom.structure.Placement('AngleBarSide_pla_'+str(i*self.N_Angle+j),
                                                    volume=AngleBarSide_lv,
                                                    pos=AngleBarSide_pos)

            main_lv.placements.append(AngleBarSide_pla.name)

        # Construct G10 Volume
        G10_shape = geom.shapes.Box('G10_shape',
                                        dx = self.AngleBarSide_dx,
                                        dy = self.AngleBarSide_dy,
                                        dz = self.G10_dz)

        G10_lv = geom.structure.Volume('volG10',
                                        material=self.G10_Material,
                                        shape=G10_shape)

        # Place G10 Volume inside Pillow volume
        for i in range(2):
            pos = [(-1)**i*(self.AngleBarTop_gap+2*self.AngleBarTop_dx+self.AngleBarSide_dx),self.Pillow_dy-2*self.PillowSide_dy-2*self.AngleBarTop_dy-2*self.Angle_dd-2*AngleSide_shape[2]+self.AngleBarSide_dy,Q('0cm')]

            G10_pos = geom.structure.Position('G10_pos_'+str(i*self.N_Angle+j),
                                                    pos[0],pos[1],pos[2])

            G10_pla = geom.structure.Placement('G10_pla_'+str(i*self.N_Angle+j),
                                                    volume=G10_lv,
                                                    pos=G10_pos)

            main_lv.placements.append(G10_pla.name)

