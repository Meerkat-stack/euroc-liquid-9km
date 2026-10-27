import argparse
from src.build import *
from src.validation import validate_flight, ValidationResult, print_requirements
from src.report import generate_flight_report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EuRoC L9 rocket simulation.")
    
    # Dodanie argumentu --mode, który pozwala na wybór trybu działania
    parser.add_argument(
        "--mode", 
        type=str, 
        choices=["standard", "optimize-fins", "historical"], 
        default="standard",
        help="Select execution mode: 'standard' for baseline simulation, 'optimize-fins' for fin geometry optimization, or 'historical' for past data analysis."    )
    parser.add_argument("--live", action="store_true", 
                        help="Execute the full optimization loop in real-time. If omitted, the script uses pre-calculated optimal fin dimensions."    
                        )
    
    args = parser.parse_args()

    # Logika wyboru na podstawie przekazanego argumentu
    if args.mode == "standard":

        flight,rocket,motor,fuel_tank,ox_tank,env = run_rocket(create_standard_enviroment,0)
        generate_flight_report(flight,rocket,motor,env)        


    elif args.mode == "optimize-fins":

        from src.optimalization import optimize_fins    

        env = create_standard_enviroment(wind_u=9.0) # Profil worst-case
        ox_tank = create_ox_tank()
        fuel_tank = create_fuel_tank()
        motor = create_motor(fuel_tank, ox_tank)
        if args.live:
            result = optimize_fins(env,motor)
            if result is None:
                print("None")
            else:
                print(result)
        """
        OptimizationResult(span=np.float64(0.14), root_chord=np.float64(0.31250000000000006), tip_chord=np.float64(0.04499999999999999), apogee=np.float64(9124.767163507555), min_stability=np.float64(1.8635413884950949), max_stability=np.float64(2.4968307580792253), out_of_rail_velocity=np.float64(31.55307420436794))
        """
        if args.live:
            span = result.span
            tip_chord = result.tip_chord
            root_chord = result.root_chord
        else:
            span = 0.14
            tip_chord = 0.044999
            root_chord = 0.312500

        flight,rocket,motor,fuel_tank,ox_tank,env = run_rocket(create_standard_enviroment,0,span,root_chord,tip_chord)
        generate_flight_report(flight,rocket,motor,env)        
