""" TPiece.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class TPieceBuilder(gegede.builder.Builder):
    """ Class to build TPiece geometry.

    """

    def configure(self,TPiece_dimension,TPieceFlange_dimension,TPiece_dz_v,TPiece_dz_h,**kwargs):

        # Read dimensions form config file
        self.TPiece_rmin        = TPiece_dimension['rmin']
        self.TPiece_rmax        = TPiece_dimension['rmax']
        self.TPiece_dz          = TPiece_dimension['dz']

        self.TPieceFlange_rmin  = TPieceFlange_dimension['rmin']
        self.TPieceFlange_rmax  = TPieceFlange_dimension['rmax']
        self.TPieceFlange_dz    = TPieceFlange_dimension['dz']

        self.TPiece_dz_v        = TPiece_dz_v
        self.TPiece_dz_h        = TPiece_dz_h

        # Material definitons
        self.TPiece_Material    = 'Steel'
        self.GAr_Material       = 'GAr'

        self.Material           = 'Air'

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.TPiece_dx  = self.TPieceFlange_rmax
        self.TPiece_dy  = self.TPiece_dz_v+2*self.TPieceFlange_dz
        self.TPiece_dz  = self.TPiece_dz_h+self.TPieceFlange_dz+self.TPieceFlange_rmax/2+self.TPiece_rmax/2

        self.halfDimension  = { 'dx':   self.TPiece_dx,
                                'dy':   self.TPiece_dy,
                                'dz':   self.TPiece_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('TPieceBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Construct TubeV Volume
        TubeV_shape = geom.shapes.Tubs('TubeV_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TPiece_rmax,
                                        dz = self.TPiece_dz_v)

        TubeV_lv = geom.structure.Volume('volTubeV',
                                        material=self.TPiece_Material,
                                        shape=TubeV_shape)

        # Construct TubeVFlange Volume
        TubeVFlange_shape = geom.shapes.Tubs('TubeVFlange_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TPieceFlange_rmax,
                                        dz = self.TPieceFlange_dz)

        TubeVFlange_lv = geom.structure.Volume('volTubeVFlange',
                                        material=self.TPiece_Material,
                                        shape=TubeVFlange_shape)

        # Construct TubeVGAr Volume
        TubeVGAr_shape = geom.shapes.Tubs('TubeVGAr_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TPiece_rmin,
                                        dz = self.TPiece_dz_v)

        TubeVGAr_lv = geom.structure.Volume('volTubeVGAr',
                                        material=self.GAr_Material,
                                        shape=TubeVGAr_shape)

        # Construct TubeH Volume
        TubeH_shape = geom.shapes.Tubs('TubeH_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TPiece_rmax,
                                        dz = self.TPiece_dz_h)

        TubeH_lv = geom.structure.Volume('volTubeH',
                                        material=self.TPiece_Material,
                                        shape=TubeH_shape)

        # Construct TubeHFlange Volume
        TubeHFlange_shape = geom.shapes.Tubs('TubeHFlange_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TPieceFlange_rmax,
                                        dz = self.TPieceFlange_dz)

        TubeHFlange_lv = geom.structure.Volume('volTubeHFlange',
                                        material=self.TPiece_Material,
                                        shape=TubeHFlange_shape)

        # Construct TubeHGAr Volume
        TubeHGAr_shape = geom.shapes.Tubs('TubeHGAr_shape',
                                        rmin = Q('0cm'),
                                        rmax = self.TPiece_rmin,
                                        dz = self.TPiece_dz_h)

        TubeHGAr_lv = geom.structure.Volume('volTubeHGAr',
                                        material=self.GAr_Material,
                                        shape=TubeHGAr_shape)

        # Place TubeV Volume inside TPiece volume
        pos = [Q('0cm'),Q('0cm'),-self.halfDimension['dz']+self.TPieceFlange_rmax]

        rot = [Q('90.0deg'),Q('0.0deg'),Q('0.0deg')]

        TubeV_pos = geom.structure.Position('TubeV_pos',
                                                pos[0],pos[1],pos[2])

        TubeV_rot = geom.structure.Rotation('TubeV_rot',
                                                rot[0],rot[1],rot[2])

        TubeV_pla = geom.structure.Placement('TubeV_pla',
                                                volume=TubeV_lv,
                                                pos=TubeV_pos,
                                                rot=TubeV_rot)

        main_lv.placements.append(TubeV_pla.name)

        # Place TubeVFlange Volume inside TubeV volume
        for i in range(2):
            pos = [Q('0cm'),(-1)**i*(self.halfDimension['dy']-self.TPieceFlange_dz),-self.halfDimension['dz']+self.TPieceFlange_rmax]

            rot = [Q('90.0deg'),Q('0.0deg'),Q('0.0deg')]

            TubeVFlange_pos = geom.structure.Position('TubeVFlange_pos_'+str(i),
                                                    pos[0],pos[1],pos[2])

            TubeVFlange_rot = geom.structure.Rotation('TubeVFlange_rot_'+str(i),
                                                    rot[0],rot[1],rot[2])

            TubeVFlange_pla = geom.structure.Placement('TubeVFlange_pla_'+str(i),
                                                    volume=TubeVFlange_lv,
                                                    pos=TubeVFlange_pos,
                                                    rot=TubeVFlange_rot)

            main_lv.placements.append(TubeVFlange_pla.name)

        # Place TubeH Volume inside TPiece volume
        pos = [Q('0cm'),Q('0cm'),self.halfDimension['dz']-self.TPiece_dz_h-2*self.TPieceFlange_dz]

        TubeH_pos = geom.structure.Position('TubeH_pos',
                                                pos[0],pos[1],pos[2])

        TubeH_pla = geom.structure.Placement('TubeH_pla',
                                                volume=TubeH_lv,
                                                pos=TubeH_pos)

        main_lv.placements.append(TubeH_pla.name)

        # Place TubeHFlange Volume inside TubeH volume
        pos = [Q('0cm'),Q('0cm'),self.halfDimension['dz']-self.TPieceFlange_dz]

        rot = [Q('0.0deg'),Q('0.0deg'),Q('0.0deg')]

        TubeHFlange_pos = geom.structure.Position('TubeHFlange_pos',
                                                pos[0],pos[1],pos[2])

        TubeHFlange_rot = geom.structure.Rotation('TubeHFlange_rot',
                                                rot[0],rot[1],rot[2])

        TubeHFlange_pla = geom.structure.Placement('TubeHFlange_pla',
                                                volume=TubeHFlange_lv,
                                                pos=TubeHFlange_pos,
                                                rot=TubeHFlange_rot)

        main_lv.placements.append(TubeHFlange_pla.name)

        # Place TubeVGAr Volume inside TubeV volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        TubeVGAr_pos = geom.structure.Position('TubeVGAr_pos',
                                                pos[0],pos[1],pos[2])

        TubeVGAr_pla = geom.structure.Placement('TubeVGAr_pla',
                                                volume=TubeVGAr_lv,
                                                pos=TubeVGAr_pos)

        TubeV_lv.placements.append(TubeVGAr_pla.name)

        # Place TubeHGAr Volume inside TubeH volume
        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        TubeHGAr_pos = geom.structure.Position('TubeHGAr_pos',
                                                pos[0],pos[1],pos[2])

        TubeHGAr_pla = geom.structure.Placement('TubeHGAr_pla',
                                                volume=TubeHGAr_lv,
                                                pos=TubeHGAr_pos)

        TubeH_lv.placements.append(TubeHGAr_pla.name)

