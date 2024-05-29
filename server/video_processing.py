import cv2
import pandas as pd
import mediapipe as mp

from utils.forces import calculate_forces
from utils.aceleration import append_aceleration_to_csv_and_json
from utils.utils import calcular_angulo, calculate_distance_between_vectors, contador_repeticiones, transform_mesaured_vector_to_mts
from utils.velocity import append_velocity_to_csv_and_json



def get_landmarks(video_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Inicializamos las columnas del dataframe
    columns = ['Frame', 'TimeStamp', 'Shoulder_X', 'Shoulder_Y', 'Elbow_X', 'Elbow_Y', 'Wrist_X', 'Wrist_Y','Shoulder_X_Normalized', 'Shoulder_Y_Normalized', 'Elbow_X_Normalized', 'Elbow_Y_Normalized', 'Wrist_X_Normalized', 'Wrist_Y_Normalized']
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

            DISTANCE_PX_ELBOW_WRIST = calculate_distance_between_vectors((elbow[0],elbow[1]),(wrist[0],wrist[1]))

            if shoulder and elbow and wrist:
                angle = round(calcular_angulo(shoulder[0], shoulder[1], elbow[0], elbow[1], wrist[0], wrist[1]))
                df = df._append({'Frame': frame_number,
                                'TimeStamp': cap.get(cv2.CAP_PROP_POS_MSEC)/1000,
                                'Shoulder_X': shoulder[0], 'Shoulder_Y': shoulder[1],
                                'Elbow_X': elbow[0], 'Elbow_Y': elbow[1],
                                'Wrist_X': wrist[0], 'Wrist_Y': wrist[1],
                                'Shoulder_X_Normalized': transform_mesaured_vector_to_mts(DISTANCE_PX_ELBOW_WRIST,shoulder[0]), 'Shoulder_Y_Normalized': transform_mesaured_vector_to_mts(DISTANCE_PX_ELBOW_WRIST,shoulder[1]),
                                'Elbow_X_Normalized': transform_mesaured_vector_to_mts(DISTANCE_PX_ELBOW_WRIST,elbow[0]), 'Elbow_Y_Normalized': transform_mesaured_vector_to_mts(DISTANCE_PX_ELBOW_WRIST,elbow[1]),
                                'Wrist_X_Normalized': transform_mesaured_vector_to_mts(DISTANCE_PX_ELBOW_WRIST,wrist[0]), 'Wrist_Y_Normalized': transform_mesaured_vector_to_mts(DISTANCE_PX_ELBOW_WRIST,wrist[1]),
                                'Angle': angle,
                                'Reps': round(contador_reps)}, ignore_index=True)
                state, contador_reps = contador_repeticiones(angle, state, contador_reps)
                frame_number += 1

    cap.release()

    df.to_csv('pose_data.csv', index=False)
    df.to_json('pose_data.json', orient='records')
    append_velocity_to_csv_and_json()
    append_aceleration_to_csv_and_json()
    calculate_forces()
    print(df)
    return True

