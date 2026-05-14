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
parser.add_argument('--show_fit', action='store_true')
parser.add_argument('--show_interpolators', action='store_true')
parser.add_argument('--no_visualizations', action='store_true')
args = parser.parse_args()

fp = folder_processor()
df, df_scint_photons, df_cheren_photons = fp.process_folder(args.folder)

sf = simulation_fitter(args.scint_profile, args.cheren_profile, df, df_scint_photons, df_cheren_photons, args.sdl)
sf.set_fit_guess(args.scint_guess,args.amplitude_guess)
scint_interp, cheren_interp = sf.get_interpolators()

visualizer = visualizations(scint_interp, cheren_interp)

if args.show_interpolators:
    visualizer.visualize_interpolators()

def handle_visualizations(data_x, data_y, sp, cp):
    if not args.no_visualizations:
        if args.show_fit:
            visualizer.visualize_data_with_fit(data_x, data_y, sp, cp)
        else:
            visualizer.visualize_data_without_fit(data_x, data_y)

#scint_time_correction = (300-300*(np.exp(-2/3)))/(300)

cmap = plt.get_cmap('plasma')
plot_tuple_array = []
step_array = [1,2,4,8]
for step_index, step in enumerate(step_array):
    print(f"Running study on {5/step:.3f}gHz")
    
    cheren_expected_percents = []
    cheren_fit_percents = []

    for event in sf.df["event"].unique():

        data = sf.get_signal_data_by_event(event)

        for data_x, data_y, data_x_coord, data_y_coord in data:

            scint_photon_guess, cheren_photon_guess, expected_amplitude, scint_photons, cheren_photons = sf.fit_data(data_x, data_y, data_x_coord, data_y_coord, event, args.particle, args.energy, step)


            scint_expected_percent  = 100*(scint_photons)/(scint_photons + cheren_photons)
            cheren_expected_percent = 100*(cheren_photons)/(scint_photons + cheren_photons) 
            
            total_fit_guess = scint_photon_guess + cheren_photon_guess
            fit_scint_fraction = scint_photon_guess/(total_fit_guess)
            fit_cheren_fraction = cheren_photon_guess/(total_fit_guess)
            print("-"*50)
            print(f"Event: {event}")
            print(f"Data Amplitude: {expected_amplitude}")
            print(f"Scint fit percentage: {(fit_scint_fraction*100):.3f}")
            print(f"Cheren fit percentage: {(fit_cheren_fraction*100):.3f}")
            print(f"Scint expected percentage: {scint_expected_percent:.3f}")
            print(f"Cheren expected percentage: {cheren_expected_percent:.3f}")
            print(f"Scint photon amount: {scint_photons}")
            print(f"Cheren photon amount: {cheren_photons}")
            print(f"ix: {data_x_coord}")
            print(f"iy: {data_y_coord}")

            handle_visualizations(data_x, data_y, scint_photon_guess, cheren_photon_guess)

            cheren_fit_percents.append((fit_cheren_fraction)*100)
            cheren_expected_percents.append(cheren_expected_percent)
    
    label = f"{5/step:.3f}gHz"
    color = cmap(step_index)
    plot_tuple = (cheren_fit_percents, cheren_expected_percents, label, color)
    plot_tuple_array.append(plot_tuple)

visualizer.visualize_rate_sampling_histograms(plot_tuple_array, bins=15)
