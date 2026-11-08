print("INITIALIZING EVA...")
import ai_brain
import datetime
import random


print("LOADING BRAIN.......")
#core folder

from core.logger import logger, log_exception

from core.startup import (check_task_reminders, startup_statistics)
from core.commands import (introduction, help_command, timedate, close)
from core.camera_command import (take_selfie_command, detect_faces_command, recognize_owner_command)
from core.whatsapp_command import (open_whatsapp_command, prepare_whatsapp_command, add_whatsapp_contact_command, show_whatsapp_contacts_command, open_whatsapp_chat_command, smart_whatsapp_message_command)
from modules.whatsapp.contacts import initialize_contacts
from core.apps import(open_apps_command, close_app_command)
from core.browser_command import(tab_control_command, search_web_command)
from core.memory_command import (memory, recall_memory, show_memories, forget_memory)
from core.note_command import ( take_note, show_notes, delete_note_command)
from core.task_command import ( add_task_command, show_tasks, complete_task_command, delete_task_command,pending_tasks_command)
from core.system_command import(system_information,screenshot_command,battery_status)
from core.media_command import(volume_control_command, volume_percentage_command, weather_command)
from core.automation_command import (shutdown_command, restart_command,lock_command, sleep_command)
from core import router
from core.speech import speak, take_command

def greet_begining():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greet= "Good Morning"
    elif 12 <= hour < 18:
        greet= "Good Afternoon"
    else:
        greet= "Good Evening"
    return greet + " Everyone!"

print("LOADING FUNCTIONS.......")

initialize_contacts()


router.register(volume_percentage_command)
router.register(volume_control_command)
router.register(screenshot_command)
router.register(battery_status)
router.register(introduction)
router.register(help_command)
router.register(timedate)
router.register(weather_command)
router.register(detect_faces_command)
router.register(take_selfie_command)
router.register(recognize_owner_command)
router.register(open_whatsapp_chat_command)
router.register(open_apps_command)
router.register(close_app_command)
router.register(tab_control_command)
router.register(search_web_command)
router.register(memory)
router.register(recall_memory)
router.register(show_memories)
router.register(forget_memory)
router.register(take_note)
router.register(show_notes)
router.register(delete_note_command)
router.register(add_task_command)
router.register(pending_tasks_command)
router.register(show_tasks)
router.register(complete_task_command)
router.register(delete_task_command)
router.register(open_whatsapp_command)
router.register(prepare_whatsapp_command)
router.register(add_whatsapp_contact_command)
router.register(show_whatsapp_contacts_command)
router.register(smart_whatsapp_message_command)
router.register(system_information)
router.register(shutdown_command)
router.register(restart_command)
router.register(lock_command)
router.register(sleep_command)
router.register(close)
print("EVERYTHING LOADED SUCCESSFULLY. EVA IS NOW ONLINE...........")
logger.info("EVA started successfully.")
def commnd_loop():
    print("======================EVA (YOUR PERSONAL ASSISTANT)==========================")
    greet=greet_begining()
    responses=[f"{greet}! MYSELF EVA, YOUR PERSONAL ASSISTANT. HOW MAY I HELP YOU MASTER?",f"{greet}! I AM EVA, YOUR PERSONAL ASSISTANT. WHAT CAN I DO FOR YOU TODAY?", f"{greet}! I AM EVA, YOUR PERSONAL ASSISTANT. HOW CAN I ASSIST YOU TODAY?"]
    reply=random.choice(responses)
    speak(reply)
    check_task_reminders()
    startup_statistics()
    while True:
        try:
            command=take_command()
            logger.info(f"USER: {command}")
            if command=="":
                continue
            if not router.process(command):
                reply = ai_brain.ask_eva(command)
                speak(reply)
        except Exception as e:
            print("Error:", e)
            reply="I'M SORRY, I ENCOUNTERED AN ERROR WHILE PROCESSING YOUR COMMAND."
            speak(reply)
if __name__ == "__main__":
    commnd_loop()