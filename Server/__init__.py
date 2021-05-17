from flask import Response, Flask, g, request
import cv2
import webbrowser


def create_cap():
    source = 0
    if "cap" not in g:
        g.cap = cv2.VideoCapture(source)

    return g.cap


def create_app(test_config=None):
    app = Flask(__name__)

    @app.route("/stream")
    def generate_frame():
        cap = create_cap()

        def gen():
            if not cap.isOpened():
                return "Turn On that damned Webcam!"

            while True:
                ret, frame = cap.read()
                yield frame.tobytes()
        return Response(gen())

    @app.route("/info")
    def get_info():
        cap = create_cap()
        ret, frame = cap.read()
        print(frame.shape)
        return Response(str({
            "shape": frame.shape,
            "size": len(frame.tobytes())
        }))

    @app.route("/open_link", methods=["POST"])
    def open_link():
        webbrowser.open(request.form["url"])
        return "link opened {:}".format(request.form["url"])

    return app
