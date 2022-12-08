void gdml2root(TString infile, TString outfile)
{
	if(!outfile.EndsWith("root"))
	{
		cout<< "Outout file must have .root extension: output.root" <<endl;
		exit(1);
	}

	TGeoManager *geo = TGeoManager::Import(infile);

	geo->CheckOverlaps(1e-5,"d");
 	geo->PrintOverlaps();
	geo->GetTopVolume()->Print();
	geo->Export(outfile);

}
