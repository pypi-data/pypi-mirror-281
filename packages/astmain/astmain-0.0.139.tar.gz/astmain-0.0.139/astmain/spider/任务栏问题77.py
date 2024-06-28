import win32api
import win32con
import win32gui
import astmain as __
import ctypes

obj1 = ""


def enum_windows_callback(hwnd, param):
    text = win32gui.GetWindowText(hwnd)
    class_name = win32gui.GetClassName(hwnd)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    # print(f"Window handle: {hwnd}")
    # print(f"Window title: {text}")
    # print(f"Window class: {class_name}")
    # print(f"Window position: ({left}, {top}, {right}, {bottom})")
    # print(f"Window style: {hex(style)}")
    # print()

    if ("oogle" in text):
        global obj1
        obj1 = dict(text=text, class_name=class_name, hwnd=hwnd)
        # return obj1

    return True


res = win32gui.EnumWindows(enum_windows_callback, None)
obj1 = __.to_obj_dict(obj1)
print("111                 :", obj1)

win32gui.SetWindowLong(obj1.hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(obj1.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

# alpha = 0
# ctypes.windll.user32.SetLayeredWindowAttributes(obj1.hwnd, 0, alpha, win32con.LWA_ALPHA)

# 设置任务栏可见性和透明度
# win32gui.SetWindowLong(obj1.hwnd, win32con.GWL_EXSTYLE, win32con.WS_EX_LAYERED)
# win32gui.SetLayeredWindowAttributes(obj1.hwnd, 0, 255, win32con.LWA_ALPHA)

win32gui.SetWindowLong(obj1.hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(obj1.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(obj1.hwnd, 0, 255, win32con.LWA_ALPHA)

icon_handle = win32gui.FindWindowEx(obj1.hwnd, None, "TrayNotifyWnd", None)

win32gui.SetWindowLong(icon_handle, win32con.GWL_EXSTYLE,     win32gui.GetWindowLong(icon_handle, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.ShowWindow(obj1.hwnd, win32con.SW_HIDE)

