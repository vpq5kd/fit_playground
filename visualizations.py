import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class visualizations:

    def __init__(self, scint_interp,cheren_interp):
        self.xmin = 0
        self.xmax = 204.8
        self.scint_interp = scint_interp
        self.cheren_interp = cheren_interp

    def visualize_data_without_fit(self, data_x, data_y):
        plt.figure()
        plt.plot(data_x, data_y,label='Data Only',color='black')
        plt.xlabel('Time (ns)')
        plt.ylabel('Voltage (mv)')
        plt.plot()
        plt.show(block=False)

        input("Press enter to cycle the next event...")
        plt.close()

    def visualize_data_with_fit(self, data_x, data_y, scint_fraction, fit_amplitude):

        A = fit_amplitude
        f = scint_fraction

        ts = np.linspace(self.xmin, self.xmax, 1024)
        sc = np.array([A*f*self.scint_interp.Eval(t) for t in ts])
        ch = np.array([A*(1-f)*self.cheren_interp.Eval(t) for t in ts])
        plt.figure()
        plt.plot(data_x,data_y, color='black', label='data')
        plt.plot(ts, sc, color='orange', label='scint fit curve')
        plt.plot(ts, ch, color='blue', label='cheren fit curve')
        plt.plot(ts, sc+ch, color='red', label='complete fit curve')
        plt.xlabel("Time (ns)")
        plt.ylabel("Voltage (mv)")
        plt.title(f"Voltage vs. Time")
        plt.legend()
        plt.show(block=False)

        input("Press enter to cycle the next event...")
        plt.close()

    def visualize_fit_vs_expected(self,cheren_expected_percents, cheren_fit_percents, amplitudes, particle, energy):

        m, b = np.polyfit(cheren_expected_percents, cheren_fit_percents, 1)
        x_vals = np.linspace(min(cheren_expected_percents), max(cheren_expected_percents), 100)
        y_vals = m * x_vals + b

        plt.figure(figsize=(8,10))
        plot = plt.scatter(cheren_expected_percents, cheren_fit_percents, c = amplitudes, cmap='viridis')
        plt.plot(x_vals, y_vals, linestyle='--', color = 'red')
        plt.colorbar(plot, label='amplitude')

        plt.xlabel(r"Cheren Expected Percentage")
        plt.ylabel(r"Cheren Fit Percentage")
        plt.title(rF"Cheren Fit vs. Expected Percentage as a Function of Amplitude | M: {m:.3f} | Particle: {particle}, Energy: {energy}")


        plt.show(block=False)

        input("Press enter to close...")
        plt.close()
