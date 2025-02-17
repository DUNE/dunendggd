#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandECalEndcapBuilder(gegede.builder.Builder):
    # ^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(
        self,
        EndcapDim=None,
        EndcapModDim=None,
        ScintMat=None,
        PasMat=None,
        PasSlabThickness=None,
        ActiveSlabThickness=None,
        nSlabs=None,
        BackPlateThick=None,
        **kwds
    ):
        self.EndcapDim = EndcapDim
        self.EndcapModDim = EndcapModDim
        self.ScintMat = ScintMat
        self.PasMat = PasMat
        self.PasSlabThickness = PasSlabThickness
        self.ActiveSlabThickness = ActiveSlabThickness
        self.nSlabs = nSlabs
        self.BackPlateThick = BackPlateThick

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

    # ^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        rmax_ec = self.EndcapDim[0]
        KLOEEndcapECALDepth = self.EndcapDim[2]
        KLOEEndcapCurvRadius = self.EndcapDim[3]
        KLOEEndcapStraight = self.EndcapDim[4]
        KLOECellWidth = self.EndcapDim[5]
        KLOEEndcapModDy = self.EndcapModDim
        AlPlateThick = self.BackPlateThick
        ColPerMod = 6
        XPosMod = -3 * KLOECellWidth
        ECTubsSize = (
            KLOEEndcapECALDepth + KLOEEndcapCurvRadius + KLOEEndcapStraight
        )

        ##########creating main straight part of the ECAL endcap module##########

        ECAL_endcap_shape_base = geom.shapes.Tubs(
            "ECAL_endcap_shape_base", rmin=Q("0m"), rmax=rmax_ec, dz=ECTubsSize / 2.0
        )
        
        # volume to be removed from MagIntVol_vol to make room for yoke endcap
        yoke_endcap_shape = geom.shapes.Tubs("yoke_endcap_shape_ec", rmin=self.EndcapDRmin, rmax=self.EndcapDRmax, dz=0.5 * (self.EndcapCZEnd - self.EndcapDZStart))
        
        yoke_ec_pos = geom.structure.Position("yoke_ec_pos_ec", Q('0m'), Q('0m'), 0.5 * (self.EndcapDZStart + self.EndcapCZEnd) - Q('1.955m'))

        ECAL_endcap_shape = geom.shapes.Boolean("ECAL_endcap_shape",
                                         type='subtraction',
                                         first=ECAL_endcap_shape_base,
                                         second=yoke_endcap_shape,
                                         pos=yoke_ec_pos)
        
        ECAL_endcap_lv = geom.structure.Volume(
            "ECAL_endcap_lv", material="Air", shape=ECAL_endcap_shape
        )
        self.add_volume(ECAL_endcap_lv)

        ZPosMod = (-ECTubsSize + KLOEEndcapECALDepth) / 2.0

        for mod in range(0, 16):
            print(("Building ECAL Endcap Module " + str(mod)))

            # width of the module
            if mod > 1 and mod < 12:
                ColPerMod = 3
            elif mod > 11:
                ColPerMod = 2

            # y position of the module
            if mod < 2:
                YPosMod = Q("111.35cm")
            else:
                YPosMod = Q("0cm")

            # x position of the module
            if mod == 2:
                XPosMod += KLOECellWidth * 4.5
            elif mod == 12:
                XPosMod += KLOECellWidth * 2.5
            elif mod > 0:
                XPosMod += KLOECellWidth * ColPerMod

            ###############################################################################
            ########## creating the volume of the ECAL endcap module ######################
            ###############################################################################

            # The endcap module shape is the union of 5 (4 for the central modules, i.e. mod == 0)
            # shapes. Out of the 5 shapes, only 3 are different:
            # - the vertical element  : [A]
            # - the curved element    : [B]
            # - the horizontal element: [C]

            ################################################################################
            #             "DEFAULT MODULE"         ##             "CENTRAL MODULE"         #
            # (Y)                                  ## (Y)                                  #
            #  ^      /----------|                 ##  ^      /----------|                 #
            #  |     /   |   [C] |                 ##  |     /   |   [C] |                 #
            #  |    / [B]/-------|                 ##  |    / [B]/-------|                 #
            #  |   /----/                          ##  |   /----/                          #
            #  |   |    |                          ##  |   |    |                          #
            #  |   |[A] |                          ##  |   |[A] |                          #
            #  |   |    |                          ##  |   |    |                          #
            #  |   \----\                          ##  |   \----\                          #
            #  |    \ [B]\-------|                 ##  |    \ [B]\                         #
            #  |     \    |  [C] |                 ##  |     \    |                        #
            #  |      \----------|                 ##  |      \---|                        #
            #  |---------------------------> (X)   ##  |---------------------------> (X)   #
            ################################################################################

            # Here we create the basic shapes: vertical, curved, horizontal
            ECAL_ec_mod_vert_shape = geom.shapes.Box(
                "ECAL_mod_" + str(mod) + "_shape1",
                dx=KLOECellWidth * ColPerMod / 2.0,
                dy=KLOEEndcapModDy[mod],
                dz=0.5 * (KLOEEndcapECALDepth + AlPlateThick),
            )

            ECAL_ec_mod_curv_shape = geom.shapes.Tubs(
                "ECAL_ec_mod_curv_" + str(mod) + "_shape1",
                rmin=KLOEEndcapCurvRadius - AlPlateThick,
                rmax=KLOEEndcapCurvRadius + KLOEEndcapECALDepth,
                dz=KLOECellWidth * ColPerMod / 2.0,
                sphi=math.pi / 2.0,
                dphi=math.pi / 2.0,
            )

            ECAL_ec_mod_hor_shape = geom.shapes.Box(
                "ECAL_ec_mod_hor_" + str(mod) + "_shape1",
                dx=KLOECellWidth * ColPerMod / 2.0,
                dy=KLOEEndcapStraight / 2.0,
                dz=0.5 * (KLOEEndcapECALDepth + AlPlateThick),
            )

            # These are the parameters of the ec module shape
            Curv_y_pos = KLOEEndcapModDy[mod] + YPosMod
            Curv_z_pos = (
                ZPosMod + KLOEEndcapECALDepth / 2.0 + KLOEEndcapCurvRadius
            )
            Straight_y_pos = (
                Curv_y_pos
                + KLOEEndcapCurvRadius
                + 0.5 * (KLOEEndcapECALDepth - AlPlateThick)
            )
            Straight_z_pos = Curv_z_pos + KLOEEndcapStraight / 2.0
            if mod < 2:
                Curv_y_bottom = -KLOEEndcapModDy[mod] + YPosMod
            else:
                Curv_y_bottom = -Curv_y_pos

            # Here we define positions and rotation of each element with
            # respect to the vertical one
            ECAL_ec_mod_curv_top_pos1 = geom.structure.Position(
                "ECAL_ec_mod_curv_" + str(mod) + "_top_pos1",
                XPosMod - XPosMod,
                Curv_y_pos - YPosMod,
                Curv_z_pos - (ZPosMod + 0.5 * AlPlateThick),
            )

            ECAL_ec_mod_curv_top_rot1 = geom.structure.Rotation(
                "ECAL_ec_mod_curv_" + str(mod) + "_top_rot1",
                Q("0deg"),
                Q("-90deg"),
                Q("0deg"),
            )

            ECAL_ec_mod_curv_bot_pos1 = geom.structure.Position(
                "ECAL_ec_mod_curv_" + str(mod) + "_bot_pos1",
                XPosMod - XPosMod,
                Curv_y_bottom - YPosMod,
                Curv_z_pos - (ZPosMod + 0.5 * AlPlateThick),
            )

            ECAL_ec_mod_curv_bot_rot1 = geom.structure.Rotation(
                "ECAL_ec_mod_curv_" + str(mod) + "_bot_rot1",
                Q("0deg"),
                Q("-90deg"),
                Q("180deg"),
            )

            ECAL_ec_mod_hor_top_pos1 = geom.structure.Position(
                "ECAL_ec_mod_hor_" + str(mod) + "_top_pos1",
                XPosMod - XPosMod,
                Straight_y_pos - YPosMod,
                Straight_z_pos - (ZPosMod + 0.5 * AlPlateThick),
            )

            ECAL_ec_mod_hor_top_rot1 = geom.structure.Rotation(
                "ECAL_ec_mod_hor_" + str(mod) + "_top_rot1",
                Q("90deg"),
                Q("0deg"),
                Q("0deg"),
            )

            ECAL_ec_mod_hor_bot_pos1 = geom.structure.Position(
                "ECAL_ec_mod_hor_" + str(mod) + "_bot_pos1",
                XPosMod - XPosMod,
                -Straight_y_pos - YPosMod,
                Straight_z_pos - (ZPosMod + 0.5 * AlPlateThick),
            )

            ECAL_ec_mod_hor_bot_rot1 = geom.structure.Rotation(
                "ECAL_ec_mod_hor_" + str(mod) + "_bot_rot1",
                Q("-90deg"),
                Q("0deg"),
                Q("0deg"),
            )

            # Here we create the ec module shape
            ECAL_ec_mod_step1 = geom.shapes.Boolean(
                "ECAL_ec_mod_" + str(mod) + "_step1",
                type="union",
                first=ECAL_ec_mod_vert_shape,
                second=ECAL_ec_mod_curv_shape,
                pos=ECAL_ec_mod_curv_top_pos1,
                rot=ECAL_ec_mod_curv_top_rot1,
            )

            ECAL_ec_mod_step2 = geom.shapes.Boolean(
                "ECAL_ec_mod_" + str(mod) + "_step2",
                type="union",
                first=ECAL_ec_mod_step1,
                second=ECAL_ec_mod_curv_shape,
                pos=ECAL_ec_mod_curv_bot_pos1,
                rot=ECAL_ec_mod_curv_bot_rot1,
            )

            ECAL_ec_mod_shape = geom.shapes.Boolean(
                "ECAL_ec_mod_" + str(mod) + "_shape",
                type="union",
                first=ECAL_ec_mod_step2,
                second=ECAL_ec_mod_hor_shape,
                pos=ECAL_ec_mod_hor_top_pos1,
                rot=ECAL_ec_mod_hor_top_rot1,
            )

            if mod > 1:
                ECAL_ec_mod_shape = geom.shapes.Boolean(
                    "ECAL_ec_central_mod_" + str(mod) + "_shape",
                    type="union",
                    first=ECAL_ec_mod_shape,
                    second=ECAL_ec_mod_hor_shape,
                    pos=ECAL_ec_mod_hor_bot_pos1,
                    rot=ECAL_ec_mod_hor_bot_rot1,
                )

            ECAL_ec_mod_lv = geom.structure.Volume(
                "ECAL_ec_mod_" + str(mod) + "_lv",
                material="Air",
                shape=ECAL_ec_mod_shape,
            )

            ###############################################################################
            ########## creating and appending the vertical part to the ECAL endcap ########
            ###############################################################################

            ECAL_ec_mod_vert_lv = self.get_ec_module_vert(geom, mod, ColPerMod)

            ECAL_ec_mod_vert_pla = geom.structure.Placement(
                "ECAL_ec_mod_vert_" + str(mod) + "_pla",
                volume=ECAL_ec_mod_vert_lv,
            )

            ECAL_ec_mod_lv.placements.append(ECAL_ec_mod_vert_pla.name)

            ###############################################################################
            ########## creating and appending the curved part to the ECAL endcap ##########
            ###############################################################################

            ECAL_ec_mod_curv_lv = self.get_ec_module_curv(geom, mod, ColPerMod)

            # Using the same rotation used to contruct composite shape
            # results in 16 overlaps. Why????
            ECAL_ec_mod_curv_top_rot2 = geom.structure.Rotation(
                "ECAL_ec_mod_curv_" + str(mod) + "_top_rot2",
                Q("0deg"),
                Q("90deg"),
                Q("0deg"),
            )

            ECAL_ec_mod_curv_top_pla = geom.structure.Placement(
                "ECAL_ec_mod_curv_" + str(mod) + "_top_pla",
                volume=ECAL_ec_mod_curv_lv,
                pos=ECAL_ec_mod_curv_top_pos1,
                rot=ECAL_ec_mod_curv_top_rot2,
            )

            ECAL_ec_mod_curv_bot_pla = geom.structure.Placement(
                "ECAL_ec_mod_curv_" + str(mod) + "_bot_pla",
                volume=ECAL_ec_mod_curv_lv,
                pos=ECAL_ec_mod_curv_bot_pos1,
                rot=ECAL_ec_mod_curv_bot_rot1,
            )

            ECAL_ec_mod_lv.placements.append(ECAL_ec_mod_curv_top_pla.name)
            ECAL_ec_mod_lv.placements.append(ECAL_ec_mod_curv_bot_pla.name)

            ###############################################################################
            ########## creating and appending the horizontal part to the ECAL endcap ######
            ###############################################################################

            ECAL_ec_mod_hor_lv = self.get_ec_module_hor(geom, mod, ColPerMod)

            ECAL_ec_mod_hor_top_pla = geom.structure.Placement(
                "ECAL_ec_mod_hor_" + str(mod) + "_top_pla",
                volume=ECAL_ec_mod_hor_lv,
                pos=ECAL_ec_mod_hor_top_pos1,
                rot=ECAL_ec_mod_hor_top_rot1,
            )

            ECAL_ec_mod_hor_bot_pla = geom.structure.Placement(
                "ECAL_ec_mod_hor_" + str(mod) + "_bot_pla",
                volume=ECAL_ec_mod_hor_lv,
                pos=ECAL_ec_mod_hor_bot_pos1,
                rot=ECAL_ec_mod_hor_bot_rot1,
            )

            ECAL_ec_mod_lv.placements.append(ECAL_ec_mod_hor_top_pla.name)

            if mod > 1:
                ECAL_ec_mod_lv.placements.append(ECAL_ec_mod_hor_bot_pla.name)

            ###############################################################################
            ########## positioning of endcap modules ######################################
            ###############################################################################

            # positioning of ec module
            ECAL_ec_mod_pos = geom.structure.Position(
                "ECAL_ec_mod_" + str(mod) + "_pos",
                XPosMod,
                YPosMod,
                ZPosMod + 0.5 * AlPlateThick,
            )

            ECAL_ec_mod_rot = geom.structure.Rotation(
                "ECAL_ec_mod_" + str(mod) + "_rot",
                Q("0deg"),
                Q("0deg"),
                Q("0deg"),
            )

            ECAL_ec_mod_pla = geom.structure.Placement(
                "ECAL_ec_mod_" + str(mod) + "_pla",
                volume=ECAL_ec_mod_lv,
                pos=ECAL_ec_mod_pos,
                rot=ECAL_ec_mod_rot,
            )

            ECAL_endcap_lv.placements.append(ECAL_ec_mod_pla.name)

            mod += 16
            ECAL_ec_mod_pos = geom.structure.Position(
                "ECAL_ec_mod_" + str(mod) + "_pos",
                -XPosMod,
                -YPosMod,
                ZPosMod + 0.5 * AlPlateThick,
            )

            ECAL_ec_mod_rot = geom.structure.Rotation(
                "ECAL_ec_mod_" + str(mod) + "_rot",
                Q("0deg"),
                Q("0deg"),
                Q("180deg"),
            )

            ECAL_ec_mod_pla = geom.structure.Placement(
                "ECAL_ec_mod_" + str(mod) + "_pla",
                volume=ECAL_ec_mod_lv,
                pos=ECAL_ec_mod_pos,
                rot=ECAL_ec_mod_rot,
            )

            ECAL_endcap_lv.placements.append(ECAL_ec_mod_pla.name)

    # create the vertical part of the ECAL endcap module
    def get_ec_module_vert(self, geom, mod, nCols):

        # params
        KLOEEndcapECALDepth = self.EndcapDim[2]
        KLOECellWidth = self.EndcapDim[5]
        KLOEEndcapModDy = self.EndcapModDim
        AlPlateThick = self.BackPlateThick

        # create endcap module vertical part volume
        ECAL_ec_mod_vert_shape = geom.shapes.Box(
            "ECAL_mod_" + str(mod) + "_shape",
            dx=KLOECellWidth * nCols / 2.0,
            dy=KLOEEndcapModDy[mod],
            dz=0.5 * (KLOEEndcapECALDepth + AlPlateThick),
        )

        ECAL_ec_mod_vert_lv = geom.structure.Volume(
            "ECAL_ec_mod_vert_" + str(mod) + "_lv",
            material="Air",
            shape=ECAL_ec_mod_vert_shape,
        )

        ########## creating the Aluminium plate for the endcap modules##########

        ECAL_end_Alplate_shape = geom.shapes.Box(
            "endECALAlplate_" + str(mod),
            dx=KLOECellWidth * nCols / 2.0,
            dy=KLOEEndcapModDy[mod],
            dz=AlPlateThick / 2.0,
        )

        ECAL_end_Alplate_lv = geom.structure.Volume(
            "endvolECALAlplate_" + str(mod),
            material="Aluminum",
            shape=ECAL_end_Alplate_shape,
        )

        ECAL_end_Alplate_pos = geom.structure.Position(
            "endECALAlplatepos_" + str(mod),
            Q("0.0cm"),
            Q("0.0cm"),
            0.5 * KLOEEndcapECALDepth,
        )

        ECAL_end_Alplate_pla = geom.structure.Placement(
            "endECALAlplatepla_" + str(mod),
            volume=ECAL_end_Alplate_lv,
            pos=ECAL_end_Alplate_pos,
        )

        ECAL_ec_mod_vert_lv.placements.append(ECAL_end_Alplate_pla.name)

        ########## creating active slab volumes ##########

        endECALActiveSlab = geom.shapes.Box(
            "endECALActiveSlab_" + str(mod),
            dx=KLOECellWidth * nCols / 2.0,
            dy=KLOEEndcapModDy[mod],
            dz=0.5 * self.ActiveSlabThickness,
        )

        endECALActiveSlab_lv = geom.structure.Volume(
            "endvolECALActiveSlab_" + str(mod),
            material=self.ScintMat,
            shape=endECALActiveSlab,
        )
        endECALActiveSlab_lv.params.append(("SensDet", "EMCalSci"))

        ########## creating passive slab volumes ##########

        endECALPassiveSlab = geom.shapes.Box(
            "endECALPassveSlab_" + str(mod),
            dx=KLOECellWidth * nCols / 2.0,
            dy=KLOEEndcapModDy[mod],
            dz=0.5 * self.PasSlabThickness,
        )

        endECALPassiveSlab_lv = geom.structure.Volume(
            "endvolECALPassiveSlab_" + str(mod),
            material=self.PasMat,
            shape=endECALPassiveSlab,
        )

        ###########################################

        for i in range(self.nSlabs):  # nSlabs

            xposSlab = Q("0cm")
            yposSlab = Q("0cm")

            zposSlabActive = (
                -(KLOEEndcapECALDepth + AlPlateThick) * 0.5
                + (i + 0.5) * self.ActiveSlabThickness
                + i * self.PasSlabThickness
            )

            zposSlabPassive = (
                zposSlabActive
                + 0.5 * self.ActiveSlabThickness
                + 0.5 * self.PasSlabThickness
            )

            ########## appending active slabs to the ECAL endcap##########

            endECALActiveSlabPos = geom.structure.Position(
                "endecalactiveslabpos_" + str(mod) + "_" + str(i),
                xposSlab,
                yposSlab,
                zposSlabActive,
            )

            endECALActiveSlabPlace = geom.structure.Placement(
                "endecalactiveslabpla_" + str(mod) + "_" + str(i),
                volume=endECALActiveSlab_lv,
                pos=endECALActiveSlabPos,
            )

            ECAL_ec_mod_vert_lv.placements.append(endECALActiveSlabPlace.name)

            ########## appending passive slabs to the ECAL endcap##########

            endECALPassiveSlabPos = geom.structure.Position(
                "endecalpassiveslabpos_" + str(mod) + "_" + str(i),
                xposSlab,
                yposSlab,
                zposSlabPassive,
            )

            endECALPassiveSlabPlace = geom.structure.Placement(
                "endecalpassiveslabpla_" + str(mod) + "_" + str(i),
                volume=endECALPassiveSlab_lv,
                pos=endECALPassiveSlabPos,
            )

            ECAL_ec_mod_vert_lv.placements.append(endECALPassiveSlabPlace.name)

        return ECAL_ec_mod_vert_lv

    # create the curved part of the ECAL endcap module
    def get_ec_module_curv(self, geom, mod, nCols):

        KLOEEndcapECALDepth = self.EndcapDim[2]
        KLOEEndcapCurvRadius = self.EndcapDim[3]
        KLOECellWidth = self.EndcapDim[5]
        AlPlateThick = self.BackPlateThick

        ECAL_ec_mod_curv_shape = geom.shapes.Tubs(
            "ECAL_ec_mod_curv_" + str(mod) + "_shape",
            rmin=KLOEEndcapCurvRadius - AlPlateThick,
            rmax=KLOEEndcapCurvRadius + KLOEEndcapECALDepth,
            dz=KLOECellWidth * nCols / 2.0,
            sphi=math.pi / 2.0,
            dphi=math.pi / 2.0,
        )

        ECAL_ec_mod_curv_lv = geom.structure.Volume(
            "ECAL_ec_mod_curv_" + str(mod) + "_lv",
            material="Air",
            shape=ECAL_ec_mod_curv_shape,
        )

        ##########Aluminium plate for the endcap curved part##########

        ECAL_ec_mod_curv_Alplate_shape = geom.shapes.Tubs(
            "ECAL_ec_mod_curv_Alplate_" + str(mod),
            rmin=KLOEEndcapCurvRadius - AlPlateThick,
            rmax=KLOEEndcapCurvRadius,
            dz=KLOECellWidth * nCols / 2.0,
            sphi=math.pi / 2.0,
            dphi=math.pi / 2.0,
        )

        ECAL_ec_mod_curv_Alplate_lv = geom.structure.Volume(
            "ECAL_ec_mod_curv_Alplate_" + str(mod) + "_lv",
            material="Aluminum",
            shape=ECAL_ec_mod_curv_Alplate_shape,
        )

        ECAL_ec_mod_curv_Alplate_pos = geom.structure.Position(
            "ECAL_ec_mod_curv_Alplate_" + str(mod) + "_pos",
            Q("0.0cm"),
            Q("0.0cm"),
            Q("0.0cm"),
        )

        ECAL_ec_mod_curv_Alplate_rot = geom.structure.Rotation(
            "ECAL_ec_mod_curv_Alplate_" + str(mod) + "_rot",
            Q("0deg"),
            Q("0deg"),
            Q("0deg"),
        )

        ECAL_ec_mod_curv_Alplate_pla = geom.structure.Placement(
            "ECAL_ec_mod_curv_Alplate_" + str(mod) + "_pla",
            volume=ECAL_ec_mod_curv_Alplate_lv,
            pos=ECAL_ec_mod_curv_Alplate_pos,
            rot=ECAL_ec_mod_curv_Alplate_rot,
        )

        ECAL_ec_mod_curv_lv.placements.append(ECAL_ec_mod_curv_Alplate_pla.name)

        ################

        for i in range(self.nSlabs):  # nSlabs

            xposSlab = Q("0cm")
            yposSlab = Q("0cm")
            zposSlab = Q("0cm")

            rmaxSlabActive = (KLOEEndcapCurvRadius + KLOEEndcapECALDepth) - (
                i * self.ActiveSlabThickness + i * self.PasSlabThickness
            )

            rmaxSlabPassive = rmaxSlabActive - self.ActiveSlabThickness

            ##########creating and appending active slabs to the ECAL endcap##########

            endECALcurvActiveSlab = geom.shapes.Tubs(
                "endECALcurvActiveSlab_" + str(mod) + "_" + str(i),
                rmax=rmaxSlabActive,
                rmin=rmaxSlabActive - self.ActiveSlabThickness,
                dz=KLOECellWidth * nCols / 2.0,
                sphi=math.pi / 2.0,
                dphi=math.pi / 2.0,
            )

            endECALcurvActiveSlab_lv = geom.structure.Volume(
                "endvolECALcurvActiveSlab_" + str(mod) + "_" + str(i),
                material=self.ScintMat,
                shape=endECALcurvActiveSlab,
            )
            endECALcurvActiveSlab_lv.params.append(("SensDet", "EMCalSci"))

            endECALcurvActiveSlabPos = geom.structure.Position(
                "endecalcurvactiveslabpos_" + str(mod) + "_" + str(i),
                xposSlab,
                yposSlab,
                zposSlab,
            )

            endECALcurvActiveSlabPlace = geom.structure.Placement(
                "endecalcurvactiveslabpla_" + str(mod) + "_" + str(i),
                volume=endECALcurvActiveSlab_lv,
                pos=endECALcurvActiveSlabPos,
            )

            ECAL_ec_mod_curv_lv.placements.append(
                endECALcurvActiveSlabPlace.name
            )

            ##########creating and appending passive slabs to the ECAL endcap##########

            endECALcurvPassiveSlab = geom.shapes.Tubs(
                "endECALcurvPassiveSlab_" + str(mod) + "_" + str(i),
                rmax=rmaxSlabPassive,
                rmin=rmaxSlabPassive - self.PasSlabThickness,
                dz=KLOECellWidth * nCols / 2.0,
                sphi=math.pi / 2,
                dphi=math.pi / 2.0,
            )

            endECALcurvPassiveSlab_lv = geom.structure.Volume(
                "endvolECALcurvPassiveSlab_" + str(mod) + "_" + str(i),
                material=self.PasMat,
                shape=endECALcurvPassiveSlab,
            )

            endECALcurvPassiveSlabPos = geom.structure.Position(
                "endecalcurvpassiveslabpos_" + str(mod) + "_" + str(i),
                xposSlab,
                yposSlab,
                zposSlab,
            )

            endECALcurvPassiveSlabPlace = geom.structure.Placement(
                "endecalcurvpassiveslabpla_" + str(mod) + "_" + str(i),
                volume=endECALcurvPassiveSlab_lv,
                pos=endECALcurvPassiveSlabPos,
            )

            ECAL_ec_mod_curv_lv.placements.append(
                endECALcurvPassiveSlabPlace.name
            )

        return ECAL_ec_mod_curv_lv

    # create the horizontal part of the ECAL endcap module
    def get_ec_module_hor(self, geom, mod, nCols):

        KLOEEndcapECALDepth = self.EndcapDim[2]
        KLOEEndcapStraight = self.EndcapDim[4]
        KLOECellWidth = self.EndcapDim[5]
        AlPlateThick = self.BackPlateThick

        ECAL_ec_mod_hor_shape = geom.shapes.Box(
            "ECAL_ec_mod_hor_" + str(mod) + "_shape",
            dx=KLOECellWidth * nCols / 2.0,
            dy=KLOEEndcapStraight / 2.0,
            dz=0.5 * (KLOEEndcapECALDepth + AlPlateThick),
        )

        ECAL_ec_mod_hor_lv = geom.structure.Volume(
            "ECAL_ec_mod_hor_" + str(mod) + "_lv",
            material="Air",
            shape=ECAL_ec_mod_hor_shape,
        )

        ##########Aluminium plate for the endcap short straight part##########

        ECAL_ec_mod_hor_Alplate_shape = geom.shapes.Box(
            "ECAL_ec_mod_hor_Alplate_" + str(mod) + "_shape",
            dx=KLOECellWidth * nCols / 2.0,
            dy=KLOEEndcapStraight / 2.0,
            dz=AlPlateThick / 2.0,
        )

        ECAL_ec_mod_hor_Alplate_lv = geom.structure.Volume(
            "ECAL_ec_mod_hor_Alplate_" + str(mod) + "_lv",
            material="Aluminum",
            shape=ECAL_ec_mod_hor_Alplate_shape,
        )

        ECAL_ec_mod_hor_Alplate_pos = geom.structure.Position(
            "ECAL_ec_mod_hor_Alplate_" + str(mod) + "_pos",
            Q("0.0cm"),
            Q("0.0cm"),
            -0.5 * KLOEEndcapECALDepth,
        )

        ECAL_ec_mod_hor_Alplate_rot = geom.structure.Rotation(
            "ECAL_ec_mod_hor_Alplate_" + str(mod) + "_rot",
            Q("0deg"),
            Q("0deg"),
            Q("0deg"),
        )

        ECAL_ec_mod_hor_Alplate_pla = geom.structure.Placement(
            "ECAL_ec_mod_hor_Alplate_" + str(mod) + "_pla",
            volume=ECAL_ec_mod_hor_Alplate_lv,
            pos=ECAL_ec_mod_hor_Alplate_pos,
            rot=ECAL_ec_mod_hor_Alplate_rot,
        )

        ECAL_ec_mod_hor_lv.placements.append(ECAL_ec_mod_hor_Alplate_pla.name)

        ###########
        endECALstraightActiveSlab = geom.shapes.Box(
            "endECALstraightActiveSlab_" + str(mod),
            dx=KLOECellWidth * nCols / 2.0,
            dy=KLOEEndcapStraight / 2.0,
            dz=0.5 * self.ActiveSlabThickness,
        )

        endECALstraightActiveSlab_lv = geom.structure.Volume(
            "endvolECALstraightActiveSlab_" + str(mod),
            material=self.ScintMat,
            shape=endECALstraightActiveSlab,
        )
        endECALstraightActiveSlab_lv.params.append(("SensDet", "EMCalSci"))

        endECALstraightPassiveSlab = geom.shapes.Box(
            "endECALstraightPassveSlab_" + str(mod),
            dx=KLOECellWidth * nCols / 2.0,
            dy=KLOEEndcapStraight / 2.0,
            dz=0.5 * self.PasSlabThickness,
        )

        endECALstraightPassiveSlab_lv = geom.structure.Volume(
            "endvolECALstraightPassiveSlab_" + str(mod),
            material=self.PasMat,
            shape=endECALstraightPassiveSlab,
        )

        for i in range(self.nSlabs):  # nSlabs

            xposSlab = Q("0cm")
            yposSlab = Q("0cm")

            zposSlabActive =( (KLOEEndcapECALDepth+AlPlateThick) * 0.5 - 
                            ((i + 0.5) * self.ActiveSlabThickness +
                            i * self.PasSlabThickness) )

            zposSlabPassive = (zposSlabActive - 
                            (0.5 * self.ActiveSlabThickness +
                            0.5 * self.PasSlabThickness))


            ##########creating and appending active slabs to the ECAL endcap##########

            endECALstraightActiveSlabPos = geom.structure.Position(
                "endecalstraightactiveslabpos_" + str(mod) + "_" + str(i),
                xposSlab,
                yposSlab,
                zposSlabActive,
            )

            endECALstraightActiveSlabPlace = geom.structure.Placement(
                "endecalstraightactiveslabpla_" + str(mod) + "_" + str(i),
                volume=endECALstraightActiveSlab_lv,
                pos=endECALstraightActiveSlabPos,
            )

            ECAL_ec_mod_hor_lv.placements.append(
                endECALstraightActiveSlabPlace.name
            )

            ##########creating and appending passive slabs to the ECAL endcap##########

            endECALstraightPassiveSlabPos = geom.structure.Position(
                "endecalstraightpassiveslabpos_" + str(mod) + "_" + str(i),
                xposSlab,
                yposSlab,
                zposSlabPassive,
            )

            endECALstraightPassiveSlabPlace = geom.structure.Placement(
                "endecalstraightpassiveslabpla_" + str(mod) + "_" + str(i),
                volume=endECALstraightPassiveSlab_lv,
                pos=endECALstraightPassiveSlabPos,
            )

            ECAL_ec_mod_hor_lv.placements.append(
                endECALstraightPassiveSlabPlace.name
            )

        return ECAL_ec_mod_hor_lv
