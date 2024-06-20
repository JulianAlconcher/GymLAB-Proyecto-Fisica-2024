import pandas as pd
import numpy as np

from utils.utils import convert_joules_to_kcal

def get_work():
    file_path = "pose_data.csv"
    df = pd.read_csv(file_path)
    
    print("Calculando trabajo")
    diff_series = df['energia_mecanica'].diff()
    print("La diff es:\n", diff_series)
    df['diferencial_t'] = diff_series
    total_work = np.abs(df['diferencial_t']).sum()
    df['trabajo'] = pd.Series(total_work)
    
    calories_burned = convert_joules_to_kcal(total_work)
    df['calorias_quemadas'] = pd.Series(calories_burned)
    
    df.to_csv('pose_data.csv', index=False)
    df.to_json('pose_data.json', orient='records')
    
    return True