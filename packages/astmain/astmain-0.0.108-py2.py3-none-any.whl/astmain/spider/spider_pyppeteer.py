import asyncio
from pyppeteer import launch

once = None
# launcher.DEFAULT_ARGS.remove("--enable-automation")
opt_chrome = {
    "devtools": True,
    'userDataDir': r'C:\Users\Administrator\Desktop\userdir',
    'executablePath': r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe',  # 浏览器安装路径   chrome://version
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
        '--window-size=1600,950',  # 屏幕大小
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        # "--enable-automation",  # 自动化模式:
        # "--disable-automation",  # 禁用自动化模式:
        # '--enable-features=OverrideAutomationWarning'  # 隐藏自动化提示:

    ],
}


class SPIDER:
    def __init__(self, *args, **kwargs):
        pass

    # 创建浏览器
    async def create_browser(self):
        # 初始化页面
        self.browser = await launch(opt_chrome)
        self.pages = await self.browser.pages()
        self.page = self.pages[0]
        await self.page.evaluate('''() => { Object.defineProperty(navigator, 'webdriver', {get: () => undefined})}''')  # evaluateOnNewDocument
        # await self.page.evaluate('''() => { Object.defineProperty(webdriver, 'webdriver', {get: () => false})}''')  # evaluateOnNewDocument

        # 反扒库
        self.web = self.pages[0]
        # await stealth(self.web)

        # 使用拦截器时会有问题
        # await self.page.setRequestInterception(True)  # 拦截
        # self.page.on('request', lambda req: asyncio.ensure_future(intercept(req)))
        return self

    # 页面跳转_设置cookies
    async def web_goto_set_cookie(self, url="", cookie={}):
        await self.web_set_cookies(cookie)  # 设置cookie
        await self.web.setViewport({"width": 1920, "height": 1080})
        print("000                waitForSelector :", 111)
        await self.web.goto(url, {"timeout": 9 * 1000})
        # await self.web.waitForSelector("div", timeout=5000)
        print("111                waitForSelector :", 111)
        await self.web.evaluate(""" document.title = 'web';  """)
        return self
        pass

    # 页面跳转
    async def web_goto(self, url=""):
        await self.web.goto(url)
        await self.web.waitForSelector("html", timeout=10 * 1000)
        await self.web.evaluate(""" document.title = 'web';  """)
        return self

    # 等待css
    async def web_await_css(self, css="body", timeout=10 * 1000):
        try:
            await self.web.waitForSelector(css, timeout=timeout)
            await self.web.querySelector(css)
            return self
        except Exception as error:
            print("error web_await_css            :", css, str(error))

    # 点击元素
    async def web_await_click(self, css="body", timeout=10 * 1000):
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
            await self.web.waitForSelector(css, timeout=timeout)
            input_element = await self.web.querySelector(css)
            # await input_element.uploadFile(r"C:\Users\Administrator\Desktop\111.png", r"C:\Users\Administrator\Desktop\222.png")
            await input_element.uploadFile(*files)
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


async def spider_pyppeteer():
    global once

    if once is None:
        print("111---spider---实例初始化       :")
        once = await SPIDER().create_browser()
        return once
    else:
        print("222---spider---实例已经存在     :")
        return once
