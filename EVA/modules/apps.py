import os
import psutil
import random

from config import APP_ALIASES
from config import PROCESS_NAMES
from config import OPEN_WORDS
def open_apps(command):
    count=0
    opened=False
    opened_apps = []
    if any(word in command for word in OPEN_WORDS):
        if any(alias in command for alias in APP_ALIASES["notepad"]):
            os.system("notepad.exe")
            count += 1
            opened_apps.append("NOTEPAD")
            opened=True
        if any(alias in command for alias in APP_ALIASES["calculator"]):
            os.system("calc.exe")
            count += 1
            opened_apps.append("CALCULATOR")
            opened=True
        if any(alias in command for alias in APP_ALIASES["paint"]):
            os.system("mspaint.exe")
            count += 1
            opened_apps.append("PAINT")         
            opened=True
        if any(alias in command for alias in APP_ALIASES["word"]):
            os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE")
            count += 1
            opened_apps.append("MICROSOFT WORD")
            opened=True
        if any(alias in command for alias in APP_ALIASES["excel"]):
            os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE")
            count += 1
            opened_apps.append("MICROSOFT EXCEL")
            opened=True
        if any(alias in command for alias in APP_ALIASES["powerpoint"]):
            os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE")
            count += 1
            opened_apps.append("MICROSOFT POWERPOINT")
            opened=True
        if any(alias in command for alias in APP_ALIASES["youtube"]):
            opened_apps.append("YOUTUBE")
            os.system("start https://www.youtube.com")
            count += 1
            opened=True
        if any(alias in command for alias in APP_ALIASES["web browser"]):
            opened_apps.append("DEFAULT WEBBROWSER")
            os.system("start https://www.google.com")
            count += 1
            opened=True
        if any(alias in command for alias in APP_ALIASES["chatgpt"]):
            opened_apps.append("chat G.P.T.")
            os.system("start https://chat.openai.com")
            count += 1
            opened=True
        if any(alias in command for alias in APP_ALIASES["instagram"]):
            opened_apps.append("INSTAGRAM")
            os.system("start https://www.instagram.com")
            count += 1
            opened=True
        if any(alias in command for alias in APP_ALIASES["whatsapp"]):
            opened_apps.append("WHATSAPP")
            os.system("start https://web.whatsapp.com")
            count += 1
            opened=True
        if any (alias in command for alias in APP_ALIASES["spotify"]):
            opened_apps.append("SPOTIFY!! HAVE FUN MASTER")
            os.system("start https://open.spotify.com")
            count+=1
            opened=True
        if count > 0:
            responses=[f"{count} APPLICATIONS OPENED SUCCESSFULLY.", f"LAUNCHED {count} APPLICATIONS FOR YOU.", f"{count} APPS ARE NOW OPEN."]
            return f"OPENING {', '.join(opened_apps)}........ {random.choice(responses)}"
        return opened
def close_process(process_name):
    found = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
                proc.kill()
                found = True
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess):
            pass
    return found
def close_app(command):
    if any(word in command for word in ["close", "exit", "quit", "terminate"]):
        count=0
        closed_apps=[]
        for app, aliases in APP_ALIASES.items():
            if any(alias in command for alias in aliases):
                process_name = PROCESS_NAMES.get(app)
                if process_name:
                    if close_process(process_name):
                        count += 1
                        closed_apps.append(app.upper())
                    else:
                        closed_apps.append(app.upper())
    
        if count > 0:
            responses = [
            f"{count} APPLICATIONS CLOSED SUCCESSFULLY.",
            f"TERMINATED {count} APPLICATIONS FOR YOU.",
            f"{count} APPS ARE NOW CLOSED."
            ]

            return (
                f"CLOSING {', '.join(closed_apps)}... "
                f"{random.choice(responses)}"
            )