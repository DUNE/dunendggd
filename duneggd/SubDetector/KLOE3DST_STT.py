#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q
import time

# liqAr + 9blocks +....
# 1 block = 9 regular module + 1 carbon module
# 1 regular module = xxyy + foils + slab
#class KLOESTTFULLNEWCONFNEWGAPBuilder(gegede.builder.Builder):
class KLOE3DST_STT_builder(gegede.builder.Builder):
    def configure( self, halfDimension=None, Material=None, useRegMod=None,
                   Box3DSTDim=None, pureSTModGap=None, offset3DSTcenter=None,
                   nFrontMod=None, nTBMod=None, nLRMod=None,nRear1Mod=None, nRear2Mod_reg=None, nRear2Mod_nos=None, nRear3Mod=None,
                   strawRadius=None, strawTubeThickness=None, strawWireWThickness=None,strawWireGThickness=None,
                   radiatorThickness=None, kloeVesselRadius=None, kloeVesselHalfDx=None,
                   extRadialgap=None, extLateralgap=None, DwGapNoRad=None,
                   nfoil=None,foilThickness=None,foilGap=None,slabThickness=None, graphiteThickness=None,
                   foilChunkThickness=None, coatThickness=None, mylarThickness=None,
                   **kwds):        
        self.start_time=time.time()
        print(("start_time:",self.start_time))
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.useRegMod=useRegMod
        self.Height3DST=Box3DSTDim[1]
        self.Depth3DST=Box3DSTDim[2]
        self.Width3DST=Box3DSTDim[0]
        self.pureSTModGap=pureSTModGap
        self.nFrontMod=nFrontMod
        self.nTBMod= nTBMod
        self.nLRMod= nLRMod
        
        self.nRear1Mod=nRear1Mod

        self.nRear2Mod=nRear2Mod_reg
        if useRegMod!=True:
            print("NOTE-------------------- use nos mod instead of reg")
            self.nRear2Mod=nRear2Mod_nos
        print(("self.nRear2Mod:",self.nRear2Mod))
        self.nRear3Mod=nRear3Mod
        self.offset3DSTcenter=offset3DSTcenter
        self.strawRadius=strawRadius
        self.strawTubeThickness=strawTubeThickness
        self.strawWireWThickness=strawWireWThickness
        self.strawWireGThickness=strawWireGThickness
        self.radiatorThickness=radiatorThickness
        self.DwGapNoRad=DwGapNoRad
        self.kloeVesselRadius=kloeVesselRadius
        self.kloeVesselHalfDx=kloeVesselHalfDx
        self.extRadialgap=extRadialgap
        self.extLateralgap=extLateralgap
        self.nfoil=nfoil
        self.foilThickness=foilThickness
        self.foilGap=foilGap
        self.slabThickness=slabThickness
        self.graphiteThickness=graphiteThickness

