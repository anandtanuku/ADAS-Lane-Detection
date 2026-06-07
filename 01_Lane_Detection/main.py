from carla_client import CarlaManager
from camera_manager import CameraManager
from lane_detector import LaneDetector
from config import HOST, PORT

import cv2
import time


# -----------------------------
# Setup
# -----------------------------

manager = CarlaManager(HOST, PORT)

vehicle = manager.spawn_vehicle()

traffic_manager = manager.client.get_trafficmanager()

vehicle.set_autopilot(
    True,
    traffic_manager.get_port()
)

camera_manager = CameraManager(
    manager.world,
    vehicle
)

camera_manager.spawn_camera()

detector = LaneDetector()

print("Waiting for camera...")

time.sleep(2)


# -----------------------------
# Main Loop
# -----------------------------

while True:

    frame = camera_manager.get_frame()

    if frame is None:
        continue

    frame = frame.copy()

    # Pipeline
    gray = detector.grayscale(frame)

    blur = detector.blur(gray)

    edges = detector.canny(blur)

    cropped = detector.region_of_interest(edges)

    lines = detector.detect_lines(cropped)

    if lines is not None:

        left_lines, right_lines = detector.classify_lines(lines)

        if len(left_lines) > 0 and len(right_lines) > 0:

            left_avg, right_avg = detector.average_lines(
                left_lines,
                right_lines
            )

            left_line = detector.make_coordinates(
                frame,
                left_avg
            )

            right_line = detector.make_coordinates(
                frame,
                right_avg
            )

            lane_image = detector.draw_lane_lines(
                frame,
                left_line,
                right_line
            )

            frame = cv2.addWeighted(
                frame,
                0.8,
                lane_image,
                1,
                0
            )

    cv2.imshow(
        "CARLA Lane Detection",
        frame
    )

    key = cv2.waitKey(1)

    if key == ord('q'):
        break


# -----------------------------
# Cleanup
# -----------------------------

cv2.destroyAllWindows()

camera_manager.destroy()

manager.destroy_all()