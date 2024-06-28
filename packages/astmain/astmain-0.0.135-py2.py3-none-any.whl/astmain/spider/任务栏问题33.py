import win32api
import win32con
import win32gui


def set_taskbar_size(width, height, transparent=False):
    """
    设置任务栏大小并控制其可见性和透明度

    参数:
    width (int): 任务栏宽度
    height (int): 任务栏高度
    transparent (bool): 是否设置任务栏透明
    """
    # 获取当前屏幕分辨率
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    # 计算任务栏位置
    taskbar_left = (screen_width - width) // 2
    taskbar_top = screen_height - height

    # 查找任务栏窗口
    def enum_windows_callback(hwnd, param):
        text = win32gui.GetWindowText(hwnd)
        # print("text                 :" ,  text   )
        class_name = win32gui.GetClassName(hwnd)
        if text == "web - Google Chrome":
            print("text                 :" ,  text   )
            param[0] = hwnd
            return False
        return True

    taskbar_handle = None
    win32gui.EnumWindows(enum_windows_callback, [taskbar_handle])

    # 设置任务栏大小
    win32gui.SetWindowPos(
        taskbar_handle,
        win32con.HWND_TOP,
        taskbar_left,
        taskbar_top,
        width,
        height,
        win32con.SWP_SHOWWINDOW
    )

    # 设置任务栏可见性和透明度
    if transparent:
        win32gui.SetWindowLong(taskbar_handle, win32con.GWL_EXSTYLE, win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(taskbar_handle, 0, 128, win32con.LWA_ALPHA)
    else:
        win32gui.SetWindowLong(taskbar_handle, win32con.GWL_EXSTYLE, 0)
        win32gui.SetLayeredWindowAttributes(taskbar_handle, 0, 255, win32con.LWA_ALPHA)


if __name__ == '__main__':
    # 设置任务栏大小为 800x50 像素
    # 设置任务栏大小为 800x50 像素,并设置为透明
    set_taskbar_size(800, 50, transparent=True)

    # 设置任务栏大小为 800x50 像素,并设置为不透明
    set_taskbar_size(800, 50, transparent=False)
