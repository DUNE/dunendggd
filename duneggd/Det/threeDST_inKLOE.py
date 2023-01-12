#!/usr/bin/env python

import gegede.builder
#from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q

class threeDST_inKLOE_Builder(gegede.builder.Builder):

    def configure(self, threeDSTboxDim=None,
                  cubeDim=None, nCubeX=None, nCubeY=None, nCubeZ=None, nScinLayer=None, ecalModDim = None, stripxDim = None, stripyDim = None, radiatorDim = None, ecalModDimTop=None, stripxDimTop=None, stripyDimTop=None, radiatorDimTop=None, nScinBar = None, ecalPos=None, ecalPosTop=None, ecalPosBot=None, ecalScinMat=None, radiatorMat=None, a3dstPos=None, ScinMat=None, tpcDim=None, tpcTopDim=None, tpcPos=None, tpcTopPos=None, tpcBotDim=None, tpcBotPos=None, tpcMat=None, magOutDim=None, magInDim=None, magPos=None, magMat=None, fullDetDim=None, rpcModDim=None, resistplateDim=None, gas_gap=None, nRPCLayer=None, rpcModMat=None, gasMat=None, resistplateMat=None, rpcPos=None, cylinderDim=None, cylinderMat=None, cylinderPos=None, **kwds):

        self.threeDSTboxDim=threeDSTboxDim
        self.fullDetDim = fullDetDim
        self.tpcDim = tpcDim
        self.tpcTopDim = tpcTopDim
        self.tpcBotDim = tpcBotDim
        
        self.cubeDim = cubeDim
        self.nCubeX = nCubeX
        self.nCubeY = nCubeY
        self.nCubeZ = nCubeZ
        self.nScinLayer = nScinLayer
        self.ecalModDim = ecalModDim
        self.stripxDim = stripxDim
        self.stripyDim = stripyDim
        self.radiatorDim = radiatorDim
        self.ecalModDimTop = ecalModDimTop
        self.stripxDimTop = stripxDimTop
        self.stripyDimTop = stripyDimTop
        self.radiatorDimTop = radiatorDimTop
        self.nScinBar = nScinBar

        self.magInDim = magInDim
        self.magOutDim = magOutDim
        
        self.ScinMat = ScinMat
        self.tpcPos = tpcPos
        self.tpcTopPos = tpcTopPos
        self.tpcBotPos = tpcBotPos
        self.tpcMat = tpcMat
        self.ecalScinMat = ecalScinMat
        self.radiatorMat = radiatorMat
        self.magMat = magMat
        self.rpcModMat = rpcModMat
        self.gasMat = gasMat
        self.resistplateMat = resistplateMat

        self.a3dstPos = a3dstPos
        self.ecalPos = ecalPos
        self.ecalPosTop = ecalPosTop
        self.ecalPosBot = ecalPosBot
        self.magPos = magPos

        self.rpcModDim = rpcModDim
        self.resistplateDim = resistplateDim
        self.gas_gap = gas_gap
        self.nRPCLayer = nRPCLayer
        self.rpcPos = rpcPos

        self.cylinderDim = cylinderDim
        self.cylinderMat = cylinderMat
        self.cylinderPos = cylinderPos

    def construct(self, geom):

        ########## logv volume of rpc
        # define box and volume for whole RPCMod,
        # to be retrieved by RPCTray*Builder

#        materials.define_materials(geom)

