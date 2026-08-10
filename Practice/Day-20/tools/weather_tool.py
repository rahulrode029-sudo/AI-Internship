import requests


def get_weather(city: str) -> str:
    """
    Get current weather information for a city.

    Args:
        city: City name.

    Returns:
        Current weather information.
    """

    try:
        if not city.strip():
            return "Weather error: City name is required."

        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_response = requests.get(
            geo_url,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=10,
        )

        geo_response.raise_for_status()

        geo_data = geo_response.json()

        if "results" not in geo_data:
            return f"Weather error: City '{city}' not found."

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
            },
            timeout=10,
        )

        weather_response.raise_for_status()

        weather_data = weather_response.json()
        current = weather_data["current"]

        return (
            f"Weather for {city_name}:\n"
            f"Temperature: {current['temperature_2m']}°C\n"
            f"Humidity: {current['relative_humidity_2m']}%\n"
            f"Wind Speed: {current['wind_speed_10m']} km/h\n"
            f"Weather Code: {current['weather_code']}"
        )

    except requests.RequestException as e:
        return f"Weather API error: {e}"

    except Exception as e:
        return f"Weather error: {e}"