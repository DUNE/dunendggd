import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class GrainBuilder(gegede.builder.Builder):
    def configure( self, configuration=None, **kwds):

        self.configuration       = configuration
        
        if self.configuration == "option_1":

            ######################################### EXTERNAL VESSEL (endcap steel 12 mm)
            #               Carbon_fiber 12 mm                                  
            ######################################### END EXTERNAL VESSEL
            #               vacuum gap                                          
            ######################################### INTERNAL VESSEL (endcap aluminum 12 mm)
            #               Aluminum 12 mm 
            ######################################### END IINTERNAL VESSEL

            self.Carbon_fiberThickness   = Q("12mm")                                    # two layers of 6 mm for a total of 12
            self.AluminumThickness   = Q("12mm")
            self.EndcapThickness     = Q("16mm")
        
            self.ExternalVesselX     = Q("297.5mm") + self.Carbon_fiberThickness        # minor semiaxis of external vessel
            self.ExternalVesselY     = Q("788mm")   + self.Carbon_fiberThickness        # major semiaxis of external vessel
            self.ExternalVesselZ     = Q("816mm")   + self.EndcapThickness              # half lenght of external vessel
        
            self.InternalVesselX     = Q("237.5mm") + self.AluminumThickness            # minor semiaxis of internal vessel
            self.InternalVesselY     = Q("728mm")   + self.AluminumThickness            # major semiaxis of internal vessel
            self.InternalVesselZ     = Q("600mm")   + self.EndcapThickness              # half lenght of internal vessel
        
            self.UpstreamVesselGap   = Q("30mm")                                        # margin between kloe vessel and the LAr target
            #self.MinDistExtVesTrMod  = Q("50mm")                                       # margin between LAr target and upstream traking module
            self.InterVesselHalfGap  = Q('30mm')


        elif self.configuration == "option_2":

            #########################################  EXTERNAL VESSEL (endcap steel 12 mm)
            #              Carbon_fiber 6 mm                                     
            #########################################
            #              honeycomb (vacuum) 50 mm     -----------> shal we put honeycomb? It is in the tool file
            #########################################
            #              Carbon_fiber 6 mm
            #########################################  END EXTERNAL VESSEL
            #              vacuum gap 
            #########################################  INTERNAL VESSEL (endcap aluminum 12 mm)
            #              aluminum 12 mm
            #########################################
            #                  LAr     
            #########################################  END INTERNAL VESSEL

            self.HoneycombThickness  = Q("50mm")
            self.Carbon_fiberThickness   = Q("6mm") #two layers of 6 mm for a total of 12
            self.AluminumThickness   = Q("12mm")
            self.EndcapThickness     = Q("16mm")
        
            self.ExternalVesselX     = Q("365mm")   + self.HoneycombThickness + self.Carbon_fiberThickness*2 # minor semiaxis of external vessel
            self.ExternalVesselY     = Q("900mm")   + self.HoneycombThickness + self.Carbon_fiberThickness*2 # major semiaxis of external vessel
            self.ExternalVesselZ     = Q("950mm")   + self.EndcapThickness                                   # half lenght of external vessel
        
            self.InternalVesselX     = Q("237.5mm") + self.AluminumThickness                                 # minor semiaxis of internal vessel
            self.InternalVesselY     = Q("728mm")   + self.AluminumThickness                                 # major semiaxis of internal vessel
            self.InternalVesselZ     = Q("650mm")   + self.EndcapThickness                                   # half lenght of internal vessel
        
            self.UpstreamVesselGap   = Q("30mm") #margin between kloe vessel and the LAr target
            #self.MinDistExtVesTrMod  = Q("50mm") #margin between LAr target and upstream traking module
            #self.InterVesselHalfGap  = Q('30mm')
            

    #def construct(self,geom):
        # whole_shape=geom.shapes.PolyhedraRegular("whole_shape_for_grain",numsides=self.nBarrelModules, rmin=Q('0cm'), rmax=self.kloeVesselRadius , dz=self.kloeVesselHalfDx, sphi=self.rotAngle)
        # upstream_shape=geom.shapes.Box("upstream_shape_for_grain", dx=0.5*self.liqArThickness, dy=self.kloeVesselRadius, dz=self.kloeVesselHalfDx )
        # upstream_shape_pos = geom.structure.Position("upstream_shape_pos_for_grain", 0.5*self.liqArThickness, Q('0m'), Q('0m'))
        # grain_shape = geom.shapes.Boolean("grain_shape",
        #                                  type='intersection',
        #                                  first=whole_shape,
        #                                  second=upstream_shape,
        #                                  rot='r180aboutY',
        #                                  pos=upstream_shape_pos)

        # main_lv = geom.structure.Volume('Grain_envelope',   material=self.Material, shape=grain_shape)
        #self.construct_GRAIN(geom, main_lv)
    def construct(self, geom):
        if self.configuration == "option_1":
            main_lv = self.construct_GRAIN_option1(geom)
        elif self.configuration == "option_2":
            main_lv = self.construct_GRAIN_option2(geom)

        #main_lv = self.construct_GRAIN(geom)
        print(( "  main_lv = "+ main_lv.name))
        self.add_volume( main_lv )

