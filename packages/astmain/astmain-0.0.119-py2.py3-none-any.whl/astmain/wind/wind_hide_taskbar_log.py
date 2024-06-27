import win32api, win32gui, win32con  # pip  install     pywin32  可能会出现问题_请看README_后端py.md




def wind_hide_taskbar_log(name_title="web - Google Chrome"):
    """ EXPLAIN : windows系统平台隐藏_任务栏图标,获取软件名称请借助  spy++
        # pip  install     pywin32  可能会出现问题_请看README_后端py.md
        EXAMPLE : print("result  :", wind_hide_taskbar_log("Postman"))  ## true/false       "Postman"/"web - Google Chrome"
    """
    handle_wind = win32gui.FindWindow(None, name_title)
    # print("handle_wind            :", handle_wind)
    result = win32gui.ShowWindow(handle_wind, 0)
    # print("result             :", result)
    if result >= 1:
        return True
    else:
        return False


if __name__ == '__main__':
    pass
    print("result  :", wind_hide_taskbar_log("Postman"))  ## true/false
