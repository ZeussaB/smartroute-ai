import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib
import os

# Load data
data = pd.read_csv("delivery_data.csv")

X = data.drop("delay", axis=1)
y = data["delay"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Ensure model folder exists
os.makedirs("model", exist_ok=True)

# Save model
joblib.dump(model, "model/delay_model.pkl")
print("Model trained and saved successfully")