#        self.foilChunkThickness=foilChunkThickness
        self.coatThickness=coatThickness
        self.mylarThickness=mylarThickness
        self.Nstraw_list=[]
    def construct(self,geom):
        #  liqAR STXXYY STXXYY ||||| 3+ 1+ 12 + 1 + 12 + 1 + 12 + 1 + 12+ 1 + 12+ 1 + 12 + 1 + 3  |||| 5 no_slab modules
        sqrt3             = 1.7320508
        kloeTrkRegRadius  = self.kloeVesselRadius - self.extRadialgap
        kloeTrkRegHalfDx  = self.kloeVesselHalfDx - self.extLateralgap
        planeXXThickness = self.strawRadius * (2 + sqrt3)
        totfoilThickness = self.nfoil * self.foilThickness + (self.nfoil-1)*self.foilGap
        regModThickness=planeXXThickness * 2 + totfoilThickness + self.slabThickness

        cModThickness=planeXXThickness * 2 + self.graphiteThickness
        noSlabModThickness=planeXXThickness * 2 + totfoilThickness

        self.planeXXThickness=planeXXThickness
        self.totfoilThickness=totfoilThickness
        self.kloeTrkRegHalfDx=kloeTrkRegHalfDx
        self.kloeTrkRegRadius=kloeTrkRegRadius
        self.pureSTModThickness=planeXXThickness*4
        self.SingleSTModThickness=planeXXThickness*2
        self.regModThickness=regModThickness
        self.noSlabModThickness=noSlabModThickness
        
        test_nfront= (kloeTrkRegRadius- self.Depth3DST/2 - self.offset3DSTcenter)/(self.pureSTModThickness+self.pureSTModGap)
        test_nMid= self.Depth3DST/(self.pureSTModThickness+self.pureSTModGap)
        test_nRear2 = kloeTrkRegRadius - self.Depth3DST/2 + self.offset3DSTcenter - (self.pureSTModThickness+self.pureSTModGap)*self.nRear1Mod - self.noSlabModThickness*self.nRear3Mod
        test_nRear2A=test_nRear2/self.regModThickness
        test_nRear2B=test_nRear2/self.noSlabModThickness
        print(("test_nfront:",test_nfront))
        print(("test_nMid:",test_nMid))
        print(("test_nRear2A:",test_nRear2A))
        print(("test_nRear2B:",test_nRear2B))
        
        self.frontGap=kloeTrkRegRadius- (self.pureSTModThickness+self.pureSTModGap)*self.nFrontMod - self.Depth3DST/2 - self.offset3DSTcenter
        print(("front gap:",self.frontGap))

        rearModsWidth=(self.pureSTModThickness+self.pureSTModGap)*self.nRear1Mod + self.regModThickness*self.nRear2Mod + self.noSlabModThickness*self.nRear3Mod
        self.rearGap= kloeTrkRegRadius - self.Depth3DST/2 + self.offset3DSTcenter - rearModsWidth
        print(("rearModsWidth:",rearModsWidth))
        print(("self.rearGap:",self.rearGap))
    
        print(("totfoilThickness:",totfoilThickness))
        print(("self.slabThickness:",self.slabThickness))
        print(("planeXXThickness:",planeXXThickness))
        print(("regModThickness:",regModThickness))
        print(("cModThickness:",cModThickness))
        print(("noSlabModThickness:",noSlabModThickness))

        main_lv, main_hDim = ltools.main_lv( self, geom, "Tubs")
        self.add_volume( main_lv )

