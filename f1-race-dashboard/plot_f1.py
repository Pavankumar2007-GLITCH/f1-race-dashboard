
import fastf1
import plotly.express as px

# Load race data
session = fastf1.get_session(2024, "Monaco", "R")
session.load()

# Get laps
laps = session.laps

# Remove laps without recorded lap times
laps = laps.dropna(subset=["LapTime"])

# Convert lap times into seconds
laps = laps.copy()
laps["LapSeconds"] = laps["LapTime"].dt.total_seconds()

# Draw the graph
fig = px.line(
    laps,
    x="LapNumber",
    y="LapSeconds",
    color="Driver",
    title="2024 Monaco GP - Lap Time Comparison",
    labels={
        "LapNumber": "Lap Number",
        "LapSeconds": "Lap Time (seconds)",
        "Driver": "Driver"
    }
)

fig.show()
