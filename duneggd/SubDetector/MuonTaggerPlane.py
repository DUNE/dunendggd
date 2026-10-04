#!/usr/bin/env python
'''
Builder di UN SINGOLO piano di scintillatore per il muon tagger / catcher di
SAND.

Un'istanza = un piano.  I quattro piani (due tagger a monte, due catcher a
valle) sono quattro sezioni distinte del file di configurazione, ciascuna
piazzata dalla hall alla propria posizione.

PERCHE' UN PIANO PER ISTANZA E NON UN ASSIEME
    Una prima versione racchiudeva i quattro piani in un unico volume madre
    d'aria.  Quel contenitore era necessariamente lungo abbastanza da coprire
    monte e valle, quindi INGLOBAVA volSAND: il test di overlap a campionamento
    segnalava "volSAND overlapping volMuonTagger" per ~359 cm.  I piani in se'
    non toccavano nulla, ma il contenitore si'.
    Con un piano per istanza non c'e' nessun contenitore, quindi nessuna
    sovrapposizione possibile, e ogni piano si sposta indipendentemente
    cambiando una riga di configurazione: e' anche la forma piu' comoda per lo
    scan di ottimizzazione.

CONFIGURAZIONE
    thickness  spessore lungo il fascio (default 5 mm: un MIP deposita ~1 MeV,
               abbondantemente sopra soglia; con 0.5 mm sarebbero 0.1 MeV, al
               limite.  In X0 sono l'1.2%, quindi la perturbazione della
               traiettoria resta trascurabile)
    halfX      semi-lato trasverso orizzontale
    halfY      semi-lato trasverso verticale
    sensdet    nome del rivelatore sensibile: gli hit compaiono in
               SegmentDetectors["<sensdet>"] negli EDEPSIM
    mat        materiale

SISTEMA DI RIFERIMENTO
    Il piano e' un box centrato nell'origine del proprio volume: la posizione
    la stabilisce la hall, in ND_Hall_Air_Volume_Only_SAND.cfg.
    Il box e' sottile lungo il proprio asse z locale; con ROTAZIONE IDENTITA'
    nella hall quell'asse coincide con il FASCIO, che e' quello che serve.
    NON dare a questi piani la rotazione -90deg di SAND: quella serve a SAND
    perche' l'asse del suo solenoide e' trasverso al fascio.
'''

import gegede.builder
from gegede import Quantity as Q


#!/usr/bin/env python
'''
Builder di UN SINGOLO piano di scintillatore per il muon tagger / catcher di
SAND.

Un'istanza = un piano.  I quattro piani (due tagger a monte, due catcher a
valle) sono quattro sezioni distinte del file di configurazione, ciascuna
piazzata dalla hall alla propria posizione.

PERCHE' UN PIANO PER ISTANZA E NON UN ASSIEME
    Una prima versione racchiudeva i quattro piani in un unico volume madre
    d'aria.  Quel contenitore era necessariamente lungo abbastanza da coprire
    monte e valle, quindi INGLOBAVA volSAND: il test di overlap a campionamento
    segnalava "volSAND overlapping volMuonTagger" per ~359 cm.  I piani in se'
    non toccavano nulla, ma il contenitore si'.
    Con un piano per istanza non c'e' nessun contenitore, quindi nessuna
    sovrapposizione possibile, e ogni piano si sposta indipendentemente
    cambiando una riga di configurazione: e' anche la forma piu' comoda per lo
    scan di ottimizzazione.

CONFIGURAZIONE
    thickness  spessore lungo il fascio (default 5 mm: un MIP deposita ~1 MeV,
               abbondantemente sopra soglia; con 0.5 mm sarebbero 0.1 MeV, al
               limite.  In X0 sono l'1.2%, quindi la perturbazione della
               traiettoria resta trascurabile)
    halfX      semi-lato trasverso orizzontale
    halfY      semi-lato trasverso verticale
    sensdet    nome del rivelatore sensibile: gli hit compaiono in
               SegmentDetectors["<sensdet>"] negli EDEPSIM
    mat        materiale

SISTEMA DI RIFERIMENTO
    Il piano e' un box centrato nell'origine del proprio volume: la posizione
    la stabilisce la hall, in ND_Hall_Air_Volume_Only_SAND.cfg.
    Il box e' sottile lungo il proprio asse z locale; con ROTAZIONE IDENTITA'
    nella hall quell'asse coincide con il FASCIO, che e' quello che serve.
    NON dare a questi piani la rotazione -90deg di SAND: quella serve a SAND
    perche' l'asse del suo solenoide e' trasverso al fascio.
'''

import gegede.builder
from gegede import Quantity as Q


class MuonTaggerPlaneBuilder(gegede.builder.Builder):

    defaults = dict(
        thickness = Q('5mm'),
        halfX     = Q('4000mm'),
        halfY     = Q('3600mm'),
        sensdet   = 'MuonTagger',
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

        # Rende il volume SENSIBILE: senza questa riga edep-sim non produce
        # alcun hit e il piano e' solo materiale passivo.
        plane_lv.params.append(('SensDet', self.sensdet))

        # Unico volume del builder: e' questo che la hall piazzera'.
        self.add_volume(plane_lv)