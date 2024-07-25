import calc
import pandas
import math
from preferences import Const, Options
from typing import List

const = Const()
options = Options()

class Data():
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

        self.CCL = self.find_CCL()
        self.LCL = self.find_LCL()
    
    def dry_adiabat(self, temp: float, alt: float) -> List[float]: #Vrací seznam teplot suché adiabaty, která prochází souřadnicemi [temp, alt]
        return [calc.adiab_dry_lift(temp, alt, a) for a in self.Alist]
    
    def mixr_curve(self, dewp: float) -> List[float]: #Vrací seznam teplot křivky směšovacího poměru s počáteční teplotou dewp od zemského povrchu
        curve = [dewp]
        for i in range(1,len(self.Plist)):
            curve.append(calc.adiab_mixr_lift(self.Plist[i], self.Plist[i-1], curve[-1], curve[-1]))
        return curve

    def find_LCL(self) -> tuple[float, float|int]: #Vrací souřadnice (temp, alt) [°C,m] výstupné kondenzační hladiny LCL v datové řadě
        for temp, dewp, alt in zip(self.dry_adiabat(self.Tlist[0], self.Alist[0]), self.mixr_curve(self.Hlist[0]), self.Alist):
            if dewp >= temp:
                return (dewp, alt)

    def find_CCL(self) -> tuple[float, float|int]: #Vrací souřadnice (temp, alt) [°C,m] konvektivní kondenzační hladiny CCL v datové řadě
        for temp, dewp, alt in zip(self.Tlist, self.mixr_curve(self.Hlist[0]), self.Alist):
            if dewp >= temp:
                return (dewp, alt)
    
    def conv_dry_adiabat(self) -> List[float]: #Vrací seznam teplot adiabaty, která prochází konvektivní kondenzační hladinou
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

    def find_tropo1(self) -> tuple[float, float|int]: #Vrací souřadnice (temp, alt) [°C, m] první konvenční tropopauzy
        for temp, alt, pres in zip(self.Tlist, self.Alist, self.Plist):
            if max([calc.lapse_rate(temp, self.Tlist[j+1], alt, self.Alist[j+1]) for j in range(calc.list_i(alt, self.Alist), calc.list_i(alt+2000, self.Alist))]) < 2 and pres < 500:
                    break
        return (temp, alt)
            
    def check_tropo2(self, tropo_temp: float, tropo_alt: float) -> bool: #Vrací bool [True/False], zda existuje druhá konvenční tropopauza
        for temp, alt in zip(self.Tlist[calc.list_i(tropo_alt, self.Alist):], self.Alist[calc.list_i(tropo_alt, self.Alist):]):
            if min([calc.lapse_rate(temp, self.Tlist[j+1], alt, self.Alist[j+1]) for j in range(calc.list_i(alt, self.Alist)-1, calc.list_i(alt+1000, self.Alist))]) > 3:
                return True
        return False

    def find_tropo2(self) -> tuple[float, float|int]: #Vrací souřadnice (temp, alt) [°C, m] druhé konvenční tropopauzy
        if self.check_tropo2(*self.find_tropo1()) is False:
            return (-273.15,99999)
        for temp, alt in zip(self.Tlist[calc.list_i(self.find_tropo1()[1], self.Alist):], self.Alist[calc.list_i(self.find_tropo1()[1], self.Alist):]):
            if min([calc.lapse_rate(temp, self.Tlist[j+1], alt, self.Alist[j+1]) for j in range(calc.list_i(alt, self.Alist)-1, calc.list_i(alt+1000, self.Alist))]) > 3:
                for t, a in zip(self.Tlist[calc.list_i(alt, self.Alist):], self.Alist[calc.list_i(alt, self.Alist):]):
                    if max([calc.lapse_rate(t, self.Tlist[j+1], a, self.Alist[j+1]) for j in range(calc.list_i(a, self.Alist), calc.list_i(a+2000, self.Alist))]) < 2:
                        return(t, a)
        return (t, a)
        
    def stability_get(self, i) -> int: #Zjišťuje stabilitu teplotního zvrstvení v hladině s indexem i. Vrací -1 při nestabilním, 0 při labilním a 1 při stabilním zvrstvení.
        if calc.lapse_rate(calc.pot_temp_K(self.Tlist[i-options.stabDif], self.Plist[i-options.stabDif]), calc.pot_temp_K(self.Tlist[i], self.Plist[i]), self.Alist[i-options.stabDif], self.Alist[i]) > 0:
            return -1
        if calc.lapse_rate(calc.pot_temp_K(self.Tlist[i-options.stabDif], self.Plist[i-options.stabDif]), calc.pot_temp_K(self.Tlist[i], self.Plist[i]), self.Alist[i-options.stabDif], self.Alist[i]) < calc.salr(self.Tlist[i], self.Plist[i])-const.gammaD:
            return 1
        #if abs(calc.lapse_rate(calc.pot_temp_K(self.Tlist[i-options.stabDif], self.Plist[i-options.stabDif]), calc.pot_temp_K(self.Tlist[i], self.Plist[i]), self.Alist[i-options.stabDif], self.Alist[i])) <= options.stabDev:
        else:
            return 0
        #return 0
    
    def brunt_vaisala_freq(self, i) -> float:
        bvfs = (const.g/calc.theta_temp_K(self.Tlist[i], self.Hlist[i], self.Plist[i]))*calc.lapse_rate(calc.theta_temp_K(self.Tlist[i], self.Hlist[i], self.Plist[i]), calc.theta_temp_K(self.Tlist[i+1], self.Hlist[i+1], self.Plist[i+1]), self.Alist[i], self.Alist[i+1])
        try:
            return math.sqrt(bvfs)
        except:
            return -1 #raise ValueError("Brunt-Vaisala frequency negative: atmospheric conditions unstable.")
            
    def brunt_vaisala_period(self, i) -> float:
        b = self.brunt_vaisala_freq(i)
        if b>0:
            return 1/b
        else:
            return -1

    def brunt_vaisala_wavelength(self, i) -> float:
        b = self.brunt_vaisala_period(i)
        if b>=0:
            return self.Slist[i]*b
        else:
            return -1

    def CAPE(self) -> float:
        pass

