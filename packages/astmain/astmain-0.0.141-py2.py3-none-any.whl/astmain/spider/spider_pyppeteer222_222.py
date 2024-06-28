import asyncio
import datetime

from pyppeteer import launch

import win32api, win32gui, win32con  # pip  install     pywin32  可能会出现问题_请看README_后端py.md

__ = None

import astmain_py777.astmain as __  # 本地包


def bbb():
    # spider = __.spider.SPIDER
    wind_find_name = __.spider.SPIDER.wind_find_name
    obj1 = wind_find_name("Google")
    print("obj1                 :", obj1)

    import ctypes

    # ctypes.windll.user32.SendMessageW(obj1["hwnd"], 0x0112, 0xF020, 0)

    window_style = ctypes.windll.user32.GetWindowLongW(obj1["hwnd"], -16)  # -16 代表 GWL_STYLE
    window_style &= ~0x10000000  # 清除 WS_VISIBLE 标志位
    ctypes.windll.user32.SetWindowLongW(obj1["hwnd"], -16, window_style)

    ctypes.windll.user32.SetWindowPos(obj1["hwnd"], None, 100, -880, 0, 0, 0x0001)
    """
    好博客 https://blog.csdn.net/weixin_30314631/article/details/97574375
    hwnd 是要移动的窗口的句柄。
    hWndInsertAfter 设为 None 表示不改变窗口的插入顺序。
    x 和 y 设置为 100,表示将窗口的左上角移动到屏幕坐标 (100, 100)。
    cx 和 cy 设为 0 表示不改变窗口的大小。
    uFlags 设为 0x0001 表示只修改窗口的位置,不修改大小。
    """


