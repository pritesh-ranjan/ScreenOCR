import os

import cv2
import pytesseract
from PySide2.QtCore import QRect, QSize
from PySide2.QtGui import QImage, QPalette, QBrush, Qt, QCloseEvent, QPixmap
from PySide2.QtWidgets import QWidget, QRubberBand, QVBoxLayout, QTextEdit

from OCR.utilities import take_screenshot


class MainGui(QWidget):
    def __init__(self):
        super(MainGui, self).__init__()
        self.config = ('-l eng --oem 1 --psm 3')
        pytesseract.pytesseract.tesseract_cmd = r"C:\Users\test\AppData\Local\Tesseract-OCR\tesseract.exe"
        self.screenshot_path = take_screenshot()
        self.widget_image = QImage(self.screenshot_path)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(self.widget_image))
        self.setPalette(palette)
        self.edit_box = QTextEdit()
        self.v_box = QVBoxLayout()
        self.edit_box.hide()
        self.v_box.addWidget(self.edit_box)
        self.setLayout(self.v_box)

    def set_window_properties(self):
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Tool)

    def mousePressEvent(self, eventQMouseEvent):
        self.originQPoint = eventQMouseEvent.pos()
        self.currentQRubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.currentQRubberBand.setGeometry(QRect(self.originQPoint, QSize()))
        self.edit_box.hide()
        self.currentQRubberBand.show()

    def mouseMoveEvent(self, eventQMouseEvent):
        self.currentQRubberBand.setGeometry(QRect(self.originQPoint, eventQMouseEvent.pos()).normalized())

    def mouseReleaseEvent(self, eventQMouseEvent):
        self.currentQRubberBand.hide()
        selected_area = self.currentQRubberBand.geometry()
        self.currentQRubberBand.deleteLater()
        crop_save_path = self.crop_selected_area(selected_area)
        self.set_edit_box_ui(crop_save_path, selected_area)

    def crop_selected_area(self, selected_area):
        crop_image = QPixmap(self.widget_image).copy(selected_area)
        save_name = "selected_shot.jpg"
        crop_save_path = os.path.join("temp", save_name)
        crop_image.save(crop_save_path)
        return crop_save_path

    def set_edit_box_ui(self, crop_save_path: str, selected_area: QRect):
        s2 = os.path.join(os.getcwd(), crop_save_path).replace("\\", "/")
        self.edit_box. setStyleSheet(f'background-image: url({s2});border: 0px;font: 11pt "Calibri"')
        self.edit_box.setReadOnly(True)
        self.edit_box.show()
        self.edit_box.setGeometry(selected_area)
        self.set_text(crop_save_path)

    def set_text(self, file):
        text = self.get_text(file)
        self.edit_box.setText(text)
        self.edit_box.setFocus()
        self.edit_box.selectAll()

    def closeEvent(self, event: QCloseEvent):
        os.remove(self.screenshot_path)

    def get_text(self, file):
        im = cv2.imread(file, 0)
        return pytesseract.image_to_string(im, config=self.config)


