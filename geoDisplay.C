// geoDisplay.C -- display di SAND + muon system con una palette ispirata ai
// disegni meccanici di KLOE/SAND.
//
//   root -l geoDisplay.C
//   root -l 'geoDisplay.C("altro.gdml", "", false)'   // altro file, senza export ne' overlap check
//
// Si disegna la caverna (volDetEnclosure) senza la caverna stessa: restano
// SAND e volMuonSystem.  I volumi d'aria e il gas di drift sono nascosti; i
// moduli dell'ECAL sono disegnati pieni, senza le ~420 lastre di ciascuno.
// Nel viewer GL: tab "Clipping" per tagliare il giogo e vedere l'interno.

#include "TGeoManager.h"
#include "TGeoVolume.h"
#include "TGeoMaterial.h"
#include "TColor.h"
#include "TGLViewer.h"
#include "TPRegexp.h"
#include "TVirtualPad.h"
#include "TString.h"

// Solo colori STANDARD di ROOT (ruota kAzure, kOrange, kViolet, ...): esistono in
// ogni sessione e in JSROOT.  Un colore creato con TColor::GetColor("#...") vive
// solo nella sessione che l'ha creato: il .root esportato salva l'indice ma non
// il colore, e riaperto (in ROOT o nel viewer di VS Code) diventa tutto grigio.
static void Paint(TGeoVolume* v, Color_t c)
{
	v->SetVisibility(kTRUE);
	v->SetLineColor(c);
}

// Colori e visibilita' di tutti i volumi della geometria.
void SANDPalette(TGeoManager* geo)
{
	TPRegexp ecalEndcapPart("^ECAL_ec_mod_(vert|curv|hor)_\\d+_lv$");
	TPRegexp trackerFrame("^s_\\d+_fr$"), trackerMylar("^s_\\d+_m$");
	TPRegexp targetC3H6("^s_\\d+_t_P$"), targetGraphite("^s_\\d+_t_C$");

	TIter next(geo->GetListOfVolumes());
	while (TGeoVolume* v = (TGeoVolume*)next()) {
		TString n = v->GetName();
		TString m = v->GetMaterial() ? v->GetMaterial()->GetName() : "";

		// Muon system: tagger e catcher con due colori distinti
		if (n == "volTaggerFar" || n == "volTaggerNear")         Paint(v, kBlue+1);    // #0000cc
		else if (n.BeginsWith("volCatcher")                      Paint(v, kOrange+7);  // #ff6600

		// Giogo: endcap sinistro e destro (pezzi A..D), barrel
		else if (n.BeginsWith("KLOEYokeEndcap") && n.Length() > 15) {
			const Color_t left[4]  = {kGray+2, kGray+1, kGray+2, kGray+1};   // #666666 #999999 #666666 #999999
			const Color_t right[4] = {kGray+2, kGray+1, kGray+2, kGray+1};   // #666666 #999999 #666666 #999999
			int piece = n[14] - 'A';                       // KLOEYokeEndcap<A..D><L|R>_volume
			if (piece < 0 || piece > 3) piece = 0;
			Paint(v, n[15] == 'L' ? left[piece] : right[piece]);
		}
		else if (n.BeginsWith("KLOEYokeBarrel")                  Paint(v, kGray+2);    // #666666

		// Solenoide: criostato, guscio della bobina, bobina
		else if (n.BeginsWith("KLOESolenoidCoilShell")           Paint(v, kGray+1);    // #999999
		else if (n.BeginsWith("KLOESolenoidCoil")                Paint(v, kOrange+5);  // #cc6633
		else if (n.BeginsWith("KLOESolenoidCryostat")            Paint(v, kGray);      // #cccccc

		// ECAL: moduli pieni, barrel ed endcap
		else if (n == "ECAL_lv")                       { Paint(v, kAzure-7); v->SetVisDaughters(kFALSE); }  // #336699
		else if (ecalEndcapPart.MatchB(n)              { Paint(v, kAzure-8); v->SetVisDaughters(kFALSE); }  // #6699cc

		// Tracker: cornici, mylar, bersagli di C3H6 e di grafite
		else if (trackerFrame.MatchB(n)                          Paint(v, kOrange-7);  // #996633
		else if (trackerMylar.MatchB(n)                          Paint(v, kOrange-8);  // #cc9966
		else if (targetC3H6.MatchB(n)                            Paint(v, kOrange-9);  // #ffcc99
		else if (targetGraphite.MatchB(n)                        Paint(v, kGray+3);    // #333333

		// GRAIN: dal guscio esterno all'argon liquido
		else if (n == "GRAIN_Ext_vessel_outer_layer_lv")         Paint(v, kMagenta-1); // #663366
		else if (n == "GRAIN_Honeycomb_layer_lv")                Paint(v, kMagenta-2); // #993399
		else if (n == "GRAIN_Ext_vessel_inner_layer_lv")         Paint(v, kMagenta+1); // #cc00cc
		else if (n == "GRAIN_inner_vessel_lv")                   Paint(v, kMagenta-10); // #ffccff
		else if (n == "GRAIN_LAr_lv")                            Paint(v, kMagenta-6); // #cc66cc

		// Contenitori d'aria, vuoto, roccia, gas di drift: nascosti
		else if (m == "Air" || m == "Air35C" || m == "Vac" || m == "Vacuum" ||
		         m == "Vacuum_cryo" || m == "Rock" || m == "driftGas")
			v->SetVisibility(kFALSE);

		// Tutto il resto
		else Paint(v, kGray+1);   // #999999
	}

	// In ROOT la trasparenza (0-100) e' una proprieta' del MATERIALE, non del
	// volume: vale per tutti i volumi fatti dello stesso materiale.
	struct { const char* mat; Char_t t; } transp[] = {
		{"Iron", 85}, {"Aluminum", 80}, {"Copper", 20}, {"Air", 20},   // Air = moduli ECAL pieni
		{"Scintillator", 60}, {"carbonComposite", 0}, {"Mylar", 70},
		{"C3H6", 40}, {"Graphite", 20},
		{"Carbon_fiber", 40}, {"Steel", 40}, {"LAr", 20},
	};
	for (auto& t : transp)
		if (TGeoMaterial* mat = geo->GetMaterial(t.mat)) mat->SetTransparency(t.t);
}


void geoDisplay(const char* gdml = "/storage/gpfs_data/neutrino/users/glupi/ND-production/ND_Production/geometry/Only_SAND_MuonSystem.gdml",
                const char* rootOut = "/storage/gpfs_data/neutrino/users/glupi/dunendggd/Only_SAND_MuonSystem.root",
                Bool_t checkOverlaps = kTRUE)
{
	TGeoManager* geo = TGeoManager::Import(gdml);
	if (!geo) return;

	if (checkOverlaps) {
		geo->CheckOverlaps(1e-5, "d");
		geo->PrintOverlaps();
	}

	SANDPalette(geo);

	// Export dopo la palette: il .root conserva colori e visibilita'.
	if (rootOut && *rootOut) geo->Export(rootOut);

	geo->SetVisLevel(7);
	geo->GetVolume("volDetEnclosure")->Draw("ogl");

	// sfondo chiaro, come nei disegni meccanici
	if (TGLViewer* glv = dynamic_cast<TGLViewer*>(gPad->GetViewer3D())) {
		glv->UseLightColorSet();
		glv->RequestDraw();
	}
}
