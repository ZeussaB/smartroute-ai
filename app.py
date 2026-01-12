from flask import Flask, render_template, request
import joblib
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

model = joblib.load("model/delay_model.pkl")

FEATURES = ["distance_km", "delivery_time", "traffic_level", "weather", "rider_workload"]

LOG_FILE = "logs/prediction_log.csv"
os.makedirs("logs", exist_ok=True)

# Create log file if not exists
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=FEATURES + ["prediction", "confidence", "timestamp"]).to_csv(LOG_FILE, index=False)

# Input Validation
def validate_inputs(distance, time, traffic, weather, workload):
    warnings = []
    if distance <= 0:
        warnings.append("Distance must be greater than 0.")
    if time <= 0:
        warnings.append("Delivery time must be greater than 0.")
    if distance <= 5 and time > 5:
        warnings.append("Delivery time seems too long for a short distance.")
    return warnings

# Explanation Logic
def generate_reason(distance, time, traffic, weather, workload):
    reasons = []
    if traffic == 2:
        reasons.append("High traffic")
    if weather == 2:
        reasons.append("Stormy weather")
    if workload == 2:
        reasons.append("High rider workload")
    if distance > 10:
        reasons.append("Long distance")

    return " and ".join(reasons) if reasons else "All conditions are favorable"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    distance = float(request.form["distance"])
    time = float(request.form["time"])
    traffic = int(request.form["traffic"])
    weather = int(request.form["weather"])
    workload = int(request.form["workload"])

    warnings = validate_inputs(distance, time, traffic, weather, workload)

    input_data = pd.DataFrame([[distance, time, traffic, weather, workload]], columns=FEATURES)

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][prediction]

    result = "Delayed" if prediction == 1 else "On Time"
    confidence = round(probability * 100, 2)
    reason = generate_reason(distance, time, traffic, weather, workload)

    # Log prediction
    log_row = input_data.copy()
    log_row["prediction"] = result
    log_row["confidence"] = confidence
    log_row["timestamp"] = datetime.now()
    log_row.to_csv(LOG_FILE, mode="a", header=False, index=False)

    return render_template("index.html", result=result, confidence=confidence, reason=reason, warnings=warnings)

# Prediction History
@app.route("/history")
def history():
    data = pd.read_csv(LOG_FILE)
    return render_template("history.html", tables=data.to_html(classes="table", index=False))

# Admin Panel
@app.route("/admin")
def admin():
    with open("model/metrics.txt", "r") as f:
        metrics = f.read()

    importances = model.feature_importances_
    importance_data = zip(FEATURES, importances)

    return render_template("admin.html", metrics=metrics, importance=importance_data)

# Scenario Testing
@app.route("/scenario", methods=["POST"])
def scenario():
    base_distance = float(request.form["distance"])
    base_time = float(request.form["time"])

    scenarios = []
    for traffic in [0, 1, 2]:
        for weather in [0, 1, 2]:
            for workload in [0, 1, 2]:
                data = pd.DataFrame([[base_distance, base_time, traffic, weather, workload]], columns=FEATURES)
                pred = model.predict(data)[0]
                scenarios.append({
                    "traffic": traffic,
                    "weather": weather,
                    "workload": workload,
                    "result": "Delayed" if pred == 1 else "On Time"
                })

    return {"scenarios": scenarios}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5500, debug=True)