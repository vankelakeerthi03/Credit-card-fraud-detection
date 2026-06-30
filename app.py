from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)

print("🔄 Loading model...")

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Model path
model_path = os.path.join(BASE_DIR, "fraud_model.pkl")

if not os.path.exists(model_path):
    print("❌ Model not found!")
    print("Run train_model.py first")
    exit()

# Load model
model = joblib.load(model_path)

print("✅ Model loaded successfully")


@app.route("/")
def home():
    return "💳 Fraud Detection API Running"


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Read input
        time = float(data.get("Time", 0))
        amount = float(data.get("Amount", 0))

        # Feature array
        features = np.array([[time, amount]])

        # Prediction
        prediction = int(model.predict(features)[0])

        # Fraud probability
        prob = 0
        if hasattr(model, "predict_proba"):
            prob = float(model.predict_proba(features)[0][1])

        # Generate OTP
        otp = str(np.random.randint(100000, 999999))

        # Status message
        if prediction == 1:
            status = "🚨 FRAUD TRANSACTION DETECTED"
        else:
            status = "✅ SAFE TRANSACTION"

        # Return response
        return jsonify({
            "prediction": prediction,
            "status": status,
            "otp": otp,
            "fraud_probability": round(prob, 4),
            "location": data.get("location", "Unknown")
        })

    except Exception as e:
        print("❌ Server Error:", e)

        return jsonify({
            "prediction": 0,
            "status": "Server Error",
            "otp": "000000",
            "fraud_probability": 0
        })


if __name__ == "__main__":
    print("🚀 Starting API → http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
