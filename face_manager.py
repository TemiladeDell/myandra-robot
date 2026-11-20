from pathlib import Path

import pickle
import face_recognition
import cv2
from picamera2 import Picamera2
from myandradb_link import load_all_faces, save_face
import time


def register_face(user_id):

    picam2 = Picamera2()

    picam2.configure(
        picam2.create_preview_configuration(
            main={"size": (640,480)}
        )
    )

    picam2.start()

    print("Look at the camera...")
    time.sleep(3)

    frame = picam2.capture_array()

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGRA2RGB
    )

    encodings = face_recognition.face_encodings(frame)

    if len(encodings) == 0:
        picam2.stop()
        picam2.close()
        print("No face found")
        return False

    Path("faces").mkdir(exist_ok=True)
    face_path = f"faces/{user_id}.pkl"

    with open(face_path, "wb") as f:
        pickle.dump(encodings[0], f)

    save_face(user_id, face_path)

    print("Face saved successfully")
    picam2.stop()
    picam2.close()

    return True

def identify_user():

    faces = load_all_faces()

    picam2 = Picamera2()

    picam2.configure(
        picam2.create_preview_configuration(
            main={"size": (640, 480)}
        )
    )

    picam2.start()

    frame = picam2.capture_array()

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGRA2RGB
    )

    encodings = face_recognition.face_encodings(frame)

    if len(encodings) == 0:
        picam2.stop()
        picam2.close()

        return None

    unknown_face = encodings[0]

    for row in faces:

        user_id = row["user_id"]
        face_file = row["face_file"]

        with open(face_file, "rb") as f:
            known_face = pickle.load(f)

        match = face_recognition.compare_faces(
            [known_face],
            unknown_face
        )[0]

        if match:
            picam2.stop()
            picam2.close()

            return user_id
    picam2.stop()
    picam2.close()

    return None
