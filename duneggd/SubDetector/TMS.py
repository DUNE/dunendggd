#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q
global Pos
class tmsBuilder(gegede.builder.Builder):
    def configure(self, mat=None, thinbox1Dimension=None, gapPosition=None, BFieldUpLow = None, BFieldUpHigh = None, BFieldDownLow = None , BFieldDownHigh = None,  
            thin_horizontal=None, thick_horizontal=None, double_horizontal=None, thin_U=None, thick_U=None, double_U=None, thin_V=None, thick_V=None, double_V=None, **kwds):    #thinbox2Dimension=None
        self.BFieldUpLow = BFieldUpLow
        self.BFieldUpHigh = BFieldUpHigh
        self.BFieldDownLow = BFieldDownLow 
        self.BFieldDownHigh = BFieldDownHigh
        self.mat=mat
        self.thinbox1Dimension=thinbox1Dimension
        #self.thinbox2Dimension=thinbox2Dimension   #remnant from old geometry version with two different steel plate widths (outer and inner)
        self.gapPosition=gapPosition
        self.thin_horizontal = thin_horizontal
        self.thick_horizontal = thick_horizontal
        self.double_horizontal = double_horizontal
        self.thin_U = thin_U
        self.thick_U = thick_U
        self.double_U = double_U
        self.thin_V = thin_V
        self.thick_V = thick_V
        self.double_V = double_V
        
        
    def construct(self, geom):        
            
        #Make Boxes for steel and logical volumes

        thinBox1 = geom.shapes.Box( 'box'+self.name,
                                    dx = 0.5*self.thinbox1Dimension[0],
                                    dy = 0.5*self.thinbox1Dimension[1],
                                    dz = 0.5*self.thinbox1Dimension[2])
        thinBox2 = geom.shapes.Box( 'box2'+self.name,
                                    dx = 0.5*self.thinbox1Dimension[0],
                                    dy = 0.5*self.thinbox1Dimension[1],
                                    dz = 0.5*self.thinbox1Dimension[2])
        
        thickBox1 = geom.shapes.Box( 'thickbox'+self.name,
                                     dx = 0.5*self.thinbox1Dimension[0],
                                     dy = 0.5*self.thinbox1Dimension[1],
                                     dz = 0.5*Q("0.040m"))
        thickBox2 = geom.shapes.Box( 'thickbox2'+self.name,
                                    dx = 0.5*self.thinbox1Dimension[0],
                                    dy = 0.5*self.thinbox1Dimension[1],
                                    dz = 0.5*Q("0.040m"))

        doubleBox1 = geom.shapes.Box( 'doublebox'+self.name,
                                    dx = 0.5*self.thinbox1Dimension[0],
                                    dy = 0.5*self.thinbox1Dimension[1],
                                    dz = 0.5*Q("0.080m"))
        doubleBox2 = geom.shapes.Box( 'doublebox2'+self.name,
                                    dx = 0.5*self.thinbox1Dimension[0],
                                    dy = 0.5*self.thinbox1Dimension[1],
                                    dz = 0.5*Q("0.080m"))



        thin_layer = geom.shapes.Box( 'thinlayerbox',
                                      dx = 0.5*Q("7.460m"), #7.036m # 4*self.thinbox1Dimension[0]+3*self.gapPosition[0] # the commented out values like this are from the old geometry. Exchange the values, if switching back to 60-40 steel geometry
                                      dy = 0.5*Q("4.700m"), #5.022m # steel height
                                      dz = 0.5*Q("0.015m"))         # thin steel thickness
        thick_layer = geom.shapes.Box( 'thicklayerbox',
                                      dx = 0.5*Q("7.460m"),
                                      dy = 0.5*Q("4.700m"),
                                      dz = 0.5*Q("0.040m"))         # thick steel thickness
        double_layer = geom.shapes.Box( 'doublelayerbox',
                                      dx = 0.5*Q("7.460m"),
                                      dy = 0.5*Q("4.700m"),
                                      dz = 0.5*Q("0.080m"))         # 2*thick steel thickness, two thick plates

        # The main box for the whole TMS
        tmsbox = geom.shapes.Box( 'tmsbox',
                                   dx = 0.5*Q("8.00m"),             # simply make big enough to fit everything
                                   dy = 0.5*Q("7.00m"), # 8.825     # same, but might need to increase once readout is added to orthogonal scintillator
                                   dz = 0.5*Q("7.55m"))#7.05m"))    # same
        
        
        thinBox1_lv = geom.structure.Volume( 'thinvol'+self.name, material=self.mat, shape=thinBox1 )
        thinBox2_lv = geom.structure.Volume( 'thinvol2'+self.name, material=self.mat, shape=thinBox2 )
        thickBox1_lv = geom.structure.Volume( 'thickvol'+self.name, material=self.mat, shape=thickBox1 )
        thickBox2_lv = geom.structure.Volume( 'thickvol2'+self.name, material=self.mat, shape=thickBox2 )
        doubleBox1_lv = geom.structure.Volume( 'doublevol'+self.name, material=self.mat, shape=doubleBox1 )
        doubleBox2_lv = geom.structure.Volume( 'doublevol2'+self.name, material=self.mat, shape=doubleBox2 )
        thinBox1_lv.params.append(('BField',self.BFieldDownHigh))
        thinBox2_lv.params.append(('BField',self.BFieldUpHigh))
        thickBox1_lv.params.append(('BField',self.BFieldDownHigh))
        thickBox2_lv.params.append(('BField',self.BFieldUpHigh))
        doubleBox1_lv.params.append(('BField',self.BFieldDownHigh))
        doubleBox2_lv.params.append(('BField',self.BFieldUpHigh))

        thin_layer_lv = geom.structure.Volume( 'thinlayervol', material='Air', shape=thin_layer )
        thick_layer_lv = geom.structure.Volume( 'thicklayervol', material='Air', shape=thick_layer )
        double_layer_lv = geom.structure.Volume( 'doublelayervol', material='Air', shape=double_layer )
        tms_lv = geom.structure.Volume( 'vol'+self.name, material='Air', shape=tmsbox )
            
        # Position steel in layer volumes (Thin)
        ### The commented out part here is a remnant from the old geometry with different steel widths (inner and outer) ###
        #lf_pos = geom.structure.Position( 'lfpos'+self.name,
        #                                  0.5*(self.thinbox1Dimension[0]+self.thinbox2Dimension[0])+self.gapPosition[0],
        #                                  Q("0m"),
        #                                  Q("0m"))
        
        #rt_pos = geom.structure.Position( 'rtpos'+self.name,
        #                                  -(0.5*(self.thinbox1Dimension[0]+self.thinbox2Dimension[0])+self.gapPosition[0]),
        #                                  Q("0m"),
        #                                  Q("0m"))
            
        #ctr_pos = geom.structure.Position( 'ctrpos'+self.name,
        #                                   Q("0m"),
        #                                   Q("0m"),
        #                                   Q("0m"))
        ### This is the geometry with the same steel widths in inner and outer parts ###
        steel_pos1 = geom.structure.Position( 'steel_pos1'+self.name,
                                            -1.5*self.thinbox1Dimension[0]-1.5*self.gapPosition[0],
                                            Q("0m"),
                                            Q("0m"))
        steel_pos2 = geom.structure.Position( 'steel_pos2'+self.name,
                                            -0.5*self.thinbox1Dimension[0]-0.5*self.gapPosition[0],
                                            Q("0m"),
                                            Q("0m"))
        steel_pos3 = geom.structure.Position( 'steel_pos3'+self.name,
                                            0.5*self.thinbox1Dimension[0]+0.5*self.gapPosition[0],
                                            Q("0m"),
                                            Q("0m"))
        steel_pos4 = geom.structure.Position( 'steel_pos4'+self.name,
                                            1.5*self.thinbox1Dimension[0]+1.5*self.gapPosition[0],
                                            Q("0m"),
                                            Q("0m"))


        # Thin steel
        ### The commented out part here is a remnant from the old geometry with different steel widths (inner and outer) ###
        #rt_pla = geom.structure.Placement( 'rtpla'+self.name, volume=thinBox1_lv, pos=rt_pos )
        #lf_pla = geom.structure.Placement( 'lfpla'+self.name, volume=thinBox1_lv, pos=lf_pos )
        #ctr_pla = geom.structure.Placement( 'ctrpla'+self.name, volume=thinBox2_lv, pos=ctr_pos )

        #thin_layer_lv.placements.append(rt_pla.name)
        #thin_layer_lv.placements.append(lf_pla.name)
        #thin_layer_lv.placements.append(ctr_pla.name)

        ### This is the geometry with the same steel widths in inner and outer parts ###
        pla_1 = geom.structure.Placement( 'plane1'+self.name, volume=thinBox1_lv, pos=steel_pos1 )
        pla_2 = geom.structure.Placement( 'plane2'+self.name, volume=thinBox2_lv, pos=steel_pos2 )
        pla_3 = geom.structure.Placement( 'plane3'+self.name, volume=thinBox2_lv, pos=steel_pos3 )
        pla_4 = geom.structure.Placement( 'plane4'+self.name, volume=thinBox1_lv, pos=steel_pos4 )

        thin_layer_lv.placements.append(pla_1.name)
        thin_layer_lv.placements.append(pla_2.name)
        thin_layer_lv.placements.append(pla_3.name)
        thin_layer_lv.placements.append(pla_4.name)

        # Thick steel
        ### The commented out part here is a remnant from the old geometry with different steel widths (inner and outer) ###
        #thick_rt_pla = geom.structure.Placement( 'thickrtpla'+self.name, volume=thickBox1_lv, pos=rt_pos )
        #thick_lf_pla = geom.structure.Placement( 'thicklfpla'+self.name, volume=thickBox1_lv, pos=lf_pos )
        #thick_ctr_pla = geom.structure.Placement( 'thickctrpla'+self.name, volume=thickBox2_lv, pos=ctr_pos )

        #thick_layer_lv.placements.append(thick_rt_pla.name)
        #thick_layer_lv.placements.append(thick_lf_pla.name)
        #thick_layer_lv.placements.append(thick_ctr_pla.name)

        ### This is the geometry with the same steel widths in inner and outer parts ###
        thick_pla_1 = geom.structure.Placement( 'thickplane1'+self.name, volume=thickBox1_lv, pos=steel_pos1 )
        thick_pla_2 = geom.structure.Placement( 'thickplane2'+self.name, volume=thickBox2_lv, pos=steel_pos2 )
        thick_pla_3 = geom.structure.Placement( 'thickplane3'+self.name, volume=thickBox2_lv, pos=steel_pos3 )
        thick_pla_4 = geom.structure.Placement( 'thickplane4'+self.name, volume=thickBox1_lv, pos=steel_pos4 )

        thick_layer_lv.placements.append(thick_pla_1.name)
        thick_layer_lv.placements.append(thick_pla_2.name)
        thick_layer_lv.placements.append(thick_pla_3.name)
        thick_layer_lv.placements.append(thick_pla_4.name)

        # Double steel
        ### The commented out part here is a remnant from the old geometry with different steel widths (inner and outer) ###
        #double_rt_pla = geom.structure.Placement( 'doublertpla'+self.name, volume=doubleBox1_lv, pos=rt_pos )
        #double_lf_pla = geom.structure.Placement( 'doublelfpla'+self.name, volume=doubleBox1_lv, pos=lf_pos )
        #double_ctr_pla = geom.structure.Placement( 'doublectrpla'+self.name, volume=doubleBox2_lv, pos=ctr_pos )

        #double_layer_lv.placements.append(double_rt_pla.name)
        #double_layer_lv.placements.append(double_lf_pla.name)
        #double_layer_lv.placements.append(double_ctr_pla.name)

        ### This is the geometry with the same steel widths in inner and outer parts ###
        double_pla_1 = geom.structure.Placement( 'doubleplane1'+self.name, volume=doubleBox1_lv, pos=steel_pos1 )
        double_pla_2 = geom.structure.Placement( 'doubleplane2'+self.name, volume=doubleBox2_lv, pos=steel_pos2 )
        double_pla_3 = geom.structure.Placement( 'doubleplane3'+self.name, volume=doubleBox2_lv, pos=steel_pos3 )
        double_pla_4 = geom.structure.Placement( 'doubleplane4'+self.name, volume=doubleBox1_lv, pos=steel_pos4 )

        double_layer_lv.placements.append(double_pla_1.name)
        double_layer_lv.placements.append(double_pla_2.name)
        double_layer_lv.placements.append(double_pla_3.name)
        double_layer_lv.placements.append(double_pla_4.name)

        # Position the thin and thick steel
        # 91 scint layers but first and last layer is scintillator
        # so only 92 steel layers, 50 thin and 34 thick and 8 double

        n_thin_steel = 50
        thinlayer_pos = [geom.structure.Position('a')]*n_thin_steel
        thin_layer_pla = [geom.structure.Placement('b',volume=thin_layer_lv,pos=thinlayer_pos[1])]*n_thin_steel

        # All the planes of steel and scintillator have the same x and y position
        xpos_planes = Q("0m")
        ypos_planes = Q("0.85m") # this is the vertical position w.r.t. the main tms box

        for plane in range(n_thin_steel):
            # zpos changes with each layer
            zpos = -Q("3.650m") + plane * Q("0.065m") + Q("0.0075m")    # half of total steel thickness with gaps (7300mm) and shift for differing air gaps for thin and double plates
            thinlayer_pos[plane] = geom.structure.Position( 'thinlayerposition'+str(plane),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            thin_layer_pla[plane] = geom.structure.Placement( 'thinlayerpla'+self.name+str(plane), volume=thin_layer_lv, pos=thinlayer_pos[plane] )
            tms_lv.placements.append(thin_layer_pla[plane].name)

        #Thick Layer Placement
        n_thick_steel = 34
        thicklayer_pos = [geom.structure.Position('c')]*n_thick_steel
        thick_layer_pla = [geom.structure.Placement('d',volume=thick_layer_lv, pos=thicklayer_pos[1])]*n_thick_steel
        
        for plane in range(n_thick_steel):
            zpos = -Q("0.3875m")+ plane * Q("0.09m") + Q("0.0075m")     # last thin steel plate + half thin steel thickness + gap + half thick steel thickness 
            thicklayer_pos[plane] = geom.structure.Position( 'thicklayerposition'+str(plane),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            thick_layer_pla[plane] = geom.structure.Placement( 'thicklayerpla'+self.name+str(plane), volume=thick_layer_lv, pos=thicklayer_pos[plane] )
            tms_lv.placements.append(thick_layer_pla[plane].name)
        
        #Double Layer Placement
        n_double_steel = 8
        doublelayer_pos = [geom.structure.Position('e')]*n_double_steel #e was scintillator so far!!!
        double_layer_pla = [geom.structure.Placement('f',volume=double_layer_lv, pos=doublelayer_pos[1])]*n_double_steel    #f was scintillator so far!!!

        for plane in range(n_double_steel):
            zpos = +Q("2.6925m") + plane * Q("0.130m") + Q("0.0075m")   # last thick steel plate + half thick steel thickness + gap + half double steel thickness
            doublelayer_pos[plane] = geom.structure.Position( 'doublelayerposition'+str(plane),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            double_layer_pla[plane] = geom.structure.Placement( 'doublelayerpla'+self.name+str(plane), volume=double_layer_lv, pos=doublelayer_pos[plane] )
            tms_lv.placements.append(double_layer_pla[plane].name)


        # Scintillator
        # Individual scintillator bar
        scinBox = geom.shapes.Box( 'scinbox'+self.name,
                                    dx = 0.5*Q("0.036m"),   # width single bar
                                    dy = 0.5*Q("3.300m"),   # length bar for stereo bars
                                    dz = 0.5*Q("0.017m"))   # thickness single bar
        
        scinBox_ortho = geom.shapes.Box( 'scinbox_ortho'+self.name,
                                    dx = 0.5*Q("3.500m"),   # length bar for orthogonal bars
                                    dy = 0.5*Q("0.036m"),   # width single bar
                                    dz = 0.5*Q("0.017m"))   # thickness single bar

        scinBox_lv = geom.structure.Volume( 'scinBoxlv'+self.name, material='Scintillator', shape=scinBox)
        scinBox_lv.params.append(("SensDet", tms_lv.name))

        scinBox_lv_ortho = geom.structure.Volume( 'scinBoxlv_ortho'+self.name, material='Scintillator', shape=scinBox_ortho)
        scinBox_lv_ortho.params.append(("SensDet", tms_lv.name))

        # Place Bars into Modules
        ModuleBox = geom.shapes.Box( 'ModuleBox',
                                     dx = 0.5*Q("0.036m")*32,    # Single module contains 32 bars
                                     dy = 0.5*Q("3.300m"),       # Same length as single stereo bar
                                     dz = 0.5*Q("0.017m"))       # Same thickness as single bar

        ModuleBox_ortho = geom.shapes.Box( 'ModuleBox_ortho',
                                    dx = 0.5*Q("3.500m"),        # Same length as single orthogonal bar
                                    dy = 0.5*Q("0.036m")*32,     # Single module contains 32 bars
                                    dz = 0.5*Q("0.017m"))        # Same thickness as single bar

        ModuleBox_lv = geom.structure.Volume( 'ModuleBoxvol', material='Air', shape=ModuleBox )

        ModuleBox_lv_ortho = geom.structure.Volume( 'ModuleBoxvol_ortho', material='Air', shape=ModuleBox_ortho)
        

        # Attempting to add aluminium box as an enclosure. NOT WORKING YET!!! TODO: This
        #Aluminium_case = geom.shapes.Box( 'AluCase',
        #                            dx = 0.5*(Q("0.03542m")*32 + Q("0.001m")),
        #                            dy = 0.5*(Q("3.096m") + Q("0.001m")),
        #                            dz = 0.5*(Q("0.017m") + Q("0.001m")))

        #Aluminium_case_ortho = geom.shapes.Box( 'AluCase_ortho',
        #                            dx = 0.5*(Q("3.096m") + Q("0.001m")),
        #                            dy = 0.5*(Q("0.03542m")*32 + Q("0.001m")),
        #                            dz = 0.5*(Q("0.017m") + Q("0.001m")))

        #Aluminium_case = geom.structure.Volume( 'AluCasevol', material='Aluminum', shape=Aluminium_case)
        #ModuleBox_lv.placements.append(geom.structure.Placement( 'AluCasePla'+self.name, volume=ModuleBox_lv,
        #                                                        pos=geom.structure.Position( 'AluCasePos',
        #                                                                                    xpos = Q("0m"),
        #                                                                                    ypos = Q("0m"),
        #                                                                                    zpos = Q("0m"))))

        #Aluminium_case_ortho = geom.structure.Volume( 'AluCasevol_ortho', material='Aluminium', shape=Aluminium_case_ortho)
        #ModuleBox_lv_ortho.placements.append(geom.structure.Placement( 'AluCaseOrthoPla'+self.name, volume=ModuleBox_lv_ortho,
        #                                                        pos=geom.structure.Position( 'AluCaseOrthoPos',
        #                                                                                    xpos = Q("0m"),
        #                                                                                    ypos = Q("0m"),
        #                                                                                    zpos = Q("0m")))) 

        # now create and place the bars
        sci_bars = 32
        sci_Bar_pos = [geom.structure.Position('g')]*sci_bars
        sci_Bar_pla = [geom.structure.Placement('h',volume=scinBox_lv, pos=sci_Bar_pos[1])]*sci_bars

        sci_Bar_pos_ortho = [geom.structure.Position('i')]*sci_bars
        sci_Bar_pla_ortho = [geom.structure.Placement('j', volume=scinBox_lv_ortho, pos=sci_Bar_pos_ortho[1])]*sci_bars

        # y and z positions are the same for each bar
        zpos_bar = Q("0m") 
        ypos_bar = Q("0m")

        zpos_bar_ortho = Q("0m")
        xpos_bar_ortho = Q("0m")

        for bar in range(sci_bars):
            xpos = -Q("0.558m")+ bar * Q("0.036m")          # middle of last bar in single module (-16*bar width + half bar width)
            sci_Bar_pos[bar] = geom.structure.Position( 'sci_barposition'+str(bar),
                                                           x = xpos,
                                                           y = ypos_bar,
                                                           z = zpos_bar)

            sci_Bar_pla[bar] = geom.structure.Placement( 'scibarpla'+self.name+str(bar), volume=scinBox_lv, pos=sci_Bar_pos[bar] )
            ModuleBox_lv.placements.append(sci_Bar_pla[bar].name)

            ypos_ortho = -Q("0.558m") + bar * Q("0.036m")  # middle of last bar in single module (-16*bar width + half bar width)
            sci_Bar_pos_ortho[bar] = geom.structure.Position( 'sci_barposition_ortho'+str(bar),
                                                            x = xpos_bar_ortho,
                                                            y = ypos_ortho,
                                                            z = zpos_bar_ortho)
            sci_Bar_pla_ortho[bar] = geom.structure.Placement( 'scibarpla_ortho'+self.name+str(bar), volume=scinBox_lv_ortho, pos = sci_Bar_pos_ortho[bar])
            ModuleBox_lv_ortho.placements.append(sci_Bar_pla_ortho[bar].name)

        # Place Modules into scint layers
        modules_in_layer = 6
        Module_layer = geom.shapes.Box( 'Modulelayerbox',
                                      dx = 0.5*Q("7.500m"), #7.04   # make it fit
                                      dy = 0.5*Q("3.500m"), #4.700m # about 3*module width
                                      dz = 0.5*Q("0.050m"))         # fill entire gap between steel

        Module_layer_lv1 = geom.structure.Volume( 'modulelayervol1', material='Air', shape=Module_layer )
        Module_layer_lv2 = geom.structure.Volume( 'modulelayervol2', material='Air', shape=Module_layer )
        Module_layer_lv3 = geom.structure.Volume( 'modulelayervol3', material='Air', shape=Module_layer )

        #Position modules in layer                                                                                            
        Mod_ri_rot = geom.structure.Rotation( 'Modrirot', '0deg','0deg','3deg')
        Mod_left_rot = geom.structure.Rotation( 'Modleftrot', '0deg','0deg','-3deg')
        Mod_ortho_rot = geom.structure.Rotation( 'Modorthorot', '0deg', '0deg', '0deg')

        mod_pos1 = geom.structure.Position( 'modpos1'+self.name,
                                            -2.5*Q("0.036m")*32-Q("0.021m"),    # position center of module (very left) and add sum of gaps
                                            Q("0m"),
                                            Q("0m"))

        mod_pos2 = geom.structure.Position( 'modpos2'+self.name,
                                            -1.5*Q("0.036m")*32-Q("0.014m"),    # position center of module (middle left) and add sum of gaps
                                            Q("0m"),
                                            Q("0m"))

        mod_pos3 = geom.structure.Position( 'modpos3'+self.name,
                                            -0.5*Q("0.036m")*32-Q("0.007m"),    # position center of module (slightly left) and add gap
                                            Q("0m"),
                                            Q("0m"))

        mod_pos4 = geom.structure.Position( 'modpos4'+self.name,
                                            +0.5*Q("0.036m")*32+Q("0.007m"),    # position center of module (slightly right) and add gap
                                            Q("0m"),
                                            Q("0m"))
        
        mod_pos5 = geom.structure.Position( 'modpos5'+self.name,
                                            +1.5*Q("0.036m")*32+Q("0.014m"),    # position center of module (middle right) and add sum of gaps
                                            Q("0m"),
                                            Q("0m"))
        
        mod_pos6 = geom.structure.Position( 'modpos6'+self.name,
                                            +2.5*Q("0.036m")*32+Q("0.021m"),    # position center of module (very right) and add sum of gaps
                                            Q("0m"),
                                            Q("0m"))

        mod_pos1_ortho = geom.structure.Position( 'modpos1_ortho'+self.name,
                                            -Q("1.750m")-Q("0.001m"),           # half of module length and assuming a gap between the sides of 2mm (left)
                                            +1.0*Q("0.036m")*32+Q("0.014m"),    # full module to center of module (up) and add sum of gaps
                                            Q("0m"))

        mod_pos2_ortho = geom.structure.Position( 'modpos2_ortho'+self.name,
                                            +Q("1.750m")+Q("0.001m"),           # half of module length and assuming a gap between the sides of 2mm (right)
                                            +1.0*Q("0.036m")*32+Q("0.014m"),    # same as for mod_pos1_ortho
                                            Q("0m"))

        mod_pos3_ortho = geom.structure.Position( 'modpos3_ortho'+self.name,
                                            -Q("1.750m")-Q("0.001m"),           # same as for mod_pos1_ortho
                                            Q("0m"),                            # middle module is heightwise at the center
                                            Q("0m"))
        
        mod_pos4_ortho = geom.structure.Position( 'modpos4_ortho'+self.name,
                                            +Q("1.750m")+Q("0.001m"),           # same as for mod_pos2_ortho
                                            Q("0m"),                            # same as for mod_pos3_ortho
                                            Q("0m"))

        mod_pos5_ortho = geom.structure.Position( 'modpos5_ortho'+self.name,
                                            -Q("1.750m")-Q("0.001m"),           # same as for mod_pos1_ortho
                                            -1.0*Q("0.036m")*32-Q("0.014m"),    # full module to center of module (down) and add sum of gaps
                                            Q("0m"))

        mod_pos6_ortho = geom.structure.Position( 'modpos6_ortho'+self.name,
                                            +Q("1.750m")+Q("0.001m"),           # same as for mod_pos2_ortho
                                            -1.0*Q("0.036m")*32-Q("0.014m"),    # same as for mod_pos5_ortho
                                            Q("0m"))


        mod_ri_pla1 = geom.structure.Placement( 'modripla1'+self.name, volume=  ModuleBox_lv, pos=mod_pos1, rot = Mod_ri_rot)
        mod_le_pla1 = geom.structure.Placement( 'modlepla1'+self.name, volume=  ModuleBox_lv, pos=mod_pos1, rot = Mod_left_rot)
        mod_ortho_pla1 = geom.structure.Placement( 'modorthopla1'+self.name, volume= ModuleBox_lv_ortho, pos=mod_pos1_ortho)

        mod_ri_pla2 = geom.structure.Placement( 'modripla2'+self.name, volume=  ModuleBox_lv, pos=mod_pos2, rot = Mod_ri_rot)
        mod_le_pla2 = geom.structure.Placement( 'modlepla2'+self.name, volume=  ModuleBox_lv, pos=mod_pos2, rot = Mod_left_rot)
        mod_ortho_pla2 = geom.structure.Placement( 'modorthopla2'+self.name, volume= ModuleBox_lv_ortho, pos=mod_pos2_ortho)

        mod_ri_pla3 = geom.structure.Placement( 'modripla3'+self.name, volume=  ModuleBox_lv, pos=mod_pos3, rot = Mod_ri_rot)
        mod_le_pla3 = geom.structure.Placement( 'modlepla3'+self.name, volume=  ModuleBox_lv, pos=mod_pos3, rot = Mod_left_rot)
        mod_ortho_pla3 = geom.structure.Placement( 'modorthopla3'+self.name, volume= ModuleBox_lv_ortho, pos=mod_pos3_ortho)

        mod_ri_pla4 = geom.structure.Placement( 'modripla4'+self.name, volume=  ModuleBox_lv, pos=mod_pos4, rot = Mod_ri_rot)
        mod_le_pla4 = geom.structure.Placement( 'modlepla4'+self.name, volume=  ModuleBox_lv, pos=mod_pos4, rot = Mod_left_rot)
        mod_ortho_pla4 = geom.structure.Placement( 'modorthopla4'+self.name, volume= ModuleBox_lv_ortho, pos=mod_pos4_ortho)

        mod_ri_pla5 = geom.structure.Placement( 'modripla5'+self.name, volume=  ModuleBox_lv, pos=mod_pos5, rot = Mod_ri_rot)
        mod_le_pla5 = geom.structure.Placement( 'modlepla5'+self.name, volume=  ModuleBox_lv, pos=mod_pos5, rot = Mod_left_rot)
        mod_ortho_pla5 = geom.structure.Placement( 'modorthopla5'+self.name, volume= ModuleBox_lv_ortho, pos=mod_pos5_ortho)

        mod_ri_pla6 = geom.structure.Placement( 'modripla6'+self.name, volume=  ModuleBox_lv, pos=mod_pos6, rot = Mod_ri_rot)
        mod_le_pla6 = geom.structure.Placement( 'modlepla6'+self.name, volume=  ModuleBox_lv, pos=mod_pos6, rot = Mod_left_rot)
        mod_ortho_pla6 = geom.structure.Placement( 'modorthopla6'+self.name, volume= ModuleBox_lv_ortho, pos=mod_pos6_ortho)

        Module_layer_lv1.placements.append(mod_ri_pla1.name)
        Module_layer_lv2.placements.append(mod_le_pla1.name)
        Module_layer_lv3.placements.append(mod_ortho_pla1.name)

        Module_layer_lv1.placements.append(mod_ri_pla2.name)
        Module_layer_lv2.placements.append(mod_le_pla2.name)
        Module_layer_lv3.placements.append(mod_ortho_pla2.name)

        Module_layer_lv1.placements.append(mod_ri_pla3.name)
        Module_layer_lv2.placements.append(mod_le_pla3.name)
        Module_layer_lv3.placements.append(mod_ortho_pla3.name)

        Module_layer_lv1.placements.append(mod_ri_pla4.name)
        Module_layer_lv2.placements.append(mod_le_pla4.name)
        Module_layer_lv3.placements.append(mod_ortho_pla4.name)

        Module_layer_lv1.placements.append(mod_ri_pla5.name)
        Module_layer_lv2.placements.append(mod_le_pla5.name)
        Module_layer_lv3.placements.append(mod_ortho_pla5.name)

        Module_layer_lv1.placements.append(mod_ri_pla6.name)
        Module_layer_lv2.placements.append(mod_le_pla6.name)
        Module_layer_lv3.placements.append(mod_ortho_pla6.name)

        #Place Layers into RMS vol
        Module_layers_thin = 50
        thinModlayer_pos = [geom.structure.Position('k')]*Module_layers_thin
        thin_Modlayer_pla = [geom.structure.Placement('l',volume=Module_layer_lv1,pos=thinModlayer_pos[1])]*Module_layers_thin

        hybrid = True

        if hybrid:
            # set U layer for double layer of scintillator in first layer
            thinModlayer_pos_first = [geom.structure.Position('q')]*51
            thin_Modlayer_pla_first = [geom.structure.Placement('r',volume=Module_layer_lv1,pos=thinModlayer_pos[1])]*51
            zpos = -Q("3.650m") -Q("0.0325m") + Q("0.0075m") - Q("0.051m") - Q("0.001m")     # first layer of thin steel - half thin steel thickness - half gap - full scintillator width - 1mm for space between modules
            thinModlayer_pos_first[0] = geom.structure.Position( 'thinModlayerposition'+str(0),
                                                            x = xpos_planes,
                                                            y = ypos_planes,
                                                            z = zpos)

            thin_Modlayer_pla_first[0] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(0), volume=Module_layer_lv2, pos=thinModlayer_pos_first[0] )     #v (To uphold the pattern and not uXuv)
            tms_lv.placements.append(thin_Modlayer_pla_first[0].name)

            #hybrid version (XUV)
            for module in range(1, Module_layers_thin + 1):
                zpos = -Q("3.650m") -Q("0.0325m") + (module-1) * Q("0.065m") + Q("0.0075m")     # first layer of thin steel - half thin steel thickness - half gap
                thinModlayer_pos_first[module] = geom.structure.Position( 'thinModlayerposition'+str(module),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            
                if module in self.thin_horizontal:   #(module-1) % 3 == 0 :
                    thin_Modlayer_pla_first[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv3, pos=thinModlayer_pos_first[module] )  #x
    
                elif module in self.thin_U:          #(module-1) % 3 == 1:
                    thin_Modlayer_pla_first[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv1, pos=thinModlayer_pos_first[module] )  #u
    
                elif module in self.thin_V:          #(module-1) % 3 == 2:
                    thin_Modlayer_pla_first[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv2, pos=thinModlayer_pos_first[module] )  #v
                
                tms_lv.placements.append(thin_Modlayer_pla_first[module].name)
        else:
            #stereo version (UV)
            for module in range(Module_layers_thin):
                zpos = -Q("3.650m") -Q("0.0325m") + module * Q("0.065m") + Q("0.0075m")     # first layer of thin steel - half thin steel thickness - half gap
                thinModlayer_pos[module] = geom.structure.Position( 'thinModlayerposition'+str(module),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)

                if module % 2 == 0 :
                   thin_Modlayer_pla[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv1, pos=thinModlayer_pos[module] )   #u
    
                else:
                    thin_Modlayer_pla[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv2, pos=thinModlayer_pos[module] )  #v

                tms_lv.placements.append(thin_Modlayer_pla[module].name)


        #Place Layers into RMS vol between thick layers                                                                                 
        Module_layers_thick = 34
        thickModlayer_pos = [geom.structure.Position('m')]*Module_layers_thick
        thick_Modlayer_pla = [geom.structure.Placement('n',volume=Module_layer_lv1,pos=thickModlayer_pos[1])]*Module_layers_thick    

        for module in range(0, Module_layers_thick):
            zpos = -Q("0.3875m") - Q("0.045m")  + module * Q("0.09m") + Q("0.0075m")    # first layer of thick steel - half thick steel thickness - half gap
            thickModlayer_pos[module] = geom.structure.Position( 'thickModlayerposition'+str(module),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            
            if hybrid:
                #hybrid version (XUV)
                if module in self.thick_horizontal:  #module % 3 == 0 :    #this handling is done to ensure a even distribution of ortho layers also across the different thicknesses (XuvXu->vXuvXuv)
                    thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv3, pos=thickModlayer_pos[module] )   #x  #2, pos=thickModlayer_pos[module] )   #v

                elif module in self.thick_U:         #module % 3 == 1:
                    thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv1, pos=thickModlayer_pos[module] )   #u  #3, pos=thickModlayer_pos[module] )   #x

                elif module in self.thick_V:         #module % 3 == 2:
                    thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv2, pos=thickModlayer_pos[module] )   #v  #1, pos=thickModlayer_pos[module] )   #u
            else:
                #stereo version (UV)
                if module % 2 == 0 :
                     thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv1, pos=thickModlayer_pos[module] )  #u
                    
                else:             
                    thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv2, pos=thickModlayer_pos[module] )   #v

            tms_lv.placements.append(thick_Modlayer_pla[module].name)

        
        #Place Layers into RMS vol between double layers
        Module_layers_double = 9
        doubleModlayer_pos = [geom.structure.Position('o')]*Module_layers_double
        double_Modlayer_pla = [geom.structure.Placement('p',volume=Module_layer_lv1,pos=doubleModlayer_pos[1])]*Module_layers_double

        for module in range(0,Module_layers_double):
            zpos = +Q("2.6925m") - Q("0.065m") + module * Q("0.130m") + Q("0.0075m")    # first layer of double steel - half double steel thickness - half gap
            doubleModlayer_pos[module] = geom.structure.Position( 'doubleModlayerposition'+str(module),
                                                            x = xpos_planes,
                                                            y = ypos_planes,
                                                            z = zpos)

            if hybrid:
                #hybrid version (XUV)
                if module in self.double_horizontal: #module % 3 == 0 :    #here the handling is not necessary as it just works
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv3, pos=doubleModlayer_pos[module] )    #x

                elif module in self.double_U:        #module % 3 == 1:
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv1, pos=doubleModlayer_pos[module] )    #u

                elif module in self.double_V:        #module % 3 == 2:
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv2, pos=doubleModlayer_pos[module] )    #v
            else:
                #stereo version (UV)
                if module % 2 == 0:
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv1, pos=doubleModlayer_pos[module] )    #u
    
                else:
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv2, pos=doubleModlayer_pos[module] )    #v

            tms_lv.placements.append(double_Modlayer_pla[module].name)

        #Add TMS to self
        self.add_volume(tms_lv)

        
