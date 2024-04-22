import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2
import mediapipe as mp
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
from multiprocessing import Process

MAX_RANGE= 160
MIN_RANGE= 50

class VideoPlayerApp:
    def __init__(self, master):
        self.master = master
        master.title("Reproductor de Video")
        self.process_running = False  # Bandera para indicar si el proceso está en ejecución

        # ComboBox con las opciones
        self.label_ejercicio = tk.Label(master, text="Ejercicio:")
        self.label_ejercicio.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.ejercicio_options = ["Curl de biceps", "Sentadilla", "Banco plano", "Banco inclinado"]
        self.combobox_ejercicio = ttk.Combobox(master, values=self.ejercicio_options)
        self.combobox_ejercicio.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.combobox_ejercicio.bind("<<ComboboxSelected>>", self.enable_video_selection)

        # Etiqueta y botón para seleccionar un video
        self.label_video = tk.Label(master, text="Video:")
        self.label_video.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.selected_video = tk.StringVar()
        self.selected_video.set("Seleccionar")
        self.button_browse = tk.Button(master, textvariable=self.selected_video, command=self.browse_video, state=tk.DISABLED)
        self.button_browse.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Etiqueta y campo de entrada para el peso
        self.label_peso = tk.Label(master, text="Peso:")
        self.label_peso.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.entry_peso = tk.Entry(master, state=tk.DISABLED)
        self.entry_peso.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.entry_peso.bind("<KeyRelease>", self.enable_send_button)

        # Botón de enviar
        self.button_send = tk.Button(master, text="Enviar", command=self.show_video_frame, state=tk.DISABLED)
        self.button_send.grid(row=3, columnspan=2, padx=10, pady=5)

        # Marco para mostrar el video
        self.video_frame = tk.LabelFrame(master, text="Video", height=500, width=900)
        self.video_frame.grid(row=4, columnspan=2, padx=10, pady=5, sticky="nesw")
        self.video_frame.grid_propagate(False)
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()

        # Spinner
        self.spinner = ttk.Label(master, text="Procesando video", font=('Helvetica', 12))
        self.spinner.grid(row=5, columnspan=2, padx=10, pady=5)
        self.spinner.grid_remove()

        # Variables para el video
        self.video_cap = None
        self.current_frame = None

        # Factor de escala para las coordenadas
        self.scale_x = None
        self.scale_y = None

    def enable_video_selection(self, event=None):
        self.button_browse.config(state=tk.NORMAL)


    

    def browse_video(self):
        filename = filedialog.askopenfilename(filetypes=[("Video files", "*.MOV")])
        if filename:
            self.video_cap = cv2.VideoCapture(filename)
            self.selected_video.set(filename.split("/")[-1])  # Obtener el nombre del video y establecerlo como texto del botón
            self.entry_peso.config(state=tk.NORMAL)  # Habilitar la entrada de peso después de seleccionar un video

            self.button_send.grid_remove()  # Ocultar el botón de enviar
            self.spinner.grid(row=3, columnspan=2, padx=10, pady=5)  # Mostrar el spinner giratorio
        
            # Iniciar el proceso en otro hilo
            threading.Thread(target=self.start_landmark_detection, args=(filename,)).start()
    def enable_send_button(self, event=None):
        peso = self.entry_peso.get()
        if peso.isdigit():
            self.button_send.config(state=tk.NORMAL)
        else:
            self.button_send.config(state=tk.DISABLED)

    def show_video_frame(self):
        self.video_frame.grid(row=4, columnspan=2, padx=10, pady=5, sticky="nesw")  # Mostrar el marco del video
        self.process_frame()  # Comenzar a procesar el video cuando se muestra el marco

    def start_landmark_detection(self, video_path):
    # Llamar a la función para iniciar la detección de puntos de referencia
        getLandmarks(video_path)
        # Cambiar el spinner giratorio de vuelta al botón de enviar al finalizar el proceso
        self.master.after(0, self.update_ui_after_detection)

    def update_ui_after_detection(self):
        self.spinner.grid_remove()  # Ocultar el spinner giratorio
        self.button_send.grid(row=3, columnspan=2, padx=10, pady=5)  # Mostrar el botón de enviar

        
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
            self.show_reps_on_video(frame)
            self.video_label.after(10, self.process_frame)  # Llama a process_frame después de 10ms para reproducir el video
        else:
            self.video_cap.release()

    def show_reps_on_video(self,frame):
        # Cargar datos desde el archivo CSV en un DataFrame
        file_path = "pose_data.csv"  
        df = pd.read_csv(file_path)

        # Obtener el angulo del frame actual
        angle=[int(row['Angle']) for index, row in df[df['Frame'] == self.video_cap.get(cv2.CAP_PROP_POS_FRAMES)].iterrows()]
        reps=[int(row['Reps']) for index, row in df[df['Frame'] == self.video_cap.get(cv2.CAP_PROP_POS_FRAMES)].iterrows()]
        cv2.putText(frame, f"Angulo: {angle}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Repeticiones: {reps}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Convertir el frame modificado a formato adecuado para mostrar en la GUI
        frame_with_text = Image.fromarray(frame)
        frame_with_text = ImageTk.PhotoImage(image=frame_with_text)

        # Mostrar el frame modificado en la GUI
        self.video_label.configure(image=frame_with_text)
        self.video_label.image = frame_with_text
        
        # Cargar datos desde el archivo CSV en un DataFrame
    def calculate_scale_factors(self):
        # Factores de escala para las coordenadas x e y
        self.scale_x = 854 / 1920
        self.scale_y = 480 / 1080

    def plot_points_on_video(self, frame):
        # Cargar datos desde el archivo CSV en un DataFrame
        file_path = "pose_data.csv"  
        df = pd.read_csv(file_path)

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

        # Convertir el frame modificado a formato adecuado para mostrar en la GUI
        frame_with_points = Image.fromarray(frame)
        frame_with_points = ImageTk.PhotoImage(image=frame_with_points)
        
        # Configurar el label para mostrar el frame con los puntos dibujados
        self.video_label.configure(image=frame_with_points)
        self.video_label.image = frame_with_points  # Mantener referencia a la imagen

def getLandmarks(video_path):

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Inicializamos las columnas del dataframe
    columns = ['Frame', 'Shoulder_X', 'Shoulder_Y', 'Elbow_X', 'Elbow_Y', 'Wrist_X', 'Wrist_Y', 'Angle']
    df = pd.DataFrame(columns=columns)

    cap = cv2.VideoCapture(video_path)

    # Procesamos cada frame, y extraemos landmarks
    frame_number = 0
    contador_reps=0
    state="up"
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(image)

        # Extraer landmarks 
        if results.pose_landmarks:
            shoulder = None
            elbow = None
            wrist = None
            for id, landmark in enumerate(results.pose_landmarks.landmark):
                if id == mp_pose.PoseLandmark.RIGHT_SHOULDER.value:
                    shoulder = (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
                elif id == mp_pose.PoseLandmark.RIGHT_ELBOW.value:
                    elbow = (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
                elif id == mp_pose.PoseLandmark.RIGHT_WRIST.value:
                    wrist = (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
                

            if shoulder and elbow and wrist:
                angle= round(calcular_angulo(shoulder[0], shoulder[1], elbow[0], elbow[1], wrist[0], wrist[1]))
                df = df._append({'Frame': frame_number,
                                'Shoulder_X': shoulder[0], 'Shoulder_Y': shoulder[1],
                                'Elbow_X': elbow[0], 'Elbow_Y': elbow[1],
                                'Wrist_X': wrist[0], 'Wrist_Y': wrist[1],
                                'Angle': angle,
                                'Reps': round(contador_reps)},
                                    ignore_index=True)
                print(f"Angle: {angle}")
                state,contador_reps=contador_repeticiones(angle,state,contador_reps)
                print("Repeticiones:", contador_reps)
                frame_number += 1

    cap.release()

    # Print the DataFrame
    # Save the DataFrame to a CSV file
    df.to_csv('pose_data.csv', index=False)

    print(df)
    return True

def contador_repeticiones(angle,state,contador_reps):
    if angle >= MAX_RANGE and state =="down":
        state="up"
    if angle <= MIN_RANGE and state =="up":
        state="down"
        contador_reps += 1
    return state,contador_reps

def calcular_angulo(a0,a1,b0,b1,c0,c1):
        
        p = np.array([a0 - b0, a1 - b1])
        q = np.array([c0 - b0, c1 - b1])

        pq = p[0] * q[0] + p[1] * q[1]

        Mp = np.sqrt(p[0] ** 2 + p[1] ** 2)
        Mq = np.sqrt(q[0] ** 2 + q[1] ** 2)

        cos_theta = pq / (Mp * Mq)

        theta = np.arccos(cos_theta)

        angle = np.degrees(theta)

        return angle


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()