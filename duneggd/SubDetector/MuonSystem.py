#!/usr/bin/env python
'''
Builder of the volMuonSystem mother volume, which holds the external muon
tagger / catcher scintillator planes around SAND.

The planes are the sub-builders (MuonSystemPlaneBuilder, MuonSystemPlane.py):
this builder places them inside itself, and the hall places volMuonSystem.
The muon system does not depend on the SAND inner tracker: it only needs the
hall, so it can be combined with any SAND configuration.

WHY A UNION OF BOXES AND NOT A SINGLE BOX
    An air box long enough to hold an upstream and a downstream plane would
    enclose volSAND and overlap with it.  Here the shape is the boolean union
    of one box per plane, each centred on its plane and larger by `margin` on
    every side: the volume covers only the planes and a thin layer of air
    around them, and the air between the planes stays in the hall.
    No GDML <assembly>: Geant4 dissolves it and the level would disappear in
    edep-sim.

CONFIGURATION
    subbuilders  the planes, in the same order as the rows of Positions
    Positions    centre of each plane in the volMuonSystem frame.  The frame
                 of a boolean union is the frame of its first solid, so the
                 origin is the centre of the FIRST plane: the first row must
                 be zero, and the hall places volMuonSystem at the hall-local
                 position of the first plane.
    margin       envelope margin on every side (default 1 mm)
    mat          envelope material (default Air, as the hall)

The planes are not rotated: their local z axis stays along the beam.
'''

import gegede.builder
from gegede import Quantity as Q


class MuonSystemBuilder(gegede.builder.Builder):

    defaults = dict(
        Positions = None,
        margin    = Q('1mm'),
        mat       = 'Air',
    )

    def construct(self, geom):

        planes = self.get_builders()
        if self.Positions is None or len(self.Positions) != len(planes):
            raise ValueError('%s: one row of Positions is needed for each of the %d planes'
                             % (self.name, len(planes)))
        if any(c.magnitude != 0 for c in self.Positions[0]):
            raise ValueError('%s: the first row of Positions must be zero '
                             '(frame origin = centre of the first plane)' % self.name)

        # Envelope: one box per plane, joined to the previous ones at the
        # position of the plane.  The last union is the shape of volMuonSystem.
        envelope = None
        for i, (plane, pos) in enumerate(zip(planes, self.Positions)):
            plane_shape = geom.store.shapes.get(plane.get_volume().shape)
            box = geom.shapes.Box(
                self.name + '_' + plane.name + '_box',
                dx = plane_shape.dx + self.margin,
                dy = plane_shape.dy + self.margin,
                dz = plane_shape.dz + self.margin)
            if envelope is None:
                envelope = box
                continue
            box_pos = geom.structure.Position(box.name + '_pos', pos[0], pos[1], pos[2])
            name = self.name + ('_shape' if i == len(planes) - 1 else '_union%d' % i)
            envelope = geom.shapes.Boolean(name, type='union',
                                           first=envelope, second=box, pos=box_pos)

        system_lv = geom.structure.Volume('vol' + self.name,
                                          material = self.mat,
                                          shape    = envelope)

        for plane, pos in zip(planes, self.Positions):
            plane_lv  = plane.get_volume()
            plane_pos = geom.structure.Position(plane_lv.name + '_pos', pos[0], pos[1], pos[2])
            plane_rot = geom.structure.Rotation(plane_lv.name + '_rot',
                                                Q('0deg'), Q('0deg'), Q('0deg'))
            plane_pla = geom.structure.Placement(plane_lv.name + '_pla', volume=plane_lv,
                                                 pos=plane_pos, rot=plane_rot)
            system_lv.placements.append(plane_pla.name)

        # The only volume of this builder: the hall places it.
        self.add_volume(system_lv)
