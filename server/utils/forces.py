import numpy as np
import pandas as pd

from utils.utils import calculate_forearm_weight

radius_bicep = 0.04
df = pd.read_csv('pose_data.csv')

def calculate_forces(weight=80, genre="Masculino", height=1.70, training_level="Principiante", distance_forearm=0.30, mass_weight=7.5):
    g = -9.81
    
    # Longitud del centro de masa
    radius_forearm = distance_forearm / 2
    print("radius_forearm: ", radius_forearm)
    # Obtenemos la masa del brazo
    mass_forearm = calculate_forearm_weight(weight, genre, height, training_level)
    print("mass_forearm: ", mass_forearm)
    # Calcular momento de inercia
    inertia_weight = mass_weight * distance_forearm ** 2
    inertia_forearm = mass_forearm * radius_forearm ** 2
    print("inertia_weight: ", inertia_weight)
    # Obtenemos la suma de los momentos de inercia
    sum_moment = (inertia_weight + inertia_forearm) * df['aceleracion_angular']
    print("sum_moment: ", sum_moment)
    # Obtenemos alpha (angulo entre r y F) apartir de theta. (Como son opuesto por el vertice, restamos pi - angulo (en radianes))
    angle_rad = 2
    print("angle_rad: ", angle_rad)
    angle_forearm_g = np.pi - angle_rad
    print("angle_forearm_g: ", angle_forearm_g)
    # Entonces obtenemos los momentos de los pesos.
    moment_weight = distance_forearm * mass_weight * g * np.sin(angle_forearm_g)
    moment_forearm = radius_forearm * mass_forearm * g * np.sin(angle_forearm_g)
    print("moment_weight: ", moment_weight)
    # Cálculo de la fuerza del bicep
    df['force_bicep'] = (sum_moment - moment_weight - moment_forearm) / (radius_bicep * np.sin(df['theta_wrist']))
    print("force_bicep: ", df['force_bicep'])
    # Obtenemos los componentes de vectores para graficarlos
    df['px_weight'] = 0
    df['py_weight'] = mass_weight * g

    df['px_forearm'] = 0
    df['py_forearm'] = mass_forearm * g
    
    df.to_csv('pose_data.csv', index=False)
    df.to_json('pose_data.json', orient='records')
    
    print("Done", df)