#!/usr/bin/env python
'''
Subbuilder of ECALBuilder
'''

import gegede.builder
from gegede import Quantity as Q
import math

class MagnetBuilder(gegede.builder.Builder):
 
    # define builder data here
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, actDimension     =None, actDimensionB=None, magGap=None, magBGap=None,
                        actThickness =None, actThicknessB=None, Location=None,
		        actMaterial =None, actMaterialB=None, nMag=None, nMagB=None, **kwds):

        self.magInDim  = actDimension     # inner dimensions of the coils
        self.magOutDim = list(actDimension) #outer dimensions of the coils
        self.magOutDim[1] += 2*actThickness # add to outer dimension in y
        self.magOutDim[2] += 2*actThickness # and in z
        self.MagMat = actMaterial 
        self.actThickness = actThickness
	self.location     = list(Location)

        self.magInDimB  = actDimensionB # inner dimension of the yoke
        self.magInDimB = list(actDimensionB) # why repeated but with list(...)?
        self.magOutDimB = list(actDimensionB)# outer dimension of the yoke 
        self.magOutDimB[0] += 2*actThicknessB # add thickness to outer dimensions in x and y
        self.magOutDimB[1] += 2*actThicknessB
        self.MagMatB = actMaterialB
	self.nMag    = nMag
	self.nMagB   = nMagB
	self.magGap  = magGap
	self.magBGap = magBGap
     
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # many of the volumes below will be defined by subtracting two others
        epsilon=Q("0.1mm") # use when subtracting volA - volB to make volB just a tiny bit bigger along x
        # this gets rid of spurious surfaces in the event display

        ##### make the geometry for a coil segment ##########################
        # the coil is segmented along X
        print(("MagnetBuilder  coil segment outer dimensions = ",self.magOutDim))
        print(("MagnetBuilder  coil segment inner dimensions = ",self.magInDim))
        magOut = geom.shapes.Box( 'MagOut',                 dx=0.5*self.magOutDim[0], 
                                  dy=0.5*self.magOutDim[1], dz=0.5*self.magOutDim[2]) 
        magIn = geom.shapes.Box(  'MagInner',               dx=0.5*self.magInDim[0]+epsilon, 
                                  dy=0.5*self.magInDim[1],  dz=0.5*self.magInDim[2]) 
        
        magBox = geom.shapes.Boolean( 'Mag', type='subtraction', first=magOut, second=magIn ) 
        Mag_lv = geom.structure.Volume('volMag', material=self.MagMat, shape=magBox)


        ##### make the geometry for a yoke segment ###########################
        # the yoke is segmented along z
        print(("MagnetBuilder  yoke segment outer dimensions = ",self.magOutDimB))
        print(("MagnetBuilder  yoke segment inner dimensions = ",self.magInDimB))
        magOutB = geom.shapes.Box( 'YokeOut',                 dx=0.5*self.magOutDimB[0],
                                  dy=0.5*self.magOutDimB[1], dz=0.5*self.magOutDimB[2])
        magInB = geom.shapes.Box(  'YokeInner',               dx=0.5*self.magInDimB[0],
                                   dy=0.5*self.magInDimB[1],  dz=0.5*self.magOutDimB[2]+epsilon)
        magBoxB = geom.shapes.Boolean( 'Yoke', type='subtraction', first=magOutB, second=magInB )
        MagBlock_lv = geom.structure.Volume('volYoke', material=self.MagMatB, shape=magBoxB)

        ##### Make a mother volume to hold the magnet segments ################
        self.MagnetOutt = [self.magOutDimB[0], self.magOutDimB[1], (self.magOutDimB[2]+self.magBGap)*self.nMagB]
	self.MagnetInn = [(self.magInDim[0]+self.magGap)*self.nMag, self.magInDim[1], self.magInDim[2]]

        print(("MagnetBuilder  full yoke outer dimensions = ",self.MagnetOutt))
        print(("MagnetBuilder  full coil inner dimesions = ",self.MagnetInn))
        
        ## define the inner dimensions of the magnet system
        magnetIn = geom.shapes.Box('MagnetInner',dx=0.5*self.MagnetInn[0], 
                                   dy=0.5*self.MagnetInn[1],  dz=0.5*self.MagnetInn[2])

        ## define the outer dimensions of the magnet system
        # The coils are inside the yoke, so it must be bigger than them in x and y.
        # Along z the coils could stick out of the yoke (as in the reference design).
        # Or maybe not, depending on their thickness and other things. 
        # We need to test this.
        coilLengthZ=self.magOutDim[2]
        yokeLengthZ=self.MagnetOutt[2]
        magnetSystemLengthZ=coilLengthZ if coilLengthZ>yokeLengthZ else yokeLengthZ
        # define a variable to hold the outer dimensions of the magnet system
        # this is useful because a builder which calls this builder can use it
        self.MagnetSystemOuterDimension=[self.magOutDimB[0],self.magOutDimB[1],magnetSystemLengthZ]
        magnetOut = geom.shapes.Box( 'MagnetOut',
                                     dx=0.5*self.MagnetSystemOuterDimension[0],
                                     dy=0.5*self.MagnetSystemOuterDimension[1],
                                     dz=0.5*self.MagnetSystemOuterDimension[2])
#        magnetIn = geom.shapes.Box(  'MagnetInner',               dx=0.5*(self.magInDim[0]+self.magGap)*self.nMag,
#                                  dy=0.5*self.magInDim[1],  dz=0.5*self.magInDim[2])
        magnetBox = geom.shapes.Boolean( 'Magnet', type='subtraction', first=magnetOut, second=magnetIn )
        Magnet_lv = geom.structure.Volume('volMagnet', 'Air', shape=magnetBox)
        self.add_volume(Magnet_lv)

        ##### Add coil and yoke segments to the magnet mother volume #########
        for i in range(self.nMag): # adding coil segments
        	magPos  = geom.structure.Position( 'magPos-'+str(i)+'_in_'+self.name,
        	                                    self.location[0]-((self.nMag-1) * self.magGap + self.nMag * self.magInDim[0])/2+(i+0.5)*self.magInDim[0]+i*self.magGap, self.location[1], self.location[2])
        	pMag = geom.structure.Placement( 'magPla-'+str(i)+'_in_'+self.name,
        	                                   volume = Mag_lv,pos = magPos)
        	Magnet_lv.placements.append( pMag.name )

        for j in range(self.nMagB): # adding yoke segments
                magBPos  = geom.structure.Position( 'magBPos-'+str(j)+'_in_'+self.name,
                                                    self.location[0], self.location[1], self.location[2]-((self.nMagB-1)*self.magBGap+self.magInDimB[2]*self.nMagB)/2+(j+0.5)*self.magInDimB[2]+j*self.magBGap)
                pMagB = geom.structure.Placement( 'magBPla-'+str(j)+'_in_'+self.name,
                                                   volume = MagBlock_lv,pos = magBPos)
                Magnet_lv.placements.append( pMagB.name )

#	Magnet_lv.params.append(("SensDet",self.name))
	return


