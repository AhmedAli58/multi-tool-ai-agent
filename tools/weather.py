import requests
import streamlit as st
from langchain.tools import tool

@tool
def weather(city: str) -> str:
    """
    Fetches the current weather for a given city.
    Input should be a city name as a string.
    Examples: 'London', 'New York', 'Tokyo'
    """
    try:
        api_key = st.secrets["OPENWEATHER_API_KEY"]
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].capitalize()

        return (
            f"Weather in {name}, {country}:\n"
            f"- Condition: {description}\n"
            f"- Temperature: {temp} C (feels like {feels_like} C)\n"
            f"- Humidity: {humidity}%"
        )
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"City '{city}' not found. Please check the spelling."
        return f"Weather API error: {str(e)}"
    except requests.exceptions.Timeout:
        return "Weather API timed out. Please try again."
    except Exception as e:
        return f"Unexpected error fetching weather: {str(e)}"
