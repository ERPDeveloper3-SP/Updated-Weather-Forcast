import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Weather Dashboard",
    layout="wide"
)

st.title("Weather Information Dashboard")
st.write("Streamlit + REST API")

# -----------------------------
# City Coordinates
# -----------------------------

cities = {
    "Pune": (18.5204, 73.8567),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
}

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("Location")

city = st.sidebar.selectbox(
    "Select City",
    list(cities.keys())
)

latitude, longitude = cities[city]

# -----------------------------
# API Function
# -----------------------------

def get_weather(lat, lon):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "precipitation,"
            "wind_speed_10m,"
            "weather_code"
        ),
        "hourly": (
            "temperature_2m,"
            "precipitation_probability"
        ),
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_sum"
        ),
        "forecast_days": 7,
        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# -----------------------------
# Get Weather
# -----------------------------

try:

    data = get_weather(
        latitude,
        longitude
    )

    st.success(
        f"Weather data loaded for {city}"
    )

    # -------------------------
    # Current Weather
    # -------------------------

    current = data["current"]

    st.subheader("Current Weather")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Temperature",
        f"{current['temperature_2m']} °C"
    )

    col2.metric(
        "Humidity",
        f"{current['relative_humidity_2m']} %"
    )

    col3.metric(
        "Feels Like",
        f"{current['apparent_temperature']} °C"
    )

    col4.metric(
        "Wind Speed",
        f"{current['wind_speed_10m']} km/h"
    )

    # -------------------------
    # Daily Forecast
    # -------------------------

    st.subheader("7-Day Forecast")

    daily = data["daily"]

    df = pd.DataFrame({
        "Date": daily["time"],
        "Maximum Temperature": daily["temperature_2m_max"],
        "Minimum Temperature": daily["temperature_2m_min"],
        "Precipitation": daily["precipitation_sum"]
    })

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------
    # Temperature Chart
    # -------------------------

    st.subheader("Temperature Forecast")

    fig = px.line(
        df,
        x="Date",
        y=[
            "Maximum Temperature",
            "Minimum Temperature"
        ],
        markers=True,
        title=f"7-Day Temperature Forecast - {city}"
    )
    

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------------
    # Raw API Response
    # -------------------------

    with st.expander(
        "View REST API Response"
    ):
        st.json(data)


except requests.exceptions.RequestException as e:

    st.error(
        f"Weather API error: {e}"
    )

except Exception as e:

    st.error(
        f"Application error: {e}"
    )