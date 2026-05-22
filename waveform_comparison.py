import ROOT
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse

from pathlib import Path
from fit_class import simulation_fitter
from folder_processor import folder_processor
from visualizations import visualizations

parser = argparse.ArgumentParser('Fit Study Arguments')
parser.add_argument('--scint_profile', type=str, help='root file with scint profile hist')
parser.add_argument('--cheren_profile', type=str, help='root file with cheren profile hist')
parser.add_argument('-f','--folder',type=str, help='root folder to fit')
parser.add_argument('--scint_guess', type=float, default=10000, help='guess of percentage scintillation for fit')
parser.add_argument('--amplitude_guess',type=float,default=40000)
parser.add_argument('--sdl', type=int, default=0, help='Use if you would like to run the SDL version, add an integer in ns after --sdl')
parser.add_argument('--particle',type=str,default='e-')
parser.add_argument('--energy',type=str,default='20GeV')
args = parser.parse_args()

fp = folder_processor()
df, df_scint_photons, df_cheren_photons = fp.process_folder(args.folder)

sf = simulation_fitter(args.scint_profile, args.cheren_profile, df, df_scint_photons, df_cheren_photons, args.sdl)
sf.set_fit_guess(args.scint_guess,args.amplitude_guess)
scint_interp, cheren_interp = sf.get_interpolators()

visualizer = visualizations(scint_interp, cheren_interp)

offsets = np.arange(15)

for event in sf.df["event"].unique():

    data = sf.get_signal_data_by_event(event)

    for data_x, data_y, data_x_coord, data_y_coord in data:
            visualizer.visualize_phase_study_waveforms(data_x, data_y, offsets)

    
