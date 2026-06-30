from flask import Flask, request, jsonify, render_template
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
   
    return render_template('index.html')


@app.route("/predict", methods=["POST"])
def predict():
    try:
        features = [float(x) for x in request.form.values()]
        prediction = model.predict([np.array(features)])

        if prediction[0] == 1:
            status = "🚨 FRAUD TRANSACTION DETECTED"
        else:
            status = "✅ SAFE TRANSACTION"

        return render_template('index.html', prediction_text=status)

    except Exception as e:
        return render_template('index.html', prediction_text="Error: Please fill all 30 values")

if __name__ == "__main__":
    app.run(debug=True)
