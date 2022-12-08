void checkOverlaps(TString filename)
{
	TGeoManager *geo = new TGeoManager();
	geo->Import(filename);

	cout<<"======================== Checking Geometry ============================="<<endl;
	//geo->CheckGeometry();
	//cout<<"========================       Done!       ============================="<<endl;
	
	cout<<"======================== Checking Overlaps with Standard Method ============================="<<endl;
	geo->CheckOverlaps(1e-6);
	geo->PrintOverlaps();
	cout<<"========================       Done!       =============================\n\n\n"<<endl;
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
	/*cout<<"======================== Checking Overlaps with samplig method ============================="<<endl;
       	geo->CheckOverlaps(1e-6,"s");
	geo->PrintOverlaps();
	cout<<"========================       Done!       =============================\n\n\n"<<endl;
	TObjArray* overlaps_sampled=geo->GetListOfOverlaps();
	for(int i=0; i<overlaps_sampled->GetEntries(); i++){
	  TObject* overlap=overlaps_sampled->At(i);
	  cout<<"========================  Drawing Overlaps ============================="<<endl;
	  cout<<"================= Overlap messages will duplicate below ================"<<endl;
	  cout<<"=================     Overlaps are in units of cm       ================"<<endl;
	  TCanvas* c_sampled = new TCanvas("c_sampled","sampling method");
	  overlap->Draw("");
	  TCanvas* k = new TCanvas("k","sampling method" );
	  overlap->Draw("ogl");
	  cout<<"========================       Done!       =============================\n\n\n"<<endl;
	  
	  }*/

}
