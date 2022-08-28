import cv2
from helper.screenshot import Screenshot


# Class For Find Object On Screen
class ObjectDetection:

    # Finds Object On Screen With Given Image
    @staticmethod
    def find_object(img_path):
        Screenshot.take_screenshot()

        img_button = cv2.imread(img_path)
        img_screenshot = Screenshot.get_screenshot_image()

        img_button_gray = cv2.cvtColor(img_button, cv2.COLOR_BGR2GRAY)
        img_screenshot_gray = cv2.cvtColor(img_screenshot, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(img_screenshot_gray, img_button_gray, cv2.TM_CCOEFF_NORMED)
        (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(result)

        threshold = 0.8
        if img_path == ImagePath.first_turn:
            threshold = 0.95
        if max_val >= threshold:
            object_loc = max_loc
        else:
            object_loc = None

        # TM_CCOEFF_NORMED uses maximum value
        return object_loc

    # Finds Object On Screen With Given Rectangle of Image
    @staticmethod
    def find_object_on_rectangle(img_path, img_path_rectangle):
        img_button = cv2.imread(img_path)
        img_rectangle = cv2.imread(img_path_rectangle)

        img_button_gray = cv2.cvtColor(img_button, cv2.COLOR_BGR2GRAY)
        img_rectangle_gray = cv2.cvtColor(img_rectangle, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(img_rectangle_gray, img_button_gray, cv2.TM_CCOEFF_NORMED)
        (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(result)

        threshold = 0.99
        if max_val >= threshold:
            object_loc = max_loc
        else:
            object_loc = None

        # TM_CCOEFF_NORMED uses maximum value
        return object_loc
