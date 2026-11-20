from picamera2 import Picamera2
import face_recognition
import cv2

picam2 = Picamera2()

picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (320, 240)}
    )
)

picam2.start()

last_direction = "center"

while True:

    frame = picam2.capture_array()

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGRA2RGB
    )

    locations = face_recognition.face_locations(frame)

    direction = "center"

    if len(locations) > 0:

        top, right, bottom, left = locations[0]

        face_center_x = (left + right) // 2

        if face_center_x < 80:
            direction = "left"

        elif face_center_x < 130:
            direction = "slightly_left"

        elif face_center_x < 190:
            direction = "center"

        elif face_center_x < 240:
            direction = "slightly_right"

        else:
            direction = "right"

    if direction != last_direction:

        with open("direction.txt", "w") as f:
            f.write(direction)

        print(direction)

        last_direction = direction
