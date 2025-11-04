from flask import Flask, render_template, request, jsonify, send_from_directory
from pymongo import MongoClient
import os

app = Flask(__name__, static_folder=None, template_folder='templates')

# --- MongoDB connection ---
client = MongoClient("mongodb+srv://Farhan:123456789lp@cluster0.b8oxyxw.mongodb.net/?appName=Cluster0")
db = client["Sample_DB"]
collection = db["Users"]

# --- Room limits ---
ROOM_LIMIT = {
    "Laxaries Rooms": 10,
    "Deluxe Room": 10,
    "Signature Room": 10,
    "Couple Room": 10
}

# --- Serve static files from inside templates ---
@app.route('/<folder>/<path:filename>')
def serve_static_files(folder, filename):
    allowed_folders = ['css', 'js', 'img', 'images', 'vendor', 'fonts']
    if folder in allowed_folders:
        path = os.path.join(app.template_folder, folder)
        return send_from_directory(path, filename)
    return "File not found", 404


@app.route('/')
def index():
    return render_template('rooms.html')


@app.route('/abc', methods=['POST'])
def print_availability():
     return jsonify({"status": "ok", "message": "Post request received"})

# --- Book room ---
@app.route('/check-availability', methods=['POST'])
def save_booking():
    room_type = request.form.get('room_type')
    check_in = request.form.get('check_in')
    check_out = request.form.get('check_out')

    if not (room_type and check_in and check_out):
        return jsonify({"status": "error", "message": "Missing booking details"})

    # Save directly to MongoDB
    collection.insert_one({
        "room_type": room_type,
        "check_in": check_in,
        "check_out": check_out
    })

    return jsonify({"status": "success", "message": "Booking details saved successfully!"})


if __name__ == '__main__':
    app.run(debug=True)
