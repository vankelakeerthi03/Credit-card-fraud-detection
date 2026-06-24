import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("📊 Loading dataset...")

# Current folder path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Dataset path
dataset_path = os.path.join(current_dir, "dataset", "credit.csv")

# Load dataset
data = pd.read_csv(dataset_path)

print("Columns found:", list(data.columns))

# Fill missing values
data = data.fillna(0)

# -----------------------------
# Ensure Time column exists
# -----------------------------
if "Time" not in data.columns:
    print("⚠ Time column missing → creating default values")
    data["Time"] = 0

# Convert Time format
def convert_time(t):
    try:
        if ":" in str(t):
            h, m = t.split(":")
            return int(h) * 60 + int(m)
        return float(t)
    except:
        return 0

data["Time"] = data["Time"].apply(convert_time)

# -----------------------------
# Ensure Amount column exists
# -----------------------------
if "Amount" not in data.columns:
    raise Exception("❌ Amount column not found in dataset")

# -----------------------------
# Create Risk column if missing
# -----------------------------
if "Risk" not in data.columns:
    print("⚠ Risk column missing → creating automatically")
    data["Risk"] = data["Amount"].apply(lambda x: 1 if x > 50000 else 0)

# Use only required columns
data = data[["Time", "Amount", "Risk"]]

print("Dataset shape:", data.shape)

# Features and label
X = data[["Time", "Amount"]]
y = data["Risk"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training samples:", len(X_train))

# Model
model = RandomForestClassifier(
    n_estimators=150,
    random_state=42
)

print("🧠 Training model...")

model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("✅ Accuracy:", round(accuracy * 100, 2), "%")

# -----------------------------
# Save model
# -----------------------------
model_dir = os.path.join(current_dir, "..", "model")
os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, "fraud_model.pkl")

joblib.dump(model, model_path)

print("💾 Model saved →", model_path)
print("🚀 Training complete")