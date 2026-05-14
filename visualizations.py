import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class visualizations:

    def __init__(self, scint_interp,cheren_interp):
        self.xmin = 0
        self.xmax = 204.8
        self.scint_interp = scint_interp
        self.cheren_interp = cheren_interp

    def visualize_interpolators(self):
        t = np.linspace(self.xmin, self.xmax, 1024)
        s = np.array([self.scint_interp.Eval(x) for x in t])
        c = np.array([self.cheren_interp.Eval(x) for x in t])
        plt.figure()
        plt.plot(t, s, color='gold',label=r'$S(t)$')
        plt.plot(t, c, color='blue',label=r'$Č(t)$')
        plt.legend()
        plt.title(r'$S(t)$ and $Č(t)$ Curves as a Function of Time')
        plt.xlabel(f"Time (ns)")
        plt.ylabel(f"Voltage (mv)")
        #plt.savefig("figures/interpolators.png")
        plt.show(block=False)

        input("Press enter to close interpolator visualization...")
        plt.close()

    def visualize_data_without_fit(self, data_x, data_y):
        plt.figure()
        plt.plot(data_x, data_y,label='Data Only',color='black')
        plt.xlabel('Time (ns)')
        plt.ylabel('Voltage (mv)')
        plt.plot()
        plt.show(block=False)

        input("Press enter to cycle the next event...")
        plt.close()

    def visualize_data_with_fit(self, data_x, data_y, sp, cp):


        ts = np.linspace(self.xmin, self.xmax, 1024)
        sc = np.array([sp*self.scint_interp.Eval(t) for t in ts])
        ch = np.array([cp*self.cheren_interp.Eval(t) for t in ts])
        plt.figure()
        plt.plot(data_x,data_y, color='black', label='data')
        plt.plot(ts, sc, color='orange', label='scint fit curve')
        plt.plot(ts, ch, color='blue', label='cheren fit curve')
        plt.plot(ts, sc+ch, color='red', label='complete fit curve')
        plt.xlabel("Time (ns)")
        plt.ylabel("Voltage (mv)")
        plt.title(f"Voltage vs. Time")
        plt.legend()
        plt.savefig("figures/fit_example.png")
        plt.show(block=False)

        input("Press enter to cycle the next event...")
        plt.close()

    def visualize_fit_vs_expected(self,cheren_expected_percents, cheren_fit_percents, amplitudes, particle, energy):



        coeffs, cov = np.polyfit(cheren_expected_percents, cheren_fit_percents, 1, cov=True)
        m, b = coeffs
        m_err = np.sqrt(cov[0,0])
        print(f"m_err = {m_err}")
        x_vals = np.linspace(min(cheren_expected_percents), max(cheren_expected_percents), 100)
        y_vals = m * x_vals + b

        plt.figure(figsize=(10,14))
        plot = plt.scatter(cheren_expected_percents, cheren_fit_percents, c = amplitudes, cmap='viridis')
        plt.plot(x_vals, y_vals, linestyle='--', color = 'red')
        plt.colorbar(plot, label='amplitude')

        plt.xlabel(r"Cheren Expected Percentage")
        plt.ylabel(r"Cheren Fit Percentage")
        plt.title(rF"Cheren Fit vs. Expected Percentage as a Function of Amplitude | M: {m:.3f} | Particle: {particle}, Energy: {energy}")

        
        plt.savefig("fit_vs_expected.png")
        plt.show(block=False)
        input("Press enter to close...")
        plt.close()

    def visualize_fit_vs_expected_histogram(self, cheren_fit_percents, cheren_expected_percents):
        cheren_fit_percents = np.array(cheren_fit_percents)
        cheren_expected_percents = np.array(cheren_expected_percents)
        
        fractions = cheren_fit_percents/cheren_expected_percents
        print(np.mean(fractions))
        plt.figure()
        counts, bins = np.histogram(cheren_fit_percents/cheren_expected_percents,bins=30)
        plt.stairs(counts, bins, linewidth=2, color='darkturquoise', fill=True, alpha=0.3)
        plt.axvline(np.mean(fractions),linestyle='--',color='mediumvioletred',label=f'Mean: {np.mean(fractions):.3f}')
        plt.legend()
        plt.xlabel(r"$\frac{Č_{fit}\%}{Č_{expected}\%}$")
        plt.ylabel("Counts")
        plt.title(r"$\frac{Č_{fit}\%}{Č_{expected}\%}$ Distribution")
        plt.show(block=False)
        input("Press enter to close...")
        plt.close()


    def visualize_rate_sampling_histograms(self, plot_tuple_array, bins=30):
       
        plot_tuple_array = plot_tuple_array[::-1]
        plt.figure()
        for cheren_fit_percents, cheren_expected_percents, label, color in plot_tuple_array:
            cheren_fit_percents = np.array(cheren_fit_percents)
            cheren_expected_percents = np.array(cheren_expected_percents)
            
            fractions = cheren_fit_percents/cheren_expected_percents
            counts, bins = np.histogram(cheren_fit_percents/cheren_expected_percents,bins=30)
            plt.stairs(counts, bins, linewidth=2, color=color, fill=True, alpha=0.7, label=label)
            plt.axvline(np.mean(fractions),linestyle='--',color=color,label=f'{label} Mean: {np.mean(fractions):.3f}')
        plt.legend()
        plt.xlabel(r"$\frac{Č_{fit}\%}{Č_{expected}\%}$")
        plt.ylabel("Counts")
        plt.title(r"$\frac{Č_{fit}\%}{Č_{expected}\%}$ Distributions for Different Sampling Rates")
        plt.show(block=False)
        input("Press enter to close...")
        plt.close()

    
