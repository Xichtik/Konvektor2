import matplotlib.pyplot as plot
import matplotlib.ticker as ticker
from preferences import Options
from input_data import Data
from calc import *
from sim import *

options = Options()


def plot_emagram(data: Data, parcel: Parcel) -> None:
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

    #emagram.plot(parcel.history.temp, parcel.history.alt, linestyle = '--', color = 'xkcd:brown')
    emagram.plot(data.Tlist, data.Alist, color = 'r', label = 'Temperature [°C]')
    emagram.plot([virt_temp_K(t, d, p)-273.15 for t, d, p in zip(data.Tlist, data.Hlist, data.Plist)], data.Alist, color = 'r', linestyle = ':', label = 'Virtual temperature [°C]')
    emagram.plot(data.Hlist, data.Alist, color = 'b', label = 'Dew point [°C]')
    emagram.plot(data.dry_adiabat(data.Tlist[0], data.Alist[0]), data.Alist, color = 'xkcd:orange', label = 'Dry adiabats')
    emagram.plot(data.mixr_curve(data.Hlist[0]), data.Alist, color = 'xkcd:gold', label = 'Isogram')
    emagram.plot(data.conv_dry_adiabat(), data.Alist, color = 'xkcd:orange')
    emagram.plot(data.sat_adiabat(data.find_LCL()[0], data.find_LCL()[1]), data.Alist, color = 'g', label = 'Saturated adiabats')
    emagram.plot(data.sat_adiabat(data.find_CCL()[0], data.find_CCL()[1]), data.Alist, color = 'g')

    
    emagram.plot(data.find_LCL()[0], data.find_LCL()[1], color = 'k', marker = '_', markersize = 20)
    emagram.plot(data.find_CCL()[0], data.find_CCL()[1], color = 'k', marker = '_', markersize = 20)
    emagram.plot(data.find_tropo1()[0], data.find_tropo1()[1], color = 'k', marker = "_", markersize = 30)
    if data.check_tropo2(*data.find_tropo1()) is True:
        emagram.plot(data.find_tropo2()[0], data.find_tropo2()[1], color = 'k', marker = "_", markersize = 30)
        emagram.text(data.find_tropo2()[0], data.find_tropo2()[1], "2nd Tropopause:   " +'\n'+ str(data.find_tropo2()[1]) + 'm, ' + str(round(data.find_tropo2()[0], 1)) + " °C   ", horizontalalignment='right', verticalalignment = 'center_baseline')
    emagram.text(data.find_LCL()[0], data.find_LCL()[1], "LCL:  " + str(data.find_LCL()[1]) + 'm, ' + str(round(data.find_LCL()[0], 1)) + " °C   ", horizontalalignment='right', verticalalignment = 'center_baseline')
    emagram.text(data.find_CCL()[0], data.find_CCL()[1], "CCL:  " + str(data.find_CCL()[1]) + 'm, ' + str(round(data.find_CCL()[0], 1)) + " °C   ", horizontalalignment='right', verticalalignment = 'center_baseline')
    emagram.text(data.find_tropo1()[0], data.find_tropo1()[1], "Tropopause:   " +'\n'+ str(data.find_tropo1()[1]) + 'm, ' + str(round(data.find_tropo1()[0], 1)) + " °C   ", horizontalalignment='right', verticalalignment = 'center_baseline')

    emagram.legend()
    emagram.grid()
    emagram.set_ylabel("Altitude AMSL [$m$]")
    emagram.set_xlabel("Temperature [$°C$]")
    pres_axis.set_ylabel("Pressure [$hPa$]")
    Emagram_fig.canvas.manager.set_window_title('Emagram')

def plot_humidity(data: Data) -> None:
    Hum_fig = plot.figure(dpi = options.dpi)
    plot.figure(Hum_fig)
    hum = plot.subplot(111)
    hum.axis([0, 100, min(data.Alist), options.Amax])

    hum.plot([rel_humi(t, d)*100 for t, d in zip(data.Tlist, data.Hlist)], data.Alist, color = 'b', label = 'Relative humidity [%]')
    hum.legend()
    hum.grid()
    hum.set_xlabel("Relative humidity [%]")
    hum.set_ylabel("Altitude AMSL [m]")
    Hum_fig.canvas.manager.set_window_title('Relative humidity')

