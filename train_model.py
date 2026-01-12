import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
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

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("Model Accuracy:", round(accuracy * 100, 2), "%")
print("Classification Report:\n", report)

# Ensure model folder exists
os.makedirs("model", exist_ok=True)

# Save model and metrics
joblib.dump(model, "model/delay_model.pkl")

with open("model/metrics.txt", "w") as f:
    f.write(f"Accuracy: {accuracy}\n\n")
    f.write(report)

print("Model trained and saved successfully")