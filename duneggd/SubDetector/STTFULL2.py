#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q
import time

class STTFULLBuilder(gegede.builder.Builder):
    def configure( self, halfDimension=None, Material=None,  **kwds):

        self.sqrt3                    = 1.7320508
        self.start_time=time.time()
        print(("start_time:",self.start_time))
        self.halfDimension, self.Material = ( halfDimension, Material )

        self.strawRadius            = Q('2.5mm')
        self.strawWireWThickness    = Q('20um')
        self.strawWireGThickness    = Q('20nm')
        self.coatThickness          = Q("100nm")
        self.mylarThickness         = Q("12um")
        
        self.kloeVesselRadius       = Q('2m')
        self.kloeVesselHalfDx       = Q('1.69m')
        self.extRadialgap           = Q("0cm")
        self.extLateralgap          = Q("0cm")
        self.kloeTrkRegRadius       = self.kloeVesselRadius - self.extRadialgap
	self.kloeTrkRegHalfDx       = self.kloeVesselHalfDx - self.extLateralgap
        
        
        self.nfoil                  = 150
        self.foilThickness          = Q("15um")
        self.foilGap                = Q("120um")
        self.totfoilThickness       = self.nfoil * self.foilThickness + (self.nfoil-1)*self.foilGap
        self.fiveFoilThickness      = self.foilThickness*5+ self.foilGap*4
        
        self.slabThickness          = Q("5.3mm")
        self.graphiteThickness      = Q("4mm")


        self.planeXXThickness = self.strawRadius * (2 + self.sqrt3)
        self.C3H6ModThickness= self.planeXXThickness * 2 + self.totfoilThickness + self.slabThickness
        self.frontStrawThickness= self.planeXXThickness*4
        self.cModThickness= self.planeXXThickness * 2 + self.graphiteThickness
        self.noSlabModThickness=self.planeXXThickness * 2 + self.totfoilThickness


        #  liqAR STXXYY STXXYY ||||| 3+ 1+ 12 + 1 + 12 + 1 + 12 + 1 + 12+ 1 + 12+ 1 + 12 + 1 + 3  |||| 5 no_slab modules
                
        self.totModsThickness = 5 * self.noSlabModThickness + 78 * self.C3H6ModThickness + 7 * self.cModThickness + self.frontStrawThickness
        self.fvModsThickness= 78 * self.C3H6ModThickness + 7 * self.cModThickness
        self.nModule= 5 + 78 + 7


        self.liqArThickness=Q("20cm") - self.frontStrawThickness
        self.endgap= self.kloeTrkRegRadius*2 - self.liqArThickness - self.totModsThickness

        
        print(("endgap:",self.endgap))
        print(("totfoilThickness:",self.totfoilThickness))
        print(("self.slabThickness:",self.slabThickness))
        print(("planeXXThickness:",self.planeXXThickness))
        print(("C3H6ModThickness:",self.C3H6ModThickness))
        print(("cModThickness:",self.cModThickness))
        print(("noSlabModThickness:",self.noSlabModThickness))
        print(("fvModsThickness:",self.fvModsThickness))
        print(("totModsThickness:",self.totModsThickness))
        print(("liqArThickness:",self.liqArThickness))
        
    def construct(self,geom):

        mod_types=["C3H6Mod","C3H6Mod","C3H6Mod"]
        for i in range(6):
            for j in range(13):
                if j==0:
                    mod_types.append("CMod")
                else:
                    mod_types.append("C3H6Mod")
        mod_types.append("CMod")
        mod_types.append("C3H6Mod")
        mod_types.append("C3H6Mod")
        mod_types.append("C3H6Mod")
        mod_types.append("NoSlabMod")
        mod_types.append("NoSlabMod")
        mod_types.append("NoSlabMod")
        mod_types.append("NoSlabMod")
        mod_types.append("NoSlabMod")
        print(mod_types)
        modthicknesses={"NoSlabMod": self.noSlabModThickness, "CMod":self.cModThickness, "C3H6Mod":self.C3H6ModThickness}


        ############################## the main tube    #######################################
        main_lv, main_hDim = ltools.main_lv( self, geom, "Tubs")
        print( "KLOESTTFULL::construct()")
        print(( "  main_lv = "+ main_lv.name))
        self.add_volume( main_lv )

        ########################################  liq Argon #################################
        self.construct_LAr_target(main_lv,geom)
        #####################################################################################
        

        pos_Slab_in_C3H6Mod=geom.structure.Position("pos_Slab_in_C3H6Mod", -self.C3H6ModThickness/2.0 +self.slabThickness/2.0, "0cm","0cm")
        pos_foilchunk_in_C3H6Mod=geom.structure.Position("pos_foilchunk_in_C3H6Mod",-self.C3H6ModThickness/2.0+self.slabThickness+self.totfoilThickness/2.0,"0cm","0cm")
        pos_ST_in_C3H6Mod=geom.structure.Position("pos_ST_in_C3H6Mod", self.C3H6ModThickness/2.0 - self.planeXXThickness, "0cm","0cm")
        pos_Graphite_in_Cmod=geom.structure.Position("pos_Graphite_in_Cmod", -self.cModThickness/2.0+self.graphiteThickness/2.0, "0cm","0cm")
        pos_ST_in_Cmod=geom.structure.Position("pos_ST_in_Cmod",self.cModThickness/2.0 - self.planeXXThickness, "0cm","0cm")
        pos_foilchunk_in_NoSlabMod=geom.structure.Position("pos_foilchunk_in_NoSlabMod", -self.noSlabModThickness/2.0 + self.totfoilThickness/2.0, "0cm","0cm")
        pos_ST_in_NoSlabMod=geom.structure.Position("pos_ST_in_NoSlabMod", self.noSlabModThickness/2.0 - self.planeXXThickness, "0cm","0cm")
        pos_hh_in_ST=geom.structure.Position("pos_hh_in_ST", -self.planeXXThickness/2.0, "0cm","0cm")
        pos_vv_in_ST=geom.structure.Position("pos_vv_in_ST", self.planeXXThickness/2.0 , "0cm","0cm")
        pos_straw2relative= geom.structure.Position("pos_straw2relative", self.strawRadius*self.sqrt3, self.strawRadius, Q('0m'))

        self.fiveFoilPositions=[]
        self.foilPositionsInFive=[]
        for i in range(self.nfoil/5):
            self.fiveFoilPositions.append(geom.structure.Position("pos_fiveFoilPositions_"+str(i),  -self.totfoilThickness/2.0 + self.fiveFoilThickness/2.0 + i*(self.fiveFoilThickness+self.foilGap) , Q('0m'), Q('0m')))

        for i in range(5):
            self.foilPositionsInFive.append(geom.structure.Position("pos_foilInFive_"+str(i), (self.foilThickness+self.foilGap)*(i-2), Q('0m'), Q('0m')))
            
        
        self.horizontalST_Xe=self.construct_strawtube(geom,"horizontalST_Xe" , self.kloeTrkRegHalfDx, "C3H6Mod")
        self.horizontalST_Ar=self.construct_strawtube(geom,"horizontalST_Ar" , self.kloeTrkRegHalfDx, "CMod")
        

        ########################################  Front ST  #################################
        usedLength=self.liqArThickness
        ratio= (self.kloeTrkRegRadius - usedLength)/self.kloeTrkRegRadius
        height=self.kloeTrkRegRadius*math.sqrt(1 - ratio*ratio)
        module_lv = self.construct_strawplane(geom, "frontST" , height, "gra")  # every time there is no raditor (with foils) we use Ar instead
        pos_frontST1=geom.structure.Position("pos_frontST1", -self.kloeTrkRegRadius+usedLength + self.planeXXThickness, "0cm","0cm")
        pos_frontST2=geom.structure.Position("pos_frontST2", -self.kloeTrkRegRadius+usedLength + 3*self.planeXXThickness,	"0cm","0cm")
        frontST_pla1=geom.structure.Placement("pla_frontST1",volume=module_lv,pos=pos_frontST1, copynumber=0)
        frontST_pla2=geom.structure.Placement("pla_frontST2",volume=module_lv,pos=pos_frontST2, copynumber=1)
        main_lv.placements.append(frontST_pla1.name)
        main_lv.placements.append(frontST_pla2.name)                
        usedLength+=self.frontStrawThickness
        #####################################################################################
        
        nModule=1
        for imod in range(nModule):
            print(("### imod ### ",imod))
            print(("### type ### ",mod_types[imod]))
            ModThickness= modthicknesses[mod_types[imod]]
            loc=[usedLength - self.kloeTrkRegRadius + 0.5 * ModThickness,Q("0cm"),Q("0cm")]
            if (usedLength+0.5 * ModThickness) < self.kloeTrkRegRadius:
                    ratio= (self.kloeTrkRegRadius - usedLength  )/self.kloeTrkRegRadius
            else:
                    ratio= ( usedLength-self.kloeTrkRegRadius + ModThickness)/self.kloeTrkRegRadius
            height=self.kloeTrkRegRadius*math.sqrt(1 - ratio*ratio)
            halfDimension = {'dx': ModThickness/2.0, 'dy':height, 'dz': self.kloeTrkRegHalfDx}
            name="STT_"+mod_types[imod]+"_"+str(imod)
            if mod_types[imod]=="NoSlabMod":               
                module_lv = self.construct_noSlabModule(geom, name,  self.Material, halfDimension)
            elif mod_types[imod]=="CMod":
                module_lv = self.construct_cModule(geom, name,  self.Material, halfDimension)
            else:
                module_lv = self.construct_C3H6Module(geom, name,  self.Material, halfDimension)
            module_pos=geom.structure.Position("pos_"+name,loc[0],loc[1],loc[2])
            module_pla=geom.structure.Placement("pla_"+name,volume=module_lv,pos=module_pos, copynumber=imod)
            main_lv.placements.append(module_pla.name)
            usedLength += ModThickness
