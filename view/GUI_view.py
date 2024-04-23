import threading
from tkinter import filedialog
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import pandas as pd
from video_processing import get_landmarks

# Importar las vistas
from view.home_view import HomeView
#from view.charts_view import ChartsView

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):
        
        self.title("GYM Analyzer")
        
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Crear el contenedor para la columna izquierda
        self.frame_left = ctk.CTkFrame(
            master=self,
            corner_radius=0,
        )
        self.frame_left.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        # Crear el contenedor para la columna derecha
        self.frame_right = ctk.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # Agregar las vistas a la columna izquierda
        home_view = HomeView(self.frame_left)  # Asumiendo que HomeView es una clase existente
        home_view.pack(fill=ctk.BOTH, expand=True)

        # Agregar la vista de los gráficos a la columna derecha
        #charts_view = ChartsView(self.frame_right)  # Asumiendo que ChartsView es una clase existente
        #charts_view.pack(fill=ctk.BOTH, expand=True)

    def on_closing(self):
        self.destroy()
