import csv
import io
from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS

from make_video import process_video
from video_processing import get_landmarks

app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "http://localhost:5173"}})
CORS(app, resources={r"/getFile": {"origins": "http://localhost:5173"}})
CORS(app, resources={r"/getVideo": {"origins": "*"}})

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload", methods=["POST"])
def upload():
    try:
        exercise = request.form.get('exercise')
        weight = request.form.get('weight')
        video_file = request.files['video']
        
        if video_file:
            filename = video_file.filename
            video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            print("Info received:", exercise, weight, filename)
            csv_state = get_landmarks("uploads/" + filename)
            
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
        process_video()
        video_path = "processed_video.mp4"
        if os.path.exists(video_path):
            return send_file(video_path, as_attachment=True, mimetype='video/mp4')
        else:
            return jsonify({"error": "Video not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)
