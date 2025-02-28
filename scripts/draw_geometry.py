import ROOT

ROOT.gROOT.SetBatch(True)
import sys
import collections
import os
import time
import hashlib
import math

import argparse
import numpy as np
import re

import colorsys

VERBOSE = False


def material_to_rgb(
    atomic_number,
    density,
    atomic_min=1,
    atomic_max=55.845,
    density_min=0.0,
    density_max=13.0,
    bw=False,
):

    # Normalize atomic number to a hue value between 0 and 1 (for colorsys)
    hue_normalized = (atomic_number - atomic_min) / (atomic_max - atomic_min)
    hue = hue_normalized  # Hue in colorsys (0 to 1 range for red to purple)

    # Normalize density to brightness (value) between 0 and 1
    if density > density_max:
        print(f"Found density > density_max: {density} > {density_max}")
    brightness_normalized = 1 - ((density - density_min) / (density_max - density_min))
    brightness = max(0, min(brightness_normalized, 1))  # Clamp between 0 and 1

    saturation = 0.0 if bw else 1.0
    small_density = 0.02
    if not bw and density < small_density:
        saturation = density / small_density

    # Convert HSV to RGB
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, brightness)

    # Scale RGB values to 0-255
    return int(r * 255), int(g * 255), int(b * 255)


def load_geometry(gdml_file):
    """Load the geometry from a GDML file."""
    geom = ROOT.TGeoManager.Import(gdml_file)
    if not geom:
        raise FileNotFoundError(f"GDML file '{gdml_file}' not found or invalid.")
    return geom


def make_image(w, h, initial_color="#FFFFFF"):
    """Makes an w x h image, with some initial color"""
    image = ROOT.TASImage(w, h)
    image.DrawBox(0, 0, w, h, initial_color, 1, 2)
    return image


def hex_color(number):
    temp = hex(number)[2:]
    if len(temp) < 2:
        temp = "0" + temp
    return temp


def from_rgb(r, g, b):
    out = "#"
    out += hex_color(r)
    out += hex_color(g)
    out += hex_color(b)
    return out


def random_color(name):
    hash_bytes = hashlib.md5(name.encode()).digest()
    return from_rgb(hash_bytes[0], hash_bytes[5], hash_bytes[11])


def get_node(geom, i, j, matrix):
    pos = calc_projection(i, j, matrix)
    return geom.FindNode(*pos)


def get_material(node):
    out = None
    med = node.GetMedium()
    if med != None:
        material = med.GetMaterial()
        if material != None:
            out = material
    return out


def material_is_air(node):
    material = get_material(node)
    out = False
    if material != None:
        if material.GetName() == "Air":
            out = True
    return out


def material_is_clear(node):
    material = get_material(node)
    out = False
    if material != None:
        if material.GetName() == "Air":
            out = True
        if material.GetName() == "Vac":
            out = True
    return out


black = "#000000"
yellow = from_rgb(253, 179, 56)
blue = from_rgb(2, 81, 150)
white = "#FFFFFF"
color_map = {"all_volDetEnclosure_0": white}
names_seen = set()


