""" TPCPlane.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class TPCPlaneBuilder(gegede.builder.Builder):
    """ Class to build TPCPlane geometry.

    """

    def configure(self,Gap_PixelTile,N_UnitsY,**kwargs):

        # Read dimensions form config file
        self.Gap_PixelTile  = Gap_PixelTile
        self.N_UnitsY       = int(N_UnitsY)

        # Material definitons
        self.Material       = 'LAr'

        # Subbuilders
        self.PixelPlane_builder  = self.get_builder('PixelPlane')


    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.PixelPlane_builder.halfDimension['dx'],
                                'dy':   self.N_UnitsY*self.PixelPlane_builder.halfDimension['dy']+(self.N_UnitsY-1)*self.Gap_PixelTile,
                                'dz':   2*self.PixelPlane_builder.halfDimension['dz']+self.Gap_PixelTile}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('TPCPlaneBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Build TPC Array
        for i in range(self.N_UnitsY):
            pos = [Q('0cm'),(-self.N_UnitsY+1+2*i)*(self.PixelPlane_builder.halfDimension['dy']+self.Gap_PixelTile),-self.PixelPlane_builder.halfDimension['dz']-self.Gap_PixelTile]

            PixelPlane_lv = self.PixelPlane_builder.get_volume()

            PixelPlane_pos = geom.structure.Position(self.PixelPlane_builder.name+'_pos_'+str(i)+'_R',
                                                pos[0],pos[1],pos[2])

            PixelPlane_pla = geom.structure.Placement(self.PixelPlane_builder.name+'_pla_'+str(i)+'_R',
                                                    volume=PixelPlane_lv,
                                                    pos=PixelPlane_pos,
                                                    copynumber=2*i)

            main_lv.placements.append(PixelPlane_pla.name)

        for i in range(self.N_UnitsY):
            pos = [Q('0cm'),(-self.N_UnitsY+1+2*i)*(self.PixelPlane_builder.halfDimension['dy']+self.Gap_PixelTile),+self.PixelPlane_builder.halfDimension['dz']+self.Gap_PixelTile]

            PixelPlane_lv = self.PixelPlane_builder.get_volume()

            PixelPlane_pos = geom.structure.Position(self.PixelPlane_builder.name+'_pos_'+str(i)+'_L',
                                                pos[0],pos[1],pos[2])

            rot =[Q('180.0deg'),Q('0.0deg'),Q('0.0deg')]

            PixelPlane_rot = geom.structure.Rotation(self.PixelPlane_builder.name+'_rot_'+str(i)+'_L',
                                                rot[0],rot[1],rot[2])

            PixelPlane_pla = geom.structure.Placement(self.PixelPlane_builder.name+'_pla_'+str(i)+'_L',
                                                    volume=PixelPlane_lv,
                                                    pos=PixelPlane_pos,
                                                    rot=PixelPlane_rot,
                                                    copynumber=(2*i)+1)

            main_lv.placements.append(PixelPlane_pla.name)

