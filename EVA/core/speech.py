import asyncio
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import tempfile
import pygame
import time
import threading
import edge_tts
import speech_recognition as sr

from core.logger import logger, log_exception


pygame.mixer.init()


# ==========================================
# API SPEECH BRIDGE
# ==========================================

last_spoken_text = ""

speech_started_event = threading.Event()


def reset_speech_event():
    global last_spoken_text

    last_spoken_text = ""
    speech_started_event.clear()


def get_last_spoken_text():
    return last_spoken_text


# ==========================================
# TEXT TO SPEECH
# ==========================================

def voice(reply):

    async def _generate():

        communicate = edge_tts.Communicate(
            text=reply.lower(),
            voice="en-IN-NeerjaNeural"
        )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        ) as f:

            temp_file = f.name

        await communicate.save(temp_file)

        return temp_file

    temp_file = asyncio.run(
        _generate()
    )

    pygame.mixer.music.load(
        temp_file
    )

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():

        time.sleep(0.1)

    pygame.mixer.music.unload()

    os.remove(temp_file)


def take_command():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        r.adjust_for_ambient_noise(
            source,
            duration=1
        )

        print("Listening.....🎤")

        try:

            audio = r.listen(
                source,
                timeout=10,
                phrase_time_limit=15
            )

        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return ""
        print("Recognizing..." )

        try:

            text = r.recognize_google(audio).strip()
            print("You said:",text.upper())
            return text.lower().strip()

        except Exception as e:
            log_exception(e,"SPEECH" )
            return ""


def speak(reply):

    global last_spoken_text
    # ==========================================
    # TELL API WHAT EVA IS ABOUT TO SAY
    # ==========================================

    last_spoken_text = str(reply)
    speech_started_event.set()

    # ==========================================
    # NORMAL EVA SPEECH
    # ==========================================

    print("EVA: ",reply)
    logger.info(f"EVA: {reply}")
    voice(reply)