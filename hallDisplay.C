void hallDisplay(TString filename, Int_t VisLevel=5, bool clip=true)
{
	TGeoManager *geo = TGeoManager::Import(filename);
	geo->DefaultColors();

	cout<<"======================== Checking Overlaps ============================="<<endl;
	geo->CheckOverlaps(1e-5,"d");
	geo->CheckGeometry();
 	geo->PrintOverlaps();
	geo->SetVisOption(1);
	geo->SetVisLevel(VisLevel);
	cout<<"========================       Done!       ============================="<<endl;

	// 521 is a rootino
	int pdg=14;
	int m1=0; int m2=0; int d1=0; int d2=0;
	double p=1.0;
	double beam_angle=0.101;
	double py=-p*sin(beam_angle);
	double pz= p*cos(beam_angle);
	double px=0;
	double vx=0;
	double vz=0; //Front of hall at -762 in global coordinate system
	/*
	double hall_start_z_in_hall_coordinates=-15.02e2;// ~15m
	double hall_length=-2*hall_start_z_in_hall_coordinates;
	double hall_back_global=-762 + hall_length;
	double beam_entering_height=592.2 - hall_start_z_in_hall_coordinates*tan(0.101);
	double global_y0_height=335;
	double vy=beam_entering_height-global_y0_height;
	cout<<"Beam enters the hall at a height of "<<beam_entering_height<<" cm"<<endl;
	cout<<"That is y= "<<vy<<" in the global coordinate system"<<endl;
	*/
	double hall_length=30e2;
	double vy=0;
	TParticle* beam_particle = new TParticle(521,1,m1,m2,d1,d2,px,py,pz,p, vx,vy,vz,0);
	Int_t track_index = geo->AddTrack(0,pdg,beam_particle);
	TVirtualGeoTrack* beam_track = geo->GetTrack(track_index);
	int npoints=100;
	double step=hall_length/(1.0*npoints);
	double linex[npoints];
	double liney[npoints];
	double linez[npoints];
	for (int ipoint=0; ipoint<npoints; ipoint++){
	  double dz=step*ipoint;
	  double dy=-dz*tan(beam_angle);
	  double z=vz+dz;
	  double y=vy+dy;
	  //cout<<"point "<<ipoint<<" : z= "<<z<<" y= "<<y<<endl;
	  beam_track->AddPoint(0,y,z,5e-9);
	  linex[ipoint]=0;
	  liney[ipoint]=y;
	  linez[ipoint]=z;
	}
	TPolyLine3D* beam_line= new TPolyLine3D(npoints,linex,liney,linez);

	// following line produces a lot of print out
	//	gGeoManager->GetListOfVolumes()->ls();

	// TGeoVolume* active =gGeoManager->GetVolume("volLArActive");

	// get argon cube active volume coordinates
	//	gGeoManager->cd("/volWorld_1/volDetEnclosure_0/volArgonCubeDetector_0/volLArCryo_0/volArgonCube_0/volArgonCubeActive_0");


	string detenc_vol="rockBox_lv_0/volDetEnclosure";
	//	string detenc_vol="/NDHallAirVol_lv_0";
	string top_vols="/volWorld_1/"; top_vols+=detenc_vol; top_vols+="_0";

	string lar_active_location=top_vols+"/volArgonCubeDetector_0/volArgonCubeCryostat_0/volReinforcedConcrete_0/volMoistureBarrier_0/volInsulationBoard2_0/volGREBoard2_0/volInsulationBoard1_0/volGREBoard1_0/volFireproofBoard_0/volSSMembrane_0/volArgonCubeService_0/volArgonCube_0/volArgonCubeActive_0";

	//	const char* lar_active_location="/volWorld_1/volDetEnclosure_0/volArgonCubeDetector_0/volArgonCubeCryostat_0/volReinforcedConcrete_0/volMoistureBarrier_0/volInsulationBoard2_0/volGREBoard2_0/volInsulationBoard1_0/volGREBoard1_0/volFireproofBoard_0/volSSMembrane_0/volArgonCubeService_0/volArgonCube_0/volArgonCubeActive_0";



	gGeoManager->cd(lar_active_location.c_str());
	TGeoMatrix *active = gGeoManager->GetCurrentMatrix();
	double local_active[3]={0,0,0};
	double master_active[3]={0,0,0};	  
	if(active){
	  active->LocalToMaster(local_active,master_active);
	cout<<"The center of ArgonCubeActive in the global coordinate system: \n"<<" ( "<<master_active[0]<<", "<<master_active[1]<<", "<<master_active[2]<<" )"<<endl;
	}

	// get detector enclosure coordinates
	gGeoManager->cd(top_vols.c_str());
	TGeoMatrix *enclosure = gGeoManager->GetCurrentMatrix();
	double local_enclosure[3]={0,0,0};
	double master_enclosure[3]={0,0,0};
	enclosure->LocalToMaster(local_enclosure,master_enclosure);
	cout<<"The center of DetEnclosure in the global coordinate system: \n"<<" ( "<<master_enclosure[0]<<", "<<master_enclosure[1]<<", "<<master_enclosure[2]<<" )"<<endl;

	// print location of LArTPC in the detector enclosure
	if(active){
	  double active_in_enclosure[3]={0,0,0};
	  enclosure->MasterToLocal(master_active,active_in_enclosure);

	  cout<<"The center of ArgonCubeActive in the DetEnclosure coordinate system: \n"<<" ( "<<active_in_enclosure[0]<<", "<<active_in_enclosure[1]<<", "<<active_in_enclosure[2]<<" )"<<endl;
	}
	// print out location of GArTPC
	string gar_vol=top_vols+"/volMPD_0/volNDHPgTPC_0/volGArTPC_0";
	gGeoManager->cd(gar_vol.c_str());
	TGeoMatrix *gartpc = gGeoManager->GetCurrentMatrix();
	if(gartpc){
	  double local_gartpc[3]={0,0,0};
	  double master_gartpc[3]={0,0,0};
	  gartpc->LocalToMaster(local_gartpc,master_gartpc);
	  cout<<"The center of GArTPC in the global coordinate system: \n"<<" ( "<<master_gartpc[0]<<", "<<master_gartpc[1]<<", "<<master_gartpc[2]<<" )"<<endl;
	  
	  double gartpc_in_enclosure[3]={0,0,0};
	  enclosure->MasterToLocal(master_gartpc,gartpc_in_enclosure);

	  cout<<"The center of GArTPC in the DetEnclosure coordinate system: \n"<<" ( "<<gartpc_in_enclosure[0]<<", "<<gartpc_in_enclosure[1]<<", "<<gartpc_in_enclosure[2]<<" )"<<endl;
	}

	geo->GetTopVolume()->Draw("ogl");
	//	geo->DrawTracks("ogl");
	beam_line->SetLineWidth(2);
	beam_line->SetLineColor(kRed);
	beam_line->SetLineStyle(kDashed);
	beam_line->Draw();
	cout<<detenc_vol<<endl;
	TGeoVolume* enc=geo->GetVolume("rockBox_lv");
	enc->SetVisibility(kTRUE);
	enc->VisibleDaughters(kTRUE);
	enc->Print();
	cout<<"volArgonCubeDetector"<<endl;
	TGeoVolume* ar3=geo->GetVolume("volArgonCubeDetector");
	if(ar3){
	  ar3->SetTransparency(50);
	  ar3->SetVisContainers(kTRUE);
	  ar3->VisibleDaughters(kTRUE);
	  ar3->Print();
	}	
	cout<<"volArgonCubeCryostat"<<endl;
	TGeoVolume* cryo=geo->GetVolume("volArgonCubeCryostat");
	if(cryo){
	  cryo->SetTransparency(50);
	  cryo->SetVisContainers(kTRUE);
	  cryo->VisibleDaughters(kTRUE);
	  cryo->Print();
	}
	cout<<"volLArActiveModWolXX"<<endl;
	for(int iwall=0; iwall<35; iwall++){
	  TGeoVolume* wall=geo->GetVolume(Form("volLArActiveModWall%02i",iwall));
	  if(wall) wall->SetTransparency(80);
	}
	TGeoVolume* cent_elec=geo->GetVolume("cent_elec_vol");
	if(cent_elec){
	  cent_elec->SetTransparency(90);
	}
	//	cout<<"cent_elec "<<cent_elec<<endl;


	// flux window
	/*
	// in hall flux window
	double xw1[5]={600, 600, -600, -600, 600 };
	double yw1[5]={-600, 570, 570, -600, -600};
	double zw1[5]={250, 250, 250, 250, 250};
	*/

	/*
	// near rock flux window
	double xw1[5]={1000, 1000, -1500, -1500, 1000 };
	double yw1[5]={-1160, 2200, 2200, -1160, -1160};
	double zw1[5]={-550, -550, -550, -550, -550};
	*/

	// MPD fiducial flux window
	double xw1[5]={350, 350, -350, -350, 350 };
	double yw1[5]={-355, 305, 305, -355, -355};
	double zw1[5]={250, 250, 250, 250, 250};

	
	TPolyLine3D* fw1= new TPolyLine3D(5,xw1,yw1,zw1);
	fw1->SetLineWidth(2);
	fw1->SetLineColor(kYellow);
	fw1->SetLineStyle(kDashed);
	fw1->Draw();

	double window_zstep=500;
	int n_ds_windows=8;
	for(int iwin=1; iwin<=n_ds_windows; iwin++){
	  double zadd=window_zstep*iwin;
	  double yadd=-zadd*sin(beam_angle);
	  double yw1_ds[5];
	  double zw1_ds[5];
	  for(int i=0; i<5; i++) {
	    yw1_ds[i]=yw1[i]+yadd;
	    zw1_ds[i]=zw1[i]+zadd;
	  }
	
	  TPolyLine3D* fw1_ds= new TPolyLine3D(5,xw1,yw1_ds,zw1_ds);
	  fw1_ds->SetLineWidth(2);
	  fw1_ds->SetLineColor(kGreen);
	  fw1_ds->SetLineStyle(kDashed);
	  fw1_ds->Draw();
	
	}

	
	TGLSAViewer *glsa = (TGLSAViewer *)gPad->GetViewer3D();
	// components - A,B,C,D - of plane eq : Ax+By+CZ+D = 0
	// kClipPlane=1
	if(clip){
	  TGLClipSet* clip =glsa->GetClipSet();
	  Double_t clip_config[6]={-1,0,0,-0.5,0,0};
	  //	clip->SetShowClip(kTRUE);
	  clip->SetAutoUpdate(kTRUE);
	  clip->SetClipState(TGLClip::EType::kClipPlane,clip_config);
	  clip->SetClipType(TGLClip::EType::kClipPlane);
	}
	glsa->DrawGuides();
	glsa->UpdateScene();

	//	TGCompositeFrame* frame = glsa->GetFrame();
}
