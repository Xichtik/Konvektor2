"""
    ZÁKLADNÍ JEDNOTKY (pokud není komentářem stanoveno jinak):
    Výška:                m
    Teplota:              °C
    Rosný bod:            °C
    Tlak:                 hPa
    Rychlost větru:       m/s
    Směr větru:           °
    Parciální tlak:       kPa
    Směšovací poměr:      kg/kg
    Relativní vlhkost:    bezr.
    Virtuální teplota:    K
    Vert. tepl. gradient: °C/km

"""

from preferences import Const, Options
from typing import List
import math

const = Const()
options = Options()


def sign(x: float) -> int: #Zjišťuje znaménko čísla x (u kladných vrací 1, u záporných -1, u 0 vrací 0)
    if x > 0:
        return 1
    if x < 0:
        return -1
    else:
        return 0

def kts_ms(v: float) -> float: # Převádí hodnotu a v uzlech na metry za sekundu
    return v*const.ktstoms

def wind_deg_rad(w_deg: float) -> float: #Převádí w_deg ve stupních na radiány
    return -1*math.radians(180-w_deg)

def alt_range(list: List[float], altlist: List[float], bottom: float, top: float) -> List[float]: #Vrací pouze tu část seznamu, jejíž data se nacházejí mezi hladinami bottom a top
    vysledek = []
    for i in range(len(altlist)):
        if altlist[i] >= bottom and altlist[i] <= top:
            vysledek.append(list[i])
    return vysledek

def vapour_p(temp: float) -> float: #Vrací maximální parciální tlak ![kPa] nasycení vzduchu vodní parou při teplotě temp
    return 0.61121*math.exp((18.678-(temp/234.5))*(temp/(257.14+temp)))

def dewp_from_vapour_p(e: float) -> float:
    return (257.14*math.log(e/0.61121))/(18.678-math.log(e/0.61121))

def rel_humi(temp: float, dewp: float) -> float: #Vrací relativní vlhkost při teplotě temp a rosném bodu dewp
    r = vapour_p(dewp)/vapour_p(temp)
    if r > 1:
        raise ValueError("Relative humidity greater than 100%!")
    return r

def mixr(temp: float, dewp: float, pres: float) -> float: #Vrací směšovací poměr vodní páry v kg/kg při teplotě temp, rosném bodu dewp a tlaku pres
    return (rel_humi(temp, dewp)*vapour_p(temp)*const.eps)/100*(pres-vapour_p(temp))/1000

def density(temp: float, dewp: float, pres: float) -> float: #Vrací hustotu vzduchu o teplotě temp [°C], rosném bodu dewp [°C] a tlaku pres [hPa]
    return ((pres*100-vapour_p(dewp)*100)*const.Md + 100*vapour_p(dewp)*const.Mv)/(const.R*(temp+273.15))

def virt_temp_K(temp: float, dewp: float, pres: float) -> float: #Vrací virtuální teplotu v K při teplotě temp, rosném bodu dewp a tlaku pres
    s = mixr(temp, dewp, pres)/(mixr(temp, dewp, pres) + 1)
    virt_t = (temp+273.15)*(1+((const.Rv/const.Rd)-1)*s)
    if virt_t-273.15 < temp:
        raise ValueError("Virtual temperature smaller than dry bulb temperature!")
    return virt_t

def eq_temp_K(temp:float, dewp:float, pres: float) -> float: #Vrací izobarickou ekvivalentní teplotu v K při teplotě temp, rosném bodu dewp a tlaku pres
    return temp + (const.L*mixr(temp, dewp, pres)/(1000*const.cp)) + 273.15

def pot_temp_K(temp: float, pres: float) -> float: #Vrací potenciální teplotu v K při teplotě temp a tlaku pres
    return (temp + 273.15)*(1000/pres)**(const.Rd/(const.cp*1000))

def theta_temp_K(temp: float, dewp: float, pres: float) -> float: #Vrací izobarickou ekvivalentní potenciální teplotu v K při teplotě temp, rosném bodu dewp a tlaku pres
    return eq_temp_K(pot_temp_K(temp, pres)-273.15, dewp, pres)

