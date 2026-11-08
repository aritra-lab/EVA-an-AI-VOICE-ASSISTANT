from modules import apps
from core.speech import speak
def open_apps_command(command):
    reply = apps.open_apps(command)
    if reply:
        speak(reply)
        return True
    return False

def close_app_command(command):
    reply = apps.close_app(command)
    if reply:
        speak(reply)
        return True
    return False
