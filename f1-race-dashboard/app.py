
import fastf1
import pandas as pd
import plotly.express as px
import streamlit as st

# -------------------------------
# 1. PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="F1 Race Analytics",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1 {
        letter-spacing: -1px;
    }

    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.08);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
</style>
""", unsafe_allow_html=True)

st.title("🏎️ F1 Race Analytics")
st.caption(
    "Race pace • Tyre strategy • Weather insights"
)

st.markdown("---")


st.title("🏎️ F1 Race Analytics Dashboard")
st.write(
    "Explore driver pace, tyre strategy and weather "
    "using historical Formula 1 data."
)

# -------------------------------
# 2. SIDEBAR: RACE SELECTION
# -------------------------------
st.sidebar.header("Race Settings")

year = st.sidebar.selectbox(
    "Season",
    [2024, 2023, 2022]
)

race = st.sidebar.selectbox(
    "Grand Prix",
    ["Monaco", "British Grand Prix", "Italian Grand Prix"]
)

if st.sidebar.button("Load Race Data", type="primary"):
    with st.spinner("Loading F1 session data..."):
        try:
            session = fastf1.get_session(year, race, "R")
            session.load()

            # Save loaded data so dashboard controls can be used
            # without downloading the race again on each rerun.
            st.session_state["f1_laps"] = session.laps.copy()
            st.session_state["f1_weather"] = (
                session.weather_data.copy()
            )
            st.session_state["f1_year"] = year
            st.session_state["f1_race"] = race

            st.success("Race data loaded successfully!")

        except Exception as error:
            st.error(f"Unable to load race data: {error}")

# -------------------------------
# 3. CHECK THAT DATA IS LOADED
# -------------------------------
if "f1_laps" not in st.session_state:
    st.info(
        "Choose a season and Grand Prix in the sidebar, "
        "then click Load Race Data."
    )
    st.stop()

laps = st.session_state["f1_laps"].copy()
weather = st.session_state["f1_weather"].copy()

loaded_year = st.session_state["f1_year"]
loaded_race = st.session_state["f1_race"]

st.subheader(f"{loaded_year} — {loaded_race}")

# Prepare lap times
laps = laps.dropna(subset=["LapTime"]).copy()
laps["LapSeconds"] = laps["LapTime"].dt.total_seconds()

# -------------------------------
# 4. SUMMARY METRICS
# -------------------------------

# -------------------------------
# 4. SUMMARY METRICS
# -------------------------------

valid_laps = laps.dropna(subset=["LapSeconds"]).copy()

if valid_laps.empty:
    st.warning("No valid lap times are available.")
    st.stop()

fastest_idx = valid_laps["LapSeconds"].idxmin()
fastest_record = valid_laps.loc[fastest_idx]

fastest_seconds = fastest_record["LapSeconds"]
average_seconds = valid_laps["LapSeconds"].mean()
driver_count = valid_laps["Driver"].nunique()

def format_lap_time(seconds):
    minutes = int(seconds // 60)
    remaining = seconds - minutes * 60
    return f"{minutes}:{remaining:06.3f}"

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Drivers Analyzed",
    driver_count
)

col2.metric(
    "Recorded Laps",
    len(valid_laps)
)

col3.metric(
    "Fastest Recorded Lap",
    format_lap_time(fastest_seconds)
)

col4.metric(
    "Average Lap Time",
    format_lap_time(average_seconds)
)

st.caption(
    f"Fastest recorded lap: {fastest_record['Driver']} "
    f"on lap {int(fastest_record['LapNumber'])}. "
    "Metrics include recorded laps and may include pit, "
    "in-laps, out-laps or other unusual laps."
)

st.divider()


# -------------------------------
# 5. DASHBOARD TABS
# -------------------------------
tab1, tab2, tab3 = st.tabs(
    ["🏁 Driver Comparison", "🛞 Tyre Analysis", "🌦️ Weather"]
)

# ===============================
# TAB 1: DRIVER COMPARISON
# ===============================
with tab1:
    st.header("Compare Driver Lap Times")

    drivers = sorted(laps["Driver"].dropna().unique())

    if len(drivers) < 2:
        st.warning("Not enough drivers found for comparison.")
    else:
        default_a = drivers.index("VER") if "VER" in drivers else 0

        default_b = (
            drivers.index("NOR")
            if "NOR" in drivers
            else min(1, len(drivers) - 1)
        )

        c1, c2 = st.columns(2)

        with c1:
            driver_a = st.selectbox(
                "Driver A",
                drivers,
                index=default_a,
                key="driver_a"
            )

        with c2:
            driver_b = st.selectbox(
                "Driver B",
                drivers,
                index=default_b,
                key="driver_b"
            )

        if driver_a == driver_b:
            st.warning("Please select two different drivers.")
        else:
            a = laps.loc[
                laps["Driver"] == driver_a,
                ["LapNumber", "LapSeconds"]
            ].rename(columns={"LapSeconds": "Time_A"})

            b = laps.loc[
                laps["Driver"] == driver_b,
                ["LapNumber", "LapSeconds"]
            ].rename(columns={"LapSeconds": "Time_B"})

            comparison = pd.merge(
                a,
                b,
                on="LapNumber",
                how="inner"
            )

            comparison["Difference"] = (
                comparison["Time_A"] - comparison["Time_B"]
            )

            if comparison.empty:
                st.warning("No matching lap numbers were found.")
            else:
                fig = px.line(
                    comparison,
                    x="LapNumber",
                    y=["Time_A", "Time_B"],
                    markers=True,
                    title="Lap Time Comparison",
                    labels={
                        "LapNumber": "Lap Number",
                        "value": "Lap Time (seconds)",
                        "variable": "Driver"
                    }
                )

                fig.update_layout(template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)

                diff_fig = px.bar(
                    comparison,
                    x="LapNumber",
                    y="Difference",
                    title=f"{driver_a} Time − {driver_b} Time",
                    labels={
                        "LapNumber": "Lap Number",
                        "Difference": "Time Difference (seconds)"
                    }
                )

                diff_fig.add_hline(y=0, line_dash="dash")
                st.plotly_chart(
                    diff_fig,
                    use_container_width=True
                )

                st.caption(
                    "Negative difference: Driver A was faster. "
                    "Positive difference: Driver B was faster."
                )

                st.subheader("Comparison Table")
                st.dataframe(
                    comparison.round(3),
                    use_container_width=True
                )

# ===============================
# TAB 2: TYRE ANALYSIS
# ===============================
with tab2:
    st.header("Tyre Compounds and Degradation")

    required = ["Compound", "TyreLife", "Stint"]

    missing = [
        column for column in required
        if column not in laps.columns
    ]

    if missing:
        st.warning(
            "Tyre analysis is unavailable because these "
            f"columns are missing: {missing}"
        )
    else:
        tyre_drivers = sorted(
            laps["Driver"].dropna().unique()
        )

        tyre_driver = st.selectbox(
            "Select driver for tyre analysis",
            tyre_drivers,
            key="tyre_driver"
        )

        tyre_data = laps[
            laps["Driver"] == tyre_driver
        ].copy()

        tyre_data = tyre_data.dropna(
            subset=[
                "Compound",
                "TyreLife",
                "Stint",
                "LapSeconds"
            ]
        )

        # Exclude pit-in and pit-out laps when these fields exist.
        for column in ["PitInTime", "PitOutTime"]:
            if column in tyre_data.columns:
                tyre_data = tyre_data[
                    tyre_data[column].isna()
                ]

        if "IsAccurate" in tyre_data.columns:
            tyre_data = tyre_data[
                tyre_data["IsAccurate"].fillna(False)
            ]

        if tyre_data.empty:
            st.warning(
                "No complete tyre records are available "
                "for this driver."
            )
        else:
            compounds = sorted(
                tyre_data["Compound"].dropna().unique()
            )

            selected_compounds = st.multiselect(
                "Choose tyre compounds",
                compounds,
                default=compounds
            )

            tyre_data = tyre_data[
                tyre_data["Compound"].isin(selected_compounds)
            ].copy()

            if tyre_data.empty:
                st.info("Select at least one tyre compound.")
            else:
                fig = px.line(
                    tyre_data.sort_values(
                        ["Stint", "TyreLife", "LapNumber"]
                    ),
                    x="TyreLife",
                    y="LapSeconds",
                    color="Compound",
                    line_group="Stint",
                    markers=True,
                    hover_data=["LapNumber", "Stint"],
                    title=f"{tyre_driver}: Lap Time vs Tyre Age",
                    labels={
                        "TyreLife": "Tyre Age (laps)",
                        "LapSeconds": "Lap Time (seconds)",
                        "Compound": "Tyre Compound",
                        "Stint": "Stint"
                    }
                )

                fig.update_layout(template="plotly_white")
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.subheader("Tyre and Stint Records")

                st.dataframe(
                    tyre_data[
                        [
                            "LapNumber",
                            "Compound",
                            "TyreLife",
                            "Stint",
                            "LapSeconds"
                        ]
                    ].sort_values("LapNumber"),
                    use_container_width=True
                )

                st.caption(
                    "Lap-time changes do not prove tyre wear alone "
                    "caused the change. Traffic, fuel, track "
                    "conditions and other factors also matter."
                )
                
    st.subheader("Driver Performance Summary")

    driver_summary = (
        valid_laps.groupby("Driver")["LapSeconds"]
        .agg(
            LapsRecorded="count",
            FastestLap="min",
            AverageLap="mean"
        )
        .reset_index()
    )

    driver_summary = driver_summary.sort_values(
        "AverageLap"
    )

    driver_summary["FastestLap"] = (
        driver_summary["FastestLap"].map(format_lap_time)
    )

    driver_summary["AverageLap"] = (
        driver_summary["AverageLap"].map(format_lap_time)
    )

    st.dataframe(
        driver_summary,
        use_container_width=True,
        hide_index=True
    )


# ===============================
# TAB 3: WEATHER ANALYSIS
# ===============================
with tab3:
    st.header("Race Weather Conditions")

    if weather.empty:
        st.warning("No weather measurements are available.")
    else:
        st.write("Available weather measurements:")
        st.dataframe(weather.head(10), use_container_width=True)

        possible_columns = [
            column
            for column in ["AirTemp", "TrackTemp", "Humidity", "WindSpeed"]
            if column in weather.columns
        ]

        if not possible_columns:
            st.info("No recognized weather measurement columns found.")
        else:
            weather_variable = st.selectbox(
                "Choose a weather measurement",
                possible_columns
            )

            if "Time" in weather.columns:
                weather_fig = px.line(
                    weather,
                    x="Time",
                    y=weather_variable,
                    markers=True,
                    title=f"{weather_variable} During the Race",
                    labels={
                        "Time": "Session Time",
                        weather_variable: weather_variable
                    }
                )

                weather_fig.update_layout(
                    template="plotly_white"
                )

                st.plotly_chart(
                    weather_fig,
                    use_container_width=True
                )
            else:
                st.info(
                    "The weather data has no Time column "
                    "for plotting."
                )

st.divider()
st.caption(
    "F1 Race Analytics | Historical data provided by FastF1"
)
