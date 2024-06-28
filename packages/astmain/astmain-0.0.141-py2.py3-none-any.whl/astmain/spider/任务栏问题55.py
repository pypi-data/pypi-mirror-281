import win32gui
import win32con
import ctypes
def enum_windows_callback(hwnd, param):
    text = win32gui.GetWindowText(hwnd)
    print("text                 :" ,  text   ,hwnd )



taskbar_handle = [None]
win32gui.EnumWindows(enum_windows_callback, taskbar_handle)

print("111                 :" ,  111   )












