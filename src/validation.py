from dataclasses import dataclass
import numpy as np

# klasa przechowująca informacje na temat spełnienia, bądź nie danego wymogu z regulaminu
@dataclass
class ValidationResult:
    rule: str
    expected_value: float
    real_value: float
    passed: bool



# funkcja sprawdzająca zgodność parametrów z wymogami, zwraca tablice obiektów klasy ValidationResult
def validate_flight(flight,motor,inclination,payload_mass,rocket_mass,rail_lenght,g0):

    results = []

    # 9km - rakieta musi osiągnąć apogeum  co najmniej 9 km
    results.append(ValidationResult(
        rule="L9",
        expected_value=9000,
        real_value=flight.apogee-flight.env.elevation,
        passed=(flight.apogee-flight.env.elevation > 9000)
    ))


    # EuRoC-LV-RQT-0350 - Początkowy system odzysku powinien być uruchomiony w apogeum lub blisko niego.

    apogee_tolerance = 3.0      # czas na zadzialanie komputera i otwrcie się spadochronu
    stablization_time = 10.0    # czas ustabilizowania się lotu po wyzwoleniu spadochronu

    if len(flight.parachute_events) > 0:
        first_deploy_time = flight.parachute_events[0][0]  # czas wyzwolenia pierwszego spadochronu
    else:
        first_deploy_time = 0.0                            # jesli żaden sie nie otworzył

    time_diff = abs(first_deploy_time - flight.apogee_time)# Czy otworzył się w apogeum?
    
    results.append(ValidationResult(
        rule="EuRoC-LV-RQT-0350",
        expected_value=flight.apogee_time,
        real_value=first_deploy_time,
        passed=(time_diff <= apogee_tolerance)
    ))

    # EuRoC-LV-RQT-0360 - Pierwszy system odzysku powinien spowodować zredukowanie prędkości spadku do wartości od 23 do 46 m/s.
    if(first_deploy_time != 0.0):
        reduced_speed = abs(flight.vz(first_deploy_time + stablization_time))
    else:
        reduced_speed = abs(flight.vz(flight.apogee_time))

    results.append(ValidationResult(
        rule="EuRoC-LV-RQT-0360",
        expected_value=34.5,
        real_value=reduced_speed,
        passed=(23<reduced_speed<46)
    ))

    # EuRoC-LV-RQT-0370 - Odpalenie głównego systemu odzysku nie powinno się odbyć na wysokości więszkszej niż 450 nad poziomem ziemi.
    if len(flight.parachute_events) > 1:
        second_deploy_time = flight.parachute_events[1][0]  # czas wyzwolenia drugiego spadochronu
        second_deploy_height = flight.z(second_deploy_time) - flight.env.elevation # wysokość wyzwolenia drugiego spadochronu
    else:
        second_deploy_time = 0.0                            # jesli żaden sie nie otworzył lub tylko jeden
        second_deploy_height = flight.z(0.0)

    results.append(ValidationResult(
        rule="EuRoC-LV-RQT-0370",
        expected_value=450,
        real_value=second_deploy_height,
        passed=(50<second_deploy_height<450)
    ))


    # EuRoC-LV-RQT-0380 - Główny system odzysku powinien spowodować spadek prędkości opadania rakiety poniżej 9 m/s.
    
    final_speed = abs(flight.vz(second_deploy_time + stablization_time))

    results.append(ValidationResult(
        rule="EuRoC-LV-RQT-0380",
        expected_value= 9,
        real_value= final_speed,
        passed=(final_speed < 9)
    ))


    # EuRoC-LV-RQT-0860 - Ładunek musi ważyć co najmniej 1000 g. Nie ustalono górnego limitu.
    results.append(ValidationResult(
        rule="EuRoC-LV-RQT-0860",
        expected_value=1,
        real_value=payload_mass,
        passed=(payload_mass>1)
    ))

    # EuRoC-LV-RQT-1000 - Start musi sie odbyć pod kątem $84\degree \pm 1\degree$. Organizatorzy ze względów bezpieczeństwa mogą obniżyć ten kąt do maksymalnie $70\degree$.
    results.append(ValidationResult(
        rule="EuRoC-LV-RQT-1000",
        expected_value=84,
        real_value=inclination,
        passed=(84 == inclination or 70<inclination<84)
    ))

    # EuRoC-LV-RQT-1100 - Rakieta musi opuścić szynę startową z prędkością większą niż 30 m/s.
    results.append(ValidationResult(
        rule="EuRoC-LV-RQT-1100",
        expected_value=30.0,
        real_value=flight.out_of_rail_velocity,
        passed=(flight.out_of_rail_velocity > 30.0)
    ))

    # EuRoC-LV-RQT-1020 - Musi istnieć sytem który odblokuje start dopiero w momencie osiągnięcia odpoweidniego ciągu. *To się tyczy tylko silników na paliwo ciekłe i silników hybrydowych.*
    # oczekiwany ciąg początkowy oszacowany z zasady zachowania energii
    # ciąg ten musi nadać taką energię aby rakieta mogła opuścić szynę z prowadnicy z odpowiednią prędkością 30 m/s
    # zakłada przy tym że ciąg na tym odcinku jest stały oraz że opór nie gra znaczącej roli
    expected_thrust_t0 = rocket_mass*((30**2)/(2*rail_lenght) + g0*np.sin(np.radians(inclination)))
    results.append(ValidationResult(
        rule="EuRoC-LV-RQT-1020",
        expected_value= expected_thrust_t0,
        real_value= motor.thrust(0.0),
        passed=(motor.thrust(0.0) > expected_thrust_t0)
    ))

    # EuRoC-LV-RQT-1030 - Rakieta musi przez cały lot, utrzymać margines stabilności co najmniej 1.5 kalibru. Jednocześnie należy unikać zbyt dużej stabilnosci znacząco powyrzej 2 kalibrów.
    # min_stability_margin = flight.stability_margin.min

    stability_data = flight.stability_margin.source
    free_flight_margins = [
        value for time, value in stability_data 
        if flight.out_of_rail_time < time <= flight.apogee_time
    ]
    min_stability_margin = min(free_flight_margins) if free_flight_margins else 0.0

    results.append(ValidationResult(
        rule="EuRoC-LV-RQT-1030",
        expected_value=2.0,
        real_value=min_stability_margin,
        passed=(min_stability_margin > 1.5)
    ))

    return results



def print_requirements(requirements):

    for requiremnt in requirements:
        if(requiremnt.passed):
            print(requiremnt)
        else:    
            print("\033[31m",requiremnt,"\033[0m")

