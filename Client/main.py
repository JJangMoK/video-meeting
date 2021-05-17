import cv2
from client import Client
from face_recog import FaceRec


def recognize(recognizer: FaceRec, frame):
    cv2.imshow("input", recognizer.recognize(frame))
    c = cv2.waitKey(1)
    if c == 27:
        # stop when press ESC
        raise Exception("DONE!!!")


if __name__ == '__main__':
    url = "http://localhost:5000"
    rec = FaceRec("./img")
    client = Client(url)
    try:
        client.request_frame(lambda frame: recognize(rec, frame))
    except Exception:
        client.send_link("https://google.com")
        cv2.destroyAllWindows()
