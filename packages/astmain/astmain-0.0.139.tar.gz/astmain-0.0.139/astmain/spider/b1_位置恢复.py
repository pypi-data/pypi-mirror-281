if __name__ == '__main__':
    import astmain_py777.astmain as __  # 本地包

    spider = __.spider.SPIDER
    wind_find_name = __.spider.SPIDER.wind_find_name
    obj1 = wind_find_name("Google")
    print("obj1                 :", obj1)

    import ctypes

    pass
    # ctypes.windll.user32.SetWindowPos(obj1["hwnd"], None, -300, -900+100, 0, 0, 0x0001)
    ctypes.windll.user32.SetWindowPos(obj1["hwnd"], None, 100, 100, 0, 0, 0x0001)
    """
    hwnd 是要移动的窗口的句柄。
    hWndInsertAfter 设为 None 表示不改变窗口的插入顺序。
    x 和 y 设置为 100,表示将窗口的左上角移动到屏幕坐标 (100, 100)。
    cx 和 cy 设为 0 表示不改变窗口的大小。
    uFlags 设为 0x0001 表示只修改窗口的位置,不修改大小。
    """
