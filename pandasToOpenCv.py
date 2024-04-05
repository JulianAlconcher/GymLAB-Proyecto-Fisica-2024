import pandas as pd
import cv2

# Cargar datos desde el archivo CSV en un DataFrame
file_path = "pose_data.csv"  
df = pd.read_csv(file_path)

# Abre el video para lectura
cap = cv2.VideoCapture("Proyecto-Fisica/Videos/fran-bicep-3.MOV") 

window_name = 'Skeleton'

# Iterar sobre cada frame en el video
while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    
    # Obtener las coordenadas de las articulaciones del frame actual
    shoulder_points = [(int(row['Shoulder_X']), int(row['Shoulder_Y'])) for index, row in df[df['Frame'] == cap.get(cv2.CAP_PROP_POS_FRAMES)].iterrows()]
    elbow_points = [(int(row['Elbow_X']), int(row['Elbow_Y'])) for index, row in df[df['Frame'] == cap.get(cv2.CAP_PROP_POS_FRAMES)].iterrows()]
    wrist_points = [(int(row['Wrist_X']), int(row['Wrist_Y'])) for index, row in df[df['Frame'] == cap.get(cv2.CAP_PROP_POS_FRAMES)].iterrows()]

    # Dibujar círculos para cada articulación en el frame actual
    for shoulder_point, elbow_point, wrist_point in zip(shoulder_points, elbow_points, wrist_points):
        cv2.circle(frame, shoulder_point, 5, (0, 255, 0), -1)  # Dibujar círculo para hombro
        cv2.circle(frame, elbow_point, 5, (0, 0, 255), -1)     # Dibujar círculo para codo
        cv2.circle(frame, wrist_point, 5, (255, 0, 0), -1)     # Dibujar círculo para muñeca
    
    # Dibujar líneas conectando los puntos de las articulaciones
    for shoulder_point, elbow_point, wrist_point in zip(shoulder_points, elbow_points, wrist_points):
        cv2.line(frame, shoulder_point, elbow_point, (0, 255, 255), 2) # Línea del hombro al codo
        cv2.line(frame, elbow_point, wrist_point, (255, 255, 0), 2)    # Línea del codo a la muñeca

    # Mostrar el cuadro con los puntos y líneas dibujados
    cv2.imshow(window_name, frame)

    # Salir si se presiona 'q'
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Liberar el video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
