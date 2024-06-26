import datetime

from write_add import write_add


def log_all(level="error", info="默认内容1", path=r"C:\log_all.txt"):
    content = level + "|||" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "|||" + info
    write_add(path, content)


if __name__ == '__main__':
    log_all(info="我的错误", path=r"C:\log_all.txt")
