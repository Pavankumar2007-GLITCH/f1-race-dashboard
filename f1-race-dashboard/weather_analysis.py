
import fastf1
import pandas as pd
import plotly.express as px

# Load race session
session = fastf1.get_session(2024, "Monaco", "R")
session.load()

# Get weather measurements
weather = session.weather_data.copy()

print("Weather columns:")
print(weather.columns.tolist())

print("\nFirst five weather records:")
print(weather.head())

# Plot available temperature measurements
if not weather.empty and "TrackTemp" in weather.columns:
    fig = px.line(
        weather,
        x="Time",
        y="TrackTemp",
        title="Monaco GP - Track Temperature",
        labels={
            "Time": "Session Time",
            "TrackTemp": "Track Temperature (°C)"
        }
    )
    fig.show()
else:
    print("No track temperature data is available.")
