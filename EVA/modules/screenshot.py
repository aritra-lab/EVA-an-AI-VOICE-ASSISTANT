import pyautogui
import datetime
import os

def take_screenshot():
    folder="screenshots"
    os.makedirs(folder, exist_ok=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(
        folder,
        f"screenshot_{now}.png"
    )
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    reply= f"SCREENSHOT SAVED AS {filename}"
    return reply