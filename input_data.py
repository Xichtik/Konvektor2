import calc
import pandas
from typing import List

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
            self.Slist[i] = calc.kts_ms(self.Slist[i])
    
    def dry_adiabat(self, temp: float, alt: float) -> List[float]: #Vrací seznam teplot suché adiabaty, která prochází souřadnicemi [temp, alt]
        return [calc.adiab_dry_lift(temp, alt, a) for a in self.Alist]
    
    def mixr_curve(self, dewp: float) -> List[float]: #Vrací seznam teplot křivky směšovacího poměru s počáteční teplotou dewp od zemského povrchu
        curve = [dewp]
        for i in range(1,len(self.Plist)):
            curve.append(calc.adiab_mixr_lift(self.Plist[i], self.Plist[i-1], curve[-1], curve[-1]))
        return curve

    def find_LCL(self) -> tuple[float, float|int]:
        for temp, dewp, alt in zip(self.dry_adiabat(self.Tlist[0], self.Alist[0]), self.mixr_curve(self.Hlist[0]), self.Alist):
            if dewp >= temp:
                return (dewp, alt)

    def find_CCL(self) -> tuple[float, float|int]:
        for temp, dewp, alt in zip(self.Tlist, self.mixr_curve(self.Hlist[0]), self.Alist):
            if dewp >= temp:
                return (dewp, alt)
    
    def conv_dry_adiabat(self) -> List[float]:
        return self.dry_adiabat(self.find_CCL()[0], self.find_CCL()[1])
    
    def sat_adiabat(self, dewp: float, alt: float) -> List[float]: #Vrací seznam teplot nasycené adiabaty procházející souřadnicemi [temp, alt]
        curve = [dewp]
        i = calc.list_i(alt, self.Alist)-1
        while i >= 0:
            new_t = curve[-1] - calc.salr(curve[-1], self.Plist[i])/1000*(self.Alist[i]-self.Alist[i+1])
            curve.append(new_t)
            i -= 1
        curve.reverse()
        for i in range(calc.list_i(alt, self.Alist)+1, len(self.Plist)):
            new_t = curve[-1] - calc.salr(curve[-1], self.Plist[i])/1000*(self.Alist[i]-self.Alist[i-1])
            if new_t > -250:
                curve.append(new_t)
            else:
                curve.append(-250)
        return curve


