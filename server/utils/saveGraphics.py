import pandas as pd
import matplotlib.pyplot as plt
import os

# Cambiar el backend de matplotlib a 'Agg'
import matplotlib
matplotlib.use('Agg')

def saveGraphics():
    try:
        # Lee el archivo CSV
        data = pd.read_csv('pose_data.csv')
        
        # Verifica si las columnas de energía existen
        if 'energia_potencial' not in data.columns or 'energia_cinetica' not in data.columns or 'energia_mecanica' not in data.columns:
            print("Las columnas de energía necesarias no están presentes en el archivo CSV.")
            return False

        # Asegúrate de que la carpeta de destino existe
        output_dir = 'static'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Crea el primer gráfico de velocidad instantánea
        if 'velocidad_instantanea_suavizada' in data.columns:
            plt.plot(data['TimeStamp'], data['velocidad_instantanea_suavizada'])
            plt.xlabel('Tiempo (seg)')
            plt.ylabel('Velocidad Instantánea (m/s)')
            plt.title('Gráfico de Velocidad Instantánea')
            plt.savefig(os.path.join(output_dir, 'velocidad_instantanea_suavizada.png'))
            plt.close()

        # Crea el segundo gráfico de aceleración instantánea
        if 'aceleracion_instantanea_suavizada' in data.columns:
            plt.plot(data['TimeStamp'], data['aceleracion_instantanea_suavizada'])
            plt.xlabel('Tiempo (seg)')
            plt.ylabel('Aceleración Instantánea (m/s^2)')
            plt.title('Gráfico de Aceleración Instantánea')
            plt.savefig(os.path.join(output_dir, 'aceleracion_instantanea_suavizada.png'))
            plt.close()

        # Crea el gráfico de energías
        plt.plot(data['TimeStamp'],data['energia_potencial'], label='Energía Potencial', color='blue')
        plt.plot(data['TimeStamp'],data['energia_cinetica'], label='Energía Cinética', color='green')
        plt.plot(data['TimeStamp'],data['energia_mecanica'], label='Energía Mecánica', color='red')
        
        plt.xlabel('Tiempo (seg)')
        plt.ylabel('Energía (J)')
        plt.title('Gráfico de Energías en Función del Tiempo')
        plt.legend()

        # Guardar el gráfico de energías
        plt.savefig(os.path.join(output_dir, 'grafico_energias.png'))
        plt.close()

        print("Los gráficos se han guardado como imágenes en la carpeta /static.")
        
        return True

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return False