def QNH(pres: float, alt: float) -> float: #Vrací QNH pro tlak pres naměřený ve výšce alt
    return pres*(1+((const.stdP**const.n)*0.0065*0.003472)*alt/(pres**const.n))**(1/const.n)

def QFF(pres: float, alt: float, temp: float, dewp: float) -> float: #Vrací QFF pro tlak pres naměřený ve výče alt při teplotě temp a rosném bodu dewp
    return pres*math.exp(const.g*alt/(287.04*virt_temp_K(temp, dewp, pres)))

def adiab_dry_lift(temp0: float, alt0: float, alt1: float) -> float: #Vrací teplotu částice při výstupu do hladiny alt1 z hladiny alt0 s počáteční teplotou temp0
    return temp0 - (alt1-alt0)*const.gammaD/1000

def adiab_mixr_lift(pres1: float, pres0: float, temp0: float, dewp0: float) -> float: #Vrací hodnotu rosného bodu v tlakové hladině pres při výstupu z výchozích hodnot pres0, temp0 a dewp0
    e = 100*pres1/((const.eps/mixr(temp0, dewp0, pres0)*1000)+1)
    dewp_error = dewp_from_vapour_p(100*pres0/((const.eps/mixr(temp0, dewp0, pres0)*1000)+1)) - dewp0
    return dewp_from_vapour_p(e) - dewp_error

def salr(temp: float, pres:float) -> float: #Vrací hodnotu nasyceně adiabatického vertikálního teplotního gradient (SALR = Saturated Adiabatic Lapse Rate) v °C/km pro nasycenou částici o teplotě (a tím pádem i rosném bodu) temp a tlaku pres
    cit = 1 + (const.eps*const.L*vapour_p(temp)*1000)/(const.Rd*(temp+273.15)*pres*100)
    jme = 1 + ((const.eps**2) * (const.L**2) * vapour_p(temp)*1000)/(1000*const.cp*const.Rd*pres*100*((temp+273.15)**2))
    return const.gammaD*cit/jme

def lapse_rate(t0: float, t1: float, a0: float, a1: float) -> float: #Vrací hodnotu vertikálního teplotního gradientu [°C/km] mezi hladinami a0 a a1 [m] při teplotách t0, t1 [°C]
    return (t0-t1)/(a1-a0-0.001)*1000

def data_at_alt(alt:float, Alist: List[float], Plist: List[float]) -> float: #Vrací tlak ve výšce alt
    for a, p in zip(Alist, Plist):
        if a >= alt:
            return p

def data_at_pres(pres:float, Plist: List[float], Alist: List[float]) -> float: #Vrací výšku tlakové hladiny pres
    for p, a in zip(Plist, Alist):
        if p <= pres:
            return a

def list_i(val: float, list: List[float]) -> int: #Vrací index položky val v seznamu list
    if list[0]>list[-1]:
        for i,p in enumerate(list):
            if val > p:
                break
        return i
    else:
        for i,a in enumerate(list):
            if val < a:
                break
        return i

def accel(temp: float, amb:float) -> float: #Vrací zrychlení [m/s^2] působící na částici o teplotě temp [°C] při okolní virtuální teplotě amb [K]
    return const.g*(temp-amb+273.15)/amb

def drag_sphere(v: float, S: float, rho: float) -> float: #Vrací sílu odporu vzduchu [N], působící na kouli o průřezu S [m^2] pohybující se rychlostí v [m/s] vzduchem o hustotě rho [kg/m^3]
    return const.cd*S*rho/2*v**2

def volume_ideal_gas(p: float, T: float, n: float = const.mol) -> float: #Vrací objem [m^3] ideálního plynu o látkovém množství n [mol], tlaku pres [hPa] a teplotě T [°C]
    return n*const.R*(T+273.15)/p/100

def radius_sphere(V: float) -> float: #Vrací poloměr [m] koule o objemu V [m^3]
    return math.cbrt(V*3/4/math.pi)

def circle_area(r: float) -> float: #Vrací obsah [m^2] kruhu o poloměru r [m]
    return math.pi*r**2

def pyth(a: float, b: float) -> float: #Vrací délku přepony pravpúhlého trojúhelníku o odvěsnách a,b
    return math.sqrt(a**2 + b**2)


