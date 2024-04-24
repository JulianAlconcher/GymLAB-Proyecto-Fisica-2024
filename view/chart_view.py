import pandas as pd
import numpy as np
import plotly.graph_objs as go
import customtkinter as ctk

class ChartsView(ctk.CTkFrame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.build_ui()

    def build_ui(self):
        # Aquí puedes agregar widgets adicionales si es necesario
        pass
 
    def plot_velocity_over_time(self, data):
        time = data['Frame']
        velocity = np.sqrt(data['vector_velocidad_x']**2 + data['vector_velocidad_y']**2)
        velocity_trace = go.Scatter(x=time, y=velocity, mode='lines', name='Velocity')
        layout = go.Layout(title='Velocity Over Time', xaxis=dict(title='Time (s)'), yaxis=dict(title='Velocity (m/s)'))
        fig = go.Figure(data=[velocity_trace], layout=layout)
        fig.update_layout(title="Velocity Over Time")
        fig.show()

    def plot_acceleration_over_time(self, data):
        time = data['Frame']
        acceleration = data['Aceleracion']
        acceleration_trace = go.Scatter(x=time, y=acceleration, mode='lines', name='Acceleration')
        layout = go.Layout(title='Acceleration Over Time', xaxis=dict(title='Time (s)'), yaxis=dict(title='Acceleration (m/s^2)'))
        fig = go.Figure(data=[acceleration_trace], layout=layout)
        fig.update_layout(title="Acceleration Over Time")
        fig.show()

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

# Llama a los métodos correspondientes en ChartsView para generar los gráficos
chart_view = ChartsView()  
chart_view.plot_velocity_over_time(datos)
chart_view.plot_acceleration_over_time(datos)
