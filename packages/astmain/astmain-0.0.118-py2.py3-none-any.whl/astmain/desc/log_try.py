import asyncio
import datetime
import inspect
import functools
import traceback

from ..fs.write_add import write_add
from ..fs.log_info import log_info
from ..colors import colors


def log_try(level="错误日志", path=r"aaa_dist_错误日志.md", is_print=True, color=colors.red):
    """ EXPLAIN : 日志追加记录函数
        PARAMS  :
        level     默认就好   "error"
        info      必填参数
        path      默认参数   r"C:\log_all.txt"
        color     默认参数   __.colors.red

        RETURN  : null
        EXAMPLE :  @__.desc.log_try(path="aaa_dist_错误日志.md", level="## 错误日志", is_print=True, color=__.colors.red)
    """

    def decorator(func):
        is_await = inspect.iscoroutinefunction(func)
        # print("is_await                 :", is_await)

        # 普通函数========================
        if is_await == False:
            # print("普通函数                 :", func.__name__)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    # content = "error|||" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "|||" + str(error)
                    # write_add(r"C:\Users\Administrator\Desktop\log.txt", content)
                    log_info(level=level, info=str(traceback.format_exc()), path=path, is_print=is_print, color=color)
                    # print("\033[31m", "失败            :", content, "\033[0m")

            return wrapper

        # 异步函数========================
        if is_await == True:
            # print("异步函数                 :", func.__name__)
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as error:
                    # content = "error|||" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "|||" + str(traceback.format_exc())
                    # write_add(r"C:\Users\Administrator\Desktop\log.txt", content)
                    # print("\033[31m", "失败            :", content, "\033[0m")
                    log_info(level=level, info=str(traceback.format_exc()), path=path, is_print=is_print, color=color)

            return wrapper

    return decorator


if __name__ == '__main__':
    # @log("debug")
    # def do_something():
    #     print("Doing something...")

    # do_something()

    @try_error("debug")
    async def do_something222():
        await asyncio.sleep(1)
        1 / 0
        print("111111111                 :", 111)


    asyncio.run(do_something222())
