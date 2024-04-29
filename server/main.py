from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS

from video_processing import get_landmarks

app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "http://localhost:5173"}})

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

        # Guardar el archivo de video en el servidor
        if video_file:
            filename = video_file.filename
            video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            print("Info received:", exercise, weight, filename)
            csv_state = get_landmarks("uploads/" + filename)
            if csv_state:
                print("CSV state:", csv_state)
                return send_file("pose_data.csv", as_attachment=True)
            else:
                return jsonify({"error": "No video file provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)
