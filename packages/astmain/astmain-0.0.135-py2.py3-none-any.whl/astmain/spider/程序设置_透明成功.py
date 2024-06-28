# 要使用win32api来控制Windows任务栏的透明度，你需要调用Windows的API函数。以下是一个简单的Python脚本，用于设置任务栏的透明度：

import win32gui
import win32con
import ctypes


# 定义一个结构体用来表示透明度信息
class TRANSPARENCY_INFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', ctypes.c_ulong),
        ('dwFlags', ctypes.c_ulong),
        ('rgba', ctypes.c_ulong),
        ('hRgnBlur', ctypes.c_void_p)
    ]


# 设置透明度的常量
LWA_ALPHA = 0x2

# 要设置的透明度值，范围从0到255
alpha = 0

# 创建透明度信息
transparency_info = TRANSPARENCY_INFO()
transparency_info.cbSize = ctypes.sizeof(TRANSPARENCY_INFO)
transparency_info.dwFlags = LWA_ALPHA
transparency_info.rgba = (alpha << 24)

# 获取任务栏窗口句柄
taskbar_handle = win32gui.FindWindow(None, "web - Google Chrome")
print("taskbar_handle                 :" ,  taskbar_handle   )

# 设置透明度
win32gui.SetWindowLong(taskbar_handle, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(taskbar_handle, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

ctypes.windll.user32.SetLayeredWindowAttributes(taskbar_handle, 0, alpha, win32con.LWA_ALPHA)

print("111                 :" ,  111   )

# ctypes.windll.user32.SetLayeredWindowAttributes(taskbar_handle, 0, alpha / 255.0, win32con.LWA_ALPHA)
#
# 请注意，这段代码需要在Windows环境下运行，并且需要安装pywin32库。代码中的透明度值alpha是一个0到255之间的整数，代表任务栏的透明度，其中255表示完全不透明，而0表示完全透明。
#
# 运行这段代码后，你会发现任务栏的透明度被设置为你指定的值。请谨慎使用此功能，因为过度的透明可能会影响用户界面的可用性。