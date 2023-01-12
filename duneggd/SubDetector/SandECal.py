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

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        ang = math.pi / self.NCaloModBarrel

        # barrel
        rmax_barrel = (self.BarrelRmin + self.caloThickness) / math.cos(ang)
        # endcap
        rmax_ec = rmax_barrel
        dz_ec = 0.5 * self.caloThickness
        zpos_ec = self.EndcapZ + 0.5 * self.caloThickness

        #        barrel_shape = geom.shapes.Tubs("kloe_calo_barrel_shape", rmin=self.BarrelRmin, rmax=rmax_barrel, dz=self.BarrelDZ)
        barrel_shape = geom.shapes.PolyhedraRegular("kloe_calo_barrel_shape",
                                                    numsides=24,
                                                    rmin=self.BarrelRmin,
                                                    rmax=self.BarrelRmin +
                                                    self.caloThickness,
                                                    dz=self.BarrelDZ,
                                                    sphi=Q('7.5deg'))
        endcap_shape = geom.shapes.Tubs("kloe_calo_endcap_shape",
                                        rmin=Q('0m'),
                                        rmax=rmax_ec,
                                        dz=dz_ec)

        calo_ec_R_pos = geom.structure.Position("calo_ec_R_pos", Q('0m'),
                                                Q('0m'), zpos_ec)

        calo_shape_tmp = geom.shapes.Boolean("kloe_calo_shape_tmp",
                                             type='union',
                                             first=barrel_shape,
                                             second=endcap_shape,
                                             rot='noRotate',
                                             pos=calo_ec_R_pos)

        calo_ec_L_pos = geom.structure.Position("calo_ec_L_pos", Q('0m'),
                                                Q('0m'), -zpos_ec)

        calo_shape = geom.shapes.Boolean("kloe_calo_shape",
                                         type='union',
                                         first=calo_shape_tmp,
                                         second=endcap_shape,
                                         rot='r180aboutY',
                                         pos=calo_ec_L_pos)

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
                Q('0mm'), self.BarrelRmin + 0.5 * self.caloThickness
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

    def buildECALEndCaps(self, main_lv, geom):

        # ENDCAPs
        # there are two endcaps which are 23 cm thick, roughly 2m outer radius,
        # 0.208m inner radius and divided into 32 modules
        # which run vertically, and curve 90degrees at the end to be read out
        # this is nontrivial to model and will take some work and improvements
        # to gegede
        # just model as a disk with a hole
        # segmentation is the same as for the barrel modules

        if self.get_builder("SANDECALENDCAP") == None:
            print("SANDECALENDCAP builder not found")
            return

        emcalo_endcap_builder = self.get_builder("SANDECALENDCAP")
        emcalo_endcap_lv = emcalo_endcap_builder.get_volume()

        for side in ['L', 'R']:

            pos = [Q('0m'), Q('0m'), Q('0m')]
            pos[2] = self.EndcapZ + self.caloThickness / 2.0
            if side == 'L':
                pos[2] = -pos[2]
                ECAL_end_rotation = geom.structure.Rotation(
                    'ECAL_end_rotation' + '_' + str(side), Q('0deg'),
                    Q('180deg'), Q('0deg'))

            else:
                ECAL_end_rotation = geom.structure.Rotation(
                    'ECAL_end_rotation' + '_' + str(side), Q('0deg'),
                    Q('0deg'), Q('0deg'))

            ECAL_end_position = geom.structure.Position(
                'ECAL_end_position' + '_' + str(side), pos[0], pos[1], pos[2])

            print(("Building Kloe ECAL Endcap module " + str(side)))  # keep compatibility with Python3 pylint: disable=superfluous-parens

            ########################################################################################
            ECAL_end_place = geom.structure.Placement("ECAL_end_pla" + '_' +
                                                      str(side),
                                                      volume=emcalo_endcap_lv,
                                                      pos=ECAL_end_position,
                                                      rot=ECAL_end_rotation)

            main_lv.placements.append(ECAL_end_place.name)
            ########################################################################################
