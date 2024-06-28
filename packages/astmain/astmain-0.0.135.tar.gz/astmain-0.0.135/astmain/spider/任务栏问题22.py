import win32api
import win32con
import win32gui


def set_taskbar_size(width, height,transparent):
    """
    设置任务栏大小

    参数:
    width (int): 任务栏宽度
    height (int): 任务栏高度
    """
    # 获取当前屏幕分辨率
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    print("222                 :" ,  screen_width ,screen_height )

    # 计算任务栏位置
    taskbar_left = (screen_width - width) // 2
    taskbar_top = screen_height - height

    print("222                 :" ,  taskbar_left,taskbar_top   )

    # 获取任务栏句柄
    taskbar_handle = win32gui.FindWindow(None,"web - Google Chrome")

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
        win32gui.SetWindowLong(taskbar_handle[0], win32con.GWL_EXSTYLE, win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(taskbar_handle[0], 0, 128, win32con.LWA_ALPHA)
    else:
        win32gui.SetWindowLong(taskbar_handle[0], win32con.GWL_EXSTYLE, 0)
        win32gui.SetLayeredWindowAttributes(taskbar_handle[0], 0, 255, win32con.LWA_ALPHA)

if __name__ == '__main__':
    # 设置任务栏大小为 800x50 像素
    # 设置任务栏大小为 800x50 像素,并设置为透明
    set_taskbar_size(800, 50, transparent=True)

    # 设置任务栏大小为 800x50 像素,并设置为不透明
    set_taskbar_size(800, 50, transparent=False)
