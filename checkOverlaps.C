void checkOverlaps(TString filename)
{
    TGeoManager *geo = TGeoManager::Import(filename);

    cout<<"======================== Checking Geometry ============================="<<endl;
    geo->CheckGeometry();
    cout<<"========================       Done!       ============================="<<endl;

    cout<<"======================== Checking Overlaps ============================="<<endl;
    geo->CheckOverlaps(1e-5,"s");
    geo->PrintOverlaps();
    cout<<"========================       Done!       =============================\n\n\n"<<endl;

    if(not gROOT->IsBatch()){
        TObjArray* overlaps=geo->GetListOfOverlaps();
        for(int i=0; i<overlaps->GetEntries(); i++){
            TObject* overlap=overlaps->At(i);
            cout<<"========================  Drawing Overlaps ============================="<<endl;
            cout<<"================= Overlap messages will duplicate below ================"<<endl;
            cout<<"=================     Overlaps are in units of cm       ================"<<endl;
            TCanvas* c = new TCanvas();
            overlap->Draw("");
            TCanvas* cogl = new TCanvas();
            overlap->Draw("ogl");
            cout<<"========================       Done!       =============================\n\n\n"<<endl;
        }
    }
}
