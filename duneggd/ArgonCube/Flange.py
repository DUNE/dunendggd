""" Flange.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class FlangeBuilder(gegede.builder.Builder):
    """ Class to build Flange geometry.

    """

    def configure(self,FlangeTop_dimension,FlangeBtm_dimension,TubeCenter_dimension,TubeSide_dimension,TubeCenterFlange_dimension,TubeSideFlange_dimension,**kwargs):

        # Read dimensions form config file
        self.FlangeTop_dx           = FlangeTop_dimension['dx']
        self.FlangeTop_dy           = FlangeTop_dimension['dy']
        self.FlangeTop_dz           = FlangeTop_dimension['dz']

        self.FlangeBtm_dx           = FlangeBtm_dimension['dx']
        self.FlangeBtm_dy           = FlangeBtm_dimension['dy']
        self.FlangeBtm_dz           = FlangeBtm_dimension['dz']

        self.TubeCenter_rmin        = TubeCenter_dimension['rmin']
        self.TubeCenter_rmax        = TubeCenter_dimension['rmax']
        self.TubeCenter_dz          = TubeCenter_dimension['dz']

        self.TubeCenterFlange_rmin  = TubeCenterFlange_dimension['rmin']
        self.TubeCenterFlange_rmax  = TubeCenterFlange_dimension['rmax']
        self.TubeCenterFlange_dz    = TubeCenterFlange_dimension['dz']

        self.TubeSide_rmin          = TubeSide_dimension['rmin']
        self.TubeSide_rmax          = TubeSide_dimension['rmax']
        self.TubeSide_dz            = TubeSide_dimension['dz']
        self.TubeSide_Offset        = TubeSide_dimension['offset']

        self.TubeSideFlange_rmin    = TubeSideFlange_dimension['rmin']
        self.TubeSideFlange_rmax    = TubeSideFlange_dimension['rmax']
        self.TubeSideFlange_dz      = TubeSideFlange_dimension['dz']

        self.Flange_dx              = self.FlangeTop_dx
        self.Flange_dy              = self.FlangeTop_dy+self.FlangeBtm_dy+self.TubeSide_dz+self.TubeSideFlange_dz
        self.Flange_dz              = self.FlangeTop_dz

        # Material definitons
        self.Flange_Material        = 'Steel'
        self.Tube_Material          = 'Steel'
        self.GAr_Material           = 'GAr'

        self.Material               = 'Air'

        # Subbuilders
        self.TPiece_builder         = self.get_builder('TPiece')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.Flange_dx,
                                'dy':   self.Flange_dy+self.TPiece_builder.halfDimension['dy'],
                                'dz':   self.Flange_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('FlangeBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Construct FlangeTop Volume
        FlangeTop_shape = geom.shapes.Box('FlangeTop_shape',
                                        dx = self.FlangeTop_dx,
                                        dy = self.FlangeTop_dy,
                                        dz = self.FlangeTop_dz)

        FlangeTop_lv = geom.structure.Volume('volFlangeTop',
                                        material=self.Flange_Material,
                                        shape=FlangeTop_shape)

        # Place FlangeTop Volume inside Flange volume
        pos = [Q('0cm'),-self.halfDimension['dy']+2*self.FlangeBtm_dy+self.FlangeTop_dy,Q('0cm')]

        FlangeTop_pos = geom.structure.Position('FlangeTop_pos',
                                                pos[0],pos[1],pos[2])

        FlangeTop_pla = geom.structure.Placement('FlangeTop_pla',
                                                volume=FlangeTop_lv,
                                                pos=FlangeTop_pos)

        main_lv.placements.append(FlangeTop_pla.name)

        # Construct FlangeBtm Volume
        FlangeBtm_shape = geom.shapes.Box('FlangeBtm_shape',
                                        dx = self.FlangeBtm_dx,
                                        dy = self.FlangeBtm_dy,
                                        dz = self.FlangeBtm_dz)

        FlangeBtm_lv = geom.structure.Volume('volFlangeBtm',
                                        material=self.Flange_Material,
                                        shape=FlangeBtm_shape)

        # Place FlangeBtm Volume inside Flange volume
        pos = [Q('0cm'),-self.halfDimension['dy']+self.FlangeBtm_dy,Q('0cm')]

        FlangeBtm_pos = geom.structure.Position('FlangeBtm_pos',
                                                pos[0],pos[1],pos[2])

        FlangeBtm_pla = geom.structure.Placement('FlangeBtm_pla',
                                                volume=FlangeBtm_lv,
                                                pos=FlangeBtm_pos)

        main_lv.placements.append(FlangeBtm_pla.name)

        # Construct TubeCenter Volume
        TubeCenter_shape = geom.shapes.Tubs('TubeCenter_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TubeCenter_rmax,
                                        dz = self.TubeCenter_dz)

        TubeCenter_lv = geom.structure.Volume('volTubeCenter',
                                        material=self.Tube_Material,
                                        shape=TubeCenter_shape)

        # Construct TubeCenterFlange Volume
        TubeCenterFlange_shape = geom.shapes.Tubs('TubeCenterFlange_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TubeCenterFlange_rmax,
                                        dz = self.TubeCenterFlange_dz)

        TubeCenterFlange_lv = geom.structure.Volume('volTubeCenterFlange',
                                        material=self.Tube_Material,
                                        shape=TubeCenterFlange_shape)

        # Construct TubeCenterGAr Volume
        TubeCenterGAr_shape = geom.shapes.Tubs('TubeCenterGAr_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TubeCenter_rmin,
                                        dz = self.TubeCenter_dz)

        TubeCenterGAr_lv = geom.structure.Volume('volTubeCenterGAr',
                                        material=self.GAr_Material,
                                        shape=TubeCenterGAr_shape)

        # Place TubeCenterGAr Volume inside TubeCenter volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        TubeCenterGAr_pos = geom.structure.Position('TubeCenterGAr_pos',
                                                pos[0],pos[1],pos[2])

        TubeCenterGAr_pla = geom.structure.Placement('TubeCenterGAr_pla',
                                                volume=TubeCenterGAr_lv,
                                                pos=TubeCenterGAr_pos)

        TubeCenter_lv.placements.append(TubeCenterGAr_pla.name)

        # Place TubeCenter anf Flange Volumes inside Flange volume
        pos = [Q('0cm'),-self.halfDimension['dy']+2*self.FlangeBtm_dy+2*self.FlangeTop_dy+self.TubeCenter_dz,Q('0cm')]

        rot = [Q('90.0deg'),Q('0.0deg'),Q('0.0deg')]

        TubeCenter_pos = geom.structure.Position('TubeCenter_pos',
                                                pos[0],pos[1],pos[2])

        TubeCenter_rot = geom.structure.Rotation('TubeCenter_rot',
                                                rot[0],rot[1],rot[2])

        TubeCenter_pla = geom.structure.Placement('TubeCenter_pla',
                                                volume=TubeCenter_lv,
                                                pos=TubeCenter_pos,
                                                rot=TubeCenter_rot)

        main_lv.placements.append(TubeCenter_pla.name)

        pos = [pos[0],pos[1]+self.TubeCenter_dz+self.TubeCenterFlange_dz,pos[2]]

        TubeCenterFlange_pos = geom.structure.Position('TubeCenterFlange_pos_A',
                                                pos[0],pos[1],pos[2])

        TubeCenterFlange_pla = geom.structure.Placement('TubeCenterFlange_pla_A',
                                                volume=TubeCenterFlange_lv,
                                                pos=TubeCenterFlange_pos,
                                                rot=TubeCenter_rot)

        main_lv.placements.append(TubeCenterFlange_pla.name)

        pos = [pos[0],pos[1]+2*self.TubeCenterFlange_dz,pos[2]]

        TubeCenterFlange_pos = geom.structure.Position('TubeCenterFlange_pos_B',
                                                pos[0],pos[1],pos[2])

        TubeCenterFlange_pla = geom.structure.Placement('TubeCenterFlange_pla_B',
                                                volume=TubeCenterFlange_lv,
                                                pos=TubeCenterFlange_pos,
                                                rot=TubeCenter_rot)

        main_lv.placements.append(TubeCenterFlange_pla.name)

        # Construct TubeSide Volume
        TubeSide_shape = geom.shapes.Tubs('TubeSide_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TubeSide_rmax,
                                        dz = self.TubeSide_dz)

        TubeSide_lv = geom.structure.Volume('volTubeSide',
                                        material=self.Tube_Material,
                                        shape=TubeSide_shape)

        # Construct TubeSideFlange Volume
        TubeSideFlange_shape = geom.shapes.Tubs('TubeSideFlange_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TubeSideFlange_rmax,
                                        dz = self.TubeSideFlange_dz)

        TubeSideFlange_lv = geom.structure.Volume('volTubeSideFlange',
                                        material=self.Tube_Material,
                                        shape=TubeSideFlange_shape)

        # Construct TubeSideGAr Volume
        TubeSideGAr_shape = geom.shapes.Tubs('TubeSideGAr_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TubeSide_rmin,
                                        dz = self.TubeSide_dz)

        TubeSideGAr_lv = geom.structure.Volume('volTubeSideGAr',
                                        material=self.GAr_Material,
                                        shape=TubeSideGAr_shape)

        # Place TubeSideGAr Volume inside TubeSide volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        TubeSideGAr_pos = geom.structure.Position('TubeSideGAr_pos',
                                                pos[0],pos[1],pos[2])

        TubeSideGAr_pla = geom.structure.Placement('TubeSideGAr_pla',
                                                volume=TubeSideGAr_lv,
                                                pos=TubeSideGAr_pos)

        TubeSide_lv.placements.append(TubeSideGAr_pla.name)

        # Place TubeSide and Flange Volumes inside Flange volume
        for i in range(2):
            pos = [(-1)**i*2*self.TubeSide_Offset,-self.halfDimension['dy']+2*self.FlangeBtm_dy+2*self.FlangeTop_dy+self.TubeSide_dz,Q('0cm')]

            rot = [Q('90.0deg'),Q('0.0deg'),Q('0.0deg')]

            TubeSide_pos = geom.structure.Position('TubeSide_pos_'+str(2*i),
                                                    pos[0],pos[1],pos[2])

            TubeSide_rot = geom.structure.Rotation('TubeSide_rot_'+str(2*i),
                                                    rot[0],rot[1],rot[2])

            TubeSide_pla = geom.structure.Placement('TubeSide_pla_'+str(2*i),
                                                    volume=TubeSide_lv,
                                                    pos=TubeSide_pos,
                                                    rot=TubeSide_rot)

            main_lv.placements.append(TubeSide_pla.name)

            pos = [pos[0],pos[1]+self.TubeSide_dz+self.TubeSideFlange_dz,pos[2]]

            TubeSideFlange_pos = geom.structure.Position('TubeSideFlange_pos_'+str(2*i),
                                                    pos[0],pos[1],pos[2])

            TubeSideFlange_pla = geom.structure.Placement('TubeSideFlange_pla_'+str(2*i),
                                                    volume=TubeSideFlange_lv,
                                                    pos=TubeSideFlange_pos,
                                                    rot=TubeSide_rot)

            main_lv.placements.append(TubeSideFlange_pla.name)

            pos = [Q('0cm'),-self.halfDimension['dy']+2*self.FlangeBtm_dy+2*self.FlangeTop_dy+self.TubeSide_dz,(-1)**i*2*self.TubeSide_Offset]

            rot = [Q('90.0deg'),Q('0.0deg'),Q('0.0deg')]

            TubeSide_pos = geom.structure.Position('TubeSide_pos_'+str(2*i+1),
                                                    pos[0],pos[1],pos[2])

            TubeSide_rot = geom.structure.Rotation('TubeSide_rot_'+str(2*i+1),
                                                    rot[0],rot[1],rot[2])

            TubeSide_pla = geom.structure.Placement('TubeSide_pla_'+str(2*i+1),
                                                    volume=TubeSide_lv,
                                                    pos=TubeSide_pos,
                                                    rot=TubeSide_rot)

            main_lv.placements.append(TubeSide_pla.name)

            pos = [pos[0],pos[1]+self.TubeSide_dz+self.TubeSideFlange_dz,pos[2]]

            TubeSideFlange_pos = geom.structure.Position('TubeSideFlange_pos_'+str(2*i+1),
                                                    pos[0],pos[1],pos[2])

            TubeSideFlange_pla = geom.structure.Placement('TubeSideFlange_pla_'+str(2*i+1),
                                                    volume=TubeSideFlange_lv,
                                                    pos=TubeSideFlange_pos,
                                                    rot=TubeSide_rot)

            main_lv.placements.append(TubeSideFlange_pla.name)

        # Build TPieces
        pos = [2*self.TubeSide_Offset,-self.halfDimension['dy']+2*self.FlangeBtm_dy+2*self.FlangeTop_dy+2*self.TubeSide_dz+2*self.TubeSideFlange_dz+self.TPiece_builder.halfDimension['dy'],self.TPiece_builder.halfDimension['dz']-self.TPiece_builder.TPieceFlange_rmax]

        TPiece_lv = self.TPiece_builder.get_volume()

        TPiece_pos = geom.structure.Position(self.TPiece_builder.name+'_pos_A',
                                                pos[0],pos[1],pos[2])

        TPiece_pla = geom.structure.Placement(self.TPiece_builder.name+'_pla_A',
                                                volume=TPiece_lv,
                                                pos=TPiece_pos)

        main_lv.placements.append(TPiece_pla.name)

        pos = [-2*self.TubeSide_Offset,-self.halfDimension['dy']+2*self.FlangeBtm_dy+2*self.FlangeTop_dy+2*self.TubeSide_dz+2*self.TubeSideFlange_dz+self.TPiece_builder.halfDimension['dy'],-self.TPiece_builder.halfDimension['dz']+self.TPiece_builder.TPieceFlange_rmax]

        rot = [Q('180.0deg'),Q('0.0deg'),Q('0.0deg')]

        TPiece_lv = self.TPiece_builder.get_volume()

        TPiece_pos = geom.structure.Position(self.TPiece_builder.name+'_pos_B',
                                                pos[0],pos[1],pos[2])

        TPiece_rot = geom.structure.Rotation(self.TPiece_builder.name+'_rot_B',
                                                rot[0],rot[1],rot[2])

        TPiece_pla = geom.structure.Placement(self.TPiece_builder.name+'_pla_B',
                                                volume=TPiece_lv,
                                                pos=TPiece_pos,
                                                rot=TPiece_rot)

        main_lv.placements.append(TPiece_pla.name)

