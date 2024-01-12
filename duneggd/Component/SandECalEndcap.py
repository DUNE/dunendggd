#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q

      
class SandECalEndcapBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
		  EndcapDim=None, 
          EndcapModDim=None,
		  ActiveMat=None, 
		  PasMat=None, 
		  PasSlabThickness=None, 
		  ActiveSlabThickness=None, 
		  nSlabs=None, 
          BackPlateThick=None,
		  **kwds):
        self.EndcapDim = EndcapDim
        self.EndcapModDim = EndcapModDim
        self.ActiveMat = ActiveMat
        self.PasMat = PasMat
        self.PasSlabThickness = PasSlabThickness
        self.ActiveSlabThickness = ActiveSlabThickness
        self.nSlabs = nSlabs
        self.BackPlateThick = BackPlateThick
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        
        rmax_ec = self.EndcapDim[0]
        KLOEEndcapECALDepth = self.EndcapDim[2]
        KLOEEndcapCurvRadius = self.EndcapDim[3]
        KLOEEndcapStraight = self.EndcapDim[4]
        KLOECellWidth = self.EndcapDim[5]
        KLOEEndcapModDy = self.EndcapModDim
        AlPlateThick = self.BackPlateThick
        ColPerMod = 6
        XPosMod = -3*KLOECellWidth
        ECTubsSize = KLOEEndcapECALDepth + KLOEEndcapCurvRadius + KLOEEndcapStraight

        ##########creating main straight part of the ECAL endcap module##########


        ECAL_endcap_shape = geom.shapes.Tubs('ECAL_endcap_shape',
                                        rmin=Q('0m'),
                                        rmax=rmax_ec,
                                        dz=ECTubsSize/2.)

        ECAL_endcap_lv = geom.structure.Volume('ECAL_endcap_lv', material='Air', shape=ECAL_endcap_shape)
        self.add_volume(ECAL_endcap_lv)
        
        ZPosMod = (-ECTubsSize+KLOEEndcapECALDepth)/2.

        for mod in range(0,16):
            print(("Building ECAL Endcap Module "+str(mod)))
            
            # width of the module
            if(mod > 1 and mod < 12):
                ColPerMod = 3
            elif (mod > 11):
                ColPerMod = 2
                
            # y position of the module
            if(mod < 2):
                YPosMod = Q('111.35cm')
            else:
                YPosMod = Q('0cm')

            # x position of the module
            if(mod == 2):
                XPosMod += KLOECellWidth*4.5
            elif(mod == 12):
                XPosMod += KLOECellWidth*2.5
            elif(mod > 0):
                XPosMod += KLOECellWidth*ColPerMod

            # create endcap module vertical part volume
            ECAL_ec_mod_vert_shape = geom.shapes.Box('ECAL_mod_'+str(mod)+'_shape',
                                     dx=KLOECellWidth*ColPerMod/2.,
                                     dy=KLOEEndcapModDy[mod],
                                     dz=0.5*(KLOEEndcapECALDepth + AlPlateThick))

            ECAL_ec_mod_vert_lv = geom.structure.Volume('ECAL_ec_mod_vert_'+str(mod)+'_lv', material='Air', shape=ECAL_ec_mod_vert_shape)

            # arrange the vertical part volume
            ECAL_ec_mod_vert_pos = geom.structure.Position(
                    'ECAL_ec_mod_vert_'+str(mod)+'_pos',
                    XPosMod, YPosMod, ZPosMod + 0.5*AlPlateThick)

            ECAL_ec_mod_vert_rot = geom.structure.Rotation('ECAL_ec_mod_vert_'+str(mod)+'_rot',
                                                Q('0deg'),Q('180deg'),Q('0deg'))

            ECAL_ec_mod_vert_pla = geom.structure.Placement(
                    'ECAL_ec_mod_vert_'+str(mod)+'_pla',
                    volume=ECAL_ec_mod_vert_lv,
                    pos=ECAL_ec_mod_vert_pos,
                    rot=ECAL_ec_mod_vert_rot) 

            ECAL_endcap_lv.placements.append(ECAL_ec_mod_vert_pla.name )

           ##########creating the Aluminium plate for the endcap modules##########

            ECAL_end_Alplate_shape = geom.shapes.Box('endECALAlplate_'+str(mod),
                                                     dx = KLOECellWidth*ColPerMod/2.,
                                                     dy = KLOEEndcapModDy[mod],
                                                     dz = AlPlateThick/2.)

            ECAL_end_Alplate_lv = geom.structure.Volume('endvolECALAlplate_'+str(mod),
                                                        material = 'Aluminum', shape = ECAL_end_Alplate_shape)

            ECAL_end_Alplate_pos = geom.structure.Position('endECALAlplatepos_'+str(mod),
                                                          Q('0.0cm'), Q('0.0cm'), 0.5*KLOEEndcapECALDepth)

            ECAL_end_Alplate_pla = geom.structure.Placement('endECALAlplatepla_'+str(mod),
                                                              volume = ECAL_end_Alplate_lv, pos = ECAL_end_Alplate_pos)

            ECAL_ec_mod_vert_lv.placements.append( ECAL_end_Alplate_pla.name)
 
            ###########################################

            for i in range(self.nSlabs): #nSlabs

                xposSlab=Q('0cm')
                yposSlab=Q('0cm')                  
          
                zposSlabActive =( -KLOEEndcapECALDepth * 0.5 + 
                             (i + 0.5) * self.ActiveSlabThickness +
                              i * self.PasSlabThickness )

                zposSlabPassive = (zposSlabActive + 
                               0.5 * self.ActiveSlabThickness +
                               0.5 * self.PasSlabThickness)

            ##########creating and appending active slabs to the ECAL endcap##########

                endECALActiveSlab = geom.shapes.Box(
                    'endECALActiveSlab_'+str(mod)+'_'+ str(i),
                    dx=KLOECellWidth*ColPerMod/2.,
                    dy=KLOEEndcapModDy[mod]     ,
                    dz=0.5 * self.ActiveSlabThickness)

                endECALActiveSlab_lv = geom.structure.Volume(
                    'endvolECALActiveSlab_' +str(mod)+ '_' + str(i),
                    material=self.ActiveMat,
                    shape=endECALActiveSlab)
                endECALActiveSlab_lv.params.append(("SensDet","EMCalSci"))

                endECALActiveSlabPos = geom.structure.Position(
                    'endecalactiveslabpos_' +str(mod)+ '_' + str(i),
                    xposSlab, yposSlab, zposSlabActive)

                endECALActiveSlabPlace = geom.structure.Placement(
                    'endecalactiveslabpla_' +str(mod)+ '_' + str(i),
                    volume=endECALActiveSlab_lv,
                    pos=endECALActiveSlabPos)

                ECAL_ec_mod_vert_lv.placements.append( endECALActiveSlabPlace.name )
            
                ##########creating and appending passive slabs to the ECAL endcap##########

                endECALPassiveSlab = geom.shapes.Box(
                    'endECALPassveSlab_' +str(mod)+ '_' + str(i),
                    dx=KLOECellWidth*ColPerMod/2.,
                    dy=KLOEEndcapModDy[mod]     ,
                    dz=0.5 * self.PasSlabThickness)

                endECALPassiveSlab_lv = geom.structure.Volume(
                    'endvolECALPassiveSlab_' +str(mod)+ '_' + str(i),
                    material=self.PasMat,
                    shape=endECALPassiveSlab)

                endECALPassiveSlabPos = geom.structure.Position(
                    'endecalpassiveslabpos_' +str(mod)+ '_' + str(i),
                    xposSlab, yposSlab, zposSlabPassive)

                endECALPassiveSlabPlace = geom.structure.Placement(
                    'endecalpassiveslabpla_' +str(mod)+ '_' + str(i),
                    volume=endECALPassiveSlab_lv,
                    pos=endECALPassiveSlabPos) 

                ECAL_ec_mod_vert_lv.placements.append( endECALPassiveSlabPlace.name )

           ##########creating and appending the curved part to the ECAL endcap##########

            ECAL_ec_mod_curv_shape = geom.shapes.Tubs('ECAL_ec_mod_curv_'+str(mod)+'_shape',
                                              rmin = KLOEEndcapCurvRadius - AlPlateThick,
                                              rmax = KLOEEndcapCurvRadius + KLOEEndcapECALDepth, 
                                              dz = KLOECellWidth*ColPerMod/2.,
                                              sphi = math.pi/2.,
                                              dphi = math.pi/2.)

            ECAL_ec_mod_curv_lv = geom.structure.Volume('ECAL_ec_mod_curv_'+str(mod)+'_lv', material='Air', shape=ECAL_ec_mod_curv_shape)

            Curv_y_pos = KLOEEndcapModDy[mod] + YPosMod
            Curv_z_pos = ZPosMod+KLOEEndcapECALDepth/2.+KLOEEndcapCurvRadius

            ECAL_ec_mod_curv_top_pos = geom.structure.Position(
                    'ECAL_ec_mod_curv_'+str(mod)+'_top_pos',
                    XPosMod, Curv_y_pos, Curv_z_pos)

            ECAL_ec_mod_curv_top_rot = geom.structure.Rotation('ECAL_ec_mod_curv_'+str(mod)+'_top_rot',
                                                Q('0deg'),Q('90deg'),Q('0deg'))

            ECAL_ec_mod_curv_top_pla = geom.structure.Placement(
                    'ECAL_ec_mod_curv_'+str(mod)+'_top_pla',
                    volume=ECAL_ec_mod_curv_lv,
                    pos=ECAL_ec_mod_curv_top_pos,
                    rot=ECAL_ec_mod_curv_top_rot) 

            ECAL_endcap_lv.placements.append(ECAL_ec_mod_curv_top_pla.name )
        
            if(mod < 2):
                Curv_y_bottom = -KLOEEndcapModDy[mod] + YPosMod
            else:
                Curv_y_bottom = -Curv_y_pos

            print(("Curv_y_bottom ="+str(Curv_y_bottom)))

            ECAL_ec_mod_curv_bot_pos = geom.structure.Position(
                    'ECAL_ec_mod_curv_'+str(mod)+'_bot_pos',
                    XPosMod, Curv_y_bottom, Curv_z_pos)

            ECAL_ec_mod_curv_bot_rot = geom.structure.Rotation('ECAL_ec_mod_curv_'+str(mod)+'_bot_rot',
                                                Q('90deg'),Q('90deg'),Q('0deg'))
 
            ECAL_ec_mod_curv_bot_pla = geom.structure.Placement(
                    'ECAL_ec_mod_curv_'+str(mod)+'_bot_pla',
                    volume=ECAL_ec_mod_curv_lv,
                    pos=ECAL_ec_mod_curv_bot_pos,
                    rot=ECAL_ec_mod_curv_bot_rot) 

            ECAL_endcap_lv.placements.append(ECAL_ec_mod_curv_bot_pla.name )
      
           ##########Aluminium plate for the endcap curved part##########

            ECAL_ec_mod_curv_Alplate_shape = geom.shapes.Tubs('ECAL_ec_mod_curv_Alplate_'+str(mod),
                                                           rmin = KLOEEndcapCurvRadius-AlPlateThick,
                                                           rmax = KLOEEndcapCurvRadius, 
                                                           dz = KLOECellWidth*ColPerMod/2.,
                                                           sphi = math.pi/2.,
                                                           dphi = math.pi/2.)

            ECAL_ec_mod_curv_Alplate_lv = geom.structure.Volume('ECAL_ec_mod_curv_Alplate_'+str(mod)+'_lv', 
                                                             material = 'Aluminum', shape = ECAL_ec_mod_curv_Alplate_shape)

            ECAL_ec_mod_curv_Alplate_pos = geom.structure.Position('ECAL_ec_mod_curv_Alplate_'+str(mod)+'_pos', 
                                                            Q('0.0cm'),Q('0.0cm'),Q('0.0cm'))

            ECAL_ec_mod_curv_Alplate_rot = geom.structure.Rotation('ECAL_ec_mod_curv_Alplate_'+str(mod)+'_rot',
                                                            Q('0deg'),Q('0deg'),Q('0deg'))

            ECAL_ec_mod_curv_Alplate_pla = geom.structure.Placement('ECAL_ec_mod_curv_Alplate_'+str(mod)+'_pla',
                                                                        volume = ECAL_ec_mod_curv_Alplate_lv, pos = ECAL_ec_mod_curv_Alplate_pos, 
                                                                        rot = ECAL_ec_mod_curv_Alplate_rot)

            ECAL_ec_mod_curv_lv.placements.append(ECAL_ec_mod_curv_Alplate_pla.name)

            ################

            for i in range(self.nSlabs): #nSlabs
            
                xposSlab=Q('0cm')
                yposSlab=Q('0cm')
                zposSlab=Q('0cm')
            