def plot_wind(data: Data) -> None:
    Wind_fig = plot.figure(dpi = options.dpi)
    plot.figure(Wind_fig)
    wind = plot.subplot(111)
    wind.axis([0, 40, min(data.Alist), options.Amax])

    wind.plot(data.Slist, data.Alist, color = 'r', label = 'Wind speed [m/s]')
    for i in range(len(data.Alist)):
        if i%int(options.Nbarbs*options.Amax/10000) == 0:
            wind.barbs(37.5, data.Alist[i], data.Slist[i]*math.sin(wind_deg_rad(data.Dlist[i]))/const.ktstoms, data.Slist[i]*math.cos(wind_deg_rad(data.Dlist[i]))/const.ktstoms, barbcolor='k', flagcolor='k', length=6, linewidth=1)

    deg_axis = wind.twiny()
    deg_axis.set_xlim(0, 360)
    deg_axis.xaxis.set_major_locator(ticker.MultipleLocator(45))

    deg_axis.scatter(data.Dlist, data.Alist, 10, color = 'b', label = 'Wind direction [°]')
    
    wind.grid()
    wind.set_xlabel("Wind speed [m/s]")
    wind.set_ylabel("Altitude AMSL [m]")
    deg_axis.set_xlabel("Wind direction [°]")
    Wind_fig.canvas.manager.set_window_title('Wind')

def plot_hodograph(data: Data) -> None:
    Hodograph_fig = plot.figure(dpi = options.dpi)
    plot.figure(Hodograph_fig)
    hodograph = plot.subplot(111, projection = 'polar')
    hodograph.set_theta_zero_location('N')
    hodograph.set_theta_direction(-1)

    hodograph.plot(alt_range([wind_deg_rad(deg) for deg in data.Dlist], data.Alist, 0, 1050), alt_range(data.Slist, data.Alist, 0, 1050), color = 'r')
    hodograph.plot(alt_range([wind_deg_rad(deg) for deg in data.Dlist], data.Alist, 1000, 2050), alt_range(data.Slist, data.Alist, 1000, 2050), color = 'xkcd:orange')
    hodograph.plot(alt_range([wind_deg_rad(deg) for deg in data.Dlist], data.Alist, 2000, 3050), alt_range(data.Slist, data.Alist, 2000, 3050), color = 'y')
    hodograph.plot(alt_range([wind_deg_rad(deg) for deg in data.Dlist], data.Alist, 3000, 6050), alt_range(data.Slist, data.Alist, 3000, 6050), color = 'g')
    hodograph.plot(alt_range([wind_deg_rad(deg) for deg in data.Dlist], data.Alist, 6000, 9050), alt_range(data.Slist, data.Alist, 6000, 9050), color = 'b')
    hodograph.plot(alt_range([wind_deg_rad(deg) for deg in data.Dlist], data.Alist, 9000, 12000), alt_range(data.Slist, data.Alist, 9000, 12000), color = 'xkcd:violet')

    hodograph.plot(wind_deg_rad(data_at_alt(1000, data.Alist, data.Dlist)), data_at_alt(1000, data.Alist, data.Slist), color = 'k', marker = 'x', markersize = 15, linewidth = 3)
    hodograph.plot(wind_deg_rad(data_at_alt(2000, data.Alist, data.Dlist)), data_at_alt(2000, data.Alist, data.Slist), color = 'k', marker = 'x', markersize = 15, linewidth = 3)
    hodograph.plot(wind_deg_rad(data_at_alt(3000, data.Alist, data.Dlist)), data_at_alt(3000, data.Alist, data.Slist), color = 'k', marker = 'x', markersize = 15, linewidth = 3)
    hodograph.plot(wind_deg_rad(data_at_alt(6000, data.Alist, data.Dlist)), data_at_alt(6000, data.Alist, data.Slist), color = 'k', marker = 'x', markersize = 15, linewidth = 3)
    hodograph.plot(wind_deg_rad(data_at_alt(9000, data.Alist, data.Dlist)), data_at_alt(9000, data.Alist, data.Slist), color = 'k', marker = 'x', markersize = 15, linewidth = 3)
    hodograph.plot(wind_deg_rad(data_at_alt(12000, data.Alist, data.Dlist)), data_at_alt(12000, data.Alist, data.Slist), color = 'k', marker = 'x', markersize = 15, linewidth = 3)

    hodograph.text(wind_deg_rad(data_at_alt(1000, data.Alist, data.Dlist)), data_at_alt(1000, data.Alist, data.Slist), " 1", verticalalignment = 'center', fontsize = 15)
    hodograph.text(wind_deg_rad(data_at_alt(2000, data.Alist, data.Dlist)), data_at_alt(2000, data.Alist, data.Slist), " 2", verticalalignment = 'center', fontsize = 15)
    hodograph.text(wind_deg_rad(data_at_alt(3000, data.Alist, data.Dlist)), data_at_alt(3000, data.Alist, data.Slist), " 3", verticalalignment = 'center', fontsize = 15)
    hodograph.text(wind_deg_rad(data_at_alt(6000, data.Alist, data.Dlist)), data_at_alt(6000, data.Alist, data.Slist), " 6", verticalalignment = 'center', fontsize = 15)
    hodograph.text(wind_deg_rad(data_at_alt(9000, data.Alist, data.Dlist)), data_at_alt(9000, data.Alist, data.Slist), " 9", verticalalignment = 'center', fontsize = 15)
    hodograph.text(wind_deg_rad(data_at_alt(12000, data.Alist, data.Dlist)), data_at_alt(12000, data.Alist, data.Slist), " 12", verticalalignment = 'center', fontsize = 15)
    
    Hodograph_fig.canvas.manager.set_window_title('Hodograph')

