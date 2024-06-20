
from utils.utils import get_forearm_Y, get_kinetic_energy, get_mechanical_energy, get_potencial_energy
import pandas as pd

def append_energy_to_csv_and_json(mass_dumbel, mass_forearm):
    file_path = "pose_data.csv"
    df = pd.read_csv(file_path)
    
    col_energia_potencial = 'energia_potencial'
    col_energia_cinetica = 'energia_cinetica'
    col_energia_mecanica = 'energia_mecanica'


    # Asegurarse de que las columnas existen
    if col_energia_potencial not in df.columns:
        df[col_energia_potencial] = 0.0
    if col_energia_cinetica not in df.columns:
        df[col_energia_cinetica] = 0.0
    if col_energia_mecanica not in df.columns:
        df[col_energia_mecanica] = 0.0


    for index, row in df.iterrows():
        current_frame = index
        current_row = df[df['Frame'] == current_frame]

        wrist_y_a = current_row['Wrist_Y_Normalized'].tolist()
        wrist_y = ' '.join(map(str, wrist_y_a))
        wrist_y_float = float(wrist_y)
        
        elbow_y_a = current_row['Elbow_Y_Normalized'].tolist()
        elbow_y = ' '.join(map(str, elbow_y_a))
        elbow_y_float = float(elbow_y)
        
        forearm_y = get_forearm_Y(elbow_y_float, wrist_y_float)
        
        velocidad_instantanea_a= current_row['velocidad_instantanea'].tolist()
        velocidad_instantanea= ' '.join(map(str, velocidad_instantanea_a))
        velocidad_instantanea_float = float(velocidad_instantanea)

        energia_potencial= get_potencial_energy(mass_dumbel,wrist_y_float) + get_potencial_energy(mass_forearm,forearm_y)
        energia_cinetica= get_kinetic_energy(mass_dumbel,velocidad_instantanea_float) + get_kinetic_energy(mass_forearm,velocidad_instantanea_float)
        energia_mecanica= energia_potencial + energia_cinetica

        # Asignar valores al DataFrame
        df.loc[df['Frame'] == current_frame, col_energia_potencial] = energia_potencial
        df.loc[df['Frame'] == current_frame, col_energia_cinetica] = energia_cinetica
        df.loc[df['Frame'] == current_frame, col_energia_mecanica] = energia_mecanica

    # Guardar el DataFrame modificado en CSV y JSON
    df.to_csv('pose_data.csv', index=False)
    df.to_json('pose_data.json', orient='records')
    return True   
