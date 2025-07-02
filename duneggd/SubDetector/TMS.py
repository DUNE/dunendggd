#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q
global Pos
class tmsBuilder(gegede.builder.Builder):
    def configure(self, mat=None, thinbox1Dimension=None, gapPosition=None, BFieldUpLow = None, BFieldUpHigh = None, BFieldDownLow = None , BFieldDownHigh = None, thin_horizontal=None, thick_horizontal=None, double_horizontal=None, thin_U=None, thick_U=None, double_U=None, thin_V=None, thick_V=None, double_V=None,  **kwds):    #thinbox2Dimension=None
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

        six_width = False
        hybrid = False #4.2c
        XY = False #4.2d
        PDR = True #7m, 3.2b

            
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

        #80 steel layers, 34 thin, 22 thinck and 24 double.

        n_thin_steel = 34#50
        thinlayer_pos = [geom.structure.Position('a')]*n_thin_steel
        thin_layer_pla = [geom.structure.Placement('b',volume=thin_layer_lv,pos=thinlayer_pos[1])]*n_thin_steel

        # All the planes of steel and scintillator have the same x and y position
        xpos_planes = Q("0m")
        ypos_planes = Q("0.85m") # this is the vertical position w.r.t. the main tms box

        moduleplusgapthickness=Q("0.50m")

        for plane in range(n_thin_steel):
            # zpos changes with each layer
            zpos = -Q("3.650m") + plane * Q("0.065m") # Q("0.0075m")    # half of total steel thickness with gaps (7300mm) and shift for differing air gaps for thin and double plates
            thinlayer_pos[plane] = geom.structure.Position( 'thinlayerposition'+str(plane),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            thin_layer_pla[plane] = geom.structure.Placement( 'thinlayerpla'+self.name+str(plane), volume=thin_layer_lv, pos=thinlayer_pos[plane] )
            tms_lv.placements.append(thin_layer_pla[plane].name)
            #print(plane,zpos)

        #Thick Layer Placement
        n_thick_steel = 22#34
        thicklayer_pos = [geom.structure.Position('c')]*n_thick_steel
        thick_layer_pla = [geom.structure.Placement('d',volume=thick_layer_lv, pos=thicklayer_pos[1])]*n_thick_steel
        
        for plane in range(n_thick_steel):
            #last position=-Q("3.650m") + (n_thin_steel-1) * Q("0.065m") 
            zpos = -Q("1.4075m")+ plane * Q("0.09m")     # last positon+half of previous (steel thickness+gap) + plane thickness
            thicklayer_pos[plane] = geom.structure.Position( 'thicklayerposition'+str(plane),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            thick_layer_pla[plane] = geom.structure.Placement( 'thicklayerpla'+self.name+str(plane), volume=thick_layer_lv, pos=thicklayer_pos[plane] )
            tms_lv.placements.append(thick_layer_pla[plane].name)
        
        #Double Layer Placement
        n_double_steel = 24#8
        doublelayer_pos = [geom.structure.Position('e')]*n_double_steel #e was scintillator so far!!!
        double_layer_pla = [geom.structure.Placement('f',volume=double_layer_lv, pos=doublelayer_pos[1])]*n_double_steel    #f was scintillator so far!!!

        for plane in range(n_double_steel):
            zpos = +Q("0.5275m")+ plane * Q("0.13m")     # last positon+half of previous (steel thickness+gap) + plane thickness
            doublelayer_pos[plane] = geom.structure.Position( 'doublelayerposition'+str(plane),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            double_layer_pla[plane] = geom.structure.Placement( 'doublelayerpla'+self.name+str(plane), volume=double_layer_lv, pos=doublelayer_pos[plane] )
            tms_lv.placements.append(double_layer_pla[plane].name)


        # Scintillator
        # Individual scintillator bar
        #0.01010526316*114
        #0.02618181818*44
        #0.03031578947*38
        #0.04430769231*26
        #0.0576*20
        #0.064*18
        #0.072*16
        #0.288*4
        barwidth=0.036
        barnumber=32
        middlepos=barwidth*barnumber/2-barwidth/2
        
        length_orth=3.5
        if six_width: length_orth=2.880 
        #scintillator= bar thickness=16mm
        scinBox = geom.shapes.Box( 'scinbox'+self.name,
                                    dx = 0.5*Q(f"{barwidth}m"),   # width single bar
                                    dy = 0.5*Q("3.300m"),   # length bar for stereo bars
                                    dz = 0.5*Q("0.016m"))   # thickness single bar
        
        scinBox_ortho = geom.shapes.Box( 'scinbox_ortho'+self.name,
                                    dx = 0.5*Q(f"{length_orth}m"),   # length bar for orthogonal bars
                                    dy = 0.5*Q(f"{barwidth}m"),   # width single bar
                                    dz = 0.5*Q("0.016m"))   # thickness single bar

        scinBox_parallel = geom.shapes.Box( 'scinbox_parallel'+self.name,
                                    dx = 0.5*Q(f"{barwidth}m"),   # width single bar
                                    dy = 0.5*Q("3.500m"),   # length bar for stereo bars
                                    dz = 0.5*Q("0.016m"))   # thickness single bar


        scinBox_lv = geom.structure.Volume( 'scinBoxlv'+self.name, material='Scintillator', shape=scinBox)
        scinBox_lv.params.append(("SensDet", tms_lv.name))

        scinBox_lv_ortho = geom.structure.Volume( 'scinBoxlv_ortho'+self.name, material='Scintillator', shape=scinBox_ortho)
        scinBox_lv_ortho.params.append(("SensDet", tms_lv.name))

        scinBox_lv_parallel = geom.structure.Volume( 'scinBoxlv_parallel'+self.name, material='Scintillator', shape=scinBox_parallel)
        scinBox_lv_parallel.params.append(("SensDet", tms_lv.name))

        # Place Bars into Modules
        ModuleBox = geom.shapes.Box( 'ModuleBox',
                                     dx = 0.5*Q(f"{barwidth}m")*barnumber,   # width single bar
                                     dy = 0.5*Q("3.300m"),       # Same length as single stereo bar
                                     dz = 0.5*Q("0.017m"))       # Same thickness as single bar

        ModuleBox_ortho = geom.shapes.Box( 'ModuleBox_ortho',
                                    dx = 0.5*Q(f"{length_orth}m"),        # Same length as single orthogonal bar
                                     dy = 0.5*Q(f"{barwidth}m")*barnumber,   # width single bar
                                    dz = 0.5*Q("0.017m"))        # Same thickness as single bar

        ModuleBox_parallel = geom.shapes.Box( 'ModuleBox_parallel',
                                     dx = 0.5*Q(f"{barwidth}m")*barnumber,   # width single bar
                                     dy = 0.5*Q("3.500m"),# + Q("0.001m")       # Same length as single stereo bar
                                     dz = 0.5*Q("0.017m"))# + Q("0.001m"))      # Same thickness as single bar

        ModuleBox_lv = geom.structure.Volume( 'ModuleBoxvol', material='Air', shape=ModuleBox )

        ModuleBox_lv_ortho = geom.structure.Volume( 'ModuleBoxvol_ortho', material='Air', shape=ModuleBox_ortho)
        
        ModuleBox_lv_parallel = geom.structure.Volume( 'ModuleBoxvol_parallel', material='Air', shape=ModuleBox_parallel)

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
        #sci_bars = 32
        sci_bars = barnumber
        sci_Bar_pos = [geom.structure.Position('g')]*sci_bars
        sci_Bar_pla = [geom.structure.Placement('h',volume=scinBox_lv, pos=sci_Bar_pos[1])]*sci_bars

        sci_Bar_pos_ortho = [geom.structure.Position('i')]*sci_bars
        sci_Bar_pla_ortho = [geom.structure.Placement('j', volume=scinBox_lv_ortho, pos=sci_Bar_pos_ortho[1])]*sci_bars

        sci_Bar_pos_parallel = [geom.structure.Position('z')]*sci_bars
        sci_Bar_pla_parallel = [geom.structure.Placement('w',volume=scinBox_lv_parallel, pos=sci_Bar_pos_parallel[1])]*sci_bars

        # y and z positions are the same for each bar
        zpos_bar = Q("0m") 
        ypos_bar = Q("0m")

        zpos_bar_ortho = Q("0m")
        xpos_bar_ortho = Q("0m")

        zpos_bar_parallel = Q("0m")
        ypos_bar_parallel = Q("0m")

        for bar in range(sci_bars):
            xpos = -Q(f"{middlepos}m")+ bar * Q(f"{barwidth}m")          # middle of last bar in single module (-16*bar width + half bar width)
            sci_Bar_pos[bar] = geom.structure.Position( 'sci_barposition'+str(bar),
                                                           x = xpos,
                                                           y = ypos_bar,
                                                           z = zpos_bar)

            sci_Bar_pla[bar] = geom.structure.Placement( 'scibarpla'+self.name+str(bar), volume=scinBox_lv, pos=sci_Bar_pos[bar] )
            ModuleBox_lv.placements.append(sci_Bar_pla[bar].name)

            ypos_ortho = -Q(f"{middlepos}m") + bar * Q(f"{barwidth}m")  # middle of last bar in single module (-16*bar width + half bar width)
            sci_Bar_pos_ortho[bar] = geom.structure.Position( 'sci_barposition_ortho'+str(bar),
                                                            x = xpos_bar_ortho,
                                                            y = ypos_ortho,
                                                            z = zpos_bar_ortho)
            sci_Bar_pla_ortho[bar] = geom.structure.Placement( 'scibarpla_ortho'+self.name+str(bar), volume=scinBox_lv_ortho, pos = sci_Bar_pos_ortho[bar])
            ModuleBox_lv_ortho.placements.append(sci_Bar_pla_ortho[bar].name)

            sci_Bar_pos_parallel[bar] = geom.structure.Position( 'sci_barposition_parallel'+str(bar),
                                                           x = xpos,
                                                           y = ypos_bar_parallel,
                                                           z = zpos_bar_parallel)
            sci_Bar_pla_parallel[bar] = geom.structure.Placement( 'scibarpla_parallel'+self.name+str(bar), volume=scinBox_lv_parallel, pos=sci_Bar_pos_parallel[bar] )
            ModuleBox_lv_parallel.placements.append(sci_Bar_pla_parallel[bar].name)

        # Place Modules into scint layers
        modules_in_layer = 6
        Module_layer = geom.shapes.Box( 'Modulelayerbox',
                                      dx = 0.5*Q("7.500m"), #7.04   # make it fit
                                      dy = 0.5*Q("3.500m"), #4.700m # about 3*module width
                                      dz = 0.5*Q("0.050m"))         # fill entire gap between steel

        Module_layer_lv1 = geom.structure.Volume( 'modulelayervol1', material='Air', shape=Module_layer )
        Module_layer_lv2 = geom.structure.Volume( 'modulelayervol2', material='Air', shape=Module_layer )
        Module_layer_lv3 = geom.structure.Volume( 'modulelayervol3', material='Air', shape=Module_layer )#X
        Module_layer_lv4 = geom.structure.Volume( 'modulelayervol4', material='Air', shape=Module_layer )

        #Position modules in layer                                                                                            
        Mod_ri_rot = geom.structure.Rotation( 'Modrirot', '0deg','0deg','3deg')
        Mod_left_rot = geom.structure.Rotation( 'Modleftrot', '0deg','0deg','-3deg')
        #it depends on how we define the position below but in this code  we don't use it anyway.
        Mod_ortho_rot = geom.structure.Rotation( 'Modorthorot', '0deg', '0deg', '0deg')
        Mod_parallel_rot = geom.structure.Rotation( 'Modparalrot', '0deg', '0deg', '0deg') # Y Bar


        if not six_width:
            mod_pos1 = geom.structure.Position( 'modpos1'+self.name,
                                                -2.5*Q(f"{barwidth}m")*barnumber-Q("0.021m"),    # position center of module (very left) and add sum of gaps
                                                #-2.5*Q("0.036m")*32-Q("0.021m"),    # position center of module (very left) and add sum of gaps
                                                Q("0m"),
                                                Q("0m"))

            mod_pos2 = geom.structure.Position( 'modpos2'+self.name,
                                                -1.5*Q(f"{barwidth}m")*barnumber-Q("0.014m"),    # position center of module (middle left) and add sum of gaps
                                                #-1.5*Q("0.036m")*32-Q("0.014m"),    # position center of module (middle left) and add sum of gaps
                                                Q("0m"),
                                                Q("0m"))

            mod_pos3 = geom.structure.Position( 'modpos3'+self.name,
                                                -0.5*Q(f"{barwidth}m")*barnumber-Q("0.007m"),    # position center of module (slightly left) and add gap
                                                #-0.5*Q("0.036m")*32-Q("0.007m"),    # position center of module (slightly left) and add gap
                                                Q("0m"),
                                                Q("0m"))

            mod_pos4 = geom.structure.Position( 'modpos4'+self.name,
                                                +0.5*Q(f"{barwidth}m")*barnumber+Q("0.007m"),    # position center of module (slightly right) and add gap
                                                #+0.5*Q("0.036m")*32+Q("0.007m"),    # position center of module (slightly right) and add gap
                                                Q("0m"),
                                                Q("0m"))
            
            mod_pos5 = geom.structure.Position( 'modpos5'+self.name,
                                                +1.5*Q(f"{barwidth}m")*barnumber+Q("0.014m"),    # position center of module (middle right) and add sum of gaps
                                                #+1.5*Q("0.036m")*32+Q("0.014m"),    # position center of module (middle right) and add sum of gaps
                                                Q("0m"),
                                                Q("0m"))
            
            mod_pos6 = geom.structure.Position( 'modpos6'+self.name,
                                                +2.5*Q(f"{barwidth}m")*barnumber+Q("0.021m"),    # position center of module (very right) and add sum of gaps
                                                #+2.5*Q("0.036m")*32+Q("0.021m"),    # position center of module (very right) and add sum of gaps
                                                Q("0m"),
                                                Q("0m"))

        #For 5vertical
        if six_width:
            mod_pos1 = geom.structure.Position( 'modpos1'+self.name,
                                               -2.0*Q(f"{barwidth}m")*barnumber-Q("0.021m"),    # position center of module (very left) and add sum of gaps
                                               #-2.5*Q("0.036m")*32-Q("0.021m"),    # position center of module (very left) and add sum of gaps
                                               Q("0m"),
                                               Q("0m"))

            mod_pos2 = geom.structure.Position( 'modpos2'+self.name,
                                           -1.0*Q(f"{barwidth}m")*barnumber-Q("0.014m"),    # position center of module (middle left) and add sum of gaps
                                           #-1.5*Q("0.036m")*32-Q("0.014m"),    # position center of module (middle left) and add sum of gaps
                                           Q("0m"),
                                           Q("0m"))

            mod_pos3 = geom.structure.Position( 'modpos3'+self.name,
                                           -0.0*Q(f"{barwidth}m")*barnumber-Q("0.007m"),    # position center of module (slightly left) and add gap
                                           #-0.5*Q("0.036m")*32-Q("0.007m"),    # position center of module (slightly left) and add gap
                                           Q("0m"),
                                           Q("0m"))

            mod_pos4 = geom.structure.Position( 'modpos4'+self.name,
                                           +1.0*Q(f"{barwidth}m")*barnumber+Q("0.007m"),    # position center of module (slightly right) and add gap
                                           #+0.5*Q("0.036m")*32+Q("0.007m"),    # position center of module (slightly right) and add gap
                                           Q("0m"),
                                           Q("0m"))

            mod_pos5 = geom.structure.Position( 'modpos5'+self.name,
                                           +2.0*Q(f"{barwidth}m")*barnumber+Q("0.014m"),    # position center of module (middle right) and add sum of gaps
                                           #+1.5*Q("0.036m")*32+Q("0.014m"),    # position center of module (middle right) and add sum of gaps
                                           Q("0m"),
                                           Q("0m"))
        ####################################################################################################################################################33

        halflen_ortho=length_orth/2

        mod_pos1_ortho = geom.structure.Position( 'modpos1_ortho'+self.name,
                                            -Q(f"{halflen_ortho}m")-Q("0.001m"),           # half of module length and assuming a gap between the sides of 2mm (left)
                                            +1.0*Q(f"{barwidth}m")*barnumber+Q("0.014m"),    # full module to center of module (up) and add sum of gaps
                                            #+1.0*Q("0.036m")*32+Q("0.014m"),    # full module to center of module (up) and add sum of gaps
                                            Q("0m"))

        mod_pos2_ortho = geom.structure.Position( 'modpos2_ortho'+self.name,
                                            +Q(f"{halflen_ortho}m")+Q("0.001m"),           # half of module length and assuming a gap between the sides of 2mm (right)
                                            +1.0*Q(f"{barwidth}m")*barnumber+Q("0.014m"),    # same as for mod_pos1_ortho
                                            #+1.0*Q("0.036m")*32+Q("0.014m"),    # same as for mod_pos1_ortho
                                            Q("0m"))

        mod_pos3_ortho = geom.structure.Position( 'modpos3_ortho'+self.name,
                                            -Q(f"{halflen_ortho}m")-Q("0.001m"),           # same as for mod_pos1_ortho
                                            Q("0m"),                            # middle module is heightwise at the center
                                            Q("0m"))
        
        mod_pos4_ortho = geom.structure.Position( 'modpos4_ortho'+self.name,
                                            +Q(f"{halflen_ortho}m")+Q("0.001m"),           # same as for mod_pos2_ortho
                                            Q("0m"),                            # same as for mod_pos3_ortho
                                            Q("0m"))

        mod_pos5_ortho = geom.structure.Position( 'modpos5_ortho'+self.name,
                                            -Q(f"{halflen_ortho}m")-Q("0.001m"),           # same as for mod_pos1_ortho
                                            -1.0*Q(f"{barwidth}m")*barnumber-Q("0.014m"),    # full module to center of module (down) and add sum of gaps
                                            #-1.0*Q("0.036m")*32-Q("0.014m"),    # full module to center of module (down) and add sum of gaps
                                            Q("0m"))

        mod_pos6_ortho = geom.structure.Position( 'modpos6_ortho'+self.name,
                                            +Q(f"{halflen_ortho}m")+Q("0.001m"),           # same as for mod_pos2_ortho
                                            -1.0*Q(f"{barwidth}m")*barnumber-Q("0.014m"),    # same as for mod_pos5_ortho
                                            #-1.0*Q("0.036m")*32-Q("0.014m"),    # same as for mod_pos5_ortho
                                            Q("0m"))


        mod_ri_pla1 = geom.structure.Placement( 'modripla1'+self.name, volume=  ModuleBox_lv, pos=mod_pos1, rot = Mod_ri_rot)
        mod_le_pla1 = geom.structure.Placement( 'modlepla1'+self.name, volume=  ModuleBox_lv, pos=mod_pos1, rot = Mod_left_rot)
        mod_ortho_pla1 = geom.structure.Placement( 'modorthopla1'+self.name, volume= ModuleBox_lv_ortho, pos=mod_pos1_ortho)
        mod_parallel_pla1 = geom.structure.Placement( 'modparallelpla1'+self.name, volume= ModuleBox_lv_parallel, pos=mod_pos1, rot = Mod_parallel_rot)

        mod_ri_pla2 = geom.structure.Placement( 'modripla2'+self.name, volume=  ModuleBox_lv, pos=mod_pos2, rot = Mod_ri_rot)
        mod_le_pla2 = geom.structure.Placement( 'modlepla2'+self.name, volume=  ModuleBox_lv, pos=mod_pos2, rot = Mod_left_rot)
        mod_ortho_pla2 = geom.structure.Placement( 'modorthopla2'+self.name, volume= ModuleBox_lv_ortho, pos=mod_pos2_ortho)
        mod_parallel_pla2 = geom.structure.Placement( 'modparallelpla2'+self.name, volume= ModuleBox_lv_parallel, pos=mod_pos2, rot = Mod_parallel_rot)

        mod_ri_pla3 = geom.structure.Placement( 'modripla3'+self.name, volume=  ModuleBox_lv, pos=mod_pos3, rot = Mod_ri_rot)
        mod_le_pla3 = geom.structure.Placement( 'modlepla3'+self.name, volume=  ModuleBox_lv, pos=mod_pos3, rot = Mod_left_rot)
        mod_ortho_pla3 = geom.structure.Placement( 'modorthopla3'+self.name, volume= ModuleBox_lv_ortho, pos=mod_pos3_ortho)
        mod_parallel_pla3 = geom.structure.Placement( 'modparallelpla3'+self.name, volume= ModuleBox_lv_parallel, pos=mod_pos3, rot = Mod_parallel_rot)

        mod_ri_pla4 = geom.structure.Placement( 'modripla4'+self.name, volume=  ModuleBox_lv, pos=mod_pos4, rot = Mod_ri_rot)
        mod_le_pla4 = geom.structure.Placement( 'modlepla4'+self.name, volume=  ModuleBox_lv, pos=mod_pos4, rot = Mod_left_rot)
        mod_ortho_pla4 = geom.structure.Placement( 'modorthopla4'+self.name, volume= ModuleBox_lv_ortho, pos=mod_pos4_ortho)
        mod_parallel_pla4 = geom.structure.Placement( 'modparallelpla4'+self.name, volume= ModuleBox_lv_parallel, pos=mod_pos4, rot = Mod_parallel_rot)

        mod_ri_pla5 = geom.structure.Placement( 'modripla5'+self.name, volume=  ModuleBox_lv, pos=mod_pos5, rot = Mod_ri_rot)
        mod_le_pla5 = geom.structure.Placement( 'modlepla5'+self.name, volume=  ModuleBox_lv, pos=mod_pos5, rot = Mod_left_rot)
        mod_ortho_pla5 = geom.structure.Placement( 'modorthopla5'+self.name, volume= ModuleBox_lv_ortho, pos=mod_pos5_ortho)
        mod_parallel_pla5 = geom.structure.Placement( 'modparallelpla5'+self.name, volume= ModuleBox_lv_parallel, pos=mod_pos5, rot = Mod_parallel_rot)

        mod_ortho_pla6 = geom.structure.Placement( 'modorthopla6'+self.name, volume= ModuleBox_lv_ortho, pos=mod_pos6_ortho)

        if not six_width: #i.e. 6 vertical modules
            mod_ri_pla6 = geom.structure.Placement( 'modripla6'+self.name, volume=  ModuleBox_lv, pos=mod_pos6, rot = Mod_ri_rot)
            mod_le_pla6 = geom.structure.Placement( 'modlepla6'+self.name, volume=  ModuleBox_lv, pos=mod_pos6, rot = Mod_left_rot)
            mod_parallel_pla6 = geom.structure.Placement( 'modparallelpla6'+self.name, volume= ModuleBox_lv_parallel, pos=mod_pos6, rot = Mod_parallel_rot)

        Module_layer_lv1.placements.append(mod_ri_pla1.name)
        Module_layer_lv2.placements.append(mod_le_pla1.name)
        Module_layer_lv3.placements.append(mod_ortho_pla1.name)
        Module_layer_lv4.placements.append(mod_parallel_pla1.name)

        Module_layer_lv1.placements.append(mod_ri_pla2.name)
        Module_layer_lv2.placements.append(mod_le_pla2.name)
        Module_layer_lv3.placements.append(mod_ortho_pla2.name)
        Module_layer_lv4.placements.append(mod_parallel_pla2.name)

        Module_layer_lv1.placements.append(mod_ri_pla3.name)
        Module_layer_lv2.placements.append(mod_le_pla3.name)
        Module_layer_lv3.placements.append(mod_ortho_pla3.name)
        Module_layer_lv4.placements.append(mod_parallel_pla3.name)

        Module_layer_lv1.placements.append(mod_ri_pla4.name)
        Module_layer_lv2.placements.append(mod_le_pla4.name)
        Module_layer_lv3.placements.append(mod_ortho_pla4.name)
        Module_layer_lv4.placements.append(mod_parallel_pla4.name)

        Module_layer_lv1.placements.append(mod_ri_pla5.name)
        Module_layer_lv2.placements.append(mod_le_pla5.name)
        Module_layer_lv3.placements.append(mod_ortho_pla5.name)
        Module_layer_lv4.placements.append(mod_parallel_pla5.name)

        Module_layer_lv3.placements.append(mod_ortho_pla6.name)

        if not six_width: #i.e. 6 vertical modules
            Module_layer_lv1.placements.append(mod_ri_pla6.name)
            Module_layer_lv2.placements.append(mod_le_pla6.name)
            Module_layer_lv4.placements.append(mod_parallel_pla6.name)




        #For_5_verticals
        #Module_layer_lv1.placements.append(mod_ri_pla6.name)
        #Module_layer_lv2.placements.append(mod_le_pla6.name)
        #For_5_verticals

        #Place Layers into RMS vol
        Module_layers_thin = 34#50
        thinModlayer_pos = [geom.structure.Position('k')]*Module_layers_thin
        thin_Modlayer_pla = [geom.structure.Placement('l',volume=Module_layer_lv1,pos=thinModlayer_pos[1])]*Module_layers_thin

        
        if hybrid:
            # set U layer for double layer of scintillator in first layer
            thinModlayer_pos_first = [geom.structure.Position('q')]*(Module_layers_thin+1)
            thin_Modlayer_pla_first = [geom.structure.Placement('r',volume=Module_layer_lv1,pos=thinModlayer_pos[1])]*(Module_layers_thin+1)
            zpos = -Q("3.650m") -Q("0.0325m") + Q("0.0065m") - Q("0.051m")#- Q("0.051m") - Q("0.001m")     # first layer of thin steel - half thin steel thickness - half gap - full scintillator width - 1mm for space between modules
            thinModlayer_pos_first[0] = geom.structure.Position( 'thinModlayerposition'+str(0),
                                                            x = xpos_planes,
                                                            y = ypos_planes,
                                                            z = zpos)

            thin_Modlayer_pla_first[0] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(0), volume=Module_layer_lv2, pos=thinModlayer_pos_first[0] )     #v (To uphold the pattern and not uXuv)
            tms_lv.placements.append(thin_Modlayer_pla_first[0].name)

            #hybrid version (XUV)
            for module in range(1, Module_layers_thin + 1):
                zpos = -Q("3.650m") -Q("0.0325m") + (module-1) * Q("0.065m")#     # first layer of thin steel - half steel+gap thickness - half gap
                thinModlayer_pos_first[module] = geom.structure.Position( 'thinModlayerposition'+str(module),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            
                if module in self.thin_horizontal:
                    thin_Modlayer_pla_first[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv3, pos=thinModlayer_pos_first[module] )  #x
    
                if module in self.thin_U:
                    thin_Modlayer_pla_first[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv1, pos=thinModlayer_pos_first[module] )  #u
    
                if module in self.thin_V:
                    thin_Modlayer_pla_first[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv2, pos=thinModlayer_pos_first[module] )  #v
                
                tms_lv.placements.append(thin_Modlayer_pla_first[module].name)
        elif XY:
            thinModlayer_pos_first = [geom.structure.Position('q')]*(Module_layers_thin+1)
            thin_Modlayer_pla_first = [geom.structure.Placement('r',volume=Module_layer_lv4,pos=thinModlayer_pos[1])]*(Module_layers_thin+1)
            zpos = -Q("3.650m") -Q("0.0325m") + Q("0.0065m") - Q("0.051m") #- Q("0.001m")     # first layer of thin steel - half thin steel thickness - half gap - full scintillator width - 1mm for space between modules
            thinModlayer_pos_first[0] = geom.structure.Position( 'thinModlayerposition'+str(0),
                                                            x = xpos_planes,
                                                            y = ypos_planes,
                                                            z = zpos)

            thin_Modlayer_pla_first[0] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(0), volume=Module_layer_lv4, pos=thinModlayer_pos_first[0] )     #v (To uphold the pattern and not uXuv)
            tms_lv.placements.append(thin_Modlayer_pla_first[0].name)

            for module in range(1,Module_layers_thin+1):
                zpos = -Q("3.650m") -Q("0.0325m") + (module-1) * Q("0.065m")      # first layer of thin steel - half thin steel thickness - half gap
                thinModlayer_pos_first[module] = geom.structure.Position( 'thinModlayerposition'+str(module),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
                #XY version (XY)
                if module in self.thin_horizontal:
                    thin_Modlayer_pla_first[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv3, pos=thinModlayer_pos_first[module] )#x
                if module in self.thin_U:
                    thin_Modlayer_pla_first[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv4, pos=thinModlayer_pos_first[module] )#y
                if module in self.thin_V:
                    thin_Modlayer_pla_first[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv4, pos=thinModlayer_pos_first[module] )#y

                tms_lv.placements.append(thin_Modlayer_pla_first[module].name)
        elif PDR:
            #stereo version (UV)
            for module in range(Module_layers_thin):
                zpos = -Q("3.650m") -Q("0.0325m") + module * Q("0.065m")#     # first layer of thin steel - half steel+gap thickness - half gap
                thinModlayer_pos[module] = geom.structure.Position( 'thinModlayerposition'+str(module),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)

                if module % 3 == 0 :
                    thin_Modlayer_pla[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv1, pos=thinModlayer_pos[module] )   #u
                if module % 3 == 1 :
                    thin_Modlayer_pla[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv2, pos=thinModlayer_pos[module] )   #v
                if module % 3 == 2 :
                    thin_Modlayer_pla[module] = geom.structure.Placement( 'thinModlayerpla'+self.name+str(module), volume=Module_layer_lv3, pos=thinModlayer_pos[module] )   #x

                tms_lv.placements.append(thin_Modlayer_pla[module].name)



        #Place Layers into RMS vol between thick layers                                                                                 
        Module_layers_thick = 22#34
        thickModlayer_pos = [geom.structure.Position('m')]*Module_layers_thick
        thick_Modlayer_pla = [geom.structure.Placement('n',volume=Module_layer_lv1,pos=thickModlayer_pos[1])]*Module_layers_thick    

        for module in range(0, Module_layers_thick):
            zpos = -Q("1.4075m") - Q("0.045m")  + module * Q("0.09m")    # first layer of thick steel(1.4725) - half of plane gap + 40mm+ gap
            thickModlayer_pos[module] = geom.structure.Position( 'thickModlayerposition'+str(module),
                                                           x = xpos_planes,
                                                           y = ypos_planes,
                                                           z = zpos)
            
            if hybrid:
                #hybrid version (XUV)
                if module in self.thick_horizontal:
                    thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv3, pos=thickModlayer_pos[module] )   #x

                if module in self.thick_U:
                    thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv1, pos=thickModlayer_pos[module] )   #u

                if module in self.thick_V:
                    thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv2, pos=thickModlayer_pos[module] )   #v
            elif XY:
                #XY version (XY)
                if module in self.thick_horizontal:
                     thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv3, pos=thickModlayer_pos[module] )#x
                if module in self.thick_U:
                     thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv4, pos=thickModlayer_pos[module] )
                if module in self.thick_V:
                    thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv4, pos=thickModlayer_pos[module] )
            elif PDR:
                #stereo version (UV)
                if module % 3 == 0 :
                    thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv1, pos=thickModlayer_pos[module] )   #u
                if module % 3 == 1 :
                    thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv2, pos=thickModlayer_pos[module] )   #v
                if module % 3 == 2 :
                    thick_Modlayer_pla[module] = geom.structure.Placement( 'thickModlayerpla'+self.name+str(module), volume=Module_layer_lv3, pos=thickModlayer_pos[module] )   #x

            tms_lv.placements.append(thick_Modlayer_pla[module].name)

        
        #Place Layers into RMS vol between double layers
        Module_layers_double = 24#8
        doubleModlayer_pos = [geom.structure.Position('o')]*Module_layers_double
        double_Modlayer_pla = [geom.structure.Placement('p',volume=Module_layer_lv1,pos=doubleModlayer_pos[1])]*Module_layers_double

        for module in range(0,Module_layers_double):
            zpos = +Q("0.5275m") - Q("0.065m")  + module * Q("0.13m")    # first layer of thick steel(0.51) -half of plane gap +40mm+ gap
            doubleModlayer_pos[module] = geom.structure.Position( 'doubleModlayerposition'+str(module),
                                                            x = xpos_planes,
                                                            y = ypos_planes,
                                                            z = zpos)

            if hybrid:
                #hybrid version (XUV)
                if module in self.double_horizontal:
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv3, pos=doubleModlayer_pos[module] )    #x

                if module in self.double_U:
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv1, pos=doubleModlayer_pos[module] )#u

                if module in self.double_V:
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv2, pos=doubleModlayer_pos[module] ) #v
            elif XY:
                #XY version (XY)
                if module in self.double_horizontal:
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv3, pos=doubleModlayer_pos[module] )
                if module in self.double_U:
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv4, pos=doubleModlayer_pos[module] )
                if module in self.double_V:
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv4, pos=doubleModlayer_pos[module] )
            elif PDR:
                #UVX
                if module % 3 == 0 :
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv1, pos=doubleModlayer_pos[module] )   #u
                if module % 3 == 1 :
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv2, pos=doubleModlayer_pos[module] )   #v
                if module % 3 == 2 :
                    double_Modlayer_pla[module] = geom.structure.Placement( 'doubleModlayerpla'+self.name+str(module), volume=Module_layer_lv3, pos=doubleModlayer_pos[module] )   #x

            tms_lv.placements.append(double_Modlayer_pla[module].name)

        #Add TMS to self
        self.add_volume(tms_lv)

        
