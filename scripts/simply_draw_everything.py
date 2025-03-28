import os
import collections
import math

RAD = math.pi / 180.0
M = 0.01  # m per cm

import ROOT

ROOT.gROOT.SetBatch(True)

import dunestyle.root as dunestyle

ROOT.gStyle.SetPaintTextFormat(".2f")

import sys


def get_subdir_and_name(hist_name):
    subdir = ""
    name = hist_name.strip()
    split = name.split("__")
    subdir = os.path.join(*split[:-1])
    name = split[-1]
    print(hist_name, subdir, name)
    return subdir, name


line_buffer = []


def draw_line(start, stop, color=ROOT.kRed, line_style=2, line_width=2):
    line = ROOT.TLine(*start, *stop)
    line.SetLineColor(color)
    line.SetLineStyle(line_style)
    line.SetLineWidth(line_width)
    line.Draw()
    line_buffer.append(line)


def make_line(box, ab, d, start):
    default_value = 1 if start else 0
    opposite_value = 0 if start else 1
    fa1 = default_value
    fb1 = default_value
    fa2 = default_value
    fb2 = default_value
    if ab == "XY":
        a = 0
        b = 1
        if d == "X":
            fa2 = opposite_value
        if d == "Y":
            fb2 = opposite_value
    if ab == "XZ":
        a = 0
        b = 2
        if d == "X":
            fa2 = opposite_value
        if d == "Z":
            fb2 = opposite_value
    if ab == "YZ":
        a = 1
        b = 2
        if d == "Y":
            fa2 = opposite_value
        if d == "Z":
            fb2 = opposite_value
    if ab == "YX":
        a = 1
        b = 0
        if d == "X":
            fb2 = opposite_value
        if d == "Y":
            fa2 = opposite_value
    if ab == "ZX":
        a = 2
        b = 0
        if d == "X":
            fb2 = opposite_value
        if d == "Z":
            fa2 = opposite_value
    if ab == "ZY":
        a = 2
        b = 1
        if d == "Y":
            fb2 = opposite_value
        if d == "Z":
            fa2 = opposite_value
    assert not (fa1 == fa2 and fb1 == fb2), "Didn't get fa nor fb changing"
    return ((box[fa1][a], box[fb1][b]), (box[fa2][a], box[fb2][b]))


def draw_flux_window(max_z, image_name):
    lines = None

    # Define the flux window
    window_start = (-6, -15, -1)
    window_end = (6, 15, -1)
    beam_angle = -3  # deg
    beam_angle_rad = beam_angle * RAD  # radians
    dy = math.tan(beam_angle_rad)

    # Define the rockbox in cm, (start)(end), x,y,z
    rockbox = [
        (-4896.4 * M, -661.473 * M, -30.54 * M),
        (621.1 * M, 1781.527 * M, 2954.9 * M),
    ]
    add_rockbox = True

    # Now make the corners of the flux window
    top_left = (window_end[0], window_end[1])
    top_right = (window_start[0], window_end[1])
    bottom_left = (window_end[0], window_start[1])
    bottom_right = (window_start[0], window_start[1])
    forward_top = (window_end[2], window_end[1])
    forward_bottom = (window_end[2], window_start[1])
    forward_left = (window_end[2], window_end[0])
    forward_right = (window_end[2], window_start[0])

    # Now group the lines
    top = (top_left, top_right)
    bottom = (bottom_left, bottom_right)
    left = (top_left, bottom_left)
    right = (top_right, bottom_right)
    forward_y = (forward_top, forward_bottom)
    forward_x = (forward_left, forward_right)

    change_color = None
    if "_xy" in image_name:
        lines = [top, left, bottom, right]
        if add_rockbox:
            change_color = len(lines)
            lines.append(make_line(rockbox, "XY", "X", False))
            lines.append(make_line(rockbox, "XY", "X", True))
            lines.append(make_line(rockbox, "XY", "Y", False))
            lines.append(make_line(rockbox, "XY", "Y", True))
    if "_yz" in image_name:
        top_end_y = window_end[1] + dy * (max_z - window_start[2])
        bottom_end_y = window_start[1] + dy * (max_z - window_start[2])
        top_line = (forward_top, (max_z, top_end_y))
        bottom_line = (forward_bottom, (max_z, bottom_end_y))
        lines = [forward_y, top_line, bottom_line]
        if add_rockbox:
            change_color = len(lines)
            lines.append(make_line(rockbox, "ZY", "Y", False))
            lines.append(make_line(rockbox, "ZY", "Y", True))
            lines.append(make_line(rockbox, "ZY", "Z", False))
            lines.append(make_line(rockbox, "ZY", "Z", True))
    if "_xz" in image_name:
        right_line_x = window_start[0]
        left_line_x = window_end[0]
        right_line = (forward_right, (max_z, right_line_x))
        left_line = (forward_left, (max_z, left_line_x))
        lines = [forward_x, right_line, left_line]
        if add_rockbox:
            change_color = len(lines)
            lines.append(make_line(rockbox, "ZX", "X", False))
            lines.append(make_line(rockbox, "ZX", "X", True))
            lines.append(make_line(rockbox, "ZX", "Z", False))
            lines.append(make_line(rockbox, "ZX", "Z", True))
    for num, line in enumerate(lines):
        color = ROOT.kRed
        if change_color != None and num >= change_color:
            color = ROOT.kCyan
        draw_line(*line, color=color)


