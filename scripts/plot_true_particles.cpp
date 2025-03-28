#include <filesystem>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

// Root specific
#include <TChain.h>
#include <TFile.h>
#include <TGeoManager.h>
#include <TGeoNode.h>
#include <TH1D.h>
#include <TH2D.h>
#include <TTree.h>
#include <TVector3.h>

// EDepSim includes
#include "EDepSim/TG4Event.h"
#include "EDepSim/TG4PrimaryVertex.h"

// dune specific
#include <DUNEStyle.h>

/*
Samples:
rock_muons - Interactions from any particle (ie primarily rock muons)
secondary_muons - Interactions from secondary muons only
not_rock_muons - Interactions from any particle other than a primary
                 rock muon (ie sample includes secondary muons)
nonmuon_sample - Interactions from any particle other than muon (primary nor
secondary)
*/

const double pot_per_file = 7.5e12;
double pot_for_full_sample = -9999;

const double M = 1e-3;   // m per mm
const double GEV = 1e-3; // GeV per MeV

// All units in meters
const TVector3 interest_region_START(-3.47848, -2.16671, 4.17924);
const TVector3 interest_region_END(3.47848, 0.829282, 9.13588);
const TVector3 TMS_ACTIVE_START(-3.3000, -2.8500, 11.3620);
const TVector3 TMS_ACTIVE_END(3.3000, 0.1600, 18.3140);
const TVector3 ND_CAVE_START(-5.0, -6.0, 0.0);
const TVector3 ND_CAVE_END(5.0, 4.0, 30.0);
const double dx = ND_CAVE_END.X() - ND_CAVE_START.X();
const double dy = ND_CAVE_END.Y() - ND_CAVE_START.Y();
const double dz = ND_CAVE_END.Z() - ND_CAVE_START.Z();
const double ce = 0.25; // cave expansion percentage
const TVector3 SAND_START(-3.0, -6.0, 20.0);
const TVector3 SAND_END(3.0, 0.1600, 30.0);

// This is the genie box for non-muon sample
const TVector3 GENIE_FIDUCIAL_START(-25, -10, -8);
const TVector3 GENIE_FIDUCIAL_END(6, 18, 32);

const double MASS_MUON = 0.105658;    // GeV
const double MASS_NEUTRON = 0.939565; // GeV

// When calculating probability, we don't want to include the whole region
// because that decreases the proability.
// So if outside this region, it's not included
const TVector3 OFFAXIS_REGION_START(-30.0, -30.0, -40.0);
const TVector3 OFFAXIS_REGION_END(30.0, 30.0, 40.0);

const TVector3 ZOOMED_REGION_START(-50.0, -20.0, -50.0);
const TVector3 ZOOMED_REGION_END(25.0, 25.0, 40.0);

template <typename... Args>
std::string string_format(const std::string &format, Args... args) {
  int size_s = std::snprintf(nullptr, 0, format.c_str(), args...) +
               1; // Extra space for '\0'
  if (size_s <= 0) {
    throw std::runtime_error("Error during formatting.");
  }
  auto size = static_cast<size_t>(size_s);
  std::unique_ptr<char[]> buf(new char[size]);
  std::snprintf(buf.get(), size, format.c_str(), args...);
  return std::string(buf.get(),
                     buf.get() + size - 1); // We don't want the '\0' inside
}

std::string getExecutableName(const char *arg) {
  std::string executableName = arg; // Convert to std::string
  size_t lastSlash =
      executableName.find_last_of("/\\"); // Find last occurrence of '/' or '\'
  if (lastSlash != std::string::npos) {
    executableName = executableName.substr(
        lastSlash + 1); // Extract substring after the last slash
  }
  size_t extensionPos =
      executableName.find_last_of('.'); // Find last occurrence of '.'
  if (extensionPos != std::string::npos) {
    executableName = executableName.substr(0, extensionPos); // Remove extension
  }
  return executableName;
}

bool createDirectory(const std::string &path) {
  try {
    // Create directory and its parents if they don't exist
    std::filesystem::create_directories(path);
    std::cout << "Created directory: " << path << std::endl;
    return true;
  } catch (const std::exception &e) {
    std::cerr << "Fatal error creating directory: " << e.what() << std::endl;
    exit(1);
  }
}

std::string getOutputFilename(const std::string &inputFilename) {
  // Find the position of the last occurrence of '/' in the input filename
  size_t pos = inputFilename.find_last_of('/');
  // Extract the filename without the directory structure
  std::string filename = (pos != std::string::npos)
                             ? inputFilename.substr(pos + 1)
                             : inputFilename;
  // Add .root to end
  if (filename.find(".root") == std::string::npos)
    filename += ".root";
  return filename;
}

std::string getOutputDirname(const std::string &outputFilename) {
  // Find the position of the last occurrence of '.' in the output filename
  size_t pos = outputFilename.find_last_of('.');
  std::string filename = (pos != std::string::npos)
                             ? outputFilename.substr(0, pos)
                             : outputFilename;
  return filename + "_images/";
}

std::unordered_map<std::string, TH1 *> mapForGetHist;

void NormalizeHists() {
  const double pot_per_spill = 7.5e13;
  const double per_spill_normalization = pot_per_spill / pot_for_full_sample;
  // Could check here for certain hists and automatically make copies with
  // column norm for example
  for (auto &hist : mapForGetHist) {
    if (hist.first.find("normalize_to_one") != std::string::npos) {
      // Normalize max to 1
      hist.second->Scale(1 / hist.second->GetMaximum());
    }
    if (hist.first.find("normalize_to_probability") != std::string::npos) {
      // Normalize to 1, as in a probability for example
      hist.second->Scale(1 / hist.second->Integral());
    }
    if (hist.first.find("normalize_per_spill") != std::string::npos) {
      // Normalize to 1, as in a probability for example
      hist.second->Scale(per_spill_normalization);
    }
  }
}

std::unordered_map<std::string, std::tuple<std::string, int, double, double>>
    registeredAxes;
inline void
RegisterAxis(std::string axis_name,
             std::tuple<std::string, int, double, double> axis_tuple) {
  // Only register the first time
  if (registeredAxes.find(axis_name) == registeredAxes.end()) {
    registeredAxes[axis_name] = axis_tuple;
  }
}

class AutoregisterAxis {
public:
  AutoregisterAxis(const std::string &name,
                   std::tuple<std::string, int, double, double> axis_tuple) {
    RegisterAxis(name, axis_tuple);
  }
};

#define REGISTER_AXIS(name, axis_tuple)                                        \
  static AutoregisterAxis reg_axis_##name(#name, axis_tuple)

int PDGtoIndex(int pdgCode) {
  // const char *pdg[] = {"e^{+/-}, #gamma", "#mu^{-}", "#mu^{+}", "#pi^{+}",
  // "#pi^{-}", "K", "n", "p", "other", "unknown"}; Unknown is -999999999
  if (pdgCode < -999999990)
    return 9;
  switch (pdgCode) {
  case 11:
    return 0; // e-
  case -11:
    return 0; // e+
  case 22:
    return 0; // gamma
  case 13:
    return 1; // mu-
  case -13:
    return 2; // mu+
  case 211:
    return 3; // pi+
  case -211:
    return 4; // pi-
  case 321:
    return 5; // K+
  case -321:
    return 5; // K-
  case 310:
    return 5; // K0
  case 130:
    return 5; // K0_L
  case 311:
    return 5; // K0_S
  case 2112:
    return 6; // Neutron
  case 2212:
    return 7; // Proton
  case -2212:
    return 7; // anti-Proton
  default:
    return 8; // other
  }
}

