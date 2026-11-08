import random
import datetime
from core.speech import speak
def introduction(command):
    if "hello" in command :
        responses = ["HELLO THERE! NICE TO MEET YOU.","WELCOME BACK MASTER!","GOOD TO SEE YOU AGAIN!","HELLO MASTER, EVA ONLINE."]
        reply = random.choice(responses)
        speak(reply)
        return True
    elif ("who" in command and "are you" in command) or ("what" in command and "your name" in command):
        responses=["I AM EVA, YOUR PERSONAL ASSISTANT. PROGRAMMED BY MASTER ARITRA SARKAR.", "MY NAME IS EVA, YOUR PERSONAL ASSISTANT. CREATED BY MASTER ARITRA SARKAR.", "I GO BY THE NAME EVA, YOUR PERSONAL ASSISTANT. DEVELOPED BY MASTER ARITRA SARKAR."]
        reply=random.choice(responses)
        speak(reply)
        return True
    elif "how" in command and "you" in command:
        responses=["I AM DOING GREAT, THANK YOU FOR ASKING! HOW CAN I HELP YOU TODAY?", "I AM FUNCTIONING WELL, THANK YOU FOR ASKING! WHAT CAN I DO FOR YOU TODAY?", "I AM FINE AND READY TO ASSIST YOU! HOW MAY I HELP YOU TODAY?"]
        reply=random.choice(responses)
        speak(reply)
        return True
    elif "thank you" in command or "thanks" in command or "thank" in command:
        responses=["YOU'RE WELCOME! it was my pleasure to assist you.", "NO PROBLEM! I'm here to help you anytime.", "ANYTIME! I'm glad I could assist you."]
        reply=random.choice(responses)
        speak(reply)
        return True
    elif "who" in command and "created" in command:
        responses=["I WAS CREATED BY MASTER ARITRA SARKAR. HE PROGRAMMED ME TO BE YOUR PERSONAL ASSISTANT.", "MY CREATOR IS MASTER ARITRA SARKAR. HE DEVELOPED ME TO HELP YOU WITH VARIOUS TASKS.", "I WAS DEVELOPED BY MASTER ARITRA SARKAR. HE BUILT ME TO BE YOUR PERSONAL ASSISTANT AND MAKE YOUR LIFE EASIER."]
        reply=random.choice(responses)
        speak(reply)
        return True
    return False
def help_command(command):
    if any(word in command for word in [
        "what can you do",
        "help",
        "show commands",
        "what are your features",
        "what are the features",
        "what are your capabilities",
    ]):
        reply = """I CAN:
        EXPLAIN THINGS AND ANSWER QUESTIONS
        OPEN APPLICATIONS AND WEBSITES
        CLOSE APPLICATIONS
        SEARCH GOOGLE AND YOUTUBE
        REMEMBER INFORMATION
        RECALL MEMORIES
        SHOW ALL STORED MEMORIES
        FORGET MEMORIES
        TAKE NOTES
        SHOW NOTES
        DELETE NOTES
        ADD TASKS
        SHOW TASKS
        SHOW PENDING TASKS
        COMPLETE TASKS
        DELETE TASKS
        TELL THE TIME AND DATE
        PROVIDE WEATHER REPORTS
        CONTROL VOLUME
            1. MUTE
            2. UNMUTE
            3. INCREASE VOLUME
            4. DECREASE VOLUME
            5. SET VOLUME PERCENTAGE
        SHOW SYSTEM INFORMATION
        SHOW BATTERY STATUS
        TAKE SCREENSHOTS
        TAKE SELFIES
        DETECT FACES
        SHUT DOWN THE COMPUTER
        RESTART THE COMPUTER
        LOCK THE COMPUTER
        PUT THE COMPUTER TO SLEEP

        JUST TELL ME WHAT YOU NEED, MASTER."""
        speak(reply)
        return True
    return False
def timedate(command):
    if any(word in command for word in ["time ", "what is the time", "tell me the time"]):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        responses=[f"THE CURRENT TIME IS {time}", f"IT IS CURRENTLY {time}", f"RIGHT NOW, THE TIME IS {time}"]
        reply=random.choice(responses)
        speak(reply)
        return True
    elif any(word in command for word in ["date ", "what is the date", "tell me the date"]):
        date = datetime.datetime.now().strftime("%m-%d-%Y")
        responses=[f"THE CURRENT DATE IS {date}", f"TODAY'S DATE IS {date}", f"RIGHT NOW, THE DATE IS {date}"]
        reply=random.choice(responses)
        speak(reply)
        return True
    return False
def close(command):
    if "bye" in command or "goodbye" in command or "shut down" in command or "shutdown" in command:
        responses=["GOODBYE MASTER! SEE YOU LATER!", "SEE YOU LATER MASTER! TAKE CARE!", "BYE MASTER! IT WAS NICE ASSISTING YOU. SEE YOU SOON!"]
        reply=random.choice(responses)
        speak(reply)
        hour = datetime.datetime.now().hour
        if 18<= hour or hour < 5:
            end= "GOOD NIGHT MASTER....."
        else:
            end="HAVE A GREAT DAY MASTER....."
        responses=[f"SHUTTING DOWN... ! {end}", f"POWERING OFF....{end}", f"GOODBYE EVERYONE!......  SHUTTING DOWN...{end}"]
        reply=random.choice(responses)
        speak(reply)
        exit()
    return False