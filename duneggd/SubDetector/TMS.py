#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q
global Pos
class tmsBuilder(gegede.builder.Builder):
    def configure(self, mat=None, thinbox1Dimension=None, thinbox2Dimension=None, gapPosition=None, BFieldUpLow = None, BFieldUpHigh = None, BFieldDownLow = None , BFieldDownHigh = None,  **kwds):
        self.BFieldUpLow = BFieldUpLow
        self.BFieldUpHigh = BFieldUpHigh
        self.BFieldDownLow = BFieldDownLow 
        self.BFieldDownHigh = BFieldDownHigh
        self.mat=mat
        self.thinbox1Dimension=thinbox1Dimension
        self.thinbox2Dimension=thinbox2Dimension
        self.gapPosition=gapPosition
        
        
    def construct(self, geom):        
            
        #Make Boxes for steel and logical volumes

        thinBox1 = geom.shapes.Box( 'box'+self.name,
                                    dx = 0.5*self.thinbox1Dimension[0],
                                    dy = 0.5*self.thinbox1Dimension[1],
                                    dz = 0.5*self.thinbox1Dimension[2])
        thinBox2 = geom.shapes.Box( 'box2'+self.name,
                                    dx = 0.5*self.thinbox2Dimension[0],
                                    dy = 0.5*self.thinbox2Dimension[1],
                                    dz = 0.5*self.thinbox2Dimension[2])
        
        thickBox1 = geom.shapes.Box( 'thickbox'+self.name,
                                     dx = 0.5*self.thinbox1Dimension[0],
                                     dy = 0.5*self.thinbox1Dimension[1],
                                     dz = 0.5*Q("0.040m"))
        thickBox2 = geom.shapes.Box( 'thickbox2'+self.name,
                                    dx = 0.5*self.thinbox2Dimension[0],
                                    dy = 0.5*self.thinbox2Dimension[1],
                                     dz = 0.5*Q("0.040m"))



        thin_layer = geom.shapes.Box( 'thinlayerbox',
                                      dx = 0.5*Q("7.036m"),
                                      dy = 0.5*Q("5.022m"),
                                      dz = 0.5*Q("0.015m"))
        thick_layer = geom.shapes.Box( 'thicklayerbox',
                                      dx = 0.5*Q("7.036m"),
                                      dy = 0.5*Q("5.022m"),
                                      dz = 0.5*Q("0.040m"))

        # The main box for the whole TMS
        tmsbox = geom.shapes.Box( 'tmsbox',
                                   dx = 0.5*Q("7.036m"),
                                   dy = 0.5*Q("6.90m"), # 8.825
                                   dz = 0.5*Q("7.05m"))
        
        
        thinBox1_lv = geom.structure.Volume( 'thinvol'+self.name, material=self.mat, shape=thinBox1 )
        thinBox2_lv = geom.structure.Volume( 'thinvol2'+self.name, material=self.mat, shape=thinBox2 )
        thickBox1_lv = geom.structure.Volume( 'thickvol'+self.name, material=self.mat, shape=thickBox1 )
        thickBox2_lv = geom.structure.Volume( 'thickvol2'+self.name, material=self.mat, shape=thickBox2 )
        thinBox1_lv.params.append(('BField',self.BFieldDownHigh))
        thinBox2_lv.params.append(('BField',self.BFieldUpHigh))
        thickBox1_lv.params.append(('BField',self.BFieldDownLow))
        thickBox2_lv.params.append(('BField',self.BFieldUpLow))


        thin_layer_lv = geom.structure.Volume( 'thinlayervol', material='Air', shape=thin_layer )
        thick_layer_lv = geom.structure.Volume( 'thicklayervol', material='Air', shape=thick_layer )
        tms_lv = geom.structure.Volume( 'vol'+self.name, material='Air', shape=tmsbox )
            
        #Poition steel in layer volumes (Thin)
        lf_pos = geom.structure.Position( 'lfpos'+self.name,
                                          0.5*(self.thinbox1Dimension[0]+self.thinbox2Dimension[0])+self.gapPosition[0],
                                          Q("0m"),
                                          Q("0m"))
        
        rt_pos = geom.structure.Position( 'rtpos'+self.name,
                                          -(0.5*(self.thinbox1Dimension[0]+self.thinbox2Dimension[0])+self.gapPosition[0]),
                                          Q("0m"),
                                          Q("0m"))
            
        ctr_pos = geom.structure.Position( 'ctrpos'+self.name,
                                           Q("0m"),
                                           Q("0m"),
                                           Q("0m"))


        # Thin steel        
        rt_pla = geom.structure.Placement( 'rtpla'+self.name, volume=thinBox1_lv, pos=rt_pos )
        lf_pla = geom.structure.Placement( 'lfpla'+self.name, volume=thinBox1_lv, pos=lf_pos )
        ctr_pla = geom.structure.Placement( 'ctrpla'+self.name, volume=thinBox2_lv, pos=ctr_pos )

        thin_layer_lv.placements.append(rt_pla.name)
        thin_layer_lv.placements.append(lf_pla.name)
        thin_layer_lv.placements.append(ctr_pla.name)

        # Thick steel
        thick_rt_pla = geom.structure.Placement( 'thickrtpla'+self.name, volume=thickBox1_lv, pos=rt_pos )
        thick_lf_pla = geom.structure.Placement( 'thicklfpla'+self.name, volume=thickBox1_lv, pos=lf_pos )
        thick_ctr_pla = geom.structure.Placement( 'thickctrpla'+self.name, volume=thickBox2_lv, pos=ctr_pos )

        thick_layer_lv.placements.append(thick_rt_pla.name)
        thick_layer_lv.placements.append(thick_lf_pla.name)
        thick_layer_lv.placements.append(thick_ctr_pla.name)

        # Postion the thin and thick steel
        # 100 scint layers but first and last layer is scintillator
        # so only 99 steel layers, 39 thin and 60 thick

        n_thin_steel = 39
        thinlayer_pos = [geom.structure.Position('a')]*n_thin_steel
        thin_layer_pla = [geom.structure.Placement('b',volume=thin_layer_lv,pos=thinlayer_pos[1])]*n_thin_steel

        # All the planes of steel and scintillator have the same x and y position
        xpos_planes = Q("0m")
        ypos_planes = Q("0.85m") # this is the vertical position w.r.t. the main tms box

        for plane in range(n_thin_steel):
            # zpos changes with each layer
            zpos = -Q("3.4645m") + plane * Q("0.055m")                                                        
            thinlayer_pos[plane] = geom.structure.Position( 'thinlayerposition'+str(plane),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            thin_layer_pla[plane] = geom.structure.Placement( 'thinlayerpla'+self.name+str(plane), volume=thin_layer_lv, pos=thinlayer_pos[plane] )
            tms_lv.placements.append(thin_layer_pla[plane].name)

        #Thick Layer Placement
        n_thick_steel = 60
        thicklayer_pos = [geom.structure.Position('c')]*n_thick_steel
        thick_layer_pla = [geom.structure.Placement('d',volume=thick_layer_lv, pos=thicklayer_pos[1])]*n_thick_steel
        
        for plane in range(n_thick_steel):
            zpos = -Q("1.307m")+ plane * Q("0.08m") #subtrack 0.015 m from zpos = -Q("1.292m") 
            thicklayer_pos[plane] = geom.structure.Position( 'thicklayerposition'+str(plane),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            thick_layer_pla[plane] = geom.structure.Placement( 'thicklayerpla'+self.name+str(plane), volume=thick_layer_lv, pos=thicklayer_pos[plane] )
            tms_lv.placements.append(thick_layer_pla[plane].name)
        

        # Scintillator
        # Individual scintillator bar
        scinBox = geom.shapes.Box( 'scinbox'+self.name,
                                    dx = 0.5*Q("0.03542m"),
                                    dy = 0.5*Q("3.096m"),
                                    dz = 0.5*Q("0.01m"))

        scinBox_lv = geom.structure.Volume( 'scinBoxlv'+self.name, material='Scintillator', shape=scinBox)
        scinBox_lv.params.append(("SensDet", tms_lv.name))

        # Place Bars into Modules
        ModuleBox = geom.shapes.Box( 'ModuleBox',
                                     dx = 0.5*Q("0.03542m")*48, # 0.04*42
                                     dy = 0.5*Q("3.096m"),
                                     dz = 0.5*Q("0.01m"))
        ModuleBox_lv = geom.structure.Volume( 'ModuleBoxvol', material='Air', shape=ModuleBox )
                                                                                                                                           
        sci_bars = 48
        sci_Bar_pos = [geom.structure.Position('e')]*sci_bars
        sci_Bar_pla = [geom.structure.Placement('f',volume=scinBox_lv, pos=sci_Bar_pos[1])]*sci_bars

        # y and z positions are the same for each bar
        zpos_bar = Q("0m") 
        ypos_bar = Q("0m")
        for bar in range(sci_bars):
            xpos = -Q("0.83237m")+ bar * Q("0.03542m")
            sci_Bar_pos[bar] = geom.structure.Position( 'sci_barposition'+str(bar),
                                                           x = xpos,
                                                           y = ypos_bar,
                                                           z = zpos_bar)
            sci_Bar_pla[bar] = geom.structure.Placement( 'scibarpla'+self.name+str(bar), volume=scinBox_lv, pos=sci_Bar_pos[bar] )
            ModuleBox_lv.placements.append(sci_Bar_pla[bar].name)

        # Place Modules into scint layers
        modules_in_layer = 4
        Module_layer = geom.shapes.Box( 'Modulelayerbox',
                                      dx = 0.5*Q("7.036m"), #7.04 
                                      dy = 0.5*Q("5.022m"),
                                      dz = 0.5*Q("0.040m"))        

        Module_layer_lv = geom.structure.Volume( 'modulelayervol', material='Air', shape=Module_layer )

        #Poition modules in layer                                                                                            
        Mod_ri_rot = geom.structure.Rotation( 'Modrirot', '0deg','0deg','3deg')
        Mod_left_rot = geom.structure.Rotation( 'Modleftrot', '0deg','0deg','-3deg')

        mod_pos1 = geom.structure.Position( 'modpos1'+self.name,
                                          -1.5*Q("0.03542m")*48-Q("0.015m"),
                                          Q("0m"),
                                          Q("0m"))

        mod_pos2 = geom.structure.Position( 'modpos2'+self.name,
                                            -0.5*Q("0.03542m")*48-Q("0.005m"),
                                            Q("0m"),
                                            Q("0m"))

        mod_pos3 = geom.structure.Position( 'modpos3'+self.name,
                                           +0.5*Q("0.03542m")*48+Q("0.005m"),
                                           Q("0m"),
                                           Q("0m"))

        mod_pos4 = geom.structure.Position( 'modpos4'+self.name,
                                            +1.5*Q("0.03542m")*48+Q("0.015m"),
                                            Q("0m"),
                                            Q("0m"))




        mod_ri_pla1 = geom.structure.Placement( 'modripla1'+self.name, volume=  ModuleBox_lv, pos=mod_pos1, rot = Mod_ri_rot)
        mod_le_pla1 = geom.structure.Placement( 'modlepla1'+self.name, volume=  ModuleBox_lv, pos=mod_pos1, rot = Mod_left_rot)

        #mod_pla1 = geom.structure.Placement( 'mod1pla'+self.name, volume=  ModuleBox_lv, pos=mod_pos1)
        mod_ri_pla2 = geom.structure.Placement( 'modripla2'+self.name, volume=  ModuleBox_lv, pos=mod_pos2, rot = Mod_ri_rot)
        mod_le_pla2 = geom.structure.Placement( 'modlepla2'+self.name, volume=  ModuleBox_lv, pos=mod_pos2, rot = Mod_left_rot)

        #mod_pla2 = geom.structure.Placement( 'mod2pla'+self.name, volume=  ModuleBox_lv, pos=mod_pos2)
        mod_ri_pla3 = geom.structure.Placement( 'modripla3'+self.name, volume=  ModuleBox_lv, pos=mod_pos3, rot = Mod_ri_rot)
        mod_le_pla3 = geom.structure.Placement( 'modlepla3'+self.name, volume=  ModuleBox_lv, pos=mod_pos3, rot = Mod_left_rot)

        mod_ri_pla4 = geom.structure.Placement( 'modripla4'+self.name, volume=  ModuleBox_lv, pos=mod_pos4, rot = Mod_ri_rot)
        mod_le_pla4 = geom.structure.Placement( 'modlepla4'+self.name, volume=  ModuleBox_lv, pos=mod_pos4, rot = Mod_left_rot)

        Module_layer_lv.placements.append(mod_ri_pla1.name)
        Module_layer_lv.placements.append(mod_le_pla1.name)

        Module_layer_lv.placements.append(mod_ri_pla2.name)
        Module_layer_lv.placements.append(mod_le_pla2.name)

        Module_layer_lv.placements.append(mod_ri_pla3.name)
        Module_layer_lv.placements.append(mod_le_pla3.name)

        Module_layer_lv.placements.append(mod_ri_pla4.name)
        Module_layer_lv.placements.append(mod_le_pla4.name)

        #Place Layers into RMS vol
        Module_layers_thin = 40
        thinModlayer_pos = [geom.structure.Position('g')]*Module_layers_thin

        thin_Modlayer_pla = [geom.structure.Placement('h',volume=Module_layer_lv,pos=thinModlayer_pos[1])]*Module_layers_thin

        for module in range(Module_layers_thin):
            zpos = -Q("3.4645m") -Q("0.0275m") + module * Q("0.055m")
            thinModlayer_pos[module] = geom.structure.Position( 'thinModlayerposition'+str(module),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            thin_Modlayer_pla[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv, pos=thinModlayer_pos[module] )
            tms_lv.placements.append(thin_Modlayer_pla[module].name)


        #Place Layers into RMS vol between thick layers                                                                                 
        Module_layers_thick = 60
        thickModlayer_pos = [geom.structure.Position('i')]*Module_layers_thick

        thick_Modlayer_pla = [geom.structure.Placement('j',volume=Module_layer_lv,pos=thickModlayer_pos[1])]*Module_layers_thick
            
        for module in range(0,Module_layers_thick):
            zpos = -Q("1.292m") + Q("0.025m")  + module * Q("0.08m") # subtract 0.015m from zpos=-Q("1.292m")+Q("0.040m")

            thickModlayer_pos[module] = geom.structure.Position( 'thickModlayerposition'+str(module),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv, pos=thickModlayer_pos[module] )
            tms_lv.placements.append(thick_Modlayer_pla[module].name)







        #Add TMS to self
        self.add_volume(tms_lv)    
        
        
