#!/usr/bin/env python
#
##### adding frame
##### frame thickness: 8cm
##### for carbon slab and normal slab: there's 7cm empty between the edge and frame
##### for straws and foils, no empty space
import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q
import time

class STTBuilder(gegede.builder.Builder):
    def configure( self, halfDimension=None, Material=None, nBarrelModules=None, configuration=None, liqArThickness=None, TestMode=False, **kwds):
        self.simpleStraw      	    = False
        self.sqrt3                  = 1.7320508
        #        self.start_time=time.time()
        #        print("start_time:",self.start_time)
        self.TestMode = TestMode
        if TestMode:
            print()
            print(" !!!!!!! Warning !!!!!! it's test mode, it's quick but miss components ")
            print()
        self.halfDimension, self.Material = ( halfDimension, Material )

        self.kloeVesselRadius       = self.halfDimension['rmax']
        self.kloeVesselHalfDx       = self.halfDimension['dz']
        self.nBarrelModules         = nBarrelModules
        self.rotAngle               = 0.5 * Q('360deg') / self.nBarrelModules
        self.liqArThickness         = liqArThickness
        self.configuration          = configuration

        print((" ----> self.configuration : ",configuration))
        print()
        self.strawRadius            = Q('2.5mm')
        self.strawWireWThickness    = Q('20um')
        self.strawWireGThickness    = Q('20nm')
        self.coatThickness          = Q("70nm")
        self.mylarThickness         = Q("12um")

        #self.kloeVesselRadius       = Q('2m')
        #self.kloeVesselHalfDx       = Q('1.69m')
        self.extRadialgap           = Q("0cm")
        self.extLateralgap          = Q("0cm")
        self.kloeTrkRegRadius       = self.kloeVesselRadius - self.extRadialgap
        self.kloeTrkRegHalfDx       = self.kloeVesselHalfDx - self.extLateralgap
        self.FrameThickness         = Q("8cm")
        self.AddGapForSlab          = Q("7cm")
        self.UpModGap               = Q("4mm")
        self.halfUpModGap           = self.UpModGap/2.


        self.nfoil                  = 105
        self.foilThickness          = Q("18um") # was 15um
        self.foilGap                = Q("117um")
        self.totfoilThickness       = self.nfoil * self.foilThickness + (self.nfoil-1)*self.foilGap
        self.nFoil1Batch            = 8
        self.nFoilBatch             = 13
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
        # the gap between the trkMod and CMod is 4.67 instead of 4.67*2
        

        print(("trkModThickness  ", self.trkModThickness))
        print(("totfoilThickness:",self.totfoilThickness))
        print(("self.slabThickness:",self.slabThickness))
        print(("planeXXThickness:",self.planeXXThickness))
        print(("C3H6ModThickness:",self.C3H6ModThickness))
        print(("cModThickness:",self.cModThickness))
        print(("--------- liqArThickness -----------:",self.liqArThickness))

       # GRAIN
        self.HoneycombThickness  = Q("50mm")
        self.Carbon_fiberThickness   = Q("6mm") #two layers of 6 mm for a total of 12
        self.AluminumThickness   = Q("12mm")
        self.EndcapThickness     = Q("16mm")

        self.ExternalVesselX     = Q("365mm") + self.HoneycombThickness + self.Carbon_fiberThickness*2 #minor semiaxis of external vessel
        self.ExternalVesselY     = Q("900mm") + self.HoneycombThickness + self.Carbon_fiberThickness*2 #major semiaxis of external vessel
        self.ExternalVesselZ     = Q("950mm") + self.EndcapThickness #half lenght of external vessel

        self.InternalVesselX     = Q("237.5mm") + self.AluminumThickness #minor semiaxis of internal vessel
        self.InternalVesselY     = Q("728mm") + self.AluminumThickness #major semiaxis of internal vessel
        self.InternalVesselZ     = Q("650mm") + self.EndcapThickness #half lenght of internal vessel

        self.UpstreamVesselGap   = Q("30mm") #margin between kloe vessel and the LAr target
        self.MinDistExtVesTrMod  = Q("50mm") #margin between LAr target and upstream traking module
        self.InterVesselHalfGap  = Q('30mm')

    def init(self, geom):
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

        self.horizontalST_Xe=self.construct_strawtube(geom,"horizontalST_Xe" , self.kloeTrkRegHalfDx - self.FrameThickness, "stGas_Xe19")
        self.horizontalST_Ar=self.construct_strawtube(geom,"horizontalST_Ar" , self.kloeTrkRegHalfDx - self.FrameThickness, "stGas_Ar19")

        self.modthicknesses={"TrkMod": self.trkModThickness, "CMod":self.cModThickness, "C3H6Mod":self.C3H6ModThickness}
        self.modBuilder = {'C3H6Mod': self.construct_C3H6Module, 'TrkMod': self.construct_TrackingModule, 'CMod': self.construct_cModule}

    def construct(self, geom):

        #self.totModsThickness = 70 * self.C3H6ModThickness + 8 * self.cModThickness + 6*self.trkModThickness ### - self.gap ## + self.planeXXThickness
        #print("self.totModsThickness:{}".format(self.totModsThickness))

        self.init(geom)
        main_lv=self.build_STTSegment(geom)
        if self.configuration == "option_1":
            self.construct_option1(geom)
        elif self.configuration == "option_2":
            self.construct_option2(geom)
        self.build_modules(geom, main_lv)
        ##############################  option 1 ######################################
        ##############################  option 1 ######################################
        ## 2*Trk + (1*C + 9*C3H6)*7 + 1*C +  7*C3H6 + 4*Trk

        ##############################  option 2 ######################################
        ##############################  option 2 ######################################
        ## based on option 1, but remove the first two C3H6 modules


    def construct_option1(self,geom):

        self.mod_list=["TrkMod","TrkMod"]
        for i in range(7):
            for j in range(10):
                if j==0:
                    self.mod_list.append("CMod")
                else:
                    self.mod_list.append("C3H6Mod")
        self.mod_list.append("CMod")
        self.mod_list.append("C3H6Mod")
        self.mod_list.append("C3H6Mod")
        self.mod_list.append("C3H6Mod")
        self.mod_list.append("C3H6Mod")
        self.mod_list.append("C3H6Mod")
        self.mod_list.append("C3H6Mod")
        self.mod_list.append("C3H6Mod")
        self.mod_list.append("TrkMod")
        self.mod_list.append("TrkMod")
        self.mod_list.append("TrkMod")
        self.mod_list.append("TrkMod")
        self.centralModId=32
        self.firstSymModId=2
        self.SymStop2upstream = self.kloeTrkRegRadius + 27 * self.C3H6ModThickness + 3.5 * self.cModThickness
        self.SymStopFirstModId=63
        self.STTUpperLength = 27 * self.C3H6ModThickness + 3.5 * self.cModThickness + 2 * self.trkModThickness
        self.realDistance2ECAL= self.kloeTrkRegRadius - self.STTUpperLength
        print((" STTUpperLength:", self.STTUpperLength))
        print(("  self.realDistance2ECAL:", self.realDistance2ECAL))

    def construct_option2(self,geom):

        self.construct_option1(geom)
        self.mod_list.remove("C3H6Mod")
        self.mod_list.remove("C3H6Mod")
        self.centralModId=30
        self.firstSymModId=3
        self.SymStop2upstream = self.kloeTrkRegRadius + 25 * self.C3H6ModThickness + 2.5 * self.cModThickness
        self.SymStopFirstModId=58
        self.STTUpperLength = 25 * self.C3H6ModThickness + 3.5 * self.cModThickness + 2 * self.trkModThickness
        self.realDistance2ECAL= self.kloeTrkRegRadius - self.STTUpperLength
        print((" STTUpperLength:", self.STTUpperLength))
        print(("  self.realDistance2ECAL:", self.realDistance2ECAL))

    def build_STTSegment(self, geom):

        whole_shape=geom.shapes.PolyhedraRegular("whole_shape_for_stt",numsides=self.nBarrelModules, rmin=Q('0cm'), rmax=self.kloeVesselRadius , dz=self.kloeVesselHalfDx, sphi=self.rotAngle)
        upstream_shape=geom.shapes.Box("upstream_shape_for_stt", dx=0.5*self.liqArThickness, dy=self.kloeVesselRadius, dz=self.kloeVesselHalfDx )
        upstream_shape_pos = geom.structure.Position("upstream_shape_pos_for_stt", -self.kloeVesselRadius+0.5*self.liqArThickness, Q('0m'), Q('0m'))
        stt_shape = geom.shapes.Boolean("stt_shape",
                                         type='subtraction',
                                         first=whole_shape,
                                         second=upstream_shape,
                                         rot='noRotate',
                                         pos=upstream_shape_pos)

        main_lv = geom.structure.Volume('STTtracker',   material=self.Material, shape=stt_shape)
        print( "KLOESTTFULL::construct()")
        print(( "  main_lv = "+ main_lv.name))
        self.add_volume( main_lv )
        return main_lv

    def build_modules(self, geom, main_lv):
        ### do not use self.liqArThickness, it is not exact value
        ### do not use self.liqArThickness, it is not exact value
        left2upstream=self.realDistance2ECAL  
        for imod in range(0, self.firstSymModId):
            name="STT_"+str(imod).zfill(2)+"_"+self.mod_list[imod]
            self.construct_one_module(main_lv, geom, name, self.Material, self.mod_list[imod], left2upstream)
            #print("name:  %s  left2upstream:  %f"%(name,left2upstream));
            print(("name:", name,"  left2upstream:",left2upstream));
            left2upstream +=  self.modthicknesses[self.mod_list[imod]]


        left2center=self.cModThickness/2
        for i in range(self.centralModId-1, self.firstSymModId-1,-1):
            #            print("imod%d  %s"%(i,self.mod_list[i]))
            ModThickness= self.modthicknesses[self.mod_list[i]]
            left2center += ModThickness
            #            print("left2center:",left2center)
            #            j=80-i
            name="STT_"+str(i).zfill(2)+"_"+self.mod_list[i]
            
            print(("name:", name, " l1:",Q("2m")-left2center," l2:", Q("2m")+left2center-ModThickness,"  ModThickness:",ModThickness));
            self.construct_2sym_modules(main_lv,geom, name, self.Material, self.mod_list[i], left2center)


        imod=self.centralModId
        left2upstream=self.kloeTrkRegRadius- self.cModThickness/2
        name="STT_"+str(imod).zfill(2)+"_"+self.mod_list[imod]
        print((" name: ",name,"  left2upstream", left2upstream));
        self.construct_one_module(main_lv, geom, name, self.Material, self.mod_list[imod], left2upstream)


        left2upstream=  self.SymStop2upstream
        for i in range(self.SymStopFirstModId, len(self.mod_list)):
            name="STT_"+str(i).zfill(2)+"_"+self.mod_list[i]
            self.construct_one_module(main_lv, geom, name, self.Material, self.mod_list[i], left2upstream)
            #print("name:  %s  left2upstream:  %f"%(name,left2upstream));
            print(("name:", name,"  left2upstream:",left2upstream));
            left2upstream += self.modthicknesses[self.mod_list[i]]


    def getHalfHeight(self,dis2c):
        nside=24
        theta=3.1415926536*2/nside
        d=self.kloeTrkRegRadius*math.tan(theta/2)
        if dis2c<d:
            return self.kloeTrkRegRadius
        projectedDis=d
        HalfHeight=self.kloeTrkRegRadius
        for i in range(1,int(nside/4)):
            projectedDisPre=projectedDis
            projectedDis+=2*d*math.cos(i*theta)
            if dis2c<projectedDis:
                return HalfHeight-(dis2c-projectedDisPre)*math.tan(i*theta)
            else:
                HalfHeight-=2*d*math.sin(i*theta)



    def construct_one_module(self, main_lv, geom, name, Material, mod_type, left2upstream):
        ModThickness= self.modthicknesses[mod_type]
        loc=[left2upstream - self.kloeTrkRegRadius + 0.5 * ModThickness,Q("0cm") - self.halfUpModGap, Q("0cm")]
        if (left2upstream+0.5 * ModThickness) < self.kloeTrkRegRadius:
            halfheight=self.getHalfHeight(self.kloeTrkRegRadius - left2upstream)
        else:
            halfheight=self.getHalfHeight(left2upstream- self.kloeTrkRegRadius +ModThickness)
        halfheight -=self.halfUpModGap
        #        halfheight -=self.FrameThickness
        fullheight=(halfheight + self.halfUpModGap)*2
        #print("%s  %f"%(name,fullheight.magnitude ))
        #        print("%s %f %f"%(name, (self.kloeTrkRegRadius-left2upstream)/Q("1mm"), (self.kloeTrkRegRadius-left2upstream-ModThickness)/Q("1mm")) )

        halfDimension = {'dx': ModThickness/2.0, 'dy':halfheight, 'dz': self.kloeTrkRegHalfDx}
        construct_mod = self.modBuilder[mod_type]
        mod_lv = construct_mod(geom, name, Material, halfDimension)

        #            module_pos=geom.structure.Position("pos_"+name,loc[0],loc[1],loc[2])

        module_pos=geom.structure.Position("pos_"+name, loc[0],loc[1], loc[2])
        module_pla=geom.structure.Placement("pla_"+name,volume=mod_lv,pos=module_pos)
        main_lv.placements.append(module_pla.name)

    def construct_2sym_modules(self, main_lv, geom, name, Material, mod_type, left2c):
        ModThickness= self.modthicknesses[mod_type]
        loc=[ -left2c + 0.5 * ModThickness,  Q("0cm") - self.halfUpModGap , Q("0cm")]
        halfheight=self.getHalfHeight(left2c)
        halfheight -=self.halfUpModGap
        #	halfheight -=self.FrameThickness

        fullheight=(halfheight + self.halfUpModGap)*2
        #print("2%s  %f"%(name,fullheight.magnitude ))
        #        print("%s %f %f"%(name, left2c.magnitude, (left2c-ModThickness).magnitude))
        halfDimension = {'dx': ModThickness/2.0, 'dy':halfheight, 'dz': self.kloeTrkRegHalfDx}
        construct_mod = self.modBuilder[mod_type]
        mod_lv = construct_mod(geom, name, Material, halfDimension)

        module_posUp=geom.structure.Position("posUp_"+name, loc[0],loc[1],loc[2])

        locDown=[-loc[0],loc[1],loc[2]]
        module_posDown=geom.structure.Position("posDown_"+name, locDown[0],locDown[1] ,locDown[2])

        module_plaUp=geom.structure.Placement("plaUp_"+name,volume=mod_lv,pos=module_posUp)
        module_plaDown=geom.structure.Placement("plaDown_"+name,volume=mod_lv,pos=module_posDown)
        main_lv.placements.append(module_plaUp.name)
        main_lv.placements.append(module_plaDown.name)


    def construct_TrackingModule(self,geom, name, Material, halfDimension, upstreamMost=False):
        
        main_shape = geom.shapes.Box("shape_"+name, dx=halfDimension['dx'], dy=halfDimension['dy'], dz=halfDimension['dz'] )
        main_lv = geom.structure.Volume(name, material="carbonComposite", shape=main_shape)
        hh_lv=self.construct_XXST(geom, "hh", name+"_hh", self.kloeTrkRegHalfDx - self.FrameThickness, halfDimension['dy']-self.FrameThickness, "stGas_Ar19")
        vv_lv=self.construct_XXST(geom, "vv", name+"_vv", halfDimension['dy'] - self.FrameThickness, self.kloeTrkRegHalfDx - self.FrameThickness, "stGas_Ar19")
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
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )

        frameOuter_shape=geom.shapes.Box("shape_"+name+"_frameOuter", dx=halfDimension['dx'], dy=halfDimension['dy'], dz=halfDimension['dz'] )
        frameInner_shape=geom.shapes.Box("shape_"+name+"_frameInner", dx=halfDimension['dx'], dy=halfDimension['dy'] - self.FrameThickness, dz=halfDimension['dz']-self.FrameThickness )
        frame_shape  = geom.shapes.Boolean("shape_"+name+"_frame",  type='subtraction',
                                              first=frameOuter_shape,
                                              second=frameInner_shape,
                                              rot='noRotate')
        frame_lv = geom.structure.Volume(name+"_frame", material="carbonComposite", shape=frame_shape )
        frame_pla=geom.structure.Placement("pla_"+name+"_frame", volume=frame_lv)
        main_lv.placements.append(frame_pla.name)

        nameslab=name+"_slab"
        slab_shape = geom.shapes.Box( "shape_"+nameslab, dx=self.slabThickness/2.0, dy=halfDimension['dy']- self.FrameThickness- self.AddGapForSlab, dz=halfDimension['dz']- self.FrameThickness-self.AddGapForSlab )
        #<--- additional 7.5cm for slab and graphite slab
        slab_lv = geom.structure.Volume(nameslab, material="C3H6", shape=slab_shape )

        namef=name+"_foil"
        foil_lv= self.construct_foils(geom, namef, halfDimension['dy'] - self.FrameThickness)


        names=name+"_ST"

        if not downstreamMost:
            slab_pla=geom.structure.Placement("pla_"+nameslab, volume=slab_lv, pos="pos_Slab_in_C3H6Mod")
            main_lv.placements.append(slab_pla.name)
            foil_pla=geom.structure.Placement("pla_"+namef, volume=foil_lv, pos="pos_foilchunk_in_C3H6Mod")
            main_lv.placements.append(foil_pla.name)
            strawplane_lv=self.construct_strawplane(geom, names, halfDimension['dy'] - self.FrameThickness,"stGas_Xe19")
            strawplane_pla=geom.structure.Placement("pla_"+names, volume=strawplane_lv, pos="pos_ST_in_C3H6Mod")
            main_lv.placements.append(strawplane_pla.name)
        else:
            slab_pla=geom.structure.Placement("pla_"+nameslab, volume=slab_lv, pos="pos_Slab_in_downstreamC3H6Mod")
            main_lv.placements.append(slab_pla.name)
            foil_pla=geom.structure.Placement("pla_"+namef, volume=foil_lv, pos="pos_foilchunk_in_downstreamC3H6Mod")
            main_lv.placements.append(foil_pla.name)
            strawplane_lv=self.construct_strawplane(geom, names, halfDimension['dy'] -self.FrameThickness ,"stGas_Xe19", True)
            strawplane_pla=geom.structure.Placement("pla_"+names, volume=strawplane_lv, pos="pos_ST_in_downstreamC3H6Mod")
            main_lv.placements.append(strawplane_pla.name)

        return main_lv

    def construct_cModule(self,geom, name, Material, halfDimension):

        main_shape = geom.shapes.Box("shape_"+name, dx=halfDimension['dx'], dy=halfDimension['dy'], dz=halfDimension['dz'] )
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )

        frameOuter_shape=geom.shapes.Box("shape_"+name+"_frameOuter", dx=halfDimension['dx'], dy=halfDimension['dy'], dz=halfDimension['dz'] )
        frameInner_shape=geom.shapes.Box("shape_"+name+"_frameInner", dx=halfDimension['dx'], dy=halfDimension['dy'] - self.FrameThickness, dz=halfDimension['dz']-self.FrameThickness )
        frame_shape  = geom.shapes.Boolean("shape_"+name+"_frame",  type='subtraction',
                                              first=frameOuter_shape,
                                              second=frameInner_shape,
                                              rot='noRotate')
        frame_lv = geom.structure.Volume(name+"_frame", material="carbonComposite", shape=frame_shape )
        frame_pla=geom.structure.Placement("pla_"+name+"_frame", volume=frame_lv)
        main_lv.placements.append(frame_pla.name)

        graphite_shape = geom.shapes.Box("shape_"+name+"_graph", dx=self.graphiteThickness/2.0, dy=halfDimension['dy']- self.FrameThickness -self.AddGapForSlab, dz=halfDimension['dz']- self.FrameThickness- self.AddGapForSlab ) #<--- additional 7.5cm for slab and graphite slab
        graphite_lv = geom.structure.Volume(name+"_graph", material="Graphite", shape=graphite_shape )
        graphite_pla=geom.structure.Placement("pla_"+name+"_graph", volume=graphite_lv, pos="pos_Graphite_in_Cmod")
        main_lv.placements.append(graphite_pla.name)

        strawplane_lv=self.construct_strawplane(geom,name+"_ST", halfDimension['dy'] - self.FrameThickness, "stGas_Ar19")
        strawplane_pla=geom.structure.Placement("pla_"+name+"_ST", volume=strawplane_lv, pos="pos_ST_in_Cmod")
        main_lv.placements.append(strawplane_pla.name)
        return main_lv

    def construct_foils(self,geom, name, halfheight):
        main_shape = geom.shapes.Box(name, dx=self.totfoilThickness/2.0, dy=halfheight, dz= self.kloeTrkRegHalfDx - self.FrameThickness )
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )
        if self.TestMode:
            return main_lv
        batchFoil_shape=geom.shapes.Box("shape_"+name+"_batch", dx=self.batchFoilThickness/2.0, dy=halfheight, dz= self.kloeTrkRegHalfDx - self.FrameThickness )
        batchFoil_lv=geom.structure.Volume(name+"_batch", material="Air35C", shape=batchFoil_shape )
        foil_shape = geom.shapes.Box("shape_"+name+"_1f", dx=self.foilThickness/2.0, dy=halfheight, dz= self.kloeTrkRegHalfDx - self.FrameThickness )
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
            main_shape = geom.shapes.Box("shape_"+name, dx=self.planeXXThickness, dy=halfheight, dz=self.kloeTrkRegHalfDx - self.FrameThickness)
        else:
            main_shape = geom.shapes.Box("shape_"+name, dx=self.planeXXThickness*3./2., dy=halfheight, dz=self.kloeTrkRegHalfDx -self.FrameThickness)
        main_lv = geom.structure.Volume(name, material="Air35C", shape=main_shape )

        if self.TestMode:
            return main_lv
        hh_lv=self.construct_XXST(geom, "hh", name+"_hh", self.kloeTrkRegHalfDx - self.FrameThickness, halfheight, gasMaterial)
        vv_lv=self.construct_XXST(geom, "vv", name+"_vv", halfheight, self.kloeTrkRegHalfDx - self.FrameThickness, gasMaterial)
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
        if self.TestMode:
            return main_lv

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
            main_lv.params.append(("SensDet","Straw"))
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

