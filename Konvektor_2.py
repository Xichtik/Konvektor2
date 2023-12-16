"""
Created on 15/12/2023 19:35 by Jindřich Novák
"""

from preferences import Const, Options
from input_data import Data
from calc import *
from graph import *

const = Const()
options = Options()
data = Data(options.csv_path)


plot_emagram(data)

plot.show()


print(salr(34, alt_pres(5000, data.Alist, data.Plist)))


