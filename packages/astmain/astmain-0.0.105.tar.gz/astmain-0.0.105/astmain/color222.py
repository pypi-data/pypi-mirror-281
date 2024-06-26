from dataclasses import dataclass

red = '\033[31m'  # 红色  用途_日志错误
green = '\033[32m'  # 绿色
yellow = '\033[33m'  # 黄色
purple = '\033[35m'  # 紫色
cyan = '\033[36m'  # 青色   用途_日志正确
end = '\033[0m'  # 结束

"""
red='\033[31m',     # 红色  用途_日志错误
green='\033[32m',   # 绿色
yellow='\033[33m',  # 黄色
purple='\033[35m',  # 紫色
cyan='\033[36m',    # 青色   用途_日志正确
end='\033[0m',      # '结束
"""


# 这两个类,有什么区别

@dataclass
class color1:
    name = 111
    age = 222

    # 文本输出
    def __repr__(self):
        # return f"{{{', '.join(f'{k}={v}' for k, v in self.__class__.__dict__.items() if not k.startswith('__'))}}}"
        parts = []
        for k, v in self.__class__.__dict__.items():
            if not k.startswith('__'):
                parts.append(f"{k}={v}")
        return f"{{{', '.join(parts)}}}"


class color2:
    name = 111
    age = 222

    def __repr__(self):
        return f"{{{', '.join(f'{k}={v}' for k, v in self.__class__.__dict__.items() if not k.startswith('__'))}}}"

class color3:
    name = 111
    age = 222
# 我想 print(color2)      得到结果   {name=111,age=222}       重写__class__


if __name__ == '__main__':
    print("color1                 :", color1)
    print("color1()               :", color1())
    print("color2.name            :", color2.name)

    print("=======================================================")

    print("color2                 :", color2)
    print("color2()               :", color2())
    print("color2.name            :", color2.__class__)
