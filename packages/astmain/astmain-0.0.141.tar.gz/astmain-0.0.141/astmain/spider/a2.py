if __name__ == '__main__':
    import astmain_py777.astmain as __  # 本地包

    spider = __.spider.SPIDER
    wind_find_name = __.spider.SPIDER.wind_find_name
    obj1 = wind_find_name("Google")
    print("obj1                 :", obj1)

    import ctypes

    # ctypes.windll.user32.SendMessageW(obj1["hwnd"], 0x0112, 0xF020, 0)

    window_style = ctypes.windll.user32.GetWindowLongW(obj1["hwnd"], -16)  # -16 代表 GWL_STYLE
    window_style &= ~0x10000000  # 清除 WS_VISIBLE 标志位
    ctypes.windll.user32.SetWindowLongW(obj1["hwnd"], -16, window_style)