bool IsMuon(int pdg) {
  bool out = false;
  if (pdg == 1)
    out = true;
  if (pdg == 2)
    out = true;
  return out;
}

bool IsMuonPdg(int pdg) {
  bool out = false;
  if (std::abs(pdg) == 13)
    out = true;
  return out;
}

bool IsNeutron(int pdg) {
  bool out = false;
  if (pdg == 6)
    out = true;
  return out;
}

bool IsProton(int pdg) {
  bool out = false;
  if (pdg == 7)
    out = true;
  return out;
}

bool IsPion(int pdg) {
  bool out = false;
  if (pdg == 3)
    out = true;
  if (pdg == 4)
    out = true;
  return out;
}

std::tuple<std::string, int, double, double> GetBinning(std::string axis_name) {
  if (axis_name == "pdg")
    return std::make_tuple("Particle", 10, -0.5, 9.5);

  // Allow for registered axis so we don't need to add them away from where
  // they're used
  if (registeredAxes.find(axis_name) != registeredAxes.end())
    return registeredAxes[axis_name];

  std::cerr << "Fatal: Add axis to GetBinning. Did not understand axis name "
            << axis_name << std::endl;
  throw std::runtime_error("Unable to understand axis name");
}

// double muon_ke_bins[] = {0.0, 0.25, 0.5,
// 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.5, 4.0, 4.5, 5.0};
// int n_muon_ke_bins = sizeof(muon_ke_bins) / sizeof(double) - 1;
std::tuple<bool, std::string, int, double *>
GetComplexBinning(std::string axis_name) {
  // if (axis_name == "ke_tms_enter") return std::make_tuple(true, "True Muon KE
  // Entering TMS (GeV);N Muons / GeV", n_muon_ke_bins, muon_ke_bins);
  if (axis_name == "") {
  }
  return std::make_tuple(false, "", 0, (double *)NULL);
}

void AdjustAxis(TH1 *hist, std::string xaxis, std::string yaxis = "",
                std::string zaxis = "") {
  if (xaxis == "pdg") {
    const char *pdg[] = {"e^{+/-}, #gamma", "#mu^{-}", "#mu^{+}", "#pi^{+}",
                         "#pi^{-}",         "K",       "n",       "p",
                         "other",           "unknown"};
    const int npdg = sizeof(pdg) / sizeof(pdg[0]);
    hist->SetNdivisions(npdg);
    for (int ib = 0; ib < npdg; ib++) {
      hist->GetXaxis()->ChangeLabel(ib + 1, -1, -1, -1, -1, -1, pdg[ib]);
    }
  }
  if (yaxis != "" || zaxis != "") {
  }
}

TH1 *MakeHist(std::string directory_and_name, std::string title,
              std::string xaxis, std::string yaxis = "",
              std::string zaxis = "") {
  if (zaxis != "") {
    // 3d hist case
    throw std::runtime_error("3d hists are not implemented yet");
  } else if (yaxis != "") {
    // 2d hist case
    TH2D *out;

    std::string xaxis_title;
    int xaxis_nbins;
    double *xaxis_bins;
    bool has_complex_binning_x;
    std::tie(has_complex_binning_x, xaxis_title, xaxis_nbins, xaxis_bins) =
        GetComplexBinning(xaxis);

    std::string yaxis_title;
    int yaxis_nbins;
    double *yaxis_bins;
    bool has_complex_binning_y;
    std::tie(has_complex_binning_y, yaxis_title, yaxis_nbins, yaxis_bins) =
        GetComplexBinning(yaxis);
    // Can't do one and not the other, but could manually create the binning if
    // we wanted
    if (has_complex_binning_y != has_complex_binning_x)
      throw std::runtime_error(
          "2d hists have to use complex y and x bins simultaneously");
    if (has_complex_binning_x) {
      auto complete_title = title + ";" + xaxis_title + ";" + yaxis_title;
      out = new TH2D(directory_and_name.c_str(), complete_title.c_str(),
                     xaxis_nbins, xaxis_bins, yaxis_nbins, yaxis_bins);
    } else {
      double xaxis_start;
      double xaxis_end;
      std::tie(xaxis_title, xaxis_nbins, xaxis_start, xaxis_end) =
          GetBinning(xaxis);

      double yaxis_start;
      double yaxis_end;
      std::tie(yaxis_title, yaxis_nbins, yaxis_start, yaxis_end) =
          GetBinning(yaxis);
      auto complete_title = title + ";" + xaxis_title + ";" + yaxis_title;
      out = new TH2D(directory_and_name.c_str(), complete_title.c_str(),
                     xaxis_nbins, xaxis_start, xaxis_end, yaxis_nbins,
                     yaxis_start, yaxis_end);
    }
    // Add special naming here
    AdjustAxis(out, xaxis, yaxis);
    return out;
  } else {
    // 1d hist case
    TH1D *out;
    std::string xaxis_title;
    int xaxis_nbins;
    double *xaxis_bins;
    bool has_complex_binning;
    std::tie(has_complex_binning, xaxis_title, xaxis_nbins, xaxis_bins) =
        GetComplexBinning(xaxis);
    if (has_complex_binning) {

      auto complete_title = title + ";" + xaxis_title;
      out = new TH1D(directory_and_name.c_str(), complete_title.c_str(),
                     xaxis_nbins, xaxis_bins);
    } else {
      double xaxis_start;
      double xaxis_end;
      std::tie(xaxis_title, xaxis_nbins, xaxis_start, xaxis_end) =
          GetBinning(xaxis);
      auto complete_title = title + ";" + xaxis_title;
      out = new TH1D(directory_and_name.c_str(), complete_title.c_str(),
                     xaxis_nbins, xaxis_start, xaxis_end);
    }
    // Add special naming here
    AdjustAxis(out, xaxis);
    return out;
  }
}

TH1 *GetHist(std::string directory_and_name, std::string title,
             std::string xaxis, std::string yaxis = "",
             std::string zaxis = "") {
  if (mapForGetHist.find(directory_and_name) == mapForGetHist.end()) {
    // Object doesn't exist, create it and store it
    mapForGetHist[directory_and_name] =
        MakeHist(directory_and_name, title, xaxis, yaxis, zaxis);
  }
  auto out = mapForGetHist[directory_and_name];
  return out;
}

bool HitBox(TVector3 pos, TVector3 start, TVector3 end) {
  bool out = true;
  if (pos.X() < start.X())
    out = false;
  if (pos.Y() < start.Y())
    out = false;
  if (pos.Z() < start.Z())
    out = false;
  if (pos.X() > end.X())
    out = false;
  if (pos.Y() > end.Y())
    out = false;
  if (pos.Z() > end.Z())
    out = false;
  return out;
}

bool HitInterestRegion(TVector3 pos) {
  return HitBox(pos, ND_CAVE_START, ND_CAVE_END);
}

int GetVtxId(std::map<int, int> vtx_track_id_map, TG4Trajectory &traj) {
  int track_id = traj.GetTrackId();
  const int DEFAULT = -99999999;
  int vtx_id = DEFAULT;
  if (vtx_track_id_map.find(track_id) != vtx_track_id_map.end()) {
    vtx_id = vtx_track_id_map.at(track_id);
  }
  if (vtx_id == DEFAULT) {
    // Didn't find it yet, try parent
    int parent_track_id = traj.GetParentId();
    if (vtx_track_id_map.find(parent_track_id) != vtx_track_id_map.end()) {
      vtx_id = vtx_track_id_map.at(parent_track_id);
    }
  }
  if (vtx_id == DEFAULT) {
    std::cerr << "Didn't find vtx id, track id: " << track_id
              << ",\tparent track id: " << traj.GetParentId() << std::endl;
  }
  return vtx_id;
}

