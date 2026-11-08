import random
from modules import task
from core.date_parser import extract_due_date
from core.speech import speak
from core.logger import log_exception

from config import SHOW_TASKS
from config import ADD_TASKS
from config import PENDING_TASKS
from config import COMPLETE_TASKS
from config import DELETE_TASKS


def add_task_command(command):
    if any(alias in command for alias in ADD_TASKS):
        main=command
        for alias in ADD_TASKS:
            if alias in command:
                task_text = command.replace(alias, "", 1).strip()
                break
        if not task_text:
            speak("PLEASE TELL ME THE TASK NAME")
            return True
        task_text, due_date = extract_due_date(task_text)

        priority="normal"

        if "high priority" in task_text:
            priority = "high"
            task_text = task_text.replace("high priority","")

        elif "low priority" in task_text:
            priority = "low"
            task_text = task_text.replace("low priority","")

        task.add_task(task_text, due_date, priority)
        if due_date != "no date":
            reply = f"TASK ADDED: {task_text}. DUE ON {due_date}"
        else:
            reply = f"TASK ADDED: {task_text}"
        speak(reply)
        return True
    return False

def pending_tasks_command(command):
    if any(alias in command for alias in PENDING_TASKS):
        tasks = task.get_pending_tasks()
        if tasks:
            reply = "HERE ARE YOUR PENDING TASKS:\n"

            for task_id, task_text, due_date in tasks:
                reply += (
                    f"{task_id}: "
                    f"{task_text} | "
                    f"due: {due_date}\n"
                )

        else:
            reply = "YOU HAVE NO PENDING TASKS."

        speak(reply)
        return True
    return False

def show_tasks(command):
    if any(alias in command for alias in SHOW_TASKS):
        tasks=task.get_tasks()
        if tasks:
            reply="HERE ARE ALL THE TASKS I HAVE STORED:\n"
            for task_id, task_text,due_date, priority, completed in tasks:
                status="COMPLETED" if completed else "PENDING"
                reply += f"{task_id}: {task_text}| priority:- {priority} |due:- {due_date} | {status}\n"
            speak(reply)
            return True
        else:
            responses=["I DON'T HAVE ANY TASKS STORED YET.", "NO TASKS FOUND IN MY MEMORY.", "MY TASK LIST IS CURRENTLY EMPTY."]
            reply=random.choice(responses)
            speak(reply)
            return True
    return False

def complete_task_command(command):
    if any(alias in command for alias in COMPLETE_TASKS):
        for alias in COMPLETE_TASKS:
            if alias in command:
                main = command.replace(alias, "", 1).strip()
                break
        try:
            if main.isdigit():
                task.complete_task(int(main))
                reply=f"TASK {main} MARKED AS COMPLETED."
            else:
                results=task.find_task_by_keyword(main)
                if results:
                    task_id=results[0][0]
                    task_name=results[0][1]
                    task.complete_task(task_id)
                    reply=f"TASK '{task_name}' (ID: {task_id}) MARKED AS COMPLETED."
                else:
                    reply=f"I COULDN'T FIND ANY TASK MATCHING '{main}'. PLEASE MAKE SURE TO USE THE CORRECT TASK ID OR KEYWORD."
            speak(reply)
            return True
        except Exception as e: 
            log_exception(e, "TASK")
            reply = "SOMETHING WENT WRONG WHILE COMPLETING THE TASK."
            speak(reply)
            return True
    return False

def delete_task_command(command):
    if any(alias in command for alias in DELETE_TASKS):
        try:
            for alias in DELETE_TASKS:
                if alias in command:
                    keyword = command.replace(alias, "", 1).strip()
                    break
            if keyword.isdigit():
                task.delete_task_by_id(int(keyword))
                reply = f"TASK {keyword} HAS BEEN DELETED."
            else:
                result = task.find_task_by_keyword(keyword)
                if result:
                    task.delete_task(keyword)
                    reply=f"TASKS MATCHING '{keyword}' HAVE BEEN DELETED."
                else:
                    reply=f"I COULDN'T FIND ANY TASK MATCHING '{keyword}'. PLEASE MAKE SURE TO USE THE CORRECT TASK ID OR KEYWORD."
            speak(reply)
            return True
        except Exception as e:
            log_exception(e, "TASK")
            reply="I'M SORRY, I COULDN'T UNDERSTAND THE TASK ID. PLEASE USE THE COMMAND LIKE 'DELETE TASK [TASK_ID]'."
            speak(reply)
            return True
    return False