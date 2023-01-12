""" PixelPlane.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class PixelPlaneBuilder(gegede.builder.Builder):
    """ Class to build PixelPlane geometry.

    """

    def configure(self,PCB_dimension,Pixel_dimension,Asic_dimension,N_Pixel,N_Asic,**kwargs):

        # Read dimensions form config file
        self.PCB_dx             = PCB_dimension['dx']
        self.PCB_dy             = PCB_dimension['dy']
        self.PCB_dz             = PCB_dimension['dz']

        self.Pixel_dx           = Pixel_dimension['dx']
        self.Pixel_dy           = Pixel_dimension['dy']
        self.Pixel_dz           = Pixel_dimension['dz']

        self.Asic_dx            = Asic_dimension['dx']
        self.Asic_dy            = Asic_dimension['dy']
        self.Asic_dz            = Asic_dimension['dz']

        self.N_Pixel            = int(N_Pixel)
        self.N_Asic             = int(N_Asic)

        # Material definitons
        self.PCB_Material       = 'FR4'
        self.Pixel_Material     = 'Gold'
        self.Asic_Material      = 'Silicon'

        self.Material           = 'LAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension  = { 'dx':   self.PCB_dx
                                        +self.Pixel_dx
                                        +self.Asic_dx,

                                'dy':   self.PCB_dy,

                                'dz':   self.PCB_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('PixelPlaneBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Construct PCB panel
        PCB_shape = geom.shapes.Box('PCB_shape',
                                       dx = self.PCB_dx,
                                       dy = self.PCB_dy,
                                       dz = self.PCB_dz)

        PCB_lv = geom.structure.Volume('volTPCPCB',
                                            material=self.PCB_Material,
                                            shape=PCB_shape)

        # Place PCB panel into main LV
        pos = [-self.Pixel_dx+self.Asic_dx,Q('0m'),Q('0m')]

        PCB_pos = geom.structure.Position('PCB_pos',
                                                pos[0],pos[1],pos[2])

        PCB_pla = geom.structure.Placement('PCB_pla',
                                                volume=PCB_lv,
                                                pos=PCB_pos)

        main_lv.placements.append(PCB_pla.name)

        # Construct Pixel
        Pixel_shape = geom.shapes.Box('Pixel_shape',
                                       dx = self.Pixel_dx,
                                       dy = self.Pixel_dy,
                                       dz = self.Pixel_dz)

        Pixel_lv = geom.structure.Volume('volTPCPixel',
                                            material=self.Pixel_Material,
                                            shape=Pixel_shape)

        for n in range(self.N_Pixel):
            for m in range(self.N_Pixel):
                # Place Pixel into PCB board
                pos = [self.PCB_dx+self.Asic_dx,-self.PCB_dy+self.Pixel_dy+(self.PCB_dy-self.Pixel_dy)/(self.N_Pixel-1)*(2*n),-self.PCB_dz+self.Pixel_dz+(self.PCB_dz-self.Pixel_dz)/(self.N_Pixel-1)*(2*m)]

                Pixel_pos = geom.structure.Position('Pixel_pos_'+str(n)+'.'+str(m),
                                                        pos[0],pos[1],pos[2])

                Pixel_pla = geom.structure.Placement('Pixel_pla_'+str(n)+'.'+str(m),
                                                        volume=Pixel_lv,
                                                        pos=Pixel_pos,
                                                        copynumber=(n*self.N_Pixel)+m)

                main_lv.placements.append(Pixel_pla.name)

        # Construct ASIC
        Asic_shape = geom.shapes.Box('Asic_shape',
                                       dx = self.Asic_dx,
                                       dy = self.Asic_dy,
                                       dz = self.Asic_dz)

        Asic_lv = geom.structure.Volume('volTPCAsic',
                                            material=self.Asic_Material,
                                            shape=Asic_shape)

        for n in range(self.N_Asic):
            for m in range(self.N_Asic):
                # Place ASICs into PCB board
                pos = [-self.PCB_dx-self.Pixel_dx,-self.PCB_dy+self.PCB_dy/self.N_Asic*(1+2*n),-self.PCB_dz+self.PCB_dz/self.N_Asic*(1+2*m)]

                Asic_pos = geom.structure.Position('Asic_pos_'+str(n)+'.'+str(m),
                                                        pos[0],pos[1],pos[2])

                Asic_pla = geom.structure.Placement('Asic_pla_'+str(n)+'.'+str(m),
                                                        volume=Asic_lv,
                                                        pos=Asic_pos)

                main_lv.placements.append(Asic_pla.name)

