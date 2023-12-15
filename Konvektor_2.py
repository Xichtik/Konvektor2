"""
Created on 15/12/2023 19:35 by Jindřich Novák
"""

from preferences import Const, Options
from input_data import Data
from calc import *

const = Const()
options = Options()
data = Data(options.csv_path)




print(adiab_mixr_lift(500, 1000, 15, 15))


