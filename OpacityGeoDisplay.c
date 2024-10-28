void OpacityGeoDisplay(TString filename, Int_t VisLevel=5)
{
	TGeoManager *geo = TGeoManager::Import(filename);
	geo->DefaultColors();

	//set Transparency of a volume
	//geo->GetVolume("volWarmSteel")->SetTransparency(99);
	
	
	
	geo->CheckOverlaps(1e-5,"d");
 	geo->PrintOverlaps();
	geo->SetVisOption(1);
	geo->SetVisLevel(VisLevel);
	geo->GetTopVolume()->Print();
	//geo->GetVolume("volCompositeWindow")->Draw("ogl");
	//Draw needs "ogl" or else there are errors
	geo->GetVolume("volArgonCubeCryostat")->Draw("ogl");

	//TString volName="volWorld";
	//geo->FindVolumeFast(volName)->Draw("ogl");
	//geo->GetTopVolume()->Draw("ogl");

        
	//--- close the geometry
	//geo->CloseGeometry();
	
	TGLViewer * v = (TGLViewer *)gPad->GetViewer3D();
	v->SetStyle(TGLRnrCtx::kOutline);
	v->SetSmoothPoints(kTRUE);
	v->SetLineScale(0.5);
	//	v->UseDarkColorSet();
	v->UpdateScene();
}
