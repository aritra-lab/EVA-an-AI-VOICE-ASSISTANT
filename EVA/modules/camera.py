import cv2
import os
import time
from datetime import datetime
#for face detection
cascade_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "haarcascade_frontalface_default.xml"
)

face_cascade = cv2.CascadeClassifier(cascade_path)
def take_selfie():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None
    ret, frame = cap.read()
    if not ret:
        cap.release()
        return None
    os.makedirs("photos", exist_ok=True)
    filename = datetime.now().strftime(
        "photos/selfie_%Y%m%d_%H%M%S.jpg"
    )
    cv2.imwrite(filename, frame)
    cap.release()

    return filename

def detect_faces():
    cap = None
    try:
         # Check whether the face detector loaded
        if face_cascade.empty():
            print("EVA: FACE CASCADE FAILED TO LOAD")
            return None

        # Open webcam
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("EVA: CAMERA COULD NOT OPEN")
            return None

        # Capture frame
        ret, frame = cap.read()

        if not ret:
            print("EVA: FAILED TO CAPTURE FRAME")
            return None

        # Convert to grayscale
        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        return len(faces)

    except Exception as e:
        print(f"EVA CAMERA ERROR: {e}")
        return None

    finally:
        if cap is not None:
            cap.release()
