#!/usr/bin/env python
'''
Builder del volume madre volMuonSystem, che contiene i piani del muon tagger /
catcher di SAND (geometria TAGGER4).

I piani sono i sub-builder (MuonTaggerPlaneBuilder, invariato): questo builder
li piazza dentro di se', e la hall piazza volMuonSystem.

PERCHE' UN'UNIONE DI BOX E NON UNA SCATOLA UNICA
    Una scatola d'aria lunga abbastanza da contenere tagger (a monte) e catcher
    (a valle) ingloberebbe volSAND: e' l'overlap della prima versione, vedi la
    docstring di MuonTaggerPlane.py.  Qui la forma e' l'unione booleana di un
    box per piano, ciascuno centrato sul proprio piano e piu' grande di
    `margin` per lato: il volume copre solo i piani e un velo d'aria attorno,
    e l'aria fra un piano e l'altro resta della caverna.
    Niente <assembly> GDML: Geant4 lo dissolve e il livello sparirebbe in
    edep-sim.

CONFIGURAZIONE
    subbuilders  i piani, nello stesso ordine delle righe di Positions
    Positions    centro di ciascun piano nel frame di volMuonSystem.  Il frame
                 di un'unione booleana e' quello del suo primo solido, quindi
                 l'origine e' il centro del PRIMO piano: la prima riga deve
                 essere nulla, e la hall piazza volMuonSystem nella posizione
                 hall-local del primo piano.
    margin       margine dell'involucro su ogni lato (default 1 mm)
    mat          materiale dell'involucro (default Air, come la caverna)

I piani non sono ruotati: il loro asse z locale resta lungo il fascio.
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
            raise ValueError('%s: serve una riga di Positions per ciascuno dei %d piani'
                             % (self.name, len(planes)))
        if any(c.magnitude != 0 for c in self.Positions[0]):
            raise ValueError('%s: la prima riga di Positions deve essere nulla '
                             '(origine del frame = centro del primo piano)' % self.name)

        # Involucro: un box per piano, unito al precedente nella posizione del
        # piano.  L'ultima unione e' la forma di volMuonSystem.
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

        # Unico volume del builder: e' questo che la hall piazzera'.
        self.add_volume(system_lv)
