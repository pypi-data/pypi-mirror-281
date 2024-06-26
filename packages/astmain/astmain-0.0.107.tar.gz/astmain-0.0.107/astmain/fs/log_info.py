import datetime

from .write_add import write_add
from ..colors import colors


def log_info(level="error", info="默认内容1", path=r"C:\log_all.txt", is_print=True, color=colors.cyan):
    """ EXPLAIN : 日志追加记录函数
        EXAMPLE :  __.fs.log_info(level="## 详情日志", info=str(sys.argv), path="aaa_dist_详情日志.md", is_print=True, color=__.colors.cyan)
    """

    content = level + "|||" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "|||" + info
    if is_print: print(color, content, colors.end)
    write_add(path, content)


if __name__ == '__main__':
    log_info(info="我的错误", path=r"C:\log_all.txt")
