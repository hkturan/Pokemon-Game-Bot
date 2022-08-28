import cv2
from PIL import ImageGrab
from helper.imagepath import ImagePath


# Class For Screenshot Events
class Screenshot:

    @staticmethod
    def take_screenshot():
        screenshot = ImageGrab.grab()
        screenshot.save(ImagePath.screenshot_name, "PNG")

    @staticmethod
    def get_screenshot_image():
        return cv2.imread(ImagePath.screenshot_name)

    @staticmethod
    def get_pokemon_name_image():
        return cv2.imread(ImagePath.pokemon_name)