##############################################################         GRAIN         ###################################################################


    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
#     def construct_GRAIN(self, geom, main_lv):

#         # build the external vessel envelop

#         Ext_vessel_outern_Carbon_fiber_layer_shape = geom.shapes.EllipticalTube("Ext_vessel_outern_Carbon_fiber_layer_shape",
#                                                                             dx = self.ExternalVesselX,
#                                                                             dy = self.ExternalVesselY,
#                                                                             dz = self.ExternalVesselZ)

#         Ext_vessel_outern_Carbon_fiber_layer_lv = geom.structure.Volume("Ext_vessel_outern_Carbon_fiber_layer_lv",
#                                                                     material = "Carbon_fiber",
#                                                                     shape = Ext_vessel_outern_Carbon_fiber_layer_shape)

#         pos = geom.structure.Position("GRAI_position",
#                                       -self.kloeVesselRadius + self.ExternalVesselX + self.UpstreamVesselGap,
#                                       Q('0mm'),
#                                       Q('0mm'))

#         Ext_vessel_outern_Carbon_fiber_layer_pla = geom.structure.Placement("Ext_vessel_outern_Carbon_fiber_layer_pla",
#                                                                         volume = Ext_vessel_outern_Carbon_fiber_layer_lv,
#                                                                         pos = pos)

