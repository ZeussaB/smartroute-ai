import pandas as pd
import random

rows = []

for _ in range(500):
    distance = random.randint(1, 20)
    delivery_time = random.randint(1, 18)
    traffic = random.randint(0, 2)      # 0=Low,1=Medium,2=High
    weather = random.randint(0, 2)      # 0=Clear,1=Rainy,2=Stormy
    workload = random.randint(0, 2)     # 0=Low,1=Medium,2=High

    # -----------------------------
    # IMPROVED DELAY LOGIC
    # -----------------------------

    score = 0

    # Time efficiency (key factor)
    time_per_km = delivery_time / distance
    if time_per_km > 2.5:
        score += 2
    elif time_per_km > 1.8:
        score += 1

    # Traffic impact
    if traffic == 2:
        score += 2
    elif traffic == 1:
        score += 1

    # Weather impact
    if weather == 2:
        score += 2
    elif weather == 1:
        score += 1

    # Rider workload impact
    if workload == 2:
        score += 2
    elif workload == 1:
        score += 1

    # Final delay decision
    delay = 1 if score >= 4 else 0

    rows.append([
        distance,
        delivery_time,
        traffic,
        weather,
        workload,
        delay
    ])

df = pd.DataFrame(rows, columns=[
    "distance_km",
    "delivery_time",
    "traffic_level",
    "weather",
    "rider_workload",
    "delay"
])

df.to_csv("delivery_data.csv", index=False)
print("Improved dataset created successfully")

# The dataset 'delivery_data.csv' contains synthetic data
# generated using a realistic scoring-based delay mechanism.