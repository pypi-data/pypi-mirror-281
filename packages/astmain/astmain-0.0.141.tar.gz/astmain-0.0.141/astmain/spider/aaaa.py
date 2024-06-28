import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
import win32api  # pip install pywin32
import win32con  # pip install win32con
import win32gui  # pip install win32gui

opt_chrome = {
    "devtools": True,
    'userDataDir': r'C:\Users\Administrator\Desktop\userdir',
    'executablePath': r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe',
    'headless': False,
    'dumpio': True,  # 减少内存消耗   set_launch = {}
    'args': [
        '--no-sandbox',  # 关闭沙盒
        '--disable-gpu',
        '--window-size=1400,950',  # 屏幕大小
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        '--window-position=100,100'
    ],
}


async def main111():
    browser = await launch(opt_chrome)
    page = await browser.newPage()
    await stealth(page)  # 反扒库
    # await page.setViewport({"width": 1920, "height": 1080, "x": 100, "y": 100})
    await page.goto('https://creator.xiaohongshu.com/creator/home')

    for i in range(10):
        await asyncio.sleep(1)
        print("i            :", i)

    # # 隐藏 Windows 任务栏
    # hwnd = win32gui.FindWindow(None, 'Google Chrome')
    # win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

    zzz = 1
    await asyncio.sleep(6666666666666666666)
    await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main111())
