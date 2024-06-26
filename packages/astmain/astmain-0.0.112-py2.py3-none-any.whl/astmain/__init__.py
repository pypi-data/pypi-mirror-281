import importlib
import os
import requests

from .fs import *  # 文件操作
from .to import *  # 数据转化
from .desc import *  # 装饰器
from .spider import *  # 爬虫
from .tool import *  # 常用工具



from .colors import *  # 颜色
from .eval_func_str import *  # eval_func_str

# import astmain_py777.astmain as __
# from astmain_py777.astmain import print
# __.print_hook = True
# print = __.print

print_hook = False
print_old = print


def print(*args, **kwargs):
    if print_hook == True:
        print_old("\033[36m", *args, **kwargs)
    if print_hook == False:
        print_old(*args, **kwargs)


# desc = import_module(".desc")

# desc = importlib.import_module(".desc", package="astmain_py777.astmain")


def test():
    print("test            :", 15160)
