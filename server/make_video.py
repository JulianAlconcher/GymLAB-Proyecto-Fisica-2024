import cv2
import pandas as pd

def count_rows(csv_file_path):
    df = pd.read_csv(csv_file_path)
    num_rows = df.shape[0]  # Obtener la cantidad de filas
    return num_rows

def process_video(video_path):
    print("Processing video:", video_path)
    input_video_path = "static/" + video_path
    csv_file_path = "pose_data.csv"
    output_video_path = "static/processed_video.mp4"
    cap = cv2.VideoCapture(input_video_path)
    df = pd.read_csv(csv_file_path)
    print("El data frame utilizado es:", df)
    fourcc = -1
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    scale_x = width / 1920
    scale_y = height / 1080
    
    # Obtener la cantidad de filas del csv
    cant_frames = count_rows(csv_file_path)
    frame_numbers = list(range(0, cant_frames))

    for frame_number in frame_numbers:
        ret, frame = cap.read()
        if not ret:
            break
        
        shoulder_x = int(df.loc[frame_number, 'Shoulder_X'] * scale_x)
        shoulder_y = int(df.loc[frame_number, 'Shoulder_Y'] * scale_y)
        elbow_x = int(df.loc[frame_number, 'Elbow_X'] * scale_x)
        elbow_y = int(df.loc[frame_number, 'Elbow_Y'] * scale_y)
        wrist_x = int(df.loc[frame_number, 'Wrist_X'] * scale_x)
        wrist_y = int(df.loc[frame_number, 'Wrist_Y'] * scale_y)
        
        shoulder_point = (shoulder_x, shoulder_y)  
        elbow_point = (elbow_x, elbow_y)  
        wrist_point = (wrist_x, wrist_y)  
        
        cv2.circle(frame, shoulder_point, 5, (0, 255, 0), -1)  
        cv2.circle(frame, elbow_point, 5, (0, 0, 255), -1)     
        cv2.circle(frame, wrist_point, 5, (255, 0, 0), -1)     
        cv2.line(frame, shoulder_point, elbow_point, (0, 255, 255), 2)  
        cv2.line(frame, elbow_point, wrist_point, (255, 255, 0), 2)  
        

        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

