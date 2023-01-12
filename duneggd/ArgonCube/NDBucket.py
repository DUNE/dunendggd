"""NDBucket.py

Original Author: A. Mastbaum, Rutgers

Not really a bucket, but adds G10 structure surrounding the InnerDetector in
the ND-LAr configuration.
"""

import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class NDBucketBuilder(gegede.builder.Builder):
    """ Class to build NDBucket geometry."""

    def configure(self,Bucket_dimension,Backplate_dx,Backplate_OffsetX,Backplate_ExtraY,**kwargs):
        # Read dimensions form config file
        self.Bucket_dx = Bucket_dimension['dx']
        self.Bucket_dy = Bucket_dimension['dy']
        self.Bucket_dz = Bucket_dimension['dz']

        self.Backplate_dx       = Backplate_dx
        self.Backplate_OffsetX  = Backplate_OffsetX
        self.Backplate_ExtraY   = Backplate_ExtraY

        # Material definitons
        self.G10_Material           = 'G10'
        self.LArPhase_Material      = 'LAr'
        self.Material               = 'LAr'

        # Subbuilders
        self.InnerDetector_builder  = self.get_builder('InnerDetector')
        self.HalfDetector_builder   = self.get_builder('HalfDetector')

    def construct(self,geom):
        """Construct the geometry."""

        self.halfDimension  = {
            'dx': self.Bucket_dx,
            'dy': self.Bucket_dy,
            'dz': self.Bucket_dz
        }

        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('NDBucketBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        # Construct a rectangular column of LAr that everything sits inside
        ArgonColumn_shape = geom.shapes.Box('ArgonColumn_shape',
                                            dx=self.Bucket_dx,
                                            dy=self.Bucket_dy,
                                            dz=self.Bucket_dz)

        ArgonColumn_lv = geom.structure.Volume('volArgonColumn',
                                        material=self.LArPhase_Material,
                                        shape=ArgonColumn_shape)

        pos = [Q('0cm'),Q('0cm'),Q('0cm')]

        ArgonColumn_pos = geom.structure.Position('ArgonColumn_pos',
                                                  pos[0],pos[1],pos[2])

        ArgonColumn_pla = geom.structure.Placement('ArgonColumn_pla',
                                                   volume=ArgonColumn_lv,
                                                   pos=ArgonColumn_pos)

        main_lv.placements.append(ArgonColumn_pla.name)

        # Build Inner Detector
        pos = [Q('0cm'),-self.Bucket_dy+self.InnerDetector_builder.halfDimension['dy'],Q('0cm')]

        InnerDetector_lv = self.InnerDetector_builder.get_volume()

        InnerDetector_pos = geom.structure.Position(self.InnerDetector_builder.name+'_pos',
                                                pos[0],pos[1],pos[2])

        InnerDetector_pla = geom.structure.Placement(self.InnerDetector_builder.name+'_pla',
                                                volume=InnerDetector_lv,
                                                pos=InnerDetector_pos)

        ArgonColumn_lv.placements.append(InnerDetector_pla.name)

        # Backplates
        Backplate_shape = geom.shapes.Box('Backplate_shape',
                                       dx=self.Backplate_dx,
                                       dy=self.InnerDetector_builder.halfDimension['dy']+self.Backplate_ExtraY,
                                       dz=self.InnerDetector_builder.halfDimension['dz'])

        Backplate_lv = geom.structure.Volume('Backplate_lv',
                                        material=self.G10_Material,
                                        shape=Backplate_shape)

        Backplate_y = -self.Bucket_dy + (self.InnerDetector_builder.halfDimension['dy'] + self.Backplate_ExtraY)

        for i, (side, sign) in enumerate((('L', -1), ('R', 1))):
            pos = [
                sign*(self.Bucket_dx-2*self.Backplate_OffsetX+self.Backplate_dx),
                Backplate_y,
                Q('0cm')
            ]
        
            Backplate_pos = geom.structure.Position('Backplate_pos_'+side,
                                                    pos[0],pos[1],pos[2])

            Backplate_pla = geom.structure.Placement('Backplate_pla_'+side,
                                                    volume=Backplate_lv,
                                                    pos=Backplate_pos,
                                                    copynumber=i)

            ArgonColumn_lv.placements.append(Backplate_pla.name)

        # Extra G10 extending in y above the InnerDetector top
        FieldcageTop_shape = geom.shapes.Box('FieldcageTop_shape',
                                       dx=self.InnerDetector_builder.halfDimension['dx'],
                                       dy=self.Backplate_ExtraY,
                                       dz=self.HalfDetector_builder.Fieldcage_dd)

        FieldcageTop_lv = geom.structure.Volume('FieldcageTop_lv',
                                        material=self.G10_Material,
                                        shape=FieldcageTop_shape)

        FieldcageTop_y = -self.Bucket_dy + (2*self.InnerDetector_builder.halfDimension['dy'] + self.Backplate_ExtraY)

        for i, (side, sign) in enumerate((('US', -1),('DS', 1))):
            pos = [
                Q('0cm'),
                FieldcageTop_y,
                sign*(self.HalfDetector_builder.Fieldcage_dz-self.HalfDetector_builder.Fieldcage_dd)
            ]

            FieldcageTop_pos = geom.structure.Position('FieldcageTop_pos_'+side,
                                                       pos[0],pos[1],pos[2])

            FieldcageTop_pla = geom.structure.Placement('FieldcageTop_pla_'+side,
                                                        volume=FieldcageTop_lv,
                                                        pos=FieldcageTop_pos,
                                                        copynumber=i)

            ArgonColumn_lv.placements.append(FieldcageTop_pla.name)

        # G10 gap fillers connecting backplate to fieldcage
        FieldcageGap = (self.Bucket_dx - self.InnerDetector_builder.halfDimension['dx']) / 2 - self.Backplate_dx * 3/2

        FieldcageGap_shape = geom.shapes.Box('FieldcageGap_shape',
                                       dx=FieldcageGap,
                                       dy=self.InnerDetector_builder.halfDimension['dy']+self.Backplate_ExtraY,
                                       dz=self.HalfDetector_builder.Fieldcage_dd)

        FieldcageGap_lv = geom.structure.Volume('FieldcageGap_lv',
                                        material=self.G10_Material,
                                        shape=FieldcageGap_shape)



        px = self.InnerDetector_builder.halfDimension['dx'] + FieldcageGap
        py = Backplate_y
        pz = self.InnerDetector_builder.halfDimension['dz'] - self.HalfDetector_builder.Fieldcage_dd

        for ii, (i, LR) in enumerate([(-1, 'L'), (1, 'R')]):
            for jj, (j, UD) in enumerate([(-1, 'U'), (1, 'D')]):
                pos = [i*px, py, j*pz]

                FieldcageGap_pos = geom.structure.Position('FieldcageGap_pos_%s_%s' % (LR, UD),
                                                           pos[0],pos[1],pos[2])

                FieldcageGap_pla = geom.structure.Placement('FieldcageTop_pla_%s_%s' % (LR, UD),
                                                            volume=FieldcageGap_lv,
                                                            pos=FieldcageGap_pos,
                                                            copynumber=2*ii*jj)

                ArgonColumn_lv.placements.append(FieldcageGap_pla.name)

