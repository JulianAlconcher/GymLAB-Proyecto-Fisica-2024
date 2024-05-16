import pandas as pd

from utils.utils import calculate_aceleration, calculate_aceleration_vector, calculate_distance_between_vectors


def append_aceleration_to_csv_and_json():
    file_path = "pose_data.csv"
    df = pd.read_csv(file_path)
    col_aceleracion = 'aceleracion_instantanea'
    col_vector_aceleracion_x = 'vector_aceleracion_x'
    col_vector_aceleracion_y = 'vector_aceleracion_y'

    # Iterar sobre cada fila del DataFrame
    for index, row in df.iterrows():
        current_frame = index

        current_row = df[df['Frame'] == current_frame]
        timestamps = current_row['TimeStamp'].tolist()
        vector_velocidad_v1 = [(float(row['vector_velocidad_x']), float(row['vector_velocidad_y'])) for _, row in current_row.iterrows()]

        next_frame = current_frame + 1
        next_row = df[df['Frame'] == next_frame]

        if not next_row.empty:
            timestamps_next = next_row['TimeStamp'].tolist()
            vector_velocidad_v2 = [(float(row['vector_velocidad_x']), float(row['vector_velocidad_y'])) for _, row in next_row.iterrows()]
        else:
            timestamps_next = None
            vector_velocidad_v2 = None

        if timestamps_next is not None and vector_velocidad_v2 is not None:
            for _, (TimeStamp_1, v1, TimeStamp_2, v2) in enumerate(zip(timestamps, vector_velocidad_v1, timestamps_next, vector_velocidad_v2)):
                aceleracion_instantanea = calculate_aceleration(calculate_distance_between_vectors(v1, v2), TimeStamp_1, TimeStamp_2)
                vector_aceleracion_x, vector_aceleracion_y = calculate_aceleration_vector(v1, v2, TimeStamp_1, TimeStamp_2)

                df.loc[df['Frame'] == current_frame, col_aceleracion] = aceleracion_instantanea
                df.loc[df['Frame'] == current_frame, col_vector_aceleracion_x] = vector_aceleracion_x
                df.loc[df['Frame'] == current_frame, col_vector_aceleracion_y] = vector_aceleracion_y

    # Guardar el DataFrame modificado en CSV y JSON
    df.to_csv('pose_data.csv', index=False)
    df.to_json('pose_data.json', orient='records')

    print(df)
