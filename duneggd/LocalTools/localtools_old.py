from gegede import Quantity as Q
import math
from platform import python_version

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def main_lv( slf, geom, shape):
    """
    """
    if "Box" == shape:
        main_shape = geom.shapes.Box( slf.name, dx=slf.halfDimension['dx'], dy=slf.halfDimension['dy'],
                                        dz=slf.halfDimension['dz'] )
        main_hDim = [main_shape.dx, main_shape.dy, main_shape.dz]
    elif "Tubs" == shape:
        main_shape = geom.shapes.Tubs( slf.name, rmin=slf.halfDimension['rmin'],
                                        rmax=slf.halfDimension['rmax'], dz=slf.halfDimension['dz'] )
        main_hDim = [main_shape.rmax, main_shape.rmax, main_shape.dz]
    elif "Sphere" == shape:
        main_shape = geom.shapes.Sphere( slf.name, rmin=slf.halfDimension['rmin'],
                                            rmax=slf.halfDimension['rmax'] )
        main_hDim = [main_shape.rmax, main_shape.rmax, main_shape.rmax]
    elif "Cone" == shape:
        main_shape = geom.shapes.Cone( slf.name, rmin1=slf.halfDimension['rmin1'],
                                        rmax1=slf.halfDimension['rmax1'], rmin2=slf.halfDimension['rmin2'],
                                        rmax2=slf.halfDimension['rmax2'],dz=slf.halfDimension['dz'] )
        main_hDim = [main_shape.rmax1 if main_shape.rmax1 >= main_shape.rmax2 else main_shape.rmax2,
                    main_shape.rmax1 if main_shape.rmax1 >= main_shape.rmax2 else main_shape.rmax2, main_shape.dz]
    elif "Trapezoid" == shape:
        main_shape = geom.shapes.Trapezoid( slf.name, dx1=slf.halfDimension['dx1'], dx2=slf.halfDimension['dx2'],
                                        dy1=slf.halfDimension['dy1'], dy2=slf.halfDimension['dy2'],
                                        dz=slf.halfDimension['dz'] )
        main_hDim = [main_shape.dx1 if main_shape.dx1 >= main_shape.dx2 else main_shape.dx2,
                    main_shape.dy1 if main_shape.dy1 >= main_shape.dy2 else main_shape.dx2, main_shape.dz]
    return geom.structure.Volume( "vol"+slf.name, material=slf.Material, shape=main_shape ), main_hDim

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def addAuxParams( slf, ggd_vol ):

    assert( slf.AuxParams != None ), " No AuxParams defined on %s " % ggd_vol.name

    for key in slf.AuxParams:
        if isinstance(slf.AuxParams[key],str):
            ggd_vol.params.append((key,slf.AuxParams[key]))

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def getShapeDimensions( ggd_vol, geom ):
    """
    """
    ggd_shape = geom.store.shapes.get(ggd_vol.shape)
    shapename = type(ggd_shape).__name__
    ggd_dim = []
    if "Box" in shapename:
        ggd_dim = [ggd_shape.dx, ggd_shape.dy, ggd_shape.dz]
    elif "Tubs" in shapename:
        ggd_dim = [ggd_shape.rmax, ggd_shape.rmax, ggd_shape.dz]
    elif "Sphere" in shapename:
        ggd_dim = [ggd_shape.rmax, ggd_shape.rmax, ggd_shape.rmax]
    elif "Cone" in shapename:
        ggd_dim = [ggd_shape.rmax1 if ggd_shape.rmax1 >= ggd_shape.rmax2 else ggd_shape.rmax2,
                    ggd_shape.rmax1 if ggd_shape.rmax1 >= ggd_shape.rmax2 else ggd_shape.rmax2, ggd_shape.dz]
    elif "Trapezoid" in shapename:
        ggd_dim = [ggd_shape.dx1 if ggd_shape.dx1 >= ggd_shape.dx2 else ggd_shape.dx2,
                    ggd_shape.dy1 if ggd_shape.dy1 >= ggd_shape.dy2 else ggd_shape.dx2, ggd_shape.dz]
    else:
        ggd_dim = None
    return ggd_dim

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def getRotation( slf, geom ):
    """
    Return the Rotation, is not defined return 0deg rotation
    """
    if slf.Rotation == None:
        return geom.structure.Rotation( slf.name+'_rot', '0.0deg', '0.0deg', '0.0deg' )
    else:
        return geom.structure.Rotation( slf.name+'_rot', str(slf.Rotation[0]),
                                            str(slf.Rotation[1]),  str(slf.Rotation[2]) )

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def getCrossRotations( slf, geom ):
    """
    Return the Rotations, is not defined return 0deg rotations
    """
    if slf.RotTop == None:
        rotTop = geom.structure.Rotation( slf.name+'_rotTop', '0deg', '0deg', '0deg' )
    else:
        rotTop = geom.structure.Rotation( slf.name+'_rotTop', str(slf.RotTop[0]),
                                                str(slf.RotTop[1]),  str(slf.RotTop[2]) )

    if slf.RotBottom == None:
        rotBottom = geom.structure.Rotation( slf.name+'_rotBottom', '0deg', '0deg', '0deg' )
    else:
        rotBottom = geom.structure.Rotation( slf.name+'_rotBottom', str(slf.RotBottom[0]),
                                                str(slf.RotBottom[1]),  str(slf.RotBottom[2]) )

    if slf.RotLeft == None:
        rotLeft = geom.structure.Rotation( slf.name+'_rotLeft', '0deg', '0deg', '0deg' )
    else:
        rotLeft = geom.structure.Rotation( slf.name+'_rotLeft', str(slf.RotLeft[0]),
                                                str(slf.RotLeft[1]),  str(slf.RotLeft[2]) )

    if slf.RotRight == None:
        rotRight = geom.structure.Rotation( slf.name+'_rotRight', '0deg', '0deg', '0deg' )
    else:
        rotRight = geom.structure.Rotation( slf.name+'_rotRight', str(slf.RotRight[0]),
                                                str(slf.RotRight[1]),  str(slf.RotLRight[2]) )

    return rotTop, rotBottom, rotLeft, rotRight

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def getInsideGap( slf ):
    """
    Return the InsideGap, if it is not defined return 0m
    """
    if slf.InsideGap == None:
        return Q('0m')
    else:
        return slf.InsideGap

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def getBeginGap( slf ):
    """
    Return the BeginGap, if it is not defined return 0m
    """
    if slf.BeginGap == None:
        return Q('0m')
    else:
        return slf.BeginGap

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def getTranspP( slf ):
    """
    Return the Transportation Plane, useful for CrossSubDetectorBuilder
    """
    if  slf.TranspP == None :
            return {'top':[1,0,0],'side':[0,1,0]}
    else:
        return slf.TranspP

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def getInitialPos( slf, ggd_dim, transpV ):
    """
    Return the initial postion for the builder based on the TranspV
    """
    begingap = getBeginGap( slf )

    if slf.NElements == 0:
        if slf.SubBPos != None:
            return slf.SubBPos
        else:
            return [Q('0m'),Q('0m'),Q('0m')]
    else:
        return [-t*(d-begingap) for t,d in zip(transpV,ggd_dim)]

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def placeBuilders( slf, geom, main_lv, TranspV ):
    """
    Place sub-builders inside the main_lv,
    simple linear arrange of 1 subbuilders
    """
    # definition local rotation
    rotation = getRotation( slf, geom )
    # check InsideGap
    InsideGap = getInsideGap( slf )
    # get the sub-builders and its dimensions
    sb = slf.get_builder()
    sb_lv = sb.get_volume()
    sb_dim = getShapeDimensions( sb_lv, geom )
    # get the main dimensions
    main_hDim = getShapeDimensions( main_lv, geom )
    # get the initial position of the sub-builders
    pos = getInitialPos( slf, main_hDim, TranspV )
    # placement n elements
    if slf.NElements > 0:
        for elem in range(slf.NElements):
            step = [ t*d for t,d in zip(TranspV, sb_dim) ]
            pos = [ p+s for p,s in zip(pos,step) ]
            sb_pos = geom.structure.Position(slf.name+sb_lv.name+str(elem)+'_pos',
                                                pos[0], pos[1], pos[2])
            sb_pla = geom.structure.Placement(slf.name+sb_lv.name+str(elem)+'_pla',
                                                volume=sb_lv, pos=sb_pos, rot =rotation)
            main_lv.placements.append(sb_pla.name)
            pos = [p+s+t*InsideGap for p,s,t in zip(pos,step,TranspV)]
    # placement simple element, component or subdetector
    elif slf.NElements == 0:
        sb_pos = geom.structure.Position(slf.name+sb_lv.name+'_pos',
                                            pos[0], pos[1], pos[2])
        sb_pla = geom.structure.Placement(slf.name+sb_lv.name+'_pla',
                                            volume=sb_lv, pos=sb_pos, rot =rotation)
        main_lv.placements.append(sb_pla.name)

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def placeUserLocationBuilders( slf, geom, main_lv, TranspV ):
    # check InsideGap
    InsideGap = getInsideGap( slf )
    # get the main dimensions
    main_hDim = getShapeDimensions( main_lv, geom )
    # initial position, based on the dimension projected on transportation vector
    pos = [-t*(d) for t,d in zip(TranspV,main_hDim)]
    # get builders
    builders = slf.get_builders()
    places = slf.UserPlace

    for i,sb in enumerate(builders):
        sb_lv = sb.get_volume()
        sb_dim = getShapeDimensions( sb_lv, geom )
        if sb_dim == None:
            assert( sb.halfDimension != None ), " No dimension defined on %s " % sb
            sb_dim = [sb.halfDimension['dx'],sb.halfDimension['dy'],sb.halfDimension['dz']]
        step = [ t*d for t,d in zip(TranspV, sb_dim) ]
        pos = [ p+s for p,s in zip(pos,step) ]

        step2 = [ -t*d for t,d in zip(places[i], sb_dim) ]
        pos2 = [ t*(d)+s for t,d,s in zip(places[i],main_hDim, step2)]

        pos = [p+p2 for p, p2 in zip(pos, pos2)] #+

        sb_pos = geom.structure.Position(slf.name+sb_lv.name+'_pos', pos[0], pos[1], pos[2])
        sb_pla = geom.structure.Placement(slf.name+sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos )
        main_lv.placements.append(sb_pla.name)

        pos = [p-p2 for p, p2 in zip(pos, pos2)] #-
        pos = [p+s+t*InsideGap for p,s,t in zip(pos,step,TranspV)]

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def placeComplexBuilders( slf, geom, main_lv, TranspV ):
    """
    Place sub-builders inside the main_lv
    """
    # definition local rotation
    rotation = getRotation( slf, geom )
    # check InsideGap
    InsideGap = getInsideGap( slf )
    # get the main dimensions
    main_hDim = getShapeDimensions( main_lv, geom )
    # initial position, based on the dimension projected on transportation vector
    pos = getInitialPos( slf, main_hDim, TranspV )
    # get builders
    builders = slf.get_builders()

    for elem in range(slf.NElements):
        for i,sb in enumerate(builders):
            # get the sub-builders and its dimensions
            sb_lv = sb.get_volume()
            sb_dim = getShapeDimensions( sb_lv, geom )
            step = [ t*d for t,d in zip(TranspV, sb_dim) ]
            pos = [ p+s for p,s in zip(pos,step) ]
            sb_pos = geom.structure.Position(slf.name+sb_lv.name+str(elem)+'_pos',
                                                pos[0], pos[1], pos[2])
            sb_pla = geom.structure.Placement(slf.name+sb_lv.name+str(elem)+'_pla',
                                                volume=sb_lv, pos=sb_pos, rot =rotation)
            main_lv.placements.append(sb_pla.name)
            pos = [p+s+t*InsideGap for p,s,t in zip(pos,step,TranspV)]

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def placeSurroundBuilders( main_lv, sb_cent, sb_surr, gap, geom ):
    """
    """
    sb_cent_lv = sb_cent.get_volume()
    sb_cent_dim = getShapeDimensions( sb_cent_lv, geom )
    sb_surr_lv = sb_surr.get_volume()
    sb_surr_dim = getShapeDimensions( sb_surr_lv, geom )

    rotLeft = geom.structure.Rotation( main_lv.name+'_rotLeft', '0deg', '0deg', '90deg' )
    rotRight = geom.structure.Rotation( main_lv.name+'_rotRight', '0deg', '0deg', '-90deg' )

    sb_cent_pos = geom.structure.Position( sb_cent_lv.name+'_pos', Q("0m"), Q("0m"), Q("0m") )
    sb_cent_pla = geom.structure.Placement( sb_cent_lv.name+'_pla', volume=sb_cent_lv, pos=sb_cent_pos )
    main_lv.placements.append( sb_cent_pla.name )

    # Top
    pos = [ Q('0m'), sb_cent_dim[1] + sb_surr_dim[1] + gap, Q('0m') ]
    sb_surr_pos = geom.structure.Position( sb_surr_lv.name+'_top_pos', pos[0], pos[1], pos[2] )
    sb_surr_pla = geom.structure.Placement( sb_surr_lv.name+'_top_pla', volume=sb_surr_lv, pos=sb_surr_pos )
    main_lv.placements.append( sb_surr_pla.name )

    # Left
    pos = [ sb_cent_dim[0] + sb_surr_dim[1] + gap, Q('0m'), Q('0m') ]
    sb_surr_pos = geom.structure.Position( sb_surr_lv.name+'_left_pos', pos[0], pos[1], pos[2] )
    sb_surr_pla = geom.structure.Placement( sb_surr_lv.name+'_left_pla', volume=sb_surr_lv,
                                                pos=sb_surr_pos, rot=rotLeft )
    main_lv.placements.append( sb_surr_pla.name )

    # Bottom
    pos = [ Q('0m'), -sb_cent_dim[1] - sb_surr_dim[1] - gap, Q('0m') ]
    sb_surr_pos = geom.structure.Position( sb_surr_lv.name+'_bottom_pos', pos[0], pos[1], pos[2] )
    sb_surr_pla = geom.structure.Placement( sb_surr_lv.name+'_bottom_pla', volume=sb_surr_lv, pos=sb_surr_pos )
    main_lv.placements.append( sb_surr_pla.name )

    #Right
    pos = [ -sb_cent_dim[0] - sb_surr_dim[1] - gap, Q('0m'), Q('0m') ]
    sb_surr_pos = geom.structure.Position( sb_surr_lv.name+'_right_pos', pos[0], pos[1], pos[2] )
    sb_surr_pla = geom.structure.Placement( sb_surr_lv.name+'_right_pla', volume=sb_surr_lv,
                                                pos=sb_surr_pos, rot=rotRight )
    main_lv.placements.append( sb_surr_pla.name )

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def placeCrossBuilders( main_lv, sb_cent, sb_top, sb_side, slf, geom ):
    """
    """
    Gap = getInsideGap( slf )
    TranspP = getTranspP( slf )
    sb_cent_lv = sb_cent.get_volume()
    sb_cent_dim = getShapeDimensions( sb_cent_lv, geom )
    sb_top_lv = sb_top.get_volume()
    sb_top_dim = getShapeDimensions( sb_top_lv, geom )
    sb_side_lv = sb_side.get_volume()
    sb_side_dim = getShapeDimensions( sb_side_lv, geom )

    sb_cent_pos = geom.structure.Position( main_lv.name+sb_cent_lv.name+'_pos', Q("0m"), Q("0m"), Q("0m") )
    sb_cent_pla = geom.structure.Placement( main_lv.name+sb_cent_lv.name+'_pla', volume=sb_cent_lv, pos=sb_cent_pos )
    main_lv.placements.append( sb_cent_pla.name )

    rotTop, rotBottom, rotLeft, rotRight = getCrossRotations( slf, geom )

    # Top
    pzero = [ Q('0m'), Q('0m'), Q('0m') ]
    pos = [pz+transp*(cen+top+Gap) for pz,transp,cen,top in zip(pzero,TranspP['top'],sb_cent_dim,sb_top_dim)]
    #pos = [ Q('0m'), sb_cent_dim[1] + sb_top_dim[1] + gap, Q('0m') ]
    sb_top_pos = geom.structure.Position( main_lv.name+sb_top_lv.name+'_top_pos', pos[0], pos[1], pos[2] )
    sb_top_pla = geom.structure.Placement( main_lv.name+sb_top_lv.name+'_top_pla', volume=sb_top_lv,
                                                pos=sb_top_pos, rot=rotTop )
    main_lv.placements.append( sb_top_pla.name )

    # Left
    pos = [pz+transp*(cen+side+Gap) for pz,transp,cen,side in zip(pzero,TranspP['side'],sb_cent_dim,sb_side_dim)]
    #pos = [ sb_cent_dim[0] + sb_side_dim[1] + gap, Q('0m'), Q('0m') ]
    sb_side_pos = geom.structure.Position( main_lv.name+sb_side_lv.name+'_left_pos', pos[0], pos[1], pos[2] )
    sb_side_pla = geom.structure.Placement( main_lv.name+sb_side_lv.name+'_left_pla', volume=sb_side_lv,
                                                pos=sb_side_pos, rot=rotLeft )
    main_lv.placements.append( sb_side_pla.name )

    # Bottom
    pos = [pz-transp*(cen+top+Gap) for pz,transp,cen,top in zip(pzero,TranspP['top'],sb_cent_dim,sb_top_dim)]
    #pos = [ Q('0m'), -sb_cent_dim[1] - sb_top_dim[1] - gap, Q('0m') ]
    sb_top_pos = geom.structure.Position( main_lv.name+sb_top_lv.name+'_bottom_pos', pos[0], pos[1], pos[2] )
    sb_top_pla = geom.structure.Placement( main_lv.name+sb_top_lv.name+'_bottom_pla', volume=sb_top_lv,
                                                pos=sb_top_pos, rot=rotBottom )
    main_lv.placements.append( sb_top_pla.name )

    #Right
    pos = [pz-transp*(cen+side+Gap) for pz,transp,cen,side in zip(pzero,TranspP['side'],sb_cent_dim,sb_side_dim)]
    #pos = [ -sb_cent_dim[0] - sb_side_dim[1] - gap, Q('0m'), Q('0m') ]
    sb_side_pos = geom.structure.Position( main_lv.name+sb_side_lv.name+'_right_pos', pos[0], pos[1], pos[2] )
    sb_side_pla = geom.structure.Placement( main_lv.name+sb_side_lv.name+'_right_pla', volume=sb_side_lv,
                                                pos=sb_side_pos, rot=rotRight )
    main_lv.placements.append( sb_side_pla.name )

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def placeBooleanBuilders( slf, geom, main_lv, TranspV ):
    # check InsideGap
    InsideGap = getInsideGap( slf )
    # get the main dimensions
    main_hDim = getShapeDimensions( main_lv, geom )
    # get shape of main_lv in case of boolean shapes
    sb_boolean_shape = geom.store.shapes.get(main_lv.shape)
    # initial position, based on the dimension projected on transportation vector
    pos = [-t*(d) for t,d in zip(TranspV,main_hDim)]
    # get builders
    builders = slf.get_builders()
    places = slf.UserPlace

    for i,sb in enumerate(builders):
        sb_lv = sb.get_volume()
        dim_dict = sb.halfDimension
        sb_dim = [ dim_dict['dx'], dim_dict['dy'], dim_dict['dz'] ]
        step = [ t*d for t,d in zip(TranspV, sb_dim) ]
        pos = [ p+s for p,s in zip(pos,step) ]

        step2 = [ -t*d for t,d in zip(places[i], sb_dim) ]
        pos2 = [ t*(d)+s for t,d,s in zip(places[i],main_hDim, step2)]

        pos = [p+p2 for p, p2 in zip(pos, pos2)] #+
        sb_pos = geom.structure.Position(slf.name+sb_lv.name+'_pos', pos[0], pos[1], pos[2])

        sb_shape = geom.store.shapes.get(sb_lv.shape)
        if i == 0 and slf.Boolean == "union":
            operation = "intersection"
        else:
            operation = slf.Boolean

        sb_boolean_shape = geom.shapes.Boolean( slf.name+'_bool_'+str(i), type=operation,
                                            first=sb_boolean_shape, second=sb_shape, pos=sb_pos)

        pos = [p-p2 for p, p2 in zip(pos, pos2)] #-
        pos = [p+s+t*InsideGap for p,s,t in zip(pos,step,TranspV)]

    sb_boolean_lv = geom.structure.Volume('vol'+sb_boolean_shape.name, material=slf.Material,
                                        shape=sb_boolean_shape)

    if slf.AuxParams != None:
        addAuxParams( slf, sb_boolean_lv )

    slf.add_volume( sb_boolean_lv )

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def rotation( axis, theta, vec ):
    """
    Return the vector rotated, the rotation matrix is called inside.
    """
    Matrix = rotation_matrix( axis, theta)
    rot_vec = [0,0,0]
    rot_vec[0] = Matrix[0][0]*vec[0] + Matrix[0][1]*vec[1] + Matrix[0][2]*vec[2]
    rot_vec[1] = Matrix[1][0]*vec[0] + Matrix[1][1]*vec[1] + Matrix[1][2]*vec[2]
    rot_vec[2] = Matrix[2][0]*vec[0] + Matrix[2][1]*vec[1] + Matrix[2][2]*vec[2]
    return rot_vec

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def rotation_matrix( axis, theta ):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta degrees. (https://en.wikipedia.org/wiki/Euler-Rodrigues_formula)
    """
    theta_rad = math.radians(theta)
    a = math.cos(theta_rad/2.0)
    b = -1*math.sin(theta_rad/2.0)*axis[0]
    c = -1*math.sin(theta_rad/2.0)*axis[1]
    d = -1*math.sin(theta_rad/2.0)*axis[2]
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return [[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)], [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]]
