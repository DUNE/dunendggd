""" Top.py

Original Author: Z. Hulcher, SLAC

"""

#fix all materials
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

#x=H, y=L, and z=W

class FullTopBuilder(gegede.builder.Builder):
    def configure(self,N_Top,top_sep,**kwargs):
        self.Material   = 'Air'
        self.N_Top  = N_Top
        self.top_sep=top_sep
        # Subbuilders
        self.top_builder            = self.get_builder('top')
    def construct(self,geom):
        self.halfDimension = {  'dx':   self.top_builder.halfDimension['dx'],
                                'dy':   self.top_builder.halfDimension['dy'],
                                'dz':   self.top_sep*self.N_Top/2+self.top_builder.halfDimension['dz']}
        main_lv, main_hDim = ltools.main_lv(self,geom,'Box')
        print('DetectorBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)
        W=int((self.N_Top-1)/2)  #pick odd number

        for i in range(-W,W):
            pos = [Q('0cm'),Q('0cm'),i*self.top_sep]
            Top_lv = self.top_builder.get_volume()
            Top_pos = geom.structure.Position(self.top_builder.name+'_pos_'+str(i),pos[0],pos[1],pos[2])
            Top_pla = geom.structure.Placement(self.top_builder.name+'_pla_'+str(i),volume=Top_lv,pos=Top_pos,copynumber=i)
            main_lv.placements.append(Top_pla.name)

class TopBuilder(gegede.builder.Builder):
    def configure(self,tub2grating, **kwargs):
        self.Material = 'Air'
        self.tub2grating=tub2grating
        # Subbuilders
        self.grating_builder = self.get_builder('grating')
        self.tub_builder = self.get_builder('tub')
        self.flanges_builder = self.get_builder('flanges')
    def construct(self,geom):
        self.halfDimension = {'dx':   self.flanges_builder.halfDimension['dx']+self.tub_builder.halfDimension['dx']+self.grating_builder.halfDimension['dx']+self.tub2grating/2,
                              'dy':   self.flanges_builder.halfDimension['dy'],
                              'dz':   self.tub_builder.halfDimension['dz']}
        main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
        print('DetectorBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        pos = [-self.halfDimension['dx']+self.grating_builder.halfDimension['dx'],Q('0cm'), Q('0cm')]
        grating_lv = self.grating_builder.get_volume()
        grating_pos = geom.structure.Position(None, pos[0], pos[1], pos[2])
        grating_pla = geom.structure.Placement(None,volume=grating_lv, pos=grating_pos)
        main_lv.placements.append(grating_pla.name)

        pos = [-self.halfDimension['dx']+2*self.grating_builder.halfDimension['dx']+self.tub_builder.halfDimension['dx']+self.tub2grating,Q('0cm'), Q('0cm')]
        tub_lv = self.tub_builder.get_volume()
        tub_pos = geom.structure.Position(None, pos[0], pos[1], pos[2])
        tub_pla = geom.structure.Placement(None,volume=tub_lv, pos=tub_pos)
        main_lv.placements.append(tub_pla.name)

        pos = [self.halfDimension['dx']-self.flanges_builder.halfDimension['dx'],Q('0cm'), Q('0cm')]
        flanges_lv = self.flanges_builder.get_volume()
        flanges_pos = geom.structure.Position(None, pos[0], pos[1], pos[2])
        flanges_pla = geom.structure.Placement(None,volume=flanges_lv, pos=flanges_pos)
        main_lv.placements.append(flanges_pla.name)

class GratingBuilder(gegede.builder.Builder):#could stand to add square holes in top cover for gratings
    def configure(self,gratingthick, gratingringwidth ,botgratinggap, topgrating_y,topgrating_z, ** kwargs):
        self.gratingthick=gratingthick
        self.gratingringwidth=gratingringwidth
        self.botgratinggap=botgratinggap
        self.topgrating_y=topgrating_y
        self.topgrating_z=topgrating_z
        self.Material = 'LAr'
        self.support_builder = self.get_builder('support')
    def construct(self,geom):
        self.halfDimension = {'dx':   self.gratingthick/2+self.support_builder.halfDimension['dx'], 
                              'dy':   self.topgrating_y/2,   
                              'dz':   self.topgrating_z/2}
        main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
        print('DetectorBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        gratingshape = geom.shapes.Box(None, self.gratingthick/2, self.halfDimension['dy'], self.halfDimension['dz'])

        grating_lv = geom.structure.Volume(None, material='SSteel304', shape=gratingshape)
        grating_pos = geom.structure.Position('grating_pos', self.halfDimension['dx']-self.gratingthick/2, Q('0 in'), Q('0 in'))
        grating_pla = geom.structure.Placement('grating_pla', volume=grating_lv, pos=grating_pos)
        main_lv.placements.append(grating_pla.name)

        sup_lv = self.support_builder.get_volume()
        supdist = self.botgratinggap+self.support_builder.botgrating_dim
        sup1_pos= geom.structure.Position('sup1_pos', -self.gratingthick/2, -2*supdist, Q('0 in'))
        sup2_pos= geom.structure.Position('sup2_pos', -self.gratingthick/2, -supdist, Q('0 in'))
        sup3_pos= geom.structure.Position('sup3_pos', -self.gratingthick/2, Q('0 in'), Q('0 in'))
        sup4_pos= geom.structure.Position('sup4_pos', -self.gratingthick/2, supdist, Q('0 in'))
        sup5_pos= geom.structure.Position('sup5_pos', -self.gratingthick/2, 2*supdist, Q('0 in'))

        rot = geom.structure.Rotation(None, x='90 deg')

        sup1_pla = geom.structure.Placement('sup1_pla', volume=sup_lv, pos=sup1_pos,rot=rot)
        sup2_pla = geom.structure.Placement('sup2_pla', volume=sup_lv, pos=sup2_pos,rot=rot)
        sup3_pla = geom.structure.Placement('sup3_pla', volume=sup_lv, pos=sup3_pos,rot=rot)
        sup4_pla = geom.structure.Placement('sup4_pla', volume=sup_lv, pos=sup4_pos,rot=rot)
        sup5_pla = geom.structure.Placement('sup5_pla', volume=sup_lv, pos=sup5_pos,rot=rot)

        main_lv.placements.append(sup1_pla.name)
        main_lv.placements.append(sup2_pla.name)
        main_lv.placements.append(sup3_pla.name)
        main_lv.placements.append(sup4_pla.name)
        main_lv.placements.append(sup5_pla.name)

class SupportBuilder(gegede.builder.Builder):   #could stand to put in grating pattern and more accurate support legs
    def configure(self, thin_x,base_x,triside,botgrating_dim,gratingthick, **kwargs):
        self.Material ='LAr'
        self.thin_x=thin_x
        self.base_x=base_x
        self.triside=triside
        self.botgrating_dim=botgrating_dim
        self.gratingthick=gratingthick
    def construct(self,geom):
        self.halfDimension = {'dx':   (self.thin_x+2*self.base_x+self.gratingthick)/2,
                              'dy':  self.botgrating_dim/2,
                              'dz':   self.botgrating_dim/2}
        main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
        print('DetectorBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)
        cs = Q("1.6in") #center to side of tri
        base_shape =geom.shapes.PolyhedraRegular(None, 3,Q("0deg"),Q("360deg"),Q("0m"),cs,self.halfDimension['dx']-self.gratingthick/2)#the 1.6 is arbitrary for now
        grating_shape = geom.shapes.Box(None, self.gratingthick/2, self.botgrating_dim/2, self.botgrating_dim/2)

        base_lv = geom.structure.Volume(None, material='SSteel304', shape=base_shape)
        grating_lv=geom.structure.Volume(None, material='SSteel304', shape=grating_shape)
        triplace = self.botgrating_dim/2-cs*pow(2,.5)
        base1_pos = geom.structure.Position('base1_pos', -self.gratingthick/2, -triplace, -triplace)
        base2_pos = geom.structure.Position('base2_pos', -self.gratingthick/2, triplace, -triplace)
        base3_pos = geom.structure.Position('base3_pos', -self.gratingthick/2, -triplace, triplace)
        base4_pos = geom.structure.Position('base4_pos', -self.gratingthick/2, triplace, triplace)
        grating_pos=geom.structure.Position(None, self.halfDimension['dx']-self.gratingthick/2, Q('0 in'), Q('0 in'))

        rot1 = geom.structure.Rotation(None, y='90 deg',z='15 deg')
        rot2 = geom.structure.Rotation(None, y='-90 deg',z='-15 deg')
        rot3 = geom.structure.Rotation(None, y='90 deg',z='-15 deg')
        rot4 = geom.structure.Rotation(None, y='-90 deg', z='15 deg')


        base1_pla = geom.structure.Placement('base1_pla', volume=base_lv, pos=base1_pos,rot=rot1)
        base2_pla = geom.structure.Placement('base2_pla', volume=base_lv, pos=base2_pos,rot=rot3)
        base3_pla = geom.structure.Placement('base3_pla', volume=base_lv, pos=base3_pos,rot=rot4)
        base4_pla = geom.structure.Placement('base4_pla', volume=base_lv, pos=base4_pos,rot=rot2)
        grating_pla=geom.structure.Placement(None, volume=grating_lv, pos=grating_pos)

        main_lv.placements.append(base1_pla.name)
        main_lv.placements.append(base2_pla.name)
        main_lv.placements.append(base3_pla.name)
        main_lv.placements.append(base4_pla.name)
        main_lv.placements.append(grating_pla.name)

        #boxout = geom.shapes.Box(None, self.Grating_z/2, self.Gratingthick/2, self.Grating_z/2)
        #boxin = geom.shapes.Box(None, self.Grating_z/2-self.Gratingringwidth/2, self.Gratingthick/2,self.Grating_z/2-self.Gratingringwidth/2)

class TubBuilder(gegede.builder.Builder):
    def configure(self,tub_y,tub_x,tub_z,bigcylID,bigcylOD,smallcylID,smallcylOD,bigholedist,smallholedist,tubthick, mat_in_flanges,**kwargs):
        self.tub_y=tub_y
        self.tub_x=tub_x
        self.tub_z=tub_z
        self.bigcylID=bigcylID
        self.bigcylOD=bigcylOD
        self.smallcylID=smallcylID
        self.smallcylOD=smallcylOD
        self.bigholedist=bigholedist
        self.smallholedist=smallholedist
        self.tubthick=tubthick
        self.Material = 'Polyurethane'
        self.mat_in_flanges=mat_in_flanges
    def construct(self, geom):
        self.halfDimension = {'dx':   self.tub_x/2,
                              'dy':  self.tub_y/2,
                              'dz':   self.tub_z/2}
        main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
        print('DetectorBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        botplatepos = [ -self.halfDimension['dx']+self.tubthick/2,Q('0cm'),Q('0cm')]
        endplate1pos = [ self.tubthick/2, -(self.halfDimension['dy']-self.tubthick/2), Q('0cm')]
        endplate2pos= [self.tubthick/2,self.halfDimension['dy']-self.tubthick/2,Q('0cm')]
        sideplate1pos = [ self.tubthick/2,Q('0cm'),-(self.halfDimension['dz']-self.tubthick/2)]
        sideplate2pos = [self.tubthick/2, Q('0cm'), self.halfDimension['dz']-self.tubthick/2]

        f1pos = [self.tubthick/2, -2*self.bigholedist, Q('0cm')]
        f2pos = [self.tubthick/2, -self.bigholedist, Q('0cm')]
        f3pos = [self.tubthick/2, Q('0cm'), Q('0cm')]
        f4pos = [self.tubthick/2, self.bigholedist, Q('0cm')]
        f5pos = [self.tubthick/2, 2*self.bigholedist, Q('0cm')]
        sfpos = [self.tubthick/2, 2*self.bigholedist+self.smallholedist, Q('0cm')]

        f_shape = geom.shapes.Tubs(None,self.bigcylID/2,self.bigcylOD/2,self.halfDimension['dx']-self.tubthick/2, Q("0deg"),Q("360deg"))
        sf_shape=geom.shapes.Tubs(None,self.smallcylID/2,self.smallcylOD/2,self.halfDimension['dx']-self.tubthick/2, Q("0deg"),Q("360deg"))
        bigfill_shape=geom.shapes.Tubs(None,Q("0in"),self.bigcylID/2,self.halfDimension['dx']-self.tubthick/2, Q("0deg"),Q("360deg"))
        smallfill_shape=geom.shapes.Tubs(None,Q("0in"),self.smallcylID/2,self.halfDimension['dx']-self.tubthick/2, Q("0deg"),Q("360deg"))

        botplate_shape=geom.shapes.Box(None, self.tubthick/2, self.tub_y/2,self.tub_z/2)
        endplate_shape=geom.shapes.Box(None, self.halfDimension['dx']-self.tubthick/2, self.tubthick/2,self.halfDimension['dz']-self.tubthick)
        sideplate_shape=geom.shapes.Box(None, self.halfDimension['dx']-self.tubthick/2, self.halfDimension['dy']-self.tubthick/2,self.tubthick/2)

        f_lv = geom.structure.Volume("f_lv", material="SSteel304", shape=f_shape)
        sf_lv = geom.structure.Volume("sf_lv", material="SSteel304", shape=sf_shape)
        bigfill_lv = geom.structure.Volume("fill_lv", material=self.mat_in_flanges, shape=bigfill_shape)
        smallfill_lv = geom.structure.Volume("smallfill_lv", material=self.mat_in_flanges, shape=smallfill_shape)

        botplate_lv = geom.structure.Volume("botplate_lv", material='SSteel304', shape=botplate_shape)
        endplate_lv = geom.structure.Volume("endplate_lv", material='SSteel304', shape=endplate_shape)
        sideplate_lv = geom.structure.Volume("sideplate_lv", material='SSteel304', shape=sideplate_shape)

        f1_pos =geom.structure.Position(None, f1pos[0], f1pos[1], f1pos[2])
        f2_pos =geom.structure.Position(None, f2pos[0], f2pos[1], f2pos[2])
        f3_pos =geom.structure.Position(None, f3pos[0], f3pos[1], f3pos[2])
        f4_pos =geom.structure.Position(None, f4pos[0], f4pos[1], f4pos[2])
        f5_pos =geom.structure.Position(None, f5pos[0], f5pos[1], f5pos[2])
        sf_pos =geom.structure.Position(None, sfpos[0], sfpos[1], sfpos[2])
        botplate_pos = geom.structure.Position(None, botplatepos[0], botplatepos[1], botplatepos[2])
        endplate1_pos= geom.structure.Position(None, endplate1pos[0], endplate1pos[1], endplate1pos[2])
        endplate2_pos= geom.structure.Position(None, endplate2pos[0], endplate2pos[1], endplate2pos[2])
        sideplate1_pos= geom.structure.Position(None, sideplate1pos[0], sideplate1pos[1], sideplate1pos[2])
        sideplate2_pos= geom.structure.Position(None, sideplate2pos[0], sideplate2pos[1], sideplate2pos[2])

        rot = geom.structure.Rotation(None, y='90 deg')
        f1_pla = geom.structure.Placement(None,volume=f_lv, pos=f1_pos,rot=rot)
        f2_pla = geom.structure.Placement(None,volume=f_lv, pos=f2_pos,rot=rot)
        f3_pla = geom.structure.Placement(None,volume=f_lv, pos=f3_pos,rot=rot)
        f4_pla = geom.structure.Placement(None,volume=f_lv, pos=f4_pos,rot=rot)
        f5_pla = geom.structure.Placement(None,volume=f_lv, pos=f5_pos,rot=rot)
        sf_pla = geom.structure.Placement(None,volume=sf_lv, pos=sf_pos,rot=rot)

        fill1_pla = geom.structure.Placement(None,volume=bigfill_lv, pos=f1_pos,rot=rot)
        fill2_pla = geom.structure.Placement(None,volume=bigfill_lv, pos=f2_pos,rot=rot)
        fill3_pla = geom.structure.Placement(None,volume=bigfill_lv, pos=f3_pos,rot=rot)
        fill4_pla = geom.structure.Placement(None,volume=bigfill_lv, pos=f4_pos,rot=rot)
        fill5_pla = geom.structure.Placement(None,volume=bigfill_lv, pos=f5_pos,rot=rot)
        fillsf_pla = geom.structure.Placement(None,volume=smallfill_lv, pos=sf_pos,rot=rot)

        botplate_pla = geom.structure.Placement('botplate_pla', volume=botplate_lv, pos=botplate_pos)
        endplate1_pla = geom.structure.Placement('endplate1_pla', volume=endplate_lv, pos=endplate1_pos)
        endplate2_pla = geom.structure.Placement('endplate2_pla', volume=endplate_lv, pos=endplate2_pos)
        sideplate1_pla = geom.structure.Placement('sideplate1_pla', volume=sideplate_lv, pos=sideplate1_pos)
        sideplate2_pla = geom.structure.Placement('sideplate2_pla', volume=sideplate_lv, pos=sideplate2_pos)
        
        main_lv.placements.append(f1_pla.name)
        main_lv.placements.append(f2_pla.name)
        main_lv.placements.append(f3_pla.name)
        main_lv.placements.append(f4_pla.name)
        main_lv.placements.append(f5_pla.name)
        main_lv.placements.append(sf_pla.name)

        main_lv.placements.append(fill1_pla.name)
        main_lv.placements.append(fill2_pla.name)
        main_lv.placements.append(fill3_pla.name)
        main_lv.placements.append(fill4_pla.name)
        main_lv.placements.append(fill5_pla.name)
        main_lv.placements.append(fillsf_pla.name)
        
        main_lv.placements.append(botplate_pla.name)
        main_lv.placements.append(endplate1_pla.name)
        main_lv.placements.append(endplate2_pla.name)
        main_lv.placements.append(sideplate1_pla.name)
        main_lv.placements.append(sideplate2_pla.name)


class FlangesBuilder(gegede.builder.Builder):
    def configure(self, bigplate_y,bigplate_z,plate_x, beamsep,bigholedist,smallholedist, **kwargs):
        self.bigplate_y=bigplate_y
        self.bigplate_z=bigplate_z
        self.plate_x=plate_x
        self.beamsep=beamsep
        self.bigholedist = bigholedist
        self.smallholedist = smallholedist
        self.Material = 'Air'
        self.smallcapcyl_builder = self.get_builder('smallcapcyl')
        self.bigcapcyl_builder = self.get_builder('bigcapcyl')
        self.crossbeam_builder = self.get_builder('crossbeam')
        self.beamend_builder = self.get_builder('beamend')
        self.beamouter_builder = self.get_builder('beamouter')
        self.beaminner_builder = self.get_builder('beaminner')
        self.beamcenter_builder = self.get_builder('beamcenter')
    def construct(self, geom):

        lipsize=self.beamcenter_builder.lipsize
        ccent=(self.beamcenter_builder.length+lipsize)/2
        cmid=self.beaminner_builder.length+lipsize+ccent
        cout=self.beamouter_builder.length+lipsize+cmid
        beamend_y=self.beamend_builder.length
        bend=cout+lipsize/2+beamend_y/2
        bouter=(cout+cmid)/2
        binner=(cmid+ccent)/2

        

        self.halfDimension = {'dx':   self.bigcapcyl_builder.halfDimension['dx']+self.plate_x, 
                              'dy':  bend+beamend_y/2,
                             'dz':   self.bigplate_z/2}
        main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
        print('DetectorBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        platepos = [-self.halfDimension['dx']+self.plate_x/2,Q('0cm'), Q('0cm')]
        #flanges
        f1pos = [self.plate_x/2, -2*self.bigholedist, Q('0cm')]
        f2pos = [self.plate_x/2, -self.bigholedist, Q('0cm')]
        f3pos = [self.plate_x/2, Q('0cm'), Q('0cm')]
        f4pos = [self.plate_x/2, self.bigholedist, Q('0cm')]
        f5pos = [self.plate_x/2, 2*self.bigholedist, Q('0cm')]
        sfpos = [self.plate_x/2, 2*self.bigholedist+self.smallholedist, Q('0cm')]
        
        beamheight=self.beamcenter_builder.midheight+2*self.beamcenter_builder.lipthick
        bh = -self.halfDimension['dx']+self.plate_x+beamheight/2

        #crossbeams
        c1pos = [bh, -cout, Q('0cm')]
        c2pos = [bh, -cmid, Q('0cm')]
        c3pos = [bh, -ccent, Q('0cm')]
        c4pos = [bh, ccent, Q('0cm')]
        c5pos = [bh, cmid, Q('0cm')]
        c6pos = [bh, cout, Q('0cm')]
        
        bs=self.beamsep/2
        #pieces of long beams
        bendLNpos=[bh,-bend,-bs]
        bendRNpos=[bh,bend,-bs]
        bendRPpos =[bh,bend,bs]
        bendLPpos =[bh,-bend,bs]

        bouterLNpos=[bh,-bouter,-bs]
        bouterRNpos=[bh,bouter,-bs]
        bouterRPpos =[bh,bouter,bs]
        bouterLPpos =[bh,-bouter,bs]

        binnerLNpos=[bh,-binner,-bs]
        binnerRNpos=[bh,binner,-bs]
        binnerRPpos =[bh,binner,bs]
        binnerLPpos =[bh,-binner,bs]

        bcenterLpos = [bh, Q('0cm'),-bs]
        bcenterRpos = [bh, Q('0cm'),bs]

        bigplateshape=geom.shapes.Box("plateshape", self.plate_x/2, self.bigplate_y/2,self.bigplate_z/2)
        bigplate_lv =  geom.structure.Volume('bigplate_lv',material='SSteel304',shape=bigplateshape)

        f_lv = self.bigcapcyl_builder.get_volume()
        sf_lv = self.smallcapcyl_builder.get_volume()
        c_lv = self.crossbeam_builder.get_volume()
        bend_lv= self.beamend_builder.get_volume()
        bouter_lv = self.beamouter_builder.get_volume()
        binner_lv = self.beaminner_builder.get_volume()
        bcenter_lv=self.beamcenter_builder.get_volume()

        bigplate_pos=geom.structure.Position('plate_pos', platepos[0], platepos[1], platepos[2])
        f1_pos = geom.structure.Position('f1_pos', f1pos[0], f1pos[1], f1pos[2])
        f2_pos = geom.structure.Position('f2_pos', f2pos[0], f2pos[1], f2pos[2])
        f3_pos = geom.structure.Position('f3_pos', f3pos[0], f3pos[1], f3pos[2])
        f4_pos = geom.structure.Position('f4_pos', f4pos[0], f4pos[1], f4pos[2])
        f5_pos = geom.structure.Position('f5_pos', f5pos[0], f5pos[1], f5pos[2])
        sf_pos = geom.structure.Position('sf_pos', sfpos[0], sfpos[1], sfpos[2])
        c1_pos = geom.structure.Position('c1_pos', c1pos[0], c1pos[1], c1pos[2])
        c2_pos = geom.structure.Position('c2_pos', c2pos[0], c2pos[1], c2pos[2])
        c3_pos = geom.structure.Position('c3_pos', c3pos[0], c3pos[1], c3pos[2])
        c4_pos = geom.structure.Position('c4_pos', c4pos[0], c4pos[1], c4pos[2])
        c5_pos = geom.structure.Position('c5_pos', c5pos[0], c5pos[1], c5pos[2])
        c6_pos = geom.structure.Position('c6_pos', c6pos[0], c6pos[1], c6pos[2])

        bendLN_pos=geom.structure.Position('bendLN_pos', bendLNpos[0], bendLNpos[1], bendLNpos[2])
        bendRN_pos=geom.structure.Position('bendRN_pos', bendRNpos[0], bendRNpos[1], bendRNpos[2])
        bendRP_pos =geom.structure.Position('bendRP_pos', bendRPpos[0], bendRPpos[1], bendRPpos[2])
        bendLP_pos =geom.structure.Position('bendLP_pos', bendLPpos[0], bendLPpos[1], bendLPpos[2])

        bouterLN_pos=geom.structure.Position('bouterLN_pos', bouterLNpos[0], bouterLNpos[1], bouterLNpos[2])
        bouterRN_pos=geom.structure.Position('bouterRN_pos', bouterRNpos[0], bouterRNpos[1], bouterRNpos[2])
        bouterRP_pos =geom.structure.Position('bouterRP_pos', bouterRPpos[0], bouterRPpos[1], bouterRPpos[2])
        bouterLP_pos =geom.structure.Position('bouterLP_pos', bouterLPpos[0], bouterLPpos[1], bouterLPpos[2])

        binnerLN_pos=geom.structure.Position('binnerLN_pos', binnerLNpos[0], binnerLNpos[1], binnerLNpos[2])
        binnerRN_pos=geom.structure.Position('binnerRN_pos', binnerRNpos[0], binnerRNpos[1], binnerRNpos[2])
        binnerRP_pos =geom.structure.Position('binnerRP_pos', binnerRPpos[0], binnerRPpos[1], binnerRPpos[2])
        binnerLP_pos =geom.structure.Position('binnerLP_pos', binnerLPpos[0], binnerLPpos[1], binnerLPpos[2])

        bcenterL_pos = geom.structure.Position('bcenterL_pos', bcenterLpos[0], bcenterLpos[1], bcenterLpos[2])
        bcenterR_pos = geom.structure.Position('bcenterR_pos', bcenterRpos[0], bcenterRpos[1], bcenterRpos[2])

        bigplate_pla = geom.structure.Placement('bigplate_pla',volume=bigplate_lv, pos=bigplate_pos)
        main_lv.placements.append(bigplate_pla.name)

        f1_pla = geom.structure.Placement(None,volume=f_lv, pos=f1_pos)
        main_lv.placements.append(f1_pla.name)
        f2_pla = geom.structure.Placement('f2_pla', volume=f_lv, pos=f2_pos)
        main_lv.placements.append(f2_pla.name)
        f3_pla = geom.structure.Placement('f3_pla', volume=f_lv, pos=f3_pos)
        main_lv.placements.append(f3_pla.name)
        f4_pla = geom.structure.Placement('f4_pla', volume=f_lv, pos=f4_pos)
        main_lv.placements.append(f4_pla.name)
        f5_pla = geom.structure.Placement('f5_pla', volume=f_lv, pos=f5_pos)
        main_lv.placements.append(f5_pla.name)
        sf_pla = geom.structure.Placement('sf_pla', volume=sf_lv, pos=sf_pos)
        main_lv.placements.append(sf_pla.name)

        rot = geom.structure.Rotation('rot',x='90 deg')

        c1_pla = geom.structure.Placement('c1_pla', volume=c_lv, pos=c1_pos,rot=rot)
        main_lv.placements.append(c1_pla.name)
        c2_pla = geom.structure.Placement('c2_pla', volume=c_lv, pos=c2_pos,rot=rot)
        main_lv.placements.append(c2_pla.name)
        c3_pla = geom.structure.Placement('c3_pla', volume=c_lv, pos=c3_pos,rot=rot)
        main_lv.placements.append(c3_pla.name)
        c4_pla = geom.structure.Placement('c4_pla', volume=c_lv, pos=c4_pos,rot=rot)
        main_lv.placements.append(c4_pla.name)
        c5_pla = geom.structure.Placement('c5_pla', volume=c_lv, pos=c5_pos,rot=rot)
        main_lv.placements.append(c5_pla.name)
        c6_pla = geom.structure.Placement('c6_pla', volume=c_lv, pos=c6_pos,rot=rot)
        main_lv.placements.append(c6_pla.name)

        bendLN_pla = geom.structure.Placement('bendLN_pla', volume=bend_lv, pos=bendLN_pos)
        main_lv.placements.append(bendLN_pla.name)
        bendRN_pla = geom.structure.Placement('bendRN_pla', volume=bend_lv, pos=bendRN_pos)
        main_lv.placements.append(bendRN_pla.name)
        bendRP_pla = geom.structure.Placement('bendRP_pla', volume=bend_lv, pos=bendRP_pos)
        main_lv.placements.append(bendRP_pla.name)
        bendLP_pla = geom.structure.Placement('bendLP_pla', volume=bend_lv, pos=bendLP_pos)
        main_lv.placements.append(bendLP_pla.name)

        bouterLN_pla = geom.structure.Placement('bouterLN_pla', volume=bouter_lv, pos=bouterLN_pos)
        main_lv.placements.append(bouterLN_pla.name)
        bouterRN_pla = geom.structure.Placement('bouterRN_pla', volume=bouter_lv, pos=bouterRN_pos)
        main_lv.placements.append(bouterRN_pla.name)
        bouterRP_pla = geom.structure.Placement('bouterRP_pla', volume=bouter_lv, pos=bouterRP_pos)
        main_lv.placements.append(bouterRP_pla.name)
        bouterLP_pla = geom.structure.Placement('bouterLP_pla', volume=bouter_lv, pos=bouterLP_pos)
        main_lv.placements.append(bouterLP_pla.name)

        binnerLN_pla = geom.structure.Placement('binnerLN_pla', volume=binner_lv, pos=binnerLN_pos)
        main_lv.placements.append(binnerLN_pla.name)
        binnerRN_pla = geom.structure.Placement('binnerRN_pla', volume=binner_lv, pos=binnerRN_pos)
        main_lv.placements.append(binnerRN_pla.name)
        binnerRP_pla = geom.structure.Placement('binnerRP_pla', volume=binner_lv, pos=binnerRP_pos)
        main_lv.placements.append(binnerRP_pla.name)
        binnerLP_pla = geom.structure.Placement('binnerLP_pla', volume=binner_lv, pos=binnerLP_pos)
        main_lv.placements.append(binnerLP_pla.name)

        bcenterL_pla = geom.structure.Placement('bcenterL_pla', volume=bcenter_lv, pos=bcenterL_pos)
        main_lv.placements.append(bcenterL_pla.name)
        bcenterR_pla = geom.structure.Placement('bcenterR_pla', volume=bcenter_lv, pos=bcenterR_pos)
        main_lv.placements.append(bcenterR_pla.name)

class CapCylBuilder(gegede.builder.Builder):
    def configure(self, cylID,cylOD,cyl_x,capOD,cap_x,mat_in_flanges, **kwargs):
        self.cylID=cylID
        self.cylOD=cylOD
        self.cyl_x=cyl_x
        self.capOD=capOD
        self.cap_x=cap_x
        self.mat_in_flanges=mat_in_flanges
        self.Material = 'Air'
    def construct(self, geom):
        self.halfDimension = {'dx':   (self.cyl_x+self.cap_x)/2,
                              'dy':   self.capOD/2,                 
                              'dz':   self.capOD/2}
        main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
        print('DetectorBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)

        tubs0=geom.shapes.Tubs(None,self.cylID/2,self.cylOD/2,self.cyl_x/2, Q("0deg"),Q("360deg"))
        fill0=geom.shapes.Tubs(None,Q('0cm'),self.cylID/2,self.cyl_x/2, Q("0deg"),Q("360deg"))
        pos = [-self.cap_x/2,Q('0cm'), Q('0cm')]
        cyl0_lv = geom.structure.Volume(None,material='SSteel304',shape=tubs0)
        fill0_lv=geom.structure.Volume(None,material=self.mat_in_flanges,shape=fill0)
        cyl0_pos = geom.structure.Position(None, x=pos[0], y=pos[1], z=pos[2])
        rot = geom.structure.Rotation(None,y='90 deg')
        cyl0_pla = geom.structure.Placement(None,volume=cyl0_lv, pos=cyl0_pos, rot=rot)
        fill0_pla = geom.structure.Placement(None,volume=fill0_lv, pos=cyl0_pos, rot=rot)
        main_lv.placements.append(cyl0_pla.name)
        main_lv.placements.append(fill0_pla.name)

        tubs1=geom.shapes.Tubs(None,self.cylID/2,self.capOD/2,self.cap_x/2, Q("0deg"),Q("360deg"))
        fill1=geom.shapes.Tubs(None,Q('0cm'),self.cylID/2,self.cap_x/2, Q("0deg"),Q("360deg"))
        pos = [self.cyl_x/2,Q('0cm'), Q('0cm')]
        cyl1_lv = geom.structure.Volume(None,material='SSteel304',shape=tubs1)
        fill1_lv=geom.structure.Volume(None,material=self.mat_in_flanges,shape=fill1)
        cyl1_pos = geom.structure.Position(None, x=pos[0], y=pos[1], z=pos[2])
        rot = geom.structure.Rotation(None, y='90 deg')
        cyl1_pla = geom.structure.Placement(None,volume=cyl1_lv, pos=cyl1_pos, rot=rot)
        fill1_pla = geom.structure.Placement(None,volume=fill1_lv, pos=cyl1_pos, rot=rot)
        main_lv.placements.append(cyl1_pla.name)
        main_lv.placements.append(fill1_pla.name)

class BeamBuilder(gegede.builder.Builder):
    def configure(self, midheight, midthick, lipsize, length,lipthick, **kwargs):
        self.midheight=midheight
        self.midthick=midthick
        self.lipsize=lipsize
        self.length=length
        self.lipthick=lipthick
        self.Material='Air'
    def construct(self, geom):
        self.halfDimension = {'dx':   self.lipthick*2/2+self.midheight/2,
                              'dy':   self.length/2,
                              'dz':   self.lipsize/2}
        main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
        print('DetectorBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)
        toplippos = [-self.halfDimension['dx']+self.lipthick/2,Q('0cm'), Q('0cm')]
        botlippos = [self.halfDimension['dx']-self.lipthick/2,Q('0cm'), Q('0cm')]
        midpos = [Q('0cm'),Q('0cm'), Q('0cm')]

        lipshape = geom.shapes.Box(None, self.lipthick/2, self.length/2,self.lipsize/2)
        midshape=geom.shapes.Box(None, self.midheight/2, self.length/2,self.midthick/2)

        toplip_lv = geom.structure.Volume(None,material='CarbonSteel',shape=lipshape)
        botlip_lv = geom.structure.Volume(None,material='CarbonSteel',shape=lipshape)
        mid_lv = geom.structure.Volume(None,material='CarbonSteel',shape=midshape)

        toplip_pos = geom.structure.Position(None, x=toplippos[0], y=toplippos[1], z=toplippos[2])
        botlip_pos = geom.structure.Position(None, x=botlippos[0], y=botlippos[1], z=botlippos[2])
        mid_pos = geom.structure.Position(None, x=midpos[0], y=midpos[1], z=midpos[2])

        toplip_pla = geom.structure.Placement(None,volume=toplip_lv, pos=toplip_pos)
        botlip_pla = geom.structure.Placement(None,volume=botlip_lv, pos=botlip_pos)
        mid_pla = geom.structure.Placement(None,volume=mid_lv, pos=mid_pos)

        main_lv.placements.append(toplip_pla.name)
        main_lv.placements.append(botlip_pla.name)
        main_lv.placements.append(mid_pla.name)


class CrossBeamBuilder(gegede.builder.Builder):
    def configure(self, midheight, midthick, lipsize, length,lipthick, **kwargs):
        self.midheight=midheight
        self.midthick=midthick
        self.lipsize=lipsize
        self.length=length
        self.lipthick=lipthick
        self.Material='Air'
    def construct(self, geom):
        self.halfDimension = {'dx':   self.lipthick*2/2+self.midheight/2,
                              'dy':   self.length/2,
                              'dz':   self.lipsize/2}
        main_lv, main_hDim = ltools.main_lv(self, geom, 'Box')
        print('DetectorBuilder::construct()')
        print(('main_lv = '+main_lv.name))
        self.add_volume(main_lv)
        toplippos = [-self.halfDimension['dx']+self.lipthick/2,Q('0cm'), Q('0cm')]
        botlippos = [self.halfDimension['dx']-self.lipthick/2,Q('0cm'), Q('0cm')]
        midpos = [Q('0cm'),Q('0cm'), Q('0cm')]
        end1pos = [Q('0cm'), self.length/2-self.lipsize/2+self.midthick/2, Q('0cm')]
        end2pos = [Q('0cm'), -self.length/2+self.lipsize/2-self.midthick/2, Q('0cm')]

        lipshape = geom.shapes.Box(None, self.lipthick/2, self.length/2,self.lipsize/2)
        midshape=geom.shapes.Box(None, self.midheight/2, self.length/2-self.lipsize/2,self.midthick/2)
        endshape=geom.shapes.Box(None, self.midheight/2, self.midthick/2,self.lipsize/2)

        lip_lv = geom.structure.Volume(None,material='CarbonSteel',shape=lipshape)
        mid_lv = geom.structure.Volume(None,material='CarbonSteel',shape=midshape)
        end_lv = geom.structure.Volume(None, material='CarbonSteel', shape=endshape)

        toplip_pos = geom.structure.Position(None, x=toplippos[0], y=toplippos[1], z=toplippos[2])
        botlip_pos = geom.structure.Position(None, x=botlippos[0], y=botlippos[1], z=botlippos[2])
        mid_pos = geom.structure.Position(None, x=midpos[0], y=midpos[1], z=midpos[2])
        end1_pos=geom.structure.Position(None, x=end1pos[0], y=end1pos[1], z=end1pos[2])
        end2_pos=geom.structure.Position(None, x=end2pos[0], y=end2pos[1], z=end2pos[2])

        toplip_pla = geom.structure.Placement(None,volume=lip_lv, pos=toplip_pos)
        botlip_pla = geom.structure.Placement(None,volume=lip_lv, pos=botlip_pos)
        mid_pla = geom.structure.Placement(None,volume=mid_lv, pos=mid_pos)
        end1_pla = geom.structure.Placement(None, volume=end_lv, pos=end1_pos)
        end2_pla = geom.structure.Placement(None, volume=end_lv, pos=end2_pos)

        main_lv.placements.append(toplip_pla.name)
        main_lv.placements.append(botlip_pla.name)
        main_lv.placements.append(mid_pla.name)
        main_lv.placements.append(end1_pla.name)
        main_lv.placements.append(end2_pla.name)


