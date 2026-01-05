import pandas as pd
import random

rows = []

for _ in range(500):
    distance = random.randint(1, 20)            # km
    delivery_time = random.randint(1, 18)       # hours
    traffic = random.randint(0, 2)              # 0=Low,1=Medium,2=High
    weather = random.randint(0, 2)              # 0=Clear,1=Rain,2=Storm
    workload = random.randint(0, 2)             # 0=Low,1=Medium,2=High

    # PERFECT CONDITION OVERRIDE
    if traffic == 0 and weather == 0 and workload == 0:
        # Delivery time should match distance realistically
        # 15–30 minutes per km -> approx 0.25–0.5 hour
        delivery_time = round(random.uniform(distance * 0.25, distance * 0.5), 2)

    # IMPROVED DELAY LOGIC
    
    score = 0
    expected_time = distance * 1  # 1 hour per km baseline

    # Time efficiency scoring
    if delivery_time > expected_time * 3:
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

    # Weather impact (short distance mitigates severity)
    if weather == 2:
        if distance >= 5:
            score += 2
        else:
            score += 1
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

# Save to CSV
df = pd.DataFrame(rows, columns=[
    "distance_km",
    "delivery_time",
    "traffic_level",
    "weather",
    "rider_workload",
    "delay"
])

df.to_csv("delivery_data.csv", index=False)
print("Dataset created successfully")