def plot_stability(data: Data) -> None:
    Stab_fig = plot.figure(dpi = options.dpi)
    plot.figure(Stab_fig)
    stab = plot.subplot(111)
    stab.axis([min(data.Tlist)+273.15, max([calc.theta_temp_K(data.Tlist[i], data.Hlist[i], data.Plist[i]) for i in range(calc.list_i(options.Amax, data.Alist))])+10, min(data.Alist), options.Amax])

    stab.plot([t+273.15 for t in data.Tlist], data.Alist, color = 'r', label = 'Temperature [K]', zorder = 3)
    stab.plot([calc.pot_temp_K(t, p) for t, p in zip(data.Tlist, data.Plist)], data.Alist, color = 'xkcd:orange', label = 'Potential temperature [K]')
    stab.plot([calc.eq_temp_K(t, d, p) for t, d, p in zip(data.Tlist, data.Hlist, data.Plist)], data.Alist, color = 'xkcd:blue', label = 'Isobaric equivalent temperature [K]')
    stab.plot([calc.theta_temp_K(t, d, p) for t, d, p in zip(data.Tlist, data.Hlist, data.Plist)], data.Alist, color = 'xkcd:violet', label = 'Theta-E [K]')

    for i in range(options.stabDif, len(data.Alist)):
        if data.stability_get(i) == -1:
            stab.plot(stab.get_xlim()[1]-5, data.Alist[i], color = 'xkcd:green', marker = '_', markersize = 30)
        if data.stability_get(i) == 1:
            stab.plot(stab.get_xlim()[1]-5, data.Alist[i], color = 'xkcd:red', marker = '_', markersize = 30)
        if data.stability_get(i) == 0:
            stab.plot(stab.get_xlim()[1]-5, data.Alist[i], color = 'xkcd:gold', marker = '_', markersize = 30)

    stab.grid()
    stab.legend()
    stab.set_xlabel("Temperature [K]")
    stab.set_ylabel("Altitude AMSL [m]")
    Stab_fig.canvas.manager.set_window_title('Stability')

def plot_density(data: Data) -> None:
    Rho_fig = plot.figure(dpi = options.dpi)
    plot.figure(Rho_fig)
    rho = plot.subplot(111)
    rho.axis([0, density(data.Tlist[0], data.Hlist[0], data.Plist[0])*1.03, min(data.Alist), options.Amax])

    rho.plot([density(t, d, p) for t, d, p in zip(data.Tlist, data.Hlist, data.Plist)], data.Alist, color = 'xkcd:brown', label = 'Air density [kg/m^3]')

    rho.legend()
    rho.grid()
    rho.set_xlabel("Density [kg/m^3]")
    rho.set_ylabel("Altitude AMSL [m]")
    Rho_fig.canvas.manager.set_window_title('Air density')

def plot_background_curves(emagram: plot, data: Data, interval:float) -> None:
    for t in range(int(-200/interval),int(100/interval)):
            emagram.plot(data.sat_adiabat(interval*t, data.Alist[0]), data.Alist, color = 'g', linestyle = ':', linewidth = 1)
            emagram.plot(data.mixr_curve(interval*t), data.Alist, color = 'xkcd:gold', linestyle = ':', linewidth = 1)

