import cv2
import mediapipe as mp
import pandas as pd

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Inicializamos las columnas del dataframe
columns = ['Frame', 'Shoulder_X', 'Shoulder_Y', 'Elbow_X', 'Elbow_Y', 'Wrist_X', 'Wrist_Y']
df = pd.DataFrame(columns=columns)

cap = cv2.VideoCapture("Proyecto-Fisica/Videos/fran-bicep-3.MOV")

# Procesamos cada frame, y extraemos landmarks
frame_number = 0
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
            if id == mp_pose.PoseLandmark.LEFT_SHOULDER.value:
                shoulder = (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
            elif id == mp_pose.PoseLandmark.LEFT_ELBOW.value:
                elbow = (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
            elif id == mp_pose.PoseLandmark.LEFT_WRIST.value:
                wrist = (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))

        if shoulder and elbow and wrist:
            df = df._append({'Frame': frame_number,
                            'Shoulder_X': shoulder[0], 'Shoulder_Y': shoulder[1],
                            'Elbow_X': elbow[0], 'Elbow_Y': elbow[1],
                            'Wrist_X': wrist[0], 'Wrist_Y': wrist[1]}, ignore_index=True)
            frame_number += 1

    # Display
    cv2.imshow('MediaPipe Pose Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Print the DataFrame
# Save the DataFrame to a CSV file
df.to_csv('pose_data.csv', index=False)

print(df)