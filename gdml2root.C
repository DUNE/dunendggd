void gdml2root(TString infile, TString outfile)
{
  if(!outfile.EndsWith("root"))
  {
    cout<< "Outout file must have .root extension: output.root" <<endl;
      exit(1);
  }

  TGeoManager *geo = TGeoManager::Import(infile);

  geo->GetTopVolume()->Print();
  geo->SetVisLevel(1);
  geo->Export(outfile);

}