#############################################################         GRAIN   1      ###################################################################

    def construct_GRAIN_option1(self, geom):
        
        print("-------------------------------------------")
        print("BUILDING GRAIN OPTION 1")
        print("-------------------------------------------")

        GRAIN_shape = geom.shapes.EllipticalTube("GRAIN_shape", 
                                                dx = self.ExternalVesselX, 
                                                dy = self.ExternalVesselY, 
                                                dz = self.ExternalVesselZ)

        GRAIN_lv = geom.structure.Volume("GRAIN_lv",  
                                        material = "Air",    
                                        shape = GRAIN_shape)

        # build the external vessel envelop 
        
        GRAIN_Ext_vessel_shape = geom.shapes.EllipticalTube("GRAIN_Ext_vessel_shape", 
                                                      dx = self.ExternalVesselX, 
                                                      dy = self.ExternalVesselY, 
                                                      dz = self.ExternalVesselZ - self.EndcapThickness)

        GRAIN_Ext_vessel_lv = geom.structure.Volume("GRAIN_Ext_vessel_lv", 
                                              material = "Carbon_fiber", 
                                              shape = GRAIN_Ext_vessel_shape)

        GRAIN_Ext_vessel_lv_pla = geom.structure.Placement("GRAIN_Ext_vessel_lv_pla",
                                                                  volume = GRAIN_Ext_vessel_lv)
        
        
        GRAIN_lv.placements.append(GRAIN_Ext_vessel_lv_pla.name) 


        # build the layer of vacuum between the two vessels

        GRAIN_gap_between_vessels_shape  = geom.shapes.EllipticalTube("GRAIN_gap_between_vessels_shape", 
                                                                       dx = self.ExternalVesselX - self.Carbon_fiberThickness, 
                                                                       dy = self.ExternalVesselY - self.Carbon_fiberThickness, 
                                                                       dz = self.ExternalVesselZ - self.EndcapThickness) 
                                                            
                                                            
        GRAIN_gap_between_vessels_lv = geom.structure.Volume("GRAIN_gap_between_vessels_lv", 
                                                              material = "Vacuum_cryo", 
                                                              shape = GRAIN_gap_between_vessels_shape)
                                                                    
        
        GRAIN_gap_between_vessels_pla = geom.structure.Placement("GRAIN_gap_between_vessels_pla",
                                                                  volume = GRAIN_gap_between_vessels_lv)
        
        
        GRAIN_Ext_vessel_lv.placements.append(GRAIN_gap_between_vessels_pla.name)  

        
        # build the layer of aluminum of the inner vessel
        
        GRAIN_Int_vessel_shape = geom.shapes.EllipticalTube("GRAIN_Int_vessel_shape", 
                                                      dx = self.InternalVesselX, 
                                                      dy = self.InternalVesselY, 
                                                      dz = self.InternalVesselZ)

        GRAIN_Int_vessel_lv = geom.structure.Volume("GRAIN_Int_vessel_lv", 
                                              material = "Aluminum", 
                                              shape = GRAIN_Int_vessel_shape)

        
        GRAIN_Int_vessel_pla = geom.structure.Placement("GRAIN_Int_vessel_pla",
                                                  volume = GRAIN_Int_vessel_lv)
                                               
        GRAIN_gap_between_vessels_lv.placements.append(GRAIN_Int_vessel_pla.name)

        
        # build the inner volume of LAr
        
        GRAIN_LAr_shape = geom.shapes.EllipticalTube("GRAIN_LAr_shape", 
                                                      dx = self.InternalVesselX - self.AluminumThickness, 
                                                      dy = self.InternalVesselY - self.AluminumThickness, 
                                                      dz = self.InternalVesselZ - self.EndcapThickness)

        GRAIN_LAr_lv = geom.structure.Volume("GRAIN_LAr_lv", 
                                              material = "LAr", 
                                              shape = GRAIN_LAr_shape)
                                              
        GRAIN_LAr_lv.params.append(("SensDet", 'LArHit'))
                                                                    
        
        GRAIN_LAr_pla = geom.structure.Placement("GRAIN_LAr_pla",
                                                  volume = GRAIN_LAr_lv)
                                               
        GRAIN_Int_vessel_lv.placements.append(GRAIN_LAr_pla.name)

        
        # build external vessel endcaps

        # LEFT
        
        GRAIN_GRAIN_EndCap_ExtVessel_shape = geom.shapes.EllipticalTube("GRAIN_GRAIN_EndCap_ExtVessel_shape", 
                                                            dx = self.ExternalVesselX, 
                                                            dy = self.ExternalVesselY, 
                                                            dz = self.EndcapThickness/2)
                                         
        GRAIN_EndCapLeft_ExtVessel_lv = geom.structure.Volume("GRAIN_EndCapLeft_ExtVessel_lv", 
                                                      material = "Steel", 
                                                      shape = GRAIN_GRAIN_EndCap_ExtVessel_shape)
                                          
        GRAIN_EndCapLeft_ExtVessel_pos = geom.structure.Position("GRAIN_EndCapLeft_ExtVessel_pos",
                                                        Q("0mm"),#- self.kloeVesselRadius + self.UpstreamVesselGap + self.ExternalVesselX,
                                                        Q("0mm"),
                                                        - self.ExternalVesselZ +  self.EndcapThickness/2)
                                      
        GRAIN_EndCapLeft_ExtVessel_pla = geom.structure.Placement("GRAIN_EndCapLeft_ExtVessel_pla",
                                                          volume = GRAIN_EndCapLeft_ExtVessel_lv,
                                                          pos = GRAIN_EndCapLeft_ExtVessel_pos)
        
        GRAIN_lv.placements.append(GRAIN_EndCapLeft_ExtVessel_pla.name)

        # RIGHT
        
        GRAIN_EndCapRight_ExtVessel_lv = geom.structure.Volume("GRAIN_EndCapRight_ExtVessel_lv", 
                                                      material = "Steel", 
                                                      shape = GRAIN_GRAIN_EndCap_ExtVessel_shape)
        
        GRAIN_EndCapRight_ExtVessel_pos = geom.structure.Position("GRAIN_EndCapRight_ExtVessel_pos",
                                                        Q("0mm"),#- self.kloeVesselRadius + self.UpstreamVesselGap + self.ExternalVesselX,
                                                        Q("0mm"),
                                                        + self.ExternalVesselZ - self.EndcapThickness/2)
                                      
        GRAIN_EndCapRight_ExtVessel_pla = geom.structure.Placement("GRAIN_EndCapRight_ExtVessel_pla",
                                                         volume = GRAIN_EndCapRight_ExtVessel_lv,
                                                         pos = GRAIN_EndCapRight_ExtVessel_pos)        
        
        GRAIN_lv.placements.append(GRAIN_EndCapRight_ExtVessel_pla.name)
        

        return GRAIN_lv


        #return self.construct_GRAIN_option2(geom)

