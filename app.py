import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Weather Information Dashboard",
    page_icon="🌤️",
    layout="wide"
)

st.title(" Weather Information Dashboard")
st.caption("Streamlit + REST API project using Open-Meteo")

CITY_COORDINATES = {
    "Pune": (18.5204, 73.8567),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Nandgaon": (35.6762, 139.6503),
}

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

@st.cache_data(ttl=600)
def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m"
        ]),
        "hourly": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation_probability",
            "precipitation",
            "wind_speed_10m",
            "weather_code"
        ]),
        "daily": ",".join([
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max"
        ]),
        "forecast_days": 7,
        "timezone": "auto"
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    return response.json()

def make_hourly_dataframe(data):
    hourly = data["hourly"]
    df = pd.DataFrame(hourly)
    df["time"] = pd.to_datetime(df["time"])
    df["weather_description"] = df["weather_code"].map(
        lambda x: WEATHER_CODES.get(int(x), "Unknown")
    )
    return df

def make_daily_dataframe(data):
    daily = data["daily"]
    df = pd.DataFrame(daily)
    df["time"] = pd.to_datetime(df["time"])
    df["weather_description"] = df["weather_code"].map(
        lambda x: WEATHER_CODES.get(int(x), "Unknown")
    )
    return df

with st.sidebar:
    st.header("📍 Location")

    location_mode = st.radio(
        "Choose location",
        ["Select a city", "Enter coordinates"]
    )

    if location_mode == "Select a city":
        city = st.selectbox("City", list(CITY_COORDINATES.keys()))
        latitude, longitude = CITY_COORDINATES[city]
        location_name = city
    else:
        latitude = st.number_input(
            "Latitude", min_value=-90.0, max_value=90.0,
            value=18.5204, format="%.4f"
        )
        longitude = st.number_input(
            "Longitude", min_value=-180.0, max_value=180.0,
            value=73.8567, format="%.4f"
        )
        location_name = f"{latitude:.4f}, {longitude:.4f}"

    refresh = st.button("🔄 Refresh Weather")

try:
    if refresh:
        st.cache_data.clear()

    data = get_weather(latitude, longitude)

    current = data["current"]
    units = data["current_units"]

    st.subheader(f"📍 {location_name}")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Temperature",
        f"{current['temperature_2m']}{units['temperature_2m']}"
    )
    col2.metric(
        "Feels Like",
        f"{current['apparent_temperature']}{units['apparent_temperature']}"
    )
    col3.metric(
        "Humidity",
        f"{current['relative_humidity_2m']}{units['relative_humidity_2m']}"
    )
    col4.metric(
        "Wind Speed",
        f"{current['wind_speed_10m']} {units['wind_speed_10m']}"
    )
    col5.metric(
        "Precipitation",
        f"{current['precipitation']} {units['precipitation']}"
    )

    st.info(
        f"**Current condition:** "
        f"{WEATHER_CODES.get(int(current['weather_code']), 'Unknown')}  |  "
        f"Updated: {current['time']}"
    )

    hourly_df = make_hourly_dataframe(data)
    daily_df = make_daily_dataframe(data)

    tab1, tab2, tab3, tab4 = st.tabs([
        "7-Day Forecast",
        "Hourly Forecast",
        "Temperature Chart",
        "Raw API Data"
    ])

    with tab1:
        display_daily = daily_df[[
            "time",
            "weather_description",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max"
        ]].copy()

        display_daily.columns = [
            "Date", "Condition", "Max Temp (°C)",
            "Min Temp (°C)", "Precipitation (mm)",
            "Max Wind (km/h)"
        ]

        st.dataframe(
            display_daily,
            hide_index=True,
            use_container_width=True
        )

        csv = display_daily.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Forecast CSV",
            csv,
            "weather_forecast.csv",
            "text/csv"
        )

    with tab2:
        selected_day = st.date_input(
            "Select date for hourly forecast",
            value=hourly_df["time"].dt.date.iloc[0]
        )

        day_df = hourly_df[
            hourly_df["time"].dt.date == selected_day
        ].copy()

        if day_df.empty:
            st.warning("No hourly data available for the selected date.")
        else:
            st.dataframe(
                day_df[[
                    "time",
                    "temperature_2m",
                    "relative_humidity_2m",
                    "precipitation_probability",
                    "precipitation",
                    "wind_speed_10m",
                    "weather_description"
                ]],
                hide_index=True,
                use_container_width=True
            )

    with tab3:
        chart = px.line(
            hourly_df,
            x="time",
            y="temperature_2m",
            title="Hourly Temperature Forecast",
            markers=True,
            labels={
                "time": "Time",
                "temperature_2m": "Temperature (°C)"
            }
        )
        st.plotly_chart(chart, use_container_width=True)

        rain_chart = px.bar(
            hourly_df,
            x="time",
            y="precipitation_probability",
            title="Hourly Precipitation Probability",
            labels={
                "time": "Time",
                "precipitation_probability": "Probability (%)"
            }
        )
        st.plotly_chart(rain_chart, use_container_width=True)

    with tab4:
        with st.expander("View current API response"):
            st.json(current)

        with st.expander("View complete API response"):
            st.json(data)

    st.divider()
    st.caption(
        "Data source: Open-Meteo Weather Forecast API. "
        "This application is an educational REST API + Streamlit project."
    )

except requests.exceptions.Timeout:
    st.error("The weather API request timed out. Please try again.")
except requests.exceptions.RequestException as e:
    st.error(f"API request failed: {e}")
except Exception as e:
    st.error(f"Unexpected error: {e}")
