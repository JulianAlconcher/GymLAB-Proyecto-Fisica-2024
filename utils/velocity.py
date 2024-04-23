import pandas as pd
import numpy as np
import math

from utils.utils import caculate_velocity_vector, calculate_distance_between_vectors, calculate_velocity

# Este codigo lee los datos del CSV, dibuja los puntos y lineas. 
# Calcula la velocidad instantanea usando los datos normalizados del csv.
def append_velocity_to_csv():
    file_path = "pose_data.csv"  
    df = pd.read_csv(file_path)
    col_velocidad = 'velocidad_instantanea'
    col_vector_velocidad_x = 'vector_velocidad_x'
    col_vector_velocidad_y = 'vector_velocidad_y'

    window_name = 'Skeleton'


        

    for index, row in df.iterrows():
        current_frame = index

        current_row = df[df['Frame'] == current_frame]

        timestamps = current_row['TimeStamp'].tolist()
        wrist_points_normalized = [(float(row['Wrist_X_Normalized']), float(row['Wrist_Y_Normalized'])) for index, row in current_row.iterrows()]

        next_frame = current_frame + 1
        next_row = df[df['Frame'] == next_frame]

        if not next_row.empty:
            timestamps_next = next_row['TimeStamp'].tolist()
            wrist_points_next_normalized = [(float(row['Wrist_X_Normalized']), float(row['Wrist_Y_Normalized'])) for index, row in next_row.iterrows()]
        else:
            timestamps_next = None
            wrist_points_next_normalized = None

        if timestamps_next is not None and wrist_points_next_normalized is not None:
            for index, (TimeStamp_1, wrist_point_1, TimeStamp_2, wrist_point_2) in enumerate(zip(timestamps, wrist_points_normalized, timestamps_next, wrist_points_next_normalized)):
                velocidad_instantanea = calculate_velocity(calculate_distance_between_vectors(wrist_point_1, wrist_point_2), TimeStamp_1, TimeStamp_2)
                df.loc[df['Frame'] == current_frame, col_velocidad] = velocidad_instantanea
                vector_velocidad_x, vector_velocidad_y = caculate_velocity_vector(wrist_point_1, wrist_point_2, TimeStamp_1, TimeStamp_2) 
                df.loc[df['Frame'] == current_frame, col_vector_velocidad_x] = vector_velocidad_x
                df.loc[df['Frame'] == current_frame, col_vector_velocidad_y] = vector_velocidad_y

        
    df.to_csv('pose_data.csv', index=False)
    print(df)
