import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from visualizations import visualizations

def minimal_68_region(data, fraction=0.68):
    data = np.asarray(data)
    data = np.sort(data)

    n = len(data)
    k = int(np.floor(fraction * n))

    if k < 1:
        raise ValueError("Not enough data points.")

    # Compute widths of all possible intervals containing k points
    widths = data[k:] - data[:n - k]

    # Find minimum width interval
    min_index = np.argmin(widths)

    lower = data[min_index]
    upper = data[min_index + k]

    return lower, upper

def generate_tables(frequency_plot_arrays):

    label_array = []
    lower_array = []
    upper_array = []
    width_array = []
    mean_array  = []
    title_array = []

    for plot_tuple_array in frequency_plot_arrays:
        for cheren_fit_percents, cheren_expected_percents, label, color, title in plot_tuple_array:
            cheren_fit_percents = np.array(cheren_fit_percents)
            cheren_expected_percents = np.array(cheren_expected_percents)
            fractions = cheren_fit_percents/cheren_expected_percents

            lower, upper = minimal_68_region(fractions)
            width = upper - lower
            mean = np.mean(np.array(fractions))

            label_array.append(label)
            lower_array.append(lower)
            upper_array.append(upper)
            width_array.append(width)
            mean_array.append(mean)
            title_array.append(title)
        
    data_dict = {"Sampling Rate":title_array, "Start Point":label_array, "Lower":lower_array, "Upper":upper_array, "Width/2":np.array(width_array)/2, "Mean":mean_array}
    df = pd.DataFrame(data_dict)
    df.to_csv("phase_min68.csv", index=False, float_format="%.3f")
    return df

def plot_min68_results(min_68_df):
    cols = ["Sampling Rate", "Start Point", "Width/2", "Mean"]
    df = min_68_df[cols]
    cmap = plt.get_cmap('cool')
    
    fig, ax = plt.subplots(2,1,sharex=True)
    for index, sr in enumerate(df["Sampling Rate"].unique()):

        sub_df = df[df["Sampling Rate"] == sr]
        color = cmap(index/(len(df["Sampling Rate"].unique())-1))
        start_point_array_1 = np.array([s.split(" ") for s in sub_df["Start Point"]])
        start_point_array = np.array([float(s[0]) for s in start_point_array_1])

        ax[0].scatter(start_point_array, sub_df["Width/2"], color=color, label=sr)
        ax[1].scatter(start_point_array, sub_df["Mean"],color=color,label=sr)
   
    ax[1].set_xlabel("Starting Point (ns)")
    ax[1].set_ylabel("Total Mean")
    ax[1].set_title("Starting Point vs. Distribution Mean")
    ax[1].legend()

    ax[0].set_ylabel("Width/2")
    ax[0].set_title("Starting Point vs. Distribution Width")
    ax[0].legend()
    plt.show(block=False)
    input("press enter to continue...")
    plt.close()


def main():
    data = np.load("new_waveform_phase_study_data.npz", allow_pickle=True)
    frequency_plot_arrays = data["frequency_plot_arrays"]

    min_68_df = generate_tables(frequency_plot_arrays) 
    print(min_68_df.to_string())
    plot_min68_results(min_68_df)

    visualizer = visualizations()
    visualizer.visualize_phase_effect_histograms(frequency_plot_arrays)

main()

