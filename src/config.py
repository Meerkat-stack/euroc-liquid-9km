from .inertia import motor_inertia, motor_mass_center, rocket_inertia, rocket_mass_center
# data section
# NazwaParametru_v od value

###---enviroment---###
LATITUDE = 39 + 23/60 + 24.53/3600   # 39°23'24.53"N
LONGITUDE = 8 + 17/60 + 21.23/3600   # 8°17'21.23"W
ELEVATION = 160                      # [m] AGL
DATE = (2027,10,25,12)               # przyszłoroczne zwody


###---tanks---###
OX_LIQUID = "Lox"                      # utleniacz
OX_DENSITY = 1141                    # gęstość utleniacza
OX_RADIUS = 0.080                     # promień wewnętrzny zbiornika z utleniaczem
OX_HEIGHT = 0.650                     # wyoskość zbiornika z utleniaczem
OX_FLUX_TIME = 15                   # czas działąnia silnika
OX_INITIAL_LIQUID_MASS = 12.3        # początkowa masa utleniacza
OX_INITIAL_GAS_MASS = 0.089           # początkowa masa gazów w zbiorniku z utleniaczem
OX_LIQUID_MASS_FLOW_RATE_IN = 0.0   # tępo przybywania utleniacza
OX_LIQUID_MASS_FLOW_RATE_OUT = 0.800  # tępo ubywania utleniacza
OX_GAS_MASS_FLOW_RATE_IN = 0.0      # tepo przybywania gazów w zbiorniku z utleniaczem
OX_GAS_MASS_FLOW_RATE_OUT = 0.0     # tepo ubywania gazów w zbiorniku z utleniaczem
OX_GAS_NAME = "N2"                    # gaz w zzbiornku z utleniaczem
OX_GAS_DENSITY = 74.0                # gęstość gazu w zbiorniku z utleniaczem
FUEL_LIQUID = "Ethanol"                      # paliwo
FUEL_DENSITY = 789                    # gęstość paliwa
FUEL_RADIUS = 0.080                     # promień wewnętrzny zbiornika z paliwem
FUEL_HEIGHT = 0.551                     # wyoskość zbiornika z paliwem
FUEL_FLUX_TIME = 15                   # czas działąnia silnika
FUEL_INITIAL_LIQUID_MASS = 6.89        # początkowa masa paliwa
FUEL_INITIAL_GAS_MASS = 0.074           # początkowa masa gazów w zbiorniku z paliwem
FUEL_LIQUID_MASS_FLOW_RATE_IN = 0.0   # tępo przybywania paliwa
FUEL_LIQUID_MASS_FLOW_RATE_OUT = 0.400  # tępo ubywania paliwa
FUEL_GAS_MASS_FLOW_RATE_IN = 0.0      # tepo przybywania gazów w zbiorniku z paliwem
FUEL_GAS_MASS_FLOW_RATE_OUT = 0.0     # tepo ubywania gazów w zbiorniku z paliwem
FUEL_GAS_NAME = "N2"                    # gaz w zzbiornku z paliwem
FUEL_GAS_DENSITY = 74.0                # gęstość gazu w zbiorniku z paliwem


###---motor---###
# ciąg w funkcji czasu
THRUST_SOURCE_MOTOR = [(0,4000),(0.5,5000),(1,5000),(3,3000),(4,3000),(5.4,1500),(6.5,1500),(9,3000),(12,3000),(14,4500),(15,0)]
DRY_MASS_MOTOR = 15.0                        # masa suchego silnika [kg]
NOZZLE_RADIUS_MOTOR = 0.0700                   # promień dyszy wylotowej [m]
NOZZLE_POSITION_MOTOR = 0.0                 # położenie dyszy wylotowej [m]
POSITION_FUEL_TANK = 0.600                    # położenie zbiornika z paliwem [m]
POSITION_OX_TANK = 1.50                      # położenie zbiornika z utleniaczem [m]
# środek ciężkości suchego silnika [m]
CENTER_OF_DRY_MASS_POSITION_MOTOR = motor_mass_center(NOZZLE_POSITION_MOTOR,POSITION_OX_TANK,OX_HEIGHT,FUEL_RADIUS)     
# moment bezwładności suchego silnika 
DRY_INERTIA_MOTOR = motor_inertia(FUEL_RADIUS,POSITION_OX_TANK,OX_HEIGHT,DRY_MASS_MOTOR)           


###---rocket---###
ROCKET_RADIUS = 0.0900             # zewnętrzny promień rakiety


NOSE_LENGHT = 0.7               # długość noska
NOSE_KIND = "vonKarman"         # kształt noska
NOSE_POSITION = 3.5             # położenie noska

PAYLOAD_MASS = 1.4                 # masa ładunku
NOSE_MASS = 2.0                  # masa głowicy
BODY_MASS = 37.0                   # masa samej obudowy
RECOVERY_MASS = 3.0                # masa systemu odzysku
AVIONICS_MASS = 1.0                # masa awioniki
ROCKET_MASS =PAYLOAD_MASS+NOSE_MASS+BODY_MASS+RECOVERY_MASS+AVIONICS_MASS  # masa rakiety z ładunkiem
ROCKET_MASS_CENTER = rocket_mass_center(ROCKET_MASS,NOSE_LENGHT,NOSE_POSITION,NOSE_MASS,RECOVERY_MASS,PAYLOAD_MASS,
                                        AVIONICS_MASS,BODY_MASS)        # środek cięzkości rakiety bez silnika
ROCKET_INERTIA = rocket_inertia(ROCKET_MASS,NOSE_LENGHT,NOSE_POSITION,NOSE_MASS,RECOVERY_MASS,PAYLOAD_MASS,AVIONICS_MASS,
                                BODY_MASS,ROCKET_RADIUS,ROCKET_MASS_CENTER)  # moment bezwładności rakiety
ROZKET_DRAG_POWER_OFF = 0.45     # współczynnik oporu powietrza rakiety
ROZKET_DRAG_POWER_ON = 0.45      # współczynnik oporu powietrza rakietyROCKET_MASS_CENTER = rocket_mass_center(ROCKET_MASS,NOSE_LENGHT,NOSE_POSITION,NOSE_MASS,RECOVERY_MASS,PAYLOAD_MASS,AVIONICS_MASS,BODY_MASS)        # środek cięzkości rakiety bez silnika


FINS_COUNT = 4                  # liczba stateczników
FINS_ROOT_CHORD = 0.35           # długość stateczników przy korpusie
FINS_TIP_CHORD = 0.12            # długość zewnętrzenj krawędzi stateczniów
FINS_SPAN = 0.14                 # szerokość stateczników
FINS_SWEEP_LENGHT = 0.18          # przesunięcie stateczników
FINS_POSITION = 0.35             # położenie stateczinków

TAIL_TOP_RADIUS = 0.09           # górny promień ogona
TAIL_BOTTOM_RADIUS = 0.08        # dolny promień ogogna
TAIL_LENGHT = 0.02               # długość ogona
TAIL_POSTITION = 0.0            # położenie ogona

MOTOR_POSITION = 0.0            # umiejscowienie silnika  w rakiecie

LOWER_BUTTON_POSITION = 1.0     # położenie dolnego zaczepu prowadnicy
UPPER_BUTTON_POSITION = 2.5     # położenie górnego zaczepu prowadnicy


###---simulation---###

RAIL_LENGHT = 12.0              # długość szyny startowej
INCLINATION = 84                # kąt podczas stortowy
HEADIN = 148                     # azymut
TERMINATE_ON_APOGEE = False     # Czy przerwać symulacje w apogeum?
