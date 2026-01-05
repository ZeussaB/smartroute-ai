from flask import Flask, render_template, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import os

app = Flask(__name__)

# Load or Train Model

DATA_FILE = "delivery_data.csv"

# Check if dataset exists
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError("Please generate 'delivery_data.csv' first using create_dataset.py")

# Load dataset
df = pd.read_csv(DATA_FILE)

# Features and target
X = df[["distance_km", "delivery_time", "traffic_level", "weather", "rider_workload"]]
y = df["delay"]

# Train Decision Tree
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Routes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form data
        distance = float(request.form["distance"])
        delivery_time = float(request.form["delivery_time"])
        traffic = int(request.form["traffic"])
        weather = int(request.form["weather"])
        workload = int(request.form["workload"])

        # Create DataFrame for prediction
        input_df = pd.DataFrame([[
            distance, delivery_time, traffic, weather, workload
        ]], columns=X.columns)

        # Make prediction
        prediction = model.predict(input_df)[0]

        # Convert to readable string
        result = "Delayed" if prediction == 1 else "On Time"

        return render_template("index.html", prediction_text=f"Prediction: {result}")

    except Exception as e:
        return render_template("index.html", prediction_text=f"Error: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)