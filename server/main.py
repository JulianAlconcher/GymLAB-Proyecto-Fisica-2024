import csv
import io
import logging
from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS

from make_video import process_video
from utils.createPDF import create_pdf
from utils.saveGraphics import saveGraphics
from utils.aceleration import append_aceleration_to_csv_and_json
from utils.forces import calculate_forces
from utils.utils import suavizar_columna
from utils.velocity import append_velocity_to_csv_and_json
from video_processing import get_landmarks

app = Flask(__name__, static_folder='static')
logging.basicConfig(level=logging.DEBUG)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Ajusta el límite de tamaño de carga (por ejemplo, 100 MB)
app.config['SEND_FILE_MAX_RANGE'] = None
cors = CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload", methods=["POST"])
def upload():
    try:
        exercise = request.form.get('exercise')
        weight = request.form.get('weight')
        weightDumbbell = request.form.get('weightDumbbell')
        height = request.form.get('height')
        experience = request.form.get('experience')
        video_file = request.files['video']
        forearmDistance = request.form.get('forearmDistance')
        
        if video_file:
            filename = video_file.filename
            video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            print("Info received:", exercise, weightDumbbell, filename, weight, height, experience, forearmDistance)
            csv_state = get_landmarks("static/" + filename)
            print("Agrego columnas de velocidad y aceleracion")
            csv_state = append_velocity_to_csv_and_json()
            csv_state = append_aceleration_to_csv_and_json()
            print("Intento suavizaar la columna de velocidad")
            csv_state = suavizar_columna('pose_data.csv', 'velocidad_instantanea')
            print("Intento suavizaar la columna de aceleracion")
            csv_state = suavizar_columna('pose_data.csv', 'aceleracion_instantanea')
            print("Intento calcular la fuerza")
            experienceNumber = getExperience(experience)
            print("La experiencia es: ", experienceNumber)
            csv_state = calculate_forces(height=float(height), weight= float(weight), mass_weight= float(weightDumbbell), training_level=experienceNumber, distance_forearm=float(forearmDistance))
            print("Guardo graficos en el servidor ")
            csv_state = saveGraphics()
            csv_state = create_pdf(weight=float(weight), height=float(height), training_level=experienceNumber, distance_forearm=float(forearmDistance), mass_weight= float(weightDumbbell))
            
            if csv_state is None: 
                return jsonify({"error": "No video file provided"}), 400
            else:
                return jsonify({"message": "Results received"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/getFile", methods=["GET"])
def get_file():
    try:
        if os.path.exists("pose_data.json"):
            return send_file("pose_data.json", as_attachment=True)
        else:
            return jsonify({"error": "No files uploaded yet"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/getVideo", methods=["GET"])
def get_video():
    try:
        input_video_path = request.args.get('video_path')
        if input_video_path is None:
            return jsonify({"error": "video_path parameter is missing"}), 400
        logging.info("Received request for video")
        process_video(input_video_path)
        video_path = "static/processed_video.mp4"
        if os.path.exists(video_path):
            logging.info("Sending video file")
            return send_file(video_path, as_attachment=False)
        else:
            logging.error("Video file not found")
            return jsonify({"error": "Video not found"}), 404
    except Exception as e:
        logging.error(f"Error processing or sending video: {e}")
        return jsonify({"error": str(e)}), 500
    
    
def getExperience(experience):
    if experience == "Principiante":
        return 0
    elif experience == "Intermedio":
        return 1
    elif experience == "Avanzado":
        return 2
    

if __name__ == "__main__":
    app.run(debug=True, port=8080,)