def color_function(node, highlight, exclude_clear=True):
    """
    Parameters:
        - node - the TGeoNode to gather properties from.
        - highlight - the highlighting function. Options are:
            random - choose random color based on name
            scintillator - scintillator is black, everything else is white
            material - plastic yellow, steel blue, rock black
            density - density determines brightness, atomic number determines hue
            density_bw - black and white, only scale based on density
        - exclude_clear - draws air and vac as white
    """
    name = node.GetName()
    names_seen.add(name)
    key = highlight + "_" + name
    try:
        return color_map[key]
    except KeyError:
        color = None
        if exclude_clear and material_is_clear(node):
            color = white
        else:
            if highlight == "random":
                color = random_color(name)
            if highlight == "scintillator":
                if "scin" in name:
                    color = black
                else:
                    color = white
            if highlight == "material":
                material = get_material(node)
                if material == None:
                    color = white
                else:
                    if material.GetName() == "Air":
                        color = white
                    if material.GetName() == "Scintillator":
                        color = yellow
                    if material.GetName() == "Polyurethane":
                        color = yellow
                    if material.GetName() == "SteelTMS":
                        color = blue
                    if "Steel" in material.GetName():
                        color = blue
                    if material.GetName() == "Rock":
                        color = black
                    if color == None:
                        raise NotImplementedError(
                            f"Do not have a color for {material.GetName()}"
                        )
            if highlight == "density" or highlight == "density_bw":
                material = get_material(node)
                if material == None:
                    color = white
                else:
                    density = material.GetDensity()
                    a = material.GetA()
                    bw = False
                    if highlight == "density_bw":
                        bw = True
                    if VERBOSE:
                        print(
                            f"atomic number: {a:0.2f},\tdensity: {density:0.2f},\tmaterial name: {material.GetName()}"
                        )
                    r, g, b = material_to_rgb(a, density, bw=bw)
                    color = from_rgb(r, g, b)
                    if color == None:
                        raise NotImplementedError(
                            f"Do not have a color for {material.GetName()}"
                        )
        if color == None:
            raise NotImplementedError(f"Do not understand highlight option {highlight}")
        color_map[key] = color
        return color


## Matrix functions
def matrix_mult(a, b):
    out = ROOT.TMatrixD(4, 4)
    # Iterate over rows of `a` and columns of `b` to fill each entry in `out`
    for i in range(4):
        for j in range(4):
            # Calculate the dot product for each element in `out`
            out[i][j] = sum(a[i][k] * b[k][j] for k in range(4))
    return out


def calc_projection(i, j, matrix):
    vec = ROOT.TVector3(i - matrix[3][0], j - matrix[3][1], 0)
    transformed_vec = matrix * vec
    x, y, z = (
        transformed_vec.X() + matrix[0][3],
        transformed_vec.Y() + matrix[1][3],
        transformed_vec.Z() + matrix[2][3],
    )
    return (x, y, z)


def create_projection_matrix(width, height, box_min, box_max, projection="XY"):
    """
    Create a transformation matrix to map pixel coordinates (i, j) to a 3D space.

    Parameters:
    - width: int, the width of the 2D image in pixels.
    - height: int, the height of the 2D image in pixels.
    - box_min: tuple, (x_min, y_min, z_min) of the 3D bounding box.
    - box_max: tuple, (x_max, y_max, z_max) of the 3D bounding box.
    - projection: str, one of "XY", "XZ", "YZ", indicating the plane of the 2D image.

    Returns:
    - ROOT.TMatrixD, a 4x4 transformation matrix for the specified projection.
    """
    # Define scaling factors based on the box dimensions and image size
    dx = (box_max[0] - box_min[0]) / width
    dy = (box_max[1] - box_min[1]) / height
    dz = (box_max[2] - box_min[2]) / height

    # Initialize a 4x4 identity matrix
    matrix = ROOT.TMatrixD(4, 4)
    matrix.UnitMatrix()

    # Set up the matrix based on the selected projection
    if projection == "XY":
        matrix = ROOT.TMatrixD(4, 4)
        matrix.UnitMatrix()
        matrix[0][0] = dx
        matrix[1][1] = dy
        matrix[0][3] = box_min[0]  # Offset x
        matrix[1][3] = box_min[1]  # Offset y
        matrix[2][3] = box_min[2]  # Fixed z position
    elif projection == "XZ":
        rotation = ROOT.TMatrixD(4, 4)
        rotation.UnitMatrix()
        cos_theta = 0
        sin_theta = 1
        # We're "rotating" the y coordinate into the z one
        rotation[1][1] = cos_theta
        rotation[2][2] = cos_theta
        rotation[2][1] = sin_theta
        rotation[1][2] = -sin_theta
        scale = ROOT.TMatrixD(4, 4)
        scale.UnitMatrix()
        scale[0][0] = dx
        scale[1][1] = dz
        temp = matrix_mult(rotation, scale)
        matrix = matrix_mult(matrix, temp)
        matrix[0][3] = box_min[0]  # Offset x
        matrix[1][3] = box_min[1]  # Offset y
        matrix[2][3] = box_min[2]  # Fixed z position

    elif projection == "YZ":
        dy = (box_min[1] - box_max[1]) / height
        dz = (box_max[2] - box_min[2]) / width
        rotation = ROOT.TMatrixD(4, 4)
        rotation.UnitMatrix()
        cos_theta = 0
        sin_theta = 1
        # We're "rotating" the x coordinate into the z one
        rotation[0][0] = cos_theta
        rotation[2][2] = cos_theta
        rotation[2][0] = sin_theta
        rotation[0][2] = -sin_theta
        scale = ROOT.TMatrixD(4, 4)
        scale.UnitMatrix()
        scale[0][0] = dz
        scale[1][1] = dy  # dy is backwards
        temp = matrix_mult(rotation, scale)
        matrix = matrix_mult(matrix, temp)
        matrix[0][3] = box_min[0]  # Offset x
        matrix[1][3] = box_max[1]  # Offset y
        matrix[2][3] = box_min[2]  # Fixed z position
    else:
        raise ValueError("Invalid projection type. Choose from 'XY', 'XZ', or 'YZ'.")

    if VERBOSE:
        print(projection)
        print(matrix_to_string(matrix))
        print(box_min, box_max)
        for i in [0, width]:  # width//2,
            for j in [0, height]:  # height//2,
                test = calc_projection(i, j, matrix)
                print(f"{i},{j} ->\t{test}")

    return matrix


