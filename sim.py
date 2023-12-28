from calc import *
from input_data import *
from preferences import *
from input_data import Data

const = Const()
options = Options()


class History():
    def __init__(self):
        self.time: List[float] = []
        self.pres: List[float] = []
        self.alt: List[float] = []
        self.temp: List[float] = []
        self.dewp: List[float] = []
        self.v_x: List[float] = []
        self.v_y: List[float] = []
        self.v_z: List[float] = []
        self.b: List[float] = []
        self.cycles: List[float] = []
        self.vol: List[float] = []
        self.r: List[float] = []
        self.area: List[float] = []


class Parcel():
    def __init__(self, data: Data, pres: float, alt: float, temp: float, dewp: float, v0: float = Options.v0) -> None:    
        self.data = data

        self.time = 0
        self.pres = pres
        self.alt = alt
        self.temp = temp
        self.dewp = dewp
        self.ambi = data_at_alt(self.alt, self.data.Alist, self.data.Tlist)
        self.adew = data_at_alt(self.alt, self.data.Alist, self.data.Hlist)
        self.v_x = 0
        self.v_y = 0
        self.v_z = v0
        self.b = 0
        self.cycles = 0
        self.vol = volume_ideal_gas(self.pres, self.temp)
        self.r = radius_sphere(self.vol)
        self.area = circle_area(self.r)
        
        self.history = History()

        self.save()

    def iterate(self):

        self.update_dimensions()
        self.update_height()
        self.update_ambient()
        self.update_temperature()
        self.update_time()        

    def save(self):
        self.history.time.append(self.time)
        self.history.pres.append(self.pres)
        self.history.alt.append(self.alt)
        self.history.temp.append(self.temp)
        self.history.dewp.append(self.dewp)
        self.history.v_x.append(self.v_x)
        self.history.v_y.append(self.v_y)
        self.history.v_z.append(self.v_z)
        self.history.b.append(self.b)
        self.history.cycles.append(self.cycles)
        self.history.vol.append(self.vol)
        self.history.r.append(self.r)
        self.history.area.append(self.area)

    def simulate(self) -> None:
        while self.cycles < options.cycles:
            self.iterate()
            self.save()
            self.cycles += 1
            self.print_report()
    
    def print_report(self) -> None:
        if self.cycles % options.notif_interval == 0:
            print(str(self.cycles) + " iterations complete.")

    def update_temperature(self) -> None:
        if self.dewp < self.temp:
            self.dewp = adiab_mixr_lift(self.pres, self.history.pres[-1], self.history.temp[-1], self.history.dewp[-1])
            self.temp -= (self.alt - self.history.alt[-1])*const.gammaD/1000
        else:
            self.dewp = self.temp
            self.temp -= (self.alt - self.history.alt[-1])*salr(self.temp, self.pres)/1000
    
    def update_ambient(self) -> None:
        self.ambi = data_at_alt(self.alt, self.data.Alist, self.data.Tlist)
        self.adew = data_at_alt(self.alt, self.data.Alist, self.data.Hlist)
        self.pres = data_at_alt(self.alt, self.data.Alist, self.data.Plist)

    def update_height(self) -> None:
        self.b = accel(self.temp, virt_temp_K(self.ambi, self.adew, self.pres)) - sign(self.v_z)*drag_sphere(self.v_z, self.area, density(self.ambi, self.adew, self.pres))
        self.v_z += self.b * options.dt
        self.alt += self.v_z * options.dt

    def update_dimensions(self) -> None:
        self.vol = volume_ideal_gas(self.pres, self.temp)
        self.r = radius_sphere(self.vol)
        self.area = circle_area(self.r)

    def update_time(self) -> None:
        self.time += options.dt