#            print("%2d %8s %10.3f %10.3f"%(imod,mod_types[imod],(usedLength-ModThickness).magnitude,usedLength.magnitude))
        end_time=time.time()
        print(("time diff:",end_time-self.start_time))


    def construct_LAr_target(self,main_lv,geom):
        
        liqArBox_shape = geom.shapes.Box("shape_liqArBox", dx= self.liqArThickness/2 , dy=self.kloeTrkRegRadius, dz= self.kloeTrkRegHalfDx )
        mainShape = geom.shapes.Tubs("shape_tube", rmin=Q("0m"), rmax=self.kloeTrkRegRadius, dz= self.kloeTrkRegHalfDx)
        ArBox_pos = geom.structure.Position("pos_ArTube2Box", -self.kloeTrkRegRadius+self.liqArThickness/2, Q('0m'), Q('0m'))
        liqAr_shape  = geom.shapes.Boolean("liqAr_shape", type='intersection',
                                           first=mainShape,
                                           second=liqArBox_shape,
                                           rot='noRotate',
                                           pos=ArBox_pos )
        liqAr_lv=geom.structure.Volume('liqAr',material="LAr", shape=liqAr_shape)
        liqAr_pla=geom.structure.Placement("pla_liqAr",volume=liqAr_lv)
        main_lv.placements.append(liqAr_pla.name)
        
    def construct_noSlabModule(self,geom, name, Material, halfDimension):
        
        main_shape = geom.shapes.Box("shape_"+name, dx=halfDimension['dx'], dy=halfDimension['dy'], dz=halfDimension['dz'] )
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )

        namef=name+"_foil"
        foil_lv= self.construct_foils(geom, namef, halfDimension['dy'])
        foil_pla=geom.structure.Placement("pla_"+namef, volume=foil_lv, pos="pos_foilchunk_in_NoSlabMod")
        main_lv.placements.append(foil_pla.name)

        names=name+"_ST"
        strawplane_lv=self.construct_strawplane(geom,names, construct_strawplane, "NoSlabMod")
        strawplane_pla=geom.structure.Placement("pla_"+names, volume=strawplane_lv, pos="pos_ST_in_NoSlabMod")
        main_lv.placements.append(strawplane_pla.name)
        return main_lv
    
    def construct_C3H6Module(self,geom, name, Material, halfDimension):

        main_shape = geom.shapes.Box("shape_"+name, dx=halfDimension['dx'], dy=halfDimension['dy'], dz=halfDimension['dz'] )
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )
 #       return main_lv
        nameslab=name+"_slab"
        slab_shape = geom.shapes.Box( "shape_"+nameslab, dx=self.slabThickness/2.0, dy=halfDimension['dy'], dz=halfDimension['dz'] )
        slab_lv = geom.structure.Volume(nameslab, material="C3H6", shape=slab_shape )
        slab_pla=geom.structure.Placement("pla_"+nameslab, volume=slab_lv, pos="pos_Slab_in_C3H6Mod")
        main_lv.placements.append(slab_pla.name)
        
        namef=name+"_foil"
        foil_lv= self.construct_foils(geom, namef, halfDimension['dy'])
        foil_pla=geom.structure.Placement("pla_"+namef, volume=foil_lv, pos="pos_foilchunk_in_C3H6Mod")
        main_lv.placements.append(foil_pla.name)
            
        names=name+"_ST"
        strawplane_lv=self.construct_strawplane(geom, names, halfDimension['dy'],"C3H6Mod")
        strawplane_pla=geom.structure.Placement("pla_"+names, volume=strawplane_lv, pos="pos_ST_in_C3H6Mod")
        main_lv.placements.append(strawplane_pla.name)
        
        return main_lv

    def construct_cModule(self,geom, name, Material, halfDimension):

        main_shape = geom.shapes.Box("shape_"+name, dx=halfDimension['dx'], dy=halfDimension['dy'], dz=halfDimension['dz'] )
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )        
        
        graphite_shape = geom.shapes.Box("shape_"+name+"_graph", dx=self.graphiteThickness/2.0, dy=halfDimension['dy'], dz=halfDimension['dz'] )
        graphite_lv = geom.structure.Volume(name+"_graph", material="Graphite", shape=graphite_shape )
        graphite_pla=geom.structure.Placement("pla_"+name+"_graph", volume=graphite_lv, pos="pos_Graphite_in_Cmod")
        main_lv.placements.append(graphite_pla.name)

        strawplane_lv=self.construct_strawplane(geom,name+"_ST", halfDimension['dy'], "CMod")
        strawplane_pla=geom.structure.Placement("pla_"+name+"_ST", volume=strawplane_lv, pos="pos_ST_in_Cmod")
        main_lv.placements.append(strawplane_pla.name)
        return main_lv

    def construct_foils(self,geom, name, halfheight):
        main_shape = geom.shapes.Box(name, dx=self.totfoilThickness/2.0, dy=halfheight, dz= self.kloeTrkRegHalfDx )
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )

        fiveFoil_shape=geom.shapes.Box("shape_"+name+"_f5", dx=self.fiveFoilThickness/2.0, dy=halfheight, dz= self.kloeTrkRegHalfDx )
        fiveFoil_lv=geom.structure.Volume(name+"_f5", material="Air35C", shape=fiveFoil_shape )
        foil_shape = geom.shapes.Box("shape_"+name+"_1f", dx=self.foilThickness/2.0, dy=halfheight, dz= self.kloeTrkRegHalfDx )
        foil_lv = geom.structure.Volume(name+"_1f", material="C3H6", shape=foil_shape )        
        for i in range(5):                        
            foil_pla=geom.structure.Placement("pla_"+name+"_"+str(i)+"inf5", volume=foil_lv, pos=self.foilPositionsInFive[i])
            fiveFoil_lv.placements.append(foil_pla.name)        
            
        for i in range(self.nfoil/5):
            #            pos = [ -self.totfoilThickness/2.0 +self.foilThickness/2.0 + i*(self.foilThickness+self.foilGap) , Q('0m'), Q('0m')]
            #            foil_pos=geom.structure.Position("pos"+namef+str(i), pos[0],pos[1], pos[2])
            foil_pla=geom.structure.Placement("pla"+name+"_grp_"+str(i), volume=fiveFoil_lv, pos=self.fiveFoilPositions[i])
            main_lv.placements.append(foil_pla.name)
            
        return main_lv
        
    def construct_strawplane(self,geom,name, halfheight, modtype):
        main_shape = geom.shapes.Box("shape_"+name, dx=self.planeXXThickness, dy=halfheight, dz=self.kloeTrkRegHalfDx)
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )

        hh_lv=self.construct_XXST(geom, "hh", name+"_hh", self.kloeTrkRegHalfDx, halfheight, modtype)
        vv_lv=self.construct_XXST(geom, "vv", name+"_vv", halfheight, self.kloeTrkRegHalfDx, modtype)
        hh_pla=geom.structure.Placement("pla_"+name+"_hh", volume=hh_lv, pos="pos_hh_in_ST")
        vv_pla=geom.structure.Placement("pla_"+name+"_vv", volume=vv_lv,   pos="pos_vv_in_ST",rot= "r90aboutX")
        main_lv.placements.append(hh_pla.name)
        main_lv.placements.append(vv_pla.name)

        return main_lv

    def construct_XXST(self,geom, tubeDirection, name, halflength, halfCrosslength, modtype):

        main_shape = geom.shapes.Box("shape_"+name, dx=self.planeXXThickness/2.0, dy=halfCrosslength , dz=halflength)
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )
        if tubeDirection=="hh":
            if modtype=="CMod":
                straw_lv=self.horizontalST_Ar
            else:
                straw_lv=self.horizontalST_Xe
        else:
            straw_lv=self.construct_strawtube(geom, name+"_ST",halflength, modtype)
        
        
        Nstraw=int((2*halfCrosslength-self.strawRadius)/self.strawRadius/2.0)

        straw_shape = geom.shapes.Tubs("shape_"+name+"_1st", rmin=Q("0m"), rmax=self.strawRadius, dz=halflength)
        twoStraw_shape  = geom.shapes.Boolean("shape_"+name+"_2straw", type='union',
                                              first=straw_shape,
                                              second=straw_shape,
                                              rot='noRotate',
                                              pos="pos_straw2relative")
        
        twoStraw_lv=geom.structure.Volume(name+"_2straw",material="Air35C", shape=twoStraw_shape)
        straw1_pla=geom.structure.Placement("pla_"+name+"_s1",volume=straw_lv)
        twoStraw_lv.placements.append(straw1_pla.name)
        straw2_pla=geom.structure.Placement("pla_"+name+"_s2",volume=straw_lv, pos="pos_straw2relative")
        twoStraw_lv.placements.append(straw2_pla.name)

        
        print(("Nstraw",Nstraw))

        for i in range(Nstraw):
            pos1=geom.structure.Position("pos_"+name+"_"+str(i), -self.planeXXThickness/2.0+self.strawRadius, halfCrosslength - (2*i+2)*self.strawRadius, Q('0m'))
            twoStraw_pla1=geom.structure.Placement("pla_"+name+"_"+str(i), volume=twoStraw_lv, pos=pos1)
            main_lv.placements.append(twoStraw_pla1.name)
        return main_lv
