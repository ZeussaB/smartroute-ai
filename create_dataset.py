import pandas as pd
import random

rows = []

for _ in range(500):
    distance = random.randint(1, 20)
    delivery_time = random.randint(1, 18)
    traffic = random.randint(0, 2)      # 0=Low,1=Medium,2=High
    weather = random.randint(0, 2)      # 0=Clear,1=Rainy,2=Stormy
    workload = random.randint(0, 2)     # 0=Low,1=Medium,2=High

    # IMPROVED DELAY LOGIC

    score = 0

    # Baseline expected delivery time (ideal conditions)
    expected_time = distance * 1  # 1 hour per km baseline

    # Time efficiency
    if delivery_time > expected_time * 3:
        # Extremely inefficient (hard delay)
        score += 4
    elif delivery_time > expected_time * 2:
        score += 2
    elif delivery_time > expected_time * 1.2:
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

    # Final decision
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