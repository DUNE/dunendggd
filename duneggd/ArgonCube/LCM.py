""" LCM.py

Original Author: P. Koller, University of Bern

"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q


class LCMBuilder(gegede.builder.Builder):
    """ Class to build LCM geometry.

    """

    def configure(self,Fiber_dimension,SiPM_LCM_dimension,SiPM_LCM_Mask,SiPM_LCM_PCB,N_Fiber_LCM,N_SiPM_LCM,**kwargs):

        # Read dimensions form config file
        self.Fiber_rmin             = Fiber_dimension['rmin']
        self.Fiber_rmax             = Fiber_dimension['rmax']
        self.Fiber_dz               = Fiber_dimension['dz']
        self.Fiber_pitch            = Fiber_dimension['pitch']
        self.Fiber_dd               = Fiber_dimension['dd']
        self.Fiber_offset           = Fiber_dimension['offset']

        self.Core_rmax              = Fiber_dimension['core_rmax']
        self.TPB_dr                 = Fiber_dimension['tpb_dr']

        self.SiPM_LCM_dx            = SiPM_LCM_dimension['dx']
        self.SiPM_LCM_dy            = SiPM_LCM_dimension['dy']
        self.SiPM_LCM_dz            = SiPM_LCM_dimension['dz']
        self.SiPM_LCM_pitch         = SiPM_LCM_dimension['pitch']

        self.SiPM_LCM_Mask_dx       = SiPM_LCM_Mask['dx']
        self.SiPM_LCM_Mask_dy       = SiPM_LCM_Mask['dy']
        self.SiPM_LCM_Mask_dz       = SiPM_LCM_Mask['dz']
        self.SiPM_LCM_Mask_pitch    = SiPM_LCM_Mask['pitch']

        self.SiPM_LCM_PCB_dx        = SiPM_LCM_PCB['dx']
        self.SiPM_LCM_PCB_dy        = SiPM_LCM_PCB['dy']
        self.SiPM_LCM_PCB_dz        = SiPM_LCM_PCB['dz']

        self.N_Fiber_LCM            = int(N_Fiber_LCM)
        self.N_SiPM_LCM             = int(N_SiPM_LCM)

        # Material definitons
        self.TPB_Material           = 'TPB'
        self.Fiber_Material         = 'Y11'
        self.Fiber_Core_Material    = 'Y11C'
        self.SiPM_LCM_Material      = 'Silicon'
        self.SiPM_LCM_Mask_Material = 'PVT'
        self.SiPM_LCM_PCB_Material  = 'FR4'

        self.Material               = 'LAr'

    def construct(self,geom):
        """ Construct the geometry.

        """

        self.halfDimension      = { 'dx':   self.Fiber_dz
                                            +self.SiPM_LCM_Mask_dx
                                            +self.SiPM_LCM_PCB_dx,

                                    'dy':   self.SiPM_LCM_PCB_dy,

                                    'dz':   self.SiPM_LCM_PCB_dz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('LCMBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Construct Fiber TPB layer
        TPB_Fiber_shape = geom.shapes.Tubs('TPB_Fiber_shape',
                                       rmin = self.Fiber_rmin,
                                       rmax = self.Fiber_rmax+self.TPB_dr,
                                       dz = self.Fiber_dz-self.Fiber_offset)

        TPB_Fiber_lv = geom.structure.Volume('volTPB_Fiber',
                                            material=self.TPB_Material,
                                            shape=TPB_Fiber_shape)

        # Construct Fiber
        Fiber_shape = geom.shapes.Tubs('Fiber_shape',
                                       rmin = self.Fiber_rmin,
                                       rmax = self.Fiber_rmax,
                                       dz = self.Fiber_dz-self.Fiber_offset)

        Fiber_lv = geom.structure.Volume('volFiber',
                                            material=self.Fiber_Material,
                                            shape=Fiber_shape)

        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        Fiber_pos = geom.structure.Position('Fiber_pos',
                                                pos[0],pos[1],pos[2])

        Fiber_pla = geom.structure.Placement('Fiber_pla',
                                                volume=Fiber_lv,
                                                pos=Fiber_pos)

        TPB_Fiber_lv.placements.append(Fiber_pla.name)

        # Construct Fiber Core
        Fiber_Core_shape = geom.shapes.Tubs('Fiber_Core_shape',
                                       rmin = self.Fiber_rmin,
                                       rmax = self.Core_rmax,
                                       dz = self.Fiber_dz-self.Fiber_offset)

        Fiber_Core_lv = geom.structure.Volume('volFiber_Core',
                                            material=self.Fiber_Core_Material,
                                            shape=Fiber_Core_shape)

        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        Fiber_Core_pos = geom.structure.Position('Fiber_Core_pos',
                                                pos[0],pos[1],pos[2])

        Fiber_Core_pla = geom.structure.Placement('Fiber_Core_pla',
                                                volume=Fiber_Core_lv,
                                                pos=Fiber_Core_pos)

        Fiber_lv.placements.append(Fiber_Core_pla.name)

        # Place LCM Fibers
        pos = [self.SiPM_LCM_Mask_dx+self.SiPM_LCM_PCB_dx-self.Fiber_offset,-self.Fiber_dd-2*self.N_Fiber_LCM*self.Fiber_pitch,Q('0cm')]
        for i in range(self.N_Fiber_LCM):
            pos[1] = pos[1] + 2*self.Fiber_pitch

            rot = [Q('0.0deg'),Q('90.0deg'),Q('0.0deg')]

            TPB_Fiber_pos = geom.structure.Position('TPB_Fiber_pos_center_'+str(i),
                                                    pos[0],pos[1],pos[2])

            TPB_Fiber_rot = geom.structure.Rotation('TPB_Fiber_rot_center_'+str(i),
                                                    rot[0],rot[1],rot[2])

            TPB_Fiber_pla = geom.structure.Placement('TPB_Fiber_pla_center_'+str(i),
                                                    volume=TPB_Fiber_lv,
                                                    pos=TPB_Fiber_pos,
                                                    rot=TPB_Fiber_rot,
                                                    copynumber=i)

            main_lv.placements.append(TPB_Fiber_pla.name)

        pos = [self.SiPM_LCM_Mask_dx+self.SiPM_LCM_PCB_dx-self.Fiber_offset,+self.Fiber_dd-2*self.Fiber_pitch,Q('0cm')]
        for i in range(self.N_Fiber_LCM,2*self.N_Fiber_LCM):
            pos[1] = pos[1] + 2*self.Fiber_pitch

            rot = [Q('0.0deg'),Q('90.0deg'),Q('0.0deg')]

            TPB_Fiber_pos = geom.structure.Position('TPB_Fiber_pos_center_'+str(i),
                                                    pos[0],pos[1],pos[2])

            TPB_Fiber_rot = geom.structure.Rotation('TPB_Fiber_rot_center_'+str(i),
                                                    rot[0],rot[1],rot[2])

            TPB_Fiber_pla = geom.structure.Placement('TPB_Fiber_pla_center_'+str(i),
                                                    volume=TPB_Fiber_lv,
                                                    pos=TPB_Fiber_pos,
                                                    rot=TPB_Fiber_rot,
                                                    copynumber=i)

            main_lv.placements.append(TPB_Fiber_pla.name)

        # Construct SiPM Mask LV
        SiPM_LCM_Mask_shape = geom.shapes.Box('SiPM_LCM_Mask_shape',
                                       dx = self.SiPM_LCM_Mask_dx,
                                       dy = self.SiPM_LCM_Mask_dy,
                                       dz = self.SiPM_LCM_Mask_dz)

        SiPM_LCM_Mask_lv = geom.structure.Volume('volSiPM_LCM_Mask',
                                            material=self.SiPM_LCM_Mask_Material,
                                            shape=SiPM_LCM_Mask_shape)

        # Place SiPM Mask LV next to Fiber plane
        pos = [-self.Fiber_dz+self.SiPM_LCM_PCB_dx,Q('0mm'),Q('0mm')]

        SiPM_LCM_Mask_pos = geom.structure.Position('SiPM_LCM_Mask_pos_',
                                                pos[0],pos[1],pos[2])

        SiPM_LCM_Mask_pla = geom.structure.Placement('SiPM_LCM_Mask_pla',
                                                volume=SiPM_LCM_Mask_lv,
                                                pos=SiPM_LCM_Mask_pos)

        main_lv.placements.append(SiPM_LCM_Mask_pla.name)

        # Construct SiPM LV
        SiPM_LCM_shape = geom.shapes.Box('SiPM_LCM_shape',
                                       dx = self.SiPM_LCM_dx,
                                       dy = self.SiPM_LCM_dy,
                                       dz = self.SiPM_LCM_dz)

        SiPM_LCM_lv = geom.structure.Volume('volSiPM_LCM',
                                            material=self.SiPM_LCM_Material,
                                            shape=SiPM_LCM_shape)

        # Place SiPMs next to Fiber plane
        for n in range(self.N_SiPM_LCM):
            posipm = [self.SiPM_LCM_Mask_dx-self.SiPM_LCM_dx,-(self.N_SiPM_LCM-1)*self.SiPM_LCM_pitch+(2*n)*self.SiPM_LCM_pitch,Q('0cm')]

            SiPM_LCM_pos = geom.structure.Position('SiPM_LCM_pos_'+str(n),
                                                    posipm[0],posipm[1],posipm[2])

            SiPM_LCM_pla = geom.structure.Placement('SiPM_LCM_pla_'+str(n),
                                                    volume=SiPM_LCM_lv,
                                                    pos=SiPM_LCM_pos,
                                                    copynumber=n)

            SiPM_LCM_Mask_lv.placements.append(SiPM_LCM_pla.name)

        # Construct and place SiPM PCBs
        SiPM_LCM_PCB_shape = geom.shapes.Box('SiPM_LCM_PCB_shape',
                                       dx = self.SiPM_LCM_PCB_dx,
                                       dy = self.SiPM_LCM_PCB_dy,
                                       dz = self.SiPM_LCM_PCB_dz)

        SiPM_LCM_PCB_lv = geom.structure.Volume('volSiPM_LCM_PCB',
                                            material=self.SiPM_LCM_PCB_Material,
                                            shape=SiPM_LCM_PCB_shape)

        # Place SiPM PCBs next to SiPM Masks
        pos = [-self.Fiber_dz-self.SiPM_LCM_Mask_dx,Q('0cm'),Q('0cm')]

        SiPM_LCM_PCB_pos = geom.structure.Position('SiPM_LCM_PCB_pos',
                                                pos[0],pos[1],pos[2])

        SiPM_LCM_PCB_pla = geom.structure.Placement('SiPM_LCM_PCB_pla',
                                                volume=SiPM_LCM_PCB_lv,
                                                pos=SiPM_LCM_PCB_pos)

        main_lv.placements.append(SiPM_LCM_PCB_pla.name)