#            pos1=[-self.planeXXThickness/2.0+self.strawRadius, halfCrosslength - (2*i+1)*self.strawRadius, Q('0m')]
#            straw_pos1=geom.structure.Position("pos_"+name+"_"+str(i), pos1[0],pos1[1], pos1[2])
#            straw_pla1=geom.structure.Placement("pla_"+name+"_"+str(i), volume=straw_lv, pos=straw_pos1, copynumber=i)
#            main_lv.placements.append(straw_pla1.name)

#            pos2=[self.planeXXThickness/2.0 - self.strawRadius,  halfCrosslength -(2*i+2)*self.strawRadius, Q('0m')]
#            straw_pos2=geom.structure.Position("pos_"+name+"_"+str(i+Nstraw), pos2[0],pos2[1], pos2[2])
#            straw_pla2=geom.structure.Placement("pla_"+name+"_"+str(i+Nstraw), volume=straw_lv, pos=straw_pos2, copynumber=i+1000)
#            main_lv.placements.append(straw_pla2.name)        

        
        
    def construct_strawtube(self,geom, name, halflength, modtype):

        if modtype=="CMod":
            airMaterial="stGas_Ar19"
        else:
            airMaterial="stGas_Xe19"
            
        main_shape = geom.shapes.Tubs("shape_"+name, rmin=Q("0m"), rmax=self.strawRadius, dz=halflength)
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )

        coat_shape=geom.shapes.Tubs("shape_"+name+"_coat", rmin = self.strawRadius- self.coatThickness , rmax = self.strawRadius, dz = halflength)
        coat_lv   = geom.structure.Volume(name+"_coat", material="Aluminum", shape=coat_shape)
        
        mylar_shape = geom.shapes.Tubs("shape_"+name+"_mylar", rmin = self.strawRadius- self.coatThickness - self.mylarThickness , rmax = self.strawRadius- self.coatThickness, dz = halflength)
        mylar_lv   = geom.structure.Volume(name+"_mylar", material="Mylar", shape=mylar_shape)

        
        air_shape=geom.shapes.Tubs("shape_"+name+"_air", rmin = self.strawWireWThickness+self.strawWireGThickness,
                                   rmax = self.strawRadius- self.coatThickness - self.mylarThickness, dz = halflength)
        air_lv   = geom.structure.Volume(name+"_air", material=airMaterial, shape=air_shape)
        air_lv.params.append(("SensDet","Straw"))

        wireW_shape = geom.shapes.Tubs("shape_"+name+"_wireW", rmin=Q("0um"), rmax = self.strawWireWThickness, dz = halflength)
        wireW_lv    = geom.structure.Volume(name+"_wireW", material="Tungsten", shape=wireW_shape)

        wireG_shape = geom.shapes.Tubs("shape_"+name+"_wireG", rmin= self.strawWireWThickness, rmax = self.strawWireWThickness+self.strawWireGThickness, dz = halflength)
        wireG_lv    = geom.structure.Volume(name+"_wireG", material="Gold", shape=wireG_shape)
        
        coat_pla = geom.structure.Placement( "pla_"+name+"_coat", volume = coat_lv )
        mylar_pla = geom.structure.Placement( "pla_"+name+"_mylar", volume = mylar_lv )
        air_pla = geom.structure.Placement( "pla_"+name+"_air", volume = air_lv )
        wireW_pla = geom.structure.Placement( "pla_"+name+"_wireW", volume = wireW_lv )
        wireG_pla = geom.structure.Placement( "pla_"+name+"_wireG", volume = wireG_lv )
        
        main_lv.placements.append( coat_pla.name )
        main_lv.placements.append( mylar_pla.name )
        main_lv.placements.append( air_pla.name )
        main_lv.placements.append( wireW_pla.name )
        main_lv.placements.append( wireG_pla.name )
        
        return main_lv
