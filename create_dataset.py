import pandas as pd
import random

rows = []

for _ in range(500):
    distance = random.randint(1, 20)
    delivery_time = random.randint(9, 18)
    traffic = random.randint(0, 2)      # 0=Low,1=Medium,2=High
    weather = random.randint(0, 2)      # 0=Clear,1=Rainy,2=Stormy
    workload = random.randint(0, 2)     # 0=Low,1=Medium,2=High

    # LOGICAL DELAY RULE
    delay = 0
    if distance > 10 and (traffic == 2 or weather == 2 or workload == 2):
        delay = 1
    elif traffic == 2 and weather == 2:
        delay = 1

    rows.append([distance, delivery_time, traffic, weather, workload, delay])

df = pd.DataFrame(rows, columns=[
    "distance_km",
    "delivery_time",
    "traffic_level",
    "weather",
    "rider_workload",
    "delay"
])

df.to_csv("delivery_data.csv", index=False)
print("Improved dataset created")

# The dataset 'delivery_data.csv' contains synthetic data for delivery scenarios.