// volBounds.C -- global bounding box (cm) of every placed volume whose name matches a regular
// expression, plus the box that encloses all of them.
//
//   root -b -q 'volBounds.C("geometry.gdml", "^volTMS$")'
//   root -b -q 'volBounds.C("geometry.gdml", "^volTMS$;^volTPCActive$", 0)'
//
// `patterns` is one or more regular expressions separated by ';', each reported separately
// (the GDML is only loaded once). A plain string matches as a substring, so use "^name$"
// for an exact volume name. `maxPrint` limits how many individual placements are listed.
//
// Each box is the shape's own bounding box transformed to world coordinates, so it is exact
// for boxes (TMS plates, LAr TPCs) and conservative for tubes, rotated or boolean shapes.
//
// Pattern syntax (PCRE, via TPRegexp):
//   ^volTMS$                  exactly volTMS
//   volTMS                    any name containing volTMS (also thinvolTMS, thickvol2TMS, ...)
//   ^(thinvolTMS|thickvolTMS)$  either name, combined into one union
//   (?i)argon                 case-insensitive
//   a;b;c                     three separate patterns (';' is split by this macro, not regex)
//
// Volume names in the ND hall geometries (checked on v2026.03.06):
//   LAr, outermost first
//     ^volArgonCubeDetector$        whole ND-LAr, including the cryostat
//     ^volArgonCubeCryostat$        cryostat (...WithTagger adds the tagger)
//     ^volLArBath$                  liquid argon bath
//     ^volArgonCubeDetector75$      module array (the production top_volume)
//     ^volNDBucket$, ^volArgonColumn$, ^volInnerDetector$          per-module structure
//     ^volHalfDetector$, ^volFieldcage$, ^volLAr$, ^volTPC$        per-TPC structure
//     ^volTPCActive$                active drift volume (70; absent from anti_fiducial files)
//     ^volTPCPlane$, ^volTPCPCB$, ^volTPCAsic$                     pixel readout planes
//   TMS
//     ^volTMS$                      TMS envelope
//     ^thinvol2?TMS$                thin steel plates
//     ^thickvol2?TMS$               thick steel plates
//     ^doublevol2?TMS$              double-thickness plates
//     ^(thin|thick|double)vol2?TMS$ all steel
//     ^scinBoxlv_orthoTMS$, ^scinBoxlv_parallelTMS$                scintillator by orientation
//     ^scinBoxlv.*TMS$              all scintillator (use maxPrint = 0)
//     ^modulelayervol               scintillator layers
//   Other
//     ^volDetEnclosure$             hall air volume
//     ^rockBox_lv$                  rock around the hall
//     ^KLOESolenoid                 SAND magnet cryostat parts
//     ^GRAIN_LAr_lv$                SAND GRAIN LAr target
//
// Older geometries may use other names. To list every volume name in a GDML:
//   grep -o '<volume name="[^"]*"' file.gdml | sed 's/.*="//;s/"//' | sort -u
#include "TGeoManager.h"
#include "TGeoBBox.h"
#include "TGeoNode.h"
#include "TGeoMatrix.h"
#include "TObjArray.h"
#include "TObjString.h"
#include "TPRegexp.h"

void printBounds(const char* pattern, int maxPrint)
{
  TPRegexp re(pattern);
  TGeoIterator it(gGeoManager->GetTopVolume());
  TGeoNode* node;
  TString path;
  double ulo[3] = {1e30, 1e30, 1e30}, uhi[3] = {-1e30, -1e30, -1e30};
  int nMatch = 0;

  printf("\n== %s ==\n", pattern);
  while ((node = it())) {
    if (!re.MatchB(node->GetVolume()->GetName())) continue;
    auto box = static_cast<TGeoBBox*>(node->GetVolume()->GetShape());
    const double* o = box->GetOrigin();
    double d[3] = {box->GetDX(), box->GetDY(), box->GetDZ()};
    const TGeoMatrix* m = it.GetCurrentMatrix();   // local -> world
    double lo[3] = {1e30, 1e30, 1e30}, hi[3] = {-1e30, -1e30, -1e30};
    for (int i = 0; i < 8; ++i) {
      double loc[3] = {o[0] + ((i & 1) ? d[0] : -d[0]),
                       o[1] + ((i & 2) ? d[1] : -d[1]),
                       o[2] + ((i & 4) ? d[2] : -d[2])};
      double g[3];
      m->LocalToMaster(loc, g);
      for (int k = 0; k < 3; ++k) { lo[k] = std::min(lo[k], g[k]); hi[k] = std::max(hi[k], g[k]); }
    }
    for (int k = 0; k < 3; ++k) { ulo[k] = std::min(ulo[k], lo[k]); uhi[k] = std::max(uhi[k], hi[k]); }
    if (nMatch++ < maxPrint) {
      it.GetPath(path);
      printf("%s\n  x [%9.2f, %9.2f]  y [%9.2f, %9.2f]  z [%9.2f, %9.2f]\n",
             path.Data(), lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]);
    }
  }
  if (nMatch == 0) {
    printf("No placed volume matches '%s'.\n", pattern);
    return;
  }
  printf("%d placements matching '%s'. Union (cm):\n", nMatch, pattern);
  printf("  x [%9.2f, %9.2f]\n  y [%9.2f, %9.2f]\n  z [%9.2f, %9.2f]\n",
         ulo[0], uhi[0], ulo[1], uhi[1], ulo[2], uhi[2]);
}

void volBounds(const char* gdml, const char* patterns, int maxPrint = 10)
{
  if (!TGeoManager::Import(gdml)) {
    printf("Could not import geometry from %s\n", gdml);
    return;
  }
  TObjArray* list = TString(patterns).Tokenize(";");
  for (auto p : *list) printBounds(static_cast<TObjString*>(p)->GetName(), maxPrint);
  delete list;
}
