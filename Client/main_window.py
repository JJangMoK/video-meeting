import sys
from face_recog import FaceRec
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from client import Client
from threading import Lock
from threading import Thread
from alarm import Alarm


form_class = uic.loadUiType("prototype.ui")[0]


@Alarm(sec=5)
def recognize(recognizer, frame):
    recognizer.recognize(frame)


class TestWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__console_lock = Lock()
        self.find_pic_button.clicked.connect(self.set_picture_location)
        self.meeting_button.clicked.connect(self.start_action)
        self.rec = None
        self.encoding_thread = None

    def set_picture_location(self):
        def worker(f):
            self.rec = FaceRec(f)

        f = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.picture_edit.setText(f)
        if self.encoding_thread and self.encoding_thread.is_alive():
            self.__print_console("Wait for encoding!")
            self.encoding_thread.join()
        self.encoding_thread = Thread(target=lambda: worker(f))
        self.encoding_thread.start()

    def start_action(self):
        from confirm_dialog import ConfirmDialog
        if self.picture_edit.text():
            self.encoding_thread.join()
            try:
                print("start")
                client = Client(self.ip_edit.text() + ":5000")
                self.rec.clean_val()
                try:
                    client.request_frame(lambda frame: recognize(self.rec, frame))
                except Exception as e:
                    self.__print_console(str(e.args))

                result = self.rec.get_result()
                self.__print_console(str(result[0]))
                confirm = ConfirmDialog(self, result[1])
                accepted = confirm.exec_()
                if accepted:
                    client.send_link(self.zoom_edit.text())
                else:
                    self.__print_console("Canceled")
                # need toplevel to get confirmation from user
            except Exception as e:
                for message in e.args:
                    self.__print_console(str(message))

    def __print_console(self, text: str):
        self.__console_lock.acquire()
        self.console.append(text + "\n")
        self.__console_lock.release()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = TestWindow()
    myWindow.show()
    app.exec_()
