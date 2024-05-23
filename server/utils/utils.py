import math
import numpy as np

MAX_RANGE = 160
MIN_RANGE = 50
DISTANCE_MTS_ELBOW_WRIST = 0.30

def contador_repeticiones(angle, state, contador_reps):
    if angle >= MAX_RANGE and state == "down":
        state = "up"
    if angle <= MIN_RANGE and state == "up":
        state = "down"
        contador_reps += 1
    return state, contador_reps

def calcular_angulo(a0, a1, b0, b1, c0, c1):
    p = np.array([a0 - b0, a1 - b1])
    q = np.array([c0 - b0, c1 - b1])

    pq = p[0] * q[0] + p[1] * q[1]

    Mp = np.sqrt(p[0] ** 2 + p[1] ** 2)
    Mq = np.sqrt(q[0] ** 2 + q[1] ** 2)

    cos_theta = pq / (Mp * Mq)

    theta = np.arccos(cos_theta)

    angle = np.degrees(theta)

    return angle

def calculate_distance_between_vectors(v1, v2):
    if len(v1) != 2 or len(v2) != 2:
        raise ValueError("Los vectores deben tener exactamente dos elementos")
    distance = math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)
    return distance

def transform_mesaured_vector_to_mts(distance,x): 
    distance_in_mts = x * DISTANCE_MTS_ELBOW_WRIST / distance
    return distance_in_mts

def calculate_distance_between_vectors(v1, v2):
    if len(v1) != 2 or len(v2) != 2:
        raise ValueError("Los vectores deben tener exactamente dos elementos")
    distance = math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)
    return distance

def calculate_velocity(dist, time_start, time_end):
    return dist / (time_end - time_start)



def calculate_velocity_vector(v1,v2,t1,t2): 
    x_component = (v2[0] - v1[0]) / (t2 - t1) 
    y_component = (v2[1] - v1[1]) / (t2 - t1) 

    return x_component, y_component

def calculate_aceleration(variation_vel, time_start, time_end):
    return variation_vel / (time_end - time_start)

def calculate_aceleration_vector(v1,v2,t1,t2): 
    x_component = (v2[0] - v1[0]) / (t2 - t1) 
    y_component = (v2[1] - v1[1]) / (t2 - t1) 

    return x_component, y_component

def getLevelConstant(training_level):
    if(training_level == "Principiante"):
        return 0.016
    if(training_level == "Intermedio"):
        return 0.020
    if(training_level == "Avanzado"):
        return 0.024
    
def calculate_forearm_weight(weight, genre, height, training_level):
    avarage_height = 0
    if(genre == "Masculino"):
        avarage_height = 171
        forearm_weight = weight * getLevelConstant(training_level) * ((1 + (height - avarage_height)/(avarage_height)))
    if(genre == "Femenino"):
        avarage_height = 160
        forearm_weight = weight * getLevelConstant(training_level) * ((1 + (height - avarage_height)/(avarage_height)))
    return round(forearm_weight, 2)

def grades_to_radians(grades):
    return grades * (math.pi / 180)