void fill_range(std::string hist_name, std::string title, double value,
                bool negative, std::string xaxis, std::string yaxis = "") {
  auto hist = GetHist(hist_name, title, xaxis, yaxis);
  int nbins = hist->GetXaxis()->GetNbins();
  const double max = hist->GetXaxis()->GetXmax();
  const double min = hist->GetXaxis()->GetXmin();
  if (std::isnan(value))
    value = (negative) ? max : min;
  int bin = hist->GetXaxis()->FindBin(value);
  // int db = -1;
  // if (negative) db = 1;
  /*for (int b = bin; b <= nbins + 2 && b >= 0; b += db) {
    value = hist->GetXaxis()->GetBinCenter(bin);
    hist->Fill(value);
  }*/
  // When value = max or min, then can end up with events on bin edges.
  // Depending on rounding, it ends up in in right bin or bin above/below
  // So pick the bin center to start to avoid issue
  double dx = (max - min) / nbins;
  if (negative)
    dx *= -1;
  value = hist->GetXaxis()->GetBinCenter(bin);
  // std::cout<<"Filling range with value "<<value<<", dx="<<dx<<",
  // min="<<min<<", max="<<max<<std::endl;
  while ((negative || value <= max) && (!negative || value >= min)) {
    hist->Fill(value);
    value += dx;
  }
}

void fill_both(std::string hist_name, std::string title, double value,
               bool negative, std::string xaxis, std::string yaxis = "") {
  const double nan = std::nan("1");
  fill_range(hist_name + "_numerator", title, value, negative, xaxis, yaxis);
  fill_range(hist_name + "_denominator", title, nan, negative, xaxis, yaxis);
  // Also save a copy of the actual value for debugging
  GetHist(hist_name + "_actual_value", "Vertices at Given Location", xaxis,
          yaxis)
      ->Fill(value);
  GetHist(hist_name + "_actual_value_normalize_per_spill", "Vertices per Spill",
          xaxis, yaxis)
      ->Fill(value);
  // Vertices per Spill given Cut Location
  fill_range(hist_name + "_normalize_per_spill", "N Vtx / Spill at Cut", value,
             negative, xaxis, yaxis);
}

void fill_probability(TG4Event *event, TG4PrimaryVertex &vtx,
                      std::string name) {
  double x = vtx.GetPosition().X() * M;
  double y = vtx.GetPosition().Y() * M;
  double z = vtx.GetPosition().Z() * M;
  fill_both(name + "__probability__z_front", "Events given Cut Location", z,
            true, "search_front_z");
  fill_both(name + "__probability__z_back", "Events given Cut Location", z,
            false, "search_end_z");
  fill_both(name + "__probability__x_other", "Events given Cut Location", x,
            false, "search_other_x");
  fill_both(name + "__probability__x_prism", "Events given Cut Location", x,
            true, "search_prism_x");
  fill_both(name + "__probability__y_bottom", "Events given Cut Location", y,
            true, "search_bottom_y");
  fill_both(name + "__probability__y_top", "Events given Cut Location", y,
            false, "search_top_y");

  bool x_fiducial_start = x >= GENIE_FIDUCIAL_START.X();
  bool x_fiducial_end = x <= GENIE_FIDUCIAL_END.X();
  bool x_fiducial = x_fiducial_start && x_fiducial_end;
  bool y_fiducial_start = y >= GENIE_FIDUCIAL_START.Y();
  bool y_fiducial_end = y <= GENIE_FIDUCIAL_END.Y();
  bool y_fiducial = y_fiducial_start && y_fiducial_end;
  bool z_fiducial_start = z >= GENIE_FIDUCIAL_START.Z();
  bool z_fiducial_end = z <= GENIE_FIDUCIAL_END.Z();
  bool z_fiducial = z_fiducial_start && z_fiducial_end;
  if (x_fiducial && y_fiducial && z_fiducial_end)
    fill_both(name + "__probability__fiducial_only__z_front",
              "Events given Cut Location (XY fiducial)", z, true,
              "search_front_z");
  if (x_fiducial && y_fiducial && z_fiducial_start)
    fill_both(name + "__probability__fiducial_only__z_back",
              "Events given Cut Location (XY fiducial)", z, false,
              "search_end_z");
  if (z_fiducial && y_fiducial && x_fiducial_start)
    fill_both(name + "__probability__fiducial_only__x_other",
              "Events given Cut Location (YZ fiducial)", x, false,
              "search_other_x");
  if (z_fiducial && y_fiducial && x_fiducial_end)
    fill_both(name + "__probability__fiducial_only__x_prism",
              "Events given Cut Location (YZ fiducial)", x, true,
              "search_prism_x");
  if (x_fiducial && z_fiducial && y_fiducial_end)
    fill_both(name + "__probability__fiducial_only__y_bottom",
              "Events given Cut Location (XZ fiducial)", y, true,
              "search_bottom_y");
  if (x_fiducial && z_fiducial && y_fiducial_start)
    fill_both(name + "__probability__fiducial_only__y_top",
              "Events given Cut Location (XZ fiducial)", y, false,
              "search_top_y");
}

