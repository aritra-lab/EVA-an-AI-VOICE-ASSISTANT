import requests
from core.logger import log_exception
API_KEY = "5c02accb6182c17219d5bbb095d45854"
def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )
    try:
        response = requests.get(url)
        data = response.json()
        if str(data.get("cod")) == "200":
            temp = data["main"]["temp"]
            feels = data["main"]["feels_like"]
            desc = data["weather"][0]["description"]
            return (
                f"The temperature in {city} is {temp} degrees Celsius. "
                f"It feels like {feels} degrees with {desc}."
            )
        return None
    except Exception as e:
        log_exception(e, "WEATHER")
        return None