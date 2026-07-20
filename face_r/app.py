from flask import Flask, render_template, Response, jsonify
import cv2
import time
import os

app = Flask(__name__)

# ---------------- Load Haar Cascade ----------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise Exception("Cannot open webcam")

prev_time = 0
img_count = 0

# Live statistics
stats = {
    "faces": 0,
    "fps": 0,
    "status": "No Face",
    "distance": "--",
    "time": "--"
}

# Create capture folder
os.makedirs("static/captures", exist_ok=True)


def generate_frames():
    global prev_time

    while True:

        success, frame = camera.read()

        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Normalize empty tuple returned by detectMultiScale when no faces found
        if isinstance(faces, tuple):
            faces = []

        # ---------------- FPS ----------------

        current_time = time.time()

        fps = 1 / (current_time - prev_time) if prev_time else 0

        prev_time = current_time

        stats["fps"] = int(fps)
        stats["faces"] = len(faces)
        stats["status"] = "Face Detected" if len(faces) else "No Face"

        timestamp = time.strftime("%d-%m-%Y %H:%M:%S")
        stats["time"] = timestamp

        # Draw information

        cv2.putText(frame, f"FPS : {int(fps)}",
                    (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2)

        cv2.putText(frame,
                    f"Faces : {len(faces)}",
                    (20, 65),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 0, 0),
                    2)

        if len(faces):

            cv2.putText(frame,
                        "Status : Face Detected",
                        (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2)

        else:

            cv2.putText(frame,
                        "Status : No Face",
                        (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2)

        stats["distance"] = "--"

        for (x, y, w, h) in faces:

            cv2.rectangle(frame,
                          (x, y),
                          (x + w, y + h),
                          (0, 255, 255),
                          3)

            cx = x + w // 2
            cy = y + h // 2

            cv2.circle(frame,
                       (cx, cy),
                       4,
                       (0, 0, 255),
                       -1)

            area = w * h

            distance = round(5000 / w, 1)

            stats["distance"] = f"{distance} cm"

            cv2.putText(frame,
                        f"Area : {area}",
                        (x, y - 45),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 0),
                        2)

            cv2.putText(frame,
                        f"Dist : {distance} cm",
                        (x, y - 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        2)

            cv2.putText(frame,
                        f"({cx},{cy})",
                        (x, y + h + 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255),
                        2)

        cv2.putText(frame,
                    timestamp,
                    (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1)

        ret, buffer = cv2.imencode(".jpg", frame)

        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame +
               b'\r\n')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/stats")
def get_stats():
    return jsonify(stats)


@app.route("/capture")
def capture():

    global img_count

    success, frame = camera.read()

    if success:

        filename = f"capture_{img_count}.jpg"

        path = os.path.join("static", "captures", filename)

        cv2.imwrite(path, frame)

        img_count += 1

        return jsonify({
            "success": True,
            "image": filename
        })

    return jsonify({"success": False})


if __name__ == "__main__":
    app.run(debug=True)