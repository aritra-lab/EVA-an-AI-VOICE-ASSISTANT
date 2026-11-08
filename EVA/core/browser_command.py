from modules import browser
from core.speech import speak

def tab_control_command(command):
    reply = browser.tab_control(command)
    if reply:
        speak(reply)
        return True
    return False

def search_web_command(command):
    reply = browser.search_web(command)
    if reply:
        speak(reply)
        return True
    return False 
