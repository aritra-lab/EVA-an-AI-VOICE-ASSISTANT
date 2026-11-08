import pyperclip

from modules.whatsapp import contacts, whatsapp
from core.speech import speak
import re

def open_whatsapp_command(command):

    if "open whatsapp" in command or "open whatsapp web" in command:
        speak("OPENING WHATSAPP WEB.")

        if whatsapp.open_whatsapp():
            speak("WHATSAPP WEB OPENED.")
        else:
            speak("I COULD NOT OPEN WHATSAPP.")

        return True

    return False



def prepare_whatsapp_message(contact, message):
    try:
        if not contact or not message:
            print("EVA: CONTACT OR MESSAGE IS MISSING.")
            return False

        while True:
            print("\n===== WHATSAPP MESSAGE PREVIEW =====")
            print(f"RECIPIENT: {contact}")
            print(f"MESSAGE: {message}")

            choice = input(
                "\nEVA: COPY, EDIT OR CANCEL? "
                "(YES/EDIT/NO): "
            ).strip().lower()

            if choice == "yes":
                pyperclip.copy(message)
                print("EVA: MESSAGE COPIED TO CLIPBOARD.")
                return True

            elif choice == "edit":
                new_message = input(
                    "EVA: ENTER YOUR UPDATED MESSAGE: "
                ).strip()

                if not new_message:
                    print("EVA: MESSAGE CANNOT BE EMPTY.")
                    continue

                message = new_message
                print("EVA: MESSAGE UPDATED.")

            elif choice == "no":
                print("EVA: MESSAGE CANCELLED.")
                return False

            else:
                print("EVA: PLEASE ENTER YES, EDIT OR NO.")

    except Exception as e:
        print(f"WHATSAPP ERROR: {e}")
        return False


def add_whatsapp_contact_command(command):

    if (
        "add whatsapp contact" in command
        or "save whatsapp contact" in command
    ):

        speak("PLEASE ENTER THE CONTACT NAME.")
        name = input("CONTACT NAME: ").strip()

        if not name:
            speak("CONTACT NAME CANNOT BE EMPTY.")
            return True

        speak("PLEASE ENTER THE PHONE NUMBER.")
        phone = input("PHONE NUMBER: ").strip()

        if not phone:
            speak("PHONE NUMBER CANNOT BE EMPTY.")
            return True

        print("\n===== NEW WHATSAPP CONTACT =====")
        print(f"NAME: {name}")
        print(f"PHONE: {phone}")

        confirmation = input(
            "SAVE THIS CONTACT? (YES/NO): "
        ).strip().lower()

        if confirmation != "yes":
            speak("CONTACT ADDITION CANCELLED.")
            return True

        if contacts.add_contact(name, phone):
            speak("CONTACT SAVED SUCCESSFULLY.")
        else:
            speak("I COULD NOT SAVE THIS CONTACT.")

        return True

    return False

def show_whatsapp_contacts_command(command):

    if (
        "show whatsapp contacts" in command
        or "show list of whatsapp contacts" in command
    ):

        saved_contacts = contacts.get_all_contacts()

        if not saved_contacts:
            speak("YOU HAVE NO WHATSAPP CONTACTS SAVED.")
            return True

        print("\n===== SAVED WHATSAPP CONTACTS =====")

        for index, item in enumerate(saved_contacts, start=1):
            contact_id, name, phone = item
            print(f"{index}. {name} - {phone}")

        speak(f"YOU HAVE {len(saved_contacts)} CONTACTS SAVED.")

        return True

    return False


def open_whatsapp_chat_command(command):

    if "open whatsapp chat" not in command or "open whatsapp chats" not in command:
        return False

    speak("PLEASE ENTER THE CONTACT NAME.")
    query = input("CONTACT NAME: ").strip()

    if not query:
        speak("CONTACT NAME CANNOT BE EMPTY.")
        return True

    # Search saved contacts
    results = contacts.search_contacts(query)

    if not results:
        speak("NO SAVED CONTACT FOUND.")
        return True

    print("\n===== CONTACT SEARCH RESULTS =====")

    for index, item in enumerate(results, start=1):
        contact_id, name, phone = item
        print(f"{index}. {name} - {phone}")

    try:
        choice = int(input("SELECT CONTACT NUMBER: "))

        if choice < 1 or choice > len(results):
            speak("INVALID CONTACT SELECTION.")
            return True

    except ValueError:
        speak("PLEASE ENTER A VALID NUMBER.")
        return True

    contact_id, name, phone = results[choice - 1]

    print(f"\nSELECTED CONTACT: {name}")
    print(f"PHONE: {phone}")

    confirmation = input(
        "OPEN THIS CONTACT'S WHATSAPP CHAT? (YES/NO): "
    ).strip().lower()

    if confirmation != "yes":
        speak("CHAT OPENING CANCELLED.")
        return True

    if whatsapp.open_whatsapp_chat(phone):
        speak("OPENING WHATSAPP CHAT.")
    else:
        speak("I COULD NOT OPEN THE WHATSAPP CHAT.")

    return True


def smart_whatsapp_message_command(command):

    # Recognize natural-language message commands
    pattern = (
        r"^(?:message|whatsapp message)\s+"
        r"(.+?)\s+saying\s+(.+)$"
    )

    match = re.match(pattern, command.strip(), re.IGNORECASE)

    if not match:
        return False

    contact_query = match.group(1).strip()
    message = match.group(2).strip()

    if not contact_query or not message:
        speak("CONTACT OR MESSAGE IS MISSING.")
        return True

    # Search saved contacts
    results = contacts.search_contacts(contact_query)

    if not results:
        speak("NO SAVED CONTACT FOUND.")
        return True

    # Display matching contacts
    print("\n===== MATCHING CONTACTS =====")

    for index, item in enumerate(results, start=1):
        contact_id, name, phone = item
        print(f"{index}. {name} - {phone}")

    if len(results) == 1:
        selected_contact = results[0]
    else:
        try:
            choice = int(input("SELECT CONTACT NUMBER: "))

            if not 1 <= choice <= len(results):
                speak("INVALID SELECTION.")
                return True

            selected_contact = results[choice - 1]

        except ValueError:
            speak("PLEASE ENTER A VALID NUMBER.")
            return True

    contact_id, name, phone = selected_contact

    recipient = f"{name} ({phone})"

    # Final recipient confirmation
    print("\n===== MESSAGE DETAILS =====")
    print(f"RECIPIENT: {recipient}")
    print(f"MESSAGE: {message}")

    confirmation = input(
        "IS EVERYTHING CORRECT? (YES/NO): "
    ).strip().lower()

    if confirmation != "yes":
        speak("MESSAGE CANCELLED.")
        return True

    # Open the selected chat
    if not whatsapp.open_whatsapp_chat(phone):
        speak("I COULD NOT OPEN THE WHATSAPP CHAT.")
        return True

    # Prepare and copy the approved draft
    if whatsapp.prepare_whatsapp_message(recipient, message):
        speak(
            "MESSAGE COPIED SUCCESSFULLY. "
            "PLEASE REVIEW AND SEND IT MANUALLY."
        )
    else:
        speak("MESSAGE PREPARATION CANCELLED OR FAILED.")

    return True
