from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

#camera1 = cv2.VideoCapture(0)  # use 0 for web camera1
camera1 = cv2.VideoCapture('rtsp://admin:ads4Sashka@192.168.1.4:554/cam/realmonitor?channel=1&subtype=1')
camera2 = cv2.VideoCapture('rtsp://admin:ads4Sashka@192.168.1.4:554/cam/realmonitor?channel=2&subtype=1')


def gen_frames(camera):  # generate frame by frame from camera1
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera1 frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed1')
def video_feed1():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(camera1),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed2')
def video_feed2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(camera2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
