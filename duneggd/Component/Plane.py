#!/usr/bin/env python
'''
Subbuilder of ECALBuilder
'''

import gegede.builder
from gegede import Quantity as Q
import math

class SBPlaneBuilder(gegede.builder.Builder):
 
    # define builder data here
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, compDimension = None,
                        compSBPlaneMat = None,
			compNElements = None,
                        compScintBarMat = None, compRotation = None,
                  specificName="",**kwds):
        self.SBPlaneMat  = compSBPlaneMat         
        self.ScintBarMat = compScintBarMat        
        self.ScintBarDim = compDimension        
        self.nScintBars  = compNElements       
        self.compRotation  = compRotation         
        self.specificName = specificName

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # Call the scint bar shape and volume
        SBPlaneBldr = self.get_builder()
        ScintBar_lv = SBPlaneBldr.get_volume()

        # define material in World Builder
        # Make the scint bar plane, used for both orientations

        self.SBPlaneDim = [ self.ScintBarDim[0] * self.nScintBars, self.ScintBarDim[1], self.ScintBarDim[2] ]
        SBPlaneBox = geom.shapes.Box( 'SBPlaneBox'+self.specificName,              dx=0.5*self.SBPlaneDim[0], 
                                      dy=0.5*self.SBPlaneDim[1], dz=0.5*self.SBPlaneDim[2])
        SBPlane_lv = geom.structure.Volume('volSBPlane'+self.specificName, material=self.SBPlaneMat, shape=SBPlaneBox)
        self.add_volume(SBPlane_lv)
        # make default material glue -- search 'epoxy' in gdmlMaterials.py
	# This volume will be retrieved by ECAL*Builder


        # Place the bars in the plane
        nScintBarsPerPlane = int(math.floor((self.SBPlaneDim[0]/self.ScintBarDim[0])))
        if self.nScintBars != nScintBarsPerPlane:
           print(( 'SBPlaneBuilder: making'+str(nScintBarsPerPlane)+' scintillator bars per plane, should be '+str(self.nScintBars)))
  
        for i in range(nScintBarsPerPlane):
            xpos = -0.5*self.SBPlaneDim[0] + (i+0.5)*self.ScintBarDim[0]
            sb_in_sp      = geom.structure.Position( 'SB-'+str(i)+'_in_'+self.name, 
                                                     xpos, '0cm', '0cm')
            psb_in_sp     = geom.structure.Placement( 'placeSB-'+str(i)+'_in_'+self.name, 
                                                      volume = ScintBar_lv, pos = sb_in_sp, rot = self.compRotation)
            SBPlane_lv.placements.append(psb_in_sp.name)

        return
