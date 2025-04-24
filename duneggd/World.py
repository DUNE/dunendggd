#!/usr/bin/env python
from subprocess import run
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q
import sys


#Changed DetEnc to Rock
class WorldBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, halfDimension=None, Material=None, RockPosition=None, RockRotation=None, **kwds):
        self.halfDimension = halfDimension
        self.Material = Material
        self.RockPosition = RockPosition
        self.RockRotation = RockRotation

        # Get current git commit hash
        ret = run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
        if ret.returncode == 0:
            self.git_commit = ret.stdout.strip()
            # Get current tag
            ret = run(["git", "describe", "--tags", "HEAD"], capture_output=True, text=True)
            self.git_tag = ret.stdout.strip()
            # Get current branch
            ret = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
            self.git_branch = ret.stdout.strip()
        else:
            # Error in calling `git`
            self.git_commit = ""
            self.git_tag = ""
            self.git_branch = ""

        # Get output file name
        self.output_file_name = ""
        if "-o" in sys.argv:
            self.output_file_name = sys.argv[sys.argv.index('-o') + 1]

        print(f"Current git commit: {self.git_commit}")
        print(f"Current git branch: {self.git_branch}")
        print(f"Current git tag:    {self.git_tag}")
        print(f"Output file name:   {self.output_file_name}")
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        ########################### Above is math, below is GGD ###########################

        materials.define_materials(geom)

        noRotate       = geom.structure.Rotation( 'noRotate',      '0deg',  '0deg',  '0deg'  )
        r90aboutX      = geom.structure.Rotation( 'r90aboutX',      '90deg',  '0deg',  '0deg'  )
        rminus90aboutX = geom.structure.Rotation( 'rminus90aboutX', '-90deg', '0deg',  '0deg'  )
        r90aboutY      = geom.structure.Rotation( 'r90aboutY',      '0deg',   '90deg', '0deg'  )
        r180aboutY     = geom.structure.Rotation( 'r180aboutY',     '0deg',   '180deg','0deg'  )
        r180aboutZ     = geom.structure.Rotation( 'r180aboutZ',     '0deg', '0deg',     '180deg')
        rminus90aboutY = geom.structure.Rotation( 'rminus90aboutY', '0deg', '-90deg',  '0deg'  )
        r90aboutZ      = geom.structure.Rotation( 'r90aboutZ',      '0deg',   '0deg',  '90deg' )
        r90aboutXZ     = geom.structure.Rotation( 'r90aboutXZ', '90deg',  '0deg', '90deg'  )
        r90aboutYZ     = geom.structure.Rotation( 'r90aboutYZ', '0deg',  '90deg', '90deg'  )
        r90aboutXminusZ     = geom.structure.Rotation( 'r90aboutXminusZ', '-90deg',  '0deg', '90deg'  )
        r90aboutYminusZ     = geom.structure.Rotation( 'r90aboutYminusZ', '0deg',  '-90deg', '90deg'  )
        r90aboutX90aboutY = geom.structure.Rotation( 'r90aboutX90aboutY', '90deg', '90deg', '0deg')
        r90aboutX180aboutY = geom.structure.Rotation( 'r90aboutX180aboutY', '90deg', '180deg', '0deg')

        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        self.add_volume(main_lv)

        # get Detector Enclosure and its logic volume
        de_sb = self.get_builder()
        de_lv = de_sb.get_volume()

        #changed DetEncPosition to RockPosition
        postemp = [Q('0m'),Q('0m'),Q('0m')]
        if self.RockPosition!=None:
            postemp=self.RockPosition
        Rock_pos = geom.structure.Position(de_lv.name+'_pos', postemp[0], postemp[1], postemp[2])
        rot=[Q("0deg"),Q("0deg"),Q("0deg")]
        if self.RockRotation!=None:
            rot=self.RockRotation
        Rock_rot = geom.structure.Rotation(de_lv.name+'_rot', rot[0], rot[1], rot[2])
        Rock_pla = geom.structure.Placement(de_lv.name+'_pla', volume=de_lv, pos=Rock_pos,rot=Rock_rot)
        main_lv.placements.append(Rock_pla.name)

        # Add metadata
        main_lv.params.append(("git_commit", self.git_commit))
        main_lv.params.append(("git_branch", self.git_branch))
        main_lv.params.append(("git_tag", self.git_tag))
        main_lv.params.append(("output_file_name", self.output_file_name))
