#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class SandECalBarrelModBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self,
		  trapezoidDim=None,
		  ScintMat=None,
		  PasMat=None,
		  PasSlabThickness=None,
		  ActiveSlabThickness=None,
		  nSlabs=None,
                  BackPlateThick=None,
		  **kwds):
        self.trapezoidDim = trapezoidDim
        self.ScintMat = ScintMat
        self.PasMat = PasMat
        self.PasSlabThickness = PasSlabThickness
        self.ActiveSlabThickness = ActiveSlabThickness
        self.nSlabs = nSlabs
        self.BackPlateThick = BackPlateThick
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        AlPlateThick = self.BackPlateThick

        ECAL_shape = geom.shapes.Trapezoid('ECAL_shape',
					   dx1=self.trapezoidDim[0],
					   dx2=self.trapezoidDim[1]+Q('0.33cm'),
					   dy1=self.trapezoidDim[2],
					   dy2=self.trapezoidDim[2],
					   dz=self.trapezoidDim[3]+AlPlateThick/2.)

        ECAL_lv = geom.structure.Volume('ECAL_lv', material='Air', shape=ECAL_shape)
        self.add_volume(ECAL_lv)
#       ECAL_position = geom.structure.Position('ECAL_position', Position[0], Position[1], Position[2])
#       ECAL_place = geom.structure.Placement('ECAL_place', volume = ECAL_lv, pos=ECAL_position)

            ######## Aluminum back plate##################

        ECAL_Alplate_shape = geom.shapes.Box('ECAL_Alplate_shape',
                                           dx = self.trapezoidDim[1],
                                           dy = self.trapezoidDim[2],
                                           dz = AlPlateThick/2.)
      
        ECAL_Alplate_lv = geom.structure.Volume('ECAL_Alplate_lv', material = 'Aluminum', 
                                              shape = ECAL_Alplate_shape)
      
        ECAL_Alplate_pos = geom.structure.Position('ECAL_Alplate_pos', Q('0cm'), Q('0cm'),
                                                   self.trapezoidDim[3])
      
        ECAL_Alplate_place = geom.structure.Placement('ECAL_Alplate_place', 
                                                    volume = ECAL_Alplate_lv, pos = ECAL_Alplate_pos)
      
        ECAL_lv.placements.append(ECAL_Alplate_place.name)

        for i in range(self.nSlabs): #nSlabs
            #tan = math.tan(math.pi/self.Segmentation)
            tan = 0.5*(self.trapezoidDim[1] - self.trapezoidDim[0])/self.trapezoidDim[3]
            xposSlab=Q('0cm')
            yposSlab=Q('0cm')
            zposSlabActive = (-self.trapezoidDim[3]-AlPlateThick/2. +
		             (i+0.5)*self.ActiveSlabThickness +
                             i*self.PasSlabThickness)
            #print("active slab position= "+ str(zposSlabActive))
            zposSlabPassive = (-self.trapezoidDim[3]-AlPlateThick/2. +
                              (i+1.)*self.ActiveSlabThickness +
                              (i+0.5)*self.PasSlabThickness)
            #print("passive slab position= "+ str(zposSlabPassive))
            bhalfActive=(self.trapezoidDim[0]+
                        i*(self.ActiveSlabThickness*tan)+
                        i*(self.PasSlabThickness*tan))
            bhalfPassive=bhalfActive+(self.ActiveSlabThickness*tan)
            BhalfActive=bhalfActive+self.ActiveSlabThickness*tan
            BhalfPassive=BhalfActive+(self.PasSlabThickness*tan)
            #print("BhalfPassive= "+ str(BhalfPassive))

            #creating and appending active slabs to the ECAL module

            aECALActiveSlab = geom.shapes.Trapezoid('ECALActiveSlab'+'_'+str(i),
						    dx1=bhalfActive,
						    dx2=BhalfActive,
						    dy1=self.trapezoidDim[2],
						    dy2=self.trapezoidDim[2],
						    dz=0.5*self.ActiveSlabThickness)

            aECALActiveSlab_lv = geom.structure.Volume('volECALActiveSlab'+'_'+str(i),
						       material=self.ScintMat,
						       shape=aECALActiveSlab)
            aECALActiveSlab_lv.params.append(("SensDet","EMCalSci"))
            
            aECALActiveSlabPos = geom.structure.Position('ecalactiveslabpos'+'_'+str(i),
							 xposSlab,
							 yposSlab,
							 zposSlabActive)

            aECALActiveSlabPlace = geom.structure.Placement('ecalactiveslabpla'+'_'+str(i),
							    volume = aECALActiveSlab_lv,
							    pos = aECALActiveSlabPos)

            ECAL_lv.placements.append( aECALActiveSlabPlace.name )

            #creating and appending passive slabs to the ECAL module

            aECALPassiveSlab = geom.shapes.Trapezoid('ECALPassiveSlab'+'_'+str(i),
						     dx1=bhalfPassive,
						     dx2=BhalfPassive,
						     dy1=self.trapezoidDim[2],
						     dy2=self.trapezoidDim[2],
						     dz=0.5*self.PasSlabThickness)

            aECALPassiveSlab_lv = geom.structure.Volume('volECALPassiveSlab'+'_'+str(i),
							material=self.PasMat,
							shape=aECALPassiveSlab)

            aECALPassiveSlabPos = geom.structure.Position('ecalpassiveslabpos'+'_'+str(i),
							  xposSlab,
							  yposSlab,
							  zposSlabPassive)

            aECALPassiveSlabPlace = geom.structure.Placement('ecalpassiveslabpla'+'_'+str(i),
							     volume = aECALPassiveSlab_lv,
							     pos = aECALPassiveSlabPos)

            ECAL_lv.placements.append( aECALPassiveSlabPlace.name )
