import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

def main():
    data = np.load("sr_study_data.npz", allow_pickle=True)
    plot_tuple_array = data["plot_tuple_array"]

    label_array = []
    lower_array = []
    upper_array = []
    width_array = []
    for cheren_fit_percents, cheren_expected_percents, label, color in plot_tuple_array:
        cheren_fit_percents = np.array(cheren_fit_percents)
        cheren_expected_percents = np.array(cheren_expected_percents)
        fractions = cheren_fit_percents/cheren_expected_percents

        lower, upper = minimal_68_region(fractions)
        width = upper - lower

        label_array.append(label)
        lower_array.append(lower)
        upper_array.append(upper)
        width_array.append(width)

        
    data_dict = {"Sampling Rate":label_array, "Lower":lower_array, "Upper":upper_array, "Width":width_array}
    df = pd.DataFrame(data_dict)
    df.to_csv("sr_min68.csv", index=False, float_format="%.3f")
    
main()