def plot_parcel_temps(parcel: Parcel) -> None:
    parcel_fig = plot.figure(dpi = options.dpi)
    plot.figure(parcel_fig)
    parcel_plot = plot.subplot(111)
    parcel_plot.axis([min(parcel.history.dewp), max(parcel.history.temp), min(parcel.history.alt), max(parcel.history.alt)])
    parcel_plot.plot(parcel.history.temp, parcel.history.alt, color = 'r', label = 'Parcel temperature [°C]')
    parcel_plot.plot(parcel.history.dewp, parcel.history.alt, color = 'b', label = 'Parcel dewpoint [°C]')
    parcel_plot.legend()
    parcel_plot.grid()
    parcel_plot.set_xlabel("Temperature [°C]")
    parcel_plot.set_ylabel("Altitude AMSL [m]")
    parcel_fig.canvas.manager.set_window_title('Parcel temperature and dewpoint')

def plot_parcel_dynamics(parcel: Parcel) -> None:
    parcel_fig = plot.figure(dpi = options.dpi)
    plot.figure(parcel_fig)
    parcel_plot = plot.subplot(111)
    parcel_plot.plot(parcel.history.v_x, parcel.history.alt, label = 'v_x [m/s]')
    parcel_plot.plot(parcel.history.v_y, parcel.history.alt, label = 'v_y [m/s]')
    parcel_plot.plot(parcel.history.v_z, parcel.history.alt, label = 'v_z [m/s]')
    parcel_plot.plot(parcel.history.a_x, parcel.history.alt, label = 'a_x [m/s^2]')
    parcel_plot.plot(parcel.history.a_y, parcel.history.alt, label = 'a_y [m/s^2]')
    parcel_plot.plot(parcel.history.b, parcel.history.alt, label = 'b (a_z) [m/s^2]')
    parcel_plot.legend()
    parcel_plot.grid()
    parcel_plot.set_xlabel("Velocity [m/s] | Acceleration [m/s^2]")
    parcel_plot.set_ylabel("Altitude AMSL [m]")
    parcel_fig.canvas.manager.set_window_title('Parcel velocities and accelerations')

def plot_parcel_track(parcel: Parcel) -> None:
    Track_fig = plot.figure(dpi = options.dpi)
    plot.figure(Track_fig)
    track = plot.subplot(111, projection = 'polar')
    track.set_theta_zero_location('N')
    track.set_theta_direction(-1)
    track.plot([math.asin(s_x/(pyth(s_x, s_y)+0.001)) for s_x, s_y in zip(parcel.history.s_x, parcel.history.s_y)], [pyth(s_x, s_y) for s_x, s_y in zip(parcel.history.s_x, parcel.history.s_y)])
    Track_fig.canvas.manager.set_window_title('Parcel ground track')

def plot_parcel_climb(parcel: Parcel) -> None:
    parcel_fig = plot.figure(dpi = options.dpi)
    plot.figure(parcel_fig)
    parcel_plot = plot.subplot(111)
    parcel_plot.plot(parcel.history.v_z, parcel.history.alt, color = 'xkcd:violet', label = 'Vertical speed [m/s]')
    parcel_plot.legend()
    parcel_plot.grid()
    parcel_plot.set_xlabel("Vertical speed [m/s]")
    parcel_plot.set_ylabel("Altitude AMSL [m]")
    parcel_fig.canvas.manager.set_window_title('Parcel climb rate')

def plot_parcel_tilt(parcel: Parcel) -> None:
    parcel_fig = plot.figure(dpi = options.dpi)
    plot.figure(parcel_fig)
    parcel_plot = plot.subplot(111)
    parcel_plot.set_xlim(0, 90)
    parcel_plot.xaxis.set_major_locator(ticker.MultipleLocator(15))
    parcel_plot.plot([parcel.comp_tilt(i) for i in range(len(parcel.history.alt))], parcel.history.alt, color = 'xkcd:violet', label = 'Vertical speed [m/s]')
    parcel_plot.legend()
    parcel_plot.grid()
    parcel_plot.set_xlabel("Parcel track tilt from vertical [°]")
    parcel_plot.set_ylabel("Altitude AMSL [m]")
    parcel_fig.canvas.manager.set_window_title('Parcel track tilt')


def plot_random(xList: List[float|int], yList: List[float|int]) -> None:
    Rnd_fig = plot.figure(dpi = options.dpi)
    plot.figure(Rnd_fig)
    rnd_plot = plot.subplot(111)
    rnd_plot.plot(xList, yList)


"""
PLOT TEMPLATE
    parcel_fig = plot.figure(dpi = options.dpi)
    plot.figure(parcel_fig)
    parcel_plot = plot.subplot(111)

    parcel_plot.legend()
    parcel_plot.grid()
    parcel_plot.set_xlabel("Velocity [m/s] | Acceleration [m/s^2]")
    parcel_plot.set_ylabel("Altitude AMSL [m]")
    parcel_fig.canvas.manager.set_window_title('Parcel velocities and accelerations')

"""