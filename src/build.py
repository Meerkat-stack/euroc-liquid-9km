from .config import *
import datetime


from rocketpy import Environment

# tworzy i zwraca standardową atmosferę bez wiatru
def create_standard_enviroment(wind_u):
    env = Environment(latitude=LATITUDE, longitude=LONGITUDE, elevation=ELEVATION)
    env.set_date(DATE) 
    env.set_atmospheric_model(type="standard_atmosphere", wind_u=wind_u, wind_v=0.0)
    return env


def create_tomorrow_enviroment():
    env = Environment(latitude=LATITUDE,longitude=LONGITUDE,elevation=ELEVATION)

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    env.set_date(
        (tomorrow.year,tomorrow.month,tomorrow.day,12)
    )
    env.set_atmospheric_model(type='Forecast', file='GFS')  
    return env




from rocketpy import Fluid, CylindricalTank, MassFlowRateBasedTank

# tworzy i zwraca zbiornik utleniacza
def create_ox_tank():
    oxidizer_fluid = Fluid(name=OX_LIQUID, density=OX_DENSITY) 
    ox_geometry = CylindricalTank(radius_function=OX_RADIUS,height=OX_HEIGHT,spherical_caps=True)
    ox_tank = MassFlowRateBasedTank(
        name="Oxidizer Tank",            
        geometry=ox_geometry,            
        flux_time=OX_FLUX_TIME,                  
        initial_liquid_mass=OX_INITIAL_LIQUID_MASS,        
        initial_gas_mass=OX_INITIAL_GAS_MASS,            
        liquid_mass_flow_rate_in=OX_LIQUID_MASS_FLOW_RATE_IN,    
        liquid_mass_flow_rate_out=OX_LIQUID_MASS_FLOW_RATE_OUT,   
        gas_mass_flow_rate_in=OX_GAS_MASS_FLOW_RATE_IN,       
        gas_mass_flow_rate_out=OX_GAS_MASS_FLOW_RATE_OUT,      
        liquid=oxidizer_fluid,
        gas=Fluid(name=OX_GAS_NAME, density=OX_GAS_DENSITY)  
    )
    return ox_tank

# tworzy i zwraca zbiornik paliwa
def create_fuel_tank():
    fuel_fluid = Fluid(name=FUEL_LIQUID, density=FUEL_DENSITY)     
    fuel_geometry = CylindricalTank(radius_function=FUEL_RADIUS, height=FUEL_HEIGHT, spherical_caps=True )
    fuel_tank = MassFlowRateBasedTank(
        name="Fuel Tank",
        geometry=fuel_geometry,
        flux_time=FUEL_FLUX_TIME,
        initial_liquid_mass=FUEL_INITIAL_LIQUID_MASS,         
        initial_gas_mass=FUEL_INITIAL_GAS_MASS,
        liquid_mass_flow_rate_in=FUEL_LIQUID_MASS_FLOW_RATE_IN,
        liquid_mass_flow_rate_out=FUEL_LIQUID_MASS_FLOW_RATE_OUT,   
        gas_mass_flow_rate_in=FUEL_GAS_MASS_FLOW_RATE_IN,
        gas_mass_flow_rate_out=FUEL_GAS_MASS_FLOW_RATE_OUT,
        liquid=fuel_fluid,
        gas=Fluid(name=FUEL_GAS_NAME, density=FUEL_GAS_DENSITY) 
    )
    return fuel_tank




from rocketpy import LiquidMotor

# przyjmuje obiekty zbiorników
# tworzy i zwraca obiekt silnika
def create_motor(fuel_tank,ox_tank):
    liquid_motor = LiquidMotor(
        coordinate_system_orientation="nozzle_to_combustion_chamber",
        thrust_source=THRUST_SOURCE_MOTOR,     
        dry_mass=DRY_MASS_MOTOR,               
        center_of_dry_mass_position=CENTER_OF_DRY_MASS_POSITION_MOTOR, 
        dry_inertia=DRY_INERTIA_MOTOR,         
        nozzle_radius=NOZZLE_RADIUS_MOTOR,     
        nozzle_position=NOZZLE_POSITION_MOTOR  
    )

    liquid_motor.add_tank(tank=fuel_tank, position=POSITION_FUEL_TANK) 
    liquid_motor.add_tank(tank=ox_tank, position=POSITION_OX_TANK) 
    return liquid_motor



