from .validation import validate_flight,print_requirements
from .config import * 


def generate_flight_report(flight, rocket, motor, env):
    env.info()
    requirements = validate_flight(flight, motor, INCLINATION, PAYLOAD_MASS, ROCKET_MASS, RAIL_LENGHT, 9.81)
    print_requirements(requirements)
    
    flight.prints.maximum_values()
    flight.plots.stability_and_control_data()
    flight.plots.trajectory_3d()

    rocket.draw()
    flight.info()

