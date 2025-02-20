from flask import Flask, render_template_string, Response
import cv2
import os

app = Flask(__name__)

# CHANGE THIS: Set your mobile IP Webcam URL
MOBILE_CAM_URL = "http://192.0.0.4:8080"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile Camera Stream</title>
</head>
<body>
    <h1>Click Below to Start Object Detection</h1>
    <a href="/video_feed" target="_blank">
        <button>Open Mobile Camera</button>
    </a>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

def generate_frames():
    cap = cv2.VideoCapture(MOBILE_CAM_URL)  # Use Mobile Camera Stream

    if not cap.isOpened():
        print("Error: Could not open mobile camera stream.")
        return

    while True:
        success, frame = cap.read()
        if not success:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
