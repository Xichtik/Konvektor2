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

"""



from preferences import Const
from typing import List
import math

const = Const()

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

def alt_range(list: List, altlist: List, bottom: float, top: float) -> List: #Vrací pouze tu část seznamu, jejíž data se nacházejí mezi hladinami bottom a top
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

def virt_temp_K(temp: float, dewp: float, pres: float) -> float: #Vrací virtuální teplotu v K při teplotě temp, rosném bodu dewp a tlaku pres
    s = mixr(temp, dewp, pres)/(mixr(temp, dewp, pres) + 1)
    virt_t = (temp+273.15)*(1+((const.Rv/const.Rd)-1)*s)
    if virt_t-273.15 < temp:
        raise ValueError("Virtual temperature smaller than dry bulb temperature!")
    return virt_t

def QNH(pres: float, alt: float) -> float: #Vrací QNH pro tlak pres naměřený ve výšce alt
    return pres*(1+((const.stdP**const.n)*0.0065*0.003472)*alt/(pres**const.n))**(1/const.n)

def QFF(pres: float, alt: float, temp: float, dewp: float) -> float: #Vrací QFF pro tlak pres naměřený ve výče alt při teplotě temp a rosném bodu dewp
    return pres*math.exp(const.g*alt/(287.04*virt_temp_K(temp, dewp, pres)))

def adiab_dry_lift(temp0: float, alt0: float, alt1: float) -> float: #Vrací teplotu částice při výstupu do hladiny alt1 z hladiny alt0 s počáteční teplotou temp0
    return temp0 - (alt1-alt0)*const.gammaD/1000

def adiab_mixr_lift(pres1: float, pres0: float, temp0: float, dewp0: float) -> float: #Vrací hodnotu rosného bodu v tlakové hladině pres při výstupu z výchozích hodnot pres0, temp0 a dewp0
    e = 100*pres1/((const.eps/mixr(temp0, dewp0, pres0)*1000)+1)
    return dewp_from_vapour_p(e)