#         main_lv.placements.append(Ext_vessel_outern_Carbon_fiber_layer_pla.name)

#         # build the layer of vacuum (in the real geometry honeycomb)

#         Honeycomb_empty_layer_shape  = geom.shapes.EllipticalTube("Honeycomb_empty_layer_shape",
#                                                                   dx = self.ExternalVesselX - self.Carbon_fiberThickness,
#                                                                   dy = self.ExternalVesselY - self.Carbon_fiberThickness,
#                                                                   dz = self.ExternalVesselZ - self.EndcapThickness) # self.EndcapThickness needed?


#         Honeycomb_empty_layer_lv = geom.structure.Volume("Honeycomb_empty_layer_lv",
#                                                           material = "Vacuum_cryo",
#                                                           shape = Honeycomb_empty_layer_shape)


#         Honeycomb_empty_layer_pla = geom.structure.Placement("Honeycomb_empty_layer_pla",
#                                                                 volume = Honeycomb_empty_layer_lv)


#         Ext_vessel_outern_Carbon_fiber_layer_lv.placements.append(Honeycomb_empty_layer_pla.name)


#         # build the inner layer of Carbon_fiber of the external vessel

#         Ext_vessel_inner_Carbon_fiber_layer_shape = geom.shapes.EllipticalTube("Ext_vessel_inner_Carbon_fiber_layer_shape",
#                                                                             dx = self.ExternalVesselX - self.Carbon_fiberThickness - self.HoneycombThickness,
#                                                                             dy = self.ExternalVesselY - self.Carbon_fiberThickness - self.HoneycombThickness,
#                                                                             dz = self.ExternalVesselZ - self.EndcapThickness)

