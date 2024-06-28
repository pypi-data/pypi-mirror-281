import asyncio
from pyppeteer import launch

import win32api, win32gui, win32con  # pip  install     pywin32  可能会出现问题_请看README_后端py.md

once = None
# launcher.DEFAULT_ARGS.remove("--enable-automation")
opt_chrome = {
    "devtools": True,
    'userDataDir': r'C:\Users\Administrator\Desktop\userdir',
    # 'executablePath': r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe',  # 浏览器安装路径   chrome://version
    'executablePath': r'C:\Program Files\Google\Chrome\Application\chrome.exe',  # 浏览器安装路径   chrome://version
    # 'executablePath': r'C:\Users\Administrator\AppData\Local\360ChromeX\Chrome\Application\360ChromeX.exe',  # 浏览器安装路径   chrome://version
    'headless': False,
    'dumpio': True,  # 减少内存消耗   set_launch = {}
    # "ignoreDefaultArgs": ["--enable-automation"],
    'args': [
        # "--headless",
        "--mute-audio",  # 禁音
        '--no-sandbox',  # 关闭沙盒
        # '--disable-gpu',  # 禁用 GPU 硬件加速
        # '--log-level=3',  # 日志等级
        # '--disable-infobars',  # 禁用提示栏 --开启后页面加载不了
        '--window-size=1600,900',  # 屏幕大小
        '--window-position=100,100',  # 桌面位置
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    ],
}


async def wind_show(win, isshow=1):
    win32gui.ShowWindow(win["hwnd"], isshow)


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
        # print("text                 :", text)
        if (name in text):
            obj1 = dict(text=text, class_name=class_name, hwnd=hwnd)
            param.append(obj1)

        return True

    param = []
    win32gui.EnumWindows(callback, param)
    obj1 = param[0]
    print("obj1                 :", obj1)
    return obj1


async def background_task_wind_hide_taskbar_log(opt=111):
    def aaa(name):
        obj1 = wind_find_name(name)
        print("obj1                 :", obj1)
        if obj1:
            # print("obj1                 :", obj1)
            win32gui.SetWindowLong(obj1["hwnd"], win32con.GWL_STYLE, win32gui.GetWindowLong(obj1["hwnd"], win32con.GWL_STYLE) & ~win32con.WS_VISIBLE)

            return True

    for i, ele in enumerate(range(100)):
        # if win32gui.ShowWindow(win32gui.FindWindow(None, "web - Google Chrome"), 0):    return True
        # if win32gui.ShowWindow(win32gui.FindWindow(None, "about:blank - Google Chrome"), 0):    return True
        # if win32gui.ShowWindow(win32gui.FindWindow(None, "about:blank - Google Chrome"), 0):    return True
        # if win32gui.ShowWindow(win32gui.FindWindow(None, "web - Google Chrome"), 0):    return True
        # if win32gui.ShowWindow(win32gui.FindWindow(None, "小红书创作服务平台 - Google Chrome"), 0):    return True
        if aaa("Google"):    return True
        # if aaa("about:blank - Google Chrome"):    return True
        # if aaa("小红书创作服务平台 - Google Chrome"):    return True

        await asyncio.sleep(0.1)