from rocketpy import Rocket


def create_rocket(liquid_motor, span=FINS_SPAN, root_chord=FINS_ROOT_CHORD, tip_chord=FINS_TIP_CHORD):
    # definicja suchej masy (bez silnika)
    rocket = Rocket(
        radius=ROCKET_RADIUS,  
        mass=ROCKET_MASS,     
        inertia=ROCKET_INERTIA,
        center_of_mass_without_motor=ROCKET_MASS_CENTER,   
        power_off_drag=ROZKET_DRAG_POWER_OFF,    
        power_on_drag=ROZKET_DRAG_POWER_ON,     
        coordinate_system_orientation="tail_to_nose" 
    )

    # głowica
    nose_cone = rocket.add_nose(length=NOSE_LENGHT,kind=NOSE_KIND,position=NOSE_POSITION)
    # stateczniki
    fins = rocket.add_trapezoidal_fins(n=FINS_COUNT,root_chord=root_chord,tip_chord=tip_chord,span=span,sweep_length=FINS_SWEEP_LENGHT,position=FINS_POSITION)
    # zwężenie ogonowe (tail)
    tail = rocket.add_tail(top_radius=TAIL_TOP_RADIUS,bottom_radius=TAIL_BOTTOM_RADIUS,length=TAIL_LENGHT,position=TAIL_POSTITION)
    # położenie silnika w rakiecie
    rocket.add_motor(motor=liquid_motor,position=MOTOR_POSITION)
    # prowadnice
    rail_buttons = rocket.set_rail_buttons(upper_button_position=UPPER_BUTTON_POSITION,lower_button_position=LOWER_BUTTON_POSITION,angular_position=45)

    return rocket


# funkcja wyzwalająca spadochron główny
def main_trigger(p, h, y):
    return True if y[5] < 0 and h < 440 else False

# funkcja dodająca spadochrony do rakiety
def build_paraschute(rocket):

    # definicja spadochronu pilotowego
    drogue = rocket.add_parachute(
        name="Drogue",         
        cd_s=1.56,             # wyznaczony współczynnik oporu
        trigger="apogee",      # istnieje gotowy wyzwalacz spadochronu na apogeum, można równie dobrze podać tutaj tą funkcję
        sampling_rate=105,     # częstotliwość próbkowania (tu 105 Hz, typowa wartość dla COTS)
        lag=1.5,               # opóźnienie pomiędzy sygnałem wyzwolenia spadochronu a pelnym napełnieniem czaszy spadochronuaszy [s]
        noise=(0, 8.3, 0.5)    # symulacja szumu czujnika
                            # jak nic nie podać to szum nie zostanie uwzględniony
                            # wartość ta bierze się z noty katalogowej odpowiedniego czujnika (barometru) z jakiego korzysta rakieta
    )


    # definicja spadochronu głównego
    main = rocket.add_parachute(
        name="Main",
        cd_s=13.5,             # ponownie wyznaczony współczynnik
        trigger=main_trigger,  # funkcja wyzwalająca spadochron
        sampling_rate=105,     # cześtotliwośc próbkowania
        lag=2.0                # główny spadochron otwiera się wolniej, bo jest zwyczajnie większy
    )


from rocketpy import Flight

# funkcja syulująca lot
def simulate_flight(rocket,env,terminate_on_apogee=TERMINATE_ON_APOGEE):
    
    flight = Flight(rocket=rocket,environment=env,rail_length=RAIL_LENGHT,inclination=INCLINATION,heading=HEADIN,terminate_on_apogee=terminate_on_apogee)

    return flight



def run_rocket(env_func,wind_u,span=FINS_SPAN, root_chord=FINS_ROOT_CHORD, tip_chord=FINS_TIP_CHORD):
    env = env_func(wind_u)
    ox_tank = create_ox_tank()
    fuel_tank = create_fuel_tank()
    motor = create_motor(fuel_tank=fuel_tank,ox_tank=ox_tank)
    rocket = create_rocket(liquid_motor=motor,span=FINS_SPAN, root_chord=FINS_ROOT_CHORD, tip_chord=FINS_TIP_CHORD)
    build_paraschute(rocket)
    flight=simulate_flight(rocket,env)

    return flight,rocket,motor,fuel_tank,ox_tank,env