#         Ext_vessel_inner_Carbon_fiber_layer_lv = geom.structure.Volume("Ext_vessel_inner_Carbon_fiber_layer_lv",
#                                                                     material = "Carbon_fiber",
#                                                                     shape = Ext_vessel_inner_Carbon_fiber_layer_shape)


#         Ext_vessel_inner_Carbon_fiber_layer_pla = geom.structure.Placement("Ext_vessel_inner_Carbon_fiber_layer_pla",
#                                                                        volume = Ext_vessel_inner_Carbon_fiber_layer_lv)


#         Honeycomb_empty_layer_lv.placements.append(Ext_vessel_inner_Carbon_fiber_layer_pla.name)


#         # build the layer of vacuum between the two vessels

#         vacuum_gap_between_vessels_shape  = geom.shapes.EllipticalTube("vacuum_gap_between_vessels_shape",
#                                                                        dx = self.ExternalVesselX - self.Carbon_fiberThickness*2 - self.HoneycombThickness,
#                                                                        dy = self.ExternalVesselY - self.Carbon_fiberThickness*2 - self.HoneycombThickness,
#                                                                        dz = self.ExternalVesselZ - self.EndcapThickness) # self.EndcapThickness needed?


#         vacuum_gap_between_vessels_lv = geom.structure.Volume("vacuum_gap_between_vessels_lv",
#                                                               material = "Vacuum_cryo",
#                                                               shape = vacuum_gap_between_vessels_shape)


