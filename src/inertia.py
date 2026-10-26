
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



DELTA = 0.27    # wyokość modułów: PAYLOAD,RECOVERY,AWIONICS

def rocket_inertia(ROCKET_MASS,NOSE_LENGHT,NOSE_POSITION,NOSE_MASS,RECOVERY_MASS,PAYLOAD_MASS,AVIONICS_MASS,BODY_MASS,ROCKET_RADIUS,ROCKET_MASS_CENTER):

    z_avionics = NOSE_POSITION-NOSE_LENGHT-5/2*DELTA - ROCKET_MASS_CENTER
    z_payload = z_avionics + DELTA 
    z_recovery = z_payload + DELTA 
    z_nose = NOSE_POSITION - 3/4*NOSE_LENGHT - ROCKET_MASS_CENTER
    z_body = (NOSE_POSITION-NOSE_LENGHT)/2 - ROCKET_MASS_CENTER

    # 1/12 m(3r**2+h**2)
    I_avionics = 1/12*AVIONICS_MASS*(3*ROCKET_RADIUS**2 + DELTA**2)
    I_payload = 1/12*PAYLOAD_MASS*(3*ROCKET_RADIUS**2 + DELTA**2)
    I_recovery = 1/12*RECOVERY_MASS*(3*ROCKET_RADIUS**2 + DELTA**2)
    I_body = 1/12*BODY_MASS*(3*ROCKET_RADIUS**2 + (NOSE_POSITION-NOSE_LENGHT)**2)
    # głowica traktowana jako stożek, wszystki inne elementy jako jednorodne walce
    # 3/20(mr**2 + mh**2)
    I_nose = 3/20*NOSE_MASS*(ROCKET_RADIUS**2 + NOSE_LENGHT**2)
    
    Ixx = (I_avionics+AVIONICS_MASS*z_avionics**2) + (I_payload+PAYLOAD_MASS*z_payload**2) + (I_recovery+RECOVERY_MASS*z_recovery**2)
    Ixx += (I_body+BODY_MASS*z_body**2) + (I_nose+NOSE_MASS*z_nose**2) 

    Iyy = (I_avionics+AVIONICS_MASS*z_avionics**2) + (I_payload+PAYLOAD_MASS*z_payload**2) + (I_recovery+RECOVERY_MASS*z_recovery**2)
    Iyy += (I_body+BODY_MASS*z_body**2) + (I_nose+NOSE_MASS*z_nose**2) 

    Izz = 0.5*(ROCKET_MASS)*ROCKET_RADIUS**2

    return (Ixx,Iyy,Izz)



def rocket_mass_center(ROCKET_MASS,NOSE_LENGHT,NOSE_POSITION,NOSE_MASS,RECOVERY_MASS,PAYLOAD_MASS,AVIONICS_MASS,BODY_MASS):
    p_nose = (NOSE_POSITION-NOSE_LENGHT)*NOSE_MASS
    p_recovery = (NOSE_POSITION - NOSE_LENGHT - DELTA/2) * RECOVERY_MASS
    p_payload = (NOSE_POSITION - NOSE_LENGHT - 3*DELTA/2) * PAYLOAD_MASS
    p_avionics = (NOSE_POSITION - NOSE_LENGHT - 5*DELTA/2) * AVIONICS_MASS
    p_body = (NOSE_POSITION - NOSE_LENGHT) * BODY_MASS / 2

    return (p_nose + p_recovery + p_payload + p_avionics + p_body) / ROCKET_MASS


