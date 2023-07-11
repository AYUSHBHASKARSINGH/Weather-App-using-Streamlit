import requests
import json
import datetime
import streamlit as st
import html

# API key for OpenWeatherMap
OPEN_WEATHER_API_KEY = "65e6a933d31eebb023eac0073f2969d4"

# Base URL for OpenWeatherMap API
OPEN_WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# Set page config
st.set_page_config(
    page_title="Weather Information",
    page_icon=":partly_sunny:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Sidebar
st.sidebar.title("Weather App")

# Ask user for city name
city_name = st.sidebar.text_input("Enter city/location name:")

if st.sidebar.button("Get Weather"):
    # Construct URL with city name and API key
    complete_url = OPEN_WEATHER_BASE_URL + "appid=" + OPEN_WEATHER_API_KEY + "&q=" + city_name

    # Send GET request to OpenWeatherMap API
    response = requests.get(complete_url)

    # Parse JSON response
    data = json.loads(response.text)

    # Check if response contains error message
    if "message" in data:
        st.error("Error: " + data["message"])
        st.write("We are Sorry...🥺")
    else:
        # Extract temperature and weather description from response
        temperature = round(data["main"]["temp"] - 273.15, 2)
        weather_desc = data["weather"][0]["main"]
        weather_emoji = {
            "Clear": "☀️",
            "Clouds": "🌤️",
            "Rain": "🌧️",
            "Drizzle": "🌧️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Atmosphere": "🌫️",
            "Haze": "🌫️"
        }
        emoji = weather_emoji.get(weather_desc, "🤷‍♂️")

        # Extract additional weather information from response
        sunrise = data["sys"]["sunrise"]
        sunset = data["sys"]["sunset"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        summary = data["weather"][0]["description"]
        feels_like = round(data["main"]["feels_like"] - 273.15, 2)

        # Convert Unix timestamps to local time
        sunrise_local = datetime.datetime.fromtimestamp(sunrise).strftime('%I:%M %p')
        sunset_local = datetime.datetime.fromtimestamp(sunset).strftime('%I:%M %p')

        # Display basic weather information
        col1, col2 = st.columns(2)

        with col1:
            st.header("Basic Weather Info")
            st.write("Weather: " + weather_desc + " " + html.unescape(emoji))
            st.write("Temperature: " + str(temperature) + " °C")
            st.write("Feels like: " + str(feels_like) + " °C")

        with col2:
            st.header("Additional Weather Info")
            st.write("Humidity: " + str(humidity) + "%")
            st.write("Pressure: " + str(pressure) + " hPa")
            st.write("Sunrise: " + str(sunrise_local))
            st.write("Sunset: " + str(sunset_local))

        # Display weather summary
        st.subheader("Summary")
        st.write(summary)

        # Get additional data from wttr
        wttr_url = 'https://wttr.in/' + city_name + "?0"
        wttr_response = requests.get(wttr_url)
        first_bytes = wttr_response.content[304:307]
        if first_bytes == b'404':
            st.error("Wttr was unable to find your location")
            st.write("We are Sorry...🥺")
        else:
            st.subheader("Additional Info from wttr.in")
            st.components.v1.iframe(wttr_url, height=600)
