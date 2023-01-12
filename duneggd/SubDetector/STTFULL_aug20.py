#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q
import time

class STTFULLBuilder(gegede.builder.Builder):
    def configure( self, halfDimension=None, Material=None,  **kwds):
        self.simpleStraw      	    = True
        self.sqrt3                  = 1.7320508
        #        self.start_time=time.time()
        #        print("start_time:",self.start_time)
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
        self.GapForST               = Q("7.5cm")
        self.AddGapForSlab          = Q("7.5cm")
        self.UpModGap               = Q("4mm")
        self.halfUpModGap           = self.UpModGap/2.
        
        
        self.nfoil                  = 119
        self.foilThickness          = Q("18um") # was 15um
        self.foilGap                = Q("117um")
        self.totfoilThickness       = self.nfoil * self.foilThickness + (self.nfoil-1)*self.foilGap
        self.nFoil1Batch            = 9
        self.nFoilBatch                 = 13
        self.batchFoilThickness     = self.foilThickness* self.nFoil1Batch + self.foilGap* (self.nFoil1Batch-1)
        self.leftNFoil              = self.nfoil - self.nFoil1Batch *  self.nFoilBatch
        
        self.slabThickness          = Q("5mm") # was 5.3mm
        self.graphiteThickness      = Q("4mm")

        self.gap                    = Q("4.67mm")
        
        self.planeXXThickness       = self.strawRadius * (2 + self.sqrt3)
        self.C3H6ModThickness       = self.planeXXThickness * 2 + self.totfoilThickness + self.slabThickness
        self.cModThickness          = self.planeXXThickness * 2 + self.graphiteThickness + self.gap*2
        self.trkModThickness        = self.planeXXThickness * 3 + self.gap*2
        self.upstream_trkModThickness        = self.planeXXThickness * 3 + self.gap*1
        self.downstream_C3H6ModThickness = self.planeXXThickness * 3 + self.totfoilThickness + self.slabThickness
        # liqAr + 1trkMod + (CMod+C3H6Mod * 12) * 6 + CMod + 6 * C3H6Mod + 4*trkMod
        # the gap between the trkMod and CMod is 4.67 instead of 4.67*2

        self.totModsThickness = 78 * self.C3H6ModThickness + 7 * self.cModThickness + 5*self.trkModThickness - self.gap + self.planeXXThickness
        self.nModule= 78 + 7 + 5
        self.nSymmetricModPair= (1+12)*3


        self.liqArThickness= self.kloeTrkRegRadius - self.trkModThickness - (self.cModThickness + 12*self.C3H6ModThickness)*3 + self.gap - self.cModThickness/2
        self.endgap= self.kloeTrkRegRadius*2 - self.liqArThickness - self.totModsThickness


        print(("endgap:",self.endgap))
        print(("totfoilThickness:",self.totfoilThickness))
        print(("self.slabThickness:",self.slabThickness))
        print(("planeXXThickness:",self.planeXXThickness))
        print(("C3H6ModThickness:",self.C3H6ModThickness))
        print(("cModThickness:",self.cModThickness))
        print(("totModsThickness:",self.totModsThickness))
        print(("liqArThickness:",self.liqArThickness))
        

    def construct(self,geom):

        pos_Slab_in_C3H6Mod=geom.structure.Position("pos_Slab_in_C3H6Mod", -self.C3H6ModThickness/2.0 +self.slabThickness/2.0, "0cm","0cm")
        pos_foilchunk_in_C3H6Mod=geom.structure.Position("pos_foilchunk_in_C3H6Mod",-self.C3H6ModThickness/2.0+self.slabThickness+self.totfoilThickness/2.0,"0cm","0cm")
        pos_ST_in_C3H6Mod=geom.structure.Position("pos_ST_in_C3H6Mod", self.C3H6ModThickness/2.0 - self.planeXXThickness, "0cm","0cm")
        pos_Slab_in_downstreamC3H6Mod=geom.structure.Position("pos_Slab_in_downstreamC3H6Mod", -self.downstream_C3H6ModThickness/2.0 +self.slabThickness/2.0, "0cm","0cm")
        pos_foilchunk_in_downstreamC3H6Mod=geom.structure.Position("pos_foilchunk_in_downstreamC3H6Mod",-self.downstream_C3H6ModThickness/2.0+self.slabThickness+self.totfoilThickness/2.0,"0cm","0cm")
        pos_ST_in_downstreamC3H6Mod=geom.structure.Position("pos_ST_in_downstreamC3H6Mod", self.downstream_C3H6ModThickness/2.0 - self.planeXXThickness*3./2., "0cm","0cm")        
        pos_Graphite_in_Cmod=geom.structure.Position("pos_Graphite_in_Cmod", -self.cModThickness/2.0+self.graphiteThickness/2.0 + self.gap, "0cm","0cm")
        pos_ST_in_Cmod=geom.structure.Position("pos_ST_in_Cmod",self.cModThickness/2.0 - self.planeXXThickness, "0cm","0cm")
        pos_hhleft_in_TrkMod=geom.structure.Position("pos_hhleft_in_TrkMod", - self.planeXXThickness, "0cm","0cm")
        pos_hhright_in_TrkMod=geom.structure.Position("pos_hhright_in_TrkMod",  self.planeXXThickness, "0cm","0cm")
        pos_hh_in_ST=geom.structure.Position("pos_hh_in_ST", -self.planeXXThickness/2.0, "0cm","0cm")
        pos_vv_in_ST=geom.structure.Position("pos_vv_in_ST", self.planeXXThickness/2.0 , "0cm","0cm")
        
        pos_straw2relative= geom.structure.Position("pos_straw2relative", self.strawRadius*self.sqrt3, self.strawRadius, Q('0m'))
        rot_mod_relative2polygon=geom.structure.Rotation("rot_mod_relative2polygon", Q('0deg'), Q('0deg'), Q('-7.5deg'))
        #        pos_moveDownEachMod=geom.structure.Position("pos_moveDownEachMod", Q('0m'), -self.halfUpModGap,Q('0m'))
        
        self.batchFoilPositions=[]
        self.foilPositionsInBatch=[]
        self.leftFoilPositions=[]
        for i in range(self.nFoilBatch):
            self.batchFoilPositions.append(geom.structure.Position("pos_batchFoilPositions_"+str(i),  -self.totfoilThickness/2.0 + self.batchFoilThickness/2.0 + i*(self.batchFoilThickness+self.foilGap) , Q('0m'), Q('0m')))
        for i in range(self.nFoil1Batch):
            self.foilPositionsInBatch.append(geom.structure.Position("pos_foilInBatch_"+str(i), -self.batchFoilThickness/2.0 + self.foilThickness/2.0 +(self.foilThickness + self.foilGap)*i, Q('0m'), Q('0m')))
        for i in range(self.leftNFoil):
            self.leftFoilPositions.append(geom.structure.Position("pos_left_"+str(i)+"_Foil", self.totfoilThickness/2.0 - self.foilThickness/2.0 - (self.foilThickness + self.foilGap)*i, Q('0m'), Q('0m')))

        self.horizontalST_Xe=self.construct_strawtube(geom,"horizontalST_Xe" , self.kloeTrkRegHalfDx - self.GapForST, "stGas_Xe19")
        self.horizontalST_Ar=self.construct_strawtube(geom,"horizontalST_Ar" , self.kloeTrkRegHalfDx - self.GapForST, "stGas_Ar19")
        
        #####################################################################################
        
        mod_types=["TrkMod"]
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
        mod_types.append("C3H6Mod")
        mod_types.append("C3H6Mod")
        mod_types.append("C3H6Mod")
        mod_types.append("TrkMod")
        mod_types.append("TrkMod")
        mod_types.append("TrkMod")
	mod_types.append("TrkMod")
        

        self.modthicknesses={"TrkMod": self.trkModThickness, "CMod":self.cModThickness, "C3H6Mod":self.C3H6ModThickness}
        self.modBuilder = {'C3H6Mod': self.construct_C3H6Module, 'TrkMod': self.construct_TrackingModule, 'CMod': self.construct_cModule}
        modthicknesses={"C3H6Mod":self.C3H6ModThickness, "TrkMod": self.trkModThickness, "CMod":self.cModThickness}

        ############################## the main tube    #######################################
        #        main_lv, main_hDim = ltools.main_lv( self, geom, "Tubs")
        stt_shape=geom.shapes.PolyhedraRegular("shape_stt",numsides=24, rmin=Q('0cm'), rmax=self.kloeVesselRadius , dz=self.kloeVesselHalfDx)
        main_lv = geom.structure.Volume('STTtracker',   material=self.Material, shape=stt_shape)
        print( "KLOESTTFULL::construct()")
        print(( "  main_lv = "+ main_lv.name))
        self.add_volume( main_lv )

        #        test_shape=geom.shapes.PolyhedraRegular("shape_test",numsides=24, rmin=self.kloeVesselRadius, rmax=self.kloeVesselRadius+Q("10cm"), dz=self.kloeVesselHalfDx)
        #        test_lv=geom.structure.Volume("test_lv",material=self.Material, shape=test_shape)
        #        test_pla=geom.structure.Placement("pla_test",volume=test_lv)
        #        main_lv.placements.append(test_pla.name)

        ########################################  liq Argon #################################
        #        self.construct_LAr_target(main_lv,geom)
        #####################################################################################
        
        imod=0
        left2upstream=self.liqArThickness
        name="STT_"+str(imod).zfill(2)+"_"+mod_types[imod]
        self.construct_one_module(main_lv, geom, name, self.Material, mod_types[imod], left2upstream, True)
        
        imod=40
        left2upstream=self.kloeTrkRegRadius- self.cModThickness/2
        name="STT_"+str(imod).zfill(2)+"_"+mod_types[imod]
        self.construct_one_module(main_lv, geom, name, self.Material, mod_types[imod], left2upstream)

        
        left2upstream=  72 * self.C3H6ModThickness + 7 * self.cModThickness + 1*self.trkModThickness - self.gap + self.liqArThickness
        for i in range(80, self.nModule):
            name="STT_"+str(i).zfill(2)+"_"+mod_types[i]
            if i==85:
                self.construct_one_module(main_lv, geom, name, self.Material, mod_types[i], left2upstream, False, True)
                left2upstream += self.modthicknesses[mod_types[i]] + self.planeXXThickness
            else:
                self.construct_one_module(main_lv, geom, name, self.Material, mod_types[i], left2upstream)
                left2upstream += self.modthicknesses[mod_types[i]]

        left2center=self.cModThickness/2
        
        for i in range(39,0,-1):
            #            print("imod%d  %s"%(i,mod_types[i]))
            ModThickness= self.modthicknesses[mod_types[i]]
            left2center += ModThickness
            #            print("left2center:",left2center)
            #            j=80-i
            name="STT_"+str(i).zfill(2)+"_"+mod_types[i]
            self.construct_2sym_modules(main_lv,geom, name, self.Material, mod_types[i], left2center)
            
            #        end_time=time.time()
            #        print("time diff:",end_time-self.start_time)

    def getHalfHeight(self,dis2c):
        nside=24
        theta=3.1415926536*2/nside
        d=self.kloeTrkRegRadius*math.tan(theta/2)
        if dis2c<d:
            return self.kloeTrkRegRadius
        projectedDis=d
        HalfHeight=self.kloeTrkRegRadius
        for i in range(1,nside/4):
            projectedDisPre=projectedDis
            projectedDis+=2*d*math.cos(i*theta)
            if dis2c<projectedDis:
                return HalfHeight-(dis2c-projectedDisPre)*math.tan(i*theta)
            else:
                HalfHeight-=2*d*math.sin(i*theta)
                
            

    def construct_one_module(self, main_lv, geom, name, Material, mod_type, left2upstream, upstreamMost_TrkMod=False, downstreamMost_C3H6Mod=False):
        ModThickness= self.modthicknesses[mod_type]
        if upstreamMost_TrkMod:
            ModThickness = self.upstream_trkModThickness            
            #        loc=[left2upstream - self.kloeTrkRegRadius + 0.5 * ModThickness,-self.halfUpModGap ,Q("0cm")]
        if downstreamMost_C3H6Mod:
            ModThickness= self.modthicknesses[mod_type] + self.planeXXThickness
        loc=[left2upstream - self.kloeTrkRegRadius + 0.5 * ModThickness,Q("0cm") - self.halfUpModGap, Q("0cm")]
        if (left2upstream+0.5 * ModThickness) < self.kloeTrkRegRadius:
            halfheight=self.getHalfHeight(self.kloeTrkRegRadius - left2upstream)
        else:
            halfheight=self.getHalfHeight(left2upstream- self.kloeTrkRegRadius +ModThickness)
        halfheight -=self.halfUpModGap
        #        halfheight -=self.GapForST
        fullheight=(halfheight + self.halfUpModGap)*2
        #        print("%s  %f"%(name,fullheight.magnitude ))
        #        print("%s %f %f"%(name, (self.kloeTrkRegRadius-left2upstream)/Q("1mm"), (self.kloeTrkRegRadius-left2upstream-ModThickness)/Q("1mm")) )
        
        halfDimension = {'dx': ModThickness/2.0, 'dy':halfheight, 'dz': self.kloeTrkRegHalfDx}
        construct_mod = self.modBuilder[mod_type]
        if upstreamMost_TrkMod:
            mod_lv = construct_mod(geom, name, Material, halfDimension, True)
        elif downstreamMost_C3H6Mod:
            mod_lv = construct_mod(geom, name, Material, halfDimension, True)            
        else:
            mod_lv = construct_mod(geom, name, Material, halfDimension)
            
            #            module_pos=geom.structure.Position("pos_"+name,loc[0],loc[1],loc[2])

        axisz = (0, 0, 1)
        loc2 = ltools.rotation(axisz, 7.5, loc)
        module_pos=geom.structure.Position("pos_"+name, loc2[0],loc2[1], loc2[2])
        module_pla=geom.structure.Placement("pla_"+name,volume=mod_lv,pos=module_pos, rot="rot_mod_relative2polygon")
        main_lv.placements.append(module_pla.name)
        
    def construct_2sym_modules(self, main_lv, geom, name, Material, mod_type, left2c):
        ModThickness= self.modthicknesses[mod_type]
        loc=[ -left2c + 0.5 * ModThickness,  Q("0cm") - self.halfUpModGap ,Q("0cm")]
        halfheight=self.getHalfHeight(left2c)
        halfheight -=self.halfUpModGap
        #	halfheight -=self.GapForST

        fullheight=(halfheight + self.halfUpModGap)*2
        #        print("%s  %f"%(name,fullheight.magnitude ))
        #        print("%s %f %f"%(name, left2c.magnitude, (left2c-ModThickness).magnitude))
        halfDimension = {'dx': ModThickness/2.0, 'dy':halfheight, 'dz': self.kloeTrkRegHalfDx}
        construct_mod = self.modBuilder[mod_type]
        mod_lv = construct_mod(geom, name, Material, halfDimension)
        
        axisz = (0, 0, 1)
        loc2 = ltools.rotation(axisz, 7.5, loc)
        module_posUp=geom.structure.Position("posUp_"+name, loc2[0],loc2[1],loc2[2])

        locDown=[-loc[0],loc[1],loc[2]]
        locDown2 = ltools.rotation(axisz, 7.5, locDown)
        module_posDown=geom.structure.Position("posDown_"+name, locDown2[0],locDown2[1] ,locDown2[2])
        
        module_plaUp=geom.structure.Placement("plaUp_"+name,volume=mod_lv,pos=module_posUp, rot="rot_mod_relative2polygon")
        module_plaDown=geom.structure.Placement("plaDown_"+name,volume=mod_lv,pos=module_posDown, rot="rot_mod_relative2polygon")
        main_lv.placements.append(module_plaUp.name)
        main_lv.placements.append(module_plaDown.name)

        
    def construct_LAr_target(self,main_lv,geom):
        
        liqArBox_shape = geom.shapes.Box("shape_liqArBox", dx= self.liqArThickness/2 - Q("1cm") , dy=self.kloeTrkRegRadius, dz= self.kloeTrkRegHalfDx )
        #        main_shape = geom.shapes.Tubs("shape_tube", rmin=Q("0m"), rmax=self.kloeTrkRegRadius, dz= self.kloeTrkRegHalfDx)
        main_shape_forLar=geom.shapes.PolyhedraRegular("shape_main_forLar",numsides=24, rmin=Q('0cm'), rmax=self.kloeTrkRegRadius, dz=self.kloeVesselHalfDx)
        loc=[-self.kloeTrkRegRadius+self.liqArThickness/2- Q("1cm"), Q('0m'), Q('0m')]
        ArBox_pos = geom.structure.Position("pos_ArTube2Box", loc[0],loc[1], loc[2])
        #### for intersection, it rotate first, then move to the posive along rotated coordinates
        #### for placement, it move to the position first, then rotate 
        rot_liqAr_relative2polygon=geom.structure.Rotation("rot_liqAr_relative2polygon", Q('0deg'), Q('0deg'), Q('7.5deg'))
        liqAr_shape  = geom.shapes.Boolean("liqAr_shape", type='intersection',
                                           first=main_shape_forLar,
                                           second=liqArBox_shape,
                                           pos=ArBox_pos,
                                           rot=rot_liqAr_relative2polygon)
        liqAr_lv=geom.structure.Volume('liqAr',material="LAr", shape=liqAr_shape)
        liqAr_pla=geom.structure.Placement("pla_liqAr",volume=liqAr_lv)
        main_lv.placements.append(liqAr_pla.name)
        
    def construct_TrackingModule(self,geom, name, Material, halfDimension, upstreamMost=False):
        
        main_shape = geom.shapes.Box("shape_"+name, dx=halfDimension['dx'], dy=halfDimension['dy'], dz=halfDimension['dz'] )
        main_lv = geom.structure.Volume(name, material="carbonComposite", shape=main_shape)
        hh_lv=self.construct_XXST(geom, "hh", name+"_hh", self.kloeTrkRegHalfDx - self.GapForST, halfDimension['dy']-self.GapForST, "stGas_Ar19")
        vv_lv=self.construct_XXST(geom, "vv", name+"_vv", halfDimension['dy'] - self.GapForST, self.kloeTrkRegHalfDx - self.GapForST, "stGas_Ar19")
        if upstreamMost:
            pos_hhleft_in_upstreamTrkMod=geom.structure.Position("pos_hhleft_in_upstreamTrkMod", self.upstream_trkModThickness/2 - self.planeXXThickness*2.5, "0cm","0cm")
            pos_hhright_in_upstreamTrkMod=geom.structure.Position("pos_hhright_in_upstreamTrkMod", self.upstream_trkModThickness/2 - self.planeXXThickness*0.5, "0cm","0cm")
            pos_vv_in_upstreamTrkMod=geom.structure.Position("pos_vv_in_upstreamTrkMod", self.upstream_trkModThickness/2 - self.planeXXThickness*1.5, "0cm","0cm")
            hh1_pla=geom.structure.Placement("pla_"+name+"_hhl", volume=hh_lv, pos="pos_hhleft_in_upstreamTrkMod")
            hh2_pla=geom.structure.Placement("pla_"+name+"_hhr", volume=hh_lv, pos="pos_hhright_in_upstreamTrkMod")
            vv_pla=geom.structure.Placement("pla_"+name+"_vv", volume=vv_lv, pos="pos_vv_in_upstreamTrkMod", rot= "r90aboutX")
            main_lv.placements.append(hh1_pla.name)
            main_lv.placements.append(hh2_pla.name)
            main_lv.placements.append(vv_pla.name)
        else:
            hh1_pla=geom.structure.Placement("pla_"+name+"_hhl", volume=hh_lv, pos="pos_hhleft_in_TrkMod")
            hh2_pla=geom.structure.Placement("pla_"+name+"_hhr", volume=hh_lv, pos="pos_hhright_in_TrkMod")
            vv_pla=geom.structure.Placement("pla_"+name+"_vv", volume=vv_lv, rot= "r90aboutX")
            main_lv.placements.append(hh1_pla.name)
            main_lv.placements.append(hh2_pla.name)
            main_lv.placements.append(vv_pla.name)
        return main_lv
    
    def construct_C3H6Module(self,geom, name, Material, halfDimension, downstreamMost=False):

        main_shape = geom.shapes.Box("shape_"+name, dx=halfDimension['dx'], dy=halfDimension['dy'], dz=halfDimension['dz'] )
        main_lv = geom.structure.Volume(name, material="carbonComposite", shape=main_shape )

        nameslab=name+"_slab"
        slab_shape = geom.shapes.Box( "shape_"+nameslab, dx=self.slabThickness/2.0, dy=halfDimension['dy']- self.GapForST- self.AddGapForSlab, dz=halfDimension['dz']- self.GapForST-self.AddGapForSlab )  #<--- additional 7.5cm for slab and graphite slab
        slab_lv = geom.structure.Volume(nameslab, material="C3H6", shape=slab_shape )
        
        namef=name+"_foil"
        foil_lv= self.construct_foils(geom, namef, halfDimension['dy'] - self.GapForST)

            
        names=name+"_ST"

        if not downstreamMost:
            slab_pla=geom.structure.Placement("pla_"+nameslab, volume=slab_lv, pos="pos_Slab_in_C3H6Mod")
            main_lv.placements.append(slab_pla.name)
            foil_pla=geom.structure.Placement("pla_"+namef, volume=foil_lv, pos="pos_foilchunk_in_C3H6Mod")
            main_lv.placements.append(foil_pla.name)
            strawplane_lv=self.construct_strawplane(geom, names, halfDimension['dy'] - self.GapForST,"stGas_Xe19")
            strawplane_pla=geom.structure.Placement("pla_"+names, volume=strawplane_lv, pos="pos_ST_in_C3H6Mod")
            main_lv.placements.append(strawplane_pla.name)
        else:
            slab_pla=geom.structure.Placement("pla_"+nameslab, volume=slab_lv, pos="pos_Slab_in_downstreamC3H6Mod")
            main_lv.placements.append(slab_pla.name)
            foil_pla=geom.structure.Placement("pla_"+namef, volume=foil_lv, pos="pos_foilchunk_in_downstreamC3H6Mod")
            main_lv.placements.append(foil_pla.name)
            strawplane_lv=self.construct_strawplane(geom, names, halfDimension['dy'] -self.GapForST ,"stGas_Xe19", True)
            strawplane_pla=geom.structure.Placement("pla_"+names, volume=strawplane_lv, pos="pos_ST_in_downstreamC3H6Mod")
            main_lv.placements.append(strawplane_pla.name)
            
        return main_lv

    def construct_cModule(self,geom, name, Material, halfDimension):

        main_shape = geom.shapes.Box("shape_"+name, dx=halfDimension['dx'], dy=halfDimension['dy'], dz=halfDimension['dz'] )
        main_lv = geom.structure.Volume(name, material="carbonComposite", shape=main_shape )        
        
        graphite_shape = geom.shapes.Box("shape_"+name+"_graph", dx=self.graphiteThickness/2.0, dy=halfDimension['dy']- self.GapForST -self.AddGapForSlab, dz=halfDimension['dz']- self.GapForST- self.AddGapForSlab ) #<--- additional 7.5cm for slab and graphite slab
        graphite_lv = geom.structure.Volume(name+"_graph", material="Graphite", shape=graphite_shape )
        graphite_pla=geom.structure.Placement("pla_"+name+"_graph", volume=graphite_lv, pos="pos_Graphite_in_Cmod")
        main_lv.placements.append(graphite_pla.name)

        strawplane_lv=self.construct_strawplane(geom,name+"_ST", halfDimension['dy'] - self.GapForST, "stGas_Ar19")
        strawplane_pla=geom.structure.Placement("pla_"+name+"_ST", volume=strawplane_lv, pos="pos_ST_in_Cmod")
        main_lv.placements.append(strawplane_pla.name)
        return main_lv

    def construct_foils(self,geom, name, halfheight):
        main_shape = geom.shapes.Box(name, dx=self.totfoilThickness/2.0, dy=halfheight, dz= self.kloeTrkRegHalfDx - self.GapForST )
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )

        batchFoil_shape=geom.shapes.Box("shape_"+name+"_batch", dx=self.batchFoilThickness/2.0, dy=halfheight, dz= self.kloeTrkRegHalfDx - self.GapForST )
        batchFoil_lv=geom.structure.Volume(name+"_batch", material="Air35C", shape=batchFoil_shape )
        foil_shape = geom.shapes.Box("shape_"+name+"_1f", dx=self.foilThickness/2.0, dy=halfheight, dz= self.kloeTrkRegHalfDx - self.GapForST )
        foil_lv = geom.structure.Volume(name+"_1f", material="C3H6", shape=foil_shape )        
        for i in range(self.nFoil1Batch):                        
            foil_pla=geom.structure.Placement("pla_"+name+"_"+str(i)+"inBatch", volume=foil_lv, pos=self.foilPositionsInBatch[i])
            batchFoil_lv.placements.append(foil_pla.name)        
            
        for i in range(self.nFoilBatch):
            foil_pla=geom.structure.Placement("pla"+name+"_batch_"+str(i), volume=batchFoil_lv, pos=self.batchFoilPositions[i])
            main_lv.placements.append(foil_pla.name)
        for i in range(self.leftNFoil):
            foil_pla=geom.structure.Placement("pla"+name+"_left_"+str(i), volume=foil_lv, pos=self.leftFoilPositions[i])
            main_lv.placements.append(foil_pla.name)
            
        return main_lv
        
    def construct_strawplane(self,geom,name, halfheight, gasMaterial, downstreamMost=False):
        if not downstreamMost:
            main_shape = geom.shapes.Box("shape_"+name, dx=self.planeXXThickness, dy=halfheight, dz=self.kloeTrkRegHalfDx - self.GapForST)
        else:
            main_shape = geom.shapes.Box("shape_"+name, dx=self.planeXXThickness*3./2., dy=halfheight, dz=self.kloeTrkRegHalfDx -self.GapForST)
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )
     
        hh_lv=self.construct_XXST(geom, "hh", name+"_hh", self.kloeTrkRegHalfDx - self.GapForST, halfheight, gasMaterial)
        vv_lv=self.construct_XXST(geom, "vv", name+"_vv", halfheight, self.kloeTrkRegHalfDx - self.GapForST, gasMaterial)
        if not downstreamMost:
            hh_pla=geom.structure.Placement("pla_"+name+"_hh", volume=hh_lv, pos="pos_hh_in_ST")
            vv_pla=geom.structure.Placement("pla_"+name+"_vv", volume=vv_lv,   pos="pos_vv_in_ST",rot= "r90aboutX")
            main_lv.placements.append(hh_pla.name)
            main_lv.placements.append(vv_pla.name)
        else:
            hh1_pla=geom.structure.Placement("pla_"+name+"_hhl", volume=hh_lv, pos="pos_hhleft_in_TrkMod")
            hh2_pla=geom.structure.Placement("pla_"+name+"_hhr", volume=hh_lv, pos="pos_hhright_in_TrkMod")
            vv_pla=geom.structure.Placement("pla_"+name+"_vv", volume=vv_lv, rot= "r90aboutX")
            main_lv.placements.append(hh1_pla.name)
            main_lv.placements.append(hh2_pla.name)
            main_lv.placements.append(vv_pla.name)
            
        return main_lv

    def construct_XXST(self,geom, tubeDirection, name, halflength, halfCrosslength, gasMaterial):

        main_shape = geom.shapes.Box("shape_"+name, dx=self.planeXXThickness/2.0, dy=halfCrosslength , dz=halflength)
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )

    
        if tubeDirection=="hh":
            if gasMaterial=="stGas_Ar19":
                straw_lv=self.horizontalST_Ar
            elif gasMaterial=="stGas_Xe19":
                straw_lv=self.horizontalST_Xe
            else:
                print("unrecognized gas material wrong wrong  wrong wrong wrong wrong wrong wrong wrong wrong wrong wrong")
        else:
            straw_lv=self.construct_strawtube(geom, name+"_ST",halflength, gasMaterial)
        
        
        Nstraw=int((2*halfCrosslength-self.strawRadius)/self.strawRadius/2.0)

        print(("%s %d %f"%(name,Nstraw*2, (halflength*2).magnitude)))
        
        return main_lv
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

        

        for i in range(Nstraw):
            pos1=geom.structure.Position("pos_"+name+"_"+str(i), -self.planeXXThickness/2.0+self.strawRadius, halfCrosslength - (2*i+2)*self.strawRadius, Q('0m'))
            twoStraw_pla1=geom.structure.Placement("pla_"+name+"_"+str(i), volume=twoStraw_lv, pos=pos1)
            main_lv.placements.append(twoStraw_pla1.name)
        return main_lv

    
    def construct_strawtube(self,geom, name, halflength, airMaterial):

        main_shape = geom.shapes.Tubs("shape_"+name, rmin=Q("0m"), rmax=self.strawRadius, dz=halflength)
        if self.simpleStraw:
            main_lv = geom.structure.Volume(name, material="straw_avg_ArXe", shape=main_shape )
            return main_lv
        
        if airMaterial!="stGas_Ar19" and airMaterial!="stGas_Xe19":
            print("unrecognized gas material wrong wrong  wrong wrong wrong wrong wrong wrong wrong wrong wrong wrong")
        
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
