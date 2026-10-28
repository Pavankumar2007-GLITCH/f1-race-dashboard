
import fastf1
import pandas as pd
import plotly.express as px

# STEP 1: Load the race
print("Loading Monaco GP tyre data...")

session = fastf1.get_session(2024, "Monaco", "R")
session.load()

# STEP 2: Get lap data
laps = session.laps.copy()

# STEP 3: Check required tyre columns
required = ["Compound", "TyreLife", "Stint"]
missing = [col for col in required if col not in laps.columns]

if missing:
    print("Tyre columns unavailable:", missing)

else:
    # STEP 4: Prepare lap times
    laps = laps.dropna(subset=["LapTime"]).copy()

    # Convert lap time from timedelta to seconds
    laps["LapSeconds"] = laps["LapTime"].dt.total_seconds()

    # Remove pit-in and pit-out laps
    laps = laps[
        laps["PitInTime"].isna() &
        laps["PitOutTime"].isna()
    ].copy()

    # Keep plausible Monaco lap times
    laps = laps[laps["LapSeconds"].between(60, 150)].copy()

    # STEP 5: Show available tyre compounds
    print("\nTyre compounds found:")
    print(laps["Compound"].dropna().unique())

    # STEP 6: Select a driver
    driver = "VER"

    driver_laps = laps[
        laps["Driver"] == driver
    ].copy()

    print(f"\nTyre information for {driver}:")

    print(
        driver_laps[
            [
                "LapNumber",
                "Compound",
                "TyreLife",
                "Stint",
                "LapTime"
            ]
        ].head(15).to_string(index=False)
    )

    
# STEP 7: Keep complete tyre records
tyre_data = driver_laps.dropna(
    subset=["Compound", "TyreLife", "Stint", "LapSeconds"]
).copy()

# STEP 8: Inspect unusually slow laps
print("\nSlowest recorded laps to inspect:")
print(
    tyre_data.nlargest(5, "LapSeconds")[
        ["LapNumber", "LapSeconds", "Compound",
         "TyreLife", "Stint"]
    ].to_string(index=False)
)

# STEP 9: Remove pit-in and pit-out laps when identified
if "PitInTime" in tyre_data.columns:
    tyre_data = tyre_data[tyre_data["PitInTime"].isna()]

if "PitOutTime" in tyre_data.columns:
    tyre_data = tyre_data[tyre_data["PitOutTime"].isna()]

# Remove laps flagged as inaccurate, if this field exists
if "IsAccurate" in tyre_data.columns:
    tyre_data = tyre_data[
        tyre_data["IsAccurate"].fillna(False)
    ]

# STEP 10: Plot separate stints
if tyre_data.empty:
    print("No valid tyre records remain after filtering.")
else:
    tyre_data = tyre_data.sort_values(
        ["Stint", "TyreLife", "LapNumber"]
    )

    fig = px.line(
        tyre_data,
        x="TyreLife",
        y="LapSeconds",
        color="Compound",
        line_group="Stint",
        markers=True,
        hover_data=["LapNumber", "Stint"],
        title=f"{driver} - Lap Time vs Tyre Age",
        labels={
            "TyreLife": "Tyre Age (laps)",
            "LapSeconds": "Lap Time (seconds)",
            "Compound": "Tyre Compound",
            "Stint": "Stint Number"
        }
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="closest"
    )

    fig.show()

print("\nTyre analysis finished.")