#        testShape = geom.shapes.Tubs("testShape", rmin=Q("2m"), rmax = Q("2.05m"), dz = self.kloeTrkRegHalfDx)
#        testlv    = geom.structure.Volume("testlv", material="Tungsten", shape=testShape)
#        testpla = geom.structure.Placement("pla_test", volume=testlv)
#        main_lv.placements.append(testpla.name)

        pos_Slab_in_RegMod=geom.structure.Position("pos_Slab_in_RegMod", -regModThickness/2.0 +self.slabThickness/2.0, "0cm","0cm")
        pos_foilchunk_in_RegMod=geom.structure.Position("pos_foilchunk_in_RegMod",-regModThickness/2.0+self.slabThickness+self.totfoilThickness/2.0,"0cm","0cm")
        pos_ST_in_RegMod=geom.structure.Position("pos_ST_in_RegMod", regModThickness/2.0 - planeXXThickness, "0cm","0cm")
        pos_Graphite_in_Cmod=geom.structure.Position("pos_Graphite_in_Cmod", -cModThickness/2.0+self.graphiteThickness/2.0, "0cm","0cm")
        pos_ST_in_Cmod=geom.structure.Position("pos_ST_in_Cmod",cModThickness/2.0 - planeXXThickness, "0cm","0cm")
        pos_foilchunk_in_NoSlabMod=geom.structure.Position("pos_foilchunk_in_NoSlabMod", -noSlabModThickness/2.0 + self.totfoilThickness/2.0, "0cm","0cm")
        pos_ST_in_NoSlabMod=geom.structure.Position("pos_ST_in_NoSlabMod", noSlabModThickness/2.0 - planeXXThickness, "0cm","0cm")
        pos_hh_in_ST=geom.structure.Position("pos_hh_in_ST", -self.planeXXThickness/2.0, "0cm","0cm")
        pos_vv_in_ST=geom.structure.Position("pos_vv_in_ST", self.planeXXThickness/2.0 , "0cm","0cm")
        pos_hh1_in_doubleST=geom.structure.Position("pos_hh1_in_doubleST", -self.planeXXThickness/2.0*3, "0cm","0cm")
        pos_vv1_in_doubleST=geom.structure.Position("pos_vv1_in_doubleST", -self.planeXXThickness/2.0 , "0cm","0cm")
        pos_hh2_in_doubleST=geom.structure.Position("pos_hh2_in_doubleST", self.planeXXThickness/2.0, "0cm","0cm")
        pos_vv2_in_doubleST=geom.structure.Position("pos_vv2_in_doubleST", self.planeXXThickness/2.0*3 , "0cm","0cm")
        pos_oneSrawDown=geom.structure.Position("pos_oneSrawDown", "0cm", -self.strawRadius*2, "0cm")

        self.foilpositions=[]
        for i in range(self.nfoil):
            self.foilpositions.append(geom.structure.Position("pos_foilpositions_"+str(i),  -self.totfoilThickness/2.0 +self.foilThickness/2.0 + i*(self.foilThickness+self.foilGap) , Q('0m'), Q('0m')))
            
        
        self.horizontalST_Xe=self.construct_strawtube(geom,"horizontalST_Xe" , kloeTrkRegHalfDx, "reg")
        self.horizontalST_Ar=self.construct_strawtube(geom,"horizontalST_Ar" , kloeTrkRegHalfDx, "gra")

        ############################ build front STT
        self.build_frontSTT(geom, main_lv)

        ############################ build top & bottom & side  STT
        self.build_TopBotSTT(geom,main_lv)
        self.build_sideSTT(geom, main_lv)
        
        ############################ build rear STT
        self.build_rearSTT(geom, main_lv)
        
        ########################### build 3DST
        self.build_3DST(geom,main_lv)
        
    def build_3DST(self,geom, main_lv):
        if self.get_builder("3DST")==None:
            print("3DST  not found")
            return
        threeDST_builder=self.get_builder("3DST")
        threeDST_lv=threeDST_builder.get_volume()
        threeDST_pos=geom.structure.Position("pos_3DST_inKLOE", -self.offset3DSTcenter, "0cm","0cm")
        threeDST_pla=geom.structure.Placement("pla_3DST",
                                         volume=threeDST_lv, pos=threeDST_pos)
        main_lv.placements.append(threeDST_pla.name)


    def build_frontSTT(self, geom, main_lv):
        # first start 25cm 
        UpstreamEmpty=Q("25cm")
        c2seg= self.kloeTrkRegRadius - UpstreamEmpty
        costh=c2seg/self.kloeTrkRegRadius
        height=self.kloeTrkRegRadius*math.sqrt(1-costh*costh)
        name="front1ST"
        mod_lv=self.construct_doubleST(geom, name , height,"reg")
        x= -self.kloeTrkRegRadius + UpstreamEmpty + (self.pureSTModThickness+self.pureSTModGap)/2.
        mod_pos=geom.structure.Position("pos_"+name, x, Q("0cm"), Q("0cm"))
        mod_pla=geom.structure.Placement("pla_"+name,volume=mod_lv, pos=mod_pos)
        main_lv.placements.append(mod_pla.name)
        
        c2seg= self.offset3DSTcenter+self.Depth3DST/2+(self.pureSTModThickness+self.pureSTModGap)
        costh=c2seg/self.kloeTrkRegRadius
        height=self.kloeTrkRegRadius*math.sqrt(1-costh*costh)
        name2="front2ST"
        mod_lv2=self.construct_doubleST(geom, name2 , height,"reg")
        x2= -self.offset3DSTcenter-self.Depth3DST/2 - (self.pureSTModThickness+self.pureSTModGap)/2.
        mod_pos2=geom.structure.Position("pos_"+name2, x2, Q("0cm"), Q("0cm"))
        mod_pla2=geom.structure.Placement("pla_"+name2,volume=mod_lv2, pos=mod_pos2)
        main_lv.placements.append(mod_pla2.name)
        
    def build_TopBotSTT(self, geom,main_lv):
        self.SingleSTModGap=Q("16mm")
        self.nTBMod=20
        Lmax=self.Depth3DST/2+self.offset3DSTcenter
        Rmax=self.Depth3DST/2-self.offset3DSTcenter
        for imod in range(self.nTBMod):
            c2seg=self.Height3DST/2 + (imod+1)*(self.SingleSTModThickness + self.SingleSTModGap )
            costh=c2seg/self.kloeTrkRegRadius
            height=self.kloeTrkRegRadius*math.sqrt(1-costh*costh)
            Lheight=height
            Rheight=height
            if height>Lmax:
                Lheight=Lmax
            if height>Rmax:
                Rheight=Rmax
            aveHalfHeight=(Lheight+Rheight)/2
            name="side_"+str(imod)
            mod_lv=self.construct_strawplane(geom,name, aveHalfHeight , "reg")
            yTop = c2seg - (self.SingleSTModThickness + self.SingleSTModGap )/2
            x= (Rheight-Lheight)/2.
            mod_posTop=geom.structure.Position("posTop_"+name, x, yTop, Q("0cm"))
            mod_posBot=geom.structure.Position("posBot_"+name, x, -yTop, Q("0cm"))
            mod_plaTop=geom.structure.Placement("plaTop_"+name,volume=mod_lv, pos=mod_posTop, rot= "r90aboutZ")
            mod_plaBot=geom.structure.Placement("plaBot_"+name,volume=mod_lv, pos=mod_posBot, rot= "r90aboutZ")
            main_lv.placements.append(mod_plaTop.name)
            main_lv.placements.append(mod_plaBot.name)
            

    def build_sideSTT(self, geom, main_lv):
        self.SingleSTModGap=Q("8mm");
        self.nLRMod=18
        height=self.Height3DST/2
        alongColumnLength= self.Depth3DST/2
        mod_lv=self.construct_strawplane(geom,"sideSingleST_LR", height, "reg", alongColumnLength)
        x= -self.offset3DSTcenter
        for imod in range(self.nLRMod):
            name="side_"+str(imod)
            z= self.Width3DST/2 + (imod+1/2.)*(self.SingleSTModThickness + self.SingleSTModGap)
            mod_posL=geom.structure.Position("posL_"+name, x, Q("0cm"), z)
            mod_posR=geom.structure.Position("posR_"+name, x, Q("0cm"), -z)
            mod_plaL=geom.structure.Placement("plaL_"+name,volume=mod_lv, pos=mod_posL, rot="r90aboutY")
            mod_plaR=geom.structure.Placement("plaR_"+name,volume=mod_lv, pos=mod_posR, rot="r90aboutY")
            main_lv.placements.append(mod_plaL.name)
            main_lv.placements.append(mod_plaR.name)
            
    def build_rearSTT(self, geom, main_lv):
        
        for imod in range(self.nRear1Mod):
            c2seg=self.Depth3DST/2 -self.offset3DSTcenter+ (imod+1)*(self.pureSTModThickness+self.pureSTModGap)
            costh=c2seg/self.kloeTrkRegRadius
            height=self.kloeTrkRegRadius*math.sqrt(1-costh*costh)
            name1="Rear_purST_"+str(imod)
            mod_lv=self.construct_doubleST(geom, name1 , height,"reg")
            x= c2seg - (self.pureSTModThickness+self.pureSTModGap)/2.
            mod_pos=geom.structure.Position("pos_"+name1, x, Q("0cm"), Q("0cm"))
            mod_pla=geom.structure.Placement("pla_"+name1,volume=mod_lv, pos=mod_pos)
            main_lv.placements.append(mod_pla.name)

        depth= self.Depth3DST/2-self.offset3DSTcenter+ self.nRear1Mod*(self.pureSTModThickness+self.pureSTModGap)
        ModThickness=self.regModThickness
        if self.useRegMod!=True:
            ModThickness=self.noSlabModThickness