void plot_everything_interesting(TG4Event *event, TG4PrimaryVertex &vtx,
                                 std::string name) {
  double x = vtx.GetPosition().X() * M;
  double y = vtx.GetPosition().Y() * M;
  double z = vtx.GetPosition().Z() * M;
  GetHist(name + "__vtx_positions__vtx_x", "Vtx X", "x")->Fill(x);
  GetHist(name + "__vtx_positions__vtx_y", "Vtx Y", "y")->Fill(y);
  GetHist(name + "__vtx_positions__vtx_z", "Vtx Z", "z")->Fill(z);
  GetHist(name + "__vtx_positions_2d__vtx_xy", "Vtx XY", "x", "y")->Fill(x, y);
  GetHist(name + "__vtx_positions_2d__vtx_yz", "Vtx YZ", "z", "y")->Fill(z, y);
  GetHist(name + "__vtx_positions_2d__vtx_xz", "Vtx XZ", "z", "x")->Fill(z, x);

  GetHist(name + "__vtx_positions_2d__z120_vtx_yz", "Vtx YZ", "z_120", "y_120")
      ->Fill(z, y);

  GetHist(name + "__vtx_positions_2d__wide_vtx_xy", "Vtx XY", "x_wide",
          "y_wide")
      ->Fill(x, y);
  GetHist(name + "__vtx_positions_2d__wide_vtx_yz", "Vtx YZ", "z_wide",
          "y_wide")
      ->Fill(z, y);
  GetHist(name + "__vtx_positions_2d__wide_vtx_xz", "Vtx XZ", "z_wide",
          "x_wide")
      ->Fill(z, x);

  GetHist(name + "__vtx_positions_2d__prism_end_xz", "Prism Vtx XZ", "prism_z",
          "prism_x")
      ->Fill(z, x);
  GetHist(name + "__vtx_positions_2d__prism_end_xy", "Prism Vtx XY", "prism_x",
          "prism_y")
      ->Fill(x, y);

  if (ND_CAVE_END.X() >= x && ND_CAVE_START.X() <= x)
    GetHist(name + "__vtx_positions_2d__cave_vtx_yz",
            "Vtx YZ, -5 <= Vtx X / m <= 5", "cave_z_hd", "cave_y_hd")
        ->Fill(z, y);
  if (ND_CAVE_END.Y() >= y && ND_CAVE_START.Y() <= y)
    GetHist(name + "__vtx_positions_2d__cave_vtx_xz",
            "Vtx XZ, -6 <= Vtx Y / m <= 4", "cave_z_hd", "cave_x_hd")
        ->Fill(z, x);
  if (ND_CAVE_END.Z() >= z && ND_CAVE_START.Z() <= z)
    GetHist(name + "__vtx_positions_2d__cave_vtx_xy",
            "Vtx XY, 0 <= Vtx Z / m <= 30", "cave_x_hd", "cave_y_hd")
        ->Fill(x, y);
  if (ND_CAVE_END.X() >= x && ND_CAVE_START.X() <= x)
    GetHist(name + "__vtx_positions_2d__ld_cave_vtx_yz", "Vtx YZ", "cave_z",
            "cave_y")
        ->Fill(z, y);
  if (ND_CAVE_END.Y() >= y && ND_CAVE_START.Y() <= y)
    GetHist(name + "__vtx_positions_2d__ld_cave_vtx_xz", "Vtx XZ", "cave_z",
            "cave_x")
        ->Fill(z, x);
  if (ND_CAVE_END.Z() >= z && ND_CAVE_START.Z() <= z)
    GetHist(name + "__vtx_positions_2d__ld_cave_vtx_xy", "Vtx XY", "cave_x",
            "cave_y")
        ->Fill(x, y);

  GetHist(name + "__vtx_positions__zoom_vtx_x", "Vtx X", "zoom_x")->Fill(x);
  GetHist(name + "__vtx_positions__zoom_vtx_y", "Vtx Y", "zoom_y")->Fill(y);
  GetHist(name + "__vtx_positions__zoom_vtx_z", "Vtx Z", "zoom_z")->Fill(z);
  GetHist(name + "__vtx_positions_2d__zoom_vtx_xy", "Vtx XY", "zoom_x",
          "zoom_y")
      ->Fill(x, y);
  GetHist(name + "__vtx_positions_2d__zoom_vtx_yz", "Vtx YZ", "zoom_z",
          "zoom_y")
      ->Fill(z, y);
  GetHist(name + "__vtx_positions_2d__zoom_vtx_xz", "Vtx XZ", "zoom_z",
          "zoom_x")
      ->Fill(z, x);

  // Want to be really sure there are no vtx from behind sand
  GetHist(name + "__vtx_positions__z_post_cave", "Vtx Z, post cave",
          "z_post_cave")
      ->Fill(z);
  GetHist(name + "__vtx_positions__z_post_cave_zoom", "Vtx Z, post cave",
          "z_post_cave_zoom")
      ->Fill(z);

  fill_probability(event, vtx, name);

  std::vector<TG4PrimaryParticle> particles = vtx.Particles;
  for (TG4PrimaryVertex::PrimaryParticles::iterator jt = particles.begin();
       jt != particles.end(); ++jt) {
    TG4PrimaryParticle particle = *jt;
    int pdg = PDGtoIndex(particle.GetPDGCode());
    GetHist(name + "__particles__all_primary_pdg", "primary pdg", "pdg")
        ->Fill(pdg);
  }
  if (event) {
  }
}

