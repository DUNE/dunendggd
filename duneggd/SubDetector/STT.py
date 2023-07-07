import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q
import time

class STTBuilder(gegede.builder.Builder):

    def configure(self, STTconfiguration=None,
                        # SANDINNERVOLUME
                        halfDimension=None,     Material=None,            nBarrelModules=None,      configuration=None,     GRAINThickness=None,    clearenceGRAINTracker=None,        clearenceECALGRAIN=None,       clearenceTrackerECAL=None,
                        # STT   tracker
                        nofUpstreamTrkMod=None, nofDownstreamTrkMod=None, nofC3H6ModAfterCMod=None, 
                        # STRAW TUBE
                        StrawRadius=None,       DistStrawStraw=None,      DistStrawWall=None,       AngleStrawStraw=None,   StrawPlug=None,      StrawWireRadius=None, StrawWireCoatThickness=None, CoatThickness=None, MylarThickness=None, StrawGas=None,
                        # STT   MODULE
                        FrameThickness=None,    AddGapForSlab=None,       targetThickness=None,     gap=None,               nofStrawPlanes=None,    radiator=None,            nofFoils=None,         FoilThickness=None,  AirGapThickness=None, RadiatorThickness=None,
                        **kwds):
            
            self.start_time = time.time()

            #*******************************************************************| SANDINNERVOLUME |***********************************************************************************

            self.halfDimension, self.Material = ( halfDimension, Material )
            self.kloeVesselRadius             = self.halfDimension['rmax'] #= Q('2m')
            self.kloeVesselHalfDx             = self.halfDimension['dz'] #= Q('1.69m')
            self.extRadialgap                 = Q("0cm")
            self.extLateralgap                = Q("0cm")
            self.kloeTrkRegRadius             = self.kloeVesselRadius - self.extRadialgap
            self.kloeTrkRegHalfDx             = self.kloeVesselHalfDx - self.extLateralgap
            self.nBarrelModules               = nBarrelModules
            self.rotAngle                     = 0.5 * Q('360deg') / self.nBarrelModules
            self.GRAINThickness               = GRAINThickness
            self.configuration                = configuration
            self.STTcofiguration              = STTconfiguration
            self.clearenceGRAINTracker        = clearenceGRAINTracker
            self.clearenceECALGRAIN           = clearenceECALGRAIN
            self.clearenceTrackerECAL         = clearenceTrackerECAL

            #************************************************************************|  STT tracker  |**********************************************************************************
            self.nofUpstreamTrkMod            = nofUpstreamTrkMod
            self.nofDownstreamTrkMod          = nofDownstreamTrkMod
            self.nofC3H6ModAfterCMod          = nofC3H6ModAfterCMod
            self.AvailableUpstreamSpace       = self.kloeTrkRegRadius - self.GRAINThickness - self.clearenceGRAINTracker - self.clearenceECALGRAIN
            self.AvalilableDowstreamSpace     = self.kloeTrkRegRadius - self.clearenceTrackerECAL

            #************************************************************************|   STRAWTUBE   |**********************************************************************************

            self.StrawRadius                  = StrawRadius
            self.StrawPlug                    = StrawPlug
            self.DistStrawStraw               = DistStrawStraw
            self.DistStrawWall                = DistStrawWall
            self.AngleStrawStraw              = AngleStrawStraw
            self.StrawWireRadius              = StrawWireRadius
            self.StrawWireCoatThickness       = StrawWireCoatThickness
            self.CoatThickness                = CoatThickness
            self.MylarThickness               = MylarThickness
            self.StrawGas                     = StrawGas

            self.planeXXThickness             = 2*(self.StrawRadius + self.StrawPlug)*(math.cos(self.AngleStrawStraw/2)+1) + self.DistStrawStraw*math.cos(self.AngleStrawStraw/2) + 2*self.DistStrawWall
            self.StrawYDist                   = 2*((self.StrawRadius+self.StrawPlug)*(2*math.sin(self.AngleStrawStraw/2)-1) + self.DistStrawStraw*math.sin(self.AngleStrawStraw/2))
            self.StrawXDist                   = 2*(self.StrawRadius+self.StrawPlug)*(math.cos(self.AngleStrawStraw/2)-1) + self.DistStrawStraw*math.cos(self.AngleStrawStraw/2)

            #************************************************************************|   STT MODULE   |**********************************************************************************

            # target
            self.FrameThickness               = FrameThickness
            self.targetThickness              = targetThickness
            self.gap                          = gap
            self.AddGapForSlab                = AddGapForSlab
            # radiator
            self.radiator                     = radiator
            self.nofFoils                     = nofFoils
            self.FoilThickness                = FoilThickness
            self.AirGapThickness              = AirGapThickness 
            self.RadiatorThickness            = RadiatorThickness
            # straw planes
            self.nofStrawPlanes               = nofStrawPlanes
            #
            self.GetModThickness              = lambda mod_type : self.gap[mod_type]*2 + self.targetThickness[mod_type] + self.RadiatorThickness[mod_type] + self.nofStrawPlanes[mod_type]*self.planeXXThickness
            self.ModThickness                 = {"CMod" : self.GetModThickness("CMod"),"C3H6Mod" : self.GetModThickness("C3H6Mod"),"TrkMod" : self.GetModThickness("TrkMod")}
            
            #************************************************************************| STT components placement |**************************************************************************
            
            self.TargetPosInMod               = lambda mod_type : {"X":-self.ModThickness[mod_type]/2 + self.gap[mod_type] + self.targetThickness[mod_type]/2,"Y": Q("0mm"),"Z":Q("0mm")}

            self.RadiatorPosInMod             = lambda mod_type : {"X":-self.ModThickness[mod_type]/2 + self.gap[mod_type] + self.targetThickness[mod_type] + self.RadiatorThickness[mod_type]/2,"Y": Q("0mm"),"Z":Q("0mm")}
            
            self.PlaneXXPosInMod              = lambda mod_type : {"X":-self.ModThickness[mod_type]/2 + self.gap[mod_type] + self.targetThickness[mod_type] + self.RadiatorThickness[mod_type] + self.planeXXThickness/2,"Y": Q("0mm"),"Z":Q("0mm")}
            self.PlaneYYPosInMod              = lambda mod_type : {"X":-self.ModThickness[mod_type]/2 + self.gap[mod_type] + self.targetThickness[mod_type] + self.RadiatorThickness[mod_type] + self.planeXXThickness*1.5,"Y": Q("0mm"),"Z":Q("0mm")}

            self.PlaneXX1PosInTrkMod          = {"X":-self.ModThickness["TrkMod"]/2 + self.gap["TrkMod"] + self.planeXXThickness/2,   "Y":Q("0mm"), "Z":Q("0mm")}
            self.PlaneYYPosInTrkMod           = {"X":-self.ModThickness["TrkMod"]/2 + self.gap["TrkMod"] + self.planeXXThickness*1.5, "Y":Q("0mm"), "Z":Q("0mm")}
            self.PlaneXX2PosInTrkMod          = {"X":-self.ModThickness["TrkMod"]/2 + self.gap["TrkMod"] + self.planeXXThickness*2.5, "Y":Q("0mm"), "Z":Q("0mm")}

            #*****************************************************************************************************************************************************************************

            print("")
            print("*"*20+" INNVERVOLUME CONFIGURATION "+str(configuration)+" "+"*"*20)
            print("*"*25+" STT CONFIGURATION "+str(STTconfiguration)+" "+"*"*20)
            print("")
            print("-"*20+" INNERVOLUME INFO "+"-"*20)
            print("")
            print("GRAINThickness              | "+str(self.GRAINThickness))
            print("distance GRAIN-ECAL         | "+str(self.clearenceECALGRAIN))
            print("distance GRAIN-STT          | "+str(self.clearenceGRAINTracker))
            print("distance STT-ECAL           | "+str(self.clearenceTrackerECAL))
            print("")
            print("-"*20+" STRAW INFO "+"-"*20)
            print("")
            print("straw radius                | "+str(self.StrawRadius))
            print("straw plug                  | "+str(self.StrawPlug))
            print("plug-plug rel distance      | "+str(self.DistStrawStraw))
            print("plug-plug X   distance      | "+str(self.StrawXDist)+"  (if neg value = intersection if they were alligned)")
            print("plug-plug Y   distance      | "+str(self.StrawYDist))
            print("plug-wall      distance     | "+str(self.DistStrawWall))
            print("")
            print("-"*20+" STT MOD INFO "+"-"*20)
            print("")
            print("Ctarget      Thickness      | "+str(self.targetThickness["CMod"]))
            print("C3H6target   Thickness      | "+str(self.targetThickness["C3H6Mod"]))
            print("planeXX      Thickness      | "+str(self.planeXXThickness))
            print("C3H6radiator Thickness      | "+str(self.RadiatorThickness["C3H6Mod"]))
            print("trkMod       Thickness      | "+str(self.ModThickness["TrkMod"]))
            print("C3H6Mod      Thickness      | "+str(self.ModThickness["C3H6Mod"]))
            print("CMod         Thickness      | "+str(self.ModThickness["CMod"]))
            print("")

    def init(self):

        #************************************** DEFINE STT SEQUENCE *************************************
        self.SuperModThickness            = self.ModThickness["CMod"] + self.ModThickness["C3H6Mod"] * self.nofC3H6ModAfterCMod
        
        # *************************************    SAND upstream    *************************************

        # 1 CMod in the SAND center and nofUpstreamTrkMod at the beginning of the tracker

        self.UpstreamSpaceLeft            = self.AvailableUpstreamSpace - self.ModThickness["CMod"]/2 - self.ModThickness["TrkMod"] * self.nofUpstreamTrkMod
        
        self.nofUpstreamSuperMod          = int((self.UpstreamSpaceLeft / self.SuperModThickness).to_base_units().magnitude)
        
        # 1 CMod always in front of sequence of C3H6Mod

        self.UpstreamSpaceLeft            -= (self.nofUpstreamSuperMod * self.SuperModThickness + self.ModThickness["CMod"])
        
        self.nofFirstUpstreamC3H6Mod      = int((self.UpstreamSpaceLeft / self.ModThickness["C3H6Mod"]).to_base_units().magnitude)
        
        self.UpstreamSpaceLeft            -= self.nofFirstUpstreamC3H6Mod * self.ModThickness["C3H6Mod"]
        
        self.STT_startX                   = - self.AvailableUpstreamSpace + self.UpstreamSpaceLeft 

        # *************************************    SAND downstream    *************************************
        
        # 1 CMod in the SAND center and nofDownstreamTrkMod at the end of the tracker

        self.DownstreamSpaceLeft          = self.AvalilableDowstreamSpace + self.ModThickness["CMod"]/2 - self.ModThickness["TrkMod"] * self.nofDownstreamTrkMod
        
        self.nofDownstreamSuperMod        = int((self.DownstreamSpaceLeft / self.SuperModThickness).to_base_units().magnitude)

        # 1 CMod always in front of sequence of C3H6Mod

        self.DownstreamSpaceLeft          -= (self.nofDownstreamSuperMod * self.SuperModThickness + self.ModThickness["CMod"])

        self.nofLastDownstreamC3H6Mod     = int((self.DownstreamSpaceLeft/self.ModThickness["C3H6Mod"]).to_base_units().magnitude)

        self.DownstreamSpaceLeft          -= self.nofLastDownstreamC3H6Mod * self.ModThickness["C3H6Mod"]

        self.nofStrawCurrentMod           = 0
        self.nofStrawTubeConstructed      = 0
        self.TotalCMass                   = 0
        self.TotalC3H6Mass                = 0

        module_sequence,modules_X_center = [],[]

        running_X = self.STT_startX

        for i in range(self.nofUpstreamTrkMod): 
            module_sequence.append("TrkMod")
            modules_X_center.append(running_X + self.ModThickness["TrkMod"]/2)
            running_X += self.ModThickness["TrkMod"]

        for i in range(self.nofFirstUpstreamC3H6Mod):
            if(i==0): 
                module_sequence.append("CMod")
                modules_X_center.append(running_X + self.ModThickness["CMod"]/2)
                running_X += self.ModThickness["CMod"]
            module_sequence.append("C3H6Mod")
            modules_X_center.append(running_X + self.ModThickness["C3H6Mod"]/2)
            running_X += self.ModThickness["C3H6Mod"]

        for i in range(self.nofUpstreamSuperMod + self.nofDownstreamSuperMod):
            module_sequence.append("CMod")
            modules_X_center.append(running_X + self.ModThickness["CMod"]/2)
            running_X += self.ModThickness["CMod"]
            for i in range(self.nofC3H6ModAfterCMod): 
                module_sequence.append("C3H6Mod")
                modules_X_center.append(running_X + self.ModThickness["C3H6Mod"]/2)
                running_X += self.ModThickness["C3H6Mod"]
        
        for i in range(self.nofLastDownstreamC3H6Mod):
            if(i==0): 
                module_sequence.append("CMod")
                modules_X_center.append(running_X + self.ModThickness["CMod"]/2)
                running_X += self.ModThickness["CMod"]
            module_sequence.append("C3H6Mod")
            modules_X_center.append(running_X + self.ModThickness["C3H6Mod"]/2)
            running_X += self.ModThickness["C3H6Mod"]
                
        
        for i in range(self.nofDownstreamTrkMod): 
            module_sequence.append("TrkMod")
            modules_X_center.append(running_X + self.ModThickness["TrkMod"]/2)
            running_X += self.ModThickness["TrkMod"]
        
        
        self.module_sequence    = module_sequence
        self.modules_X_center   = modules_X_center
    

    def construct(self, geom):

        self.init()
        main_lv = self.build_STTSegment(geom)

        print("")
        print("nof C3H6 Mod                | "+str((self.nofUpstreamSuperMod+self.nofDownstreamSuperMod)*self.nofC3H6ModAfterCMod+self.nofFirstUpstreamC3H6Mod+self.nofLastDownstreamC3H6Mod))
        print("nof C Mod                   | "+str( self.nofUpstreamSuperMod+self.nofDownstreamSuperMod + 2))
        print("nof Trk Mod                 | "+str(self.nofUpstreamTrkMod+self.nofDownstreamTrkMod))
        print("")

        for mod_id in range(len(self.module_sequence)):

            print("Building STT MODULE "+str(mod_id)+" "+self.module_sequence[mod_id])
            mod_lv       = self.construct_one_mod(geom, main_lv, mod_id) 
            mod_position = geom.structure.Position("mod_"+str(mod_id)+"_pos", self.modules_X_center[mod_id], Q("0m"), Q("0m"))
            mod_place    = geom.structure.Placement("mod_"+str(mod_id)+"_place", volume = mod_lv.name, pos = mod_position.name)

            main_lv.placements.append(mod_place.name)

            # if mod_id==4: break
        
        self.stop_time = time.time()
        print("")
        print("nof straws constructed      | "+str(self.nofStrawTubeConstructed))
        print("total Carbon mass           | "+str(self.TotalCMass))
        print("total C3H6   mass           | "+str(self.TotalC3H6Mass))
        print("time to construct STT       | "+str(self.stop_time-self.start_time)+" seconds")
        print("")
        

    def build_STTSegment(self, geom):

        whole_shape         = geom.shapes.PolyhedraRegular("whole_shape_for_stt",numsides=self.nBarrelModules, rmin=Q('0cm'), rmax=self.kloeVesselRadius , dz=self.kloeVesselHalfDx, sphi=self.rotAngle)
        upstream_shape      = geom.shapes.Box("upstream_shape_for_stt", dx=0.5*self.GRAINThickness, dy=self.kloeVesselRadius, dz=self.kloeVesselHalfDx )
        upstream_shape_pos  = geom.structure.Position("upstream_shape_pos_for_stt", - self.kloeVesselRadius + 0.5*self.GRAINThickness + self.clearenceECALGRAIN, Q('0m'), Q('0m'))
        stt_shape           = geom.shapes.Boolean("stt_shape", type='subtraction', first=whole_shape, second=upstream_shape, rot='noRotate', pos=upstream_shape_pos)
        main_lv             = geom.structure.Volume('STTtracker',   material=self.Material, shape=stt_shape)
        print(( "  main_lv = "+ main_lv.name))
        self.add_volume( main_lv )
        return main_lv

    def getHalfHeight(self,dis2c):

        nside   = 24
        theta   = 3.1415926536*2/nside
        d       = self.kloeTrkRegRadius*math.tan(theta/2)
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
    
    # def getHalfHeight(self,dis2c):
    #     PolyAngle   = 2*math.pi/self.nBarrelModules
    #     alpha0      = PolyAngle/2
    #     alpha       = lambda i : alpha0 + i*PolyAngle
    #     x           = lambda i : self.kloeTrkRegRadius * math.sin(alpha(i-1))
    #     y           = lambda i : self.kloeTrkRegRadius * math.cos(alpha(i-1))
    #     m           = lambda i : (y(i-1) - y(i)) / (x(i-1) - x(i))
    #     q           = lambda i : (x(i-1)*y(i) - x(i)*y(i-1)) / (x(i-1) - x(i))
        
    #     halfHeight=0
    #     # halfHeight = Q("3.9657794455m")
    #     for i in range(1,int(self.nBarrelModules/4)):
    #         if (dis2c > x(i-1)) and (dis2c < x(i)):
    #             print(str(m(i))+" "+str(q(i)))
    #             halfHeight = m(i) * dis2c + q(i)

    #         elif(dis2c > x(int(self.nBarrelModules/4)-1)):
    #             x_last = self.kloeTrkRegRadius * math.cos(alpha0)
    #             y_last = self.kloeTrkRegRadius * math.sin(alpha0)
    #             m_last = (y(i) - y_last) / (x(i) - x_last)
    #             q_last = (x(i)*y_last - x_last*y(i)) / (x(i) - x_last)
    #             halfHeight = m_last * dis2c + q_last

    #     return halfHeight

    def construct_one_mod(self, geom, main_lv, mod_id):
        # module will be completely defined once you know the module id

        module_type             = self.module_sequence[mod_id]
        base_name               = module_type + "_" + str(mod_id).zfill(2) 
        module_half_heigth      = self.getHalfHeight(abs(self.modules_X_center[mod_id]) + self.ModThickness[module_type]/2)
        main_shape              = geom.shapes.Box(base_name+"_shape", dx=self.ModThickness[module_type]/2, dy=module_half_heigth, dz=self.kloeTrkRegHalfDx )
        main_lv                 = geom.structure.Volume(base_name, material="Air35C", shape=main_shape )

        planeXX_name            = base_name+"_planeXX" 
        planeYY_name            = base_name+"_planeYY" 
        planeXX                 = self.constructStrawPlane(geom, planeXX_name, dy = module_half_heigth - self.FrameThickness,     dz = self.kloeTrkRegHalfDx - self.FrameThickness, gas = self.StrawGas[module_type])
        planeYY                 = self.constructStrawPlane(geom, planeYY_name, dy = self.kloeTrkRegHalfDx - self.FrameThickness,  dz = module_half_heigth - self.FrameThickness,    gas = self.StrawGas[module_type])
        self.nofStrawTubeConstructed += self.nofStrawCurrentMod * self.nofStrawPlanes[module_type]
        
        
        if(module_type!="TrkMod"):
            frame        = self.constructFrame(geom,    base_name,    module_type,    dy = module_half_heigth,                                            dz = self.kloeTrkRegHalfDx)
            target       = self.constructTarget(geom,   base_name,    module_type,    dy = module_half_heigth - self.FrameThickness - self.AddGapForSlab, dz = self.kloeTrkRegHalfDx - self.FrameThickness - self.AddGapForSlab)
            if (self.radiator=="yes" and module_type=='C3H6Mod'):Radiator = self.constructRadiator(geom, base_name,    module_type,    dy = module_half_heigth - self.FrameThickness, dz = self.kloeTrkRegHalfDx - self.FrameThickness)
            
            frame_pos    = geom.structure.Position(base_name+"_frame_pos",Q("0mm"),Q("0mm"),Q("0mm"))
            target_pos   = geom.structure.Position(base_name+"_target_pos",    self.TargetPosInMod(module_type)["X"],   self.TargetPosInMod(module_type)["Y"],   self.TargetPosInMod(module_type)["Z"])
            planeXX_pos  = geom.structure.Position(planeXX_name+"_pos",        self.PlaneXXPosInMod(module_type)["X"],  self.PlaneXXPosInMod(module_type)["Y"],  self.PlaneXXPosInMod(module_type)["Z"])
            planeYY_pos  = geom.structure.Position(planeYY_name+"_pos",        self.PlaneYYPosInMod(module_type)["X"],  self.PlaneYYPosInMod(module_type)["Y"],  self.PlaneYYPosInMod(module_type)["Z"])
            if (self.radiator=="yes" and module_type=='C3H6Mod'):Radiator_pos = geom.structure.Position(base_name+"_radiator_pos",  self.RadiatorPosInMod(module_type)["X"], self.RadiatorPosInMod(module_type)["Y"], self.RadiatorPosInMod(module_type)["Z"])

            frame_pla    = geom.structure.Placement(base_name+"_frame_pla",     volume = frame,    pos = frame_pos)
            target_pla   = geom.structure.Placement(base_name+"_target_pla",    volume = target,   pos = target_pos)
            planeXX_pla  = geom.structure.Placement(planeXX_name+"_pla",        volume = planeXX,  pos = planeXX_pos)
            planeYY_pla  = geom.structure.Placement(planeYY_name+"_pla",        volume = planeYY,  pos = planeYY_pos, rot= "r90aboutX")
            if (self.radiator=="yes" and module_type=='C3H6Mod'):Radiator_pla = geom.structure.Placement(base_name+"_radiator_pla",  volume = Radiator, pos = Radiator_pos)

            main_lv.placements.append(frame_pla.name)
            main_lv.placements.append(target_pla.name)
            if (self.radiator=="yes" and module_type=='C3H6Mod'): main_lv.placements.append(Radiator_pla.name)
            main_lv.placements.append(planeXX_pla.name)
            main_lv.placements.append(planeYY_pla.name)


        else:

            planeXX1_pos = geom.structure.Position(planeXX_name+"1_pos",self.PlaneXX1PosInTrkMod["X"],self.PlaneXX1PosInTrkMod["Y"],self.PlaneXX1PosInTrkMod["Z"])
            planeYY_pos  = geom.structure.Position(planeYY_name+"_pos" ,self.PlaneYYPosInTrkMod["X"], self.PlaneYYPosInTrkMod["Y"], self.PlaneYYPosInTrkMod["Z"])
            planeXX2_pos = geom.structure.Position(planeXX_name+"2_pos",self.PlaneXX2PosInTrkMod["X"],self.PlaneXX2PosInTrkMod["Y"],self.PlaneXX2PosInTrkMod["Z"])

            planeXX1_pla = geom.structure.Placement(planeXX_name+"1_pla", volume = planeXX, pos = planeXX1_pos)
            planeYY_pla  = geom.structure.Placement(planeYY_name+"_pla",  volume = planeYY, pos = planeYY_pos, rot= "r90aboutX")
            planeXX2_pla = geom.structure.Placement(planeXX_name+"2_pla", volume = planeXX, pos = planeXX2_pos)

            main_lv.placements.append(planeXX1_pla.name)
            main_lv.placements.append(planeYY_pla.name)
            main_lv.placements.append(planeXX2_pla.name)
            
        return main_lv

    def constructFrame(self, geom, base_name, module_type, dy, dz):
        frame_name       = base_name+"_frame"
        outerFrame_shape = geom.shapes.Box(frame_name+"_out_shape", dx=self.ModThickness[module_type]/2, dy=dy, dz=dz)
        innerFrame_shape = geom.shapes.Box(frame_name+"_in_shape" , dx=self.ModThickness[module_type]/2, dy=dy-self.FrameThickness, dz=dz-self.FrameThickness)
        frame_shape      = geom.shapes.Boolean(frame_name+"_shape", type="subtraction", first=outerFrame_shape, second=innerFrame_shape, rot='noRotate')
        
        frame_lv         = geom.structure.Volume(frame_name, material="carbonComposite", shape=frame_shape)
        return frame_lv

        
    def constructTarget(self, geom, base_name, module_type, dy, dz):
        target_name     = base_name + "_target"
        target_material = "Graphite" if module_type == 'CMod' else "C3H6"
        target_shape    = geom.shapes.Box(target_name+"_shape",dx=self.targetThickness[module_type]/2, dy=dy, dz=dz)
        target_lv       = geom.structure.Volume(target_name, material=target_material, shape=target_shape)

        # keep track of the total mass count
        if(module_type=="CMod"):
            self.TotalCMass    += Q("2.23 g/cm^2")  * (self.targetThickness[module_type]/2*dy*dz)*2 # grams
        elif(module_type=="C3H6Mod"):
            self.TotalC3H6Mass += Q("0.946 g/cm^2") * (self.targetThickness[module_type]/2*dy*dz)*2
        return target_lv
    
    def constructRadiator(self, geom, base_name, module_type, dy, dz):
        radiator_name   = base_name + "_radiator"
        radiator_shape  = geom.shapes.Box(radiator_name+"_shape", dx=self.RadiatorThickness[module_type]/2, dy=dy, dz=dz)
        radiator_lv     = geom.structure.Volume(radiator_name, material="Air35C", shape=radiator_shape)

        foil_name       = base_name + "_foil"
        foil_shape      = geom.shapes.Box(foil_name+"_shape", dx=self.FoilThickness/2, dy=dy, dz=dz)
        foil_lv         = geom.structure.Volume(foil_name, material="C3H6", shape=foil_shape)

        running_x = - self.RadiatorThickness[module_type]/2 + self.FoilThickness/2
        for i in range(self.nofFoils):
            foil_i_name = foil_name+str(i)
            foil_pos    = geom.structure.Position(foil_i_name+"_pos", running_x, Q('0m'), Q('0m'))
            foil_place  = geom.structure.Placement(foil_i_name+"_place", volume = foil_lv.name, pos = foil_pos.name)
            radiator_lv.placements.append(foil_place.name)

            running_x += self.FoilThickness + self.AirGapThickness
        
        return radiator_lv


    def constructStrawPlane(self, geom, base_name, dy, dz, gas):

        plane_shape = geom.shapes.Box(base_name, dx=self.planeXXThickness/2, dy=dy, dz=dz)
        plane_lv    = geom.structure.Volume(base_name,material="Air35C", shape=plane_shape)
        straw_lv    = self.constructStraw(geom, base_name, dz, gas)

        Nstraw      = int((dy/(self.StrawRadius + self.StrawPlug + self.StrawYDist/2)).to_base_units().magnitude)*2 - 1

        left_spaceY = dy.to_base_units().magnitude*1E3%(self.StrawRadius + self.StrawPlug + self.StrawYDist/2).to_base_units().magnitude

        running_y   = dy - Q(str(left_spaceY)+"mm")
        
        for i in range(Nstraw):

            running_y   -= (2*self.StrawRadius + 2*self.StrawPlug + self.DistStrawStraw)*math.sin(self.AngleStrawStraw/2) 
            running_x   = (-1)**(i+1) * (2*(self.StrawRadius+self.StrawPlug)+self.StrawXDist)/2
            straw_name  = base_name+"straw"+str(i).zfill(3)
            straw_pos   = geom.structure.Position(straw_name+"_pos", running_x, running_y, Q('0m'))
            straw_place = geom.structure.Placement(straw_name+"_place", volume = straw_lv.name, pos = straw_pos.name)
            plane_lv.placements.append(straw_place.name) 

        self.nofStrawCurrentMod = Nstraw

        return plane_lv

    def constructStraw(self, geom, base_name, straw_half_length, gas):
        # straw 
        straw_name          = base_name+"_straw"
        straw_shape         = geom.shapes.Tubs(straw_name+"_shape", rmin=Q("0m"), rmax=self.StrawRadius + self.StrawPlug, dz=straw_half_length)
        straw_lv            = geom.structure.Volume(straw_name, material="Air35C", shape = straw_shape)

        # straw ring
        if(self.StrawPlug!=Q("0mm")):
            ring_name           = straw_name+"_ring"
            ring_shape          = geom.shapes.Tubs(ring_name+"_shape", rmin = self.StrawRadius, rmax = self.StrawRadius + self.StrawPlug, dz=straw_half_length)
            ring_lv             = geom.structure.Volume(ring_name, material="Air35C", shape = ring_shape)
            ring_pla            = geom.structure.Placement(ring_name+"_place", volume = ring_lv)

        # coat
        Alcoat_name         = straw_name+"_Alcoat"
        Alcoat_shape        = geom.shapes.Tubs(Alcoat_name+"_shape", rmin = self.StrawRadius - self.CoatThickness, rmax=self.StrawRadius, dz=straw_half_length)
        Alcoat_lv           = geom.structure.Volume(Alcoat_name, material="Aluminum", shape = Alcoat_shape)
        Alcoat_pla          = geom.structure.Placement(Alcoat_name+"_place", volume = Alcoat_lv)

        # mylar
        mylar_name          = straw_name+"_mylar"
        mylar_shape         = geom.shapes.Tubs(mylar_name+"_shape", rmin = self.StrawRadius - self.CoatThickness - self.MylarThickness, rmax = self.StrawRadius - self.CoatThickness, dz=straw_half_length)
        mylar_lv            = geom.structure.Volume(mylar_name, material="Mylar", shape = mylar_shape)
        mylar_pla           = geom.structure.Placement(mylar_name+"_place", volume = mylar_lv)

        # gas
        gas_name            = straw_name+"_"+gas
        gas_shape           = geom.shapes.Tubs(gas_name+"_shape", rmin = self.StrawWireRadius + self.StrawWireCoatThickness, rmax = self.StrawRadius - self.CoatThickness - self.MylarThickness, dz=straw_half_length)
        gas_lv              = geom.structure.Volume(gas_name, material=gas, shape = gas_shape)
        gas_pla             = geom.structure.Placement(gas_name+"_place", volume = gas_lv)
        gas_lv.params.append(("SensDet","Straw"))

        # wire coating
        wireCoat_name       = straw_name+"_wireCoating"
        wireCoat_shape      = geom.shapes.Tubs(wireCoat_name+"_shape", rmin = self.StrawWireRadius, rmax = self.StrawWireRadius + self.StrawWireCoatThickness, dz=straw_half_length)
        wireCoat_lv         = geom.structure.Volume(wireCoat_name, material="Tungsten", shape=wireCoat_shape)
        wireCoat_pla        = geom.structure.Placement(wireCoat_name+"_place", volume = wireCoat_lv)

        # wire
        wire_name           = straw_name+"_wire"
        wire_shape          = geom.shapes.Tubs(wire_name+"_shape", rmin = Q("0mm"), rmax = self.StrawWireRadius, dz=straw_half_length)
        wire_lv             = geom.structure.Volume(wire_name, material="Gold",shape=wire_shape)
        wire_pla            = geom.structure.Placement(wire_name+"_place", volume = wire_lv)


        if(self.StrawPlug!=Q("0mm")): straw_lv.placements.append(ring_pla.name)
        straw_lv.placements.append(Alcoat_pla.name)
        straw_lv.placements.append(mylar_pla.name)
        straw_lv.placements.append(gas_pla.name)
        straw_lv.placements.append(wireCoat_pla.name)
        straw_lv.placements.append(wire_pla.name)

        return straw_lv

        
        

