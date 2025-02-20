from flask import Flask, render_template_string
import subprocess
import threading
import cv2

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Object Detection</title>
</head>
<body>
    <h1>Click Below to Start Object Detection</h1>
    <a href="/start-detection" target="_blank">
        <button>Open Camera & Detect Objects</button>
    </a>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/start-detection')
def start_detection():
    thread = threading.Thread(target=detect_objects)
    thread.start()
    return "✅ Object Detection Started! Check your camera window."

def detect_objects():
    cap = cv2.VideoCapture(0)  # Open Camera
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Object Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    app.run(debug=True)
