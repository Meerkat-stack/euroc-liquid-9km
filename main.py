from src.build import *
from src.validation import validate_flight, ValidationResult, print_requirements

env = create_standard_enviroment()
ox_tank = create_ox_tank()
fuel_tank = create_fuel_tank()
motor = create_motor(fuel_tank=fuel_tank,ox_tank=ox_tank)
rocket = create_rocket(liquid_motor=motor)
build_paraschute(rocket)
flight=simulate_flight(rocket,env)

rocket.draw()
rocket.plots.static_margin()

# flight.plots.trajectory_3d()
# flight.prints.maximum_values()
# flight.plots.attitude_data()

# flight.info()

requirements = validate_flight(flight,motor,INCLINATION,PAYLOAD_MASS,ROCKET_MASS,RAIL_LENGHT,9.81)
print_requirements(requirements)



# from rocketpy.simulation import FlightDataExporter
# FlightDataExporter(flight).export_kml(
#     file_name="./output/trajectory.kml",
#     extrude=True,
#     altitude_mode="relativetoground",
# )