#                zposSlabActive =( -KLOEEndcapECALDepth * 0.5 + 
#                             (i + 0.5) * self.ActiveSlabThickness +
#                              i * self.PasSlabThickness )

                rminSlabActive =( KLOEEndcapCurvRadius+ 
                            i * self.ActiveSlabThickness +
                            i * self.PasSlabThickness )
                              
#                zposSlabPassive = (zposSlabActive + 
#                               0.5 * self.ActiveSlabThickness +
#                               0.5 * self.PasSlabThickness)

                rminSlabPassive = (rminSlabActive + 
                             self.ActiveSlabThickness)
# +
#                             self.PasSlabThickness )
                                          
        ##########creating and appending active slabs to the ECAL endcap##########

                endECALcurvActiveSlab = geom.shapes.Tubs(
                    'endECALcurvActiveSlab_'+str(mod)+ '_' + str(i),
                    rmin = rminSlabActive ,
                    rmax = rminSlabActive + self.ActiveSlabThickness,
                    dz= KLOECellWidth*ColPerMod/2.,
                    sphi = math.pi/2.,
                    dphi = math.pi/2.)            

                endECALcurvActiveSlab_lv = geom.structure.Volume(
                    'endvolECALcurvActiveSlab_' +str(mod)+ '_' + str(i),
                    material=self.ActiveMat,
                    shape=endECALcurvActiveSlab)
                endECALcurvActiveSlab_lv.params.append(("SensDet","EMCalSci"))

                endECALcurvActiveSlabPos = geom.structure.Position(
                    'endecalcurvactiveslabpos_' +str(mod)+ '_' + str(i),
                    xposSlab, yposSlab, zposSlab)

                endECALcurvActiveSlabPlace = geom.structure.Placement(
                    'endecalcurvactiveslabpla_' +str(mod)+ '_' + str(i),
                    volume=endECALcurvActiveSlab_lv,
                    pos=endECALcurvActiveSlabPos)

                ECAL_ec_mod_curv_lv.placements.append( endECALcurvActiveSlabPlace.name )
            
                ##########creating and appending passive slabs to the ECAL endcap##########

                endECALcurvPassiveSlab = geom.shapes.Tubs(
                    'endECALcurvPassiveSlab_' +str(mod)+ '_' + str(i),
                    rmin = rminSlabPassive,
                    rmax = rminSlabPassive+ self.PasSlabThickness,
                    dz= KLOECellWidth*ColPerMod/2.,
                    sphi = math.pi/2,
                    dphi = math.pi/2.)

                endECALcurvPassiveSlab_lv = geom.structure.Volume(
                    'endvolECALcurvPassiveSlab_' +str(mod)+ '_' + str(i),
                    material=self.PasMat,
                    shape=endECALcurvPassiveSlab)

                endECALcurvPassiveSlabPos = geom.structure.Position(
                    'endecalcurvpassiveslabpos_' +str(mod)+ '_' + str(i),
                    xposSlab, yposSlab, zposSlab)

                endECALcurvPassiveSlabPlace = geom.structure.Placement(
                    'endecalcurvpassiveslabpla_' +str(mod)+ '_' + str(i),
                    volume=endECALcurvPassiveSlab_lv,
                    pos=endECALcurvPassiveSlabPos) 

                ECAL_ec_mod_curv_lv.placements.append( endECALcurvPassiveSlabPlace.name )
 
            ##########creating and appending the short strtaight part to the ECAL endcap##########

            ECAL_ec_mod_hor_shape = geom.shapes.Box('ECAL_ec_mod_hor_'+str(mod)+'_shape',
                                     dx=KLOECellWidth*ColPerMod/2.,
                                     dy=KLOEEndcapStraight/2.,
                                     dz=0.5*(KLOEEndcapECALDepth + AlPlateThick))

            ECAL_ec_mod_hor_lv = geom.structure.Volume('ECAL_ec_mod_hor_'+str(mod)+'_lv', material='Air', shape=ECAL_ec_mod_hor_shape)

            Straight_y_pos = Curv_y_pos + KLOEEndcapCurvRadius + 0.5*(KLOEEndcapECALDepth - AlPlateThick)
            Straight_z_pos = Curv_z_pos + KLOEEndcapStraight/2.

            ECAL_ec_mod_hor_top_pos = geom.structure.Position('ECAL_ec_mod_hor_'+str(mod)+'_top_pos',
                                                    XPosMod,
						                            Straight_y_pos,
                                                    Straight_z_pos)

            ECAL_ec_mod_hor_top_rot = geom.structure.Rotation('ECAL_ec_mod_hor_'+str(mod)+'_top_rot',
                                                Q('90deg'),Q('0deg'),Q('0deg'))

            ECAL_ec_mod_hor_top_pla = geom.structure.Placement(
                     'ECAL_ec_mod_hor_'+str(mod)+'_top_pla',
                    volume=ECAL_ec_mod_hor_lv,
                    pos=ECAL_ec_mod_hor_top_pos,
                    rot=ECAL_ec_mod_hor_top_rot) 

            ECAL_endcap_lv.placements.append(ECAL_ec_mod_hor_top_pla.name )

            if(mod > 1):
                ECAL_ec_mod_hor_bot_pos = geom.structure.Position('ECAL_ec_mod_hor_'+str(mod)+'_bot_pos',
                                                    XPosMod,
						                            -Straight_y_pos,
                                                    Straight_z_pos)

                ECAL_ec_mod_hor_bot_rot = geom.structure.Rotation('ECAL_ec_mod_hor_'+str(mod)+'_bot_rot',
                                                Q('-90deg'),Q('0deg'),Q('0deg'))

                ECAL_ec_mod_hor_bot_pla = geom.structure.Placement(
                     'ECAL_ec_mod_hor_'+str(mod)+'_bot_pla',
                    volume=ECAL_ec_mod_hor_lv,
                    pos=ECAL_ec_mod_hor_bot_pos,
                    rot=ECAL_ec_mod_hor_bot_rot) 

                ECAL_endcap_lv.placements.append(ECAL_ec_mod_hor_bot_pla.name )

             ##########Aluminium plate for the endcap short straight part##########

            ECAL_ec_mod_hor_Alplate_shape = geom.shapes.Box(
                'ECAL_ec_mod_hor_Alplate_'+str(mod)+'_shape', 
                dx = KLOECellWidth*ColPerMod/2., dy=KLOEEndcapStraight/2., 
                dz = AlPlateThick/2.)

            ECAL_ec_mod_hor_Alplate_lv = geom.structure.Volume(
                'ECAL_ec_mod_hor_Alplate_'+str(mod)+'_lv', 
                material = 'Aluminum', shape = ECAL_ec_mod_hor_Alplate_shape)

            ECAL_ec_mod_hor_Alplate_pos = geom.structure.Position(
                'ECAL_ec_mod_hor_Alplate_'+str(mod)+'_pos', 
                XPosMod, 0.5*KLOEEndcapECALDepth, Straight_z_pos)

            ECAL_ec_mod_hor_Alplate_rot = geom.structure.Rotation(
                'ECAL_ec_mod_hor_Alplate_'+str(mod)+'_rot',
                 Q('90deg'),Q('0deg'),Q('0deg'))

            ECAL_ec_mod_hor_Alplate_pla = geom.structure.Placement(
                'ECAL_ec_mod_hor_Alplate_'+str(mod)+'_pla',
                volume = ECAL_ec_mod_hor_Alplate_lv, 
                pos = ECAL_ec_mod_hor_Alplate_pos, 
                rot = ECAL_ec_mod_hor_Alplate_rot)

            ECAL_endcap_lv.placements.append(ECAL_ec_mod_hor_Alplate_pla.name)
               
           ###########

            for i in range(self.nSlabs): #nSlabs
            
                xposSlab=Q('0cm')
                yposSlab=Q('0cm')

                zposSlabActive =( -KLOEEndcapECALDepth * 0.5 + 
                             (i + 0.5) * self.ActiveSlabThickness +
                              i * self.PasSlabThickness )

                zposSlabPassive = (zposSlabActive + 
                               0.5 * self.ActiveSlabThickness +
                               0.5 * self.PasSlabThickness)

                ##########creating and appending active slabs to the ECAL endcap##########

                endECALstraightActiveSlab = geom.shapes.Box(
                    'endECALstraightActiveSlab_'+str(mod)+ '_' + str(i),
                    dx=KLOECellWidth*ColPerMod/2.,
                    dy=KLOEEndcapStraight/2.,
                    dz=0.5 * self.ActiveSlabThickness)

                endECALstraightActiveSlab_lv = geom.structure.Volume(
                    'endvolECALstraightActiveSlab_' +str(mod)+ '_' + str(i),
                    material=self.ActiveMat,
                    shape=endECALstraightActiveSlab)
                endECALstraightActiveSlab_lv.params.append(("SensDet","EMCalSci"))

                endECALstraightActiveSlabPos = geom.structure.Position(
                    'endecalstraightactiveslabpos_' +str(mod)+ '_' + str(i),
                    xposSlab, yposSlab, zposSlabActive)
            
                endECALstraightActiveSlabPlace = geom.structure.Placement(
                    'endecalstraightactiveslabpla_' +str(mod)+ '_' + str(i),
                    volume=endECALstraightActiveSlab_lv,
                    pos=endECALstraightActiveSlabPos)

                ECAL_ec_mod_hor_lv.placements.append( endECALstraightActiveSlabPlace.name )
            
                ##########creating and appending passive slabs to the ECAL endcap##########

                endECALstraightPassiveSlab = geom.shapes.Box(
                    'endECALstraightPassveSlab_' +str(mod)+ '_' + str(i),
                    dx=KLOECellWidth*ColPerMod/2.,
                    dy=KLOEEndcapStraight/2.,
                    dz=0.5 * self.PasSlabThickness)

                endECALstraightPassiveSlab_lv = geom.structure.Volume(
                    'endvolECALstraightPassiveSlab_' +str(mod)+ '_' + str(i),
                    material=self.PasMat,
                    shape=endECALstraightPassiveSlab)

                endECALstraightPassiveSlabPos = geom.structure.Position(
                    'endecalstraightpassiveslabpos_' +str(mod)+ '_' + str(i),
                    xposSlab, yposSlab, zposSlabPassive)

                endECALstraightPassiveSlabPlace = geom.structure.Placement(
                    'endecalstraightpassiveslabpla_' +str(mod)+ '_' + str(i),
                    volume=endECALstraightPassiveSlab_lv,
                    pos=endECALstraightPassiveSlabPos) 

                ECAL_ec_mod_hor_lv.placements.append( endECALstraightPassiveSlabPlace.name )