#        print "self.useRegMod:",self.useRegMod
        for imod in range(self.nRear2Mod):
            c2seg=depth+ (imod+1)*ModThickness
            costh=c2seg/self.kloeTrkRegRadius
            height=self.kloeTrkRegRadius*math.sqrt(1-costh*costh)
            name2="Rear_reg_"+str(imod)
            if self.useRegMod!=True:
                name2="Rear_nos_"+str(imod)
            halfDimension = {'dx': ModThickness/2.0, 'dy':height, 'dz': self.kloeTrkRegHalfDx}
            if self.useRegMod:
                mod_lv=self.construct_regModule(geom, name2, self.Material, halfDimension)
            else:
                mod_lv=self.construct_noSlabModule(geom, name2, self.Material, halfDimension)
            x= c2seg - ModThickness/2
            mod_pos=geom.structure.Position("pos_"+name2, x, Q("0cm"), Q("0cm"))
            mod_pla=geom.structure.Placement("pla_"+name2,volume=mod_lv, pos=mod_pos)
            main_lv.placements.append(mod_pla.name)

        depth+=self.nRear2Mod * ModThickness
        
        for imod in range(self.nRear3Mod):
            c2seg=depth+(imod+1)*self.noSlabModThickness
            costh=c2seg/self.kloeTrkRegRadius
            height=self.kloeTrkRegRadius*math.sqrt(1-costh*costh)
            name3="Rear_noslab_"+str(imod)
            halfDimension = {'dx': self.noSlabModThickness/2.0, 'dy':height, 'dz': self.kloeTrkRegHalfDx}
            mod_lv=self.construct_noSlabModule(geom, name3, self.Material, halfDimension)
            x= c2seg - self.noSlabModThickness/2
            mod_pos=geom.structure.Position("pos_"+name3, x, Q("0cm"), Q("0cm"))
            mod_pla=geom.structure.Placement("pla_"+name3,volume=mod_lv, pos=mod_pos)
            main_lv.placements.append(mod_pla.name)


    def construct_noSlabModule(self,geom, name, Material, halfDimension):
        
        main_shape = geom.shapes.Box( name, dx=halfDimension['dx'], dy=halfDimension['dy'], dz=halfDimension['dz'] )
        main_lv = geom.structure.Volume( "vol"+name, material="Air35C", shape=main_shape )
        height=halfDimension['dy']
        namef=name+"_foil"
        foil_lv= self.construct_foils(geom, namef, height)
        foil_pla=geom.structure.Placement("pla_"+namef, volume=foil_lv, pos="pos_foilchunk_in_NoSlabMod")
        main_lv.placements.append(foil_pla.name)

        names=name+"_ST"
        strawplane_lv=self.construct_strawplane(geom,names, height, "nos")
        strawplane_pla=geom.structure.Placement("pla_"+names, volume=strawplane_lv, pos="pos_ST_in_NoSlabMod")
        main_lv.placements.append(strawplane_pla.name)
        return main_lv
    
    def construct_regModule(self,geom, name, Material, halfDimension):

        main_shape = geom.shapes.Box( name, dx=halfDimension['dx'], dy=halfDimension['dy'], dz=halfDimension['dz'] )
        main_lv = geom.structure.Volume( "vol"+name, material="Air35C", shape=main_shape )

        nameslab=name+"_slab"
        slab_shape = geom.shapes.Box( nameslab, dx=self.slabThickness/2.0, dy=halfDimension['dy'], dz=halfDimension['dz'] )
        slab_lv = geom.structure.Volume( "vol"+nameslab, material="C3H6", shape=slab_shape )
        slab_pla=geom.structure.Placement("pla_"+nameslab, volume=slab_lv, pos="pos_Slab_in_RegMod")
        main_lv.placements.append(slab_pla.name)
        
        height=halfDimension['dy']
        namef=name+"_foil"
        foil_lv= self.construct_foils(geom, namef, height)
        foil_pla=geom.structure.Placement("pla_"+namef, volume=foil_lv, pos="pos_foilchunk_in_RegMod")
        main_lv.placements.append(foil_pla.name)
            
        names=name+"_ST"
        strawplane_lv=self.construct_strawplane(geom,names, height,"reg")
        strawplane_pla=geom.structure.Placement("pla_"+names, volume=strawplane_lv, pos="pos_ST_in_RegMod")
        main_lv.placements.append(strawplane_pla.name)

        
        return main_lv

    def construct_cModule(self,geom, name, Material, halfDimension):

        main_shape = geom.shapes.Box( name, dx=halfDimension['dx'], dy=halfDimension['dy'], dz=halfDimension['dz'] )
        main_lv = geom.structure.Volume( "vol"+name, material="Air35C", shape=main_shape )        

        graphite_shape = geom.shapes.Box( name+"_graph", dx=self.graphiteThickness/2.0, dy=halfDimension['dy'], dz=halfDimension['dz'] )
        graphite_lv = geom.structure.Volume( "vol"+name+"_graph", material="Graphite", shape=graphite_shape )
        graphite_pla=geom.structure.Placement("pla_"+name+"_graph", volume=graphite_lv, pos="pos_Graphite_in_Cmod")
        main_lv.placements.append(graphite_pla.name)

        height=halfDimension['dy']
        strawplane_lv=self.construct_strawplane(geom,name+"_ST", height, "gra")
        strawplane_pla=geom.structure.Placement("pla_"+name+"_ST", volume=strawplane_lv, pos="pos_ST_in_Cmod")
        main_lv.placements.append(strawplane_pla.name)
        return main_lv

    def construct_foils(self,geom, name, height):
        main_shape = geom.shapes.Box( name, dx=self.totfoilThickness/2.0, dy=height, dz= self.kloeTrkRegHalfDx )
        main_lv = geom.structure.Volume( "vol"+name, material="Air35C", shape=main_shape )
        namef=name+"_f"
        foil_shape = geom.shapes.Box( namef, dx=self.foilThickness/2.0, dy=height, dz= self.kloeTrkRegHalfDx )
        foil_lv = geom.structure.Volume( "vol"+namef, material="C3H6", shape=foil_shape )
        for i in range(self.nfoil):
            #            pos = [ -self.totfoilThickness/2.0 +self.foilThickness/2.0 + i*(self.foilThickness+self.foilGap) , Q('0m'), Q('0m')]
            #            foil_pos=geom.structure.Position("pos"+namef+str(i), pos[0],pos[1], pos[2])
            foil_pla=geom.structure.Placement("pla"+namef+str(i), volume=foil_lv, pos=self.foilpositions[i])
            main_lv.placements.append(foil_pla.name)
            
        return main_lv
        
    def construct_doubleST(self,geom, name, height, modtype, dcolumnLen=None):
        if dcolumnLen==None:
              dcolumnLen=self.kloeTrkRegHalfDx
        main_shape = geom.shapes.Box( name, dx=self.planeXXThickness*2, dy=height, dz=dcolumnLen)
        main_lv = geom.structure.Volume( "vol"+name, material="Air35C", shape=main_shape )

        hh_lv=self.construct_XXST(geom, "hh", name+"_hor", dcolumnLen,height, modtype)
        vv_lv=self.construct_XXST(geom, "vv", name+"_ver",height,dcolumnLen,modtype)
        hh_pla1=geom.structure.Placement("pla1_"+name+"_hh", volume=hh_lv, pos="pos_hh1_in_doubleST")
        vv_pla1=geom.structure.Placement("pla1_"+name+"_vv", volume=vv_lv,   pos="pos_vv1_in_doubleST",rot= "r90aboutX")
        hh_pla2=geom.structure.Placement("pla2_"+name+"_hh", volume=hh_lv, pos="pos_hh2_in_doubleST")
        vv_pla2=geom.structure.Placement("pla2_"+name+"_vv", volume=vv_lv,   pos="pos_vv2_in_doubleST",rot= "r90aboutX")
        main_lv.placements.append(hh_pla1.name)
        main_lv.placements.append(vv_pla1.name)
        main_lv.placements.append(hh_pla2.name)
        main_lv.placements.append(vv_pla2.name)
        return main_lv


    def construct_strawplane(self,geom,name, height, modtype, dcolumnLen=None):
        if dcolumnLen==None:
              dcolumnLen=self.kloeTrkRegHalfDx
        main_shape = geom.shapes.Box( name, dx=self.planeXXThickness, dy=height, dz=dcolumnLen)
        main_lv = geom.structure.Volume( "vol"+name, material="Air35C", shape=main_shape )
        
        hh_lv=self.construct_XXST(geom, "hh", name+"_hor", dcolumnLen,height, modtype)
        vv_lv=self.construct_XXST(geom, "vv", name+"_ver",height,dcolumnLen,modtype)
        hh_pla=geom.structure.Placement("pla_"+name+"_hh", volume=hh_lv, pos="pos_hh_in_ST")
        vv_pla=geom.structure.Placement("pla_"+name+"_vv", volume=vv_lv,   pos="pos_vv_in_ST",rot= "r90aboutX")
        main_lv.placements.append(hh_pla.name)
        main_lv.placements.append(vv_pla.name)

        return main_lv

    def construct_XXST(self,geom, tubeDirection, name, halflength, halfCrosslength, modtype):

        main_shape = geom.shapes.Box( name, dx=self.planeXXThickness/2.0, dy=halfCrosslength , dz=halflength)
        main_lv = geom.structure.Volume( "vol"+name, material="Air35C", shape=main_shape )

        if tubeDirection=="hh" and halflength==self.kloeTrkRegHalfDx:
            if modtype=="gra":
                straw_lv=self.horizontalST_Ar
            else:
                straw_lv=self.horizontalST_Xe
        else:
            straw_lv=self.construct_strawtube(geom, name+"_ST",halflength, modtype)
        
        
        Nstraw=int((2*halfCrosslength-self.strawRadius)/self.strawRadius/2.0)
