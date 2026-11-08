from modules import automation
from core.speech import speak
from core.speech import speak, take_command

def shutdown_command(command):

    if "shut down the computer" in command or "shutdown the computer" in command or "shut down computer" in command or "shutdown computer" in command or "shutdown the pc" in command or "shut down the pc" in command:
        if confirm_action():
            reply = automation.shutdown_pc()
            speak(reply)
        else:
            speak("SHUTDOWN CANCELLED.")
        return True
    return False

def restart_command(command):

    if "restart computer" in command or "restart the computer" in command or "restart the pc" in command:
        if confirm_action():
            reply = automation.restart_pc()
            speak(reply)
        else:
            speak("RESTART CANCELLED.")
        return True
    return False

def lock_command(command):

    if "lock the computer" in command:
        reply = automation.lock_pc()
        speak(reply)
        return True
    return False

def sleep_command(command):

    if "sleep computer" in command:
        reply = automation.sleep_pc()
        speak(reply)
        return True
    return False

def confirm_action():

    speak("ARE YOU SURE?")
    answer = take_command()
    if "yes" in answer:
        return True
    return False