def matrix_to_string(matrix):
    out = "[\t"
    for i in range(4):
        temp = []
        for j in range(4):
            temp.append(f"{matrix[i][j]:8.1f}")
        out += ",\t".join(temp)
        if i != 3:
            out += "\n \t"
        else:
            out += "\t]"
    return out


def draw_image(geom, matrix, w, h, color_function):
    start_time = time.perf_counter()
    image = make_image(w, h)
    for i in range(w):
        for j in range(h):
            vec = ROOT.TVector3(i - matrix[3][0], j - matrix[3][1], 0)
            transformed_vec = matrix * vec
            x, y, z = (
                transformed_vec.X() + matrix[0][3],
                transformed_vec.Y() + matrix[1][3],
                transformed_vec.Z() + matrix[2][3],
            )

            node = geom.FindNode(x, y, z)
            if node == None:
                # print(f"None node at ({i}, {j}) ->\t({x:0.1f},{y:0.1f},{z:0.1f})")
                continue
            image.PutPixel(i, j, color_function(node))
    end_time = time.perf_counter()
    t = end_time - start_time
    time_per_pixel = t / float(w * h)
    print(
        f"time for {w}x{h} image was {t:0.2f}s, or {time_per_pixel*1000:0.3f}ms/pixel"
    )
    return image


def get_axis(matrix, w, h, projection):
    start = calc_projection(0, 0, matrix)
    end = calc_projection(w, h, matrix)
    understood_projection = False
    scale_factor = 0.01  # cm to m
    if projection == "XY":
        titlex = "X (m)"
        titley = "Y (m)"
        start_x = start[0] * scale_factor
        start_y = start[1] * scale_factor
        end_x = end[0] * scale_factor
        end_y = end[1] * scale_factor
        understood_projection = True
    if projection == "XZ":
        titlex = "X (m)"
        titley = "Z (m)"
        start_x = start[0] * scale_factor
        start_y = start[2] * scale_factor
        end_x = end[0] * scale_factor
        end_y = end[2] * scale_factor
        understood_projection = True
    if projection == "YZ":
        titlex = "Z (m)"
        titley = "Y (m)"
        start_x = start[2] * scale_factor
        start_y = end[1] * scale_factor
        end_x = end[2] * scale_factor
        end_y = start[1] * scale_factor
        understood_projection = True
    if not understood_projection:
        raise NotImplementedError(f"Didn't understand projection {projection}")
    nbins = 1000
    if VERBOSE:
        print(
            f"size: {w}x{h}\tx axis: {start_x:0.2f} to {end_x:0.2f},\ty axis: {start_y:0.2f} to {end_y:0.2f}"
        )
    if projection == "XZ":
        # TODO TGaxis isn't happy with cases where end_y < start_y but end_y is not negative
        outy = ROOT.TGaxis(1, 1, 1, 0, start_y, end_y, 510, "")
        outy.SetLabelOffset(0.075)
        outy.SetTitleOffset(-1.95)
        outy.SetTitle(titley)
    else:
        outy = ROOT.TGaxis(0, 0, 0, 1, start_y, end_y, 510, "")
        outy.SetTitle(titley)
        outy.SetTitleOffset(1.25)

    outx = ROOT.TGaxis(0, 0, 1, 0, start_x, end_x, 510, "")
    outx.SetTitle(titlex)
    return outx, outy


