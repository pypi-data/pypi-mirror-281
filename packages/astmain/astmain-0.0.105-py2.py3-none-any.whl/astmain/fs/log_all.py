import datetime

from .write_add import write_add
from ..color import color


def log_all(level="error", info="默认内容1", path=r"C:\log_all.txt", is_print=False):
    """ EXPLAIN : 日志追加记录函数
        PARAMS  :
        level     默认就好   "error"
        info      必填参数
        path      默认参数   r"C:\log_all.txt"

        RETURN  : null
        EXAMPLE :  log_all(info="我的错误", path=r"C:\log_all.txt")
    """

    content = level + "|||" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "|||" + info
    if is_print: print(color.red, content, color.end)
    write_add(path, content)


if __name__ == '__main__':
    log_all(info="我的错误", path=r"C:\log_all.txt")
