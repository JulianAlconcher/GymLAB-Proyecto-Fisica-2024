import csv
import io
import logging
from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS

from make_video import process_video
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
        exercice_weight = request.form.get('weight')
        video_file = request.files['video']
        
        if video_file:
            filename = video_file.filename
            video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            print("Info received:", exercise, exercice_weight, filename)
            csv_state = get_landmarks("static/" + filename)
            print("Agrego columnas de velocidad y aceleracion")
            csv_state = append_velocity_to_csv_and_json()
            csv_state = append_aceleration_to_csv_and_json()
            print("Intento suavizaar la columna de velocidad")
            csv_state = suavizar_columna('pose_data.csv', 'velocidad_instantanea')
            print("Intento suavizaar la columna de aceleracion")
            csv_state = suavizar_columna('pose_data.csv', 'aceleracion_instantanea')
            print("Intento calcular la fuerza")
            #csv_state = calculate_forces()
            
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

if __name__ == "__main__":
    app.run(debug=True, port=8080,)
