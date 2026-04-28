# Fit Playground: A sandbox for our team to figure out what is going wrong with the fit code.

## Build
run `pip install -r requirements.txt` after downloading the repo. 

## `fit_study.py`
This is the main program, run `python fit_study.py -h` to see available arguments. The easiest way to run this program is `python fit_study.py --scint_profile profiles/scintillation_profile.root --cheren_profile profiles/cherenkov_profile.root --folder events/ --scint_guess 0.9 --show_fit`. `--show_fit` can be replaced either by being deleted (which defaults to only showing a waveform) or by writing `--no_visualizations` instead, which doesn't show any of the waveforms at all and proceeds directly to the fit vs. expected scatter plot.

## Classes

### `fit_class.py` - `simulation_fitter`
This is where the fit itself occurs. This class builds the interpolators, sets the parameters, applies the SDL if needed, and does a fit with ROOT.TGraph.Fit(). 

### `folder_processor.py` - `folder_processor`

`folder_processsor` contains methods that process a folder of single-event simple trees into a combined pandas dataframe.

### `visualizations.py`- `visualizations`

`visualizations` contains methods to visualize the fits, waveforms, and expected vs fit percentages.

## events/
This is a folder of 6 single-event simple trees from a BGO electron study at 20GeV.

## profiles/
scintillation and cherenkov profiles are stored as root files here.
