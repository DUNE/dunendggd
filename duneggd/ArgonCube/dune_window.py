import gegede.builder
from gegede import Quantity as Q
#import numpy as np
from . import make_beam
from duneggd.LocalTools import localtools as ltools
import math

#make_beam.did_it_work()


class WorldBuilder(gegede.builder.Builder):
    '''
    Build a simple box world of given material and size.
    '''
    def configure(self, material = 'Air', show_cover_sheets = True, length = Q("8620mm") * 1.1 , height = Q("3800mm") * 1.1, dz = Q("374.62mm") *1.1,
                  n_support_beams = 8, n_support_beams_hori = 1, verti_active_area = Q("0mm"), hori_active_area = Q("0mm"), AuxParams = None,  **kwds):
        
        self.material, self.length, self.height, self.depth = (material, length, height, dz)
        self.show_cover_sheets = show_cover_sheets
        self.n_support_beams = n_support_beams
        self.n_support_beams_hori = n_support_beams_hori
        self.verti_active_area = verti_active_area
        self.hori_active_area = hori_active_area
        self.AuxParams = AuxParams
        
        pass

    def construct(self, geom):
        
        ## Define the materials.  All materials should be defined in
        ## the world builder construct method.
        ## some elements from https://pubchem.ncbi.nlm.nih.gov/periodic-table
        h = geom.matter.Element("Elem_hydrogen", "H", 1, "1.00791*g/mole" )
        c = geom.matter.Element("Elem_carbon",   "C", 6, "12.0107*g/mole")
        n = geom.matter.Element("Elem_nitrogen", "N", 7, "14.0671*g/mole")
        o = geom.matter.Element("Elem_oxygen",   "O", 8, "15.999*g/mole" )

        fe = geom.matter.Element("Elem_iron", "Fe", 26, "55.845*g/mole")

        mn = geom.matter.Element("Elem_manganese", "Mn", 25, "54.938*g/mole")

        p = geom.matter.Element("Elem_phosphorus", "P", 15, "30.973762*g/mole")

        s = geom.matter.Element("Elem_sulfur", "S", 16, "32.07*g/mole")

        si = geom.matter.Element("Elem_silicon", "Si", 14, "28.085*g/mole")
        
        plastic = geom.matter.Mixture("Plastic",   density="1.05*g/cc",
                                      components = (
                                          ("Elem_carbon",   0.9),
                                          ("Elem_hydrogen", 0.1)
                                    ))
        #comment out below as Air already in use
        #air = geom.matter.Mixture("Air",
         #                         density = "0.001225*g/cc",
          #                        components = (
           #                           ("Elem_nitrogen", 0.8),
            #                          ("Elem_oxygen",   0.2),
             #                       ))
        #assuming only using low carbon steel (0.3%) approx dens 7.87 g/cm3
        simple_steel = geom.matter.Mixture("Simple_steel",    density = "7.87*g/cc",
                                    components = (
                                        ("Elem_carbon", 0.003),
                                        ("Elem_iron", 0.997),
                                    ))
        #Grad 50 A572 steel at this link https://www.matweb.com/search/datasheet.aspx?matguid=9ced5dc901c54bd1aef19403d0385d7f&ckck=1
        # Also silicon range is 0.15 - 0.40% https://en.wikipedia.org/wiki/A572_steel

        # Steel mixture already in use, 
        #steel = geom.matter.Mixture("Steel",    density = "7.80*g/cc",
         #                           components = (
          #                              ("Elem_carbon", 0.0021),
           #                             ("Elem_manganese", 0.0135),
            #                            ("Elem_phosphorus", 0.0003),
             #                           ("Elem_sulfur", 0.0003),
              #                          ("Elem_carbon", 0.0021),
               #                         ("Elem_silicon", 0.00275), #this is avg of silicon range above
                #                        ("Elem_iron", 0.97895), #quickly calced using 1 - others
                 #                   ))
        
        
    
        

        

        #make the full rectangle builder
        full_rectangle_subBuilder = self.get_builders()[0]
        #make the smaller steel sub builder
        smaller_rectangle_subBuilder = self.get_builders()[1]
        #sideways_smaller_rectangle_subBuilder = self.get_builders()[2]
        zaxis_smaller_rectangle_subBuilder = self.get_builders()[6] #to remove the wall in the zaxis
        #get the support beam
        support_beam_subBuilder = self.get_builders()[2]
        #get the triangle_builder
        middle_triangle_subBuilder = self.get_builders()[4]
        side_triangle_subBuilder = self.get_builders()[5]
        #get support beam end holes
        support_beam_hole_subBuilder = self.get_builders()[7]
        #get the sideways support beam
        sideways_support_beam_subBuilder = self.get_builders()[3]
        #get the line for the end of the support beam
        support_beam_endline_subBuilder = self.get_builders()[8]
        #get the extra thick intersection points
        support_beam_intersection_subBuilder = self.get_builders()[9]
        support_beam_hole_hori_subBuilder = self.get_builders()[10]

        #make the steel sheets
        inner_sheet_subBuilder = self.get_builders()[11]
        outer_sheet_subBuilder = self.get_builders()[12]

        #get hori triangles
        hori_middle_triangle_subBuilder = self.get_builders()[13]
        hori_side_triangle_subBuilder = self.get_builders()[14]
        
        

        
        
    
        
        #make the subVolumes
        full_rectangle_subVolume = full_rectangle_subBuilder.get_volume()
        smaller_rectangle_subVolume = smaller_rectangle_subBuilder.get_volume()
        zaxis_smaller_rectangle_subVolume = zaxis_smaller_rectangle_subBuilder.get_volume()
        #sideways_smaller_rectangle_subVolume = sideways_smaller_rectangle_subBuilder.get_volume()
        support_beam_subVolume = support_beam_subBuilder.get_volume()
        middle_triangle_subVolume = middle_triangle_subBuilder.get_volume()
        side_triangle_subVolume = side_triangle_subBuilder.get_volume()
        sideways_support_beam_subVolume = sideways_support_beam_subBuilder.get_volume()
        support_beam_hole_subVolume = support_beam_hole_subBuilder.get_volume()
        support_beam_endline_subVolume = support_beam_endline_subBuilder.get_volume()
        support_beam_intersection_subVolume = support_beam_intersection_subBuilder.get_volume()
        support_beam_hole_hori_subVolume = support_beam_hole_hori_subBuilder.get_volume()
        inner_sheet_subVolume = inner_sheet_subBuilder.get_volume()
        outer_sheet_subVolume = outer_sheet_subBuilder.get_volume()
        hori_middle_triangle_subVolume = hori_middle_triangle_subBuilder.get_volume()
        hori_side_triangle_subVolume = hori_side_triangle_subBuilder.get_volume()
        
        
        #make the shapes we will need
        full_rectangle_shape = geom.store.shapes.get(full_rectangle_subVolume.shape)
        smaller_rectangle_shape = geom.store.shapes.get(smaller_rectangle_subVolume.shape)
        zaxis_smaller_rectangle_shape = geom.store.shapes.get(zaxis_smaller_rectangle_subVolume.shape)
        #sideways_smaller_rectangle_shape = geom.store.shapes.get(sideways_smaller_rectangle_subVolume.shape)
        support_beam_shape = geom.store.shapes.get(support_beam_subVolume.shape)
        middle_triangle_shape = geom.store.shapes.get(middle_triangle_subVolume.shape)
        side_triangle_shape = geom.store.shapes.get(side_triangle_subVolume.shape)
        sideways_support_beam_shape = geom.store.shapes.get(sideways_support_beam_subVolume.shape)
        support_beam_hole_shape = geom.store.shapes.get(support_beam_hole_subVolume.shape)
        support_beam_endline_shape = geom.store.shapes.get(support_beam_endline_subVolume.shape)
        support_beam_intersection_shape = geom.store.shapes.get(support_beam_intersection_subVolume.shape)
        support_beam_hole_hori_shape = geom.store.shapes.get(support_beam_hole_hori_subVolume.shape)
        inner_sheet_shape = geom.store.shapes.get(inner_sheet_subVolume.shape)
        outer_sheet_shape = geom.store.shapes.get(outer_sheet_subVolume.shape)
        hori_middle_triangle_shape = geom.store.shapes.get(hori_middle_triangle_subVolume.shape)
        hori_side_triangle_shape = geom.store.shapes.get(hori_side_triangle_subVolume.shape)
        
        
        #make the position for the smaller rectangle removal
        rectangle_removal_coord =  [  Q("0.0mm"), Q("0.0mm"), Q("0mm") ]
        rectangle_removal_pos = geom.structure.Position(self.name+'_pos', rectangle_removal_coord[0], rectangle_removal_coord[1], rectangle_removal_coord[2] )
        rectangle_removal_boolean = "subtraction"
        rectangle_removal_shape = geom.shapes.Boolean( self.name+'_zaxis_'+rectangle_removal_boolean , type = rectangle_removal_boolean ,
                                                       first = full_rectangle_shape, second=zaxis_smaller_rectangle_shape, pos=rectangle_removal_pos)
        
        #rectangle_removal_shape = geom.shapes.Boolean( self.name+'_'+rectangle_removal_boolean , type = rectangle_removal_boolean , first = rectangle_removal_shape, second=smaller_rectangle_shape, pos=rectangle_removal_pos)
        #remove the sideways triangle to remove material on top of rectangle
        #rectangle_removal_shape = geom.shapes.Boolean( self.name+'_sideways_'+rectangle_removal_boolean , type = rectangle_removal_boolean ,
         #                                              first = rectangle_removal_shape, second=sideways_smaller_rectangle_shape, pos=rectangle_removal_pos)

        
        #rectangle_removal_lv = geom.structure.Volume('vol'+rectangle_removal_shape.name, material=self.material,shape=rectangle_removal_shape)

        #add information for support beams
        full_rectangle_length = full_rectangle_subBuilder.length
        full_rectangle_height = full_rectangle_subBuilder.height
        n_support_beams = self.n_support_beams
        support_beam_length = support_beam_subBuilder.length #length refers to x-axis
        hori_active_area = self.hori_active_area
        support_beam_gap = (hori_active_area ) / (n_support_beams -1) # minus 1 as there is an extra beam on the end

        #Get triangle height for later
        triangle_height = middle_triangle_subBuilder.height#mark this as middle for now but will likely want changing
        #Get gap between up and down triangles
        triangle_gap = middle_triangle_subBuilder.triangle_gap#mark this as middle for now but will likely want changing
        
        #support sections are the boxes containing triangles holes
        n_support_sections = 8#5
        verti_active_area = self.verti_active_area #uses 3285 not 3030 from diagram, 3030 breaks this. 
        support_section_length = verti_active_area  / (n_support_sections)


        #up and down refers to triangle direction that it is pointing in, left and right refers to if the triangle is on the left or right.
        # for ease of debugging
        triangle_x_origin = Q("-0.55m") * 0
        triangle_z = Q("0mm")
        support_beam_z = Q("5m") * 0
        
        
        #time to add the support beams
        support_beam_boolean = "union"
        triangle_boolean = "subtraction"

        #n_support_beams = 1 #this should not be 1, but I am changing this so it is easier to view
        support_beam_union_shape = make_beam.make_beam(geom, n_support_beams, full_rectangle_length, support_beam_gap, support_beam_z, support_beam_subBuilder, n_support_sections, triangle_x_origin, middle_triangle_subBuilder,
                                                             full_rectangle_height, support_section_length, triangle_z, triangle_boolean, support_beam_shape, middle_triangle_shape, side_triangle_subBuilder, side_triangle_shape,
                                                             support_beam_hole_subBuilder, support_beam_hole_shape, support_beam_endline_subBuilder, support_beam_endline_shape, rectangle_removal_shape, support_beam_boolean,
                                                             main_angle_rotx = Q("0deg") , main_angle_roty = Q("0deg"), main_angle_rotz = Q("0deg")  )

        n_support_beams_hori = self.n_support_beams_hori #should be 2
        support_beam_gap_hori = ( verti_active_area) / (n_support_beams_hori + 1) # the arena surrounds beams so +1
        support_beam_subBuilder_hori = sideways_support_beam_subBuilder
        
        n_support_sections_hori = 14 #this to be changed now !!!
        support_section_length_hori = hori_active_area / (n_support_sections_hori) # this time plus 3 for 1.5 sections on either end of hori beam
        
        #middle_triangle_subBuilder_hori = middle_triangle_subBuilder
        
        support_beam_shape_hori = sideways_support_beam_shape
        #middle_triangle_shape_hori = middle_triangle_shape
        #side_triangle_subBuilder_hori = side_triangle_subBuilder
        #side_triangle_shape_hori = side_triangle_shape
        support_beam_hole_subBuilder_hori = support_beam_hole_hori_subBuilder #change now!!!
        support_beam_hole_shape_hori = support_beam_hole_hori_shape #change now!!!
        support_beam_endline_subBuilder_hori = support_beam_endline_subBuilder
        support_beam_endline_shape_hori = support_beam_endline_shape
        
        support_beam_union_shape = make_beam.make_beam(geom, n_support_beams_hori, full_rectangle_height, support_beam_gap_hori, support_beam_z, support_beam_subBuilder_hori, n_support_sections_hori, triangle_x_origin,
                                                       hori_middle_triangle_subBuilder, full_rectangle_length, support_section_length_hori, triangle_z, triangle_boolean, support_beam_shape_hori, hori_middle_triangle_shape,
                                                       hori_side_triangle_subBuilder, hori_side_triangle_shape,
                                                       support_beam_hole_subBuilder_hori, support_beam_hole_shape_hori, support_beam_endline_subBuilder_hori, support_beam_endline_shape_hori,support_beam_union_shape,
                                                       #should be support_beam_union_shape
                                                       support_beam_boolean, Q("0deg") , Q("0deg"),  Q("90deg"), "_hori_")





        if self.show_cover_sheets == True:
            #add the inner and outer sheets
            outer_sheet_coord =  [  Q("0.0mm"), Q("0.0mm"), full_rectangle_subBuilder.thickness + outer_sheet_subBuilder.thickness  ]
            outer_sheet_pos = geom.structure.Position(outer_sheet_subBuilder.name+'_pos', outer_sheet_coord[0], outer_sheet_coord[1], outer_sheet_coord[2] )
            outer_sheet_boolean = "union"
            support_beam_union_shape = geom.shapes.Boolean( outer_sheet_subBuilder.name+'_union_shape_' , type = outer_sheet_boolean ,
                                                    first = support_beam_union_shape, second= outer_sheet_shape, pos = outer_sheet_pos)

            inner_sheet_coord =  [  Q("0.0mm"), Q("0.0mm"),Q("0.0mm") - full_rectangle_subBuilder.thickness - inner_sheet_subBuilder.thickness  ]
            inner_sheet_pos = geom.structure.Position(inner_sheet_subBuilder.name+'_pos', inner_sheet_coord[0], inner_sheet_coord[1], inner_sheet_coord[2] )
            inner_sheet_boolean = "union"
            support_beam_union_shape = geom.shapes.Boolean( 'composite_window_with_cover_sheets' , type = inner_sheet_boolean ,
                                                       first = support_beam_union_shape, second= inner_sheet_shape, pos = inner_sheet_pos)
        else:
            pass
        

        support_beam_union_lv = geom.structure.Volume( 'volCompositeWindow', material=support_beam_subBuilder.material, shape=support_beam_union_shape) #'vol'+ support_beam_union_shape.name
        #triangle_subtract_lv = geom.structure.Volume('vol'+ triangle_subtract_shape.name, material=self.material, shape=triangle_subtract_shape)

        #make world vol
        dim = (self.length, self.height, self.depth)
        world_shape = geom.shapes.Box(self.name + '_box_shape', *dim)

        world_volume = geom.structure.Volume(self.name+'_volume', material=self.material, shape=world_shape)
        
        #world_angle = [Q("0deg") , Q("0deg"),  Q("90deg")]
        #world_rot = geom.structure.Rotation(self.name+'_rot', world_angle[0], world_angle[1], world_angle[2] )
        #placement = geom.structure.Placement('place'+ support_beam_union_shape.name, volume = support_beam_union_lv)
        #volume = geom.structure.Volume('my_volume', material = self.material, placements = placement)

        #need to append the daughter
        #world_volume.placements.append(placement.name)
        
        volume = support_beam_union_lv
        self.add_volume(volume) #used to be world_volume
        ########### new lines below!!
        if self.AuxParams != None:
            ltools.addAuxParams( self, volume )

        #time to remove triangles from support beams
        
        
        
        

