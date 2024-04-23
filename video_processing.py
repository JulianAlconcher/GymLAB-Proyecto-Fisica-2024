import cv2
import numpy as np
import pandas as pd
import mediapipe as mp

MAX_RANGE = 160
MIN_RANGE = 50

def get_landmarks(video_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Inicializamos las columnas del dataframe
    columns = ['Frame', 'Shoulder_X', 'Shoulder_Y', 'Elbow_X', 'Elbow_Y', 'Wrist_X', 'Wrist_Y', 'Angle', 'Reps']
    df = pd.DataFrame(columns=columns)

    cap = cv2.VideoCapture(video_path)

    # Procesamos cada frame y extraemos los landmarks
    frame_number = 0
    contador_reps = 0
    state = "up"

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
                angle = round(calcular_angulo(shoulder[0], shoulder[1], elbow[0], elbow[1], wrist[0], wrist[1]))
                df = df.append({'Frame': frame_number,
                                'Shoulder_X': shoulder[0], 'Shoulder_Y': shoulder[1],
                                'Elbow_X': elbow[0], 'Elbow_Y': elbow[1],
                                'Wrist_X': wrist[0], 'Wrist_Y': wrist[1],
                                'Angle': angle,
                                'Reps': round(contador_reps)}, ignore_index=True)
                print(f"Angulo: {angle}")
                state, contador_reps = contador_repeticiones(angle, state, contador_reps)
                print("Repeticiones:", contador_reps)
                frame_number += 1

    cap.release()

    # Guardar el DataFrame en un archivo CSV
    df.to_csv('pose_data.csv', index=False)

    print(df)
    return True

def contador_repeticiones(angle, state, contador_reps):
    if angle >= MAX_RANGE and state == "down":
        state = "up"
    if angle <= MIN_RANGE and state == "up":
        state = "down"
        contador_reps += 1
    return state, contador_reps

def calcular_angulo(a0, a1, b0, b1, c0, c1):
    p = np.array([a0 - b0, a1 - b1])
    q = np.array([c0 - b0, c1 - b1])

    pq = p[0] * q[0] + p[1] * q[1]

    Mp = np.sqrt(p[0] ** 2 + p[1] ** 2)
    Mq = np.sqrt(q[0] ** 2 + q[1] ** 2)

    cos_theta = pq / (Mp * Mq)

    theta = np.arccos(cos_theta)

    angle = np.degrees(theta)

    return angle
