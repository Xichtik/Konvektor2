"""
Created on 15/12/2023 19:35 by Jindřich Novák
"""

from preferences import Const, Options
from input_data import Data
from calc import *
from graph import *
import sim

const = Const()
options = Options()
data = Data(options.csv_path)
parcel = sim.Parcel(data, data.Plist[0], data.Alist[0], data.conv_dry_adiabat()[0], data.Hlist[0], 0)
thermal = sim.Thermal(data, data.Plist[0], data.Alist[0], data.conv_dry_adiabat()[0], data.Hlist[0], 0)
column = sim.Column(data, data.Plist[0], data.Alist[0], data.conv_dry_adiabat()[0], data.Hlist[0], 0)
"""
parcel.simulate()
thermal.simulate()
column.simulate()
results = [parcel, thermal, column]
plot_parcel_dynamics(results)
plot_parcel_track(results)
plot_parcel_climb(results)
plot_parcel_tilt(results)
"""
plot_emagram(data)
"""
plot_humidity(data)
plot_wind(data)
plot_hodograph(data)
plot_stability(data)
plot_density(data)
"""
#plot_parcel_temps(parcel)

plot_BVF(data)
plot_BVP(data)
plot_BVW(data)
#plot_random(thermal.history.time, thermal.history.alt)
print("Press Ctrl+C to close.")

plot.show()




