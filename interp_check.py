import matplotlib.pyplot as plt
import numpy as np
import ROOT
from fit_class import simulation_fitter
from scipy import integrate

scint_profile = "profiles/scintillation_profile.root"
cheren_profile = "profiles/cherenkov_profile.root"
df_data = None
df_scint_photons = None
df_cheren_photons = None

sf = simulation_fitter(scint_profile, cheren_profile, df_data, df_scint_photons, df_cheren_photons)

scint_interp, cheren_interp = sf.get_interpolators()

cmap = plt.get_cmap('cool')
T = np.linspace(sf.xmin, sf.xmax, 1024)
f_array = [1.0, .95, .90, .85, .80]
for i,f in enumerate(f_array):
    
    vals  = np.array([((f*scint_interp.Eval(t))+((1-f)*cheren_interp.Eval(t))) for t in T])

    y = integrate.cumulative_trapezoid(vals,T,initial=0)
    
    color = cmap(i/(len(f_array)-1))
    plt.plot(T,y,color=color,label=f"f: {f}")

plt.legend()
plt.xlabel("Time")
plt.ylabel(r"$\int_0^t f*S(t) + (1-f)*C(t) dt$")
plt.title(r"$\int_0^t f*S(t) + (1-f)*C(t) dt$ for Different $f$ Values")
plt.show(block=False)
input("Press enter to continue...")
plt.close()

plt.figure()
for i,f in enumerate(f_array):
    
    vals  = np.array([((f*scint_interp.Eval(t))+((1-f)*cheren_interp.Eval(t))) for t in T])

    
    color = cmap(i/(len(f_array)-1))
    plt.plot(T,vals,color=color,label=f"f: {f}")

plt.legend()
plt.xlabel("Time (ns)")
plt.ylabel(r"$f*S(t) + (1-f)*Č(t)$")
plt.title(r"$f*S(t) + (1-f)*Č(t)$ for Different $f$ values")
plt.show(block=False)
input("Press enter to continue...")
plt.close()

plt.figure()
for i,f in enumerate(f_array):

    vals  = np.array([((f*scint_interp.Eval(t))+((1-f)*cheren_interp.Eval(t))) for t in T])

    derivative = np.gradient(vals, T)
    color = cmap(i/(len(f_array)-1))
    plt.plot(T,derivative,color=color,label=f"f: {f}")

plt.legend()
plt.xlabel("Time (ns)")
plt.ylabel(r"$\frac{d}{dt} f*S(t) + (1-f)*Č(t)$")
plt.title(r"$\frac{d}{dt} f*S(t) + (1-f)*Č(t)$ for Different $f$ values")

plt.xlim(0, 40)
plt.tight_layout()
plt.show(block=False)
input("Press enter to continue...")
plt.close()



