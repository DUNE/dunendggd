#!/usr/bin/env python
'''
NDHPgTPC_SPYv3_Builder: Builds the multi purpose tracker
'''

import gegede.builder
from gegede import Quantity as Q
from math import asin, sqrt


class NDGArLite(gegede.builder.Builder):
    '''
    Build a concept of the ND HPgTPC detector. This class directly
    sub-builders for the GArTPC, the ECAL and for the Yoke.

    Arguments:
    innerBField: the magnetic field inside of the magnet
    buildTrackerSc: Flag to build the Tracker planes
    buildCryostat: Flag to build the cryostat
    buildYoke: Flag to build the Yoke

    '''

    defaults = dict(innerBField="0.5 T, 0.0 T, 0.0 T",
                    TrackerScStepLimit="1 mm",
                    buildTrackerSc=True,
                    buildYoke=False,
                    buildCryostat=False,
                    space=Q("10cm")
                    )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        ''' Top level volume (MPD) - It is rotated later in the cavern (x, y, z) -> (z, y, x)'''

        magnet_shape = geom.get_shape("Cryostat")
        r = magnet_shape.rmax
        dz = magnet_shape.dz

        if self.buildYoke == True:
            eyoke_shape = geom.get_shape("YokeEndcap_max")
            if r < eyoke_shape.rmax:
                r = eyoke_shape.rmax
            if dz < eyoke_shape.dz:
                dz = eyoke_shape.dz

        dx_main = r+self.space  # dimension along the beam
        dy_main = r+self.space  # dimension in height
        dz_main = dz+self.space  # dimension perp to the beam

        print(("Dimension of the MPD in along the beam ", dx_main*2,
              " dimension in height ", dy_main*2, " and dimension perp to the beam ", dz_main*2))

        main_shape = geom.shapes.Box('MPD', dx=dx_main, dy=dy_main, dz=dz_main)
        main_lv = geom.structure.Volume(
            'vol'+main_shape.name, material='Air', shape=main_shape)

        self.add_volume(main_lv)

        ##### build a fake volume that contains the MPD without the magnet to define the magnetized volume correctly ###
        # fake_lv = self.buildMagnetizedVolume(main_lv, geom)

        ######### build the TPC       ##########################
        # use GArTPC Builder, but "disable" the cyrostat by tweaking
        # EndcapThickness, WallThickness, and ChamberMaterial
        # do that in the cfg file
        if self.buildTrackerSc:
            print("Adding TrackerSc to main volume")
            self.build_trackersc(main_lv, geom)

        ######### magnet ##################################
        # Build a simple magnet of Al to get the total mass
        # A description of the return magnetic field and the coils is not implemented
        if self.buildCryostat:
            print("Adding Cryostat+Coils to main volume")
            self.build_cryostat(main_lv, geom)

        ######### magnet yoke ##################################
        # Build the yoke Barrel and Endcaps
        # A description of the return magnetic field and the coils is not implemented
        if self.buildYoke:
            print("Adding Yoke to main volume")
            self.build_yoke(main_lv, geom)

        return

    def buildMagnetizedVolume(self, main_lv, geom):
        '''Magnetized volume (fake volume) for G4 that includes the TPC + ECAL only'''

        print("Making fake magnetized volume and adding to main volume")

        eECal_shape = geom.get_shape("ECALEndcap_max")
        fake_shape = geom.shapes.PolyhedraRegular('NDHPgTPC', numsides=eECal_shape.numsides, rmin=Q(
            "0m"), rmax=eECal_shape.rmax, dz=eECal_shape.dz)
        fake_lv = geom.structure.Volume(
            'vol'+fake_shape.name, material='Air', shape=fake_shape)
        fake_lv.params.append(("BField", self.innerBField))
        rot_z = Q("90.0deg")-Q("180.0deg")/eECal_shape.numsides
        fake_lv_rot = geom.structure.Rotation(fake_lv.name+"_rot", z=rot_z)
        fake_pla = geom.structure.Placement(
            "NDHPgTPC"+"_pla", volume=fake_lv, rot=fake_lv_rot)
        # Place it in the main lv
        main_lv.placements.append(fake_pla.name)

        return fake_lv

    def build_trackersc(self, main_lv, geom):

        #Build TPC
        trackersc_builder = self.get_builder('TrackerScBuilder')
        if trackersc_builder == None:
            return

        trackersc_vol = trackersc_builder.get_volume()
        # Add the magnetic field to the volume
        trackersc_vol.params.append(("BField", self.innerBField))
        trackersc_vol.params.append(("StepLimit", self.TrackerScStepLimit))

        trackersc_pla = geom.structure.Placement("TrackerSc"+"_pla", volume=trackersc_vol)
        # Place it in the main lv
        main_lv.placements.append(trackersc_pla.name)

    def build_cryostat(self, main_lv, geom):

        #Build the PV Barrel
        cryostat_builder = self.get_builder('CryostatBuilder')
        if cryostat_builder == None:
            return

        cryo_vol = cryostat_builder.get_volume("volCryostat")
        cryo_pla = geom.structure.Placement("Cryostat"+"_pla", volume=cryo_vol)
        # Place it in the main lv
        main_lv.placements.append(cryo_pla.name)

        rot_z = Q("0.0deg")
        ecryo_vol = cryostat_builder.get_volume("volCryostatEndcap")
        ecryo_rot = geom.structure.Rotation(ecryo_vol.name+"_rot", z=rot_z)
        ecryo_pla = geom.structure.Placement(
            "CryostatEndcap"+"_pla", volume=ecryo_vol, rot=ecryo_rot)

        # Place it in the main lv
        main_lv.placements.append(ecryo_pla.name)

    def build_yoke(self, main_lv, geom):

        yoke_builder = self.get_builder('YokeBuilder')
        if yoke_builder == None:
            return

        byoke_vol = yoke_builder.get_volume("volYokeBarrel")
        yoke_shape = geom.store.shapes.get(byoke_vol.shape)
        nsides = yoke_shape.numsides
        print(("Number of yoke sides", nsides))

        rot_z = Q("90.0deg")-Q("180.0deg")/nsides
        if nsides == 16:
            rot_z = rot_z + Q("22.5deg")

        byoke_rot = geom.structure.Rotation(byoke_vol.name+"_rot", z=rot_z)
        byoke_pla = geom.structure.Placement(
            "YokeBarrel"+"_pla", volume=byoke_vol, rot=byoke_rot)

        # Place it in the main lv
        main_lv.placements.append(byoke_pla.name)

        eyoke_vol = yoke_builder.get_volume("volYokeEndcap")
        eyoke_rot = geom.structure.Rotation(eyoke_vol.name+"_rot", z=rot_z)
        eyoke_pla = geom.structure.Placement(
            "YokeEndcap"+"_pla", volume=eyoke_vol, rot=eyoke_rot)

        # Place it in the main lv
        main_lv.placements.append(eyoke_pla.name)
