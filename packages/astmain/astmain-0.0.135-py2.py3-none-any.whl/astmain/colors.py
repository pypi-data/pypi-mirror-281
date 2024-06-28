from dataclasses import dataclass

from .class_base import class_base


class colors(metaclass=class_base):
    """ EXPLAIN :   系统颜色
        PARAMS  :   参数
                    red = '\033[31m'  # 红色  用途_日志错误
                    green = '\033[32m'  # 绿色
                    yellow = '\033[33m'  # 黄色
                    purple = '\033[35m'  # 紫色
                    cyan = '\033[36m'  # 青色   用途_日志正确
                    end = '\033[0m'  # 结束
        RETURN  :   null
        EXAMPLE :   print("color.red             :", color.red, 1111)
    """
    red = '\033[31m'  # 红色  用途_日志错误
    green = '\033[32m'  # 绿色
    yellow = '\033[33m'  # 黄色
    purple = '\033[35m'  # 紫色
    cyan = '\033[36m'  # 青色   用途_日志正确
    end = '\033[0m'  # 结束

    # # 文本输出
    # def __repr__(self):
    #     # return f"{{{', '.join(f'{k}={v}' for k, v in self.__class__.__dict__.items() if not k.startswith('__'))}}}"
    #     parts = []
    #     for k, v in self.__class__.__dict__.items():
    #         if not k.startswith('__'):
    #             parts.append(f"{k}={v}")
    #     return f"{{{', '.join(parts)}}}"


if __name__ == '__main__':
    print("color                 :", colors)
    print("color.red             :", colors.red, 1111)
