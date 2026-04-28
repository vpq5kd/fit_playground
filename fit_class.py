import ROOT
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from ROOT import RDataFrame
from ctypes import c_double

class simulation_fitter:
    
    
    def __init__(self, scint_profile, cheren_profile, df_data, df_scint_photons, df_cheren_photons, sdl_number=0):
        f = ROOT.TFile(scint_profile, "READ")
        a = ROOT.TFile(cheren_profile, "READ")
        
        scint_prof = f.Get("p")
        cheren_prof = a.Get("p")
    
        scint_prof.SetDirectory(0)
        cheren_prof.SetDirectory(0)


        self.scint_prof = scint_prof
        self.cheren_prof = cheren_prof

        self.sdl_number = sdl_number
        
        self.scint_interp, scint_xmin, scint_xmax = self.create_interpolator(scint_prof, 10)
        self.cheren_interp, cheren_xmin, cheren_xmax = self.create_interpolator(cheren_prof)
        
        self.xmin = max(float(scint_xmin), float(cheren_xmin))
        self.xmax = min(float(scint_xmax), float(cheren_xmax))
        
        self.df = df_data
        self.df_scint_photons = df_scint_photons
        self.df_cheren_photons = df_cheren_photons

        f.Close()
        a.Close()
    
    def get_interpolators(self):
        return self.scint_interp, self.cheren_interp

    def sdl(self,x,y,n):

        if n == 0:
                return x, y

        y_prime = y.copy()
        for i in range(n, len(y)):
                y_prime[i] = y[i]-y[i-n]
        x_prime = x[n:]
        y_prime = y_prime[n:]
        return x_prime,y_prime

    def create_interpolator(self, prof, interp_scale=1):
        nbins = prof.GetNbinsX()
        x = np.array([prof.GetBinCenter(i) for i in range(1,nbins+1)])
        y = np.array([prof.GetBinContent(i) for i in range (1,nbins+1)])*interp_scale
        x, y = self.sdl(x, y, self.sdl_number)

        interp = ROOT.Math.Interpolator(len(x), ROOT.Math.Interpolation.kCSPLINE)
        #integral = np.trapezoid(y,x)
        interp.SetData(len(x), x, y/np.max(y))

        return interp, x.min(), x.max()


    def get_signal_data_by_event(self, event):
        
        data = []

        df_filtered = self.df[self.df["event"] == event].copy()
        
        max_values = []
        for arr in df_filtered["ys_combined"]:
            max_values.append(arr.max())

        max_value = np.max(max_values)

        index = 0
        for val in max_values:
            if val >= 0.05*max_value:
                data_x = np.asarray((df_filtered["xs_cheren"].iloc[index]), dtype=float)
                data_y = np.asarray((df_filtered["ys_combined"].iloc[index]), dtype=float)
                data_x, data_y = self.sdl(data_x, data_y, self.sdl_number)
    
                data_x_coord = df_filtered["ix"].iloc[index]
                data_y_coord = df_filtered["iy"].iloc[index]


                data.append((data_x, data_y, data_x_coord, data_y_coord))
            index+=1 
        return data
        
    def get_photon_data_by_event(self, event, data_x_coord, data_y_coord):
        dsp = self.df_scint_photons.copy()
        dsp = dsp[(dsp["ix"]==data_x_coord) & (dsp["iy"] == data_y_coord) & (dsp["event"] == event)]
        dcp = self.df_cheren_photons.copy()
        dcp = dcp[(dcp["ix"]==data_x_coord) & (dcp["iy"] == data_y_coord) & (dcp["event"] == event)]
        
        scint_photon_amount = len(dsp)*10
        cheren_photon_amount = len(dcp)
        
        return scint_photon_amount, cheren_photon_amount


    def interp_fit_func(self, x, par):
        t = x[0]
        f = par[0]
        A = par[1]
        scint_val = self.scint_interp.Eval(t)
        cheren_val = self.cheren_interp.Eval(t)

        return A*((f)*scint_val + (1-f)*cheren_val)
    

    def set_fit_guess(self, fraction_guess, amplitude_guess):
        fit_func = ROOT.TF1("fit_func", self.interp_fit_func, self.xmin,self.xmax,2)
        fit_func.SetParameters(fraction_guess, amplitude_guess)

        self.fit_func = fit_func


    def fit_data(self, data_x, data_y, data_x_coord, data_y_coord, event, particle, energy):
        graph = ROOT.TGraph(len(data_x), data_x, data_y)
        graph.SetTitle(f"Particle: {particle}, Energy: {energy}, Layer: 1, Event: {event}")
        graph.Fit(self.fit_func, "R")
        
        scint_photons, cheren_photons = self.get_photon_data_by_event(event, data_x_coord, data_y_coord)

        scint_fraction = self.fit_func.GetParameter(0)
        fit_amplitude = self.fit_func.GetParameter(1)

        expected_amplitude = data_y.max()

        return scint_fraction, fit_amplitude, expected_amplitude, scint_photons, cheren_photons