if __name__ == '__main__':
    pass


    async def aaa():
        pass
        opt = dict(
            title="title222小许" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            text="text2222",
            files=[r"C:\Users\Administrator\Desktop\111.png", r"C:\Users\Administrator\Desktop\222.png"],
            cookies_str="""[
    {
        "name": "abRequestId",
        "value": "a376129c-d49b-5bbc-a8f4-170cc4bfe129",
        "domain": ".xiaohongshu.com",
        "hostOnly": false,
        "path": "/",
        "secure": false,
        "httpOnly": false,
        "session": false,
        "expirationDate": 1751043092.862638,
        "sameSite": "unspecified"
    },
    {
        "name": "a1",
        "value": "1905a9c0831wg416b0zniax0jqghkn390f4cocqpf50000243666",
        "domain": ".xiaohongshu.com",
        "hostOnly": false,
        "path": "/",
        "secure": false,
        "httpOnly": false,
        "session": false,
        "expirationDate": 1751043093,
        "sameSite": "unspecified"
    },
    {
        "name": "webId",
        "value": "6e110199fae6482d9b9f8ba843732d83",
        "domain": ".xiaohongshu.com",
        "hostOnly": false,
        "path": "/",
        "secure": false,
        "httpOnly": false,
        "session": false,
        "expirationDate": 1751043093,
        "sameSite": "unspecified"
    },
    {
        "name": "websectiga",
        "value": "984412fef754c018e472127b8effd174be8a5d51061c991aadd200c69a2801d6",
        "domain": ".xiaohongshu.com",
        "hostOnly": false,
        "path": "/",
        "secure": false,
        "httpOnly": false,
        "session": false,
        "expirationDate": 1719771432,
        "sameSite": "unspecified"
    },
    {
        "name": "gid",
        "value": "yj820jSJyW8Dyj820jS8YiSAqyEk4yKD8uI34Ui0C8VAkS28xTIqjl888J4qKKK8yKqfJWW8",
        "domain": ".xiaohongshu.com",
        "hostOnly": false,
        "path": "/",
        "secure": false,
        "httpOnly": false,
        "session": false,
        "expirationDate": 1754072239.355501,
        "sameSite": "unspecified"
    },
    {
        "name": "xsecappid",
        "value": "xhs-pc-web",
        "domain": ".xiaohongshu.com",
        "hostOnly": false,
        "path": "/",
        "secure": false,
        "httpOnly": false,
        "session": false,
        "expirationDate": 1751048236,
        "sameSite": "unspecified"
    },
    {
        "name": "acw_tc",
        "value": "34c2c09702979dbc55eba1576545febc0fddd0a0fc0f0b928dd2a4fd5803e004",
        "domain": "www.xiaohongshu.com",
        "hostOnly": true,
        "path": "/",
        "secure": false,
        "httpOnly": true,
        "session": false,
        "expirationDate": 1719514031.519517,
        "sameSite": "unspecified"
    },
    {
        "name": "webBuild",
        "value": "4.23.1",
        "domain": ".xiaohongshu.com",
        "hostOnly": false,
        "path": "/",
        "secure": false,
        "httpOnly": false,
        "session": true,
        "sameSite": "unspecified"
    },
    {
        "name": "sec_poison_id",
        "value": "3116f21d-6593-4b6a-a780-3ff76159bc1f",
        "domain": ".xiaohongshu.com",
        "hostOnly": false,
        "path": "/",
        "secure": false,
        "httpOnly": false,
        "session": false,
        "expirationDate": 1719512837,
        "sameSite": "unspecified"
    },
    {
        "name": "web_session",
        "value": "0400698e30a4ad561bd2d4e448344b3da94447",
        "domain": ".xiaohongshu.com",
        "hostOnly": false,
        "path": "/",
        "secure": true,
        "httpOnly": true,
        "session": false,
        "expirationDate": 1751048248.987734,
        "sameSite": "unspecified"
    },
    {
        "name": "unread",
        "value": "{%22ub%22:%2266798188000000001e013457%22%2C%22ue%22:%22667d734b000000001c02806a%22%2C%22uc%22:25}",
        "domain": ".xiaohongshu.com",
        "hostOnly": false,
        "path": "/",
        "secure": false,
        "httpOnly": false,
        "session": true,
        "sameSite": "unspecified"
    }
]""",
        )

        num = 0
        opt = __.to_obj_dict(opt)

        # spider = await spider_pyppeteer()
        # spider = await __.spider.spider_pyppeteer(**dict( x=300, y=1))
        # spider = await __.spider.spider_pyppeteer(**dict(x=0, y=-900 + 2))
        spider = await __.spider.spider_pyppeteer(**dict(x=-10, y=-900 + 999))
        page = spider.page
        # cookies登陆
        # await spider.web_goto_set_cookie("https://creator.xiaohongshu.com/publish/publish", __.to.JSON(opt.cookies_str))
        await spider.web_goto_set_cookie("https://creator.xiaohongshu.com", __.to.JSON(opt.cookies_str))
        await asyncio.sleep(0.1)
        await spider.web_goto("https://creator.xiaohongshu.com/publish/publish")
        for ele in range(10):
            await asyncio.sleep(1)
            print("循环ele                 :", ele + 1)
        num += 1
        bbb()
        print(num, "cookies登陆url                 :", 111)
        await __.tool_await(1)

        # 点击发布图文_上传图片
        await spider.web_await_click(css=".tab:nth-child(2)")
        await spider.web_await_input_files(css=".upload-input", files=opt.files)
        num += 1
        print(num, "点击发布图文_上传图片                 :")

        # 输入标题
        await spider.web_await_input_text(css=".titleInput .el-input__wrapper .el-input__inner", text=opt.title)
        num += 1
        print(num, "输入标题                 :")

        # 输入描述
        await spider.web_await_input_text(css=".topic-container", text=opt.text)
        num += 1
        print(num, "输入描述                 :")

        # 添加地点
        pass

        # 权限设置_私密
        await spider.web_await_click(css=".el-radio__label")
        num += 1
        print(num, "权限设置_私密                 :")

        # 发布_按钮点击
        await spider.web_await_click(css=".publishBtn")
        num += 1
        print(num, "发布_按钮点击                 :")

        # 判断_是否_成功
        await spider.web_await_css(css=".btn-content")
        html = await page.content()
        num += 1
        print(num, "成功:发布内容---xiaohongshu")

        await __.tool_await(0.1)
        await __.tool_await(9999)
        await spider.browser.close()
        print("成功:关闭浏览器---xiaohongshu")


    asyncio.get_event_loop().run_until_complete(aaa())