#        noRotate       = geom.structure.Rotation( 'noRotate',      '0deg',  '0deg',  '0deg'  )
#        r90aboutX      = geom.structure.Rotation( 'r90aboutX',      '90deg',  '0deg',  '0deg'  )
#        rminus90aboutX = geom.structure.Rotation( 'rminus90aboutX', '-90deg', '0deg',  '0deg'  )
#        r90aboutY      = geom.structure.Rotation( 'r90aboutY',      '0deg',   '90deg', '0deg'  )
#        r180aboutY     = geom.structure.Rotation( 'r180aboutY',     '0deg',   '180deg','0deg'  )
#        r180aboutZ     = geom.structure.Rotation( 'r180aboutZ',     '0deg', '0deg',     '180deg')
#        rminus90aboutY = geom.structure.Rotation( 'rminus90aboutY', '0deg', '-90deg',  '0deg'  )
#        r90aboutZ      = geom.structure.Rotation( 'r90aboutZ',      '0deg',   '0deg',  '90deg' )
#        r90aboutXZ     = geom.structure.Rotation( 'r90aboutXZ', '90deg',  '0deg', '90deg'  )
#        r90aboutYZ     = geom.structure.Rotation( 'r90aboutYZ', '0deg',  '90deg', '90deg'  )
#        r90aboutXminusZ     = geom.structure.Rotation( 'r90aboutXminusZ', '-90deg',  '0deg', '90deg'  )
#        r90aboutYminusZ     = geom.structure.Rotation( 'r90aboutYminusZ', '0deg',  '-90deg', '90deg'  )

#        full3dstBox = geom.shapes.Tubs('fullDetBox', rmin=self.fullDetDim[0], rmax=self.fullDetDim[1], dz=0.5*self.fullDetDim[2], sphi=self.fullDetDim[3], dphi=self.fullDetDim[4])
        full3dstBox = geom.shapes.Box('3dstBox',dx=self.threeDSTboxDim[0]/2, dy=self.threeDSTboxDim[1]/2, dz=self.threeDSTboxDim[2]/2)

        #full3dstBox = geom.shapes.Box('fullDetBox', 
        #        dx = 0.5*self.fullDetDim[0], 
        #        dy = 0.5*self.fullDetDim[1],
        #        dz = 0.5*self.fullDetDim[2])

        full3dst_lv = geom.structure.Volume('vol_3dstBox', material='Air', shape=full3dstBox)
        self.add_volume(full3dst_lv)

        a3dstPos = self.a3dstPos
        tpcPos = self.tpcPos
        ecalPos = self.ecalPos
        magPos = self.magPos
        rpcPos = self.rpcPos
        cylinderPos = self.cylinderPos

        self.getA3dst(full3dst_lv, a3dstPos, geom)
#        self.getTPC(full3dst_lv, a3dstPos, geom)
        #self.getEcal(full3dst_lv, ecalPos, geom)
        #self.getMagnet(full3dst_lv, magPos, geom)
        #self.getRPC(full3dst_lv, rpcPos, geom)
        #self.getCylinder(full3dst_lv, cylinderPos, geom)

        return

    def getA3dst(self, full3dst_lv, a3dstPos, geom):

        nCubeX = self.nCubeX
        nCubeY = self.nCubeY
        nCubeZ = self.nCubeZ

        a3dstBox = geom.shapes.Box( '3dst',                 dx=0.5*self.cubeDim[0]*nCubeX,
                              dy=0.5*self.cubeDim[1]*nCubeY, dz=0.5*self.cubeDim[2]*nCubeZ)
        a3dst_lv = geom.structure.Volume('vol3DST', material='Air', shape=a3dstBox)

        a3dstPlane = geom.shapes.Box( '3dstplane',                 dx=0.5*self.cubeDim[0]*nCubeX,
                              dy=0.5*self.cubeDim[1]*nCubeY, dz=0.5*self.cubeDim[2])
        a3dstPlane_lv = geom.structure.Volume('vol3DSTPlane', material='Air', shape=a3dstPlane)

        a3dstBar = geom.shapes.Box( '3dstBar',                 dx=0.5*self.cubeDim[0]*nCubeX,
                              dy=0.5*self.cubeDim[1], dz=0.5*self.cubeDim[2])
        a3dstBar_lv = geom.structure.Volume('vol3DSTBar', material='Air', shape=a3dstBar)

        a3dstCube = geom.shapes.Box( '3dstCube',                 dx=0.5*self.cubeDim[0],
                              dy=0.5*self.cubeDim[1], dz=0.5*self.cubeDim[2])
        a3dstCube_lv = geom.structure.Volume('volcube', material='Scintillator', shape=a3dstCube)
        a3dstCube_lv.params.append(("SensDet", 'volCube'))

        for i in range(nCubeX):

            xposCube=-0.5*self.cubeDim[0]*nCubeX +(i+0.5)*self.cubeDim[0]
            yposCube=Q('0cm')
            zposCube=Q('0cm')

            a3dstBar_lv.placements.append( geom.structure.Placement( 'a3dstBar'+'_'+str(i),
                                               volume = a3dstCube_lv, pos = geom.structure.Position('a3dstCubevol'+'_'+str(i),
                                                xposCube,
                                                yposCube,
                                                zposCube)).name )

        for j in range(nCubeY):

            xposBar=Q('0cm')
            yposBar=-0.5*self.cubeDim[1]*nCubeY +(j+0.5)*self.cubeDim[1]
            zposBar=Q('0cm')

            a3dstPlane_lv.placements.append( geom.structure.Placement( 'a3dstPlane'+'_'+str(i)+'_'+str(j),
                                             volume = a3dstBar_lv, pos = geom.structure.Position('a3dstBarvol'+'_'+str(j),
                                             xposBar,
                                             yposBar,
                                             zposBar)).name )

        for k in range(nCubeZ):