#         vacuum_gap_between_vessels_pla = geom.structure.Placement("vacuum_gap_between_vessels_pla",
#                                                                   volume = vacuum_gap_between_vessels_lv)


#         Ext_vessel_inner_Carbon_fiber_layer_lv.placements.append(vacuum_gap_between_vessels_pla.name)


#         # build the layer of aluminum of the inner vessel

#         Aluminum_layer_inner_vessel_shape = geom.shapes.EllipticalTube("Aluminum_layer_inner_vessel_shape",
#                                                                        dx = self.InternalVesselX,
#                                                                        dy = self.InternalVesselY,
#                                                                        dz = self.InternalVesselZ)

#         Aluminum_layer_inner_vessel_lv = geom.structure.Volume("Aluminum_layer_inner_vessel_lv",
#                                                                 material = "Aluminum",
#                                                                 shape = Aluminum_layer_inner_vessel_shape)


#         Aluminum_layer_inner_vessel_pla = geom.structure.Placement("Aluminum_layer_inner_vessel_pla",
#                                                                    volume = Aluminum_layer_inner_vessel_lv)

#         vacuum_gap_between_vessels_lv.placements.append(Aluminum_layer_inner_vessel_pla.name)


#         # build the inner volume of LAr

#         LAr_volume_shape = geom.shapes.EllipticalTube("LAr_volume_shape",
#                                                       dx = self.InternalVesselX - self.AluminumThickness,
#                                                       dy = self.InternalVesselY - self.AluminumThickness,
#                                                       dz = self.InternalVesselZ - self.EndcapThickness)

