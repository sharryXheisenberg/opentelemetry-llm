import requests
import sys

def get_weather(city: str = "London"):
    print(f"Fetching weather for {city}...\n")
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    
    try:
        geo_response = requests.get(geo_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            print(f" City '{city}' not found. Try a different spelling or nearby city.")
            return
            
        result = geo_data["results"][0]
        lat = result["latitude"]
        lon = result["longitude"]
        city_name = result.get("name", city)
        country = result.get("country", "")
        
    except Exception as e:
        print(" Error finding location. Check your internet connection.")
        print(e)
        return

    
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
        f"weather_code,wind_speed_10m,wind_direction_10m"
        f"&timezone=auto"
    )
    
    try:
        response = requests.get(weather_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data["current"]
        weather_codes = {
            0: "Clear sky ☀️",
            1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅", 3: "Overcast ☁️",
            45: "Fog 🌫️", 48: "Depositing rime fog 🌫️",
            51: "Light drizzle 🌧️", 53: "Moderate drizzle 🌧️", 55: "Dense drizzle 🌧️",
            61: "Slight rain 🌦️", 63: "Moderate rain 🌧️", 65: "Heavy rain 🌧️",
            71: "Slight snow ❄️", 73: "Moderate snow ❄️", 75: "Heavy snow ❄️",
            80: "Rain showers 🌦️", 81: "Moderate rain showers 🌧️", 82: "Violent rain showers ⛈️",
            95: "Thunderstorm ⛈️", 96: "Thunderstorm with hail ⛈️", 99: "Thunderstorm with heavy hail ⛈️"
        }
        
        description = weather_codes.get(current["weather_code"], "Unknown conditions")
        
        print(f"🌍 Weather in **{city_name}, {country}**")
        print(f"🌡️  Temperature     : {current['temperature_2m']}°C")
        print(f"🌡️  Feels like      : {current['apparent_temperature']}°C")
        print(f"💧  Humidity        : {current['relative_humidity_2m']}%")
        print(f"🌬️  Wind            : {current['wind_speed_10m']} km/h at {current['wind_direction_10m']}°")
        print(f"☁️  Conditions      : {description}")
        print(f"🕒 Updated at      : {current['time']}")
        
    except Exception as e:
        print(" Error fetching weather data.")
        print("Please check your internet connection.")
        print(e)

if __name__ == "__main__":
    city = sys.argv[1] if len(sys.argv) > 1 else "London"
    get_weather(city)