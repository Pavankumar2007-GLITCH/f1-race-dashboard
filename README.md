# F1 Race Analytics Dashboard

An interactive Formula 1 analytics dashboard built with Python, FastF1, Pandas, Plotly, and Streamlit.

## Features

- **Driver comparison:** Compare lap times between two drivers and visualize their lap-by-lap time differences.
- **Tyre analysis:** Explore tyre compounds, tyre age, stints, and lap-time trends.
- **Weather analysis:** Visualize available track and weather measurements.
- **Race summary:** View recorded laps, driver counts, fastest recorded lap, and average lap time.

## Tech Stack

- Python
- FastF1
- Pandas
- Plotly
- Streamlit

## Run Locally

1. Clone or download this repository.
2. Install the dependencies:

   `python -m pip install -r requirements.txt`

3. Start the application:

   `python -m streamlit run app.py`

4. Open the local URL displayed in the terminal.

## Data

Historical Formula 1 session data is retrieved through FastF1. Data availability and completeness may vary by session.

## Limitations

Lap times can be affected by pit stops, traffic, safety cars, fuel load, track conditions, and other factors. Observed lap-time changes should not be interpreted as tyre degradation alone.

## Future Improvements

- Filter outliers and unusual laps.
- Add driver-specific pace metrics.
- Improve stint comparisons and tyre degradation estimates.
- Add race and season selection.
- Deploy the dashboard publicly.

