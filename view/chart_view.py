import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

class ChartsView(ctk.CTkFrame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.build_ui()

    def build_ui(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.canvas.draw()
        pass
 
    def plot_velocity_over_time(self, data):
        self.ax1.clear()
        self.ax1.plot(data['Frame'], np.sqrt(data['vector_velocidad_x']**2 + data['vector_velocidad_y']**2))
        self.ax1.set_title('Velocity Over Time')
        self.ax1.set_xlabel('Time (s)')
        self.ax1.set_ylabel('Velocity (m/s)')
        self.canvas.draw()

    def plot_acceleration_over_time(self, data):
        self.ax2.clear()
        self.ax2.plot(data['Frame'], data['Aceleracion'])
        self.ax2.set_title('Acceleration Over Time')
        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel('Acceleration (m/s^2)')
        self.canvas.draw()

# Dentro de la clase App
def cargar_datos_desde_csv(ruta_csv):
    # Carga los datos desde el CSV utilizando pandas
    return pd.read_csv(ruta_csv)

# Calcular la aceleración
def calcular_aceleracion(data):
    data['Aceleracion'] = data['velocidad'].diff() / data['Frame'].diff()

ruta_csv = "pose_data.csv"
datos = cargar_datos_desde_csv(ruta_csv)

# Calcular la velocidad utilizando los vectores de velocidad
datos['velocidad'] = np.sqrt(datos['vector_velocidad_x']**2 + datos['vector_velocidad_y']**2)

# Calcular aceleración
calcular_aceleracion(datos)
