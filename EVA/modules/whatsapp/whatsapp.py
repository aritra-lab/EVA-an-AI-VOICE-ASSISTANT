
import pyperclip
import webbrowser
import re

def open_whatsapp():
    try:
        import webbrowser

        webbrowser.open("https://web.whatsapp.com/")
        return True

    except Exception as e:
        print(f"WHATSAPP OPEN ERROR: {e}")
        return False

def open_whatsapp_chat(phone):

    try:
        phone = re.sub(r"[\s\-()]", "", phone)
        phone = phone.lstrip("+")

        if not re.fullmatch(r"[0-9]{8,15}", phone):
            print("EVA: INVALID PHONE NUMBER.")
            return False

        url = f"https://web.whatsapp.com/send?phone={phone}"

        webbrowser.open(url)

        print("EVA: WHATSAPP CHAT PAGE OPENED.")
        return True

    except Exception as e:
        print(f"WHATSAPP CHAT ERROR: {e}")
        return False

def prepare_whatsapp_message(contact, message):

    try:
        if not contact or not message:
            print("EVA: CONTACT OR MESSAGE IS MISSING.")
            return False

        print("\n===== WHATSAPP MESSAGE PREVIEW =====")
        print(f"RECIPIENT: {contact}")
        print(f"MESSAGE: {message}")

        confirmation = input(
            "EVA: COPY THIS MESSAGE? (YES/NO): "
        ).strip().lower()

        if confirmation != "yes":
            print("EVA: MESSAGE CANCELLED.")
            return False

        pyperclip.copy(message)

        print("EVA: MESSAGE COPIED TO CLIPBOARD.")
        return True

    except Exception as e:
        print(f"WHATSAPP ERROR: {e}")
        return False
