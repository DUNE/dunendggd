#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandECalBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, NCaloModBarrel=None, **kwds):
        self.NCaloModBarrel = NCaloModBarrel
        self.caloThickness = Q('23cm')
        self.EndcapZ = Q('1.69m')
        self.EndcapRmin = Q('20.8cm')
        self.BarrelRmin = Q('2m')
        self.BarrelDZ = Q('2.15m')
        self.ECCurvRad = Q('10cm')
        self.ECStraight = Q('20cm')
        self.AlPlateThick= Q('2.5cm')

        ### Below values should be the same as the one in SANDBuilder
        ### and will be used to construct subtraction boolean volume
        ### to avoid overlap with yoke endcap elements (C,D)
        
        # part C is a TUBS, 2.15<|x|<2.58m, rmin=0.84m, rmax=1.34m
        self.EndcapCZStart=Q("2.15m")
        self.EndcapCZEnd=Q("2.58m")
        self.EndcapCRmax=Q("1.34m")
        self.EndcapCRmin=Q("0.84m")
        
        # part D is a TUBS, 1.96<|x|<2.15m, rmin=0.512m, rmax=1.73m
        self.EndcapDZStart=Q("1.96m")
        self.EndcapDZEnd=Q("2.15m")
        
        # Here we reduce the size of the D element of the yoke endcap
        # to avoid overlap with the curved element of the ecal endcap module
        self.EndcapDRmax=Q("1.66m")
        self.EndcapDRmin=Q("0.62m")

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        ang = math.pi / self.NCaloModBarrel

        # barrel
        rmax_barrel = (self.BarrelRmin + self.caloThickness) / math.cos(ang)
        # endcap
        rmin_ec = Q('0cm')
        rmax_ec = self.BarrelRmin
        dz_ec = (self.caloThickness+self.ECCurvRad+self.ECStraight)/2.
        xpos_ec = Q('0cm')
        ypos_ec = Q('0cm')
        zpos_ec = self.EndcapZ + dz_ec

        barrel_shape = geom.shapes.PolyhedraRegular("kloe_calo_barrel_shape",
                                                    numsides=24,
                                                    rmin=self.BarrelRmin,
                                                    rmax=self.BarrelRmin + 
                                                    self.caloThickness+self.AlPlateThick,
                                                    dz=self.BarrelDZ,
                                                    sphi=Q('7.5deg'))

        endcap_shape = geom.shapes.Tubs("kloe_calo_endcap_shape",
                                        rmin=rmin_ec,
                                        rmax=rmax_ec,
                                        dz=dz_ec)
        
        
        # volume to be removed from MagIntVol_vol to make room for yoke endcap
        yoke_endcap_shape = geom.shapes.Tubs("yoke_endcap_shape_cl", rmin=self.EndcapDRmin, rmax=self.EndcapDRmax, dz=0.5 * (self.EndcapCZEnd - self.EndcapDZStart))

        calo_eca_pos = geom.structure.Position("calo_eca_pos", xpos_ec,
                                                ypos_ec, -zpos_ec)

        calo_ecb_pos = geom.structure.Position("calo_ecb_pos", xpos_ec,
                                                ypos_ec, zpos_ec)

        calo_tmp1 = geom.shapes.Boolean("kloe_calo_tmp1",
                                         type='union',
                                         first=barrel_shape,
                                         second=endcap_shape,
                                         pos=calo_eca_pos)

        calo_tmp2 = geom.shapes.Boolean("kloe_calo_tmp2",
                                         type='union',
                                         first=calo_tmp1,
                                         second=endcap_shape,
                                         pos=calo_ecb_pos)
        
        yoke_ec_pos = geom.structure.Position("yoke_ec_pos_cl", Q('0m'), Q('0m'), 0.5 * (self.EndcapDZStart + self.EndcapCZEnd))

        calo_tmp3 = geom.shapes.Boolean("kloe_calo_tmp3",
                                         type='subtraction',
                                         first=calo_tmp2,
                                         second=yoke_endcap_shape,
                                         pos=yoke_ec_pos)
        
        yoke_ec_pos = geom.structure.Position("yoke_ec_pos", Q('0m'), Q('0m'), -0.5 * (self.EndcapDZStart + self.EndcapCZEnd))

        calo_shape = geom.shapes.Boolean("kloe_calo_tmp4",
                                         type='subtraction',
                                         first=calo_tmp3,
                                         second=yoke_endcap_shape,
                                         pos=yoke_ec_pos)

        calo_lv = geom.structure.Volume('kloe_calo_volume',
                                        material="Air",
                                        shape=calo_shape)

        self.add_volume(calo_lv)

        self.buildECALBarrel(calo_lv, geom)
        self.buildECALEndCaps(calo_lv, geom)

    def buildECALBarrel(self, main_lv, geom):

        # References
        # M. Adinolfi et al., NIM A 482 (2002) 364-386
        # and a talk at the June 2017 ND workshop
        #
        # ECAL is a Pb/SciFi/epoxy sandwich in the volume ratio 42:48:10
        # with an average density of 5.3g/cc
        #
        # fibers are coupled to lightguides at both ends and readout by PMTs
        #
        # BARREL
        # there is a barrel section that is nearly cylindrical, with 24 modules
        # each covering 15 degrees. The modules are 4.3m long, 23cm thick,
        # trapezoids with bases of 52 and 59 cm.

        if self.get_builder("SANDECALBARRELMOD") == None:
            print("SANDECALBARRELMOD builder not found")
            return

        emcalo_module_builder = self.get_builder("SANDECALBARRELMOD")
        emcalo_module_lv = emcalo_module_builder.get_volume()

        for j in range(self.NCaloModBarrel):

            axisy = (0, 1, 0)
            axisz = (1, 0, 0)
            ang = 360 / self.NCaloModBarrel
            theta = j * ang
            ModPosition = [
                Q('0mm'),
                Q('0mm'), self.BarrelRmin + 0.5 * self.caloThickness + 0.5*self.AlPlateThick
            ]
            ModPositionNew = ltools.rotation(
                axisy, theta, ModPosition
            )  #Rotating the position vector (the slabs will be rotated automatically after append)
            ModPositionNew = ltools.rotation(axisz, -90, ModPositionNew)

            ECAL_position = geom.structure.Position(
                'ECAL_position' + '_' + str(j), ModPositionNew[0],
                ModPositionNew[1], ModPositionNew[2])

            ECAL_rotation = geom.structure.Rotation(
                'ECAL_rotation' + '_' + str(j), Q('90deg'), -theta * Q('1deg'),
                Q('0deg'))  #Rotating the module on its axis accordingly

            print(("Building Kloe ECAL module " + str(j)))  # keep compatibility with Python3 pylint: disable=superfluous-parens

            ####Placing and appending the j ECAL Module#####

            ECAL_place = geom.structure.Placement('ECAL_place' + '_' + str(j),
                                                  volume=emcalo_module_lv,
                                                  pos=ECAL_position,
                                                  rot=ECAL_rotation)
            
            main_lv.placements.append(ECAL_place.name)

    def buildECALEndCaps(self, main_lv, geom):

        # Real ENDCAP as 32 modules of different length and widht
        # curved at both ends by 90 degrees

        if self.get_builder("SANDECALENDCAP") == None:
            print("SANDECALENDCAP builder not found")
            return

        emcalo_endcap_builder = self.get_builder("SANDECALENDCAP")
        emcalo_endcap_lv = emcalo_endcap_builder.get_volume()

        pos = [Q('0m'), Q('0m'), Q('0m')]
        pos[2] = -(self.EndcapZ + (self.caloThickness + self.ECCurvRad + self.ECStraight) / 2.0)
        
        ECAL_endA_rotation = geom.structure.Rotation(
            'ECAL_endA_rotation', Q('0deg'), Q('180deg'), Q('0deg'))

        ECAL_endA_position = geom.structure.Position(
            'ECAL_endA_position', pos[0], pos[1], pos[2])
        
        ECAL_endB_rotation = geom.structure.Rotation(
            'ECAL_endB_rotation', Q('0deg'), Q('0deg'), Q('0deg'))

        ECAL_endB_position = geom.structure.Position(
            'ECAL_endB_position', pos[0], pos[1], -pos[2])

        print(("Building Kloe ECAL Endcap"))  # keep compatibility with Python3 pylint: disable=superfluous-parens

        ECAL_endA_place = geom.structure.Placement("ECAL_endA_pla",
                                            volume=emcalo_endcap_lv,
                                            pos=ECAL_endA_position,
                                            rot=ECAL_endA_rotation)
        
        ECAL_endB_place = geom.structure.Placement("ECAL_endB_pla",
                                            volume=emcalo_endcap_lv,
                                            pos=ECAL_endB_position,
                                            rot=ECAL_endB_rotation)

        main_lv.placements.append(ECAL_endA_place.name)
        main_lv.placements.append(ECAL_endB_place.name)