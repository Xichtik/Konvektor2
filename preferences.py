from dataclasses import dataclass

@dataclass
class Const:

    # --- PŘEVODY JEDNOTEK ---
    ktstoms = 0.5144444 #Převodní poměr mezi uzly a metry za sekundu
    n = 0.190284 #Koeficient pro výpočet QNH

    # --- STANDARDNÍ ATMOSFÉRA
    stdRho = 1.225 #Hustota vzduchu na hladině moře dle mezinárodní standardní atmosféry 
    stdP = 1013.25 #Tlak na střední hladině moře dle mezinárodní standardní atmosféry
    stdTC = 15 #Teplota ve °C na střední hladině moře dle mezinárodní standardní atmosféry
    stdTK = stdTC + 273.15 #Teplota v K na střední hladině moře dle mezinárodní standardní atmosféry


    # --- VLASTNOSTI PLYNŮ ---
    cp = 1.006 #Izobarická měrná tepelná kapacita vzduchu
    cv = 0.718 #Izochorická měrná tepelná kapacita vzduchu
    kappa = cp/cv #Poissonova konstanta
    L = 2501000 #Měrné skupenské teplo vypařování vody za normálních podmínek
    Md = 0.0289652 #Molární hmotnost suchého vzduchu
    Mv = 0.018016 #Molární hmotnost vodní páry
    R = 8.31446 #Molární plynová konstanta
    Rv = 461.5 #Měrná plynová konstanta pro vodní páru
    Rd = 287.04 #Měrná plynová konstanta pro suchý vzduch
    eps = Rd/Rv #Poměr měrných plynových konstant
       

    # --- SIMULACE ---
    cd = 0.47 #Součinitel aerodynamického odporu koule
    k = 0.052 #Součinitel vnitřního tření konvektivní částice
    mol = 1 #Látkové množství vzduchu simulované částice
    opt = 3 #Konstanta pro výpočet rychlosti stoupání dle učebnice (default 3)

    # --- RŮZNÉ ---
    g = 9.80665 #Tíhové zrychlení zemské
    gammaD = g/cp #Sucho-adiabatický vertikální teplotní gradient

@dataclass
class Options:

    csv_path = "./data/RAW_11747_2021-06-24_1200.csv"

    # --- SIMULACE ---
    dt = 0.01   #Časový krok pro simulace
    sim_secs = 6000   #Simulovaná doba v sekundách
    cycles = int(sim_secs/dt)   #Počet iterací simulace
    simUntilCCL = False #Při hodnotě True se simulace automaticky zastaví při dostoupání částice do kondenzační hladiny
    notif_interval = 50000   #Interval, po kolika iteracích se printuje oznámení
    
    v0 = 0   #Počáteční vertikální rychlost konvektivní částice
    virtv0 = 0   #Počáteční vertikální rychlost konvektivní částice při výpočtech s virtuální teplotou
    speedInterval = 0.05   #Rychlostní krok, o který se zvyšuje počáteční vertikální rychlost konvektivní částice
    

    # --- ZOBRAZENÍ ---
    dpi = 60 #Rozlišení grafů v DPI
    Nbarbs = 30   #Vykreslovat šipku větru pro každý Nbarbs-tý datový bod
    showNEL = False #Zobrazovat NEL?

    Tmin = -30   #Nejnižší teplota emagramu
    Tmax = "auto"   #Nejvyšší teplota emagramu. Nastavením na "auto" se automaticky nastaví nejvyšší teplota datové řady zvýšená o 1°C.
    Amax = 10000   #Nejvyšší výška emagramu

    background_curves = True #Zobrazovat standardní adiabaty do pozadí?
    background_curves_interval = 2 #Vykreslovat adiabaty do pozadí každých x °C

    # --- VÝPOČET ---
    CCLlimit = 400 #Nejnižší povolená výska konvektivní kondenzační hladiny
    stabDev = -0.4 #Při kladných hodnotách bude zvrstvení hodnoceno jako více stabilní, při záporných jako méně stabilní
    stabDif = 5 #Výškový krok mezi srovnávanými hladinami při určování stability teplotního zvrstvení

    
    

    
    
    


    