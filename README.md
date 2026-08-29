# Weather Information Dashboard — Streamlit + REST API

## 1. Project Overview

This project demonstrates how to consume a REST API from a Streamlit application and convert the JSON response into an interactive weather dashboard.

The application uses the Open-Meteo Weather Forecast API.

## 2. Features

- Select a city from a predefined list
- Enter latitude and longitude manually
- Fetch current weather data
- Display temperature
- Display apparent/feels-like temperature
- Display humidity
- Display wind speed
- Display precipitation
- Display weather condition
- Display 7-day forecast
- Display hourly forecast
- Interactive temperature chart
- Precipitation probability chart
- Download forecast as CSV
- Display raw JSON API response
- Error handling
- API response caching
- Refresh button

## 3. Technology Stack

- Python
- Streamlit
- REST API
- Requests
- Pandas
- Plotly
- Open-Meteo API

## 4. Project Structure

```text
Weather_Streamlit_REST_API_Project/
│
├── app.py
├── requirements.txt
├── README.md
└── run_app.bat
```

## 5. Installation

Open Command Prompt or PowerShell in the project folder.

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 6. Run the Application

Use:

```bash
streamlit run app.py
```

The browser should open automatically.

If it does not, copy the local URL displayed in the terminal into your browser.

## 7. How the REST API Works

The application sends an HTTP GET request to:

```text
https://api.open-meteo.com/v1/forecast
```

Parameters include latitude, longitude, current weather variables, hourly variables, daily variables, forecast length and timezone.

Example concept:

```python
response = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": 18.5204,
        "longitude": 73.8567,
        "current": "temperature_2m,relative_humidity_2m",
        "forecast_days": 7,
        "timezone": "auto"
    }
)

data = response.json()
```

## 8. Learning Outcomes

After completing this project, learners can:

1. Understand REST APIs.
2. Send GET requests from Python.
3. Pass query parameters to an API.
4. Parse JSON responses.
5. Convert API JSON into Pandas DataFrames.
6. Display API results using Streamlit.
7. Create interactive charts.
8. Add caching to API calls.
9. Handle API errors.
10. Build a real-world Streamlit application.

## 9. Suggested Udemy Teaching Flow

### Lecture 1
What is a REST API?

### Lecture 2
Understanding the Open-Meteo API.

### Lecture 3
Testing an API with Python Requests.

### Lecture 4
Reading JSON responses.

### Lecture 5
Building the Streamlit interface.

### Lecture 6
Adding city selection.

### Lecture 7
Connecting Streamlit to the API.

### Lecture 8
Displaying current weather.

### Lecture 9
Displaying a 7-day forecast.

### Lecture 10
Creating interactive Plotly charts.

### Lecture 11
Adding caching.

### Lecture 12
Adding error handling.

### Lecture 13
Adding CSV download.

### Lecture 14
Testing the complete application.

### Lecture 15
Deployment preparation.

## 10. Student Assignment

Modify the application to add:

- Sunrise and sunset
- UV index
- Weather icons
- 10-day forecast
- Wind direction
- Searchable city list
- Better dashboard styling

## 11. Extension Project

Build a **Multi-City Weather Comparison Dashboard**.

The user selects 3–5 cities and the application compares:

- Temperature
- Humidity
- Wind speed
- Rain probability
- Weekly temperature trends

## 12. API Reference

Open-Meteo documentation:

https://open-meteo.com/en/docs

Streamlit documentation:

https://docs.streamlit.io/
