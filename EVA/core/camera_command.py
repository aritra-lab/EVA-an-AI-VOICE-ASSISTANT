from modules import camera, face_recognition
from core.speech import speak
import time


def take_selfie_command(command):

    if "take selfie" in command:

        speak("ON THE COUNT OF 3 PLEASE SMILE.....")
        time.sleep(0.5)

        speak("3....")
        speak("2....")
        speak("1....")
        speak("SMILE...!!")

        filename = camera.take_selfie()

        if filename:
            print(f"SELFIE SAVED AS {filename}")
            speak("THE SELFIE IS TOO GOOD MASTER AND I HAVE SAVED IT")
        else:
            speak("I COULD NOT TAKE THE SELFIE")

        return True

    return False


def detect_faces_command(command):

    if "detect face" in command or "count faces" in command:

        count = camera.detect_faces()

        if count is None:
            speak("I AM HAVING TROUBLE ACCESSING THE CAMERA.")

        elif count == 0:
            speak("I CANNOT SEE ANY FACES.")

        elif count == 1:
            speak("I CAN SEE 1 FACE.")

        else:
            speak(f"I CAN SEE {count} FACES.")

        return True

    return False


def recognize_owner_command(command):

    if (
        "recognize me" in command
        or "recognise me" in command
        or "who is in the camera" in command
        or "who is in front of the camera" in command
        or "recognise face" in command
        or "recognize face" in command
    ):

        speak("STARTING OWNER RECOGNITION.")

        result = face_recognition.recognize_owner()

        if result == "owner":

            speak(
                "WELCOME BACK, MASTER ARITRA SARKAR. "
                "I AM HAPPY TO SEE YOU."
            )

        elif result == "unknown":

            speak(
                "I COULD NOT CONFIRM THE OWNER PROFILE."
            )

        elif result == "no_face":

            speak("I COULD NOT DETECT ANY FACE.")

        elif result == "cancelled":

            speak("FACE RECOGNITION CANCELLED.")

        else:

            speak(
                "FACE RECOGNITION ENCOUNTERED AN ERROR."
            )

        return True

    return False