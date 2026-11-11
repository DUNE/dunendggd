void geoDisplay()
{
	//gSystem->Load("libGdml");
	gSystem->Load("libGeom");
	TGeoManager *geo = new TGeoManager();
	geo->Import("/storage/gpfs_data/neutrino/users/glupi/dunendggd/only_SAND_DRIFT_TAGGER3.gdml");
	geo->Export("/storage/gpfs_data/neutrino/users/glupi/dunendggd/only_SAND_DRIFT_TAGGER3.root");
	
	geo->DefaultColors();


	geo->CheckOverlaps(1e-5,"d");
 	geo->PrintOverlaps();

	//geo->SetMaxVisNodes(70000);
	//geo->SetVisLevel(3);
	geo->SetVisLevel(4);
	//geo->ViewLeaves(true);

       	geo->GetTopVolume()->Draw("ogl");
}
