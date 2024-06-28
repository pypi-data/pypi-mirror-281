import win32gui
import win32con
import win32api
import win32api
import win32con
import os
import astmain as __

obj1 = __.wind_find_name("Goog")
print("111                 :", obj1)

# win32gui.ShowWindow(obj1["hwnd"], 0)


# 隐藏主窗口
win32gui.SetWindowPos(obj1["hwnd"], win32con.HWND_HIDDEN, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

obj1 = __.wind_find_name("Goog")
print("obj1                 :", obj1)
win32gui.SetWindowLong(obj1["hwnd"], win32con.GWL_STYLE, win32gui.GetWindowLong(obj1["hwnd"], win32con.GWL_STYLE) & ~win32con.WS_VISIBLE)
