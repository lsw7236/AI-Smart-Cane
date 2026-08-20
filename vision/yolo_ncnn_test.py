from picamera2 import Picamera2
from ultralytics import YOLO
import cv2
import time


# =========================
# Settings
# =========================

WIDTH = 640
HEIGHT = 640

CONF_THRESHOLD = 0.25

MODEL_PATH = "models/yolov8n_ncnn_model"


# =========================
# Grid position
# =========================

def get_grid_position(x_center, y_center, frame_width, frame_height):

    cell_width = frame_width / 3
    cell_height = frame_height / 3

    # Column
    if x_center < cell_width:
        column = 0
    elif x_center < cell_width * 2:
        column = 1
    else:
        column = 2

    # Row
    if y_center < cell_height:
        row = 0
    elif y_center < cell_height * 2:
        row = 1
    else:
        row = 2

    positions = [
        [
            "TOP_LEFT",
            "TOP_CENTER",
            "TOP_RIGHT"
        ],
        [
            "MIDDLE_LEFT",
            "CENTER",
            "MIDDLE_RIGHT"
        ],
        [
            "BOTTOM_LEFT",
            "BOTTOM_CENTER",
            "BOTTOM_RIGHT"
        ]
    ]

    return positions[row][column]


# =========================
# Draw 3x3 grid
# =========================

def draw_grid(frame):

    height, width = frame.shape[:2]

    x1 = width // 3
    x2 = (width // 3) * 2

    y1 = height // 3
    y2 = (height // 3) * 2

    cv2.line(
        frame,
        (x1, 0),
        (x1, height),
        (255, 255, 255),
        2
    )

    cv2.line(
        frame,
        (x2, 0),
        (x2, height),
        (255, 255, 255),
        2
    )

    cv2.line(
        frame,
        (0, y1),
        (width, y1),
        (255, 255, 255),
        2
    )

    cv2.line(
        frame,
        (0, y2),
        (width, y2),
        (255, 255, 255),
        2
    )


# =========================
# Load YOLO NCNN model
# =========================

print("Loading NCNN model...")

model = YOLO(
    MODEL_PATH,
    task="detect"
)

print("YOLO model loaded.")


# =========================
# Camera setup
# =========================

print("Starting camera...")

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
# Detection loop
# =========================

try:

    while True:

        frame = picam2.capture_array()

        results = model.predict(
            source=frame,
            imgsz=640,
            conf=CONF_THRESHOLD,
            verbose=False
        )

        result = results[0]

        # YOLO detection boxes
        annotated_frame = result.plot()

        # Draw 3x3 grid
        draw_grid(annotated_frame)

        # =========================
        # Object position
        # =========================

        for box in result.boxes:

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2

            class_id = int(box.cls[0])

            class_name = model.names[class_id]

            confidence = float(box.conf[0])

            position = get_grid_position(
                x_center,
                y_center,
                WIDTH,
                HEIGHT
            )

            print(
                f"Object: {class_name} | "
                f"Position: {position} | "
                f"Confidence: {confidence:.2f}"
            )

            # Show object center point
            cv2.circle(
                annotated_frame,
                (
                    int(x_center),
                    int(y_center)
                ),
                5,
                (255, 255, 255),
                -1
            )

        cv2.imshow(
            "YOLO NCNN 3x3 Grid",
            annotated_frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


except KeyboardInterrupt:

    print()
    print("Detection interrupted.")


finally:

    picam2.stop()

    cv2.destroyAllWindows()

    print("Camera stopped.")