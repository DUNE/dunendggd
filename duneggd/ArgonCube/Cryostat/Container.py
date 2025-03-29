#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q
import numpy as np

class ContainerBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, dz=None, rmax=None, rmin=None,
                    positions=None, Material=None, connectionshifts=None,
                    inletshifts=None, legshift=None, **kwds ):
        self.rmin, self.rmax, self.dz = (rmin, rmax, dz)
        self.Material = Material
        self.positions = positions
        self.connectionshifts = connectionshifts
        self.inletshifts = inletshifts
        self.legshift = legshift

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        # container
        cont_shape = geom.shapes.Tubs( self.name, rmin=self.rmin, rmax=self.rmax, dz=self.dz )
        cont_lv=geom.structure.Volume( "vol"+cont_shape.name, material=None, shape=None )
        self.add_volume( cont_lv )

        # we will handle the connections, inlets, legs seperately
        sbs = self.get_builders()
        sbs_aux = sbs[-4:]
        inlet_lv   = sbs_aux[2].get_volume()
        conn_lv    = sbs_aux[3].get_volume()
        leg_lv     = sbs_aux[0].get_volume()
        legcon_lv = sbs_aux[1].get_volume()

        nComp = len(sbs) - len(sbs_aux)
        sbs = sbs[:nComp]
        # place the first components
        for i, (sb, pos) in enumerate(zip(sbs, self.positions)):
            sb_lv = sb.get_volume()
            sb_pos = geom.structure.Position(self.name+sb_lv.name+'_pos',
                                             pos[0], pos[1], pos[2])     
            sb_rot = geom.structure.Rotation(self.name+sb_lv.name+'_rot',
                                             '0.0deg', '0.0deg', '0.0deg')                            
            sb_pla = geom.structure.Placement(self.name+sb_lv.name+'_pla',
                                              volume=sb_lv, pos=sb_pos, rot=sb_rot)
            cont_lv.placements.append(sb_pla.name)

        # place the connections
        self.placeConnections(geom, conn_lv, cont_lv)

        # place the inlets
        self.placeInlets(geom, inlet_lv, cont_lv)

        # place legs
        self.placeLegs(geom, leg_lv, legcon_lv, cont_lv)  

    def placeConnections(self, geom, conn_lv, cont_lv):
        connR = self.connectionshifts[2]
        connAng = self.connectionshifts[1]
        connZ1 = self.connectionshifts[0]
        connZ2 = self.connectionshifts[3]
        # hard coding here!
        # very rough
        connR2 = connR - Q('19cm')

        pos = [connR*np.cos(connAng), connR*np.sin(connAng), connZ1]  
        rot1 = Q('90.deg') - connAng
        rot2 = Q('90.deg') + connAng

        conn1_pos = geom.structure.Position(self.name+conn_lv.name+'1_pos', pos[0], pos[1], pos[2])     
        conn1_rot = geom.structure.Rotation(self.name+conn_lv.name+'1_rot', '90.0deg', -1*rot1, '0.0deg')                            
        conn1_pla = geom.structure.Placement(self.name+conn_lv.name+'1_pla', volume=conn_lv, pos=conn1_pos, rot=conn1_rot)
        cont_lv.placements.append(conn1_pla.name)

        conn2_pos = geom.structure.Position(self.name+conn_lv.name+'2_pos', pos[0], -1*pos[1], pos[2])     
        conn2_rot = geom.structure.Rotation(self.name+conn_lv.name+'2_rot', '90.0deg', -1*rot2, '0.0deg')                            
        conn2_pla = geom.structure.Placement(self.name+conn_lv.name+'2_pla', volume=conn_lv, pos=conn2_pos, rot=conn2_rot)
        cont_lv.placements.append(conn2_pla.name)

        conn3_pos = geom.structure.Position(self.name+conn_lv.name+'3_pos', connR2, Q('0m'), connZ2)     
        conn3_rot = geom.structure.Rotation(self.name+conn_lv.name+'3_rot', '0.0deg', '-153.0deg', '0.0deg') # Constant roughly measured from CAD
        conn3_pla = geom.structure.Placement(self.name+conn_lv.name+'3_pla', volume=conn_lv, pos=conn3_pos, rot=conn3_rot)
        cont_lv.placements.append(conn3_pla.name)

    def placeInlets(self, geom, inlet_lv, cont_lv):
        inletR   = self.inletshifts[2]
        inletAngs = self.inletshifts[1]
        inletZ   = self.inletshifts[0]

        pos = []
        rot = []
        for ang in inletAngs:
            pos.append([inletR*np.cos(ang), inletR*np.sin(ang), inletZ])  
            rot.append(Q('90deg') + ang)

        for i in range(0,4):            
            inlet_pos = geom.structure.Position(self.name+inlet_lv.name+str(i+1)+'_pos', pos[i][0], -1*pos[i][1], pos[i][2])     
            inlet_rot = geom.structure.Rotation(self.name+inlet_lv.name+str(i+1)+'_rot', '90.0deg', -1*rot[i], '0.0deg')                            
            inlet_pla = geom.structure.Placement(self.name+inlet_lv.name+str(i+1)+'_pla', volume=inlet_lv, pos=inlet_pos, rot=inlet_rot)
            cont_lv.placements.append(inlet_pla.name)    

    def placeLegs(self, geom, leg_lv, legcon_lv, cont_lv):
        # legs
        pla = self.legshift[0]*np.cos(np.pi/4.)

        leg_pos1 = geom.structure.Position(self.name+leg_lv.name+ '_pos1', pla, pla, self.legshift[1])     
        leg_rot1 = geom.structure.Rotation(self.name+leg_lv.name+ '_rot1', '0.0deg', '0.0deg', '0.0deg')                            
        leg_pla1 = geom.structure.Placement(self.name+leg_lv.name+'_pla1', volume=leg_lv, pos=leg_pos1, rot=leg_rot1)
        cont_lv.placements.append(leg_pla1.name)

        leg_pos2 = geom.structure.Position(self.name+leg_lv.name+ '_pos2', -1*pla, pla, self.legshift[1])     
        leg_rot2 = geom.structure.Rotation(self.name+leg_lv.name+ '_rot2', '0.0deg', '0.0deg', '0.0deg')                            
        leg_pla2 = geom.structure.Placement(self.name+leg_lv.name+'_pla2', volume=leg_lv, pos=leg_pos2, rot=leg_rot2)
        cont_lv.placements.append(leg_pla2.name)

        leg_pos3 = geom.structure.Position(self.name+leg_lv.name+ '_pos3', -1*pla, -1*pla, self.legshift[1])     
        leg_rot3 = geom.structure.Rotation(self.name+leg_lv.name+ '_rot3', '0.0deg', '0.0deg', '0.0deg')                            
        leg_pla3 = geom.structure.Placement(self.name+leg_lv.name+'_pla3', volume=leg_lv, pos=leg_pos3, rot=leg_rot3)
        cont_lv.placements.append(leg_pla3.name)

        leg_pos4 = geom.structure.Position(self.name+leg_lv.name+ '_pos4', pla, -1*pla, self.legshift[1])     
        leg_rot4 = geom.structure.Rotation(self.name+leg_lv.name+ '_rot4', '0.0deg', '0.0deg', '0.0deg')                            
        leg_pla4 = geom.structure.Placement(self.name+leg_lv.name+'_pla4', volume=leg_lv, pos=leg_pos4, rot=leg_rot4)
        cont_lv.placements.append(leg_pla4.name)

        # connectors
        shiftZ = -1*self.dz + Q('10cm')
        con_pos1 = geom.structure.Position(self.name+legcon_lv.name+ '_pos1', pla, Q('0m'), shiftZ)     
        con_rot1 = geom.structure.Rotation(self.name+legcon_lv.name+ '_rot1', '90.0deg', '0.0deg', '0.0deg')                            
        con_pla1 = geom.structure.Placement(self.name+legcon_lv.name+'_pla1', volume=legcon_lv, pos=con_pos1, rot=con_rot1)
        cont_lv.placements.append(con_pla1.name)

        con_pos2 = geom.structure.Position(self.name+legcon_lv.name+ '_pos2', Q('0m'), pla, shiftZ)     
        con_rot2 = geom.structure.Rotation(self.name+legcon_lv.name+ '_rot2', '0.0deg', '90.0deg', '0.0deg')                            
        con_pla2 = geom.structure.Placement(self.name+legcon_lv.name+'_pla2', volume=legcon_lv, pos=con_pos2, rot=con_rot2)
        cont_lv.placements.append(con_pla2.name)

        con_pos3 = geom.structure.Position(self.name+legcon_lv.name+ '_pos3', -1*pla, Q('0m'), shiftZ)     
        con_rot3 = geom.structure.Rotation(self.name+legcon_lv.name+ '_rot3', '90.0deg', '0.0deg', '0.0deg')                            
        con_pla3 = geom.structure.Placement(self.name+legcon_lv.name+'_pla3', volume=legcon_lv, pos=con_pos3, rot=con_rot3)
        cont_lv.placements.append(con_pla3.name)

        con_pos4 = geom.structure.Position(self.name+legcon_lv.name+ '_pos4', Q('0m'), -1*pla, shiftZ)     
        con_rot4 = geom.structure.Rotation(self.name+legcon_lv.name+ '_rot4', '0.0deg', '90.0deg', '0.0deg')                            
        con_pla4 = geom.structure.Placement(self.name+legcon_lv.name+'_pla4', volume=legcon_lv, pos=con_pos4, rot=con_rot4)
        cont_lv.placements.append(con_pla4.name)                