#        print "name",name,"Nstraw ",Nstraw*2," length ",halflength*2
#        return main_lv
#        self.Nstraw_list.append(Nstraw*2)
        for i in range(Nstraw):
            pos1=[-self.planeXXThickness/2.0+self.strawRadius, halfCrosslength - (2*i+1)*self.strawRadius, Q('0m')]
            straw_pos1=geom.structure.Position("pos_"+name+"_"+str(i), pos1[0],pos1[1], pos1[2])
            straw_pla1=geom.structure.Placement("pla_"+name+"_"+str(i), volume=straw_lv, pos=straw_pos1)
            main_lv.placements.append(straw_pla1.name)

            pos2=[self.planeXXThickness/2.0 - self.strawRadius,  halfCrosslength -(2*i+2)*self.strawRadius, Q('0m')]
            straw_pos2=geom.structure.Position("pos_"+name+"_"+str(i+Nstraw), pos2[0],pos2[1], pos2[2])
            straw_pla2=geom.structure.Placement("pla_"+name+"_"+str(i+Nstraw), volume=straw_lv, pos=straw_pos2)
            main_lv.placements.append(straw_pla2.name)        
        return main_lv
        
        
    def construct_strawtube(self,geom, name, halflength, modtype):

        if modtype=="gra":
            airMaterial="stGas_Ar19"
        else:
            airMaterial="stGas_Xe19"
            
        main_shape = geom.shapes.Tubs(name, rmin=Q("0m"), rmax=self.strawRadius, dz=halflength)
        main_lv = geom.structure.Volume( "vol"+name, material="Air35C", shape=main_shape )

        coat_shape=geom.shapes.Tubs(name+"_coat", rmin = self.strawRadius- self.coatThickness , rmax = self.strawRadius, dz = halflength)
        coat_lv   = geom.structure.Volume(name+"_coat_lv", material="Aluminum", shape=coat_shape)
        
        mylar_shape = geom.shapes.Tubs(name+"_mylar", rmin = self.strawRadius- self.coatThickness - self.mylarThickness , rmax = self.strawRadius- self.coatThickness, dz = halflength)
        mylar_lv   = geom.structure.Volume(name+"_mylar_lv", material="Mylar", shape=mylar_shape)

        
        air_shape=geom.shapes.Tubs(name+"_air", rmin = self.strawWireWThickness+self.strawWireGThickness,
                                   rmax = self.strawRadius- self.coatThickness - self.mylarThickness, dz = halflength)
        air_lv   = geom.structure.Volume(name+"_air_lv", material=airMaterial, shape=air_shape)
        air_lv.params.append(("SensDet","Straw"))

        wireW_shape = geom.shapes.Tubs(name+"_wireW", rmin=Q("0um"), rmax = self.strawWireWThickness, dz = halflength)
        wireW_lv    = geom.structure.Volume(name+"_wireW_lv", material="Tungsten", shape=wireW_shape)

        wireG_shape = geom.shapes.Tubs(name+"_wireG", rmin= self.strawWireWThickness, rmax = self.strawWireWThickness+self.strawWireGThickness, dz = halflength)
        wireG_lv    = geom.structure.Volume(name+"_wireG_lv", material="Gold", shape=wireG_shape)
        
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
