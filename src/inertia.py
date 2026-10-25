# from config import DRY_MASS_MOTOR,POSITION_OX_TANK,FUEL_RADIUS,OX_HEIGHT,NOZZLE_POSITION_MOTOR

# zakłada że zbiornik z utleniaczem jest wyżej od zbiornika z paliwem

# oblicza moment bezwładności suchego silnika
# zakłada że jest to walec
def motor_inertia(FUEL_RADIUS,POSITION_OX_TANK,OX_HEIGHT,DRY_MASS_MOTOR):
    Ixx = 1/12 * (3*FUEL_RADIUS**2 + (POSITION_OX_TANK + FUEL_RADIUS + 0.5*OX_HEIGHT)**2)
    Iyy = 1/12 * (3*FUEL_RADIUS**2 + (POSITION_OX_TANK + FUEL_RADIUS + 0.5*OX_HEIGHT)**2)
    Izz = 1/2  * DRY_MASS_MOTOR * FUEL_RADIUS**2
    return (Ixx,Iyy,Izz)

# oblicza położenie środka masy suchego silnika
# zadkłada że jest to walec
def motor_mass_center(NOZZLE_POSITION_MOTOR,POSITION_OX_TANK,OX_HEIGHT,FUEL_RADIUS):
    return (NOZZLE_POSITION_MOTOR + POSITION_OX_TANK + FUEL_RADIUS + OX_HEIGHT/2) / 2


def rocket_inertia():
    Ixx = 0.5
    Iyy = 0.5
    Izz = 0.5
    return (Ixx,Iyy,Izz)

def rocket_mass_center():

    return 2.5