##############################################################        END GRAIN    1    #################################################################        


##############################################################         GRAIN   2      ###################################################################
    
    
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    #def construct_GRAIN(self, geom, main_lv):
    def construct_GRAIN_option2(self, geom):

        print("-------------------------------------------")
        print("BUILDING GRAIN OPTION 2")
        print("-------------------------------------------")

        GRAIN_shape = geom.shapes.EllipticalTube("GRAIN_shape", 
                                                dx = self.ExternalVesselX, 
                                                dy = self.ExternalVesselY, 
                                                dz = self.ExternalVesselZ)

        GRAIN_lv = geom.structure.Volume("GRAIN_lv",  
                                        material = "Air",    
                                        shape = GRAIN_shape)
        
    
        # build the external vessel envelop 
        
        GRAIN_Ext_vessel_outer_layer_shape = geom.shapes.EllipticalTube("GRAIN_Ext_vessel_outer_layer_shape", 
                                                                            dx = self.ExternalVesselX, 
                                                                            dy = self.ExternalVesselY, 
                                                                            dz = self.ExternalVesselZ)# - self.EndcapThickness)

        GRAIN_Ext_vessel_outer_layer_lv = geom.structure.Volume("GRAIN_Ext_vessel_outer_layer_lv", 
                                                                    material = "Carbon_fiber", 
                                                                    shape = GRAIN_Ext_vessel_outer_layer_shape)

        GRAIN_Ext_vessel_outer_layer_pla = geom.structure.Placement("GRAIN_Ext_vessel_outer_layer_pla",
                                                                volume = GRAIN_Ext_vessel_outer_layer_lv)     

        GRAIN_lv.placements.append(GRAIN_Ext_vessel_outer_layer_pla.name)                                                                                                                                           
                                                        
        
        # build the layer of vacuum (in the real geometry honeycomb)
        
        GRAIN_Honeycomb_layer_shape  = geom.shapes.EllipticalTube("GRAIN_Honeycomb_layer_shape", 
                                                                  dx = self.ExternalVesselX - self.Carbon_fiberThickness, 
                                                                  dy = self.ExternalVesselY - self.Carbon_fiberThickness, 
                                                                  dz = self.ExternalVesselZ - self.Carbon_fiberThickness) 
                                                            
                                                            
        GRAIN_Honeycomb_layer_lv = geom.structure.Volume("GRAIN_Honeycomb_layer_lv", 
                                                          material = "Vacuum_cryo", 
                                                          shape = GRAIN_Honeycomb_layer_shape)
                                                                    
        
        GRAIN_Honeycomb_layer_pla = geom.structure.Placement("GRAIN_Honeycomb_layer_pla",
                                                                volume = GRAIN_Honeycomb_layer_lv)
        
        
        GRAIN_Ext_vessel_outer_layer_lv.placements.append(GRAIN_Honeycomb_layer_pla.name)
        
        
        # build the inner layer of Carbon_fiber of the external vessel
        
        GRAIN_Ext_vessel_inner_layer_shape = geom.shapes.EllipticalTube("GRAIN_Ext_vessel_inner_layer_shape", 
                                                                            dx = self.ExternalVesselX - self.Carbon_fiberThickness - self.HoneycombThickness, 
                                                                            dy = self.ExternalVesselY - self.Carbon_fiberThickness - self.HoneycombThickness, 
                                                                            dz = self.ExternalVesselZ - self.Carbon_fiberThickness - self.HoneycombThickness)

        GRAIN_Ext_vessel_inner_layer_lv = geom.structure.Volume("GRAIN_Ext_vessel_inner_layer_lv", 
                                                                    material = "Carbon_fiber", 
                                                                    shape = GRAIN_Ext_vessel_inner_layer_shape)
                                                                    
                                                                    
        GRAIN_Ext_vessel_inner_layer_pla = geom.structure.Placement("GRAIN_Ext_vessel_inner_layer_pla",
                                                                       volume = GRAIN_Ext_vessel_inner_layer_lv)
                                               
        
        GRAIN_Honeycomb_layer_lv.placements.append(GRAIN_Ext_vessel_inner_layer_pla.name)
        
        
        # build the layer of vacuum between the two vessels
        
        GRAIN_gap_between_vessels_shape  = geom.shapes.EllipticalTube("GRAIN_gap_between_vessels_shape", 
                                                                       dx = self.ExternalVesselX - self.Carbon_fiberThickness*2 - self.HoneycombThickness, 
                                                                       dy = self.ExternalVesselY - self.Carbon_fiberThickness*2 - self.HoneycombThickness, 
                                                                       dz = self.ExternalVesselZ - self.Carbon_fiberThickness*2 - self.HoneycombThickness) 
                                                            
                                                            
        GRAIN_gap_between_vessels_lv = geom.structure.Volume("GRAIN_gap_between_vessels_lv", 
                                                              material = "Vacuum_cryo", 
                                                              shape = GRAIN_gap_between_vessels_shape)
                                                                    
        
        GRAIN_gap_between_vessels_pla = geom.structure.Placement("GRAIN_gap_between_vessels_pla",
                                                                  volume = GRAIN_gap_between_vessels_lv)
        
        
        GRAIN_Ext_vessel_inner_layer_lv.placements.append(GRAIN_gap_between_vessels_pla.name)
        
        
        # build the layer of aluminum of the inner vessel
        
        GRAIN_inner_vessel_shape = geom.shapes.EllipticalTube("GRAIN_inner_vessel_shape", 
                                                                       dx = self.InternalVesselX, 
                                                                       dy = self.InternalVesselY, 
                                                                       dz = self.InternalVesselZ)

        GRAIN_inner_vessel_lv = geom.structure.Volume("GRAIN_inner_vessel_lv", 
                                                                material = "Aluminum", 
                                                                shape = GRAIN_inner_vessel_shape)

        
        GRAIN_inner_vessel_pla = geom.structure.Placement("GRAIN_inner_vessel_pla",
                                                                   volume = GRAIN_inner_vessel_lv)
                                               
        GRAIN_gap_between_vessels_lv.placements.append(GRAIN_inner_vessel_pla.name)
        
        
        # build the inner volume of LAr
        
        GRAIN_LAr_shape = geom.shapes.EllipticalTube("GRAIN_LAr_shape", 
                                                      dx = self.InternalVesselX - self.AluminumThickness, 
                                                      dy = self.InternalVesselY - self.AluminumThickness, 
                                                      dz = self.InternalVesselZ - self.EndcapThickness)

        GRAIN_LAr_lv = geom.structure.Volume("GRAIN_LAr_lv", 
                                              material = "LAr", 
                                              shape = GRAIN_LAr_shape)
                                              
        GRAIN_LAr_lv.params.append(("SensDet", 'LArHit'))
                                                                    
        
        GRAIN_LAr_pla = geom.structure.Placement("GRAIN_LAr_pla",
                                                  volume = GRAIN_LAr_lv)
                                               
        GRAIN_inner_vessel_lv.placements.append(GRAIN_LAr_pla.name)
        
        """
        # build external vessel endcaps
        
        GRAIN_EndCap_ExtVessel_shape = geom.shapes.EllipticalTube("GRAIN_EndCap_ExtVessel_shape", 
                                                            dx = self.ExternalVesselX, 
                                                            dy = self.ExternalVesselY, 
                                                            dz = self.EndcapThickness/2)
                                         
        GRAIN_EndCapLeft_ExtVessel_lv = geom.structure.Volume("GRAIN_EndCapLeft_ExtVessel_lv", 
                                                      material = "Steel", 
                                                      shape = GRAIN_EndCap_ExtVessel_shape)
                                          
        GRAIN_EndCapLeft_ExtVessel_pos = geom.structure.Position("GRAIN_EndCapLeft_ExtVessel_pos",
                                                        Q("0mm"),#- self.kloeVesselRadius + self.UpstreamVesselGap + self.ExternalVesselX,
                                                        Q("0mm"),
                                                        - self.ExternalVesselZ +  self.EndcapThickness/2)
                                      
        GRAIN_EndCapLeft_ExtVessel_pla = geom.structure.Placement("GRAIN_EndCapLeft_ExtVessel_pla",
                                                          volume = GRAIN_EndCapLeft_ExtVessel_lv,
                                                          pos = GRAIN_EndCapLeft_ExtVessel_pos)
        
        GRAIN_lv.placements.append(GRAIN_EndCapLeft_ExtVessel_pla.name)
        
        
        GRAIN_EndCapRight_ExtVessel_lv = geom.structure.Volume("GRAIN_EndCapRight_ExtVessel_lv", 
                                                      material = "Steel", 
                                                      shape = GRAIN_EndCap_ExtVessel_shape)
        
        GRAIN_EndCapRight_ExtVessel_pos = geom.structure.Position("GRAIN_EndCapRight_ExtVessel_pos",
                                                        Q("0mm"),#- self.kloeVesselRadius + self.UpstreamVesselGap + self.ExternalVesselX,
                                                        Q("0mm"),
                                                        + self.ExternalVesselZ - self.EndcapThickness/2)
                                      
        GRAIN_EndCapRight_ExtVessel_pla = geom.structure.Placement("GRAIN_EndCapRight_ExtVessel_pla",
                                                         volume = GRAIN_EndCapRight_ExtVessel_lv,
                                                         pos = GRAIN_EndCapRight_ExtVessel_pos)        
        
        GRAIN_lv.placements.append(GRAIN_EndCapRight_ExtVessel_pla.name)
        """
        
        return GRAIN_lv
        
        
    
##############################################################        END GRAIN    2     ################################################################