# Conversion factors to centimeters
UNIT_CONVERSIONS = {
    "m": 100.0,  # 1 meter = 100 cm
    "cm": 1.0,  # 1 cm = 1 cm
    "dm": 10.0,  # 1 dm = 10 cm
    "mm": 0.1,  # 1 mm = 0.1 cm
    "km": 100000.0,  # 1 km = 100000 cm
    "in": 2.54,  # 1 inch = 2.54 cm
    "ft": 30.48,  # 1 foot = 30.48 cm
    "yd": 91.44,  # 1 yard = 91.44 cm
    "mi": 160934.0,  # 1 mile = 160934 cm
}


def unit_float(value):
    """Parses a string like '1m', '100cm', etc., into a float in centimeters."""
    match = re.fullmatch(r"t?(-?\d*\.?\d+)\s*(\w*)", value.strip())
    if not match:
        raise argparse.ArgumentTypeError(f"Invalid unit format: {value}")

    number, unit = match.groups()
    number = float(number)

    if unit and unit not in UNIT_CONVERSIONS:
        raise argparse.ArgumentTypeError(f"Unknown unit: {unit}")

    return number * UNIT_CONVERSIONS.get(
        unit, 1.0
    )  # Defaults to cm if no unit is provided


def get_default_view(args, view_name, w, h, translate):
    matrix = None
    projection = None
    ratio = h / float(w)
    m = 100
    if view_name == "sand_top":
        y_mid = -250
        box_min = (-450 * ratio, y_mid + translate, 1950)
        box_max = (450 * ratio, y_mid + translate, 2850)
        matrix = create_projection_matrix(w, h, box_min, box_max, "XZ")
        projection = "XZ"
    if view_name == "sand_side":
        box_min = (translate, -750 * ratio, 1950)
        box_max = (translate, 150 * ratio, 2850)
        matrix = create_projection_matrix(w, h, box_min, box_max, "YZ")
        projection = "YZ"
    if view_name == "lar_top":
        box_min = (-800 * ratio, translate, -200)
        box_max = (800 * ratio, translate, 1400)
        matrix = create_projection_matrix(w, h, box_min, box_max, "XZ")
        projection = "XZ"
    if view_name == "lar_side":
        box_min = (translate, -800 * ratio, 0)
        box_max = (translate, 400 * ratio, 1200)
        matrix = create_projection_matrix(w, h, box_min, box_max, "YZ")
        projection = "YZ"
    if view_name == "tms_top":
        box_min = (-400, translate, 1100)
        box_max = (400, translate, 1900)
        matrix = create_projection_matrix(w, h, box_min, box_max, "XZ")
        projection = "XZ"
    if view_name == "tms_side":
        box_min = (translate, -600 * ratio, 1100)
        box_max = (translate, 200 * ratio, 1900)
        matrix = create_projection_matrix(w, h, box_min, box_max, "YZ")
        projection = "YZ"
    if view_name == "rock_side":
        box_min = (-180 * m * ratio, 0, -300 * m)
        box_max = (180 * m * ratio, 0, 60 * m)
        matrix = create_projection_matrix(w, h, box_min, box_max, "XZ")
        projection = "XZ"
    if view_name == "rock_top":
        box_min = (0, -180 * m * ratio, -300 * m)
        box_max = (0, 180 * m * ratio, 60 * m)
        matrix = create_projection_matrix(w, h, box_min, box_max, "YZ")
        projection = "YZ"
    if view_name == "xz":
        box_min = (-35 * m * ratio, 0, -10 * m)
        box_max = (10 * m * ratio, 0, 35 * m)
        matrix = create_projection_matrix(w, h, box_min, box_max, "XZ")
        projection = "XZ"
    if view_name == "xz_wide":
        box_min = (-200 * m * ratio, 0, -200 * m)
        box_max = (200 * m * ratio, 0, 200 * m)
        matrix = create_projection_matrix(w, h, box_min, box_max, "XZ")
        projection = "XZ"
    if view_name == "yz":
        box_min = (0, -15 * m * ratio, -5 * m)
        box_max = (0, 25 * m * ratio, 35 * m)
        matrix = create_projection_matrix(w, h, box_min, box_max, "YZ")
        projection = "YZ"
    if view_name == "yz_wide":
        box_min = (0, -110 * m * ratio, -110 * m)
        box_max = (0, 110 * m * ratio, 110 * m)
        matrix = create_projection_matrix(w, h, box_min, box_max, "YZ")
        projection = "YZ"
    if view_name == "xz_zoom":
        box_min = (-21 * m * ratio, 0, -1 * m)
        box_max = (9 * m * ratio, 0, 29 * m)
        matrix = create_projection_matrix(w, h, box_min, box_max, "XZ")
        projection = "XZ"
    if view_name == "yz_zoom":
        box_min = (0, -10 * m * ratio, -1 * m)
        box_max = (0, 18 * m * ratio, 29 * m)
        matrix = create_projection_matrix(w, h, box_min, box_max, "YZ")
        projection = "YZ"
    if matrix == None:
        raise ValueError(f"Did not understand view named {view_name}")
    args.matrix = matrix
    args.projection = projection


