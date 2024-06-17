import pandas as pd
import matplotlib.pyplot as plt
import os

def saveGraphics():
    try:
        # Lee el archivo CSV
        data = pd.read_csv('pose_data.csv')
        
        # Verifica si las columnas existen
        if 'velocidad_instantanea_suavizada' not in data.columns or 'aceleracion_instantanea_suavizada' not in data.columns:
            print("Las columnas necesarias no están presentes en el archivo CSV.")
            return False

        # Asegúrate de que la carpeta de destino existe
        output_dir = 'static'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Crea el primer gráfico de velocidad instantánea
        plt.plot(data['velocidad_instantanea_suavizada'])
        plt.xlabel('Tiempo')
        plt.ylabel('Velocidad Instantánea')
        plt.title('Gráfico de Velocidad Instantánea')
        plt.savefig(os.path.join(output_dir, 'velocidad_instantanea_suavizada.png'))
        plt.close()

        # Crea el segundo gráfico de aceleración instantánea
        plt.plot(data['aceleracion_instantanea_suavizada'])
        plt.xlabel('Tiempo')
        plt.ylabel('Aceleración Instantánea')
        plt.title('Gráfico de Aceleración Instantánea')
        plt.savefig(os.path.join(output_dir, 'aceleracion_instantanea_suavizada.png'))
        plt.close()

        print("Los gráficos se han guardado como imágenes en la carpeta /static.")
        
        return True

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return False