#         LAr_volume_lv = geom.structure.Volume("LAr_volume_lv",
#                                               material = "LAr",
#                                               shape = LAr_volume_shape)

#         LAr_volume_lv.params.append(("SensDet", 'LArHit'))


#         LAr_volume_pla = geom.structure.Placement("LAr_volume_pla",
#                                                   volume = LAr_volume_lv)

#         Aluminum_layer_inner_vessel_lv.placements.append(LAr_volume_pla.name)


#         # build external vessel endcaps

#         EndCap_ExtVessel_shape = geom.shapes.EllipticalTube("EndCap_ExtVessel_shape",
#                                                             dx = self.ExternalVesselX,
#                                                             dy = self.ExternalVesselY,
#                                                             dz = self.EndcapThickness/2)

#         EndCap1_ExtVessel_lv = geom.structure.Volume("EndCap1_ExtVessel_lv",
#                                                       material = "Steel",
#                                                       shape = EndCap_ExtVessel_shape)

#         EndCap1_ExtVessel_pos = geom.structure.Position("EndCap1_ExtVessel_pos",
#                                                         Q("0mm"),#- self.kloeVesselRadius + self.UpstreamVesselGap + self.ExternalVesselX,
#                                                         Q("0mm"),
#                                                         - self.ExternalVesselZ +  self.EndcapThickness/2)

