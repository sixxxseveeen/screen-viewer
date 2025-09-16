from flask import Flask, Response, request
import threading

app = Flask(__name__)
latest_frame = None
lock = threading.Lock()

@app.route("/upload", methods=["POST"])
def upload():
    """Receive screenshot from client"""
    global latest_frame
    with lock:
        latest_frame = request.data
    return "OK"

@app.route("/")
def stream():
    """Stream frames to browser"""
    def generate():
        global latest_frame
        while True:
            with lock:
                if latest_frame:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' +
                           latest_frame + b'\r\n')
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
