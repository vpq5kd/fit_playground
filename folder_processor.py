import ROOT
import numpy as np
import pandas as pd
import numpy as np 

from pathlib import Path
from ROOT import RDataFrame

class folder_processor:

    def set_fit_file(self, filename):
        cheren_digis = "CalvisionSiPMCherenWaveform"
        rdf_cheren_digis = RDataFrame(cheren_digis, filename)
        rdf_cheren_digis = rdf_cheren_digis.Filter(f"layer == 1")
        df_cheren_digis = pd.DataFrame(rdf_cheren_digis.AsNumpy())


        scint_digis = "CalvisionSiPMScintWaveform"
        rdf_scint_digis = RDataFrame(scint_digis, filename)
        rdf_scint_digis = rdf_scint_digis.Filter(f"layer == 1")
        df_scint_digis = pd.DataFrame(rdf_scint_digis.AsNumpy())

        df = df_cheren_digis.merge(df_scint_digis, on=["event","ix","iy"], suffixes=("_cheren", "_scint"))
        #df["ys_combined"] = df["ys_cheren"].to_numpy()
        df["ys_combined"] = [np.asarray(yc, dtype=float) + 10*np.asarray(ys, dtype=float) for yc, ys in zip(df["ys_cheren"], df["ys_scint"])]
        
        passed_scint = "passedScintPhotons"
        passed_cheren = "passedCherenPhotons"
        
        rdf_scint = RDataFrame(passed_scint, filename)
        rdf_scint = rdf_scint.Filter(f"layer == 1")
        
        rdf_cheren = RDataFrame(passed_cheren, filename)
        rdf_cheren = rdf_cheren.Filter(f"layer == 1")
   	
        return df, pd.DataFrame(rdf_scint.AsNumpy()), pd.DataFrame(rdf_cheren.AsNumpy())

    def _set_fit_folder_helper(self, file):

        names = file.name.split('_')
        event_number = int(names[2].split('.')[0])
        df_single, df_scint_single, df_cheren_single = self.set_fit_file(str(file))
        df_single["event"] = event_number
        df_scint_single["event"] = event_number
        df_cheren_single["event"] = event_number

        return df_single, df_scint_single, df_cheren_single
        
    def process_folder(self, foldername):
        folder = Path(foldername)
        dfs = []
        df_scints = []
        df_cherens = []
        
        for file in folder.iterdir():
            if file.is_file():
                df_single, df_scint_single, df_cheren_single = self._set_fit_folder_helper(file)
                dfs.append(df_single)
                df_scints.append(df_scint_single)
                df_cherens.append(df_cheren_single)

        df = pd.concat(dfs, ignore_index=True).sort_values(by='event')
        df_scint_photons = pd.concat(df_scints, ignore_index=True).sort_values(by='event')
        df_cheren_photons = pd.concat(df_cherens, ignore_index=True).sort_values(by='event')

        return df, df_scint_photons, df_cheren_photons
        
