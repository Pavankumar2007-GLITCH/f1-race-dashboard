
import fastf1
import pandas as pd
import plotly.express as px

# STEP 1: Choose the race
session = fastf1.get_session(2024, "Monaco", "R")
session.load()

# STEP 2: Get all lap records
laps = session.laps.copy()

# STEP 3: Select two drivers
driver_a = "VER"
driver_b = "NOR"

# STEP 4: Prepare Driver A's lap times
a = laps.loc[
    laps["Driver"] == driver_a,
    ["LapNumber", "LapTime"]
].copy()

a = a.dropna(subset=["LapTime"])
a["Time_A"] = a["LapTime"].dt.total_seconds()
a = a[["LapNumber", "Time_A"]]

# STEP 5: Prepare Driver B's lap times
b = laps.loc[
    laps["Driver"] == driver_b,
    ["LapNumber", "LapTime"]
].copy()

b = b.dropna(subset=["LapTime"])
b["Time_B"] = b["LapTime"].dt.total_seconds()
b = b[["LapNumber", "Time_B"]]

# STEP 6: Match both drivers by lap number
comparison = pd.merge(
    a,
    b,
    on="LapNumber",
    how="inner"
)

# STEP 7: Calculate the time difference
comparison["Difference"] = (
    comparison["Time_A"] - comparison["Time_B"]
)

# STEP 8: Display the comparison table
print(f"\nDriver A: {driver_a}")
print(f"Driver B: {driver_b}")
print("\nLap-time comparison:")

print(
    comparison.round(3).to_string(index=False)
)

# STEP 9: Plot the time differences
fig = px.bar(
    comparison,
    x="LapNumber",
    y="Difference",
    title=f"{driver_a} vs {driver_b} - Lap Time Difference",
    labels={
        "LapNumber": "Lap Number",
        "Difference": "A time - B time (seconds)"
    }
)

# Zero is the reference line
fig.add_hline(y=0, line_dash="dash")

fig.update_layout(
    template="plotly_white",
    hovermode="x unified"
)

fig.show()
