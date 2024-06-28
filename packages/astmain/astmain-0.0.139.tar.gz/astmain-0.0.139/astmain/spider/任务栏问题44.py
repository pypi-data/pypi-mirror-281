import win32gui


def enum_windows_callback(hwnd, param):
    text = win32gui.GetWindowText(hwnd)
    # print("text                 :", text)
    class_name = win32gui.GetClassName(hwnd)
    # print("class_name                 :" ,  class_name   )
    if text == "web - Google Chrome":
        param[0] = hwnd
        print("111                 :" ,  111   )
        return False
    return True


taskbar_handle = [None]
win32gui.EnumWindows(enum_windows_callback, taskbar_handle)

print("111                 :", taskbar_handle)
#
# if taskbar_handle[0] is not None:
#     print(f"Task bar window handle: {taskbar_handle[0]}")
# else:
#     print("Task bar window not found")
