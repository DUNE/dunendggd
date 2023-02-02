void checkOverlaps(TString filename, Int_t method =0)
{
  TGeoManager *geo = TGeoManager::Import(filename);
  cout<<"======================== Checking Geometry ============================="<<endl;
  //geo->CheckGeometry();
  //cout<<"========================       Done!       ============================="<<endl;
  if(method==1){
    cout<<"======================== Checking Overlaps with samplig method ============================="<<endl;
    cout<<"Enter Method: "<<endl;
    geo->CheckOverlaps(1e-6,"s");
    geo->PrintOverlaps();
    cout<<"========================       Done!       =============================\n\n\n"<<endl;
    if(not gROOT->IsBatch()){
      TObjArray* overlaps=geo->GetListOfOverlaps();
      for(int i=0; i<overlaps->GetEntries(); i++){
        TObject* overlap=overlaps->At(i);
        cout<<"========================  Drawing Overlaps ============================="<<endl;
        cout<<"================= Overlap messages will duplicate below ================"<<endl;
        cout<<"=================     Overlaps are in units of cm       ================"<<endl;
        TCanvas* c = new TCanvas("c","sampling method");
        overlap->Draw("");
        TCanvas* cogl = new TCanvas();
        overlap->Draw("ogl");
        cout<<"========================       Done!       =============================\n\n\n"<<endl;
      }
    }
  } else {
    cout<<"======================== Checking Overlaps with Standard Method ============================="<<endl;
    geo->CheckOverlaps(1e-6);
    geo->PrintOverlaps();
    cout<<"========================       Done!       =============================\n\n\n"<<endl;
    if(not gROOT->IsBatch()){
      TObjArray* overlaps_standard=geo->GetListOfOverlaps();
      for(int i=0; i<overlaps_standard->GetEntries(); i++){
        TObject* overlap=overlaps_standard->At(i);
        cout<<"========================  Drawing Overlaps ============================="<<endl;
        cout<<"================= Overlap messages will duplicate below ================"<<endl;
        cout<<"=================     Overlaps are in units of cm       ================"<<endl;
        TCanvas* c_standard = new TCanvas("c_standard","standard method");
        overlap->Draw();
        TCanvas* p = new TCanvas("p","standard method_1");
        overlap->Draw("ogl");
        cout<<"========================       Done!       =============================\n\n\n"<<endl;
      }
    }
  }
}
