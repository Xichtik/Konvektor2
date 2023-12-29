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
parcel = sim.Parcel(data, data.Plist[0], data.Alist[0], 7, data.Hlist[0], 0)



parcel.simulate()

plot_emagram(data, parcel)
plot_humidity(data)
plot_wind(data)
plot_hodograph(data)
plot_stability(data)
plot_density(data)
plot_parcel_temps(parcel)
plot_parcel_dynamics(parcel)
plot_parcel_track(parcel)
plot_parcel_climb(parcel)
plot_parcel_tilt(parcel)
plot_random(parcel.history.time, parcel.history.alt)
print("Press Ctrl+C to close.")

plot.show()




