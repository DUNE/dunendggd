//
//  geovis.C
//  garsoft-mrb
//
//  Original from Brian Rebel
//  
//
#include "TGeoManager.h"
#include "TFile.h"
#include "TSystem.h"
#include "TString.h"
#include "TObjArray.h"

bool IsTStringInArray(const TString& targetString, std::vector<TString> stringArray) {
    if (stringArray.size() == 0)
        return false;

    // Loop through the array and check if targetString is present
    for (int i = 0; i < stringArray.size(); ++i) {
        TString currentString = stringArray[i];
        if (currentString && currentString.Contains(targetString))
            return true;
    }

    return false;
}

void hideVolumes(TGeoVolume* volume){
  volume->SetVisibility(false);
  TObjArray* daughters = volume->GetNodes();
  if (daughters) {
    int numDaughters = daughters->GetEntriesFast();
    for (int i = 0; i < numDaughters; ++i) {
        TGeoNode* node = (TGeoNode*)daughters->UncheckedAt(i);
        //node->SetVisibility(false);
        hideVolumes(node->GetVolume());
    }
  } 
}

void hideVolumesNotDaughters(TGeoVolume* volume){
  volume->SetVisibility(false);
  std::cout << "    volume: " << volume->GetName() << std::endl;
  TObjArray* daughters = volume->GetNodes();
  if (daughters) {
    int numDaughters = daughters->GetEntriesFast();
    for (int i = 0; i < numDaughters; ++i) {
        TGeoNode* node = (TGeoNode*)daughters->UncheckedAt(i);
        node->SetVisibility(true);
        TGeoVolume* daughter_volume = node->GetVolume();
        std::cout << "        daughter: " << daughter_volume->GetName() << std::endl;
        //hideVolumesNotDaughters(node->GetVolume());
    }
  } 
}

typedef struct _drawopt {
  const char* volume;
  int         color;
  float       transparency;
} drawopt;
// filebase is for the gdml file   TString filebase= "nd_hall_with_lar_tms_sand_old_window.gdml"
void geoVis_heirarchy(TString filebase, TString volName="volWorld", bool checkoverlaps=false, bool writerootfile=false){
  
  gSystem->Load("libGeom");
  gSystem->Load("libGdml");
  
  TString gdmlfile=filebase;
  //gdmlfile += ".gdml";
  TGeoManager::Import(gdmlfile);

  /* drawopt opt[] = {
    {"volWorld",           0},
    {"volDetEnclosure",    0},
    {"volCryostat",        0},
    {"volTPCWidthFace",    0},
    {"volTPCLengthFace",   0},
    {"volTPCBottomFace",   0},
    {"volTubBottom",       0},
    {"voltheX",            0},
    {"volArgon_solid_L",   0},
    {"volArgon_cap_L",     0},
    {"volArgon_cap_front", 0},
    {"volTPC",             0},
    {"TPCGas_vol",         0},
    {"volDetEnclosure",    0},
    {"volTPCActive",       0},
    {"volYokeBarrel",      kBlue},
    {0, 0}
  }; */
  
  /* for (int i=0;; ++i) {
    if (opt[i].volume==0) break;
    std::cout << opt[i].volume << std::endl;
    gGeoManager->FindVolumeFast(opt[i].volume)->SetLineColor(opt[i].color);
    gGeoManager->FindVolumeFast(opt[i].volume)->SetTransparency(opt[i].transparency);
  } */
  
  /* TList* mat = gGeoManager->GetListOfMaterials();
  TIter next(mat);
  TObject *obj;
  while (obj = next()) {
   obj->Print();
  } */

  std::vector<TString> volsToHide = {/*"volCryostat",
                                     "volCryostatEndcap",
                                     "volYokeEndcap"
                                     "volEndcapECal",
                                     "volYokeBarrel"*/};

  std::vector<TString> volsToHideLAr = {/*"volArgonCubeCryostat",
					  "volWarmSteel"*/};

  if (checkoverlaps)
    {
      gGeoManager->CheckOverlaps(0.01);
      gGeoManager->PrintOverlaps();
    }
  gGeoManager->SetMaxVisNodes(70000);

  // I think the while loop os not relevant if I am not hiding anything
  TObjArray *vollist = gGeoManager->GetListOfVolumes();
  TIter next(vollist);
  TObject *obj = next();
  while (obj) {
    //obj->Print();
    TString volName = obj->GetName();
    std::cout << volName << std::endl;
    TGeoVolume* volume = gGeoManager->FindVolumeFast(volName);
    if(IsTStringInArray(volName, volsToHide)){
      hideVolumes(volume);
    }
    if(IsTStringInArray(volName, volsToHideLAr)){
      hideVolumesNotDaughters(volume);
    }
    obj = next();
   }

  //gGeoManager->GetTopVolume()->Draw();
  gGeoManager->FindVolumeFast(volName)->Draw("ogl");
  //gGeoManager->FindVolumeFast(volName)->Draw("");

  if (writerootfile)
    {
      TString rootfile=filebase;
      rootfile += ".root";
      TFile *tf = new TFile(rootfile, "RECREATE");
      gGeoManager->Write();
      tf->Close();
    }
}
