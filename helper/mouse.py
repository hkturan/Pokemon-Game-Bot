import win32api
import win32con


# Class For Mouse Events
class Mouse:

    @staticmethod
    def click(loc):
        win32api.SetCursorPos((loc[0], loc[1]))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, loc[0], loc[1], 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, loc[0], loc[1], 0, 0)
        win32api.SetCursorPos((0, 0))
