""" OpticalDet.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class OpticalDetBuilder(gegede.builder.Builder):
    """ Class to build OpticalDet geometry.

    """

    def configure(self,Gap_LightTile,Gap_LightTile_PixelPlane,N_TilesY,**kwargs):

        # Read dimensions form config file
        self.Gap_LightTile              = Gap_LightTile
        self.Gap_LightTile_PixelPlane   = Gap_LightTile_PixelPlane
        self.N_TilesY                   = int(N_TilesY)

        # Material definitons
        self.Material                   = 'LAr'

        # Subbuilders
        self.ArCLight_builder           = self.get_builder('ArCLight')
        self.TPCPlane_builder           = self.get_builder('TPCPlane')
        self.PixelPlane_builder         = self.TPCPlane_builder.get_builder('PixelPlane')

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.TPCPlane_builder.halfDimension['dx']
                                        +self.ArCLight_builder.halfDimension['dx']
                                        +self.Gap_LightTile_PixelPlane,

                                'dy':   self.TPCPlane_builder.halfDimension['dy'],
                                'dz':   self.ArCLight_builder.halfDimension['dz']}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('OpticalDetBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Build ArCLight Array
        for i in range(self.N_TilesY):
                pos = [self.TPCPlane_builder.halfDimension['dx']+self.Gap_LightTile_PixelPlane,(-self.N_TilesY+1+2*i)*(self.ArCLight_builder.halfDimension['dy']+self.Gap_LightTile),Q('0cm')]

                ArCLight_lv = self.ArCLight_builder.get_volume()

                ArCLight_pos = geom.structure.Position(self.ArCLight_builder.name+'_pos_'+str(i),
                                                    pos[0],pos[1],pos[2])

                ArCLight_pla = geom.structure.Placement(self.ArCLight_builder.name+'_pla_'+str(i),
                                                        volume=ArCLight_lv,
                                                        pos=ArCLight_pos)

                main_lv.placements.append(ArCLight_pla.name)

        # Construct PCB Bar
        PCBBar_shape = geom.shapes.Box('PCBBar_shape',
                                        dx = self.PixelPlane_builder.PCB_dx,
                                        dy = self.PixelPlane_builder.PCB_dy,
                                        dz = self.ArCLight_builder.halfDimension['dz'])

        PCBBar_lv = geom.structure.Volume('volPCBBar',
                                        material=self.PixelPlane_builder.PCB_Material,
                                        shape=PCBBar_shape)

        # Place PCB Bar
        for i in range(self.TPCPlane_builder.N_UnitsY):
            pos = [-self.ArCLight_builder.halfDimension['dx']-self.Gap_LightTile_PixelPlane-self.PixelPlane_builder.Pixel_dx+self.PixelPlane_builder.Asic_dx,(-self.N_TilesY+1+2*i)*(self.ArCLight_builder.halfDimension['dy']+self.Gap_LightTile),Q('0cm')]

            PCBBar_pos = geom.structure.Position('PCBBar_pos_'+str(i),
                                                    pos[0],pos[1],pos[2])

            PCBBar_pla = geom.structure.Placement('PCBBar_pla_'+str(i),
                                                    volume=PCBBar_lv,
                                                    pos=PCBBar_pos)

            main_lv.placements.append(PCBBar_pla.name)
