
import win32gui
import win32con
import os


def wind_find_name(name):
    def callback(hwnd, param):
        # print("param                 :" ,  111   )
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
        # print("name                 :", name, text)
        if (name in text):
            obj1 = dict(text=text, class_name=class_name, hwnd=hwnd)
            param.append(obj1)
        return True

    param = []
    win32gui.EnumWindows(callback, param)
    return param[0]


if __name__ == '__main__':
    print("111                 :", wind_find_name("Goog"))
