#Importamos dependencias
import cv2
import mediapipe as mp
import numpy as np #Funciones trigonometricas

mp_drawing = mp.solutions.drawing_utils #Utilidades de dibujo
mp_pose = mp.solutions.pose #Importamos el modelo de POSE


    # Funcion que calcula el angulo entre los puntos A,B,C (landmarks)
def calcular_angulo(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    # C[1] - B[1] = Cy - By
    # C[0] - B[0] = Cx - Bx
    # A[1] - B[1] = Ay - By
    # A[0] - B[0] = Ax - Bx
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 
   
cap = cv2.VideoCapture("Proyecto-Fisica/Videos/fran-bicep-3.MOV")#Abrimos Webcam (0) (podemos cambiarlo)
## Setup mediapipe instance
# Min_detection_confidence: El porcentaje de confianza que se debe tener en la detección de un objeto para que se consideren los puntos de referencia. 
# Min_tracking_confidence: El porcentaje de confianza que se debe tener en la detección de un objeto para que se considere que el objeto se encuentra en la imagen. 
counter = 0 
stage = None
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose: #Nueva instancia de Setup mediapipe
    while cap.isOpened():
        ret, frame = cap.read()
        
        #BGR --> RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        image.flags.writeable = False
      
        # Guardamos los resultados
        results = pose.process(image)
    
        #RGB --> BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extraer landmarks e imprimimos (0-33)
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            # Calculate angle
            angle = calcular_angulo(shoulder, elbow, wrist)
            
            # Renderizar el angulo en la imagen
            # np.multiply(elbow, [640, 480]) multiplico coordenadas del hombro por los px de la webcam.
            # Ya que las coordenadas de los landmarks son cartesianas comunes y no pixeles
            cv2.putText(image, str(angle), 
                           tuple(np.multiply(elbow, [1920, 1080]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Contador de flexiones de brazo.
            if angle > 160:
                stage = "down"
            if angle < 30 and stage =='down':
                stage="up"
                counter +=1
                print(counter)
                       
        except:
            pass
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    