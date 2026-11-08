import os
import cv2

# OWNER DETAILS
OWNER_NAME = "Master Aritra Sarkar"
OWNER_ID = "owner"

# PROJECT PATHS
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

PROFILE_DIR = os.path.join(
    BASE_DIR, "data", "face_profiles"
)

OWNER_DIR = os.path.join(
    PROFILE_DIR, OWNER_ID
)

USERS_DIR = os.path.join(
    PROFILE_DIR, "users"
)

SAMPLES_DIR = os.path.join(
    OWNER_DIR, "samples"
)

CASCADE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "haarcascade_frontalface_default.xml"
)


def initialize_face_storage():

    try:
        os.makedirs(SAMPLES_DIR, exist_ok=True)
        os.makedirs(USERS_DIR, exist_ok=True)

        print("EVA: FACE PROFILE STORAGE READY")
        print(f"EVA: {OWNER_NAME}'S PROFILE INITIALIZED")

        return True

    except OSError as e:
        print(f"EVA STORAGE ERROR: {e}")
        return False


def enroll_owner():

    cap = None

    try:
        print("\n===== EVA OWNER ENROLLMENT =====")
        print(f"Owner: {OWNER_NAME}")
        print("EVA will capture 30 face samples.")
        
        consent = input(
            "Type YES to consent to local face enrollment: "
        ).strip().upper()

        if consent != "YES":
            print("EVA: ENROLLMENT CANCELLED")
            return False

        face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

        if face_cascade.empty():
            print("EVA: FACE DETECTOR FAILED TO LOAD")
            return False

        os.makedirs(SAMPLES_DIR, exist_ok=True)

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("EVA: CAMERA COULD NOT OPEN")
            return False

        count = 0
        total_samples = 30

        print("\nEVA: CAMERA READY")
        print("Position your face inside the rectangle.")
        print("Press SPACE to capture a sample.")
        print("Press Q to cancel.")

        while count < total_samples:

            ret, frame = cap.read()

            if not ret:
                print("EVA: CAMERA FRAME FAILED")
                return False

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(80, 80)
            )

            selected_face = None

            for (x, y, w, h) in faces:

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                selected_face = gray[y:y+h, x:x+w]

            cv2.putText(
                frame,
                f"Samples: {count}/{total_samples}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.imshow(
                "EVA - Owner Enrollment",
                frame
            )

            key = cv2.waitKey(10) & 0xFF

            if key == ord('q') or key == 27:
                print("EVA: ENROLLMENT CANCELLED")
                return False

            if key == 32:

                if selected_face is None:
                    print("EVA: NO FACE DETECTED")
                    continue

                face_image = cv2.resize(
                    selected_face,
                    (200, 200)
                )

                filename = os.path.join(
                    SAMPLES_DIR,
                    f"owner_{count + 1:03d}.jpg"
                )

                saved = cv2.imwrite(
                    filename,
                    face_image
                )

                if saved:
                    count += 1
                    print(
                        f"EVA: SAMPLE {count}/{total_samples} SAVED"
                    )

        print("\nEVA: OWNER ENROLLMENT COMPLETED!")
        print(f"OWNER: {OWNER_NAME}")
        print(f"TOTAL SAMPLES: {count}")

        return True

#train LBPH recognizer with the captured samples


    except Exception as e:
        print(f"EVA ENROLLMENT ERROR: {e}")
        return False

    finally:
        if cap is not None:
            cap.release()

        cv2.destroyAllWindows()
