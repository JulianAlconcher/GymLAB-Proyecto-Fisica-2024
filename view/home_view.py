import threading
from PIL import Image, ImageTk
from tkinter import filedialog
import customtkinter as ctk
import cv2
import pandas as pd

from video_processing import get_landmarks

class HomeView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.build_ui()

    def build_ui(self):

        # Configurar columnas del contenedor (self) para expandirse
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        options_frame = ctk.CTkFrame(master = self, 
                                     fg_color="transparent",
                                     )

        # Etiqueta y combobox para seleccionar el ejercicio        
        self.label_ejercicio = ctk.CTkLabel(options_frame, text="Ejercicio:")
        self.label_ejercicio.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.ejercicio_options = ["Curl de biceps", "Sentadilla", "Banco plano", "Banco inclinado"]
        self.combobox_ejercicio = ctk.CTkComboBox(options_frame, values=self.ejercicio_options)
        self.combobox_ejercicio.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Etiqueta y botón para seleccionar un video
        self.label_video = ctk.CTkLabel(options_frame, text="Video:")
        self.label_video.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.selected_video = ctk.StringVar()
        self.selected_video.set("Seleccionar")
        self.button_browse = ctk.CTkButton(options_frame, textvariable=self.selected_video, command=self.browse_video)
        self.button_browse.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Etiqueta y campo de entrada para el peso
        self.label_peso = ctk.CTkLabel(options_frame, text="Peso:")
        self.label_peso.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.entry_peso = ctk.CTkEntry(options_frame, state="disabled")
        self.entry_peso.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.entry_peso.bind("<KeyRelease>", self.enable_send_button)

        # Botón de enviar
        self.button_send = ctk.CTkButton(options_frame, text="Enviar", command=self.show_video_frame)
        self.button_send.grid(row=1, columnspan=2, padx=10, pady=5)
        self.button_send.grid_remove()  # Ocultar el botón al inicio

        # Barra de progreso
        self.progressbar = ctk.CTkProgressBar(options_frame, orientation="horizontal", mode="indeterminate", determinate_speed=0.1, border_width=1, corner_radius=20, height=20)
        self.progressbar.grid(row=5, columnspan=2, padx=10, pady=5)
        self.progressbar.grid_remove()  # Ocultar la barra de progreso al inicio

        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)

        options_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="nesw")  

        self.video_frame = ctk.CTkFrame(self, corner_radius=10, width=854, height=480)
        self.video_frame.grid(row=1, padx=0, pady=5, sticky="nesw")

        self.video_label = ctk.CTkLabel(self.video_frame, text="")
        self.video_label.pack()
        self.video_frame.grid_remove()  # Ocultar el marco al inicio


        self.repeticiones = ctk.CTkLabel(self, text="Repeticiones: 0")
        self.repeticiones.grid(row=5, columnspan=2, padx=10, pady=5)
        self.repeticiones.grid_remove()

        self.velocidad = ctk.CTkLabel(self, text="Velocidad: 0")
        self.velocidad.grid(row=6, columnspan=2, padx=10, pady=5)
        self.velocidad.grid_remove()

    def browse_video(self):
        filename = filedialog.askopenfilename(filetypes=[("Video files", "*.MOV;*.MP4;*.AVI")])
        if filename:
            self.video_cap = cv2.VideoCapture(filename)
            self.selected_video.set(filename.split("/")[-1])  
            self.entry_peso.configure(state="normal")  

            # Configurar la barra de progreso
            self.progressbar.set(0)
            self.progressbar.grid()  
            self.progressbar.start()
            
            # Iniciar el proceso de detección de puntos de referencia en un hilo separado
            threading.Thread(target=self.start_landmark_detection, args=(filename,)).start()

    def enable_send_button(self, event=None):
        peso = self.entry_peso.get()
        if peso.isdigit():
            self.button_send.configure("NORMAL")
        else:
            self.button_send.configure("DISABLED")

    def show_video_frame(self):
        self.video_frame.grid(row=4, columnspan=2, padx=10, pady=5, sticky="nesw")  # Mostrar el marco del video
        self.process_frame()  # Comenzar a procesar el video cuando se muestra el marco

    def start_landmark_detection(self, video_path):
        # Llamar a la función para iniciar la detección de puntos de referencia
        get_landmarks(video_path)
        self.progressbar.grid_remove()  # Ocultar la barra de progreso
        self.button_send.grid(row=3, columnspan=2, padx=10, pady=5)

    def process_frame(self):
        ret, frame = self.video_cap.read()
        if ret:
            frame = cv2.resize(frame, (854, 480))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.current_frame = Image.fromarray(frame)
            self.current_frame = ImageTk.PhotoImage(image=self.current_frame)
            self.video_label.configure(image=self.current_frame)
            self.video_label.image = self.current_frame  # Mantener referencia a la imagen
            self.calculate_scale_factors()  # Calcular los factores de escala
            self.plot_points_on_video(frame)
            self.video_label.after(10, self.process_frame)  # Llama a process_frame después de 10ms para reproducir el video
        else:
            self.video_cap.release()  

    def calculate_scale_factors(self):
        # Factores de escala para las coordenadas x e y
        self.scale_x = 854 / 1920
        self.scale_y = 480 / 1080

    def plot_points_on_video(self, frame):
        # Cargar datos desde el archivo CSV en un DataFrame
        file_path = "pose_data.csv"  
        df = pd.read_csv(file_path)

        self.repeticiones.grid()
        self.velocidad.grid()

        # Obtener las coordenadas de las articulaciones del frame actual
        shoulder_points = [(int(row['Shoulder_X']) * self.scale_x, int(row['Shoulder_Y']) * self.scale_y) for index, row in df[df['Frame'] == self.video_cap.get(cv2.CAP_PROP_POS_FRAMES)].iterrows()]
        elbow_points = [(int(row['Elbow_X']) * self.scale_x, int(row['Elbow_Y']) * self.scale_y) for index, row in df[df['Frame'] == self.video_cap.get(cv2.CAP_PROP_POS_FRAMES)].iterrows()]
        wrist_points = [(int(row['Wrist_X']) * self.scale_x, int(row['Wrist_Y']) * self.scale_y) for index, row in df[df['Frame'] == self.video_cap.get(cv2.CAP_PROP_POS_FRAMES)].iterrows()]

        # Dibujar círculos para cada articulación en el frame actual
        for shoulder_point, elbow_point, wrist_point in zip(shoulder_points, elbow_points, wrist_points):
            cv2.circle(frame, (int(shoulder_point[0]), int(shoulder_point[1])), 5, (0, 255, 0), -1)  # Dibujar círculo para hombro
            cv2.circle(frame, (int(elbow_point[0]), int(elbow_point[1])), 5, (0, 0, 255), -1)         # Dibujar círculo para codo
            cv2.circle(frame, (int(wrist_point[0]), int(wrist_point[1])), 5, (255, 0, 0), -1)         # Dibujar círculo para muñeca
        
        # Dibujar líneas conectando los puntos de las articulaciones
        for shoulder_point, elbow_point, wrist_point in zip(shoulder_points, elbow_points, wrist_points):
            cv2.line(frame, (int(shoulder_point[0]), int(shoulder_point[1])), (int(elbow_point[0]), int(elbow_point[1])), (0, 255, 255), 2) # Línea del hombro al codo
            cv2.line(frame, (int(elbow_point[0]), int(elbow_point[1])), (int(wrist_point[0]), int(wrist_point[1])), (255, 255, 0), 2)    # Línea del codo a la muñeca

            # Calcular punto intermedio para la curva Bezier
            mid_point = ((elbow_point[0] + wrist_point[0]) // 2, (elbow_point[1] + wrist_point[1]) // 2)
            control_point = (int(elbow_point[0]), int(mid_point[1]))  # Convertir las coordenadas a números enteros

            # Dibujar curva Bezier
            cv2.line(frame, (int(elbow_point[0]), int(elbow_point[1])), (int(mid_point[0]), int(mid_point[1])), (0, 255, 0), 2)  # Línea del codo al punto medio
            cv2.line(frame, (int(mid_point[0]), int(mid_point[1])), (int(wrist_point[0]), int(wrist_point[1])), (0, 255, 0), 2)  # Línea del punto medio a la muñeca

            # Mostrar el ángulo
            
            angles = [int(row['Angle']) for index, row in df[df['Frame'] == self.video_cap.get(cv2.CAP_PROP_POS_FRAMES)].iterrows()]
            angle = angles[0] if angles else None
            reps=[int(row['Reps']) for index, row in df[df['Frame'] == self.video_cap.get(cv2.CAP_PROP_POS_FRAMES)].iterrows()]
            velocidad=[float(row['velocidad_instantanea']) for index, row in df[df['Frame'] == self.video_cap.get(cv2.CAP_PROP_POS_FRAMES)].iterrows()]           
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(frame, f'Angulo: {angle}', (int(elbow_point[0]) + 10, int(elbow_point[1])), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


            # Actualizar el label con las repeticiones
            if reps:
                self.repeticiones.configure(text=f"Repeticiones: {reps[0]}")
            if velocidad:
                self.velocidad.configure(text=f"Velocidad: {round(velocidad[0],2)}m/s")

   
       # Convertir el frame modificado a formato adecuado para mostrar en la GUI
        frame_with_points = Image.fromarray(frame)
        frame_with_points = ImageTk.PhotoImage(image=frame_with_points)
        
        # Configurar el label para mostrar el frame con los puntos dibujados
        self.video_label.configure(image=frame_with_points)
        self.video_label.image = frame_with_points  # Mantener referencia a la imagen