# TODO erase the output dir subdirs (except event displays) because sometimes the hists don't exist if they weren't filled at least once
def draw_histograms(input_file):
    # Open the input ROOT file
    root_file = ROOT.TFile.Open(input_file)

    # Create a directory to save images
    output_dir = os.path.splitext(input_file)[0] + "_images"
    os.makedirs(output_dir, exist_ok=True)

    canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)

    # Save special plots here
    recoeff_plots_numerators = dict()
    recoeff_plots_denominators = dict()
    stack_plots = collections.defaultdict(dict)

    # Loop over all keys in the ROOT file
    for key in root_file.GetListOfKeys():
        obj = key.ReadObj()
        output_subdir = output_dir
        name = obj.GetName()

        subdir, image_name = get_subdir_and_name(name)
        output_subdir = os.path.join(output_dir, subdir)

        if "width" in name:
            obj.Scale(1, "width")

        # Can add reco eff
        reco_eff = False
        if "numerator" in name or "denominator" in name:
            reco_eff = True
        stack = False
        if "stack" in name:
            stack = True
        if reco_eff or stack:
            output_subdir = os.path.join(output_subdir, "additional_plots")
        os.makedirs(output_subdir, exist_ok=True)
        if isinstance(obj, ROOT.TH2):
            # For 2D histograms, draw with "colz" option and save as png
            obj.GetYaxis().SetTitleOffset(1.4)
            obj.GetZaxis().SetTitleOffset(0.5)
            normalized = "normalized" in image_name
            if normalized and obj.GetXaxis().GetNbins() < 20:
                obj.SetMarkerColor(ROOT.kRed + 1)
                obj.GetZaxis().SetRangeUser(0.001, obj.GetMaximum())
                obj.Draw("colz text")
            else:
                obj.Draw("colz")
            if "_xy" in image_name or "_xz" in image_name or "_yz" in image_name:
                max_z = obj.GetXaxis().GetXmax()
                draw_flux_window(max_z, image_name)
            dunestyle.Simulation()
            print(f"{obj.GetName()} integral: {obj.Integral()}")
            canvas.Print(os.path.join(output_subdir, image_name + ".png"))
        elif isinstance(obj, ROOT.TH1):
            # For 1D histograms, draw and save as png
            top = obj.GetMaximum() * 1.2
            obj.GetYaxis().SetRangeUser(0, top)
            obj.GetYaxis().SetTitleOffset(1.4)
            obj.SetLineColor(ROOT.kBlack)
            if "(m)" in obj.GetXaxis().GetTitle():
                obj.GetYaxis().SetTitle("N Vertices")
            obj.Draw()
            dunestyle.Simulation()
            # print(f"{obj.GetName()} integral: {obj.Integral()}")
            canvas.Print(os.path.join(output_subdir, image_name + ".png"))
        if reco_eff:
            key = name.replace("_numerator", "").replace("_denominator", "")
            if "numerator" in name:
                recoeff_plots_numerators[key] = obj
            if "denominator" in name:
                recoeff_plots_denominators[key] = obj
        if stack:
            if "_stack_" in name:
                split_stack = name.split("_stack_")
            if "_nostack_" in name:
                split_stack = name.split("_nostack_")
            stack_key = split_stack[0]
            stack_plots[stack_key][split_stack[1]] = obj
            # stack_plots[stack_key + "_log"][split_stack[1]] = obj

    # Draw the stacks
    # First define some unique colors and line styles
    colors = [
        ROOT.kBlue,
        ROOT.kRed,
        ROOT.kGreen,
        ROOT.kMagenta,
        ROOT.kBlack,
        ROOT.kCyan,
    ]
    line_styles = [1, 2, 7, 9]
    # Loop over each stack
    for name, hist_and_name in stack_plots.items():
        index = 0
        first_hist = None
        first_hist_name = None
        ymax = 0
        hist_stack = ROOT.THStack()
        leg = ROOT.TLegend(0.2, 0.67, 0.8, 0.82)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.SetNColumns(2)

        log = False
        if "log" in name:
            log = True
        if log:
            canvas.SetLogy(True)
        else:
            canvas.SetLogy(False)

        area_norm = False
        if "area_norm" in name:
            area_norm = True

        headroom = 1.4  # 1.3
        if log:
            headroom = 5  # 3

        l = list(hist_and_name.items())
        l.sort()
        for item_name, hist in l:
            if area_norm:
                integral = hist.Integral()
                if integral != 0:
                    hist.Scale(1 / integral)
            hist.SetLineColor(colors[index % len(colors)])
            hist.SetLineStyle(line_styles[index % len(line_styles)])
            if index == 0:
                first_hist = hist
                first_hist_name = item_name
            ymax = max(ymax, hist.GetMaximum())
            hist_stack.Add(hist)
            name_for_legend = item_name
            if ":" in hist.GetTitle():
                name_for_legend = hist.GetTitle().split(":")[1].strip()
            leg.AddEntry(hist, name_for_legend, "lep")
            index += 1

        # Use the first hist to set the title and stuff
        # Draw first to make the underlying histogram
        hist_stack.Draw(
            "hist nostack" if "nostack" in first_hist.GetName() else "hist stack"
        )
        if first_hist != None:
            hist_stack.SetTitle(
                first_hist.GetTitle().replace(f": {first_hist_name}", "").split(":")[0]
            )
            hist_stack.GetXaxis().SetTitle(first_hist.GetXaxis().GetTitle())
            hist_stack.GetYaxis().SetTitle(first_hist.GetYaxis().GetTitle())

        # Canvas gets mad if min is set to zero because log(0) is issue
        ymin = 0
        if log:
            ymin = 10
        for hist in hist_and_name.values():
            hist.GetYaxis().SetRangeUser(ymin, ymax * headroom)

        # Now finally draw and save
        hist_stack.Draw(
            "hist nostack" if "nostack" in first_hist.GetName() else "hist stack"
        )
        leg.Draw()
        dunestyle.Simulation()
        subdir, image_name = get_subdir_and_name(name)
        output_subdir = os.path.join(output_dir, subdir)
        outfilename = os.path.join(output_subdir, image_name + ".png")
        print(f"Saving in {outfilename}")
        canvas.Print(outfilename)

    # Turn off log y if it's already on
    canvas.SetLogy(False)

    # Draw reco eff
    all_names = set(recoeff_plots_numerators.keys()) & set(
        recoeff_plots_denominators.keys()
    )
    for name in all_names:
        # First confirm we have both numerator and denominator
        error = False
        if name not in recoeff_plots_numerators:
            print(f"Didn't find {name} in {recoeff_plots_numerators}")
            error = True
        if name not in recoeff_plots_denominators:
            print(f"Didn't find {name} in {recoeff_plots_denominators}")
            error = True
        # Skip gracefully it not
        if error:
            print(f"Had one or more errors, skipping {name}")
            continue

        # Get the numerator and denominator, and then divide
        numerator = recoeff_plots_numerators[name]
        denominator = recoeff_plots_denominators[name]
        newtitle = numerator.GetTitle()
        newtitle = newtitle.replace(": Numerator", "").strip()
        numerator.SetTitle(newtitle)
        numerator.Divide(denominator)
        numerator.Scale(1.0)  # resets the axis

        # Now make it look nice, and draw
        max_y = numerator.GetMaximum()
        numerator.GetYaxis().SetRangeUser(0, 1.2 * max_y)
        numerator.GetYaxis().SetTitle("Probability")
        xmin = numerator.GetXaxis().GetXmin()
        xmax = numerator.GetXaxis().GetXmax()
        numerator.Draw("hist")
        dunestyle.Simulation()
        # Make dotted line
        # line = ROOT.TLine(xmin, 1, xmax, 1)
        # line.SetLineStyle(2)
        # line.Draw()

        # Get an output name and subdir, and save
        name = numerator.GetName()
        name = name.replace("_numerator", "")
        subdir, image_name = get_subdir_and_name(name)
        output_subdir = os.path.join(output_dir, subdir)
        canvas.Print(os.path.join(output_subdir, image_name + ".png"))

    # Close the input ROOT file
    root_file.Close()


if __name__ == "__main__":
    # Check if input file is provided as argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_root_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print("Error: Input file does not exist!")
        sys.exit(1)

    # Initialize ROOT
    ROOT.gROOT.SetBatch(True)  # Prevent ROOT from trying to open X11 windows
    ROOT.gStyle.SetOptStat(0)  # Hide statistics box in histograms

    # Call function to draw histograms
    draw_histograms(input_file)
