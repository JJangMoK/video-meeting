import sys
# from face_recog import FaceRec
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from client import Client
from threading import Lock
from alarm import Alarm


form_class = uic.loadUiType("prototype.ui")[0]


# @Alarm(sec=10)
# def recognize(recognizer, frame):
#     cv2.imshow("input", recognizer.recognize(frame))
#     c = cv2.waitKey(1)
#     if c == 27:
#         # stop when press ESC
#         raise Exception("DONE!!!")
#     pass


class TestWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__console_lock = Lock()
        self.find_pic_button.clicked.connect(self.set_picture_location)
        self.meeting_button.clicked.connect(self.start_action)

    def set_picture_location(self):
        f = str(QFileDialog.getOpenFileName(self, "Select Directory")[0])
        self.picture_edit.setText(f)

    def start_action(self):
        pass
        # if self.picture_edit.text() and self.zoom_edit.text()\
        #    and self.ip_edit.text():

            # rec = FaceRec(self.picture_edit.text())
            # client = Client(self.ip_edit.text() + ":5000")
            # try:
            #     client.request_frame(lambda frame: recognize(rec, frame))
            # except Exception:
            #     result = rec.get_result()
            #     for val in result:
            #         self.__print_console(str(val))
            #     client.send_link(self.zoom_edit.text())

    def __print_console(self, text:str):
        self.__console_lock.acquire()
        self.console.append(text)
        self.__console_lock.release()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = TestWindow()
    myWindow.show()
    app.exec_()