class SPIDER:
    wind_find_name = wind_find_name

    def __init__(self, *args, **kwargs):
        pass

    # 创建浏览器
    async def create_browser(self, is_hide=True):
        # 初始化页面
        self.browser = await launch(opt_chrome)
        self.pages = await self.browser.pages()
        # self.page = self.pages[0]
        self.page = await self.browser.newPage()
        await self.page.evaluate('''() => { Object.defineProperty(navigator, 'webdriver', {get: () => undefined})}''')  # evaluateOnNewDocument
        # await self.page.evaluate('''() => { Object.defineProperty(webdriver, 'webdriver', {get: () => false})}''')  # evaluateOnNewDocument

        # 反扒库
        self.web = self.page
        await self.web.setViewport({"width": 1920, "height": 1080})
        # if is_hide: await background_task_wind_hide_taskbar_log()  # 隐藏任务栏目图标
        # await stealth(self.web)

        # 使用拦截器时会有问题
        # await self.page.setRequestInterception(True)  # 拦截
        # self.page.on('request', lambda req: asyncio.ensure_future(intercept(req)))
        return self

    # 页面跳转
    async def web_goto(self, url=""):
        await self.web.goto(url)
        await self.web.waitForSelector("html", timeout=10 * 1000)
        await self.web.evaluate(""" document.title = 'web';  """)
        return self

    # 页面跳转_设置cookies
    async def web_goto_set_cookie(self, url="", cookie={}, is_hide=True):
        await self.web_set_cookies(cookie)  # 设置cookie
        # print("000                waitForSelector :", 111)
        await self.web.goto(url, {"timeout": 9 * 1000})

        # if is_hide: await background_task_wind_hide_taskbar_log()  # 隐藏任务栏目图标
        # await self.web.waitForSelector("div", timeout=5000)
        # print("111                waitForSelector :", 111)
        await self.web.evaluate('''() => { Object.defineProperty(navigator, 'webdriver', {get: () => undefined})}''')  # evaluateOnNewDocument
        await self.web.evaluate(""" document.title = 'web';  """)
        self.win = wind_find_name("Google")
        # await wind_show(self.win, 0)
        print("self.win                 :", self.win)

        print("成功:页面跳转设置cookies--", "web_goto_set_cookie", url)
        return self
        pass

    # 等待css
    async def web_await_css(self, css="body", timeout=10 * 1000):
        # await wind_show(self.win, 1)
        try:
            await self.web.waitForSelector(css, timeout=timeout)
            await self.web.querySelector(css)
            return self
        except Exception as error:
            print("error web_await_css            :", css, str(error))

    # 点击元素
    async def web_await_click(self, css="body", timeout=10 * 1000):
        # await wind_show(self.win, 1)
        try:
            await self.web.waitForSelector(css, timeout=timeout)
            await self.web.click(css)
            # print("isok  web_await_click          :", css)
            return self
        except Exception as error:
            print("error web_await_click          :", css, str(error))

    # input上传文件
    async def web_await_input_files(self, css="body", files=[], timeout=10 * 1000):
        try:
            # await wind_show(self.win, 1)
            await self.web.waitForSelector(css, timeout=timeout)
            input_element = await self.web.querySelector(css)
            # await input_element.uploadFile(r"C:\Users\Administrator\Desktop\111.png", r"C:\Users\Administrator\Desktop\222.png")
            await input_element.uploadFile(*files)
            print("图片上传完成                 :", 111)
        except Exception as error:
            print("error web_await_input_files          :", css, str(error))

    # input输入文字
    async def web_await_input_text(self, css="body", text="hello world", timeout=10 * 1000):
        try:
            await self.web.waitForSelector(css, timeout=11111)
            await self.web.click(css)
            await self.web.type(css, text), await asyncio.sleep(1)
        except Exception as error:
            print("error web_await_input_files          :", css, str(error))

    # 设置cookies
    async def web_set_cookies(self, cookies):
        if type(cookies) == dict:
            for key in cookies:
                # print("key            :", key)
                await self.web.setCookie({'name': key, 'value': cookies[key], 'domain': '.xiaohongshu.com'})

        if type(cookies) == list:
            for ele in cookies:
                await self.web.setCookie(ele)


async def spider_pyppeteer(x=1, y=1):
    """ EXPLAIN :   启动一个浏览器窗口
        EXAMPLE :
spider = await spider_pyppeteer()  #通常开发_浏览器位置,默认
spider = await __.spider.spider_pyppeteer(**dict( x=100, y=100))    #通常开发_浏览器位置,默认
spider = await __.spider.spider_pyppeteer(**dict(x=99999, y=99999)) #通常开发_浏览器位置,移动到屏幕外
page = spider.page
    """

    global once

    # if once is None:
    #     print("111---spider---实例初始化       :")
    #     once = await SPIDER().create_browser()
    #     return once
    # else:
    #     print("222---spider---实例已经存在     :")
    #     return once

    opt_chrome["args"] = [
        # "--headless",
        "--mute-audio",  # 禁音
        '--no-sandbox',  # 关闭沙盒
        '--disable-gpu',  # 禁用 GPU 硬件加速
        # '--log-level=3',  # 日志等级
        '--disable-infobars',  # 禁用提示栏 --开启后页面加载不了
        '--start-maximized',
        '--window-size=1600,900',  # 屏幕大小
        f'--window-position={x},{y}',  # 桌面位置
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    ]
    once = await SPIDER().create_browser()
    print("成功:启动浏览器---spider                 位置", x, y)
    return once