#         EndCap1_ExtVessel_pla = geom.structure.Placement("EndCap1_ExtVessel_pla",
#                                                           volume = EndCap1_ExtVessel_lv,
#                                                           pos = EndCap1_ExtVessel_pos)

#         Ext_vessel_outern_Carbon_fiber_layer_lv.placements.append(EndCap1_ExtVessel_pla.name)


#         EndCap2_ExtVessel_lv = geom.structure.Volume("EndCap2_ExtVessel_lv",
#                                                       material = "Steel",
#                                                       shape = EndCap_ExtVessel_shape)

#         EndCap2_ExtVessel_pos = geom.structure.Position("EndCap2_ExtVessel_pos",
#                                                         Q("0mm"),#- self.kloeVesselRadius + self.UpstreamVesselGap + self.ExternalVesselX,
#                                                         Q("0mm"),
#                                                         + self.ExternalVesselZ - self.EndcapThickness/2)

#         EndCap2_ExtVessel_pla = geom.structure.Placement("EndCap2_ExtVessel_pla",
#                                                          volume = EndCap2_ExtVessel_lv,
#                                                          pos = EndCap2_ExtVessel_pos)

#         Ext_vessel_outern_Carbon_fiber_layer_lv.placements.append(EndCap2_ExtVessel_pla.name)


#         #return Ext_vessel_outern_Carbon_fiber_layer_lv



# ##############################################################        END GRAIN         ###################################################################
