
import gegede.builder
from gegede import Quantity as Q


class MuonSystemPlaneBuilder(gegede.builder.Builder):

    defaults = dict(
        thickness = Q('5mm'),
        halfX     = Q('4000mm'),
        halfY     = Q('3600mm'),
        sensdet   = 'MuonSystem',
        mat       = 'Scintillator',
    )

    def construct(self, geom):

        plane_shape = geom.shapes.Box(
            self.name + '_shape',
            dx = self.halfX,
            dy = self.halfY,
            dz = 0.5 * self.thickness)

        plane_lv = geom.structure.Volume(
            'vol' + self.name,
            material = self.mat,
            shape    = plane_shape)
        
        plane_lv.params.append(('SensDet', self.sensdet))

return