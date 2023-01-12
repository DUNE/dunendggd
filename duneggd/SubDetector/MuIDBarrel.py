#!/usr/bin/env python
'''
Subbuilder of Detector
'''

import gegede.builder
import math
from gegede import Quantity as Q


class MuIDBarrelBuilder(gegede.builder.Builder):
    '''
    Assemble configured number of RPC trays
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
                  modMuidPos = [Q('0cm'),Q('0cm'),Q('0cm')], 
                  modMuidDim = None,
                  modSteelPlateDim = None, 
                  modNTraysPerPlane = None, 
                  modNPlanes = None,
                  modMuidRot = None, nMuTracker = None,
                  modMuidMat = 'Steel', **kwds):

        self.muidAbsPos     = modMuidPos
        self.muidMat        = modMuidMat 
        self.muidDim        = modMuidDim 
        self.steelPlateDim  = modSteelPlateDim 
        self.nTraysPerPlane = modNTraysPerPlane 
        self.nPlanes        = modNPlanes 
        self.muidRot        = modMuidRot 
        self.nMuTracker     = nMuTracker
        
        #print( self.builders)
        self.RPCTrayBldr = self.get_builder('RPCTray_End')
	return

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # Get the RPC tray volume and position
        rpcTray_lv = self.RPCTrayBldr.get_volume('volRPCTray_End')
        rpcTrayDim = self.RPCTrayBldr.rpcTrayDim
        
        # Calculate the muidDim[2] (z dim) with other configured parameters: 
        #   number of planes, thicknesses...


        # Make volume to be retrieved by DetectorBuilder
        muidBox = geom.shapes.Box( self.name,
                                   dx=0.5*self.muidDim[0],
                                   dy=0.5*self.muidDim[1],
                                   dz=0.5*self.muidDim[2])
        muid_lv = geom.structure.Volume('vol'+self.name, material=self.muidMat, shape=muidBox)
        self.add_volume(muid_lv)

        # Place the RPC trays and steel sheets between in the configured way
        # Steel Sheets: just leave the default material of volMuID* steel 
        #   and leave spaces instead of placing explicit volumes
	
        print(( 'Abs pos for '+ str(self.name) +' along Z: '+ str(self.muidAbsPos[2])))
        print(( math.cos(math.radians(60))))
        EachAngle = int(360/self.nMuTracker)

 	#EachAngle = 0
	for ii in range(self.nMuTracker):
		Zrot         = Q('0deg')+EachAngle*ii*Q('1deg')
		print(( 'rotating angle of '+str(ii)+' muon tracker: '+str(Zrot)))
		#rAboutXZ     = geom.structure.Rotation( 'rAboutXZ'+str(ii), '0deg',  '0deg', -Zrot+Q('90deg')  )	
		rAboutXZ     = geom.structure.Rotation( 'rAboutXZ'+str(ii),  Zrot-Q('0deg') , '0deg', '0deg'  )

        for i in range(self.nPlanes):
            #xpos = self.muidDim[1]*math.cos(Zrot)
            #ypos = self.muidDim[1]*math.sin(Zrot)	
            #zpos = self.muidDim[2] + self.muidAbsPos[2]
            xpos = self.muidDim[0] + self.muidAbsPos[0]
            ypos = self.muidDim[1]*math.sin(Zrot) + self.muidAbsPos[1]
            zpos = self.muidDim[1]*math.cos(Zrot) + self.muidAbsPos[2]
            print(( 'position of tracker: '+str(xpos)+' '+str(ypos)+' '+str(zpos)))

            for j in range(self.nTraysPerPlane):
                #xpos = -0.5*self.muidDim[0]+self.muidAbsPos[0]
        		#ypos = -0.5*self.muidDim[1]+self.muidAbsPos[1]
        		rpct_in_muid  = geom.structure.Position( 'rpct-'+str(self.nTraysPerPlane*i+j)+'_in_'+self.name+'_'+str(ii),
                		                                 xpos,  ypos,  zpos)
        		prpct_in_muid = geom.structure.Placement( 'prpct-'+str(self.nTraysPerPlane*i+j)+'_in_'+self.name+'_'+str(ii),
                		                                  volume = rpcTray_lv, pos = rpct_in_muid, rot='rAboutXZ'+str(ii) )
        		muid_lv.placements.append( prpct_in_muid.name )
         
        return
