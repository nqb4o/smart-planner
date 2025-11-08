import requests

class WeatherForecastTool:
    def __init__(self, api_key: str):
        """
        Initialize the WeatherForecastTool.
        Args:
            api_key (str): Your OpenWeatherMap API key.
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_current_weather(self, place: str):
        """
        Get current weather for a city/place.
        Args:
            place (str): City name.
        Returns:
            dict: JSON response containing current weather data, or empty dict if failed.
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": place,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else {}
        
        except Exception as e:
            return {"error": str(e)}
    
    def get_forecast_weather(self, place: str):
        """
        Get weather forecast for a city/place.
        Args:
            place (str): City name.
        Returns:
            dict: JSON response containing forecast data, or empty dict if failed.
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": place,
                "appid": self.api_key,
                "cnt": 10,           # Number of forecast entries (each is 3-hour step)
                "units": "metric"    # Temp in Celsius instead of Kelvin
            }
            
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else {}
        
        except Exception as e:
            return {"error": str(e)}
