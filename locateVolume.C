void locateVolume(TString filename, TString volname)
{
  cout << "== Loading Geometry ==" << endl;
  TGeoManager *geo = TGeoManager::Import(filename);

  cout << "== Switching to volume path: " << volname << " ==" << endl;
  geo->cd(volname);

  cout << "== Volume information ==" << endl;
  TGeoVolume *vol = geo->GetCurrentVolume();
  vol->Print();

  cout << "== Node information ==" << endl;
  TGeoNode *node = geo->GetCurrentNode();
  node->Print();

  cout << "== Matrix information ==" << endl;
  TGeoMatrix *mat = gGeoManager->GetCurrentMatrix();
  mat->Print();
}
