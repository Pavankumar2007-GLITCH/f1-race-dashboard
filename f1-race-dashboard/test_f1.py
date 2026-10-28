
import fastf1

print("Starting F1 data test...")

session = fastf1.get_session(2024, "Monaco", "R")

try:
    session.load(telemetry=False)
    print("\nSUCCESS! Race data loaded.")
    print(session.laps.head())
except Exception as error:
    print("\nDATA LOADING FAILED:")
    print(type(error).__name__)
    print(error)
