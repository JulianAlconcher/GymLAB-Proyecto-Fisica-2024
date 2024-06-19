
from utils.utils import get_kinetic_energy, get_mechanical_energy, get_potencial_energy
import pandas as pd

def append_energy_to_csv_and_json(mass_dumbel):
    print("ESTOY LLAMANDO A APPEND ENERGY TO CSV AND JSON")
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
    # Iterar sobre cada fila del DataFrame
    for index, row in df.iterrows():
        print("ADENTRO DEL FOR")
        current_frame = index
        current_row = df[df['Frame'] == current_frame]



        wrist_y_a = current_row['Wrist_Y_Normalized'].tolist()
        wrist_y = ' '.join(map(str, wrist_y_a))
        velocidad_instantanea_a= current_row['velocidad_instantanea'].tolist()
        velocidad_instantanea= ' '.join(map(str, velocidad_instantanea_a))
        
        print("HOLA ESTOY EN EL FOR SEGUNDO")
        print("velocidad_instantanea: ",velocidad_instantanea)
        print("wrist_y: ",wrist_y)

        #energia_potencial= get_potencial_energy(mass_dumbel,wrist_y)
        #print("TERMINE GET POTENCIAL ENERGY")
        #energia_cinetica= get_kinetic_energy(mass_dumbel,velocidad_instantanea)
        #energia_mecanica= get_mechanical_energy(mass_dumbel,wrist_y,velocidad_instantanea)
        #print("ENERGIAS:",energia_potencial,energia_cinetica,energia_mecanica)

        # Asignar valores al DataFrame
        df.loc[df['Frame'] == current_frame, col_energia_potencial] = 1
        df.loc[df['Frame'] == current_frame, col_energia_cinetica] = energia_cinetica
        df.loc[df['Frame'] == current_frame, col_energia_mecanica] = 1

    # Guardar el DataFrame modificado en CSV y JSON
    df.to_csv('pose_data.csv', index=False)
    df.to_json('pose_data.json', orient='records')
    return True   
