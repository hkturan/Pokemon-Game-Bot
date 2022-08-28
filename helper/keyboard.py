import pyautogui
import time

pyautogui.FAILSAFE = False


# Class For Keyboard Events
class Keyboard:

    @staticmethod
    def press(key):
        pyautogui.press(key)

    @staticmethod
    def hold(key, seconds):
        start = time.time()
        while time.time() - start < seconds:  # Hold Key for X Seconds
            pyautogui.keyDown(key)
        pyautogui.keyUp(key)
