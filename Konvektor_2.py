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
parcel = sim.Parcel(data, data.Plist[0], data.Alist[0], 35, data.Hlist[0], 0)


"""
parcel.simulate()
plot_parcel_alt(parcel)
print(density(data.Tlist[0], data.Hlist[0], data.Plist[0]))
"""

plot_emagram(data, parcel)
plot_humidity(data)
plot_wind(data)
plot_hodograph(data)
plot_stability(data)
plot_density(data)
print("Press Ctrl+C to close.")

plot.show()




