from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)

# Load a pre-trained object detection model (YOLO, Haar Cascades, etc.)
object_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")  

def generate_frames():
    camera = cv2.VideoCapture(0)  # Capture video from webcam

    while True:
        success, frame = camera.read()
        if not success:
            break

        # Convert frame to grayscale for object detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        objects = object_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(objects) > 0:
            color = (0, 0, 255)  # Red outline if object detected
        else:
            color = (0, 255, 0)  # Green outline if no object

        # Draw rectangles on detected objects
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)

        # Convert frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')  # Load the webpage

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
