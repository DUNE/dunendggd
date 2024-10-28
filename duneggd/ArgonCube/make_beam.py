from gegede import Quantity as Q
import gegede.builder

def did_it_work():
    print("it imported nicely")
    return 3

#geom needed, n_support_beams, full_rectnangle_length is size of the dim of shell that you want to build support beams in the direction of, support_beam_gap gap between support beams, support_beam_z
# support_beam_subBuilder, n_support_sections is number of sections that contain triangle gaps, triangle_x_origin, middle_triangle_subBuilder, full_rectangle_height is the size of shell dim paralell to support beam lengths
# support_section_length is the length of each support beam section, triangle_z, triangle_boolean, support_beam_shape, middle_triangle_shape, side_triangle_subBuilder, side_triangle_shape, support_beam_hole_subBuilder,
# support_beam_hole_shape, support_beam_endline_subBuilder, support_beam_endline_shape, rectangle_removal_shape is the frame that we add support beams to, support_beam_boolean,
# main_angle_roti is the rot for support beams in relation to the frame centre in i direction
def make_beam(geom, n_support_beams, full_rectangle_length, support_beam_gap, support_beam_z, support_beam_subBuilder, n_support_sections, triangle_x_origin, middle_triangle_subBuilder,
              full_rectangle_height, support_section_length, triangle_z, triangle_boolean, support_beam_shape, middle_triangle_shape, side_triangle_subBuilder, side_triangle_shape,
              support_beam_hole_subBuilder, support_beam_hole_shape, support_beam_endline_subBuilder, support_beam_endline_shape, rectangle_removal_shape, support_beam_boolean = "union",
              main_angle_rotx = Q("0deg") , main_angle_roty = Q("0deg"), main_angle_rotz = Q("0deg"), extra_name_bit = ""  ):

    # the reason for the x coord is because (n_support_beams-1) *  support_beam_gap / 2 is centre of support_frame, which we want to match the centre of the main frame, then * 2 as we deal with half units
    if n_support_beams ==2:#cheat for 2 hori beams, rotate is not around centre of support frame, so translate the centre after rotation
        support_frame_coord = [  Q("0.0mm") - (n_support_beams-2) *  support_beam_gap , Q("0.0mm") - support_beam_gap, support_beam_z ]
    else:
        support_frame_coord = [  Q("0.0mm") - (n_support_beams-1) *  support_beam_gap , Q("0.0mm"), support_beam_z ]

    
    support_frame_pos = geom.structure.Position(support_beam_subBuilder.name+'frame_pos'+ extra_name_bit, support_frame_coord[0], support_frame_coord[1], support_frame_coord[2] )
    
    for i in range(1, n_support_beams + 1): #should be n_support_beams + 1 i think
        #start building the support beam in negative then finish at positve
        #support_beam_coord = [  Q("0.0cm") - full_rectangle_length + 2 * support_beam_gap * i, Q("0.0cm"), support_beam_z ]
        
        #support_beam_pos = geom.structure.Position(support_beam_subBuilder.name+'_pos'+ extra_name_bit +str(i), support_beam_coord[0], support_beam_coord[1], support_beam_coord[2] )
            

        for j in range(1, n_support_sections+1):
                        
                    
            # up(down) triangle is the triangle pointing up(down)            
            up_triangle_coord = [  triangle_x_origin , Q("0.0mm") - full_rectangle_height + support_beam_hole_subBuilder.height * 2 + middle_triangle_subBuilder.height +
                                   middle_triangle_subBuilder.triangle_gap*2 + support_section_length * (j - 1) * 2, triangle_z ] #j-1 as we want the val to start at 0
            up_triangle_pos = geom.structure.Position(middle_triangle_subBuilder.name+'_pos'+ extra_name_bit +str(i)+str(j), up_triangle_coord[0], up_triangle_coord[1], up_triangle_coord[2] )
            up_triangle_angle = [ Q("270deg") , Q("0deg"), Q("0deg") ]
            up_triangle_rot = geom.structure.Rotation(middle_triangle_subBuilder.name+'_rot'+str(i)+str(j)+ extra_name_bit, up_triangle_angle[0], up_triangle_angle[1], up_triangle_angle[2] )
                    
            if j == 1:
                beam_minus_up_triangle = geom.shapes.Boolean( middle_triangle_subBuilder.name+'_'+ triangle_boolean + str(i) + str(j)+ extra_name_bit, type = triangle_boolean,
                                                              first = support_beam_shape, second = middle_triangle_shape, pos= up_triangle_pos, rot = up_triangle_rot)
            else:
                beam_minus_up_triangle = geom.shapes.Boolean( middle_triangle_subBuilder.name+'_'+ triangle_boolean + str(i) + str(j)+ extra_name_bit, type = triangle_boolean,
                                                              first = last_shape_j_loop, second = middle_triangle_shape, pos= up_triangle_pos, rot = up_triangle_rot)
                    
            #down triangle setting up
            down_triangle_coord = [  triangle_x_origin , Q("0.0mm") - full_rectangle_height + support_beam_hole_subBuilder.height * 2 + support_section_length * (j) * 2
                                     - middle_triangle_subBuilder.height - middle_triangle_subBuilder.triangle_gap
                                     , triangle_z ]
            down_triangle_pos = geom.structure.Position(middle_triangle_subBuilder.name+'down_pos'+str(i)+str(j)+ extra_name_bit, down_triangle_coord[0], down_triangle_coord[1], down_triangle_coord[2] )
            down_triangle_angle = [ Q("90deg") , Q("0deg"), Q("0deg") ]
            down_triangle_rot = geom.structure.Rotation(middle_triangle_subBuilder.name+'down_rot'+str(i)+str(j)+ extra_name_bit, down_triangle_angle[0], down_triangle_angle[1], down_triangle_angle[2] )
                        
            beam_minus_down_triangle = geom.shapes.Boolean( middle_triangle_subBuilder.name+'_down_'+ triangle_boolean + str(i) + str(j)+ extra_name_bit, type = triangle_boolean,
                                                    first = beam_minus_up_triangle, second = middle_triangle_shape, pos= down_triangle_pos, rot = down_triangle_rot)
                    
                    
                        #setup the half triangles
                        #left triangle setup
                        
                        
                    
                                    
                    
                    
                    
                        #setup the left and right triangles
                        #at the start make the extra triangle at bottom, at top have the triangle from the loop, then turn these into halves
            '''
            if j == 1:
                right_triangle_coord = [  triangle_x_origin , Q("0.0mm") - full_rectangle_height + support_beam_hole_subBuilder.height * 2  + support_section_length * (j-0.5) * 2 ,
                                          triangle_z  + side_triangle_subBuilder.height  + side_triangle_subBuilder.side_triangle_gap ]
                right_triangle_pos = geom.structure.Position(side_triangle_subBuilder.name+'down_right_pos'+str(i)+str(j)+ extra_name_bit, right_triangle_coord[0], right_triangle_coord[1], right_triangle_coord[2] )
                right_triangle_angle = [ Q("180deg") , Q("0deg"), Q("0deg") ]
                right_triangle_rot = geom.structure.Rotation(side_triangle_subBuilder.name+'down_right_rot'+str(i)+str(j)+ extra_name_bit, right_triangle_angle[0], right_triangle_angle[1], right_triangle_angle[2] )
                beam_minus_right_triangle = geom.shapes.Boolean( side_triangle_subBuilder.name+'_down_right_'+ triangle_boolean + str(i) + str(j)+ extra_name_bit, type = triangle_boolean,
                                        first = beam_minus_down_triangle, second = side_triangle_shape, pos= right_triangle_pos, rot = right_triangle_rot)
                            
                left_triangle_coord = [  triangle_x_origin , Q("0.0mm") - full_rectangle_height - support_section_length + support_section_length * (j-0.5) * 2 + support_beam_hole_subBuilder.height * 2,
                                                     triangle_z - side_triangle_subBuilder.height - side_triangle_subBuilder.side_triangle_gap]
                left_triangle_pos = geom.structure.Position(side_triangle_subBuilder.name+'down_left_pos'+str(i)+str(j)+ extra_name_bit, left_triangle_coord[0], left_triangle_coord[1], left_triangle_coord[2] )
                left_triangle_angle = [ Q("0deg") , Q("0deg"), Q("0deg") ]
                left_triangle_rot = geom.structure.Rotation(side_triangle_subBuilder.name+'down_left_rot'+str(i)+str(j)+ extra_name_bit, left_triangle_angle[0], left_triangle_angle[1], left_triangle_angle[2] )
                        #cheating with the name below to make things easier
                beam_minus_down_triangle = geom.shapes.Boolean( side_triangle_subBuilder.name+'_down_left_'+ triangle_boolean + str(i) + str(j)+ extra_name_bit, type = triangle_boolean,
                                                                                first = beam_minus_right_triangle, second = side_triangle_shape, pos= left_triangle_pos, rot = left_triangle_rot)
                    
                        
            else:
                pass
            '''
            
            right_triangle_coord = [  triangle_x_origin , Q("0.0mm") - full_rectangle_height + support_beam_hole_subBuilder.height * 2  + support_section_length * (j-0.5) * 2 ,
                                                  triangle_z  + side_triangle_subBuilder.height + side_triangle_subBuilder.side_triangle_gap]
            right_triangle_pos = geom.structure.Position(side_triangle_subBuilder.name+'right_pos'+str(i)+str(j)+ extra_name_bit, right_triangle_coord[0], right_triangle_coord[1], right_triangle_coord[2] )
            right_triangle_angle = [ Q("180deg") , Q("0deg"), Q("0deg") ]
            right_triangle_rot = geom.structure.Rotation(side_triangle_subBuilder.name+'right_rot'+str(i)+str(j)+ extra_name_bit, right_triangle_angle[0], right_triangle_angle[1], right_triangle_angle[2] )
            beam_minus_right_triangle = geom.shapes.Boolean( side_triangle_subBuilder.name+'_right_'+ triangle_boolean + str(i) + str(j)+ extra_name_bit, type = triangle_boolean,
                                                                                first = beam_minus_down_triangle, second = side_triangle_shape, pos= right_triangle_pos, rot = right_triangle_rot)
                        
            left_triangle_coord = [  triangle_x_origin , Q("0.0mm") - full_rectangle_height  + support_beam_hole_subBuilder.height * 2 + support_section_length * (j-0.5) * 2
                                                 , triangle_z - side_triangle_subBuilder.height - side_triangle_subBuilder.side_triangle_gap]
            left_triangle_pos = geom.structure.Position(side_triangle_subBuilder.name+'left_pos'+str(i)+str(j)+ extra_name_bit, left_triangle_coord[0], left_triangle_coord[1], left_triangle_coord[2] )
            left_triangle_angle = [ Q("0deg") , Q("0deg"), Q("0deg") ]
            left_triangle_rot = geom.structure.Rotation(side_triangle_subBuilder.name+'left_rot'+str(i)+str(j)+ extra_name_bit, left_triangle_angle[0], left_triangle_angle[1], left_triangle_angle[2] )
            last_shape_j_loop = geom.shapes.Boolean( side_triangle_subBuilder.name+'_left_'+ triangle_boolean + str(i) + str(j)+ extra_name_bit, type = triangle_boolean,
                                                                                first = beam_minus_right_triangle, second = side_triangle_shape, pos= left_triangle_pos, rot = left_triangle_rot)
            #time to include the blocks at top and bottom
                        
            if j == 1:
                support_beam_hole_coord = [ triangle_x_origin, Q("0.0mm") - full_rectangle_height + support_beam_hole_subBuilder.height, triangle_z ]
                support_beam_hole_pos = geom.structure.Position(support_beam_hole_subBuilder.name+'_pos'+str(i)+str(j)+ extra_name_bit, support_beam_hole_coord[0], support_beam_hole_coord[1], support_beam_hole_coord[2] )
                last_shape_j_loop = geom.shapes.Boolean( support_beam_hole_subBuilder.name+'_'+ triangle_boolean + str(i) + str(j)+ extra_name_bit, type = triangle_boolean,
                                                                                first = last_shape_j_loop, second = support_beam_hole_shape, pos= support_beam_hole_pos)
                    
                #add the support beam end lines
                support_beam_endline_coord = [ triangle_x_origin, Q("0.0mm") - full_rectangle_height + support_beam_hole_subBuilder.height*2 - support_beam_endline_subBuilder.height, triangle_z ]
                support_beam_endline_pos = geom.structure.Position(support_beam_endline_subBuilder.name+'_pos'+str(i)+str(j)+ extra_name_bit, support_beam_endline_coord[0], support_beam_endline_coord[1], support_beam_endline_coord[2] )
                last_shape_j_loop = geom.shapes.Boolean( support_beam_endline_subBuilder.name+'_'+ str(i) + str(j)+ extra_name_bit, type = support_beam_boolean,
                                                                                first = last_shape_j_loop, second = support_beam_endline_shape, pos= support_beam_endline_pos)
                        
                    
                            
            elif j == n_support_sections:
                up_support_beam_hole_coord = [ triangle_x_origin, Q("0.0mm") + full_rectangle_height -  support_beam_hole_subBuilder.height, triangle_z ]
                up_support_beam_hole_pos = geom.structure.Position(support_beam_hole_subBuilder.name+'_up_pos'+str(i)+str(j)+ extra_name_bit, up_support_beam_hole_coord[0], up_support_beam_hole_coord[1], up_support_beam_hole_coord[2] )
                last_shape_j_loop = geom.shapes.Boolean( support_beam_hole_subBuilder.name+'_'+ triangle_boolean + str(i) + str(j)+ extra_name_bit, type = triangle_boolean,
                                                                                first = last_shape_j_loop, second = support_beam_hole_shape, pos= up_support_beam_hole_pos)
                    
                up_support_beam_endline_coord = [ triangle_x_origin, Q("0.0mm") + full_rectangle_height - support_beam_hole_subBuilder.height * 2  + support_beam_endline_subBuilder.height, triangle_z ]
                up_support_beam_endline_pos = geom.structure.Position(support_beam_endline_subBuilder.name+'_up_pos'+str(i)+str(j)+ extra_name_bit,
                                                                                  up_support_beam_endline_coord[0], up_support_beam_endline_coord[1], up_support_beam_endline_coord[2] )
                last_shape_j_loop = geom.shapes.Boolean( support_beam_endline_subBuilder.name+'_'+  str(i) + str(j)+ extra_name_bit, type = support_beam_boolean,
                                                                                first = last_shape_j_loop, second = support_beam_endline_shape, pos= up_support_beam_endline_pos)
                        
                        
                        
                    
        print(i)
        #below uses shape beam_minus_down_triangle as it is the last shape made in the j loop not left triangle
        

        if i == 1:

            
            support_beam_union_shape = last_shape_j_loop#geom.shapes.Boolean( support_beam_subBuilder.name+'_'+ support_beam_boolean + str(i)+ extra_name_bit, type = support_beam_boolean,
                                        #                    first = rectangle_removal_shape, second = last_shape_j_loop, pos= support_beam_pos, rot = main_rot)
            
        else:

            support_beam_coord = [  Q("0.0mm")  + 2 * support_beam_gap * (i-1), Q("0.0mm"), support_beam_z ]
        
            support_beam_pos = geom.structure.Position(support_beam_subBuilder.name+'_pos'+ extra_name_bit +str(i), support_beam_coord[0], support_beam_coord[1], support_beam_coord[2] )
        
            support_beam_union_shape = geom.shapes.Boolean( support_beam_subBuilder.name+'_'+ support_beam_boolean + str(i)+ extra_name_bit, type = support_beam_boolean,
                                                                        first = support_beam_union_shape, second = last_shape_j_loop, pos=support_beam_pos)

    
    main_angle = [main_angle_rotx, main_angle_roty, main_angle_rotz]
    main_rot = geom.structure.Rotation(support_beam_subBuilder.name+'_rot'+ extra_name_bit, main_angle[0], main_angle[1], main_angle[2] )
    support_beam_union_shape = geom.shapes.Boolean( 'composite_window_no_cover_sheets' + extra_name_bit, type = support_beam_boolean,
                                                    first = rectangle_removal_shape, second = support_beam_union_shape, pos=support_frame_pos, rot = main_rot)

    
    return support_beam_union_shape
        
