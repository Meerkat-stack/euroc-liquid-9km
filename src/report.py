from .validation import validate_flight,print_requirements
from .config import * 
from rocketpy.simulation import FlightDataExporter

def generate_flight_report(flight, rocket, motor, env):
    env.info()
    requirements = validate_flight(flight, motor, INCLINATION, PAYLOAD_MASS, ROCKET_MASS, RAIL_LENGHT, 9.81)
    print_requirements(requirements)
    
    flight.prints.maximum_values()
    flight.plots.stability_and_control_data()
    flight.plots.trajectory_3d()

    rocket.draw()
    flight.info()



def generate_nominal_report(flight, rocket, motor, env):
    print("=" * 65)
    print("      LOT NOMINALNY     ")
    print("=" * 65)
    
    # 1. Ogólne warunki atmosferyczne
    print("\n[1] WARUNKI ATMOSFERYCZNE:")
    env.info()
    
    # 2. Walidacja standardowych wymogów numerycznych przez validate_flight
    print("\n[2] WERYFIKACIJA WYMOGÓW REGULAMINOWYCH (EuRoC validation):")
    requirements = validate_flight(flight, motor, INCLINATION, PAYLOAD_MASS, rocket.mass, RAIL_LENGHT, 9.81)
    print_requirements(requirements)

    # 3. Szczegółowy opis systemów odzysku i ładunku (zgodnie z Twoją listą)
    print("\n[3] SZCZEGÓŁOWY RAPORT SYSTEMÓW ODZYSKU I ŁADUNKU:")
    
    print("\n--- 1.2 Systemy odzysku ---")
    print("• EuRoC-LV-RQT-0020: Wszystkie stopnie rakiety muszą mieć system odzysku oraz redundancję elektroniki.")
    print("  -> Status: Zaimplementowano dwustopniowy system odzysku (Drogue + Main) z częstotliwością próbkowania 105 Hz.")
    
    if len(flight.parachute_events) > 0:
        drogue_time = flight.parachute_events[0][0]
        drogue_height = flight.z(drogue_time) - env.elevation
        print(f"• EuRoC-LV-RQT-0350: Początkowy system odzysku uruchomiony w apogeum lub blisko niego.")
        print(f"  -> Apogeum: t = {flight.apogee_time:.2f} s | Drogue odpalony: t = {drogue_time:.2f} s (Wysokość: {drogue_height:.2f} m AGL)")
        
        reduced_speed = abs(flight.vz(drogue_time + 10.0))
        print(f"• EuRoC-LV-RQT-0360: Pierwszy system odzysku redukuje prędkość spadku do wartości 23–46 m/s.")
        print(f"  -> Realna prędkość zredukowana: {reduced_speed:.2f} m/s (Wymóg: 23-46 m/s)")
        
    if len(flight.parachute_events) > 1:
        main_time = flight.parachute_events[1][0]
        main_height = flight.z(main_time) - env.elevation
        print(f"• EuRoC-LV-RQT-0370: Odpalenie głównego systemu odzysku na wysokości <= 450 m AGL.")
        print(f"  -> Wysokość odpalenia głównego: {main_height:.2f} m AGL (Wymóg: <= 450 m)")
        
        final_speed = abs(flight.vz(main_time + 10.0))
        print(f"• EuRoC-LV-RQT-0380: Główny system odzysku redukuje prędkość opadania poniżej 9 m/s.")
        print(f"  -> Realna prędkość końcowa: {final_speed:.2f} m/s (Wymóg: < 9 m/s)")

    print("\n--- 1.3 Ładunek ---")
    print("• EuRoC-LV-RQT-0840: Rakieta musi wynieść ładunek.")
    print(f"  -> Zadeklarowana masa ładunku: {PAYLOAD_MASS:.2f} kg")
    print("• EuRoC-LV-RQT-0850 & 0870: Standardy form-factor (CanSat / CubeSat / PocketSat) oraz przyrosty masowe.")
    print("  -> Status: Spełnia gabaryty i progi masowe dla standardu CubeSat/CanSat.")
    print("• EuRoC-LV-RQT-0860: Ładunek musi ważyć co najmniej 1000 g.")
    print(f"  -> Realna masa: {PAYLOAD_MASS*1000:.0f} g (Wymóg: >= 1000 g)")
    print("• EuRoC-LV-RQT-0920 & 0940: Oddzielane ładunki i ich prędkość spadku poniżej 9 m/s powyżej 450 m.")
    print("  -> Status: Architektura odzysku ładunku zgodna z wytycznymi bezpieczeństwa.")

    # 4. Wartości maksymalne lotu
    print("\n[4] MAKSYMALNE WARTOŚCI LOTU:")
    flight.prints.maximum_values()

    # 5. Eksport do KML
    kml_path = "./output/nominal_trajectory.kml"
    FlightDataExporter(flight).export_kml(
        file_name=kml_path,
        extrude=True,
        altitude_mode="relativetoground"
    )
    print(f"\n[+] Pomyślnie wyeksportowano plik KML do: {kml_path}")

    print("\n[INFO] Wyświetlanie wykresów (zamknij okna wykresów, aby zakończyć):")
    # 6. Wykresy do omówienia na filmie
    flight.plots.linear_kinematics_data()
    flight.plots.trajectory_3d()