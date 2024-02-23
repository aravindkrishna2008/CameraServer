import cv2
from flask import Flask, Response

app = Flask(__name__)
camera = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # H.264 codec
width, height = int(camera.get(3)), int(camera.get(4))
video_writer = cv2.VideoWriter('output_video.mp4', fourcc, 20.0, (width, height))

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            video_writer.write(frame)
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