def train_owner_model():

    try:
        if not hasattr(cv2, "face"):
            print("EVA: OPENCV FACE MODULE NOT AVAILABLE")
            return False

        recognizer = cv2.face.LBPHFaceRecognizer_create()

        faces = []
        labels = []

        if not os.path.exists(SAMPLES_DIR):
            print("EVA: OWNER SAMPLES NOT FOUND")
            return False

        for filename in os.listdir(SAMPLES_DIR):

            if not filename.lower().endswith((".jpg", ".png", ".jpeg")):
                continue

            image_path = os.path.join(SAMPLES_DIR, filename)

            image = cv2.imread(
                image_path,
                cv2.IMREAD_GRAYSCALE
            )

            if image is None:
                print(f"EVA: COULD NOT LOAD {filename}")
                continue

            image = cv2.resize(image, (200, 200))

            faces.append(image)
            labels.append(0)

        if len(faces) < 10:
            print("EVA: NOT ENOUGH VALID SAMPLES")
            return False

        import numpy as np

        recognizer.train(
            faces,
            np.array(labels, dtype="int32")
        )

        model_path = os.path.join(OWNER_DIR, "owner_model.yml")
        recognizer.save(model_path)

        print("EVA: OWNER MODEL TRAINED SUCCESSFULLY")
        print(f"EVA: VALID SAMPLES USED: {len(faces)}")

        return True

    except Exception as e:
        print(f"EVA TRAINING ERROR: {e}")
        return False

##face recognition function to identify the owner using the trained model

def recognize_owner():

    cap = None

    try:
        model_path = os.path.join(
            OWNER_DIR,
            "owner_model.yml"
        )

        if not os.path.exists(model_path):
            print("EVA: MODEL NOT FOUND")
            return "error"

        face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

        if face_cascade.empty():
            print("EVA: FACE DETECTOR FAILED")
            return "error"

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(model_path)

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("EVA: CAMERA COULD NOT OPEN")
            return "error"

        print("EVA: FACE RECOGNITION STARTED")

        owner_match_streak = 0
        required_matches = 5
        face_seen = False

        while True:

            ret, frame = cap.read()

            if not ret:
                print("EVA: CAMERA FRAME FAILED")
                return "error"

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(80, 80)
            )

            owner_found = False

            if len(faces) > 0:
                face_seen = True

            for (x, y, w, h) in faces:

                face = gray[y:y+h, x:x+w]

                face = cv2.resize(
                    face,
                    (200, 200)
                )

                label, confidence = recognizer.predict(face)

                if label == 0 and confidence < 60:

                    result = OWNER_NAME
                    color = (0, 255, 0)
                    owner_found = True

                else:

                    result = "UNKNOWN"
                    color = (0, 0, 255)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    color,
                    2
                )

                cv2.putText(
                    frame,
                    f"{result} ({confidence:.1f})",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )

            if owner_found:
                owner_match_streak += 1
            else:
                owner_match_streak = 0

            cv2.imshow(
                "EVA - Face Recognition",
                frame
            )

            if owner_match_streak >= required_matches:

                print("EVA: OWNER RECOGNIZED")

                cv2.waitKey(500)
                return "owner"

            key = cv2.waitKey(10) & 0xFF

            if key == ord("q") or key == 27:

                if face_seen:
                    return "unknown"

                return "no_face"

    except KeyboardInterrupt:
        print("\nEVA: RECOGNITION INTERRUPTED")
        return "cancelled"

    except Exception as e:
        print(f"EVA RECOGNITION ERROR: {e}")
        return "error"

    finally:
        if cap is not None:
            cap.release()

        cv2.destroyAllWindows()

if __name__ == "__main__":

    # STEP 1: INITIALIZE STORAGE
    if not initialize_face_storage():
        raise SystemExit("EVA: STORAGE INITIALIZATION FAILED")

    # STEP 2: CHECK OWNER SAMPLES
    existing_samples = [
        f for f in os.listdir(SAMPLES_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if len(existing_samples) < 10:

        print("EVA: OWNER PROFILE NOT FOUND OR INCOMPLETE")

        if not enroll_owner():
            raise SystemExit("EVA: ENROLLMENT FAILED")

    else:
        print(f"EVA: {len(existing_samples)} OWNER SAMPLES FOUND")

    # STEP 3: CHECK MODEL
    model_path = os.path.join(
        OWNER_DIR,
        "owner_model.yml"
    )

    if not os.path.exists(model_path):

        print("EVA: MODEL NOT FOUND")

        if not train_owner_model():
            raise SystemExit("EVA: MODEL TRAINING FAILED")

    else:
        print("EVA: TRAINED MODEL FOUND")

    # STEP 4: START RECOGNITION
    print("EVA: FACE SYSTEM READY")

    recognize_owner()


