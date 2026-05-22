import pandas as pd
import numpy as np
import concurrent.futures
import ROOT
import os
import argparse
from pathlib import Path
from itertools import repeat
from ROOT import RDataFrame
from tqdm import tqdm
parser = argparse.ArgumentParser('profile creator')
parser.add_argument('--folder', type=str)
parser.add_argument('--type', type=str)
parser.add_argument('--particle', type=str)
parser.add_argument('--energy', type=str)
parser.add_argument('-o','--rout', type=str)
args = parser.parse_args()
type_dict = {"scint":("CalvisionSiPMScintWaveform","passedScintPhotons"), "cheren":("CalvisionSiPMCherenWaveform","passedCherenPhotons")}



def process_file(filename, event, digi_type):
    has_photons = True
    df_tree = None
    num_photons = None
    try:
        waveforms, photons = digi_type
        rdf_tree = RDataFrame(waveforms, filename)
        rdf_tree = rdf_tree.Filter("layer == 1")
        df_tree = pd.DataFrame(rdf_tree.AsNumpy())
        df_tree["event"] = event

        rdf_photons = RDataFrame(photons, filename)
        rdf_photons = rdf_photons.Filter("layer == 1")
        num_photons = rdf_photons.Count().GetValue()
    except:
        has_photons = False

    return df_tree, num_photons, has_photons

def process_folder(foldername, digi_type):
    folder = Path(foldername)
    dfs = []
    photon_count = 0
    zero_photons_count = 0

    files = []
    events = []
    for file in Path(foldername).iterdir():
        files.append(str(file))
        names = file.name.split("_")
        events.append(int(names[2].split('.')[0]))

    with concurrent.futures.ProcessPoolExecutor(max_workers = os.cpu_count()) as executor:
        for file_df, file_photon_count, has_photons in tqdm(executor.map(process_file, files, events, repeat(digi_type)), total = len(files)):
            if has_photons:
                dfs.append(file_df)
                photon_count += file_photon_count
            else:
                zero_photons_count += 1
    print(f"{zero_photons_count} events produced 0 photons.")
    return pd.concat(dfs, ignore_index = True).sort_values(by='event'), photon_count

def main():
    df, photon_count = process_folder(args.folder, type_dict[args.type])
    print(f"{photon_count} photons")
    xmin = df["xs"][0].min()
    xmax = df["xs"][0].max()
    hist = ROOT.TH1F("p", f"{type_dict[args.type]} Profile Histogram | Particle: {args.particle} | Energy: {args.energy} | Layer: 1;Time (ns);Average Amplitude", 1024, xmin, xmax)
    
    for xarr, yarr in zip(df["xs"], df["ys"]):
        for x, y in zip(xarr, yarr):
            hist.Fill(float(x), float(y)/photon_count)

    f = ROOT.TFile(args.rout, "RECREATE")
    hist.Write()
    f.Close()

    hist.Draw()

    input("press enter to exit...")
    
main()
