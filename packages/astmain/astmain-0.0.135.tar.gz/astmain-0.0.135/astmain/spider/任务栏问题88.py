import win32gui
import win32con
import os
import astmain as __

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

print("111                 :", win32gui.GetWindowText(obj1.hwnd))

# win32gui.Shell_NotifyIcon(win32con.NIM_MODIFY, (obj1.hwnd, 0, win32con.NIF_TIP, 0, None, "My Program"))

# win32gui.Shell_NotifyIcon(win32con.NIM_MODIFY, (obj1.hwnd, 0, win32con.NIF_SHOWTIP, 0, None, "My Program", "This is my program."))


win32gui.ShowWindow(obj1.hwnd, 0)
