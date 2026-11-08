from modules import task
from core.speech import speak
from modules import notes
from modules import task

def check_task_reminders():
    due_tasks = task.get_due_tasks()
    overdue_tasks = task.get_overdue_tasks()
    if due_tasks:
        speak(f"MASTER, YOU HAVE {len(due_tasks)} TASKS DUE TODAY.....")
    if overdue_tasks:
        speak(f"WARNING...!! TOU HAVE {len(overdue_tasks)} OVER-DUE TASKS..... ")
    
def startup_statistics():
    note_count = notes.notes_count()
    if note_count != 0:
        speak(f"MASTER, YOU HAVE {note_count} NOTES SAVED")
    total_tasks = task.task_count()
    if total_tasks != 0:
        speak(f"MASTER, YOU HAVE {total_tasks} TOTAL TASKS")
    pending_tasks = task.pending_task_count()
    if pending_tasks != 0:
        speak(f"MASTER, YOU HAVE {pending_tasks} PENDING TASKS")
    if note_count == 0 and total_tasks == 0 and pending_tasks == 0:
        speak("MASTER, YOU HAVE NO NOTES OR TASKS SAVED")