def get_color_function(color_function_name, exclude_clear):
    out = None
    if color_function_name == "scintillator":
        out = lambda x: color_function(x, "scintillator", exclude_clear)
    if color_function_name == "material":
        out = lambda x: color_function(x, "material", exclude_clear)
    if color_function_name == "density_bw":
        out = lambda x: color_function(x, "density_bw", exclude_clear)
    if color_function_name == "density":
        out = lambda x: color_function(x, "density", exclude_clear)
    if color_function_name == "random":
        out = lambda x: color_function(x, "random", exclude_clear)

    if out == None:
        raise ValueError(
            f"Did not understand color function named {color_function_name}"
        )
    return out


def parse_args():
    global VERBOSE
    parser = argparse.ArgumentParser(
        description="Process geometry files with optional transformations and visualization settings."
    )

    parser.add_argument(
        "--filename", required=True, help="Input geometry filename (required)."
    )
    parser.add_argument(
        "--outdir", default="output", help="Output directory (defaults to 'output')."
    )
    parser.add_argument(
        "--outfilename",
        help="Custom output filename (defaults to view_name.png or custom_matrix.png).",
    )
    parser.add_argument(
        "--view",
        default="xz",
        help="Draw built-in view (xz, xz_wide, xz_zoom, yz, yz_wide, yz_zoom, lar_top, lar_side, tms_top, tms_side, sand_top, sand_side, rock_top, rock_side)",
    )
    parser.add_argument(
        "--color",
        default="density",
        help="Color function to use. (density, density_bw, random, material, scintillator)",
    )
    parser.add_argument(
        "--draw_air",
        action="store_true",
        help="Whether to draw air/vac. Normally white",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Draw 1/4th size preview image (16x faster)",
    )
    parser.add_argument("--height", type=int, default=800, help="Image height")
    parser.add_argument("--width", "-w", type=int, default=1000, help="Image width")
    parser.add_argument("--scale", type=float, default=1, help="Scale image")
    parser.add_argument(
        "--axis",
        action="store_true",
        help="Whether to draw the axis (experimental, will make image more square)",
    )
    parser.add_argument(
        "--translate",
        "-t",
        type=unit_float,
        default=0,
        metavar="VALUE",
        help="Translate the 3rd axis by this amount. Useful for making slices. (e.g., '1m', '100cm', 't-0.5mm'). Defaults to cm if no unit is given.",
    )
    # Parsing a 4x4 matrix as a space-separated string of 16 numbers
    parser.add_argument(
        "--matrix",
        type=str,
        help="Custom 4x4 transformation matrix (16 space-separated values).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print interpreted matrix plus some test values to check",
    )

    args = parser.parse_args()

    if args.verbose:
        VERBOSE = True

    if args.axis:
        # Unfortunately axis is slightly wrong unless height == width
        # Todo fix issue
        dimension = max(args.height, args.width)
        args.height = dimension
        args.width = dimension
        print(
            f"********\nWarning: --axis option is still experimental.\n"
            f"Setting height and width to the same value of {dimension}.\n"
            f"Otherwise the axis can be off sometimes\n************"
        )

    # Decide on the final image size
    if args.preview:
        args.scale *= 0.25
    args.height = int(args.height * args.scale)
    args.width = int(args.width * args.scale)

    # Process the matrix if provided
    matrix = None
    if args.matrix:
        values = list(map(unit_float, args.matrix.split()))
        if len(values) != 16:
            raise ValueError("Matrix must contain exactly 16 values.")
        args.matrix = np.array(values).reshape(4, 4)
        args.projection = "AB"
    else:
        # Use a default view instead
        get_default_view(args, args.view, args.width, args.height, args.translate)

    # Set default output filename
    if not args.outfilename:
        args.outfilename = os.path.join(
            args.outdir, (args.view if args.view else "custom_matrix") + ".png"
        )
    else:
        if not (".png" in args.outfilename or ".jpg" in args.outfilename):
            raise ValueError(f"outfilename is missing file type. {args.outfilename}")
        args.outfilename = os.path.join(args.outdir, args.outfilename)

    # Get the color function
    if args.color:
        args.color_function = get_color_function(args.color, not args.draw_air)

    return args


