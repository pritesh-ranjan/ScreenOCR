import os
import random
import string

import cv2
import pytesseract
from PIL.ImageGrab import grab


def new_file_name():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + ".jpg"


def take_screenshot() -> str:
    print("This is an real!!")
    screenshot = grab()
    file_path = os.path.join("temp", "screenshot.jpg")
    screenshot.save(file_path)
    return file_path


