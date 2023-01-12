""" Feedthrough.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class FeedthroughBuilder(gegede.builder.Builder):
    """ Class to build Feedthrough geometry.

    """

    def configure(self,TubeCenter_dimension,TubeSide_dimension,TubeCenterFlange_dimension,TubeSideFlange_dimension,**kwargs):

        # Read dimensions form config file
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

        # Material definitons
        self.Flange_Material    = 'Steel'
        self.Vacuum_Material    = 'GAr' #'Vacuum' CHANGE!!!!!
        self.Tube_Material      = 'Steel'
        self.GAr_Material       = 'GAr'

        self.Material           = 'Air'

        # Subbuilders
        self.Flange_builder     = self.get_builder('Flange')
        self.Pillow_builder     = self.get_builder('Pillow')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.Feedthrough_dx     = self.Pillow_builder.PillowSide_dx-2*self.Pillow_builder.PillowSide_dd
        self.Feedthrough_dy     = self.TubeCenter_dz+self.TubeCenterFlange_dz
        self.Feedthrough_dz     = self.Pillow_builder.PillowSide_dz-2*self.Pillow_builder.PillowSide_dd

        self.halfDimension  = { 'dx':   self.Feedthrough_dx,
                                'dy':   self.Feedthrough_dy,
                                'dz':   self.Feedthrough_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('FeedthroughBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Construct FlangePart Volume
        FlangePart_shape = geom.shapes.Box('FlangePart_shape',
                                        dx = self.halfDimension['dx'],
                                        dy = self.Flange_builder.halfDimension['dy'],
                                        dz = self.halfDimension['dz'])

        FlangePart_lv = geom.structure.Volume('volFlangePart',
                                        material=self.Flange_Material,
                                        shape=FlangePart_shape)

        # Place FlangePart Volume inside Feedthrough volume
        pos = [Q('0cm'),-self.halfDimension['dy']+2*self.Pillow_builder.PillowSide_dy+self.Flange_builder.halfDimension['dy'],Q('0cm')]

        FlangePart_pos = geom.structure.Position('FlangePart_pos',
                                                pos[0],pos[1],pos[2])

        FlangePart_pla = geom.structure.Placement('FlangePart_pla',
                                                volume=FlangePart_lv,
                                                pos=FlangePart_pos)

        main_lv.placements.append(FlangePart_pla.name)

        # Construct VacuumPart Volume
        VacuumPart_shape = geom.shapes.Box('VacuumPart_shape',
                                        dx = self.halfDimension['dx'],
                                        dy = self.Pillow_builder.PillowSide_dy-self.Pillow_builder.PillowBottom_dy,
                                        dz = self.halfDimension['dz'])

        VacuumPart_lv = geom.structure.Volume('volVacuumPart',
                                        material=self.Vacuum_Material,
                                        shape=VacuumPart_shape)

        # Place VacuumPart Volume inside Feedthrough volume
        pos = [Q('0cm'),-self.halfDimension['dy']+self.Pillow_builder.PillowBottom_dy+self.Pillow_builder.PillowSide_dy,Q('0cm')]

        VacuumPart_pos = geom.structure.Position('VacuumPart_pos',
                                                pos[0],pos[1],pos[2])

        VacuumPart_pla = geom.structure.Placement('VacuumPart_pla',
                                                volume=VacuumPart_lv,
                                                pos=VacuumPart_pos)

        main_lv.placements.append(VacuumPart_pla.name)

        # Construct PillowPart Volume
        PillowPart_shape = geom.shapes.Box('PillowPart_shape',
                                        dx = self.halfDimension['dx'],
                                        dy = self.Pillow_builder.PillowBottom_dy,
                                        dz = self.halfDimension['dz'])

        PillowPart_lv = geom.structure.Volume('volPillowPart',
                                        material=self.Flange_Material,
                                        shape=PillowPart_shape)

        # Place PillowPart Volume inside Feedthrough volume
        pos = [Q('0cm'),-self.halfDimension['dy']+self.Pillow_builder.PillowBottom_dy,Q('0cm')]

        PillowPart_pos = geom.structure.Position('PillowPart_pos',
                                                pos[0],pos[1],pos[2])

        PillowPart_pla = geom.structure.Placement('PillowPart_pla',
                                                volume=PillowPart_lv,
                                                pos=PillowPart_pos)

        main_lv.placements.append(PillowPart_pla.name)

        # Construct TubeCenter Volume
        TubeCenter_shape = geom.shapes.Tubs('TubeCenter_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TubeCenter_rmax,
                                        dz = self.TubeCenter_dz+self.TubeCenterFlange_dz)

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

        # Place TubeCenterFlange Volume inside TubeCenter volume
        pos = [Q('0cm'),Q('0cm'),self.TubeCenter_dz-2*self.TubeCenterFlange_dz]

        TubeCenterFlange_pos = geom.structure.Position('TubeCenterFlange_pos_A',
                                                pos[0],pos[1],pos[2])

        TubeCenterFlange_pla = geom.structure.Placement('TubeCenterFlange_pla_A',
                                                volume=TubeCenterFlange_lv,
                                                pos=TubeCenterFlange_pos)

        TubeCenter_lv.placements.append(TubeCenterFlange_pla.name)

        pos = [Q('0cm'),Q('0cm'),self.TubeCenter_dz]

        TubeCenterFlange_pos = geom.structure.Position('TubeCenterFlange_pos_B',
                                                pos[0],pos[1],pos[2])

        TubeCenterFlange_pla = geom.structure.Placement('TubeCenterFlange_pla_B',
                                                volume=TubeCenterFlange_lv,
                                                pos=TubeCenterFlange_pos)

        TubeCenter_lv.placements.append(TubeCenterFlange_pla.name)

        # Place TubeCenterGAr Volume inside TubeCenter volume
        pos = [Q('0cm'),Q('0cm'),-self.TubeCenterFlange_dz]

        TubeCenterGAr_pos = geom.structure.Position('TubeCenterGAr_pos',
                                                pos[0],pos[1],pos[2])

        TubeCenterGAr_pla = geom.structure.Placement('TubeCenterGAr_pla',
                                                volume=TubeCenterGAr_lv,
                                                pos=TubeCenterGAr_pos)

        TubeCenter_lv.placements.append(TubeCenterGAr_pla.name)

        # Place TubeCenter Volume inside Feedthrough volume
        pos = [Q('0cm'),-self.halfDimension['dy']+self.TubeCenter_dz+self.TubeCenterFlange_dz,Q('0cm')]

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

        # Place TubeSideFlange Volume inside TubeSide volume
        pos = [Q('0cm'),Q('0cm'),self.TubeSide_dz-self.TubeSideFlange_dz]

        TubeSideFlange_pos = geom.structure.Position('TubeSideFlange_pos',
                                                pos[0],pos[1],pos[2])

        TubeSideFlange_pla = geom.structure.Placement('TubeSideFlange_pla',
                                                volume=TubeSideFlange_lv,
                                                pos=TubeSideFlange_pos)

        TubeSide_lv.placements.append(TubeSideFlange_pla.name)

        # Place TubeSideGAr Volume inside TubeSide volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        TubeSideGAr_pos = geom.structure.Position('TubeSideGAr_pos',
                                                pos[0],pos[1],pos[2])

        TubeSideGAr_pla = geom.structure.Placement('TubeSideGAr_pla',
                                                volume=TubeSideGAr_lv,
                                                pos=TubeSideGAr_pos)

        TubeSide_lv.placements.append(TubeSideGAr_pla.name)

        # Place TubeSide Volume inside Feedthrough volume
        for i in range(2):
            pos = [(-1)**i*2*self.TubeSide_Offset,-self.halfDimension['dy']+self.TubeSide_dz,Q('0cm')]

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

            pos = [Q('0cm'),-self.halfDimension['dy']+self.TubeSide_dz,(-1)**i*2*self.TubeSide_Offset]

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