if __name__ == "__main__":
    # Parse the args
    args = parse_args()
    # Load the gdml
    geom = load_geometry(args.filename)
    # Make the output dir
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
    assert os.path.exists(args.outdir), f"Failed to make outdir {args.outdir}"

    # Make the image
    image = make_image(args.width, args.height)
    image = draw_image(geom, args.matrix, args.width, args.height, args.color_function)
    if args.axis:
        margin_top = 0.03
        margin_right = 0.04
        margin_left = 0.12
        margin_bottom = 0.085
        # TODO this is part of the XZ kludge in get_axis
        if args.projection == "XZ":
            margin_left = 0.04
            margin_right = 0.15
        # This is kludge. Otherwise axis comes out slightly too wide in x axis assuming height == width
        kludge_margin = -0.02
        remaining_space_x = 1 - (margin_right + margin_left + kludge_margin)
        remaining_space_y = 1 - (margin_top + margin_bottom)
        aspect_ratio = args.width / float(args.height)
        H = max(1000, args.height)
        W = int(H * aspect_ratio * remaining_space_y / remaining_space_x)
        canvas = ROOT.TCanvas("c1", "c1", W, H)
        canvas.SetTopMargin(margin_top)
        canvas.SetRightMargin(margin_right)
        canvas.SetBottomMargin(margin_bottom)
        canvas.SetLeftMargin(margin_left)
        axis_x, axis_y = get_axis(args.matrix, args.width, args.height, args.projection)
        image.Draw()
        axis_x.Draw()
        axis_y.Draw()
        canvas.Print(args.outfilename)
    else:
        image.WriteImage(args.outfilename)
