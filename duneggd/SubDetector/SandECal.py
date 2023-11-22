#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandECalBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, **kwds):
        self.NCaloModBarrel = 24
        self.caloThickness = Q('23cm')
        self.EndcapZ = Q('1.69m')
        self.EndcapRmin = Q('20.8cm')
        self.BarrelRmin = Q('2m')
        self.BarrelDZ = Q('2.15m')
        self.ECCurvRad = Q('10cm')
        self.ECStraight = Q('20cm')
        self.AlPlateThick= Q('2.5cm')

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

        calo_eca_pos = geom.structure.Position("calo_eca_pos", xpos_ec,
                                                ypos_ec, -zpos_ec)

        calo_ecb_pos = geom.structure.Position("calo_ecb_pos", xpos_ec,
                                                ypos_ec, zpos_ec)

        calo_tmp = geom.shapes.Boolean("kloe_calo_tmp",
                                         type='union',
                                         first=barrel_shape,
                                         second=endcap_shape,
                                         pos=calo_eca_pos)

        calo_shape = geom.shapes.Boolean("kloe_calo_shape",
                                         type='union',
                                         first=calo_tmp,
                                         second=endcap_shape,
                                         pos=calo_ecb_pos)

        calo_lv = geom.structure.Volume('kloe_calo_volume',
                                        material="Air",
                                        shape=calo_shape)

        self.add_volume(calo_lv)
# Test 22/5/2023
        self.buildECALBarrel(calo_lv, geom)
        self.buildECALEndCapA(calo_lv, geom)
        self.buildECALEndCapB(calo_lv, geom)

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

            ################################################

    def buildECALEndCapA(self, main_lv, geom):

        # Real ENDCAP as 32 modules of different length and widht
        # curved at both ends by 90 degrees

        if self.get_builder("SANDECALECMOD") == None:
            print("SANDECALECMOD builder not found")
            return

        emcalo_endcap_builder = self.get_builder("SANDECALECMOD")
        emcalo_endcap_lv = emcalo_endcap_builder.get_volume()

        for quarter in range (0,2):

            pos = [Q('0m'), Q('0m'), Q('0m')]
            pos[2] = -(self.EndcapZ + (self.caloThickness + self.ECCurvRad + self.ECStraight) / 2.0)
            if (quarter == 0):
                ECAL_endA_rotation = geom.structure.Rotation(
                    'ECAL_endA_rotation' + '_' + str(quarter), Q('0deg'),
                    Q('180deg'), Q('0deg'))

            else:
                ECAL_endA_rotation = geom.structure.Rotation(
                    'ECAL_endA_rotation' + '_' + str(quarter), Q('0deg'),
                    Q('180deg'), Q('180deg'))

            ECAL_endA_position = geom.structure.Position(
                'ECAL_endA_position' + '_' + str(quarter), pos[0], pos[1], pos[2])

            print(("Building Kloe ECAL Endcap A quarter " + str(quarter)))  # keep compatibility with Python3 pylint: disable=superfluous-parens

            ########################################################################################
            ECAL_endA_place = geom.structure.Placement("ECAL_endA_pla" + '_' +
                                                      str(quarter),
                                                      volume=emcalo_endcap_lv,
                                                      pos=ECAL_endA_position,
                                                      rot=ECAL_endA_rotation)

            main_lv.placements.append(ECAL_endA_place.name)
            ########################################################################################

    def buildECALEndCapB(self, main_lv, geom):

        # Real ENDCAP as 32 modules of different length and widht
        # curved at both ends by 90 degrees

        if self.get_builder("SANDECALECMOD") == None:
            print("SANDECALECMOD builder not found")
            return

        emcalo_endcap_builder = self.get_builder("SANDECALECMOD")
        emcalo_endcap_lv = emcalo_endcap_builder.get_volume()

        for quarter in range (0,2):

            pos = [Q('0m'), Q('0m'), Q('0m')]
            pos[2] = self.EndcapZ + (self.caloThickness + self.ECCurvRad + self.ECStraight) / 2.0
            if (quarter == 0):
                ECAL_endB_rotation = geom.structure.Rotation(
                    'ECAL_endB_rotation' + '_' + str(quarter), Q('0deg'),
                    Q('0deg'), Q('0deg'))

            else:
                ECAL_endB_rotation = geom.structure.Rotation(
                    'ECAL_endB_rotation' + '_' + str(quarter), Q('0deg'),
                    Q('0deg'), Q('180deg'))

            ECAL_endB_position = geom.structure.Position(
                'ECAL_endB_position' + '_' + str(quarter), pos[0], pos[1], pos[2])

            print(("Building Kloe ECAL Endcap B quarter " + str(quarter)))  # keep compatibility with Python3 pylint: disable=superfluous-parens

            ########################################################################################
            ECAL_endB_place = geom.structure.Placement("ECAL_endB_pla" + '_' +
                                                      str(quarter),
                                                      volume=emcalo_endcap_lv,
                                                      pos=ECAL_endB_position,
                                                      rot=ECAL_endB_rotation)

            main_lv.placements.append(ECAL_endB_place.name)
            ########################################################################################