class Block(gegede.builder.Builder):
   
    def configure(self, material = 'Steel', length = Q("5cm"), height = Q("1cm"), thickness = Q("0.1cm"),  AuxParams = None, **kwds):

        self.material = material
        self.thickness, self.length, self.height = (thickness, length, height)
        pass

    def construct(self, geom):
        

        # get volumes from sub-builders.  Note, implicitly assume
        # order, which must be born out by configuration.  Once could
        # remove this by querying each sub-builder for its "location"
        # configuration parameter, but this then requires other
        # assumptions.
        #blocks = [sb.get_volume() for sb in self.get_builders()]
        #block_shape = geom.store.shapes.get(blocks[-1].shape)
        
        #blocks.reverse()        # you'll see why

        # Calculate overall dimensions from daughters.  Assume identical cubes!
        #half_size = (block_shape.dx + self.gap) * 3
        #dim = (half_size,)*3

        #Try and make my own volume
        dim = (self.length, self.height, self.thickness)
        #dim = (half_size,) * 3
        
        # make overall shape and LV
        shape = geom.shapes.Box(self.name + '_box_shape', *dim)
        
        volume = geom.structure.Volume(self.name+'_volume',
                                       material=self.material, shape=shape)
        self.add_volume(volume)



class TriangleGap(gegede.builder.Builder):
    #Build a Rubik's cube (kind of).  

    #Delegate to three sub-builders assumed to provide each one of, in
    #order, corner, edge and center blocks.  Blocks are assumed to be
    #cubes of equal size.

    def configure(self,  material = 'Steel', side_length = Q("5cm"), angle = 45 * 3.14 / 180, thickness = Q("0.1cm"), triangle_gap = Q("7.5cm"), side_triangle_gap = Q("0cm"), **kwds):
        
        self.material = material
        self.thickness, self.side_length = (thickness, side_length)
        #self height is to make sure the triangle is equilateral
        self.height = side_length / 2 * math.tan(angle)
        self.triangle_gap = triangle_gap
        self.side_triangle_gap  = side_triangle_gap
        pass

    def construct(self, geom):
        

        # get volumes from sub-builders.  Note, implicitly assume
        # order, which must be born out by configuration.  Once could
        # remove this by querying each sub-builder for its "location"
        # configuration parameter, but this then requires other
        # assumptions.
        #blocks = [sb.get_volume() for sb in self.get_builders()]
        #block_shape = geom.store.shapes.get(blocks[-1].shape)
        
        #blocks.reverse()        # you'll see why

        # Calculate overall dimensions from daughters.  Assume identical cubes!
        #half_size = (block_shape.dx + self.gap) * 3
        #dim = (half_size,)*3

        
        #Try and make my own volume
        dim = (self.thickness, self.thickness, self.side_length, Q("0cm"), self.height)
        
        
        # make overall shape and LV
        shape = geom.shapes.Trapezoid(self.name + '_box_shape', *dim)
        volume = geom.structure.Volume(self.name+'_volume', 
                                   material=self.material, shape=shape)
        self.add_volume(volume)

