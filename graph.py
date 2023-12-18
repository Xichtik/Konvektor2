import matplotlib.pyplot as plot
import matplotlib.ticker as ticker
from preferences import Options
from input_data import Data
from calc import *

options = Options()



def plot_emagram(data: Data) -> None:
    Emagram_fig = plot.figure(dpi = options.dpi)
    plot.figure(Emagram_fig)
    emagram = plot.subplot(111)
    emagram.axis([options.Tmin, max(data.Tlist), min(data.Alist), options.Amax]) #Nejnižší výška musí být zemský povrch (kvůli tlakové škále)

    #Tlaková škála emagramu
    pres_axis = emagram.twinx()
    pres_axis.set_ylim(data.Plist[0], alt_range(data.Plist, data.Alist, data.Alist[0], options.Amax)[-1]) #Nastavení krajních limitů tlakové osy
    pres_axis.plot(0,0) #Placeholder
    pres_axis.set_yscale('log') #Nastavení tlakové škály na logaritmickou
    pres_axis.yaxis.set_major_locator(ticker.LogLocator())
    pres_axis.yaxis.set_major_formatter(ticker.ScalarFormatter())
    pres_axis.yaxis.set_minor_formatter(ticker.LogFormatter(minor_thresholds=(1500,1500)))
    pres_axis.yaxis.grid(color = 'b', linestyle = ':', which = 'both', linewidth = 0.25)

    if options.background_curves is True:
        plot_background_curves(emagram, data, options.background_curves_interval)

    emagram.plot(data.Tlist, data.Alist, color = 'r')
    emagram.plot(data.Hlist, data.Alist, color = 'b')
    emagram.plot(data.dry_adiabat(data.Tlist[0], data.Alist[0]), data.Alist, color = 'xkcd:orange')
    emagram.plot(data.mixr_curve(data.Hlist[0]), data.Alist, color = 'xkcd:gold')
    emagram.plot(data.conv_dry_adiabat(), data.Alist, color = 'xkcd:orange')
    emagram.plot(data.sat_adiabat(data.find_LCL()[0], data.find_LCL()[1]), data.Alist, color = 'g')
    emagram.plot(data.sat_adiabat(data.find_CCL()[0], data.find_CCL()[1]), data.Alist, color = 'g')
    

    emagram.plot(data.find_LCL()[0], data.find_LCL()[1], color = 'k', marker = '_', markersize = 20)
    emagram.plot(data.find_CCL()[0], data.find_CCL()[1], color = 'k', marker = '_', markersize = 20)
    emagram.text(data.find_LCL()[0], data.find_LCL()[1], "     LCL     " + str(data.find_LCL()[1]) + 'm, ' + str(round(data.find_LCL()[0], 1)) + " °C", horizontalalignment='right')
    emagram.text(data.find_CCL()[0], data.find_CCL()[1], "     CCL     " + str(data.find_CCL()[1]) + 'm, ' + str(round(data.find_CCL()[0], 1)) + " °C", horizontalalignment='right')

    emagram.grid()
    emagram.set_ylabel("Altitude AMSL [$m$]")
    emagram.set_xlabel("Temperature [$°C$]")
    pres_axis.set_ylabel("Pressure [$hPa$]")

def plot_background_curves(emagram: plot, data: Data, interval:float) -> None:
    for t in range(-200/interval,100/interval):
            emagram.plot(data.sat_adiabat(interval*t, data.Alist[0]), data.Alist, color = 'g', linestyle = ':', linewidth = 1)
            emagram.plot(data.mixr_curve(interval*t), data.Alist, color = 'xkcd:gold', linestyle = ':', linewidth = 1)
