#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
import math
from gegede import Quantity as Q
import time as tm

class STTFULLBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, **kwds ):
        sqrt3                    = 1.7320508
        self.halfDimension, self.Material = ( halfDimension, Material )
        
        # ST
        self.strawRadius         = Q('2.5mm')
        self.coatThickness       = Q("100nm")
        self.mylarThickness      = Q("20um")
        self.strawWireWThickness = Q('20um')
        self.strawWireGThickness = Q('20nm')
        
        # XY STT planes
        self.planeXXThickness    = self.strawRadius * (2 + sqrt3)
        
        # STT MODULE 
        self.nfoil               = 150
        self.foilThickness       = Q("15um")
        self.foilGap             = Q("120um")
        self.totFoilsThickness   = self.nfoil * self.foilThickness + (self.nfoil-1)*self.foilGap
        self.slabThickness       = Q("5.3mm")
        self.graphiteThickness   = Q("4mm")
        
        # STT
        self.kloeVesselHalfDx    = Q('1.69m')
        self.kloeVesselRadius    = Q('2m')
        self.extLateralgap       = Q("0cm")
        self.extRadialgap        = Q("0cm")
        self.kloeTrkRegRadius    = self.kloeVesselRadius - self.extRadialgap
        self.kloeTrkRegHalfDx    = self.kloeVesselHalfDx - self.extLateralgap
        self.nMod_NoSlab         = 5
        self.nMod_C3H6           = 78
        self.nMod_C              = 7
        self.nMod_Tot            = self.nMod_NoSlab + self.nMod_C3H6 + self.nMod_C
        self.nFrontST            = 2
        self.nFrontC3H6          = 3
        self.NoSlabModThickness  = self.planeXXThickness * 2 + self.totFoilsThickness
        self.C3H6ModThickness    = self.planeXXThickness * 2 + self.totFoilsThickness + self.slabThickness
        self.CModThickness       = self.planeXXThickness * 2 + self.graphiteThickness
        
        # LAr target
        self.LArThickness        = Q("20cm") - 4*self.planeXXThickness
        self.LArBoxThickness     = Q("1mm")
        
        pass

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct STT 
    def construct(self,geom):
        start_time=tm.time()
                
        main_lv, main_hDim = ltools.main_lv( self, geom, "Tubs")
        print( "KLOESTTFULL::construct()")
        print(( "  main_lv = "+ main_lv.name))
        self.add_volume( main_lv )
        
        # LAr target
        LAr_tgt_lv = self.construct_LAr_target(geom)
        LAr_tgt_pla = geom.structure.Placement("LAr_tgt_pla",volume=LAr_tgt_lv)
        main_lv.placements.append(LAr_tgt_pla.name)
        
        # 2 XY module after LAr target
        currentXPos = -self.kloeTrkRegRadius + self.LArThickness
        cos = 0.0
        halfHeight = 0.0
        
        for imod in range(self.nFrontST):
            currentXPos += imod * 2 * self.planeXXThickness
            cos = currentXPos / self.kloeTrkRegRadius
            halfHeight = self.kloeTrkRegRadius*math.sqrt(1 - cos*cos)
            name = "frontST"+str(imod)

            frontST_lv = self.construct_XYSTPlane(geom, name+"_vol", halfHeight, self.kloeTrkRegHalfDx, "stGas_Ar19")                                  
            frontST_pos = geom.structure.Position(name + "_pos", currentXPos + self.planeXXThickness, Q('0cm'), Q('0cm'))
            frontST_pla = geom.structure.Placement(name + "_pla",volume=frontST_lv,pos=frontST_pos)
            main_lv.placements.append(frontST_pla.name)           

        currentXPos += 2 * self.planeXXThickness
        
        modBuilder = {'C3H6Mod': self.construct_C3H6_Module, 'NoSlabMod': self.construct_NoSlab_Module, 'CMod': self.construct_C_Module}

        for imod in range(self.nMod_Tot):
            name = "sttmod" + str(imod)
            
            if((imod - 3) % 13 == 0):
                modThickness = self.CModThickness    
                modType = 2
                construct_mod = modBuilder['CMod']
            elif(imod > 84):
                modThickness = self.NoSlabModThickness    
                modType = 3
                construct_mod = modBuilder['NoSlabMod']
            else:
                modThickness = self.C3H6ModThickness    
                modType = 1
                construct_mod = modBuilder['C3H6Mod']
            
            if(currentXPos + 0.5 * modThickness) < 0.0:
                cos = currentXPos/self.kloeTrkRegRadius
            else:
                cos = (currentXPos + modThickness)/self.kloeTrkRegRadius
                    
            halfHeight = self.kloeTrkRegRadius*math.sqrt(1 - cos*cos)
            halfDimension = {'dx': modThickness/2.0, 'dy':halfHeight, 'dz': self.kloeTrkRegHalfDx}
                
            mod_lv = construct_mod(geom, name, halfDimension)
            mod_pos = geom.structure.Position(name + "_pos", currentXPos + 0.5*modThickness, Q('0cm'), Q('0cm'))
            mod_pla = geom.structure.Placement(name + "_pla",volume=mod_lv,pos=mod_pos)
            main_lv.placements.append(mod_pla.name) 
            
            currentXPos += modThickness
            
        end_time=tm.time()
        elapsed_time = end_time-start_time
        print(("elapsed time:" + str(elapsed_time)))

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct LAr target
    def construct_LAr_target(self,geom):
        tub_env_shape = geom.shapes.Tubs("LAr_tube_env_shape", 
                                         rmin=Q("0m"), 
                                         rmax=self.kloeVesselRadius, 
                                         dz=self.kloeTrkRegHalfDx)
                                      
        box_env_shape = geom.shapes.Box("LAr_box_env_shape", 
                                        dx=self.kloeVesselRadius, 
                                        dy=self.kloeVesselRadius, 
                                        dz=self.kloeTrkRegHalfDx)
                                      
        pos = geom.structure.Position("LAr_tgt_env_tub_box_pos", 
                                      self.LArThickness, 
                                      Q('0m'),
                                      Q('0m'))
        
        LAr_tgt_box_shape  = geom.shapes.Boolean("LAr_tgt_box_shape", type='subtraction', 
                                                 first=tub_env_shape,
                                                 second=box_env_shape,
                                                 rot='noRotate',
                                                 pos=pos)

        LAr_tgt_box_lv = geom.structure.Volume("LAr_tgt_box_lv", 
                                               material="Aluminum", 
                                               shape=LAr_tgt_box_shape)
                                               
        tub_lar_shape = geom.shapes.Tubs("LAr_tube_shape", 
                                         rmin=Q("0m"), 
                                         rmax=self.kloeVesselRadius - self.LArBoxThickness, 
                                         dz=self.kloeTrkRegHalfDx - self.LArBoxThickness)
                                      
        box_lar_shape = geom.shapes.Box("LAr_box_shape", 
                                        dx=self.kloeVesselRadius - self.LArBoxThickness, 
                                        dy=self.kloeVesselRadius - self.LArBoxThickness, 
                                        dz=self.kloeTrkRegHalfDx - self.LArBoxThickness)
                                      
        pos = geom.structure.Position("LAr_tgt_tub_box_pos", 
                                      self.LArThickness - self.LArBoxThickness, 
                                      Q('0m'),
                                      Q('0m'))
        
        LAr_tgt_shape  = geom.shapes.Boolean("LAr_tgt_shape", type='subtraction', 
                                             first=tub_lar_shape,
                                             second=box_lar_shape,
                                             rot='noRotate',
                                             pos=pos)

        LAr_tgt_lv = geom.structure.Volume("LAr_tgt_lv", 
                                           material="LAr", 
                                           shape=LAr_tgt_box_shape)
        
        LAr_pla = geom.structure.Placement("LAr_pla", 
                                           volume=LAr_tgt_lv)

        LAr_tgt_box_lv.placements.append(LAr_pla.name)
        
        return LAr_tgt_box_lv

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct straw tube module (without C3H6 target): radiator foils + straw tube XY plane. To be used in the downstream part of the tracking region
    def construct_NoSlab_Module(self,geom, name, halfDimension): 
        
        main_shape = geom.shapes.Box(name + "_shape", 
                                     dx=halfDimension['dx'], 
                                     dy=halfDimension['dy'], 
                                     dz=halfDimension['dz'])

        main_lv = geom.structure.Volume(name + "_vol", 
                                        material="Air35C", 
                                        shape=main_shape)

        print( "STTModuleFULL::construct()")
        print(( "  main_lv = "+ main_lv.name))

        foil_lv= self.construct_Foils(geom, 
                                      name + "_foils",
                                      halfDimension['dy'], 
                                      halfDimension['dz'])


        foil_pos = geom.structure.Position(name + "_pos_foilchunk_in_NoSlab_Mod", 
                                           -self.NoSlabModThickness/2.0 + self.totFoilsThickness/2.0,
                                           Q('0cm'),
                                           Q('0cm'))

        foil_pla=geom.structure.Placement(name + "_foils_pla", 
                                          volume=foil_lv, 
                                          pos=foil_pos)

        main_lv.placements.append(foil_pla.name)

        strawplane_lv=self.construct_XYSTPlane(geom,
                                               name + "_ST",
                                               halfDimension['dy'],
                                               halfDimension['dz'],
                                               "stGas_Xe19")
        
        strawplane_pos = geom.structure.Position(name + "_pos_ST_in_NoSlab_Mod", 
                                                 self.NoSlabModThickness/2.0 - self.planeXXThickness,
                                                 Q('0cm'),
                                                 Q('0cm'))
                                           
        strawplane_pla=geom.structure.Placement(name + "_ST_pla", 
                                                volume=strawplane_lv, 
                                                pos=strawplane_pos)

        main_lv.placements.append(strawplane_pla.name)
        return main_lv

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct straw tube regular module: C3H6 target + radiator foils + straw tube XY plane
    def construct_C3H6_Module(self,geom, name, halfDimension):

        main_shape = geom.shapes.Box(name + "_shape", 
                                     dx=halfDimension['dx'], 
                                     dy=halfDimension['dy'], 
                                     dz=halfDimension['dz'])

        main_lv = geom.structure.Volume(name + "_vol", 
                                        material="Air35C", 
                                        shape=main_shape)

        print( "STTModuleFULL::construct()")
        print(( "  main_lv = "+ main_lv.name))

        slab_shape = geom.shapes.Box(name + "_slab_shape", 
                                     dx=self.slabThickness/2.0, 
                                     dy=halfDimension['dy'], 
                                     dz=halfDimension['dz'])

        slab_lv = geom.structure.Volume(name + "_slab_vol", 
                                        material="C3H6", 
                                        shape=slab_shape)
        
        slab_pos = geom.structure.Position(name + "_pos_slab_in_C3H6_Mod", 
                                           -self.C3H6ModThickness/2.0 + self.slabThickness/2.0, 
                                           Q('0cm'),
                                           Q('0cm'))

        slab_pla=geom.structure.Placement(name + "_slab_pla", 
                                          volume=slab_lv, 
                                          pos=slab_pos)

        main_lv.placements.append(slab_pla.name)
        
        foil_lv = self.construct_Foils(geom, 
                                      name + "_foils", 
                                      halfDimension['dy'], 
                                      halfDimension['dz'])
        
        foil_pos = geom.structure.Position(name + "_pos_foilchunk_in_C3H6_Mod",
                                           -self.C3H6ModThickness/2.0 + self.slabThickness + self.totFoilsThickness/2.0,
                                           Q('0cm'),
                                           Q('0cm'))

        foil_pla=geom.structure.Placement(name + "_foils_pla", 
                                          volume=foil_lv, 
                                          pos=foil_pos)

        main_lv.placements.append(foil_pla.name)
            
        strawplane_lv=self.construct_XYSTPlane(geom,
                                               name + "_ST",
                                               halfDimension['dy'],
                                               halfDimension['dz'],
                                               "stGas_Xe19")
        
        strawplane_pos = geom.structure.Position(name + "_pos_ST_in_C3H6_Mod", 
                                                 self.C3H6ModThickness/2.0 - self.planeXXThickness,
                                                 Q('0cm'),
                                                 Q('0cm'))
                                           
        strawplane_pla=geom.structure.Placement(name + "_ST_pla", 
                                                volume=strawplane_lv, 
                                                pos=strawplane_pos)

        main_lv.placements.append(strawplane_pla.name)
        return main_lv

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct straw tube module (with graphite target): graphite target + straw tube XY plane
    def construct_C_Module(self,geom, name, halfDimension):

        main_shape = geom.shapes.Box(name + "_shape", 
                                     dx=halfDimension['dx'], 
                                     dy=halfDimension['dy'], 
                                     dz=halfDimension['dz'])

        main_lv = geom.structure.Volume(name + "_vol", 
                                        material="Air35C", 
                                        shape=main_shape)
        
        print( "STTModuleFULL::construct()")
        print(( "  main_lv = "+ main_lv.name))

        graphite_shape = geom.shapes.Box(name+"_graph_shape", 
                                         dx=self.graphiteThickness/2.0, 
                                         dy=halfDimension['dy'], 
                                         dz=halfDimension['dz'])

        graphite_lv = geom.structure.Volume(name+"_graph_vol", 
                                            material="Graphite", 
                                            shape=graphite_shape)
        
        graphite_pos = geom.structure.Position(name + "_pos_graphite_in_C_Mod", 
                                               -self.CModThickness/2.0+self.graphiteThickness/2.0, 
                                               Q('0cm'),
                                               Q('0cm'))
        
        graphite_pla=geom.structure.Placement(name+"_graph_pla", 
                                              volume=graphite_lv, 
                                              pos=graphite_pos)

        main_lv.placements.append(graphite_pla.name)

        strawplane_lv=self.construct_XYSTPlane(geom,
                                               name+"_ST", 
                                               halfDimension['dy'],
                                               halfDimension['dz'],
                                               "stGas_Ar19")
        
        strawplane_pos = geom.structure.Position(name + "_pos_ST_in_C_Mod",
                                                 self.CModThickness/2.0 - self.planeXXThickness,
                                                 Q('0cm'),
                                                 Q('0cm'))

        strawplane_pla=geom.structure.Placement("pla_"+name+"_ST", 
                                                volume=strawplane_lv, 
                                                pos=strawplane_pos)

        main_lv.placements.append(strawplane_pla.name)
        return main_lv

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct radiator foils
    def construct_Foils(self,geom, name, halfheight, halflength):
        main_shape = geom.shapes.Box(name, 
                                     dx=self.totFoilsThickness/2.0, 
                                     dy=halfheight, 
                                     dz=halflength)

        main_lv = geom.structure.Volume("vol"+name, 
                                        material="Air35C", 
                                        shape=main_shape)

        print( "STTModuleFULL::construct()")
        print(( "  main_lv = "+ main_lv.name))
        
        foil_shape = geom.shapes.Box(name + "_foil_shape", 
                                     dx=self.foilThickness/2.0, 
                                     dy=halfheight, 
                                     dz=halflength)

        foil_lv = geom.structure.Volume(name + "_foil_vol", 
                                        material="C3H6", 
                                        shape=foil_shape)
        
        for i in range(self.nfoil):
            foil_pos = geom.structure.Position(name + "_pos_foil_"+str(i), 
                                          -self.totFoilsThickness/2.0 + self.foilThickness/2.0 + i*(self.foilThickness+self.foilGap), 
                                          Q('0m'), 
                                          Q('0m'))

            foil_pla = geom.structure.Placement("pla_"+name + "_foil_"+str(i), 
                                              volume=foil_lv, 
                                              pos=foil_pos)
            main_lv.placements.append(foil_pla.name)
        return main_lv

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct XY straw tube plane
    def construct_XYSTPlane(self,geom, name, halfheight, halflength, gasMaterial):
        main_shape = geom.shapes.Box(name, 
                                     dx=self.planeXXThickness, 
                                     dy=halfheight, 
                                     dz=halflength)
        main_lv = geom.structure.Volume("vol"+name, 
                                        material="Air35C", 
                                        shape=main_shape)
        
        pos_hh_in_ST=geom.structure.Position(name + "pos_hh_in_ST", -self.planeXXThickness/2.0, Q('0cm'),Q('0cm'))
        pos_vv_in_ST=geom.structure.Position(name + "pos_vv_in_ST", self.planeXXThickness/2.0 , Q('0cm'),Q('0cm'))
        
        hh_lv=self.construct_STPlane(geom, 
                                     name+"_hor",
                                     halfheight,
                                     halflength, 
                                     gasMaterial)
        vv_lv=self.construct_STPlane(geom, 
                                     name+"_ver",
                                     halflength,
                                     halfheight,
                                     gasMaterial)
        
        hh_pla=geom.structure.Placement("pla_"+name+"_hh", 
                                        volume=hh_lv, 
                                        pos=pos_hh_in_ST)
        vv_pla=geom.structure.Placement("pla_"+name+"_vv", 
                                        volume=vv_lv,   
                                        pos=pos_vv_in_ST,
                                        rot= "r90aboutX")
        
        main_lv.placements.append(hh_pla.name)
        main_lv.placements.append(vv_pla.name)
        return main_lv  

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct straw tube plane. Straw tubes are staggered
    def construct_STPlane(self,geom, name, halfheight, halflength, gasMaterial):
        main_shape = geom.shapes.Box(name + "_shape", 
                                     dx=self.planeXXThickness/2.0, 
                                     dy=halfheight, 
                                     dz=halflength)
        main_lv = geom.structure.Volume(name + "_vol", 
                                        material="Air35C", 
                                        shape=main_shape )
        straw_lv=self.construct_ST(geom,
                                   name + "_ST_" + gasMaterial , 
                                   halflength=halflength, 
                                   gasMaterial=gasMaterial)
            
        Nstraw=int(0.5*(2.*halfheight/self.strawRadius-1.))
        
        for i in range(Nstraw):
            pos1=[-self.planeXXThickness/2.0 + self.strawRadius, 
                  halfheight - (2*i+1)*self.strawRadius, 
                  Q('0m')]
            straw_pos1=geom.structure.Position("pos_"+name+"_"+str(i),
                                               pos1[0],pos1[1],pos1[2])
            straw_pla1=geom.structure.Placement("pla_"+name+"_"+str(i), 
                                                volume=straw_lv, 
                                                pos=straw_pos1)
            main_lv.placements.append(straw_pla1.name)

            pos2=[self.planeXXThickness/2.0 - self.strawRadius,  
                  halfheight -(2*i+2)*self.strawRadius, 
                  Q('0m')]
            straw_pos2=geom.structure.Position("pos_"+name+"_"+str(i+Nstraw), 
                                               pos2[0],pos2[1],pos2[2])
            straw_pla2=geom.structure.Placement("pla_"+name+"_"+str(i+Nstraw), 
                                                volume=straw_lv, 
                                                pos=straw_pos2)
            main_lv.placements.append(straw_pla2.name)    
        return main_lv  

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    # construct straw tube        
    def construct_ST( self, geom, name, halflength, gasMaterial ):
        main_shape = geom.shapes.Tubs(name + "_shape", 
                                      rmin=Q("0m"), 
                                      rmax=self.strawRadius, 
                                      dz=halflength)
        main_lv = geom.structure.Volume(name + "_vol", 
                                        material = "Air35C", 
                                        shape = main_shape )

        coat_shape = geom.shapes.Tubs(name + "_coat", 
                                      rmin = self.strawRadius- self.coatThickness , 
                                      rmax = self.strawRadius, 
                                      dz = halflength)
        coat_lv = geom.structure.Volume(name + "_coat_lv", 
                                        material = "Aluminum", 
                                        shape = coat_shape)
        
        mylar_shape = geom.shapes.Tubs(name + "_mylar", 
                                       rmin = self.strawRadius- self.coatThickness - self.mylarThickness , 
                                       rmax = self.strawRadius- self.coatThickness, 
                                       dz = halflength)
        mylar_lv   = geom.structure.Volume(name + "_mylar_lv", 
                                           material = "Mylar", 
                                           shape = mylar_shape)

        
        air_shape=geom.shapes.Tubs(name+"_air", 
                                   rmin = self.strawWireWThickness + self.strawWireGThickness,
                                   rmax = self.strawRadius- self.coatThickness - self.mylarThickness, 
                                   dz = halflength)
        air_lv   = geom.structure.Volume(name+"_air_lv", 
                                         material = gasMaterial, 
                                         shape = air_shape)
        air_lv.params.append(("SensDet","Straw"))

        wireW_shape = geom.shapes.Tubs(name + "_wireW", 
                                       rmin = Q("0um"), 
                                       rmax = self.strawWireWThickness, 
                                       dz = halflength)
        wireW_lv    = geom.structure.Volume(name + "_wireW_lv", 
                                            material = "Tungsten", 
                                            shape = wireW_shape)

        wireG_shape = geom.shapes.Tubs(name + "_wireG", 
                                       rmin = self.strawWireWThickness, 
                                       rmax = self.strawWireWThickness + self.strawWireGThickness, 
                                       dz = halflength)
        wireG_lv    = geom.structure.Volume(name + "_wireG_lv", 
                                            material = "Gold", 
                                            shape = wireG_shape)
        
        coat_pla  = geom.structure.Placement( "pla_"+name+"_coat" , volume = coat_lv )
        mylar_pla = geom.structure.Placement( "pla_"+name+"_mylar", volume = mylar_lv )
        air_pla   = geom.structure.Placement( "pla_"+name+"_air"  , volume = air_lv )
        wireW_pla = geom.structure.Placement( "pla_"+name+"_wireW", volume = wireW_lv )
        wireG_pla = geom.structure.Placement( "pla_"+name+"_wireG", volume = wireG_lv )
        
        main_lv.placements.append( coat_pla.name )
        main_lv.placements.append( mylar_pla.name )
        main_lv.placements.append( air_pla.name )
        main_lv.placements.append( wireW_pla.name )
        main_lv.placements.append( wireG_pla.name )
        return main_lv        
        
