from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load("model/delay_model.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    distance = float(request.form["distance"])
    delivery_time = int(request.form["delivery_time"])
    traffic = int(request.form["traffic"])
    weather = int(request.form["weather"])
    workload = int(request.form["workload"])

    input_data = pd.DataFrame([{
    "distance_km": distance,
    "delivery_time": delivery_time,
    "traffic_level": traffic,
    "weather": weather,
    "rider_workload": workload
    }])

    prediction = model.predict(input_data)

    result = "Delayed" if prediction[0] == 1 else "On Time"
    return render_template("index.html", prediction=result)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5500, debug=True)