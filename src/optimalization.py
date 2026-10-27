import numpy as np
from dataclasses import dataclass
from .build import *
# import config as config
from . import config
from .validation import print_requirements, validate_flight, requirements_passed
from .report import generate_flight_report


@dataclass
class OptimizationResult:
    span: float
    root_chord: float
    tip_chord: float
    apogee: float
    min_stability: float
    max_stability: float
    out_of_rail_velocity: float

    @property
    def is_valid(self) -> bool:
        stable = 1.5 <= self.min_stability and self.max_stability <= 2.5 
        safe_rail_exit = self.out_of_rail_velocity > 30.0
        valid_apogee = self.apogee > 7000 
        return stable and safe_rail_exit and valid_apogee


def optimize_fins_loop(spans,root_chords,tip_chords,motor,env):

    results = []

    for test_span in spans:

        print("test_span: ",test_span," ...")
        
        for test_root_chord in root_chords:
            for test_tip_chord in tip_chords:
                if test_tip_chord >= test_root_chord:
                    continue
                
                rocket = create_rocket(
                    liquid_motor=motor, 
                    span=test_span, 
                    root_chord=test_root_chord, 
                    tip_chord=test_tip_chord
                )
                
                flight = simulate_flight(rocket, env, terminate_on_apogee=True)

                stability_data = flight.stability_margin.source
                free_flight_margins = [
                    value for time, value in stability_data 
                    if flight.out_of_rail_time < time <= flight.apogee_time
                ]

                if free_flight_margins:
                    min_stab = min(free_flight_margins)
                    max_stab = max(free_flight_margins)
                else:
                    min_stab, max_stab = 0.0, 0.0

                apogee_agl = flight.apogee - env.elevation

                result = OptimizationResult(
                    span=test_span,
                    root_chord=test_root_chord,
                    tip_chord=test_tip_chord,
                    apogee=apogee_agl,
                    min_stability=min_stab,
                    max_stability=max_stab,
                    out_of_rail_velocity=flight.out_of_rail_velocity
                )

                if result.is_valid:
                    results.append(result)

    if not results:
        return None
    else:
        # best_result = min(results, key=lambda r: abs(r.apogee - 9000))
        return min(results, key=lambda r: r.apogee)



def optimize_fins(env,motor):

    spans = np.arange(0.12, 0.18, 0.02)      
    root_chords = np.arange(0.25, 0.45, 0.05)
    tip_chords = np.arange(0.02, 0.22, 0.02)

    best_result = optimize_fins_loop(spans,root_chords,tip_chords,motor,env)

    best_span = best_result.span
    best_root_chord = best_result.root_chord
    best_tip_chord = best_result.tip_chord

    spans = np.arange(max(0.02,best_span-0.02), best_span+0.02, 0.005)      
    root_chords = np.arange(max(0.02,best_root_chord-0.05), best_root_chord+0.05, 0.0125)
    tip_chords = np.arange(max(0.02,best_tip_chord-0.02), best_tip_chord+0.02, 0.005)

    best_result = optimize_fins_loop(spans,root_chords,tip_chords,motor,env)

    return best_result


def optimize_payload_mass():


    last_valid_payload = 0.0


    env = create_standard_enviroment(wind_u=0.0) # profil worst-case
    ox_tank = create_ox_tank()
    fuel_tank = create_fuel_tank()
    motor = create_motor(fuel_tank, ox_tank)



    for current_payload_mass in np.arange(1.4,10,0.1):

        print(current_payload_mass)
        
        rocket = create_rocket(motor,payload_mass=current_payload_mass)
        build_paraschute(rocket)
        flight = simulate_flight(rocket, env, terminate_on_apogee=False) 

        requirements = validate_flight(flight,motor,config.INCLINATION,current_payload_mass,rocket.mass,config.RAIL_LENGHT,9.81)

        ascent_requirements = []
        for requiremnt in requirements:
            if (requiremnt.rule in ["EuRoC-LV-RQT-1030","EuRoC-LV-RQT-1020","EuRoC-LV-RQT-1100","EuRoC-LV-RQT-0860","L9"]) == True:
                ascent_requirements.append(requiremnt)

        if requirements_passed(ascent_requirements):
            last_valid_payload = current_payload_mass
            last_ok_requirements = requirements
            last_rocket = rocket
            last_flight = flight
        else:
            break

    print("Best: ",last_valid_payload," kg")
    print_requirements(last_ok_requirements) 

    generate_flight_report(last_flight, last_rocket, motor, env)           


