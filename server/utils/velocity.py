import pandas as pd
from utils.utils import calculate_velocity_vector, calculate_distance_between_vectors, calculate_velocity, grades_to_radians

max_velocity = 0

def append_velocity_to_csv_and_json():
    global max_velocity

    file_path = "pose_data.csv"
    df = pd.read_csv(file_path)
    
    col_velocidad = 'velocidad_instantanea'
    col_vector_velocidad_x = 'vector_velocidad_x'
    col_vector_velocidad_y = 'vector_velocidad_y'
    col_velocidad_angular = 'velocidad_angular'

    # Asegurarse de que las columnas existen
    if col_velocidad not in df.columns:
        df[col_velocidad] = 0.0
    if col_vector_velocidad_x not in df.columns:
        df[col_vector_velocidad_x] = 0.0
    if col_vector_velocidad_y not in df.columns:
        df[col_vector_velocidad_y] = 0.0
    if col_velocidad_angular not in df.columns:
        df[col_velocidad_angular] = 0.0

    # Iterar sobre cada fila del DataFrame
    for index, row in df.iterrows():
        current_frame = index

        current_row = df[df['Frame'] == current_frame]
        timestamps = current_row['TimeStamp'].tolist()
        wrist_points_normalized = [(float(row['Wrist_X_Normalized']), float(row['Wrist_Y_Normalized'])) for _, row in current_row.iterrows()]
        angles = current_row['Angle'].tolist()

        next_frame = current_frame + 1
        next_row = df[df['Frame'] == next_frame]

        if not next_row.empty:
            timestamps_next = next_row['TimeStamp'].tolist()
            wrist_points_next_normalized = [(float(row['Wrist_X_Normalized']), float(row['Wrist_Y_Normalized'])) for _, row in next_row.iterrows()]
            angles_next = next_row['Angle'].tolist()
        else:
            timestamps_next = None
            wrist_points_next_normalized = None
            angles_next = None

        if timestamps_next is not None and wrist_points_next_normalized is not None and angles_next is not None:
            for _, (TimeStamp_1, wrist_point_1, TimeStamp_2, wrist_point_2, angle_1, angle_2) in enumerate(zip(timestamps, wrist_points_normalized, timestamps_next, wrist_points_next_normalized, angles, angles_next)):
                # Calcular velocidad instantánea y vector de velocidad
                velocidad_instantanea = calculate_velocity(calculate_distance_between_vectors(wrist_point_1, wrist_point_2), TimeStamp_1, TimeStamp_2)
                if velocidad_instantanea > max_velocity:
                    max_velocity = velocidad_instantanea

                vector_velocidad_x, vector_velocidad_y = calculate_velocity_vector(wrist_point_1, wrist_point_2, TimeStamp_1, TimeStamp_2)

                # Calcular velocidad angular
                velocidad_angular = grades_to_radians(calculate_velocity(angle_2 - angle_1, TimeStamp_1, TimeStamp_2))

                # Asignar valores al DataFrame
                df.loc[df['Frame'] == current_frame, col_velocidad] = velocidad_instantanea
                df.loc[df['Frame'] == current_frame, col_vector_velocidad_x] = vector_velocidad_x
                df.loc[df['Frame'] == current_frame, col_vector_velocidad_y] = vector_velocidad_y
                df.loc[df['Frame'] == current_frame, col_velocidad_angular] = velocidad_angular

    # Guardar el DataFrame modificado en CSV y JSON
    df.to_csv('pose_data.csv', index=False)
    df.to_json('pose_data.json', orient='records')

    print(df)

def get_max_velocity():
    return max_velocity
