from modules import volume
from modules import weather
from core.speech import speak
from config import WEATHER_COMMANDS

def volume_control_command(command):
    reply = volume.volume_control(command)
    if reply:
        speak(reply)
        return True
    return False

def volume_percentage_command(command):
    reply = volume.volume_percentage(command)
    if reply:
        speak(reply)
        return True
    return False

def weather_command(command):
    if any(phrase in command for phrase in WEATHER_COMMANDS):
        for phrase in WEATHER_COMMANDS:
            if phrase in command:
                city = command.split(phrase, 1)[-1].strip()
                break
        else:
            city = "Kolkata"  # Default city if none specified

        report = weather.get_weather(city)
        if report:
            speak(report)
        else:
            speak("I COULDN'T FIND WEATHER INFORMATION FOR THAT CITY.")
        return True
    return False
