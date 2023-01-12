#!/usr/bin/env python
'''
Builds compontents for the MPD
'''

import gegede.builder
from duneggd.SubDetector import NDHPgTPC as NDHPgTPC
from gegede import Quantity as Q
from math import *

class NDHPgTPCLayerBuilder(gegede.builder.Builder):

    """Builds ECAL Layers"""

    defaults = dict(dx=Q("10mm"), dy=Q("10mm"),
                dz=[Q('2mm'), Q('10mm'), Q('1mm')],
                lspacing=[Q('0.1mm'), Q('0.1mm'), Q('0.1mm')],
                mat=['Copper', 'Scintillator', 'FR4'],
                active=[False, True, False],
                material='Air',
                type = "Box",
                output_name='MPTECalHGLayer',
                sensdet_name='Ecal',
                nsides = 8,
                rmin = Q("0mm"),
                rmax = Q("0mm"),
                quadr = Q("0mm")
                )

    def depth(self):
        dzm = Q("0mm")
        for dz, lspace in zip(self.dz, self.lspacing):
            dzm += dz + lspace
        return dzm

    def BarrelConfigurationLayer(self, dx = None, dy = None, name = None, sensname = None, type = None):
        # print "---- Barrel ----"
        # print "Layer parameters dx=", dx, "dy=", dy, "layername=", name, "type=", type
        self.dx = dx
        self.dy = dy
        self.output_name = name
        self.sensdet_name = sensname
        self.type = type
        return

    def EndcapConfigurationLayer(self, nsides = None, rmin = None, rmax = None, quadr = None, name = None, sensname = None, type = None):
        # print "---- Endcap ----"
        # print "Layer parameters nsides=", nsides, "rmin=", rmin, "rmax=", rmax, "quadr=", quadr, "layername=", name, "type=", type
        self.nsides = nsides
        self.rmin = rmin
        self.rmax = rmax
        self.quadr = quadr
        self.output_name = name
        self.sensdet_name = sensname
        self.type = type
        return

    def construct(self, geom):

        dzm = self.depth()
        dzm = dzm/2.0  # Box() requires half dimensions

        # make the mother volume
        name = self.output_name

        if self.type == "Box":
            layer_shape = geom.shapes.Box(name, dx=(self.dx)/ 2.0, dy=(self.dy)/2.0, dz=(self.depth()) /2.0)
            layer_lv = geom.structure.Volume(name + "_vol", shape=layer_shape, material=self.material)
        elif self.type == "Intersection":
            layer_shape_full = geom.shapes.PolyhedraRegular(name+"_full", numsides=self.nsides, sphi=pi/8, rmin=self.rmin, rmax=self.rmax, dz=(self.depth()))
            layer_quadrant = geom.shapes.Box(name+"_quadrant", dx=self.quadr, dy=self.quadr, dz=(self.depth()) /2.0)
            layer_quad_pos = geom.structure.Position(name+"_quadrant_pos", x=self.quadr, y=self.quadr)
            layer_shape = geom.shapes.Boolean(name, type='intersection', first=layer_shape_full, second=layer_quadrant, pos=layer_quad_pos)
            layer_lv = geom.structure.Volume(name +"_vol", shape=layer_shape, material=self.material)
        elif self.type == "IntersectionInside":
            layer_shape_full = geom.shapes.Tubs(name+"_full", sphi=Q("0deg"), dphi=Q("360deg"), rmin=self.rmin, rmax=self.rmax, dz=(self.depth()))
            layer_quadrant = geom.shapes.Box(name+"_quadrant", dx=self.quadr, dy=self.quadr, dz=(self.depth()) /2.0)
            layer_quad_pos = geom.structure.Position(name+"_quadrant_pos", x=self.quadr, y=self.quadr)
            layer_shape = geom.shapes.Boolean(name, type='intersection', first=layer_shape_full, second=layer_quadrant, pos=layer_quad_pos)
            layer_lv = geom.structure.Volume(name +"_vol", shape=layer_shape, material=self.material)

        # no skipped space before the first layer
        skip = Q("0mm")
        cntr = 1
        zloc = Q("0mm")

        for dz, lspace, mat, active in zip(self.dz, self.lspacing, self.mat, self.active):
            sname = (layer_shape.name + "_slice%i" % cntr)
            zloc = zloc + skip + dz / 2.0

            if self.type == "Box":
                slice_shape = geom.shapes.Box(sname, self.dx/2.0, self.dy/2.0, dz / 2.0)
                slice_lv = geom.structure.Volume(sname + "_vol", material=mat, shape=slice_shape)
            elif self.type == "Intersection":
                slice_shape_full = geom.shapes.PolyhedraRegular(sname+"_full", numsides=self.nsides, sphi=pi/8, rmin=self.rmin, rmax=self.rmax, dz=dz)
                slice_quadrant = geom.shapes.Box(sname+"_quadrant", dx=self.quadr, dy=self.quadr, dz=dz/2.0)
                slice_quad_pos = geom.structure.Position(sname+"_quadrant_pos", x=self.quadr, y=self.quadr)
                slice_shape = geom.shapes.Boolean(sname, type='intersection', first=slice_shape_full, second=slice_quadrant, pos=slice_quad_pos)
                slice_lv = geom.structure.Volume(sname + "_vol", material=mat, shape=slice_shape)
            elif self.type == "IntersectionInside":
                slice_shape_full = geom.shapes.Tubs(sname+"_full", sphi=Q("0deg"), dphi=Q("360deg"), rmin=self.rmin, rmax=self.rmax, dz=dz)
                slice_quadrant = geom.shapes.Box(sname+"_quadrant", dx=self.quadr, dy=self.quadr, dz=dz/2.0)
                slice_quad_pos = geom.structure.Position(sname+"_quadrant_pos", x=self.quadr, y=self.quadr)
                slice_shape = geom.shapes.Boolean(sname, type='intersection', first=slice_shape_full, second=slice_quadrant, pos=slice_quad_pos)
                slice_lv = geom.structure.Volume(sname + "_vol", material=mat, shape=slice_shape)

            if active:
                #slice_lv.params.append(("SensDet", name))
                slice_lv.params.append(("SensDet", self.sensdet_name))

            # dzm is the half depth of the mother volume
            # we need to subtract it off to position layers
            # relative to the center of the mother
            slice_pos = geom.structure.Position(sname + "_pos", x='0mm', y='0mm', z=zloc - dzm)
            slice_pla = geom.structure.Placement(sname + "_pla", volume=slice_lv, pos=slice_pos)
            layer_lv.placements.append(slice_pla.name)

            skip = dz / 2.0 + lspace  # set the skipped space before the next layer
            cntr += 1

        self.add_volume(layer_lv)

