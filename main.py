from src.build import *

env = create_standard_enviroment()
ox_tank = create_ox_tank()
fuel_tank = create_fuel_tank()
motor = create_motor(fuel_tank=fuel_tank,ox_tank=ox_tank)
rocket = create_rocket(liquid_motor=motor)

rocket.draw()
