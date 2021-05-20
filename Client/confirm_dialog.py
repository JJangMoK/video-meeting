from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
from PyQt5 import uic

form_class = uic.loadUiType("confirm.ui")[0]

def convert_cv2img_to_PyQtPixMap(img):
    return QPixmap(QImage(img, img.shape[1],
                          img.shape[0], img.shape[1]*3, QImage.Format_RGB888))


class ConfirmDialog(QDialog, form_class):
    def __init__(self, parent, img_to_show):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Confirm Meeting")
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        pixmap = convert_cv2img_to_PyQtPixMap(img_to_show)
        self.picture_label.setPixmap(pixmap)
        self.picture_label.resize(pixmap.width(), pixmap.height())