int main(int argc, char *argv[]) {
  // Check if the correct number of arguments is provided
  if (argc < 2) {
    std::cerr << "Usage: " << argv[0]
              << " <input_filename> <num_events (optional)>" << std::endl;
    return 1;
  }

  // Extract input filename and number of events from command line arguments
  std::string inputFilename = argv[1];
  int numEvents = -1;
  if (argc > 2)
    numEvents = atoi(argv[2]);

  // std::string filename =
  // "/pnfs/dune/scratch/users/kleykamp/nd_production/2025-02-13_test_larger_window_1spill/edep/RHC/00m/00/*.edep.root";
  // std::string filename =
  // "/pnfs/dune/scratch/users/kleykamp/nd_production/2025-02-15_updated_rockbox_wider_window/edep/RHC/00m/00/*.edep.root";
  // std::string filename =
  // "/pnfs/dune/scratch/users/kleykamp/nd_production/2025-02-15_anti-fiducial/edep/RHC/00m/00/*.edep.root";
  std::string filename;
  if (inputFilename.find("abooth") == std::string::npos)
    filename = inputFilename + "/edep/RHC/00m/00/*.edep.root";
  else
    filename = inputFilename + "/*.root";

  TChain *gRoo = new TChain("DetSimPassThru/gRooTracker");
  gRoo->Add(filename.c_str());
#define __EDEP_SIM_MAX_PART__ 1000
  int StdHepPdg[__EDEP_SIM_MAX_PART__];
  double StdHepP4[__EDEP_SIM_MAX_PART__][4];
  double EvtVtx[__EDEP_SIM_MAX_PART__][4];
  if (gRoo) {
    gRoo->SetBranchStatus("*", false);
    gRoo->SetBranchStatus("StdHepPdg", true);
    gRoo->SetBranchStatus("StdHepP4", true);
    gRoo->SetBranchStatus("EvtVtx", true);
    gRoo->SetBranchAddress("StdHepPdg", StdHepPdg);
    gRoo->SetBranchAddress("StdHepP4", StdHepP4);
    gRoo->SetBranchAddress("EvtVtx", EvtVtx);
  }

  TChain *events = new TChain("EDepSimEvents");
  // events->Add(inputFilename.c_str());
  events->Add(filename.c_str());

  std::string exeName = getExecutableName(argv[0]);
  std::string directoryPath = "/exp/dune/data/users/" +
                              std::string(getenv("USER")) + "/dunendggd/" +
                              exeName + "/";

  createDirectory(directoryPath);

  // Create output filename, GIT_BRANCH_NAME + "_" +
  std::string outputFilename = directoryPath + getOutputFilename(inputFilename);
  std::cout << "Saving output in " << outputFilename << std::endl;

  std::string save_location = getOutputDirname(outputFilename);

  createDirectory(save_location);

  // Get the geometry
  // TFile input(inputFilename.c_str());
  // TGeoManager *geom = (TGeoManager*)input.Get("EDepSimGeometry");
  // if (geom == NULL) {
  //  std::cout<<"Fatal: Wasn't able to load the geometry from
  //  "<<inputFilename<<std::endl; exit(1);
  //}

  TG4Event *event = NULL;
  events->SetBranchAddress("Event", &event);

  // Create TFile with the output filename
  TFile outputFile(outputFilename.c_str(), "RECREATE");

  REGISTER_AXIS(energy, std::make_tuple("KE (GeV)", 51, 0, 100));
  REGISTER_AXIS(true_visible_e,
                std::make_tuple("True Visible E (MeV)", 200, 0, 200));

  REGISTER_AXIS(x, std::make_tuple("X (m)", 61, -30, 30));
  REGISTER_AXIS(y, std::make_tuple("Y (m)", 61, -15, 25));
  REGISTER_AXIS(z, std::make_tuple("Z (m)", 61, -150, 50));

  REGISTER_AXIS(y_120, std::make_tuple("Y (m)", 61, -30, 50));
  REGISTER_AXIS(z_120, std::make_tuple("Z (m)", 61, -120, 120));

  REGISTER_AXIS(x_wide, std::make_tuple("X (m)", 101, -300, 300));
  REGISTER_AXIS(y_wide, std::make_tuple("Y (m)", 101, -300, 300));
  REGISTER_AXIS(z_wide, std::make_tuple("Z (m)", 101, -300, 300));

  REGISTER_AXIS(cave_x,
                std::make_tuple("X (m)", 31, ND_CAVE_START.X() - dx * ce,
                                ND_CAVE_END.X() + dx * ce));
  REGISTER_AXIS(cave_y,
                std::make_tuple("Y (m)", 31, ND_CAVE_START.Y() - dy * ce,
                                ND_CAVE_END.Y() + dy * ce));
  REGISTER_AXIS(cave_z,
                std::make_tuple("Z (m)", 31, ND_CAVE_START.Z() - dz * ce,
                                ND_CAVE_END.Z() + dz * ce));
  REGISTER_AXIS(cave_x_hd,
                std::make_tuple("X (m)", 101, ND_CAVE_START.X() - dx * ce,
                                ND_CAVE_END.X() + dx * ce));
  REGISTER_AXIS(cave_y_hd,
                std::make_tuple("Y (m)", 101, ND_CAVE_START.Y() - dy * ce,
                                ND_CAVE_END.Y() + dy * ce));
  REGISTER_AXIS(cave_z_hd,
                std::make_tuple("Z (m)", 101, ND_CAVE_START.Z() - dz * ce,
                                ND_CAVE_END.Z() + dz * ce));

  REGISTER_AXIS(zoom_x, std::make_tuple("X (m)", 101, ZOOMED_REGION_START.X(),
                                        ZOOMED_REGION_END.X()));
  REGISTER_AXIS(zoom_y, std::make_tuple("Y (m)", 101, ZOOMED_REGION_START.Y(),
                                        ZOOMED_REGION_END.Y()));
  REGISTER_AXIS(zoom_z, std::make_tuple("Z (m)", 101, ZOOMED_REGION_START.Z(),
                                        ZOOMED_REGION_END.Z()));

  REGISTER_AXIS(search_front_z,
                std::make_tuple("Z Location (m)", 100, -10.0, 0.0));
  REGISTER_AXIS(search_end_z, std::make_tuple("Z Location (m)", 40, 0, 40));
  REGISTER_AXIS(search_other_x,
                std::make_tuple("X Location (m)", 150, 0, 15.0));
  REGISTER_AXIS(search_prism_x,
                std::make_tuple("X Location (m)", 600, -60.0, 0.0));
  REGISTER_AXIS(search_bottom_y,
                std::make_tuple("Y Location (m)", 200, -20.0, 0.0));
  REGISTER_AXIS(search_top_y, std::make_tuple("Y Location (m)", 400, 0, 40.0));

  REGISTER_AXIS(prism_x, std::make_tuple("X (m)", 41, -60, 0));
  REGISTER_AXIS(prism_y, std::make_tuple("Y (m)", 41, -20, 40));
  REGISTER_AXIS(prism_z, std::make_tuple("Z (m)", 41, -30, 30));

  REGISTER_AXIS(z_post_cave,
                std::make_tuple("Z (m)", 41, ND_CAVE_END.Z(), 120));
  REGISTER_AXIS(z_post_cave_zoom,
                std::make_tuple("Z (m)", 40, ND_CAVE_END.Z(), 40));

  const long original_n_entries = events->GetEntries();
  long n_entries = original_n_entries;
  if (numEvents > 0)
    n_entries = numEvents;
  if (n_entries == 0) {
    std::cerr << "Fatal: Found no events. Did you get the right file names?"
              << std::endl;
    std::cerr << "Input path: " << filename << std::endl;
    exit(1);
  }

  int n_files = events->GetNtrees();
  pot_for_full_sample = n_files * pot_per_file;
  std::cout << "Found " << n_files << " files. Calculate "
            << pot_for_full_sample << " pot for full sample" << std::endl;
  if (numEvents > 0) {
    pot_for_full_sample *= ((double)numEvents) / ((double)original_n_entries);
    std::cout << "numEvents " << numEvents << ". Recalculated to "
              << pot_for_full_sample << " pot for subsample" << std::endl;
  }

  std::cout << "Looping over " << n_entries << " entries" << std::endl;
  for (long i = 0; i < n_entries; i++) {
    if (i % 5393 == 0) {
      double remaining = 100 * i / (double)n_entries;
      std::cout << "\r" << i << "\t" << remaining << "%\t\t\t" << std::flush;
    }
    events->GetEntry(i);

    // This lets us backtrack vertex id from track id
    std::map<int, int> vtx_track_id_map;
    std::map<int, int> ultimate_parent_map;
    std::map<int, int> ultimate_parent_pdg_map;
    std::map<int, bool> has_muon_history_map;
    std::map<int, bool> is_primary_map;
    std::map<int, TVector3> vtx_pos_map;
    std::map<int, int> track_id_pdg_map;
    std::map<int, bool> vtx_has_hits_in_interest_region_flags;
    std::map<int, bool> vtx_has_hits_in_interest_region_from_nonmuon_flags;
    std::map<int, bool> vtx_has_hits_in_interest_region_from_secondary_muons;
    std::map<int, bool>
        vtx_has_hits_in_interest_region_not_even_secondary_muons_flags;

    for (TG4PrimaryVertexContainer::iterator it = event->Primaries.begin();
         it != event->Primaries.end(); ++it) {
      TG4PrimaryVertex vtx = *it;
      int vtx_id = vtx.GetInteractionNumber();
      vtx_pos_map[vtx_id] = vtx.GetPosition().Vect() * M;

      plot_everything_interesting(event, vtx, "all_vertices");

      double x = vtx.GetPosition().X() * M;
      double y = vtx.GetPosition().Y() * M;
      double z = vtx.GetPosition().Z() * M;

      bool in_axis_x =
          (OFFAXIS_REGION_END.X() >= x && OFFAXIS_REGION_START.X() <= x);
      bool in_axis_y =
          (OFFAXIS_REGION_END.Y() >= y && OFFAXIS_REGION_START.Y() <= y);
      bool in_axis_z =
          (OFFAXIS_REGION_END.Z() >= z && OFFAXIS_REGION_START.Z() <= z);
      if (in_axis_y && in_axis_z)
        GetHist("probability__vtx_x_denominator", "Vtx X", "x")->Fill(x);
      if (in_axis_x && in_axis_z)
        GetHist("probability__vtx_y_denominator", "Vtx Y", "y")->Fill(y);
      if (in_axis_y && in_axis_x)
        GetHist("probability__vtx_z_denominator", "Vtx Z", "z")->Fill(z);

      std::vector<TG4PrimaryParticle> particles = vtx.Particles;
      for (TG4PrimaryVertex::PrimaryParticles::iterator jt = particles.begin();
           jt != particles.end(); ++jt) {
        TG4PrimaryParticle particle = *jt;
        int pdg = PDGtoIndex(particle.GetPDGCode());
        GetHist("probability__primary_pdg_denominator", "primary pdg", "pdg")
            ->Fill(pdg);

        int track_id = particle.GetTrackId();
        vtx_track_id_map[track_id] = vtx_id;
        track_id_pdg_map[track_id] = pdg;
      }
    }

    // This loop finds the ultimate parent particle of each trajectory
    for (TG4TrajectoryContainer::iterator jt = event->Trajectories.begin();
         jt != event->Trajectories.end(); ++jt) {
      TG4Trajectory traj = *jt;
      int track_id = traj.GetTrackId();
      int track_id_for_vtx_lookup = track_id;
      int current_parent = traj.GetParentId();
      int initial_pdg = traj.GetPDGCode();
      track_id_pdg_map[track_id] = PDGtoIndex(initial_pdg);
      int ultimate_parent_pdg_code = initial_pdg;
      bool is_primary = current_parent == -1;
      if (current_parent != -1)
        track_id_for_vtx_lookup = current_parent;
      int vtx_id = -9999;
      bool has_muon_history = IsMuonPdg(ultimate_parent_pdg_code);

// #define DISPLAY_DECAY_RECORD
#ifdef DISPLAY_DECAY_RECORD
      std::string parents =
          string_format("track id: %i <- %i", track_id, current_parent);
      std::string pdg_string = string_format("track pdg: %i", initial_pdg);
#endif

      while (current_parent != -1) {
        ultimate_parent_pdg_code =
            event->Trajectories[current_parent].GetPDGCode();
        // Only update if not true yet
        if (!has_muon_history)
          has_muon_history = IsMuonPdg(ultimate_parent_pdg_code);
        current_parent = event->Trajectories[current_parent].GetParentId();
        if (current_parent != -1)
          track_id_for_vtx_lookup =
              event->Trajectories[current_parent].GetTrackId();
#ifdef DISPLAY_DECAY_RECORD
        if (current_parent != -1) {
          parents += string_format(" <- %i", current_parent);
          pdg_string += string_format(",\tipdg: %i", ultimate_parent_pdg_code);
        }
#endif
      }
      // Didn't find it yet, so look it up
      if (vtx_id < 0)
        vtx_id = vtx_track_id_map.at(track_id_for_vtx_lookup);
      ultimate_parent_map[track_id] = vtx_id;
      ultimate_parent_pdg_map[track_id] = ultimate_parent_pdg_code;
      has_muon_history_map[track_id] = has_muon_history;
      is_primary_map[track_id] = is_primary;
#ifdef DISPLAY_DECAY_RECORD
      parents +=
          string_format(",\tvtx: %i (%i)", vtx_id, track_id_for_vtx_lookup);
      pdg_string +=
          string_format(",\tultimate pdg: %i", ultimate_parent_pdg_code);
      std::cerr << parents << std::endl;
      std::cerr << pdg_string << std::endl;
#endif
    }

    for (auto it = event->SegmentDetectors.begin();
         it != event->SegmentDetectors.end(); ++it) {
      std::string det_name = it->first;
      // Skip muon tagger since that'll be removed
      if (det_name == "muTag")
        continue;
      // Combine two sand components
      if (det_name == "EMCalSci" || det_name == "Straw" || det_name == "LArHit")
        det_name = "Sand";
      if (det_name == "volTMS")
        det_name = "TMS";
      if (det_name == "volTPCActive")
        det_name = "ND-LAr";
      // https://internal.dunescience.org/doxygen/classTG4HitSegment.html#ae951786c5ad10d98ef97dbce7f7e0b65
      TG4HitSegmentContainer tms_hits = (*it).second;
      for (TG4HitSegmentContainer::iterator kt = tms_hits.begin();
           kt != tms_hits.end(); ++kt) {
        TG4HitSegment edep_hit = *kt;
        // This returns the track id of the primary particle, no the specific
        // particle that made it
        int track_id = edep_hit.GetPrimaryId();
        if (vtx_track_id_map.find(track_id) != vtx_track_id_map.end()) {
          int vtx_id = vtx_track_id_map.at(track_id);
          int pdg_track_id = track_id_pdg_map.at(track_id);
          int ultimate_parent_pdg =
              PDGtoIndex(ultimate_parent_pdg_map.at(track_id));
          bool has_muon_history = has_muon_history_map.at(track_id);

          TLorentzVector avg = (edep_hit.GetStart() + edep_hit.GetStart());
          avg *= 0.5;

          double x = avg.X() * M;
          double y = avg.Y() * M;
          double z = avg.Z() * M;
          double e = edep_hit.GetEnergyDeposit();

          GetHist("segment_detectors__positions__cave_vtx_yz", "Vtx YZ",
                  "cave_z_hd", "cave_y_hd")
              ->Fill(z, y);
          GetHist("segment_detectors__positions__cave_vtx_xz", "Vtx XZ",
                  "cave_z_hd", "cave_x_hd")
              ->Fill(z, x);
          GetHist("segment_detectors__positions__cave_vtx_xy", "Vtx XY",
                  "cave_x_hd", "cave_y_hd")
              ->Fill(x, y);

          // Validate renaming of sand component
          if (det_name == "Sand")
            GetHist("segment_detectors__positions__validate__sand_cave_vtx_yz",
                    "Sand Validation, Vtx YZ", "cave_z_hd", "cave_y_hd")
                ->Fill(z, y);

          GetHist("segment_detectors__energy__true_visible_e", "True Visible E",
                  "true_visible_e")
              ->Fill(e);
          if (e > 5)
            GetHist("segment_detectors__energy__true_visible_e_above_5MeV",
                    "True Visible E, > 5 MeV", "true_visible_e")
                ->Fill(e);

          GetHist("segment_detectors__pdg__" + det_name + "_pdg_primary",
                  "PDG of Primary Particle", "pdg")
              ->Fill(pdg_track_id);
          GetHist("segment_detectors__pdg__all_det_pdg_primary",
                  "PDG of Primary Particle", "pdg")
              ->Fill(pdg_track_id);
          GetHist("segment_detectors__pdg__pdg_primary_nostack_" + det_name,
                  "PDG of Primary Particle: " + det_name, "pdg")
              ->Fill(pdg_track_id);
          // GetHist("segment_detectors__pdg__" + det_name +
          // "_pdg_ultimate_parent",
          //         "PDG of Ultimate Parent",
          //         "pdg")->Fill(ultimate_parent_pdg);
          // GetHist("segment_detectors__pdg__" + det_name +
          // "_pdg_segment_energy_weighted",
          //         "PDG of Segment, Energy Weighted;;Particles*True Vis E",
          //         "pdg")->Fill(pdg_track_id, e);
          // GetHist("segment_detectors__pdg__" + det_name +
          // "_pdg_ultimate_parent_energy_weighted",
          //         "PDG of Ultimate Parent, Energy Weighted;;Particles*True
          //         Vis E", "pdg")->Fill(ultimate_parent_pdg, e);

          // Contrib has the track ids of all the trajectories that contributed
          for (auto c : edep_hit.Contrib) {
            int c_track_id = c;
            if (track_id_pdg_map.find(c_track_id) != track_id_pdg_map.end()) {
              int c_pdg_track_id = track_id_pdg_map.at(c_track_id);
              GetHist("segment_detectors__pdg__" + det_name +
                          "_pdg_contributors",
                      "PDG of Contributors", "pdg")
                  ->Fill(c_pdg_track_id);
              GetHist("segment_detectors__pdg__" + det_name +
                          "_pdg_contributors_2_nostack_0_all",
                      "PDG of Segment: All", "pdg")
                  ->Fill(c_pdg_track_id);
              GetHist("segment_detectors__pdg__" + det_name +
                          "_pdg_contributors_energy_weighted_nostack_0_all",
                      "PDG of Segment, Energy Weighted: All", "pdg")
                  ->Fill(c_pdg_track_id, e);
              bool is_primary = is_primary_map.at(c_track_id);
              if (!is_primary) {
                GetHist("segment_detectors__pdg__" + det_name +
                            "_pdg_contributors_nonprimary_only",
                        "PDG of Nonprimary Contributors", "pdg")
                    ->Fill(c_pdg_track_id);
                GetHist("segment_detectors__pdg__" + det_name +
                            "_pdg_contributors_2_nostack_2_nonprimary_only",
                        "PDG of Segment: Secondary Particles", "pdg")
                    ->Fill(c_pdg_track_id);
                GetHist("segment_detectors__pdg__" + det_name +
                            "_pdg_contributors_energy_weighted_nostack_2_"
                            "nonprimary_only",
                        "PDG of Segment, Energy Weighted: Secondary Particles",
                        "pdg")
                    ->Fill(c_pdg_track_id, e);
              } else {
                GetHist("segment_detectors__pdg__" + det_name +
                            "_pdg_contributors_primary_only",
                        "PDG of Nonprimary Contributors", "pdg")
                    ->Fill(c_pdg_track_id);
                GetHist("segment_detectors__pdg__" + det_name +
                            "_pdg_contributors_2_nostack_1_primary_only",
                        "PDG of Segment: Primary Particles", "pdg")
                    ->Fill(c_pdg_track_id);
                GetHist("segment_detectors__pdg__" + det_name +
                            "_pdg_contributors_energy_weighted_nostack_1_"
                            "primary_only",
                        "PDG of Segment, Energy Weighted: Primary Particles",
                        "pdg")
                    ->Fill(c_pdg_track_id, e);
              }
            } else {
              std::cerr << "Got contrib track id out of range: " << c_track_id
                        << ", max size " << track_id_pdg_map.size()
                        << std::endl;
            }
          }

          if (!has_muon_history) {
            GetHist("segment_detectors__non_muon_sample_pdg__" + det_name +
                        "_pdg_segment",
                    "PDG of Segment", "pdg")
                ->Fill(pdg_track_id);
            GetHist("segment_detectors__non_muon_sample_pdg__all_pdg_segment",
                    "PDG of Segment", "pdg")
                ->Fill(pdg_track_id);
            // GetHist("segment_detectors__non_muon_sample_pdg__" + det_name +
            // "_pdg_ultimate_parent",
            //         "PDG of Ultimate Parent",
            //         "pdg")->Fill(ultimate_parent_pdg);
            GetHist(
                "segment_detectors__non_muon_sample_pdg__pdg_primary_nostack_" +
                    det_name,
                "PDG of Primary Particle: " + det_name, "pdg")
                ->Fill(pdg_track_id);
            GetHist("segment_detectors__non_muon_sample_pdg__pdg_primary_"
                    "energy_weighted_nostack_" +
                        det_name,
                    "PDG of Primary Particle, Energy Weighted: " + det_name,
                    "pdg")
                ->Fill(pdg_track_id, e);
          }
        }
      }
    }

    for (TG4TrajectoryContainer::iterator jt = event->Trajectories.begin();
         jt != event->Trajectories.end(); ++jt) {
      TG4Trajectory traj = *jt;
      int track_id = traj.GetTrackId();
      bool hit_region = false;
      double z_location = 1e9;
      int vtx_id = ultimate_parent_map.at(track_id);

      for (std::vector<TG4TrajectoryPoint>::iterator kt = traj.Points.begin();
           kt != traj.Points.end(); kt++) {
        TG4TrajectoryPoint pt = *kt;
        auto pos = pt.GetPosition().Vect() * M;

        if (HitInterestRegion(pos)) {
          hit_region = true;

          double x = pos.X();
          double y = pos.Y();
          double z = pos.Z();

          if (z < z_location)
            z_location = z;

          if (ND_CAVE_END.X() >= x && ND_CAVE_START.X() <= x)
            GetHist("traj__positions__cave_vtx_yz", "Vtx YZ", "cave_z_hd",
                    "cave_y_hd")
                ->Fill(z, y);
          if (ND_CAVE_END.Y() >= y && ND_CAVE_START.Y() <= y)
            GetHist("traj__positions__cave_vtx_xz", "Vtx XZ", "cave_z_hd",
                    "cave_x_hd")
                ->Fill(z, x);
          if (ND_CAVE_END.Z() >= z && ND_CAVE_START.Z() <= z)
            GetHist("traj__positions__cave_vtx_xy", "Vtx XY", "cave_x_hd",
                    "cave_y_hd")
                ->Fill(x, y);
          GetHist("traj__positions__vtx_xz", "Vtx XZ", "z", "x")->Fill(z, x);
          GetHist("traj__positions__vtx_yz", "Vtx YZ", "z", "y")->Fill(z, y);
          GetHist("traj__positions__vtx_z", "Vtx Z", "z")->Fill(z);
        }
      }

      int pdg = PDGtoIndex(traj.GetPDGCode());
      int ultimate_parent_pdg =
          PDGtoIndex(ultimate_parent_pdg_map.at(track_id));
      bool has_muon_history = has_muon_history_map.at(track_id);
      bool is_primary = traj.GetParentId() == -1;
      GetHist("interest_region__particles__pdg_all_traj", "pdg", "pdg")
          ->Fill(pdg);
      if (is_primary)
        GetHist("interest_region__primary_particles__pdg_all_traj", "pdg",
                "pdg")
            ->Fill(pdg);
      GetHist("interest_region__ultimate_parent_particle__pdg_all_traj", "pdg",
              "pdg")
          ->Fill(ultimate_parent_pdg);
      if (hit_region) {
        GetHist("traj__positions__lowest_z_hit_location",
                "Lowest Z Hit Location", "z")
            ->Fill(z_location);

        GetHist("interest_region__ultimate_parent_particle__pdg", "pdg", "pdg")
            ->Fill(ultimate_parent_pdg);
        // if (IsMuon(ultimate_parent_pdg))
        // GetHist("interest_region__ultimate_parent_particle__dist_muon", "dist
        // muon", "dist")->Fill(dist);

        // Only fill these once per traj, but only if traj hit region
        GetHist("interest_region__particles__pdg", "pdg", "pdg")->Fill(pdg);
        if (is_primary)
          GetHist("interest_region__primary_particles__pdg", "pdg", "pdg")
              ->Fill(pdg);
        double ke =
            (traj.GetInitialMomentum().E() - traj.GetInitialMomentum().M()) *
            GEV;
        if (IsMuon(pdg))
          GetHist("interest_region__energy__energy_muon", "KE", "energy")
              ->Fill(ke);
        if (IsNeutron(pdg))
          GetHist("interest_region__energy__energy_neutron", "KE", "energy")
              ->Fill(ke);
        if (IsProton(pdg))
          GetHist("interest_region__energy__energy_proton", "KE", "energy")
              ->Fill(ke);
        if (IsPion(pdg))
          GetHist("interest_region__energy__energy_pion", "KE", "energy")
              ->Fill(ke);
        if (vtx_id >= 0) {
          // This is the important thing to fill
          vtx_has_hits_in_interest_region_flags[vtx_id] = true;
          // This looks for primary muons only
          if (!IsMuon(ultimate_parent_pdg))
            vtx_has_hits_in_interest_region_from_nonmuon_flags[vtx_id] = true;
          // This looks for any muons, like those from secondary interactions.
          // They might not be picked up by the rockbox, especially when
          // side-entering
          if (!has_muon_history)
            vtx_has_hits_in_interest_region_not_even_secondary_muons_flags
                [vtx_id] = true;
          // Looks for specifically secondary muons
          if (!IsMuon(ultimate_parent_pdg) && has_muon_history)
            vtx_has_hits_in_interest_region_from_secondary_muons[vtx_id] = true;
          if (vtx_pos_map.find(vtx_id) != vtx_pos_map.end()) {
            auto pos = vtx_pos_map[vtx_id];
            double z = pos.Z();
            double x = pos.X();
            // std::cerr<<"xz: "<<x<<"\t"<<z<<std::endl;
            if (pos.Z() < -10)
              GetHist("interest_region__particles__pdg_z_n010", "pdg", "pdg")
                  ->Fill(pdg);
            if (pos.Z() < -50)
              GetHist("interest_region__particles__pdg_z_n050", "pdg", "pdg")
                  ->Fill(pdg);
            if (pos.Z() < -100)
              GetHist("interest_region__particles__pdg_z_n100", "pdg", "pdg")
                  ->Fill(pdg);
            if (pos.Z() < -10 && is_primary)
              GetHist("interest_region__primary_particles__pdg_z_n010", "pdg",
                      "pdg")
                  ->Fill(pdg);
            if (pos.Z() < -50 && is_primary)
              GetHist("interest_region__primary_particles__pdg_z_n050", "pdg",
                      "pdg")
                  ->Fill(pdg);
            if (pos.Z() < -100 && is_primary)
              GetHist("interest_region__primary_particles__pdg_z_n100", "pdg",
                      "pdg")
                  ->Fill(pdg);

            if (IsMuon(pdg) && pos.Z() < -10)
              GetHist("interest_region__energy__energy_muon_z_n010", "KE",
                      "energy")
                  ->Fill(ke);
            if (IsMuon(pdg) && pos.Z() < -50)
              GetHist("interest_region__energy__energy_muon_z_n050", "KE",
                      "energy")
                  ->Fill(ke);
            if (IsMuon(pdg) && pos.Z() < -100)
              GetHist("interest_region__energy__energy_muon_z_n100", "KE",
                      "energy")
                  ->Fill(ke);
            if (IsMuon(pdg) && pos.Z() < -100 && is_primary)
              GetHist("interest_region__energy__energy_primary_muon_z_n100",
                      "KE", "energy")
                  ->Fill(ke);
            if (IsNeutron(pdg) && pos.Z() < -50)
              GetHist("interest_region__energy__energy_neutron_z_n050", "KE",
                      "energy")
                  ->Fill(ke);
            if (IsNeutron(pdg) && pos.Z() < -50 && is_primary)
              GetHist("interest_region__energy__energy_primary_neutron_z_n050",
                      "KE", "energy")
                  ->Fill(ke);

            if (IsMuon(pdg) && is_primary)
              GetHist("interest_region__energy__primary_muon_vtx_z", "z", "z")
                  ->Fill(z);
            if (IsMuon(pdg) && is_primary)
              GetHist("interest_region__energy__primary_muon_vtx_xz", "xz", "z",
                      "x")
                  ->Fill(z, x);
            if (IsMuon(pdg) && pos.Z() < -100 && is_primary)
              GetHist("interest_region__energy__primary_muon_vtx_z_n100", "z",
                      "z")
                  ->Fill(z);
            if (IsMuon(pdg) && pos.Z() < -100 && is_primary)
              GetHist("interest_region__energy__primary_muon_vtx_xz_n100", "xz",
                      "z", "x")
                  ->Fill(z, x);
          }
        }
      }
    }

    for (TG4PrimaryVertexContainer::iterator it = event->Primaries.begin();
         it != event->Primaries.end(); ++it) {
      TG4PrimaryVertex vtx = *it;
      int vtx_id = vtx.GetInteractionNumber();
      // gRoo->GetEntry(vtx_id);
      //  Already in GeV
      // size_t vertex_number = it - event->Primaries.begin();
      // TLorentzVector enu(StdHepP4[vertex_number][0],
      // StdHepP4[vertex_number][1], StdHepP4[vertex_number][2],
      // StdHepP4[vertex_number][3]); double energy = (enu.E() - enu.M());
      double x = vtx.GetPosition().X() * M;
      double y = vtx.GetPosition().Y() * M;
      double z = vtx.GetPosition().Z() * M;
      bool is_rock_muon = false;
      // Plot the rock muon sample specifically
      if (vtx_has_hits_in_interest_region_flags.find(vtx_id) !=
              vtx_has_hits_in_interest_region_flags.end() &&
          vtx_has_hits_in_interest_region_flags.at(vtx_id)) {

        plot_everything_interesting(event, vtx, "rock_muons");
        is_rock_muon = true;

        bool in_axis_x =
            (OFFAXIS_REGION_END.X() >= x && OFFAXIS_REGION_START.X() <= x);
        bool in_axis_y =
            (OFFAXIS_REGION_END.Y() >= y && OFFAXIS_REGION_START.Y() <= y);
        bool in_axis_z =
            (OFFAXIS_REGION_END.Z() >= z && OFFAXIS_REGION_START.Z() <= z);
        if (in_axis_y && in_axis_z)
          GetHist("probability__vtx_x_numerator", "Vtx X", "x")->Fill(x);
        if (in_axis_x && in_axis_z)
          GetHist("probability__vtx_y_numerator", "Vtx Y", "y")->Fill(y);
        if (in_axis_y && in_axis_x)
          GetHist("probability__vtx_z_numerator", "Vtx Z", "z")->Fill(z);

        std::vector<TG4PrimaryParticle> particles = vtx.Particles;
        for (TG4PrimaryVertex::PrimaryParticles::iterator jt =
                 particles.begin();
             jt != particles.end(); ++jt) {
          TG4PrimaryParticle particle = *jt;
          int pdg = PDGtoIndex(particle.GetPDGCode());
          GetHist("probability__primary_pdg_numerator", "primary pdg", "pdg")
              ->Fill(pdg);
        }
      }

      bool is_nonmuon_sample =
          vtx_has_hits_in_interest_region_not_even_secondary_muons_flags.find(
              vtx_id) !=
              vtx_has_hits_in_interest_region_not_even_secondary_muons_flags
                  .end() &&
          vtx_has_hits_in_interest_region_not_even_secondary_muons_flags.at(
              vtx_id);

      bool is_not_rock_muon_sample =
          vtx_has_hits_in_interest_region_from_nonmuon_flags.find(vtx_id) !=
              vtx_has_hits_in_interest_region_from_nonmuon_flags.end() &&
          vtx_has_hits_in_interest_region_from_nonmuon_flags.at(vtx_id);

      bool is_secondary_muon_sample =
          vtx_has_hits_in_interest_region_from_secondary_muons.find(vtx_id) !=
              vtx_has_hits_in_interest_region_from_secondary_muons.end() &&
          vtx_has_hits_in_interest_region_from_secondary_muons.at(vtx_id);

      // This is the box used to compute the non-muon sample
      // The probability numerator here would tell us the total computational
      // load for the chosen cuts
      bool is_in_fiducial_box = true;
      if (is_in_fiducial_box &&
          (z < GENIE_FIDUCIAL_START.Z() || z > GENIE_FIDUCIAL_END.Z()))
        is_in_fiducial_box = false;
      if (is_in_fiducial_box &&
          (x < GENIE_FIDUCIAL_START.X() || x > GENIE_FIDUCIAL_END.X()))
        is_in_fiducial_box = false;
      if (is_in_fiducial_box &&
          (y < GENIE_FIDUCIAL_START.Y() || y > GENIE_FIDUCIAL_END.Y()))
        is_in_fiducial_box = false;

      if (is_secondary_muon_sample)
        plot_everything_interesting(event, vtx, "secondary_muons");
      if (is_not_rock_muon_sample)
        plot_everything_interesting(event, vtx, "not_rock_muon");
      if (is_nonmuon_sample)
        plot_everything_interesting(event, vtx, "nonmuon_sample");
      if (is_in_fiducial_box)
        plot_everything_interesting(event, vtx, "fiducial_box");
    }
  }
  std::cout << "\rall done                         " << std::endl;
  NormalizeHists();
  outputFile.Write();

  // Close the output file
  outputFile.Close();

  std::cout << "Output file created: " << outputFilename << std::endl;

  return 0;
}