class NDHPgTPCTempDetElementBuilder(gegede.builder.Builder):

    """Builds the temporary tracking layers for the temporary MPD"""

    defaults = dict(geometry = 'Barrel',
                    material = 'Air',
                    output_name = 'MPTECalDetElement',
                    layer_builder_name = ["NDHPgTPCHGLayerBuilder", "NDHPgTPCLGLayerBuilder"],
                    PosLayer = [Q('-500cm'), Q('-300cm'), Q('0cm'), Q('300cm'), Q('500cm')],
                    dX = Q("3000mm"),
                    dY = Q("2500mm"),
                    CryostatHalfLength=Q("3894mm"),
                    CryostatInnerR = Q("3362.5mm")
                    )

    def construct(self, geom):
        if self.geometry == 'TrackerSc':
            self.construct_tracker(geom)
        else:
            print("Could not find the geometry asked!")
            return
        return

    def construct_tracker(self, geom):

        safety = Q('0.1cm')
        tracker_name = self.output_name
        tracker_shape = geom.shapes.Tubs(tracker_name, rmin=Q(
            '0cm'), rmax=self.CryostatInnerR - safety, dz=self.CryostatHalfLength, sphi="0deg", dphi="360deg")
        tracker_vol = geom.structure.Volume("vol"+tracker_name, shape=tracker_shape, material="Air")

        nlayer = len(self.PosLayer)
        sensname = "Tracker_vol"
        for ilayer, layerp in zip(list(range(nlayer)), self.PosLayer):
            layername = self.output_name + "_layer%02i" % ilayer
            layer_builder = self.get_builder('MinervaPlane')
            l_dim_x = self.dX
            l_dim_y = self.dY
            NDHPgTPCLayerBuilder.BarrelConfigurationLayer(layer_builder, l_dim_x, l_dim_y, layername, sensname, "Box")
            NDHPgTPCLayerBuilder.construct(layer_builder, geom)
            layer_lv = layer_builder.get_volume(layername+"_vol")
            layer_shape = geom.store.shapes.get(layer_lv.shape)

            #Placement layer in stave
            layer_pos = geom.structure.Position(layername+"_pos", x=layerp)
            layer_rot = geom.structure.Rotation(layername+"_rot", y=Q('90deg'))
            layer_pla = geom.structure.Placement(layername+"_pla", volume=layer_lv, pos=layer_pos, rot=layer_rot)

            print(( "placing layer", layername, "at position", layerp, "with dimension dX=", layer_shape.dx, "dY=", layer_shape.dy, "and dZ=", layer_shape.dz))

            tracker_vol.placements.append(layer_pla.name)

        self.add_volume(tracker_vol)