#            print "loop the cube layer  "
#            print k
            xpos3dstPlane=Q('0m')
            ypos3dstPlane=Q('0m')
            zpos3dstPlane=-0.5*self.cubeDim[2]*nCubeZ + (k+0.5)*self.cubeDim[2]

            f3dstPos = geom.structure.Position('cube3dstpos'+'_'+str(i)+'_'+str(j)+'_'+str(k),
                                               xpos3dstPlane,
                                               ypos3dstPlane,
                                               zpos3dstPlane)
            
            place3dst = geom.structure.Placement( 'f3dst'+'_'+str(i)+'_'+str(j)+'_'+str(k),
                                                   volume = a3dstPlane_lv,pos = f3dstPos) #,rot = "r90aboutX" )
            a3dst_lv.placements.append( place3dst.name )

        #########################################
#        a3dstPosition = geom.structure.Position('a3dstPosition', a3dstPos[0], a3dstPos[1], a3dstPos[2])
        placeA3dst = geom.structure.Placement('placeA3dstName', volume = a3dst_lv , rot="r90aboutY")
        full3dst_lv.placements.append( placeA3dst.name )
        #########################################


    def getTPC(self, full3dst_lv, tpcPos, geom):

        print('location of TPC')
        print((self.tpcPos[0]))
        print((self.tpcPos[1]))
        print((self.tpcPos[2]))

        tpcBox = geom.shapes.Box('tpc', dx=0.5*self.tpcDim[0], dy=0.5*self.tpcDim[1], dz=0.5*self.tpcDim[2])

        tpc_lv = geom.structure.Volume('volTpc', material=self.tpcMat, shape=tpcBox)
        tpc_lv.params.append(("SensDet", 'voltpc'))

        tpcPosition = geom.structure.Position('tpcPosition', self.tpcPos[0], self.tpcPos[1], self.tpcPos[2])

        tpcTopBox = geom.shapes.Box('tpcTop', dx=0.5*self.tpcTopDim[0], dy=0.5*self.tpcTopDim[1], dz=0.5*self.tpcTopDim[2])
        tpcTop_lv = geom.structure.Volume('volTpcTop', material=self.tpcMat, shape=tpcTopBox)
        tpcTop_lv.params.append(("sensDet", 'voltpcTop'))
        tpcTopPosition = geom.structure.Position('tpcTopPosition', self.tpcTopPos[0], self.tpcTopPos[1], self.tpcTopPos[2])

        tpcBotBox = geom.shapes.Box('tpcBot', dx=0.5*self.tpcBotDim[0], dy=0.5*self.tpcBotDim[1], dz=0.5*self.tpcBotDim[2])
        tpcBot_lv = geom.structure.Volume('volTpcBot', material=self.tpcMat, shape=tpcBotBox)
        tpcBot_lv.params.append(("sensDet", 'voltpcBot'))
        tpcBotPosition = geom.structure.Position('tpcBotPosition', self.tpcBotPos[0], self.tpcBotPos[1], self.tpcBotPos[2])

        placeTpc = geom.structure.Placement('placeTpcName', volume = tpc_lv, pos=tpcPosition, rot="r90aboutY")
        full3dst_lv.placements.append( placeTpc.name )

        placeTpcTop = geom.structure.Placement('placeTpcTopName', volume = tpcTop_lv, pos=tpcTopPosition, rot="r90aboutY")
        full3dst_lv.placements.append ( placeTpcTop.name )

        placeTpcBot = geom.structure.Placement('placeTpcBotName', volume = tpcBot_lv, pos=tpcBotPosition, rot="r90aboutY")
        full3dst_lv.placements.append ( placeTpcBot.name )

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
        ecalStripx_lv.params.append(("SensDet", 'volecalStripx'))
         

        ecalStripy = geom.shapes.Box( 'ecalStripy',
                                    dx = 0.5*self.stripyDim[0],
                                    dy = 0.5*self.stripyDim[1],
                                    dz = 0.5*self.stripyDim[2])
        ecalStripy_lv = geom.structure.Volume('volECALStripy', material=self.ecalScinMat, shape=ecalStripy)
        ecalStripy_lv.params.append(("SensDet", 'volecalStripy'))
 

        ecalRadiator = geom.shapes.Box( 'ecalRadiator',
                                     dx = 0.5*self.radiatorDim[0],
                                     dy = 0.5*self.radiatorDim[1],
                                     dz = 0.5*self.radiatorDim[2])
        radiator_lv = geom.structure.Volume('volRadiatorPlate', material=self.radiatorMat, shape=ecalRadiator)
        radiator_lv.params.append(("SensDet", 'volradiator'))
 

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
        #ecalPosition = geom.structure.Position('ecalPosition', Q('0m'), Q('0m'),Q('2.5m'))
        ecalPosition = geom.structure.Position('ecalPosition', self.ecalPos[0], self.ecalPos[1], self.ecalPos[2])
        placeEcal = geom.structure.Placement('placeEcalName', volume = ecalMod_lv, pos=ecalPosition, rot = 'r180aboutY')
        full3dst_lv.placements.append( placeEcal.name )

