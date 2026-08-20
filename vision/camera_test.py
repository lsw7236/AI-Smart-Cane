from picamera2 import Picamera2
import cv2
import time


# =========================
# Camera settings
# =========================

WIDTH = 640
HEIGHT = 640


# =========================
# Camera setup
# =========================

picam2 = Picamera2()

camera_config = picam2.create_preview_configuration(
    main={
        "format": "RGB888",
        "size": (WIDTH, HEIGHT),
    }
)

picam2.configure(camera_config)

picam2.start()

time.sleep(2)

print("Camera started.")
print("Press Q to quit.")


# =========================
# Camera loop
# =========================

try:

    while True:

        frame = picam2.capture_array()

        cv2.imshow(
            "Pi Camera Test",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


except KeyboardInterrupt:

    print()
    print("Camera test interrupted.")


finally:

    picam2.stop()

    cv2.destroyAllWindows()

    print("Camera stopped.")