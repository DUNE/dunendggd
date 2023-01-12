#!/usr/bin/env python

import gegede.builder
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q

class test_3DSTBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, rpcModDim=None, resiplateDim=None, gas_gap=None, magOutDim=None,
                        magInDim=None, magOutDimB=None, magInDimB=None, tpcDim=None,  
                        cubeDim=None, nRPCLayer=None, nCubeX=None, nCubeY=None, nCubeZ=None, 
                        nScinLayer=None, ecalModDim=None,  stripxDim=None, stripyDim=None,
                        radiatorDim=None, rpcPos=None, ecalPos=None, magPos=None, tpcPos=None, a3dstPos=None, 
                        nScinBar=None,
                        rpcModMat=None, resiplateMat=None, gasMat=None, MagMat=None, MagMatB=None, 
                        tpcMat=None, ScinMat=None, ecalScinMat=None, radiatorMat=None, fullDetDim=None,
                        **kwds):

        self.fullDetDim = fullDetDim
        self.rpcModDim  =   rpcModDim
        self.resiplateDim = resiplateDim
        self.gas_gap = gas_gap
        self.magOutDim = magOutDim
        self.magInDim = magInDim
        self.magOutDimB = magOutDimB
        self.magInDimB = magInDimB
        self.tpcDim = tpcDim
        self.cubeDim = cubeDim

        self.nRPCLayer = nRPCLayer
        self.nCubeX = nCubeX
        self.nCubeY = nCubeY
        self.nCubeZ = nCubeZ
        self.nScinLayer = nScinLayer
        self.ecalModDim = ecalModDim
        self.stripxDim = stripxDim
        self.stripyDim = stripyDim
        self.radiatorDim = radiatorDim
        self.nScinBar = nScinBar

        self.rpcPos = rpcPos
        self.ecalPos = ecalPos
        self.magPos = magPos
        self.tpcPos = tpcPos
        self.a3dstPos = a3dstPos

        self.rpcModMat = rpcModMat
        self.resiplateMat = resiplateMat
        self.gasMat = gasMat
        self.MagMat = MagMat
        self.MagMatB = MagMatB
        self.tpcMat = tpcMat
        self.ScinMat = ScinMat
        self.ecalScinMat = ecalScinMat
        self.radiatorMat = radiatorMat

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        ########## logv volume of rpc
        # define box and volume for whole RPCMod,
        # to be retrieved by RPCTray*Builder

        full3dstBox = geom.shapes.Box('fullDetBox',
                                  dx = 0.5*self.fullDetDim[0],
                                  dy = 0.5*self.fullDetDim[1],
                                  dz = 0.5*self.fullDetDim[2])

        full3dst_lv = geom.structure.Volume('volMainDet', material='Air', shape=full3dstBox)
        self.add_volume(full3dst_lv)

        rpcPos = self.rpcPos
        magPos = self.magPos
        ecalPos = self.ecalPos
        a3dstPos = self.a3dstPos
        tpcPos = self.tpcPos

        self.getRPC(full3dst_lv, geom)
        #self.getMagnet(full3dst_lv, magPos, geom)
        self.getTPC(full3dst_lv, tpcPos, geom)
        self.getA3dst(full3dst_lv, a3dstPos, geom)
        self.getEcal(full3dst_lv, ecalPos, geom)


        ##########################################
        ############ test area
        ##########################################



        ##########################################
        ############ test done
        ##########################################


        return


    def getRPC(self, full3dst_lv, geom):

        print('RPC location')
        print((self.rpcPos[0])) 
        print((self.rpcPos[1])) 
        print((self.rpcPos[2]))

        rpcModBox = geom.shapes.Box('rpcModBox', #Q('1m'), Q('1m'),Q('1m'))
                                    dx=0.5*self.rpcModDim[0], 
                                    dy=0.5*self.rpcModDim[1], 
                                    dz=0.5*self.rpcModDim[2])
        rpcMod_lv = geom.structure.Volume('volRPC', material=self.rpcModMat, shape=rpcModBox)
        
        # define box and volume for resistive plate (maybe the same volume for anode and cathode?)
        resiplate = geom.shapes.Box( 'ResistivePlate',
                                     dx=0.5*self.resiplateDim[0],
                                     dy=0.5*self.resiplateDim[1],
                                     dz=0.5*self.resiplateDim[2])
        resiplate_lv = geom.structure.Volume('volResistivePlate', material=self.resiplateMat, shape=resiplate)

        # define box and volume for gas in rpc
        rpcGas = geom.shapes.Box( 'RPCGas',
                                  dx = 0.5*self.resiplateDim[0],
                                  dy = 0.5*self.resiplateDim[1],
                                  dz = 0.5*self.gas_gap)
        rpcGas_lv = geom.structure.Volume('volRPCGas', material=self.gasMat, shape=rpcGas)

        #pG_in_Module  = geom.structure.Placement( 'placeG_in_'+self.name, volume = rpcGas_lv )
        #rpcMod_lv.placements.append( pG_in_Module.name )

        nLayers = self.nRPCLayer

        for i in range(nLayers):

            xpos  = '0cm'
            ypos  = '0cm'
            zpos  = -0.5*self.rpcModDim[2]+i*self.resiplateDim[2]+i*self.gas_gap+0.5*self.resiplateDim[2]

            xS_in_m  = geom.structure.Position( 'rpcxpos-'+str(i),
                                               xpos,  ypos,  zpos)
            pxS_in_m = geom.structure.Placement( 'placeRPC-'+str(i),
                                               volume = resiplate_lv,pos = xS_in_m) #,rot = "r90aboutX" )
            rpcMod_lv.placements.append( pxS_in_m.name )

            xpos2  = '0cm'
            ypos2  = '0cm'
            zpos2  = -0.5*self.rpcModDim[2]+i*self.resiplateDim[2]+i*self.gas_gap+self.resiplateDim[2]+0.5*self.gas_gap

            xS_in_m2  = geom.structure.Position( 'rpcxpos2-'+str(i),
                                               xpos2,  ypos2,  zpos2)
            pxS_in_m2 = geom.structure.Placement( 'placeRPC2-'+str(i),
                                               volume = rpcGas_lv,pos = xS_in_m2) #,rot = "r90aboutX" )
            rpcMod_lv.placements.append( pxS_in_m2.name )

        #self.add_volume(rpcMod_lv)

        ################################################

        rpcPosition = geom.structure.Position('rpc-Pos', Q('0m'), Q('0m'),Q('3.7m'))
        placeRpc = geom.structure.Placement('placeRpcName', volume = rpcMod_lv, pos=rpcPosition)
        full3dst_lv.placements.append( placeRpc.name )
      
        # now the inner part size is 9m x 7m x 7m

        r90aboutXY      = geom.structure.Rotation( 'r90aboutXYagain',      '90deg',  '90deg',  '0deg'  )

        rpcPosition2 = geom.structure.Position('rpc-Pos2', Q('0m'), Q('3.7m'),Q('0m'))
        placeRpcUp = geom.structure.Placement('placeRpcName2', volume = rpcMod_lv, pos=rpcPosition2, rot = "r90aboutX")
        full3dst_lv.placements.append( placeRpcUp.name )

        rpcPosition3 = geom.structure.Position('rpc-Pos3', Q('0m'), Q('-3.7m'),Q('0m'))
        placeRpcDn = geom.structure.Placement('placeRpcName3', volume = rpcMod_lv, pos=rpcPosition3, rot = "r90aboutX")
        full3dst_lv.placements.append( placeRpcDn.name )

        rpcPosition4 = geom.structure.Position('rpc-Pos4', Q('3.7m'), Q('0m'),Q('0m'))
        placeRpcLf = geom.structure.Placement('placeRpcName4', volume = rpcMod_lv, pos=rpcPosition4, rot = "r90aboutXYagain")
        full3dst_lv.placements.append( placeRpcLf.name )

        rpcPosition5 = geom.structure.Position('rpc-Pos5', Q('-3.7m'), Q('0m'),Q('0m'))
        placeRpcRt = geom.structure.Placement('placeRpcName5', volume = rpcMod_lv, pos=rpcPosition5, rot = "r90aboutXYagain")
        full3dst_lv.placements.append( placeRpcRt.name )
        

        ################################################

        ############
        ############block of magnet
        ############
        ############
        ############
        ############
    def getMagnet(self, full3dst_lv, magPos, geom):

        print('magnet location')
        print((magPos[0]))
        print((magPos[1]))
        print((magPos[2]))

        magOut = geom.shapes.Box( 'MagOut',                 dx=0.5*self.magOutDim[0],
                                  dy=0.5*self.magOutDim[1], dz=0.5*self.magOutDim[2])
        magIn = geom.shapes.Box(  'MagInner',               dx=0.5*self.magInDim[0],
                                  dy=0.5*self.magInDim[1],  dz=0.5*self.magInDim[2])

        magBox = geom.shapes.Boolean( 'Magnet', type='subtraction', first=magOut, second=magIn )
        Mag_lv = geom.structure.Volume('volMagnet', material=self.MagMat, shape=magBox)

        magOutB = geom.shapes.Box( 'YokeOut',                 dx=0.5*self.magOutDimB[0],
                                  dy=0.5*self.magOutDimB[1], dz=0.5*self.magOutDimB[2])
        magInB = geom.shapes.Box(  'YokeInner',               dx=0.5*self.magInDimB[0],
                                  dy=0.5*self.magInDimB[1],  dz=0.5*self.magInDimB[2])

        magBoxB = geom.shapes.Boolean( 'Yoke', type='subtraction', first=magOutB, second=magInB )
        MagBlock_lv = geom.structure.Volume('volYoke', material=self.MagMatB, shape=magBoxB)

        ################################################
        magPosition = geom.structure.Position('magPosition', magPos[0], magPos[1], magPos[2])
        placeMag = geom.structure.Placement('placeMagName', volume = Mag_lv, pos=magPosition)
        full3dst_lv.placements.append( placeMag.name )

        ################################################

        #self.add_volume(Mag_lv)
        #self.add_volume(MagBlock_lv)

        ############
        ############block of gas TPC
        ############
        ############
        ############
        ############

    def getTPC(self, full3dst_lv, tpcPos, geom):

        print('location of TPC')
        print((self.tpcPos[0]))
        print((self.tpcPos[1]))
        print((self.tpcPos[2]))

        tpcBox = geom.shapes.Box( 'tpc',                 dx=0.5*self.tpcDim[0],
                              dy=0.5*self.tpcDim[1], dz=0.5*self.tpcDim[2])

        tpc_lv = geom.structure.Volume('volTPC', material=self.tpcMat, shape=tpcBox)

        ################################
        tpcPosition = geom.structure.Position('tpcPosition', Q('0m'), Q('0m'),Q('1.5m'))
        placeTpc = geom.structure.Placement('placeTpcName', volume = tpc_lv, pos=tpcPosition)
        full3dst_lv.placements.append( placeTpc.name )

        tpcBoxTop = geom.shapes.Box( 'tpcTop',                 dx=0.5*Q('4m'),
                              dy=0.5*Q('2m'), dz=0.5*Q('1m'))
        tpcTop_lv = geom.structure.Volume('volTPCTop', material=self.tpcMat, shape=tpcBoxTop)
        tpcPositionTop = geom.structure.Position('tpcTopPosition', Q('0m'), Q('1.5m'),Q('0m'))
        placeTpcTop = geom.structure.Placement('placeTpcTopName', volume = tpcTop_lv, pos=tpcPositionTop, rot="r90aboutX")
        full3dst_lv.placements.append( placeTpcTop.name )

        tpcPositionBot = geom.structure.Position('tpcBotPosition',  Q('0m'), Q('-1.5m'),Q('0m'))
        placeTpcBot = geom.structure.Placement('placeTpcBotName', volume = tpcTop_lv, pos=tpcPositionBot, rot="r90aboutX")
        full3dst_lv.placements.append( placeTpcBot.name )
        '''
        tpcBoxLf = geom.shapes.Box( 'tpcLf',                 dx=0.5*Q('2m'),
                              dy=0.5*Q('2m'), dz=0.5*Q('1m'))
        tpcLf_lv = geom.structure.Volume('volTPCLf', material=self.tpcMat, shape=tpcBoxLf)
        tpcPositionLf = geom.structure.Position('tpcPositionLfi', Q('2.5m'), Q('0m'),Q('0m'))
        placeTpcLf = geom.structure.Placement('placeTpcLfName', volume = tpcLf_lv, pos=tpcPositionLf, rot="r90aboutY")
        full3dst_lv.placements.append( placeTpcLf.name )

        tpcPositionRt = geom.structure.Position('tpcPositionRt', Q('-2.5m'), Q('0m'),Q('0m'))
        placeTpcRt = geom.structure.Placement('placeTpcRtName', volume = tpcLf_lv, pos=tpcPositionRt, rot="r90aboutY")
        full3dst_lv.placements.append( placeTpcRt.name )
        '''
        ################################

        #self.add_volume(tpc_lv)

        ############
        ############block of scintillator cubes
        ############
        ############
        ############
        ############

    def getA3dst(self, full3dst_lv, a3dstPos, geom):

        print('location of 3DST')
        print((a3dstPos[0]))
        print((a3dstPos[1]))
        print((a3dstPos[2]))

        nCubeX = self.nCubeX
        nCubeY = self.nCubeY
        nCubeZ = self.nCubeZ

        scinBox = geom.shapes.Box( 'scin',                 dx=0.5*self.cubeDim[0],
                              dy=0.5*self.cubeDim[1], dz=0.5*self.cubeDim[2])
        scin_lv = geom.structure.Volume('volcube', material=self.ScinMat, shape=scinBox)

        a3dstBox = geom.shapes.Box( '3dst',                 dx=0.5*self.cubeDim[0]*nCubeX,
                              dy=0.5*self.cubeDim[1]*nCubeY, dz=0.5*self.cubeDim[2]*nCubeZ)
        a3dst_lv = geom.structure.Volume('vol3DST', material='Air', shape=a3dstBox)

        for i in range(nCubeX):

            for j in range(nCubeY):

                for k in range(nCubeZ):
                    xposCube=-0.5*nCubeX*self.cubeDim[0] +i*self.cubeDim[0]+0.5*self.cubeDim[0]
                    yposCube=-0.5*nCubeY*self.cubeDim[1] +j*self.cubeDim[1]+0.5*self.cubeDim[1]
                    zposCube=-0.5*nCubeZ*self.cubeDim[2] +k*self.cubeDim[2]+0.5*self.cubeDim[2]

                    scinPos = geom.structure.Position('scinpos-'+str(i)+'_'+str(j)+'_'+str(k),
                                                        xposCube,
                                                        yposCube,
                                                        zposCube)
                    placeScin = geom.structure.Placement( 'a3dst-'+str(i)+'_'+str(j)+'_'+str(k),
                                                       volume = scin_lv,pos = scinPos) #,rot = "r90aboutX" )
                    a3dst_lv.placements.append( placeScin.name )

        #########################################
        a3dstPosition = geom.structure.Position('a3dstPosition', a3dstPos[0], a3dstPos[1], a3dstPos[2])
        placeA3dst = geom.structure.Placement('placeA3dstName', volume = a3dst_lv, pos=a3dstPosition)
        full3dst_lv.placements.append( placeA3dst.name )
        #########################################


        #self.add_volume(a3dst_lv)

        ############
        ############block of ecal
        ############
        ############
        ############
        ############
    def getEcal(self, full3dst_lv, ecalPos, geom):

        print('location of ECAL')
        print((ecalPos[0]))
        print((ecalPos[1]))
        print((ecalPos[2]))

        ecalMod = geom.shapes.Box( 'ecalBox',
                                  dx = 0.5*self.ecalModDim[0],
                                  dy = 0.5*self.ecalModDim[1],
                                  dz = 0.5*self.ecalModDim[2])
        ecalMod_lv = geom.structure.Volume('volEcal', material=self.ecalScinMat, shape=ecalMod)

        ecalStripx = geom.shapes.Box( 'ecalStripx',
                                    dx = 0.5*self.stripxDim[0],
                                    dy = 0.5*self.stripxDim[1],
                                    dz = 0.5*self.stripxDim[2])
        ecalStripx_lv = geom.structure.Volume('volECALStripx', material=self.ecalScinMat, shape=ecalStripx)

        ecalStripy = geom.shapes.Box( 'ecalStripy',
                                    dx = 0.5*self.stripyDim[0],
                                    dy = 0.5*self.stripyDim[1],
                                    dz = 0.5*self.stripyDim[2])
        ecalStripy_lv = geom.structure.Volume('volECALStripy', material=self.ecalScinMat, shape=ecalStripy)

        ecalRadiator = geom.shapes.Box( 'ecalRadiator',
                                     dx = 0.5*self.radiatorDim[0],
                                     dy = 0.5*self.radiatorDim[1],
                                     dz = 0.5*self.radiatorDim[2])
        radiator_lv = geom.structure.Volume('volRadiatorPlate', material=self.radiatorMat, shape=ecalRadiator)

        nScins = self.nScinLayer
        nBars  = self.nScinBar

        for i in range(nScins):

            for j in range(nBars):
                xposx  = -0.5*self.ecalModDim[0]+(j+0.5)*self.stripxDim[0]
                yposx  = '0cm'
                zposx  = -0.5*self.ecalModDim[2]+i*self.radiatorDim[2]+i*self.stripxDim[2]+i*self.stripyDim[2]+0.5*self.stripxDim[2]

                ecalModPos = geom.structure.Position('ECALPos'+str(i)+'_'+str(j), xposx, yposx, zposx)
                ecal = geom.structure.Placement('placeEcal'+str(i)+'_'+str(j), volume=ecalStripx_lv,
                                               pos=ecalModPos)
                ecalMod_lv.placements.append(ecal.name)

                xposy  = '0cm'
                yposy  = -0.5*self.ecalModDim[1]+(j+0.5)*self.stripyDim[1]
                zposy  = -0.5*self.ecalModDim[2]+i*self.radiatorDim[2]+i*self.stripxDim[2]+i*self.stripyDim[2]+self.stripxDim[2]+0.5*self.stripyDim[2]

                ecalModPos2 = geom.structure.Position('ECALPos2'+str(i)+'_'+str(j), xposy, yposy, zposy)
                ecal2 = geom.structure.Placement('placeEcal2'+str(i)+'_'+str(j), volume=ecalStripy_lv,
                                                pos=ecalModPos2)
                ecalMod_lv.placements.append(ecal2.name)

            xposr  = '0cm'
            yposr  = '0cm'
            zposr  = -0.5*self.ecalModDim[2]+i*self.radiatorDim[2]+i*self.stripxDim[2]+i*self.stripyDim[2]+self.stripxDim[2]+self.stripyDim[2]+0.5*self.radiatorDim[2]

            ecalModPos3 = geom.structure.Position('ECALPos3'+str(i)+'_'+str(j), xposr, yposr, zposr)
            ecal3 = geom.structure.Placement('placeEcal3'+str(i), volume=radiator_lv,
                                             pos=ecalModPos3)
            ecalMod_lv.placements.append(ecal3.name)

        ################################################
        ecalPosition = geom.structure.Position('ecalPosition', Q('0m'), Q('0m'),Q('2.5m'))
        placeEcal = geom.structure.Placement('placeEcalName', volume = ecalMod_lv, pos=ecalPosition)
        full3dst_lv.placements.append( placeEcal.name )

        # so far, inner box is 6m x 4m x 3m, the end eCAL size is 6m x 4m x 1m
        ecalPositionTop = geom.structure.Position('ecalTopPosition', Q('0m'), Q('2.5m'),Q('0m'))
        placeEcalTop = geom.structure.Placement('placeEcalTopName', volume = ecalMod_lv, pos=ecalPositionTop, rot="r90aboutX")
        full3dst_lv.placements.append( placeEcalTop.name )

        ecalPositionBot = geom.structure.Position('ecalBotPosition',  Q('0m'), Q('-2.5m'),Q('0m'))
        placeEcalBot = geom.structure.Placement('placeEcalBotName', volume = ecalMod_lv, pos=ecalPositionBot, rot="r90aboutX")
        full3dst_lv.placements.append( placeEcalBot.name )

        r90aboutXY      = geom.structure.Rotation( 'r90aboutXY',      '90deg',  '90deg',  '0deg'  )

        ecalPositionLf = geom.structure.Position('ecalPositionLfi', Q('2.5m'), Q('0m'),Q('0m'))
        placeEcalLf = geom.structure.Placement('placeEcalLfName', volume = ecalMod_lv, pos=ecalPositionLf, rot="r90aboutXY")
        full3dst_lv.placements.append( placeEcalLf.name )

        ecalPositionRt = geom.structure.Position('ecalPiositionRt', Q('-2.5m'), Q('0m'),Q('0m'))
        placeEcalRt = geom.structure.Placement('placeEcalRtName', volume = ecalMod_lv, pos=ecalPositionRt, rot="r90aboutXY")
        full3dst_lv.placements.append( placeEcalRt.name )


        ################################################

        #self.add_volume(ecalMod_lv)

        #rpc_lv = self.MagnetBldr.get_volume('volRPC')
        #mag_lv = self.MagnetBldr.get_volume('volMagnet')
        #ecal_lv = self.MagnetBldr.get_volume('volEcal')
        #a3dst_lv = self.MagnetBldr.get_volume('vol3DST')
        #tpc_lv = self.MagnetBldr.get_volume('volTPC')
        
        #placeRpc = geom.structure.Placement('placeRpcName',
        #                                     volume=rpcMod_lv, 
        #                                     pos=rpcPos)
        #placeMag = geom.structure.Placement('placeMagName', volume = Mag_lv, pos=magPos)
        #placeEcal = geom.structure.Placement('placeEcalName', volume = ecalMod_lv, pos=ecalPos)
        #placeA3dst = geom.structure.Placement('placeA3dstName', volume = a3dst_lv, pos=a3dstPos)
        #placeTpc = geom.structure.Placement('placeTpcName', volume = tpc_lv, pos=tpcPos)
        #print placeRpc.name

        #det_lv.placements.append(placeRpc.name)                 
        #det_lv.placements.append( placeMag.name )
        #det_lv.placements.append( placeEcal )
        #det_lv.placements.append( placeA3dst )
        #det_lv.placements.append( placeTpc.name )
        
        #return
