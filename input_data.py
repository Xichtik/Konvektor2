from dataclasses import dataclass
from calc import *
import pandas

class Data:
    def __init__(self, name: str):
        self.csv = pandas.read_csv(name, header=0)
        self.Plist = list(self.csv.Pressure) #Seznam tlaků
        self.Alist = list(self.csv.Altitude) #Seznam výšek
        self.Tlist = list(self.csv.Temperature) #Seznam teplot
        self.Hlist = list(self.csv.Dew_point) #Seznam rosných bodů
        self.Dlist = list(self.csv.Wind_direction) #Seznam směrů větru
        self.Slist = list(self.csv.Wind_speed) #Seznam rychlostí větru

        for i in range(len(self.Slist)): #Převod z uzlů na metry za sekundu
            self.Slist[i] = kts_ms(self.Slist[i])
    