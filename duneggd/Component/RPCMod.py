#!/usr/bin/env python
'''
Subbuilder of RPCTray*Builder
'''

import gegede.builder
from gegede import Quantity as Q

class RPCModBuilder(gegede.builder.Builder):
    '''
    Build the RPC modules, the effective unit of the MuID, 
    constituting an X and Y plane of RPC strips 
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  compResiplateDim = None, 
                  compStripxDim  = None,
                  compStripyDim  = None,
                  compRpcModDim  = None,
                  compGas_gap    = None,
		  compRotPlaneOdd = None,
		  compRotPlaneEven= None,
                   **kwds):
         self.resiplateDim  = compResiplateDim 
         self.stripxDim      = compStripxDim  
         self.stripyDim      = compStripyDim  
         self.rpcModDim      = compRpcModDim  
         self.gas_gap        = compGas_gap
         self.rotateOdd      = compRotPlaneOdd
         self.rotateEven     = compRotPlaneEven
         self.rpcBldr   = self.get_builder('RPCPad')
         return


    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        rpcMod_lv = self.rpcBldr.get_volume('volRPCPad')
        self.add_volume(rpcMod_lv)

        rpcStripx_lv = self.rpcBldr.get_volume('volRPCStripx')
        rpcStripy_lv = self.rpcBldr.get_volume('volRPCStripy')
        resiplate_lv = self.rpcBldr.get_volume('volResistivePlate')

        # total nu of X and Y strips
        nXStrips = int(self.resiplateDim[0]/self.stripxDim[0])
        nYStrips = int(self.resiplateDim[1]/self.stripyDim[1])

        print(( 'RPCModBuilder: '+ str(nXStrips) +' X-Strips per RPC '))
        print(( 'RPCModBuilder: '+ str(nYStrips) +' Y-Strips per RPC '))

        # for loop to position and place X strips in RPCMod
        for i in range(nXStrips):

            xpos  = -0.5*self.resiplateDim[0]+(i+0.5)*self.stripxDim[0]
            ypos  = '0cm'
            zpos  = 0.5*self.rpcModDim[2]-0.5*self.stripxDim[2]
            
            xS_in_m  = geom.structure.Position( 'XStrip-'+str(i)+'_in_'+self.name,
                                                xpos,  ypos,  zpos)
            pxS_in_m = geom.structure.Placement( 'placeXStrip-'+str(i)+'_in_'+self.name,
                                                 volume = rpcStripx_lv,pos = xS_in_m, rot = self.rotateEven) #,rot = "r90aboutX" )
            rpcMod_lv.placements.append( pxS_in_m.name )
            #print( str(i)+' x-strip pos: '+str(xpos)+str(ypos)+str(zpos))


        # for loop to position and place Y strips in RPCMod
        for j in range(nYStrips):

            xpos  = '0cm'
            ypos  = -0.5*self.resiplateDim[1]+(j+0.5)*self.stripyDim[1]
            zpos  = -0.5*self.rpcModDim[2]+0.5*self.stripyDim[2]
            yS_in_m  = geom.structure.Position( 'YStrip-'+str(j)+'_in_'+self.name,
                                                xpos,  ypos,  zpos)
            pyS_in_m = geom.structure.Placement( 'placeYStrip-'+str(j)+'_in_'+self.name,
                                                 volume = rpcStripy_lv,pos = yS_in_m, rot = self.rotateEven )#,rot = "r90aboutX")
            rpcMod_lv.placements.append( pyS_in_m.name )
            #print( str(j)+' y-strip pos: '+str(xpos)+str(ypos)+str(zpos))


        for k in range(2):

            xpos = '0cm'
            ypos = '0cm'
            zpos = -(0.5*self.gas_gap+0.5*self.resiplateDim[2])
            if (k==1):
                    zpos = -zpos
            RP_in_m  = geom.structure.Position( 'RP-'+str(k)+'_in_'+self.name,
                                                xpos,  ypos,  zpos)
            pRP_in_m = geom.structure.Placement( 'placeRP-'+str(k)+'_in_'+self.name,
                                                 volume = resiplate_lv,pos = RP_in_m)
            rpcMod_lv.placements.append( pRP_in_m.name )


        return
