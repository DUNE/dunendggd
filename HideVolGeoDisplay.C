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

void geoDisplay(TString filename, Int_t VisLevel=5)
{
	TGeoManager *geo = TGeoManager::Import(filename);
	geo->DefaultColors();

	std::vector<TString> volsToHide = {"volCompositeWindow"};
	//below print the volumes
	
	TObjArray *vollist = gGeoManager->GetListOfVolumes();
	TIter next(vollist);
	TObject *obj = next();
	while (obj) {
	  //obj->Print();
	  TString volName = obj->GetName();
	  std::cout << volName << std::endl;
	  TGeoVolume* volume = gGeoManager->FindVolumeFast(volName);
          //if(IsTStringInArray(volName, volsToHide)){
	    //volume->SetVisibility(false);
	  //}
	  obj = next();
	}

	geo->CheckOverlaps(1e-5,"d");
 	geo->PrintOverlaps();
	geo->SetVisOption(1);
	geo->SetVisLevel(VisLevel);
	geo->GetTopVolume()->Print();
	geo->GetTopVolume()->Draw("ogl");

	
	TGLViewer * v = (TGLViewer *)gPad->GetViewer3D();
	v->SetStyle(TGLRnrCtx::kOutline);
	v->SetSmoothPoints(kTRUE);
	v->SetLineScale(0.5);
	//	v->UseDarkColorSet();
	v->UpdateScene();
}
