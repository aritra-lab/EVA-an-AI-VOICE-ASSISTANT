from pycaw.pycaw import AudioUtilities
import pyautogui
import random
from core.logger import log_exception
def get_system_volume():
    device = AudioUtilities.GetSpeakers()
    volume = device.EndpointVolume
    current = volume.GetMasterVolumeLevelScalar()
    return int(current * 100)
def set_system_volume(percent):
    device = AudioUtilities.GetSpeakers()
    volume = device.EndpointVolume
    percent = max(0, min(100, percent))
    volume.SetMasterVolumeLevelScalar(percent / 100, None)
def volume_percentage(command):
    try:
        if "set volume to" in command:
            text = command.replace("set volume to", "")
            text = text.replace("percent", "")
            percent = int(text.strip())
            set_system_volume(percent)
            return(f"VOLUME SET TO {percent} PERCENT.")
    except Exception as e:
        log_exception(e, "VOLUME")
        return("PLEASE TELL ME A VALID VOLUME PERCENTAGE.")
    return None
def volume_control(command):
    if "mute" in command:
        pyautogui.press("volumemute")
        responses=["DEVICE MUTED.", "I HAVE MUTED THE DEVICE FOR YOU.", "THE DEVICE IS NOW MUTED."]
        reply=random.choice(responses)
        return(reply)
    elif "unmute" in command:
        pyautogui.press("volumemute")
        responses=["DEVICE UNMUTED.", "I HAVE UNMUTED THE DEVICE FOR YOU.", "THE DEVICE IS NOW UNMUTED."]
        reply=random.choice(responses)
        return(reply)    
    elif "increase volume by" in command:
        amount = int(command.replace("increase volume by", "").strip())
        current = get_system_volume()
        new_volume = min(100, current + amount)
        set_system_volume(new_volume)
        return(f"VOLUME INCREASED TO {new_volume} PERCENT.")
    elif "decrease volume by" in command:
        amount = int(command.replace("decrease volume by", "").strip())
        current = get_system_volume()
        new_volume = max(0, current - amount)
        set_system_volume(new_volume)
        return(f"VOLUME DECREASED TO {new_volume} PERCENT.")
    elif "current volume" in command or "what is the volume" in command:
        current = get_system_volume()
        return(f"CURRENT VOLUME IS {current} PERCENT.")
    return None