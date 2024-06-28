import asyncio
from pyppeteer import launch

import win32api, win32gui, win32con  # pip  install     pywin32  可能会出现问题_请看README_后端py.md

__ = None

import astmain_py777.astmain as __  # 本地包

if __name__ == '__main__':
    pass


    async def aaa():
        pass
        opt = dict(
            title="小许",
            text="1111",
            files=[r"C:\Users\Administrator\Desktop\111.png", r"C:\Users\Administrator\Desktop\222.png"],
            cookies_str="""[
    {
        "name": "acw_tc",
        "value": "154f43315f9dd63775e16408461fa4c82934e714470824df342755d810f2dd0d",
        "domain": "www.xiaohongshu.com",
        "hostOnly": true,
        "path": "/",
        "secure": false,
        "httpOnly": true,
        "session": false,
        "expirationDate": 1719508892.862441,
        "sameSite": "unspecified"
    },
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
        "expirationDate": 1719766294,
        "sameSite": "unspecified"
    },
    {
        "name": "sec_poison_id",
        "value": "f4fa6476-d599-4d89-8c13-d2096c48a76b",
        "domain": ".xiaohongshu.com",
        "hostOnly": false,
        "path": "/",
        "secure": false,
        "httpOnly": false,
        "session": false,
        "expirationDate": 1719507699,
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
        "expirationDate": 1754067249.237062,
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
        "expirationDate": 1751043246,
        "sameSite": "unspecified"
    },
    {
        "name": "web_session",
        "value": "0400698e30a4ad561bd2b1d048344bd1202e4a",
        "domain": ".xiaohongshu.com",
        "hostOnly": false,
        "path": "/",
        "secure": true,
        "httpOnly": true,
        "session": false,
        "expirationDate": 1751043156.445488,
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
    }
]""",
        )

        opt = __.to_obj_dict(opt)

        # spider = await spider_pyppeteer()
        # spider = await __.spider.spider_pyppeteer(**dict( x=300, y=1))
        # spider = await __.spider.spider_pyppeteer(**dict(x=0, y=-900 + 2))
        spider = await __.spider.spider_pyppeteer(**dict(x=-1800, y=-900 + 999))
        page = spider.page
        # cookies登陆
        # await spider.web_goto_set_cookie("https://creator.xiaohongshu.com/publish/publish", __.to.JSON(opt.cookies_str))
        # await spider.web_goto_set_cookie("https://creator.xiaohongshu.com", __.to.JSON(opt.cookies_str))
        await spider.web_goto_set_cookie("https://creator.xiaohongshu.com/publish/publish", __.to.JSON(opt.cookies_str))
        await __.tool_await(1)

        # 点击发布图文
        await spider.web_await_click(css=".tab:nth-child(2)")
        await spider.web_await_input_files(css=".upload-input", files=opt.files)

        # 输入标题
        await spider.web_await_input_text(css=".titleInput .el-input__wrapper .el-input__inner", text=opt.title)

        # 输入描述
        await spider.web_await_input_text(css=".topic-container", text=opt.text)

        # 添加地点
        pass

        # 权限设置_私密
        await spider.web_await_click(css=".el-radio__label")

        # 发布_按钮点击
        await spider.web_await_click(css=".publishBtn")

        # 判断_是否_成功
        await spider.web_await_css(css=".btn-content")
        html = await page.content()

        await __.tool_await(0.1)
        await __.tool_await(9999)
        await spider.browser.close()
        print("成功:发布内容---关闭浏览器---xiaohongshu")


    asyncio.get_event_loop().run_until_complete(aaa())
