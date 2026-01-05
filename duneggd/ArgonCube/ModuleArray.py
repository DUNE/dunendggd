""" ModuleArray.py

Original Author: A. Mastbaum, Rutgers

A bank of ND modules (NDBuckets)
"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class ModuleArrayBuilder(gegede.builder.Builder):
    """ Class to build Module Array geometry."""

    def configure(self, N_ModuleX, N_ModuleZ, TopLArHeight, **kwargs):
        self.Material   = 'LAr'

        # Read dimensions form config file
        self.N_ModuleX  = N_ModuleX
        self.N_ModuleZ  = N_ModuleZ
        self.TopLArHeight = TopLArHeight

        # Subbuilders
        self.NDBucket_builder = self.get_builder('NDBucket')
        self.Grating_builder = self.get_builder('Grating')

    def construct(self,geom):
        """ Construct the geometry."""

        arraydz = self.Grating_builder.halfDimension['dy']
        GratingHeight = 0
        self.halfDimension  = { 'dx':   self.NDBucket_builder.halfDimension['dx']*self.N_ModuleX,
                                'dy':   self.NDBucket_builder.halfDimension['dy'] + self.TopLArHeight + GratingHeight,
                                'dz':   arraydz}

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('ModuleArrayBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Build Array
        for i in range(self.N_ModuleX):
            # Place an array of modules
            for j in range(self.N_ModuleZ):
                pos = [
                    -self.halfDimension['dx']+(2*i+1)*self.NDBucket_builder.halfDimension['dx'],
                    -self.halfDimension['dy']+self.NDBucket_builder.halfDimension['dy'],
                    -arraydz+(2*j+1)*self.NDBucket_builder.halfDimension['dz']
                ]

                Module_lv = self.NDBucket_builder.get_volume()

                Module_pos = geom.structure.Position(self.NDBucket_builder.name+'_pos_'+str(i)+'.'+str(j),
                                                        pos[0],pos[1],pos[2])

                Module_pla = geom.structure.Placement(self.NDBucket_builder.name+'_pla_'+str(i)+'.'+str(j),
                                                        volume=Module_lv,
                                                        pos=Module_pos,
                                                        copynumber=2*j+i)

                main_lv.placements.append(Module_pla.name)

            # Add grating
            Grating_lv = self.Grating_builder.get_volume()
            pos = [
                -self.halfDimension['dx']+(2*i+1)*self.NDBucket_builder.halfDimension['dx'],
                -self.halfDimension['dy']+2*self.NDBucket_builder.halfDimension['dy']+self.Grating_builder.halfDimension['dx'],
                Q('0mm')
            ]
            Grating_pos = geom.structure.Position('Grating_pos_'+str(i),pos[0],pos[1],pos[2])
            Grating_rot = geom.structure.Rotation('Grating_rot_'+str(i),x='0deg',y='-90deg',z='-90deg')
            Grating_pla = geom.structure.Placement('Grating_pla_'+str(i),volume=Grating_lv,pos=Grating_pos,rot=Grating_rot,copynumber=i)
            main_lv.placements.append(Grating_pla.name)


class SimpleTPCArrayBuilder(gegede.builder.Builder):
    """Class to build simple array of TPCs"""

    def configure(self, N_TpcX=1, N_TpcY=1, N_TpcZ=1, **kwargs):
        self.Material = 'LAr'

        self.N_TpcX = N_TpcX
        self.N_TpcY = N_TpcY
        self.N_TpcZ = N_TpcZ

        self.TPC_builder = self.get_builder()

    def construct(self, geom):
        self.halfDimension = {
            'dx': self.TPC_builder.halfDimension['dx'] * self.N_TpcX,
            'dy': self.TPC_builder.halfDimension['dy'] * self.N_TpcY,
            'dz': self.TPC_builder.halfDimension['dz'] * self.N_TpcZ
        }

        main_lv, _mainhDim = ltools.main_lv(self, geom, 'Box')
        print('SimpleTpcArrayBuilder::construct()')
        print('main_lv = ' + main_lv.name)
        self.add_volume(main_lv)

        for i in range(self.N_TpcX):
            for j in range(self.N_TpcY):
                for k in range(self.N_TpcZ):
                    copy = k + (j * self.N_TpcZ) + (i * self.N_TpcY * self.N_TpcZ)

                    pos = [
                        -self.halfDimension['dx'] + (i+1)*self.TPC_builder.halfDimension['dx'],
                        -self.halfDimension['dy'] + (j+1)*self.TPC_builder.halfDimension['dy'],
                        -self.halfDimension['dz'] + (k+1)*self.TPC_builder.halfDimension['dz']
                    ]

                    TPC_lv = self.TPC_builder.get_volume()

                    TPC_pos = geom.structure.Position(f'{self.TPC_builder.name}_pos_{i}.{j}.{k}',
                                                      pos[0], pos[1], pos[2])

                    TPC_pla = geom.structure.Placement(f'{self.TPC_builder.name}_pla_{i}.{j}.{k}',
                                                       volume=TPC_lv, pos=TPC_pos, copynumber=copy)

                    main_lv.placements.append(TPC_pla.name)
