import numpy as np
import pandas as pd
import math as math

from utils.utils import calculate_forearm_weight

def calculate_forces(weight=80, genre="Masculino", height=1.70, training_level=1, distance_forearm=0.30, mass_weight=7.5):
    radius_bicep = 0.04
    df = pd.read_csv('pose_data.csv')
    print("Inicio calculo de fuerzas con el siguiente df: ", df)
    print("El peso de la mancuera es: ", mass_weight)
    print("El peso de la persona es: ", weight)
    print("La altura de la persona es: ", height)
    print("La distancia entre el hombro y la muneca es: ", distance_forearm)
    print("El nivel de entrenamiento es: ", training_level)
    print("El genero es: ", genre)
    
    max_force = 0
    g = -9.81
    
    # Longitud del centro de masa
    radius_forearm = distance_forearm / 2
    
    # Obtenemos la masa del brazo
    mass_forearm = calculate_forearm_weight(weight, genre, height, training_level)
   
    # Calcular momento de inercia
    inertia_weight = mass_weight * distance_forearm ** 2
    inertia_forearm = mass_forearm * radius_forearm ** 2

    # Inicializar la lista para almacenar las fuerzas del bíceps
    bicep_forces = []
    
    # Obtenemos alpha (angulo entre r y F) apartir de theta. (Como son opuesto por el vertice, restamos pi - angulo (en radianes))
    for index, row in df.iterrows():
                
        current_frame = index
        current_row = df[df['Frame'] == current_frame]

        aceleration_column = current_row['aceleracion_angular'].tolist()
        angular_aceleration = ' '.join(map(str,aceleration_column))
        angular_aceleration_float = float(angular_aceleration)
        
        # Obtenemos la suma de los momentos de inercia
        sum_moment = (inertia_weight + inertia_forearm) * angular_aceleration_float
        
        angle_column = current_row['Angle'].tolist()        
        angle = ' '.join(map(str,angle_column))
        angle_float = float(angle)
        angle_rad = math.radians(angle_float)
        
        # Angulo entre el antebrazo y la gravedad
        angle_forearm_g = np.pi - angle_rad
        
        # Entonces obtenemos los momentos de los pesos.
        moment_weight = distance_forearm * mass_weight * g * np.sin(angle_forearm_g)
        moment_forearm = radius_forearm * mass_forearm * g * np.sin(angle_forearm_g)
        
        # # Cálculo de la fuerza del bicep
        force_bicep = (sum_moment - moment_weight - moment_forearm) / (radius_bicep * np.sin(angle_rad))        
        if(force_bicep > max_force):
            max_force = force_bicep
        bicep_forces.append(force_bicep)       

    # Agregar la lista de fuerzas como una nueva columna en el DataFrame
    df['fuerza_bicep'] = bicep_forces
    print("Termino calculo de fuerzas, la fuerza MAXIMA ALCANZADA ES : ", max_force)
    df['max_fuerza_bicep'] = pd.Series([max_force] + [np.nan] * (len(df) - 1))
    
    average_force = df['fuerza_bicep'].mean()
    print("El promedio de la fuerza del bíceps es: ", average_force)
    df['average_fuerza_bicep'] = pd.Series([average_force] + [np.nan] * (len(df) - 1))
    
    df.to_csv('pose_data.csv', index=False)
    df.to_json('pose_data.json', orient='records')
    
    
    return True