import random
from modules import memory as memory_db
from core.speech import speak
from core.logger import log_exception

from config import REMEMBER_MEMORY 
from config import RECALL_MEMORY
from config import SHOW_MEMORIES
from config import FORGET_MEMORY
def memory(command):
    if any(alias in command for alias in REMEMBER_MEMORY):
        for alias in REMEMBER_MEMORY:
            if alias in command:
                main = command.replace(alias, "", 1).strip()
                break
        try:
            if " is " in main:
                before, after = main.split(" is ", 1)
            else:
                speak("Please say: remember X is Y")
                return True
            key=before.strip()
            value=after.strip()
            reply = memory_db.remember(key, value)
            if "my" in key:
                key=key.replace("my ", "your ")
            elif "your" in key:
                key=key.replace("your ", "my ")
            responses=[f"I WILL REMEMBER THAT {key} IS {value}.", f"GOT IT! {key} IS NOW STORED IN MY MEMORY AS {value}.", f"MEMORY UPDATED: {key} IS {value}. I WILL REMEMBER THIS FOR YOU."]
            reply=random.choice(responses)
            speak(reply)
            return True
        except Exception as e:
            log_exception(e, "MEMORY")
            reply="I'M SORRY, I COULDN'T UNDERSTAND THE MEMORY COMMAND. PLEASE USE IS IN THE COMMAND LIKE 'REMEMBER [KEY] IS [VALUE]'."
            speak(reply)
    return False
def recall_memory(command):
    if any(alias in command for alias in RECALL_MEMORY):
        for alias in RECALL_MEMORY:
            if alias in command:
                main = command.replace(alias, "", 1).strip()
                break
        key=main.strip()
        value=memory_db.recall(key)
        try:
            if value:
                if "my" in key:
                    key=key.replace("my ", "your ")
                elif "your" in key:
                    key=key.replace("your ", "my ")
                responses=[ f"I remember that {key} is {value}", f"The memory for {key} is {value}", f"{key} is stored in my memory as {value}" ]
                reply = random.choice(responses)
                speak(reply)
                return True
            return False
        except Exception as e:
            print("Recall Error:", e)
            print("EVA: ", "I'M SORRY, I ENCOUNTERED AN ERROR WHILE RECALLING MEMORY.")
            speak("I'M SORRY, I ENCOUNTERED AN ERROR WHILE RECALLING MEMORY.")
            return True
    return False
def show_memories(command):
    if any(alias in command for alias in SHOW_MEMORIES):
        memories=memory_db.get_all_memories()
        if memories:
            responses=["HERE ARE ALL THE MEMORIES I HAVE STORED:\n", "LIST OF MY MEMORIES:\n", "HERE ARE THE MEMORIES I REMEMBER:\n"]
            reply=random.choice(responses)
            for key, value in memories:
                if "my" in key:
                    key=key.replace("my ", "your ")
                elif "your" in key:
                    key=key.replace("your ", "my ")
                reply += f"{key}: {value}\n"
            speak(reply)
            return True
        else:
            responses=["I DON'T HAVE ANY MEMORIES STORED YET.", "NO MEMORIES FOUND IN MY BRAIN.", "MY MEMORY IS CURRENTLY EMPTY."]
            reply=random.choice(responses)
            speak(reply)
            return True
    return False
def forget_memory(command):
    if any(alias in command for alias in FORGET_MEMORY):
        for alias in FORGET_MEMORY:
            if alias in command:
                key = command.replace(alias, "", 1).strip()
                break
        if " is " in key:
            key=key.split(" is ")[0].strip()
        memory_db.forget(key)
        reply=f"I HAVE FORGOTTEN THE MEMORY FOR {key}."
        speak(reply)
        return True
    return False