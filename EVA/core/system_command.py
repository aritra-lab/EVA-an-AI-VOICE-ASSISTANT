from modules import battery
from modules import screenshot
from modules import system_info
from core.speech import speak

def battery_status(command):
    if any(word in command for word in ["battery status", "battery percentage","what is the battery percentage", "how much battery"]):
        if "battery" in command:
            speak(battery.battery_status())
            return True 
        return False


def screenshot_command(command):
    if any(word in command for word in [
        "take a screenshot",
        "capture screen",
        "take a screen shot",
        "capture the screen",
    ]):
        filename = screenshot.take_screenshot()
        speak(f"SCREENSHOT SAVED AS {filename}")
        return True
    return False

def system_information(command):
    if any(word in command for word in [
        "system information",
        "system info",
        "computer information",
        "computer info"
    ]):
        speak(system_info.get_system_info())
        return True
    return False
