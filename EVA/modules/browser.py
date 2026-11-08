import pyautogui
import webbrowser
def tab_control(command):
    if any(word in command for word in [
        "close the tab",
        "close the current tab",
        "close this tab",
        "close tab"
    ]):
        pyautogui.hotkey("ctrl","w")
        return "CURRENT TAB CLOSED."

    elif "next tab" in command or "switch the tab" in command:
        pyautogui.hotkey("ctrl", "tab")
        return "SWITCHING TO NEXT TAB."

    elif "new tab" in command or "open another tab" in command:
        pyautogui.hotkey("ctrl", "t")
        return "OPENING NEW TAB."
    return None
def search_web(command):
    if "search" in command:

        main = command

        for word in [
            "search for",
            "search",
            "in google",
            "on google",
            "in youtube",
            "on youtube",
            "google",
            "youtube"
        ]:
            main = main.replace(word, "")

        main = main.strip()

        web = "google"

        urls = {
            "google": "https://www.google.com/search?q=",
            "youtube": "https://www.youtube.com/results?search_query="
        }

        if "youtube" in command:
            web = "youtube"

        webbrowser.open(urls[web] + main)

        return f"SEARCHING FOR {main} ON {web.upper()}..."

    return None