#########################################################

        ecalModTop = geom.shapes.Box( 'ecalBoxTop',
                                  dx = 0.5*self.ecalModDimTop[0],
                                  dy = 0.5*self.ecalModDimTop[1],
                                  dz = 0.5*self.ecalModDimTop[2])
        ecalModTop_lv = geom.structure.Volume('volEcalTop', material=self.ecalScinMat, shape=ecalModTop)

        ecalStripxTop = geom.shapes.Box( 'ecalStripxTop',
                                    dx = 0.5*self.stripxDimTop[0],
                                    dy = 0.5*self.stripxDimTop[1],
                                    dz = 0.5*self.stripxDimTop[2])
        ecalStripxTop_lv = geom.structure.Volume('volECALStripxTop', material=self.ecalScinMat, shape=ecalStripxTop)
        ecalStripxTop_lv.params.append(("SensDet", 'volecalStripxTop'))
 

        ecalStripyTop = geom.shapes.Box( 'ecalStripyTop',
                                    dx = 0.5*self.stripyDimTop[0],
                                    dy = 0.5*self.stripyDimTop[1],
                                    dz = 0.5*self.stripyDimTop[2])
        ecalStripyTop_lv = geom.structure.Volume('volECALStripyTop', material=self.ecalScinMat, shape=ecalStripyTop)
        ecalStripyTop_lv.params.append(("SensDet", 'volecalStripyTop'))


        ecalRadiatorTop = geom.shapes.Box( 'ecalRadiatorTop',
                                     dx = 0.5*self.radiatorDimTop[0],
                                     dy = 0.5*self.radiatorDimTop[1],
                                     dz = 0.5*self.radiatorDimTop[2])
        radiatorTop_lv = geom.structure.Volume('volRadiatorPlateTop', material=self.radiatorMat, shape=ecalRadiatorTop)
        radiatorTop_lv.params.append(("SensDet", 'volradiatorTop'))
 

        nScins = self.nScinLayer
        nBars  = self.nScinBar

        for i in range(nScins):

            for j in range(nBars):
                xposx  = -0.5*self.ecalModDimTop[0]+(j+0.5)*self.stripxDimTop[0]
                yposx  = '0cm'
                zposx  = -0.5*self.ecalModDimTop[2]+i*self.radiatorDimTop[2]+i*self.stripxDimTop[2]+i*self.stripyDimTop[2]+0.5*self.stripxDimTop[2]

                ecalModPosTop = geom.structure.Position('ECALPosTop'+str(i)+'_'+str(j), xposx, yposx, zposx)
                ecalTop = geom.structure.Placement('placeEcalTop'+str(i)+'_'+str(j), volume=ecalStripxTop_lv,
                                               pos=ecalModPosTop)
                ecalModTop_lv.placements.append(ecalTop.name)

                xposy  = '0cm'
                yposy  = -0.5*self.ecalModDimTop[1]+(j+0.5)*self.stripyDimTop[1]
                zposy  = -0.5*self.ecalModDimTop[2]+i*self.radiatorDimTop[2]+i*self.stripxDimTop[2]+i*self.stripyDimTop[2]+self.stripxDimTop[2]+0.5*self.stripyDimTop[2]

                ecalModPosTop2 = geom.structure.Position('ECALPosTop2'+str(i)+'_'+str(j), xposy, yposy, zposy)
                ecalTop2 = geom.structure.Placement('placeEcalTop2'+str(i)+'_'+str(j), volume=ecalStripyTop_lv,
                                                pos=ecalModPosTop2)
                ecalModTop_lv.placements.append(ecalTop2.name)

            xposr  = '0cm'
            yposr  = '0cm'
            zposr  = -0.5*self.ecalModDimTop[2]+i*self.radiatorDimTop[2]+i*self.stripxDimTop[2]+i*self.stripyDimTop[2]+self.stripxDimTop[2]+self.stripyDimTop[2]+0.5*self.radiatorDimTop[2]

            ecalModPosTop3 = geom.structure.Position('ECALPosTop3'+str(i)+'_'+str(j), xposr, yposr, zposr)
            ecalTop3 = geom.structure.Placement('placeEcalTop3'+str(i), volume=radiatorTop_lv,
                    pos=ecalModPosTop3)
            ecalModTop_lv.placements.append(ecalTop3.name)

        ecalPositionTop = geom.structure.Position('ecalTopPosition', self.ecalPosTop[0], self.ecalPosTop[1], self.ecalPosTop[2])
        placeEcalTop = geom.structure.Placement('placeEcalTopName', volume = ecalModTop_lv, pos=ecalPositionTop, rot="r90aboutX")
        full3dst_lv.placements.append( placeEcalTop.name )

        ecalPositionBot = geom.structure.Position('ecalBotPosition',  self.ecalPosBot[0], self.ecalPosBot[1], self.ecalPosBot[2])
        placeEcalBot = geom.structure.Placement('placeEcalBotName', volume = ecalModTop_lv, pos=ecalPositionBot, rot="r90aboutX")
        full3dst_lv.placements.append( placeEcalBot.name )

    def getMagnet(self, full3dst_lv, magPos, geom):

        print('magnet location')
        print((magPos[0]))
        print((magPos[1]))
        print((magPos[2]))

        magOut = geom.shapes.Box( 'MagOut', dx = 0.5*self.magOutDim[0], dy = 0.5*self.magOutDim[1], dz = 0.5*self.magOutDim[2])
        magIn = geom.shapes.Box ('MagInner', dx = 0.5*self.magInDim[0], dy = 0.5*self.magInDim[1], dz = 0.5*self.magInDim[2])

        magBox = geom.shapes.Boolean( 'Magnet', type='subtraction', first=magOut, second=magIn )
        mag_lv = geom.structure.Volume( 'volMagnet', material = self.magMat, shape = magBox)
        mag_lv.params.append(("SensDet", 'volmag'))
 

        #########################################

        magPosition = geom.structure.Position( 'magPosition', self.magPos[0], self.magPos[1], self.magPos[2])
        placeMag = geom.structure.Placement( 'placeMagName', volume = mag_lv, pos = magPosition)

        full3dst_lv.placements.append( placeMag.name )

    def getRPC(self, full3dst_lv, rpcPos, geom):

        print('rpc location')
        print((rpcPos[0]))
        print((rpcPos[1]))
        print((rpcPos[2]))
       
        rpcModDim = self.rpcModDim
        rpcModBox = geom.shapes.Box('rpcModBox', dx=0.5*self.rpcModDim[0], dy=0.5*self.rpcModDim[1], dz=0.5*rpcModDim[2])
        rpcMod_lv = geom.structure.Volume('volRPC', material=self.rpcModMat, shape=rpcModBox)

        resisplate = geom.shapes.Box( 'ResistivePlate',dx=0.5*self.resistplateDim[0], dy=0.5*self.resistplateDim[1], dz=0.5*self.resistplateDim[2])
        resistplate_lv = geom.structure.Volume('volResistivePlate', material=self.resistplateMat, shape=resisplate)
        resistplate_lv.params.append(("SensDet", 'volresistplate'))
 

        rpcGas = geom.shapes.Box( 'RPCGas', dx=0.5*self.resistplateDim[0], dy=0.5*self.resistplateDim[1],dz=0.5*self.resistplateDim[2])
        rpcGas_lv = geom.structure.Volume('volRPCGas', material=self.gasMat, shape=rpcGas)
        rpcGas_lv.params.append(("SensDet", 'volrpcGas'))


        nLayers = self.nRPCLayer

        for i in range(nLayers):
            
            xpos = '0cm'
            ypos = '0cm'
            zpos = -0.5*self.rpcModDim[2]+i*self.resistplateDim[2]+i*self.gas_gap+0.5*self.resistplateDim[2]

            xS_in_m = geom.structure.Position( 'rpcxpos-'+str(i), xpos, ypos, zpos)
            pxS_in_m = geom.structure.Placement( 'placeRPC-'+str(i), volume = resistplate_lv, pos = xS_in_m)

            rpcMod_lv.placements.append( pxS_in_m.name )

            xpos2  = '0cm'
            ypos2  = '0cm'
            zpos2  = -0.5*self.rpcModDim[2]+i*self.resistplateDim[2]+i*self.gas_gap+self.resistplateDim[2]+0.5*self.gas_gap

            xS_in_m2  = geom.structure.Position( 'rpcxpos2-'+str(i),
                                               xpos2,  ypos2,  zpos2)
            pxS_in_m2 = geom.structure.Placement( 'placeRPC2-'+str(i),
                                               volume = rpcGas_lv,pos = xS_in_m2) #,rot = "r90aboutX" )
            rpcMod_lv.placements.append( pxS_in_m2.name )

        ################################################

        rpcPosition = geom.structure.Position( None, rpcPos[0], rpcPos[1], rpcPos[2])
        placeRpc = geom.structure.Placement('placeRpcName', volume = rpcMod_lv, pos=rpcPosition)
        full3dst_lv.placements.append( placeRpc.name )

    def getCylinder(self, full3dst_lv, cylinderPos, geom):

        print('Cylinder location')
        print((self.cylinderPos[0]))
        print((self.cylinderPos[1]))
        print((self.cylinderPos[2]))

        cylinderShape = geom.shapes.Tubs('cylinderShape', rmin=0.5*self.cylinderDim[0], rmax=self.cylinderDim[1], dz=0.5*self.cylinderDim[2], sphi=self.cylinderDim[3], dphi=self.cylinderDim[4])

        cylinder_lv = geom.structure.Volume('volCylinder', material=self.cylinderMat, shape=cylinderShape)

        cylinder_lv.params.append(("SensDet", 'volCylinder'))

        cylinderPosition = geom.structure.Position('cylinderPosition', cylinderPos[0], cylinderPos[1], cylinderPos[2])
        placeCylinder = geom.structure.Placement('placeCylinderName', volume=cylinder_lv, pos=cylinderPosition)#, rot='r90aboutY')
        full3dst_lv.placements.append( placeCylinder.name )
