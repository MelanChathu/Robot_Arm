import cv2
import serial
import time
from ultralytics import YOLO

# Set up the serial connection to Arduino
ser = serial.Serial('COM8', 9600, timeout=1)  # Replace 'COM8' with your port
time.sleep(2)  # Wait for the connection to establish

# Load the YOLO model
model = YOLO('best.pt')

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

def send_move_command(x, y, z):
    """Send MOVE command with x, y, and z coordinates to Arduino."""
    command = f"MOVE {x:.2f} {y:.2f} {z:.2f}\n"
    ser.write(command.encode())
    print(f"Sent: {command.strip()}")

    response = ser.readline().decode().strip()
    if response:
        print(f"Arduino Response: {response}")

def open_camera():
    """Open the camera and perform object detection."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Perform object detection using YOLO
        results = model(frame)

        for result in results:
            for detection in result.boxes.data:
                confidence = float(detection[4])

                if confidence > 0.7:
                    x_min, y_min, x_max, y_max = map(int, detection[:4])
                    center_x = (x_min + x_max) // 2
                    center_y = (y_min + y_max) // 2

                    # Simulate z-coordinate (optional: add depth sensor data)
                    z = 10.0  # Example z-coordinate

                    print(f"Detected object at center: ({center_x}, {center_y}, {z})")

                    # Send the coordinates to Arduino
                    send_move_command(center_x, center_y, z)
                    break

        cv2.imshow('Detection Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

try:
    open_camera()
except KeyboardInterrupt:
    print("Program interrupted.")
finally:
    ser.close()
