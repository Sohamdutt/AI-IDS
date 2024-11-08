# app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
from capture import start_sniffing
from inference import make_prediction, load_model
from preprocess import preprocess_data
from train import update_model
from src.utils import setup_logger, send_alert_email, log_alert
import threading
import logging
import json

# Initialize Flask app and logging
app = Flask(__name__)

logging.basicConfig(filename='app.log', level=logging.INFO)

# Load the pre-trained model
model = load_model()

# Initialize the logger
logger = setup_logger()

# Start packet sniffing in a separate thread for real-time detection
def start_real_time_detection(interface="eth0"):
    start_sniffing(interface=interface, packet_count=0)

# Start sniffing in the background
sniffing_thread = threading.Thread(target=start_real_time_detection, args=("eth0",))
sniffing_thread.daemon = True
sniffing_thread.start()

# Log a sample alert
log_alert(logger, "Suspicious traffic detected from IP 10.0.0.1")
send_alert_email("Suspicious Activity Detected", "Details of the threat...")

# Route for the main dashboard
@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Prediction endpoint
@app.route("/predict", methods=["POST"])
def predict_endpoint():
    data = request.json.get("data", [])
    prediction, probability = make_prediction(model, data)
    result = "Normal" if prediction == 0 else "Threat Detected"
    return jsonify({"result": result, "probability": probability})

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Authentication logic here
        session['user_id'] = "authenticated_user"
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Registration logic here
        return redirect(url_for('verify_otp'))
    return render_template('register.html')

# OTP verification route
@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        # OTP verification logic here
        return redirect(url_for('login'))
    return render_template('verify_otp.html')

# Real-time packet upload and analysis endpoint
@app.route('/api/upload', methods=['POST'])
def upload_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    processed_data = preprocess_data(data)
    prediction, probability = make_prediction(model, processed_data)

    # Log the result
    logging.info(f"Prediction: {prediction}, Probability: {probability}")

    # If a threat is detected, log it to alerts.log
    if prediction == "threat":
        with open("logs/alerts.log", "a") as alert_log:
            alert = {
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "src_ip": data.get('src_ip'),
                "dest_ip": data.get('dest_ip'),
                "prediction": prediction,
                "probability": probability
            }
            alert_log.write(json.dumps(alert) + "\n")

    return jsonify({"prediction": prediction, "probability": probability})

# Endpoint to fetch recent alerts for the dashboard
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    try:
        with open("logs/alerts.log", "r") as f:
            alerts = [json.loads(line) for line in f.readlines()]
        return jsonify(alerts)
    except FileNotFoundError:
        return jsonify([])

# Endpoint to train/update the model with new data
@app.route('/api/update_model', methods=['POST'])
def train_model():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided for training"}), 400

    update_model(data)  # Calls function from train.py to retrain the model
    return jsonify({"message": "Model updated successfully!"})

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True)
