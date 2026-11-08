import random
from modules import notes
from core.speech import speak
from core.logger import log_exception

from config import ADD_NOTES, SHOW_NOTES, DELETE_NOTES

def take_note(command):
    if any(alias in command for alias in ADD_NOTES):
        note = ""
        for alias in ADD_NOTES:
            if alias in command:
                note = command.replace(alias, "", 1).strip()
                break
        if not note:
            speak("PLEASE TELL ME WHAT NOTE TO SAVE.")
            return True
        notes.add_note(note)
        responses = [
            f"NOTE TAKEN: {note}",
            f"I HAVE STORED THE NOTE: {note}",
            f"NOTE SAVED: {note}"
        ]
        reply = random.choice(responses)
        speak(reply)
        return True
    return False


def show_notes(command):
    if any(alias in command for alias in SHOW_NOTES):
        all_notes=notes.get_notes()
        if all_notes:
            reply="HERE ARE ALL THE NOTES I HAVE TAKEN:\n"
            for note_id, note_text in all_notes:
                reply += f"{note_id}: {note_text}\n"
            speak(reply)
            return True
        else:
            responses = ["I DON'T HAVE ANY NOTES YET.","NO NOTES FOUND.","MY NOTEBOOK IS CURRENTLY EMPTY."]
            reply = random.choice(responses)
            speak(reply)
            return True
    return False


def delete_note_command(command):
    if any(alias in command for alias in DELETE_NOTES):
        for alias in DELETE_NOTES:
            if alias in command:
                keyword = command.replace(alias, "", 1).strip()
                break
        try:
            if keyword.isdigit():
            
                notes.delete_note(int(keyword))

                reply = f"NOTE {keyword} HAS BEEN DELETED."
            else:
            
                result = notes.find_note_by_keyword(keyword)

                if result:
                
                    note_id = result[0][0]

                    notes.delete_note(note_id)

                    reply = f"NOTE MATCHING {keyword} HAS BEEN DELETED."

                else:
                
                    reply = f"I COULD NOT FIND ANY NOTE MATCHING {keyword}"
            speak(reply)
            return True
        except Exception as e:
        
            log_exception(e, "NOTES")

            speak("SOMETHING WENT WRONG WHILE DELETING THE NOTE.")

            return True
    return False