class NDHPgTPCDetElementBuilder(gegede.builder.Builder):

    """Builds a detector element (ECAL Barrel, ECAL Endcap, PV, Yoke, GArTPC) for the ND HPgTPC"""

    defaults = dict(geometry = 'Barrel',
                    phi_range = [Q("0deg"), Q("360deg")],
                    material = 'Air',
                    nsides = 8,
                    nModules = 5,
                    output_name = 'MPTECalDetElement',
                    layer_builder_name = ["NDHPgTPCHGLayerBuilder", "NDHPgTPCLGLayerBuilder"],
                    pvEndCapBulge = Q("100cm"),
                    pvMaterial = "Steel",
                    pvThickness = Q("20mm"),
                    yokeMaterial = "Steel",
                    yokeThickness = Q("500mm"),
                    yokePhiCutout = Q("90deg"),
                    rInnerTPC = Q("2740mm"),
                    TPC_halfZ = Q('2600mm'),
                    nLayers_Barrel = [8, 72],
                    nLayers_Endcap = [6, 54],
                    Endcap_Inside = False,
                    magnetMaterial = "Aluminum",
                    magnetThickness = Q("130mm"),
                    magnetInnerR = Q("3250cm"),
                    magnetHalfLength = Q("5m"),
                    magnetType = "",
                    PRYMaterial = "Iron",
                    buildThinUpstream = False,
                    nLayers_Upstream = [8, 0],
                    nsides_yoke = 8,
                    IntegratedMuID = False,
                    MuID_nLayers = 3,
                    nModules_yoke = 1,
                    buildYokeEndcap = True,
                    yoke_stave_to_remove = [7]
                    )

    #def configure(self, **kwds):
        #super(NDHPgTPCDetElementBuilder, self).configure(**kwds)

    # def checkVariables(self):
    #     if len(self.nLayers_Barrel) != len(self.layer_builder_name):
    #         return False
    #     if len(self.nLayers_Endcap) != len(self.layer_builder_name):
    #         return False
    #     else:
    #         return True

    def get_ecal_barrel_module_thickness(self, geom):

        ecal_barrel_module_thickness = Q("0mm")
        print("Ecal Barrel thickness")
        for nlayer, type in zip(self.nLayers_Barrel, self.layer_builder_name):
            # print "Builder name ", type
            Layer_builder = self.get_builder(type)
            Layer_lv = Layer_builder.get_volume()

            Layer_shape = geom.store.shapes.get(Layer_lv.shape)
            layer_thickness = Layer_shape.dz * 2

            print(("nLayer ", nlayer, " of type ", type, " have thickness ", layer_thickness))
            ecal_barrel_module_thickness += nlayer * layer_thickness

        return ecal_barrel_module_thickness

    def get_ecal_endcap_module_thickness(self, geom):

        ecal_endcap_module_thickness = Q("0mm")
        print("Ecal Endcap thickness")
        for nlayer, type in zip(self.nLayers_Endcap, self.layer_builder_name):
            # print "Builder name ", type
            Layer_builder = self.get_builder(type)
            Layer_lv = Layer_builder.get_volume()

            Layer_shape = geom.store.shapes.get(Layer_lv.shape)
            layer_thickness = Layer_shape.dz * 2

            print(("nLayer ", nlayer, " of type ", type, " have thickness ", layer_thickness))
            ecal_endcap_module_thickness += nlayer * layer_thickness

        return ecal_endcap_module_thickness

    def get_pv_endcap_length(self, geom):
        safety = Q("0.1mm")
        length = self.TPC_halfZ + self.pvEndCapBulge + self.pvThickness

        return length

    def get_pv_endcap_position(self, geom):
        safety = Q("0.1mm")
        pv_rInner = self.rInnerTPC
        pv_rmin = sqrt((pv_rInner/Q("1mm"))**2)*Q("1mm")
        h = self.pvEndCapBulge
        if self.Endcap_Inside == True:
            h = self.pvEndCapBulge - self.get_ecal_endcap_module_thickness(geom)
        x = pv_rmin
        q = ((h/Q("1mm"))**2 + (x/Q("1mm"))**2)
        R = q/(2*h/Q("1mm"))*Q("1mm")
        xpos = self.TPC_halfZ-(R-h)
        if self.Endcap_Inside == True:
            xpos = self.TPC_halfZ+self.get_ecal_endcap_module_thickness(geom)-(R-h) + safety

        print(("PV Endcap put at xpos", xpos))

        return xpos

    def get_yoke_barrel_module_thickness(self, geom):
        yoke_barrel_module_thickness = Q("0mm")
        print("Yoke barrel thickness")
        for nlayer, type in zip(self.MuID_nLayers, ['MuIDLayerBuilder']):
            # print "Builder name ", type
            Layer_builder = self.get_builder(type)
            Layer_lv = Layer_builder.get_volume()

            Layer_shape = geom.store.shapes.get(Layer_lv.shape)
            layer_thickness = Layer_shape.dz * 2

            print(("nLayer ", nlayer, " of type ", type, " have thickness ", layer_thickness))
            yoke_barrel_module_thickness += nlayer * layer_thickness

        return yoke_barrel_module_thickness

    def construct(self, geom):

        # if self.checkVariables() == False:
        #     print "The variables nLayers and layer_builder_name have different sizes! for builder", self.name
        #     exit()

        if self.geometry == 'ECALBarrel':
            self.construct_ecal_barrel_staves(geom)
        elif self.geometry == 'ECALEndcap':
            self.construct_ecal_endcap_staves(geom)
        elif self.geometry == 'PV':
            self.construct_pv(geom)
        elif self.geometry == 'Magnet':
            self.construct_magnet(geom)
        elif self.geometry == 'Yoke':
            self.construct_yoke(geom)
        else:
            print("Could not find the geometry asked!")
            return
        return

    def construct_magnet(self, geom):
        ''' construct the Magnet '''
        safety = Q("1mm")

        if self.magnetType == "5Coils" or self.magnetType == "4Coils" or self.magnetType == "2Coils":
            ''' construct a 5/4/2 Helmoltz coil design based on Vladimir Kashikhin model'''
            ''' 1st coil is at 0, side coils at +/- 3m and shielding coils at +/- 5.5 m '''
            ''' coil thickness is 62 cm and with is 27 cm for center and shielding coils, 61,6 cm for the side coils '''
            ''' the model does not separate coil and cryo - the inner radius is 3.5m and the thickness is 70 cm '''
            ''' total weight for the 5 coil design is around 93t '''

            if self.magnetType == "5Coils":
                print(("Construct Magnet - 5 Coils type with ", self.magnetMaterial, " with a radius of ", self.magnetInnerR, " a thickness of ", self.magnetThickness, " and a length of ", self.magnetHalfLength*2))
                nCoils = 5
                CoilWidth = [Q("27cm"), Q("61.6cm"), Q("27cm"), Q("61.6cm"), Q("27cm")]
                CoilPos = [Q("-5.5m"), Q("-3m"), Q("0m"), Q("3m"), Q("5.5m")]
            if self.magnetType == "4Coils":
                print(("Construct Magnet - 4 Coils type with ", self.magnetMaterial, " with a radius of ", self.magnetInnerR, " a thickness of ", self.magnetThickness, " and a length of ", self.magnetHalfLength*2))
                nCoils = 4
                CoilWidth = [Q("27cm"), Q("61.6cm"), Q("61.6cm"), Q("27cm")]
                CoilPos = [Q("-5.5m"), Q("-3m"), Q("3m"), Q("5.5m")]
            if self.magnetType == "2Coils":
                print(("Construct Magnet - 2 Coils type with ", self.magnetMaterial, " with a radius of ", self.magnetInnerR, " a thickness of ", self.magnetThickness, " and a length of ", self.magnetHalfLength*2))
                nCoils = 2
                CoilWidth = [Q("61.6cm"), Q("61.6cm")]
                CoilPos = [Q("-3m"), Q("3m")]

            ''' Fake shape filled with Air to contain the coils '''
            magnet_name = self.output_name
            magnet_shape = geom.shapes.Tubs(magnet_name, rmin=self.magnetInnerR, rmax=self.magnetInnerR+self.magnetThickness, dz=self.magnetHalfLength, sphi="0deg", dphi="360deg")
            magnet_vol = geom.structure.Volume("vol"+magnet_name, shape=magnet_shape, material="Air")

            for ncoil, coilw, coilp in zip(list(range(nCoils)), CoilWidth, CoilPos):
                coil_name = self.output_name + "_Coil%01i" % ncoil
                coil_shape = geom.shapes.Tubs(coil_name, rmin=self.magnetInnerR, rmax=self.magnetInnerR+self.magnetThickness, dz=coilw/2., sphi="0deg", dphi="360deg")
                coil_vol = geom.structure.Volume("vol"+coil_name, shape=coil_shape, material=self.magnetMaterial)

                '''Place the coils in the magnet volume'''
                #Placement layer in stave
                coil_pos = geom.structure.Position(coil_name+"_pos", z=coilp)
                coil_pla = geom.structure.Placement(coil_name+"_pla", volume=coil_vol, pos=coil_pos)
                magnet_vol.placements.append(coil_pla.name)

            self.add_volume(magnet_vol)

        elif self.magnetType == "SPY":
            ''' construct a solenoid with partial return Yoke (SPY)'''
            ''' The soleinoid tickness is 10 cm of Al'''
            ''' The PRY fills the rest of the space available (up to 8.4m in diameter for the full MPD) '''
            ''' The PRY covers only +/- 30 deg up and down the MPD and has a bore of 3.5m'''
            ''' Total weight is ~XXXt '''

            print(("Construct Magnet SPY - Solenoid made of ", self.magnetMaterial, " with a radius of ", self.magnetInnerR, " a thickness of ", self.magnetThickness, " and a length of ", self.magnetHalfLength*2))

            nCoils = 4
            CoilWidth = Q("1496mm")
            CoilSpace = Q("304mm")
            CoilPos = [Q("-2.6m"), Q("-0.8m"), Q("0.8m"), Q("2.6m")]

            ''' Fake shape filled with Air to contain the coils '''
            magnet_name = self.output_name
            magnet_shape = geom.shapes.Tubs(magnet_name, rmin=self.magnetInnerR, rmax=self.magnetInnerR+self.magnetThickness, dz=Q("2.6m")+Q("1496mm")/2., sphi="0deg", dphi="360deg")
            magnet_vol = geom.structure.Volume("vol"+magnet_name, shape=magnet_shape, material="Air")

            for ncoil, coilp in zip(list(range(nCoils)), CoilPos):
                coil_name = self.output_name + "_Coil%01i" % ncoil
                coil_shape = geom.shapes.Tubs(coil_name, rmin=self.magnetInnerR, rmax=self.magnetInnerR+self.magnetThickness, dz=CoilWidth/2., sphi="0deg", dphi="360deg")
                coil_vol = geom.structure.Volume("vol"+coil_name, shape=coil_shape, material=self.magnetMaterial)

                '''Place the coils in the magnet volume'''
                #Placement layer in stave
                coil_pos = geom.structure.Position(coil_name+"_pos", z=coilp)
                coil_pla = geom.structure.Placement(coil_name+"_pla", volume=coil_vol, pos=coil_pos)
                magnet_vol.placements.append(coil_pla.name)

            self.add_volume(magnet_vol)

        elif self.magnetType == "Uniform":
            print(("Construct Magnet - Approximation to a magnet of 100t made of ", self.magnetMaterial, " with a radius of ", self.magnetInnerR, " a thickness of ", self.magnetThickness, " and a length of ", self.magnetHalfLength*2))

            magnet_name = self.output_name
            magnet_shape = geom.shapes.Tubs(magnet_name, rmin=self.magnetInnerR, rmax=self.magnetInnerR+self.magnetThickness, dz=self.magnetHalfLength, sphi="0deg", dphi="360deg")
            magnet_vol = geom.structure.Volume("vol"+magnet_name, shape=magnet_shape, material=self.magnetMaterial)

            self.add_volume(magnet_vol)
        else:
            print("Magnet model unknown.... ")
            return

    def construct_pv(self, geom):
        ''' construct the Pressure Vessel '''

        print("Construct PV Barrel")

        safety = Q("0.1mm")
        nsides = self.nsides
        pv_rInner = self.rInnerTPC
        pvHalfLength = self.TPC_halfZ
        if self.Endcap_Inside == True:
            pvHalfLength = self.TPC_halfZ + self.get_ecal_endcap_module_thickness(geom) + safety
        pv_rmin = pv_rInner
        pv_rmax = pv_rmin + self.pvThickness

        # build the pressure vessel barrel
        pvb_name = self.output_name + "Barrel"
        pvb_shape = geom.shapes.Tubs(pvb_name, rmin=pv_rmin, rmax=pv_rmax, dz=pvHalfLength, sphi="0deg", dphi="360deg")
        pvb_vol = geom.structure.Volume("vol"+pvb_name, shape=pvb_shape, material=self.pvMaterial)

        self.add_volume(pvb_vol)

        print("Construct PV Endcap")

        # build the pressure vessel endcaps
        # some euclidean geometry documented in my notebook
        h = self.pvEndCapBulge
        x = pv_rmin
        if self.Endcap_Inside == True:
            h = self.pvEndCapBulge - self.get_ecal_endcap_module_thickness(geom)
        q = ((h/Q("1mm"))**2 + (x/Q("1mm"))**2)
        R = q/(2*h/Q("1mm"))*Q("1mm")
        dtheta = asin( 2*(h/Q("1mm"))*(x/Q("1mm"))/q)

        print(("h, x, q, R, dtheta = ", h, x, q, R, dtheta))

        pvec_name = self.output_name + "Endcap"
        pvec_shape = geom.shapes.Sphere(pvec_name, rmin=R, rmax=R + self.pvThickness, sphi="0deg", dphi="360deg", stheta="0deg", dtheta=dtheta)
        pvec_vol = geom.structure.Volume("vol"+pvec_name, shape=pvec_shape, material=self.pvMaterial)

        self.add_volume(pvec_vol)

    def construct_ecal_barrel_staves(self, geom):
        ''' construct a set of ECAL staves for the Barrel '''

        #       ECAL stave
        #   /----------------\         //Small side
        #  /                  \
        # /____________________\       //Large side
        #
        # z
        # ^
        # |
        # |-----> x
        #
        # need to create the layer based on the position in depth z -> different layer sizes

        print("Construct ECAL Barrel")

        # ECAL Barrel
        safety = Q("0.1mm")
        nsides = self.nsides
        dphi = (2*pi/nsides)
        hphi = dphi/2;

        #ecal module thickness
        ecal_barrel_module_thickness = self.get_ecal_barrel_module_thickness(geom)
        ecal_barrel_module_thickness_noSupport = ecal_barrel_module_thickness - safety
        #inner radius ecal (TPC + pv + safety)
        rInnerEcal = self.rInnerTPC + self.pvThickness
        print(("Ecal inner radius ", rInnerEcal))
        #barrel length (TPC + PV)
        Barrel_halfZ = self.get_pv_endcap_length(geom)
        if self.Endcap_Inside == True:
            Barrel_halfZ = self.TPC_halfZ + self.get_ecal_endcap_module_thickness(geom)
        #outer radius ecal (inner radius ecal + ecal module)
        rOuterEcal = rInnerEcal + ecal_barrel_module_thickness
        print(("Ecal outer radius ", rOuterEcal))
        #check that the ECAL thickness does not go over the magnet radius
        ecal_barrel_module_thickness_max = self.magnetInnerR * cos(pi/nsides) - rInnerEcal

        print(("Barrel Module thickness ", ecal_barrel_module_thickness))
        print(("Maximum allowed thickness ", ecal_barrel_module_thickness_max))

        if ecal_barrel_module_thickness > ecal_barrel_module_thickness_max:
            print("Will have overlaps if the magnet is present!")

        #minimum dimension of the stave
        min_dim_stave = 2 * tan( pi/nsides ) * rInnerEcal
        #maximum dimension of the stave
        max_dim_stave = 2 * tan( pi/nsides ) * rOuterEcal

        Ecal_Barrel_halfZ = Barrel_halfZ
        Ecal_Barrel_n_modules = self.nModules
        #dimension of a module along the ND x direction
        Ecal_Barrel_module_dim = Ecal_Barrel_halfZ * 2 / Ecal_Barrel_n_modules

        print(("Large side of the stave", max_dim_stave))
        print(("Small side of the stave", min_dim_stave))
        print(("Barrel module dim in z", Ecal_Barrel_module_dim))
        print(("Build Thinner Upstream ECAL", self.buildThinUpstream))
        if self.buildThinUpstream:
            print(("Number of layers for the Upstream ECAL", self.nLayers_Upstream))

        #Position of the stave in the Barrel (local coordinates)
        X = rInnerEcal + safety + ecal_barrel_module_thickness / 2.
        #Y = (ecal_barrel_module_thickness_noSupport / 2.) / sin(2.*pi/nsides)
        Y = Q('0mm')

        #print "X ", X, " and Y ", Y
        #Mother volume Barrel
        barrel_shape = geom.shapes.PolyhedraRegular(self.output_name, numsides=nsides, rmin=rInnerEcal, rmax=rOuterEcal+2*safety, dz=Ecal_Barrel_halfZ+safety)
        barrel_lv = geom.structure.Volume("vol"+self.output_name, shape=barrel_shape, material=self.material)

        sensname = self.output_name + "_vol"
        for istave in range(nsides):
            stave_id = istave+1
            dstave = int( nsides/4.0 )
            phirot =  hphi + pi/2.0
            phirot += (istave - dstave)*dphi
            phirot2 =  (istave - dstave) * dphi + hphi

            placing_angle = phirot2*180/pi+292.5
            if placing_angle >= 360:
                placing_angle = placing_angle - 360

            print(("Placing stave ", stave_id, " at angle ", placing_angle, " deg"))

            for imodule in range(Ecal_Barrel_n_modules):
                module_id = imodule+1
                print(("Placing stave ", stave_id, " and module ", module_id))

                stave_name = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id)
                stave_volname = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id) + "_vol"

                stave_shape = geom.shapes.Trapezoid(stave_name, dx1=min_dim_stave/2.0, dx2=max_dim_stave/2.0,
                dy1=(Ecal_Barrel_module_dim-safety)/2.0, dy2=(Ecal_Barrel_module_dim-safety)/2.0,
                dz=ecal_barrel_module_thickness/2.0)

                stave_lv = geom.structure.Volume(stave_volname, shape=stave_shape, material=self.material)

                zPos = Q("0mm")
                layer_id = 1

                # check if angle is below -90/90 deg for full modules, otherwise thinner upstream ECAL
                if placing_angle < 315 and placing_angle > 45:
                    for nlayer, type in zip(self.nLayers_Barrel, self.layer_builder_name):
                        for ilayer in range(nlayer):

                            layername = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id) + "_layer_%02i" % (layer_id)

                            #Configure the layer length based on the zPos in the stave
                            Layer_builder = self.get_builder(type)
                            layer_thickness = NDHPgTPCLayerBuilder.depth(Layer_builder)
                            l_dim_x = min_dim_stave + 2 * zPos * tan( pi/nsides )
                            l_dim_y = Ecal_Barrel_module_dim - safety

                            NDHPgTPCLayerBuilder.BarrelConfigurationLayer(Layer_builder, l_dim_x, l_dim_y, layername, sensname, "Box")
                            NDHPgTPCLayerBuilder.construct(Layer_builder, geom)
                            layer_lv = Layer_builder.get_volume(layername+"_vol")

                            #Placement layer in stave
                            layer_pos = geom.structure.Position(layername+"_pos", z=zPos + layer_thickness/2.0 - ecal_barrel_module_thickness/2.0)
                            layer_pla = geom.structure.Placement(layername+"_pla", volume=layer_lv, pos=layer_pos)

                            stave_lv.placements.append(layer_pla.name)

                            zPos += layer_thickness;
                            layer_id += 1
                else:
                    nLoopLayers = self.nLayers_Barrel
                    if self.buildThinUpstream:
                        nLoopLayers = self.nLayers_Upstream

                    for nlayer, type in zip(nLoopLayers, self.layer_builder_name):
                        for ilayer in range(nlayer):

                            layername = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id) + "_layer_%02i" % (layer_id)

                            #Configure the layer length based on the zPos in the stave
                            Layer_builder = self.get_builder(type)
                            layer_thickness = NDHPgTPCLayerBuilder.depth(Layer_builder)
                            l_dim_x = min_dim_stave + 2 * zPos * tan( pi/nsides )
                            l_dim_y = Ecal_Barrel_module_dim - safety

                            NDHPgTPCLayerBuilder.BarrelConfigurationLayer(Layer_builder, l_dim_x, l_dim_y, layername, sensname, "Box")
                            NDHPgTPCLayerBuilder.construct(Layer_builder, geom)
                            layer_lv = Layer_builder.get_volume(layername+"_vol")

                            #Placement layer in stave
                            layer_pos = geom.structure.Position(layername+"_pos", z=zPos + layer_thickness/2.0 - ecal_barrel_module_thickness/2.0)
                            layer_pla = geom.structure.Placement(layername+"_pla", volume=layer_lv, pos=layer_pos)

                            stave_lv.placements.append(layer_pla.name)

                            zPos += layer_thickness;
                            layer_id += 1

                #Placement staves in Barrel
                name = stave_lv.name

                #print "Placing stave at x= ", (X*cos(phirot2)-Y*sin(phirot2))
                #print "Placing stave at y= ", (X*sin(phirot2)+Y*cos(phirot2))

                pos = geom.structure.Position(name + "_pos", x=(X*cos(phirot2)-Y*sin(phirot2)), y=(X*sin(phirot2)+Y*cos(phirot2)), z=( imodule+0.5 )*Ecal_Barrel_module_dim - Barrel_halfZ )
                rot = geom.structure.Rotation(name + "_rot", x=pi/2.0, y=phirot+pi, z=Q("0deg"))
                pla = geom.structure.Placement(name + "_pla", volume=stave_lv, pos=pos, rot=rot)

                barrel_lv.placements.append(pla.name)

        self.add_volume(barrel_lv)

    def construct_ecal_endcap_staves(self, geom):
        ''' construct a set of ECAL staves for the Endcap '''

        if self.Endcap_Inside == False:
            print("Construct ECAL Endcap outside the PV")

            # ECAL Endcap
            safety = Q("0.1mm")
            nsides = self.nsides
            ecal_barrel_module_thickness = self.get_ecal_barrel_module_thickness(geom)
            ecal_endcap_module_thickness = self.get_ecal_endcap_module_thickness(geom)
            rInnerEcal = self.rInnerTPC + self.pvThickness + safety
            Barrel_halfZ = self.get_pv_endcap_length(geom) + safety

            EcalEndcap_inner_radius = Q("0mm")
            EcalEndcap_outer_radius = rInnerEcal + ecal_barrel_module_thickness
            Ecal_Barrel_halfZ = Barrel_halfZ
            EcalEndcap_min_z = Ecal_Barrel_halfZ
            EcalEndcap_max_z = Ecal_Barrel_halfZ + ecal_endcap_module_thickness
            Ecal_Barrel_n_modules = self.nModules

            rmin = EcalEndcap_inner_radius
            rmax = EcalEndcap_outer_radius + 2*safety

            print(("Quadrant side ", rmax))
            print(("Endcap thickness ", ecal_endcap_module_thickness))

            #Mother volume Endcap
            endcap_shape_min = geom.shapes.PolyhedraRegular("ECALEndcap_min", numsides=nsides, rmin=rmin, rmax=rmax, dz=EcalEndcap_min_z)
            endcap_shape_max = geom.shapes.PolyhedraRegular("ECALEndcap_max", numsides=nsides, rmin=rmin, rmax=rmax, dz=EcalEndcap_max_z)

            endcap_shape = geom.shapes.Boolean( self.output_name, type='subtraction', first=endcap_shape_max, second=endcap_shape_min )
            endcap_lv = geom.structure.Volume( "vol"+self.output_name, shape=endcap_shape, material=self.material )

            # Place staves in the Endcap Volume
            sensname = self.output_name + "_vol"
            module_id = -1
            for iend in range(2):
                if iend == 0:
                    module_id = 0
                else:
                    module_id = Ecal_Barrel_n_modules + 1

                this_module_z_offset = (EcalEndcap_min_z + EcalEndcap_max_z)/2.
                if iend == 0:
                    this_module_z_offset *= -1

                this_module_rotY = 0.;
                if iend == 0:
                    this_module_rotY = pi;
                # this_module_rotY = pi;

                rotZ_offset = (pi/8. + 3.*pi/4.)
                if iend == 0:
                    rotZ_offset = (pi/8. - pi/2.)
                # rotZ_offset = (pi/8. - pi/2.)

                for iquad in range(4):
                    stave_id = iquad+1
                    this_module_rotZ = 0
                    if iend == 0:
                        this_module_rotZ = rotZ_offset - (iquad-2) * pi/2.
                    else:
                        this_module_rotZ = rotZ_offset + (iquad+1) * pi/2.

                    print(("Placing stave ", stave_id, " and module ", module_id))

                    #Create a template module
                    stave_name = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id)
                    stave_volname = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id) + "_vol"

                    endcap_stave_full = geom.shapes.PolyhedraRegular(stave_name+"_full", numsides=nsides, sphi=pi/8, dphi=Q("360deg"), rmin=rmin, rmax=rmax, dz=ecal_endcap_module_thickness)
                    quadr = rmax
                    quadrant = geom.shapes.Box(stave_name+"_quadrant", dx=quadr, dy=quadr, dz=ecal_endcap_module_thickness/2)

                    endcap_stave_pos = geom.structure.Position(stave_name+"_pos", x=quadr, y=quadr, z=Q("0mm"))
                    endcap_stave_shape = geom.shapes.Boolean(stave_name, type='intersection', first=endcap_stave_full, second=quadrant, pos=endcap_stave_pos)
                    endcap_stave_lv = geom.structure.Volume(stave_volname, shape=endcap_stave_shape, material=self.material)

                    zPos = Q("0mm")
                    layer_id = 1

                    for nlayer, type in zip(self.nLayers_Endcap, self.layer_builder_name):
                        for ilayer in range(nlayer):
                            layername = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id) + "_layer_%02i" % (layer_id)

                            Layer_builder = self.get_builder(type)
                            layer_thickness = NDHPgTPCLayerBuilder.depth(Layer_builder)
                            NDHPgTPCLayerBuilder.EndcapConfigurationLayer(Layer_builder, nsides, rmin, rmax, quadr, layername, sensname, "Intersection")
                            NDHPgTPCLayerBuilder.construct(Layer_builder, geom)
                            layer_lv = Layer_builder.get_volume(layername+"_vol")

                            # Placement layer in stave
                            layer_pos = geom.structure.Position(layername+"_pos", z=zPos + layer_thickness/2.0 - ecal_endcap_module_thickness/2.0)
                            layer_pla = geom.structure.Placement(layername+"_pla", volume=layer_lv, pos=layer_pos)

                            endcap_stave_lv.placements.append(layer_pla.name)

                            zPos += layer_thickness;
                            layer_id += 1

                    #Placement staves in Endcap
                    name = endcap_stave_lv.name
                    endcap_stave_pos = geom.structure.Position(name + "_pos", z=this_module_z_offset )
                    endcap_stave_rot = geom.structure.Rotation(name + "_rot", x=Q("0deg"), y=this_module_rotY, z=this_module_rotZ+pi/4)
                    endcap_stave_pla = geom.structure.Placement(name + "_pla", volume=endcap_stave_lv, pos=endcap_stave_pos, rot=endcap_stave_rot)
                    endcap_lv.placements.append(endcap_stave_pla.name)

            self.add_volume(endcap_lv)
        else:
            #ECAL Endcap inside the PV
            safety = Q("0.1mm")
            ecal_endcap_module_thickness = self.get_ecal_endcap_module_thickness(geom)
            rInnerEcal = self.rInnerTPC - safety
            Barrel_halfZ = self.TPC_halfZ + safety

            EcalEndcap_inner_radius = Q("0mm")
            EcalEndcap_outer_radius = rInnerEcal
            Ecal_Barrel_halfZ = Barrel_halfZ
            EcalEndcap_min_z = Ecal_Barrel_halfZ
            EcalEndcap_max_z = Ecal_Barrel_halfZ + ecal_endcap_module_thickness
            Ecal_Barrel_n_modules = self.nModules

            rmin = EcalEndcap_inner_radius
            rmax = EcalEndcap_outer_radius

            print(("Quadrant side ", rmax))
            print(("Endcap thickness ", ecal_endcap_module_thickness))

            #Mother volume Endcap
            endcap_shape_min = geom.shapes.Tubs("ECALEndcap_min", rmin=rmin, rmax=rmax, dz=EcalEndcap_min_z, sphi="0deg", dphi="360deg")
            endcap_shape_max = geom.shapes.Tubs("ECALEndcap_max", rmin=rmin, rmax=rmax, dz=EcalEndcap_max_z, sphi="0deg", dphi="360deg")

            endcap_shape = geom.shapes.Boolean( self.output_name, type='subtraction', first=endcap_shape_max, second=endcap_shape_min )
            endcap_lv = geom.structure.Volume( "vol"+self.output_name, shape=endcap_shape, material=self.material )

            # Place staves in the Endcap Volume
            sensname = self.output_name + "_vol"
            module_id = -1
            for iend in range(2):
                if iend == 0:
                    module_id = 0
                else:
                    module_id = Ecal_Barrel_n_modules + 1

                this_module_z_offset = (EcalEndcap_min_z + EcalEndcap_max_z)/2.
                if iend == 0:
                    this_module_z_offset *= -1

                this_module_rotY = 0.;
                if iend == 0:
                    this_module_rotY = pi;
                # this_module_rotY = pi;

                rotZ_offset = (pi/8. + 3.*pi/4.)
                if iend == 0:
                    rotZ_offset = (pi/8. - pi/2.)
                # rotZ_offset = (pi/8. - pi/2.)

                for iquad in range(4):
                    stave_id = iquad+1
                    this_module_rotZ = 0
                    if iend == 0:
                        this_module_rotZ = rotZ_offset - (iquad-2) * pi/2.
                    else:
                        this_module_rotZ = rotZ_offset + (iquad+1) * pi/2.

                    print(("Placing stave ", stave_id, " and module ", module_id))

                    #Create a template module
                    stave_name = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id)
                    stave_volname = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id) + "_vol"

                    endcap_stave_full = geom.shapes.Tubs(stave_name+"_full", sphi=Q("0deg"), dphi=Q("360deg"), rmin=rmin, rmax=rmax, dz=ecal_endcap_module_thickness)
                    quadr = rmax
                    quadrant = geom.shapes.Box(stave_name+"_quadrant", dx=quadr, dy=quadr, dz=ecal_endcap_module_thickness/2)

                    endcap_stave_pos = geom.structure.Position(stave_name+"_pos", x=quadr, y=quadr, z=Q("0mm"))
                    endcap_stave_shape = geom.shapes.Boolean(stave_name, type='intersection', first=endcap_stave_full, second=quadrant, pos=endcap_stave_pos)
                    endcap_stave_lv = geom.structure.Volume(stave_volname, shape=endcap_stave_shape, material=self.material)

                    zPos = Q("0mm")
                    layer_id = 1

                    for nlayer, type in zip(self.nLayers_Endcap, self.layer_builder_name):
                        for ilayer in range(nlayer):
                            layername = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id) + "_layer_%02i" % (layer_id)

                            Layer_builder = self.get_builder(type)
                            layer_thickness = NDHPgTPCLayerBuilder.depth(Layer_builder)
                            NDHPgTPCLayerBuilder.EndcapConfigurationLayer(Layer_builder, 0, rmin, rmax, quadr, layername, sensname, "IntersectionInside")
                            NDHPgTPCLayerBuilder.construct(Layer_builder, geom)
                            layer_lv = Layer_builder.get_volume(layername+"_vol")

                            # Placement layer in stave
                            layer_pos = geom.structure.Position(layername+"_pos", z=zPos + layer_thickness/2.0 - ecal_endcap_module_thickness/2.0)
                            layer_pla = geom.structure.Placement(layername+"_pla", volume=layer_lv, pos=layer_pos)

                            endcap_stave_lv.placements.append(layer_pla.name)

                            zPos += layer_thickness;
                            layer_id += 1

                    #Placement staves in Endcap
                    name = endcap_stave_lv.name
                    endcap_stave_pos = geom.structure.Position(name + "_pos", z=this_module_z_offset )
                    endcap_stave_rot = geom.structure.Rotation(name + "_rot", x=Q("0deg"), y=this_module_rotY, z=this_module_rotZ+pi/4)
                    endcap_stave_pla = geom.structure.Placement(name + "_pla", volume=endcap_stave_lv, pos=endcap_stave_pos, rot=endcap_stave_rot)
                    endcap_lv.placements.append(endcap_stave_pla.name)

            self.add_volume(endcap_lv)

    def construct_yoke(self, geom):
        '''Construct the Yoke'''

        safety = Q("1mm")
        space = Q("1cm")
        yoke_barrel_thickness = self.get_yoke_barrel_module_thickness(geom)
        rmin_barrel = self.magnetInnerR + self.magnetThickness + space
        # rmax_endcap = self.rInnerTPC + Q("1400mm")
        rmax_endcap = rmin_barrel + yoke_barrel_thickness + safety
        ecal_endcap_module_thickness = self.get_ecal_endcap_module_thickness(geom)
        YokeEndcap_min_z = self.get_pv_endcap_length(geom) + ecal_endcap_module_thickness + safety
        YokeEndcap_max_z = YokeEndcap_min_z + yoke_barrel_thickness + safety

        if self.Endcap_Inside == True:
            YokeEndcap_min_z = self.TPC_halfZ + self.get_ecal_endcap_module_thickness(geom) + self.pvEndCapBulge + safety
            YokeEndcap_max_z = YokeEndcap_min_z + yoke_barrel_thickness + safety

        print(("Construct PRY made of ", self.PRYMaterial, " with a radius of ", rmin_barrel, " a thickness of ", yoke_barrel_thickness, " and a length of ", YokeEndcap_min_z*2))
        print(("Build integrated Muon ID ", self.IntegratedMuID))

        '''Barrel'''
        byoke_name = "YokeBarrel"
        yoke_barrel_shape = geom.shapes.PolyhedraRegular(byoke_name, numsides=self.nsides_yoke, rmin=rmin_barrel, rmax=rmax_endcap, dz=YokeEndcap_min_z)
        yoke_barrel_vol = geom.structure.Volume("vol"+byoke_name, shape=yoke_barrel_shape, material="Air")

        #minimum dimension of the stave
        min_dim_stave = 2 * tan( pi/self.nsides_yoke ) * rmin_barrel
        #maximum dimension of the stave
        max_dim_stave = 2 * tan( pi/self.nsides_yoke ) * rmax_endcap
        Yoke_Barrel_n_modules = self.nModules_yoke
        Yoke_Barrel_module_dim = YokeEndcap_min_z * 2 / Yoke_Barrel_n_modules

        #Position of the stave in the Barrel (local coordinates)
        dphi = (2*pi/self.nsides_yoke)
        hphi = dphi/2;
        minus_deg = 0
        if self.nsides_yoke == 16:
            minus_deg = 11.25
        sensname = "MuID" + "_vol"

        ''' Normal stave '''
        for istave in range(self.nsides_yoke):

            X = rmin_barrel + yoke_barrel_thickness / 2.
            Y = Q('0mm')
            stave_id = istave+1
            dstave = int( self.nsides_yoke/4.0 )
            phirot =  hphi + pi/2.0
            phirot += (istave - dstave)*dphi
            phirot2 =  (istave - dstave) * dphi + hphi

            placing_angle = phirot2*180/pi+292.5 + minus_deg
            if placing_angle >= 360:
                placing_angle = placing_angle - 360

            xpos = X*cos(phirot2)-Y*sin(phirot2)
            ypos = X*sin(phirot2)+Y*cos(phirot2)

            #remove the stave(s) in front of the LAr
            #nsides = 8 -> stave 8
            #nsides = 16 -> stave 4,5,6
            set_stave = set(self.yoke_stave_to_remove)
            if stave_id in set_stave:
                print(("Ignoring stave", stave_id))
                continue

            # if stave_id > 2: continue

            print(("Placing stave ", stave_id, " at angle ", placing_angle, " deg"))

            for imodule in range(Yoke_Barrel_n_modules):
                module_id = imodule+1
                print(("Placing stave ", stave_id, " and module ", module_id))

                stave_name = byoke_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id)
                stave_volname = byoke_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id) + "_vol"

                stave_shape = geom.shapes.Trapezoid(stave_name, dx1=min_dim_stave/2.0, dx2=max_dim_stave/2.0,
                dy1=(Yoke_Barrel_module_dim-safety)/2.0, dy2=(Yoke_Barrel_module_dim-safety)/2.0,
                dz=yoke_barrel_thickness/2.0)
                stave_lv = geom.structure.Volume(stave_volname, shape=stave_shape, material=self.PRYMaterial)

                if self.IntegratedMuID == True:
                    zPos = Q("0mm")
                    layer_id = 1

                    for nlayer, type in zip(self.MuID_nLayers, ['MuIDLayerBuilder']):
                        for ilayer in range(nlayer):

                            layername = byoke_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id) + "_layer_%02i" % (layer_id)

                            print(("Adding ", layername))

                            #Configure the layer length based on the zPos in the stave
                            Layer_builder = self.get_builder(type)
                            layer_thickness = NDHPgTPCLayerBuilder.depth(Layer_builder)
                            l_dim_x = min_dim_stave + 2 * zPos * tan( pi/self.nsides_yoke )
                            l_dim_y = Yoke_Barrel_module_dim - safety

                            NDHPgTPCLayerBuilder.BarrelConfigurationLayer(Layer_builder, l_dim_x, l_dim_y, layername, sensname, "Box")
                            NDHPgTPCLayerBuilder.construct(Layer_builder, geom)
                            layer_lv = Layer_builder.get_volume(layername+"_vol")

                            #Placement layer in stave
                            layer_pos = geom.structure.Position(layername+"_pos", z=zPos + layer_thickness/2.0 - yoke_barrel_thickness/2.0)
                            layer_pla = geom.structure.Placement(layername+"_pla", volume=layer_lv, pos=layer_pos)

                            stave_lv.placements.append(layer_pla.name)

                            zPos += layer_thickness;
                            layer_id += 1

                #Placement staves in Barrel
                name = stave_lv.name
                pos = geom.structure.Position(name + "_pos", x=xpos, y=ypos, z=( imodule+0.5 )*Yoke_Barrel_module_dim - YokeEndcap_min_z )
                rot = geom.structure.Rotation(name + "_rot", x=pi/2.0, y=phirot+pi, z=Q("0deg"))
                pla = geom.structure.Placement(name + "_pla", volume=stave_lv, pos=pos, rot=rot)

                yoke_barrel_vol.placements.append(pla.name)

        self.add_volume(yoke_barrel_vol)

        if self.buildYokeEndcap:
            '''Endcaps'''
            #Mother volume Endcap
            yoke_endcap_shape_min = geom.shapes.PolyhedraRegular("YokeEndcap_min", numsides=self.nsides_yoke, rmin=self.rInnerTPC, rmax=rmax_endcap, dz=YokeEndcap_min_z)
            yoke_endcap_shape_max = geom.shapes.PolyhedraRegular("YokeEndcap_max", numsides=self.nsides_yoke, rmin=self.rInnerTPC, rmax=rmax_endcap, dz=YokeEndcap_max_z)

            eyoke_name = "YokeEndcap"
            yoke_endcap_shape = geom.shapes.Boolean( eyoke_name, type='subtraction', first=yoke_endcap_shape_max, second=yoke_endcap_shape_min )
            # yoke_endcap_vol = geom.structure.Volume( "vol"+eyoke_name, shape=yoke_endcap_shape, material=self.PRYMaterial)
            yoke_endcap_vol = geom.structure.Volume( "vol"+eyoke_name, shape=yoke_endcap_shape, material="Air")

            for side in ["L", "R"]:
                #Create the volume for the endcaps
                yoke_thickness = YokeEndcap_max_z - YokeEndcap_min_z
                eyoke_name = eyoke_name + side
                eyoke_volname = "vol"+ eyoke_name + side
                yoke_endcap_shape_one = geom.shapes.PolyhedraRegular(eyoke_name, numsides=self.nsides_yoke, rmin=self.rInnerTPC, rmax=rmax_endcap,    dz=yoke_thickness/2.)
                yoke_endcap_lv = geom.structure.Volume( eyoke_volname, shape=yoke_endcap_shape_one, material=self.PRYMaterial)
                z_pos = YokeEndcap_max_z - yoke_thickness/2.
                if side == 'R':
                    z_pos = -z_pos
                pos = geom.structure.Position(eyoke_name + side + "_pos", z=z_pos)
                rot = geom.structure.Rotation(eyoke_name + side + "_rot", z=Q("0deg"))
                pla = geom.structure.Placement(eyoke_name + side + "_pla", volume=yoke_endcap_lv, pos=pos, rot=rot)
                yoke_endcap_vol.placements.append(pla.name)

            self.add_volume(yoke_endcap_vol)
