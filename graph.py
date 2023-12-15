import matplotlib.pyplot as plot
import matplotlib.ticker as ticker
from preferences import Options
from input_data import Data

options = Options()

def plot_emagram(data: Data):
    Emagram_fig = plot.figure(dpi = options.dpi)
    plot.figure(Emagram_fig)
    emagram = plot.subplot(111)
    emagram.axis([min(data.Tlist), max(data.Tlist), min(data.Alist), max(data.Alist)]) #Nejnižší výška musí být zemský povrch (kvůli tlakové škále)

    pres_axis = emagram.twinx()
    pres_axis.set_ylim(data.Plist[0], data.Plist[-1]) #Nastavení krajních limitů tlakové osy
    pres_axis.plot(0,0) #Placeholder
    pres_axis.set_yscale('log') #Nastavení tlakové škály na logaritmickou
    pres_axis.yaxis.set_major_locator(ticker.LogLocator())
    pres_axis.yaxis.set_major_formatter(ticker.ScalarFormatter())
    pres_axis.yaxis.set_minor_formatter(ticker.LogFormatter(minor_thresholds=(1500,1500)))
    pres_axis.yaxis.grid(color = 'b', linestyle = ':', which = 'both', linewidth = 0.25)

    emagram.plot(data.Tlist, data.Alist, color = 'r')

    emagram.grid()
    emagram.set_ylabel("Altitude AMSL [$m$]")
    emagram.set_xlabel("Temperature [$°C$]")
    pres_axis.set_ylabel("Pressure [$hPa$]")

