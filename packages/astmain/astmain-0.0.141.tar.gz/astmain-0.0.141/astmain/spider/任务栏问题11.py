import win32api
import win32con
import win32gui

task_bar_handle = win32gui.FindWindow(None, "web - Google Chrome")

# 设置任务栏窗口的风格为隐藏
style = win32gui.GetWindowLong(task_bar_handle, win32con.GWL_STYLE)
print("style                 :", style)
style &= ~win32con.WS_VISIBLE
print("style                 :", style)
aaa1=win32gui.SetWindowLong(task_bar_handle, win32con.GWL_STYLE, style)
print("aaa1                 :", aaa1)
# 更新任务栏窗口
aaa2 = win32gui.ShowWindow(task_bar_handle, win32con.SW_HIDE)

print("aaa2                 :", aaa2)
