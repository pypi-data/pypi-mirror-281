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

class color1:
    name = 111
    age = 222

    def __str__(self):
        return f"{{name:{self.name},age:{self.age}}}"

    def __repr__(self):
        return f"<color1 object1111111>"


# 我想 print(color1)   输出{name:111,age:222}       但是你给我的的输出结果是       <class '__main__.color1'>           我不想用 print(color1())

if __name__ == '__main__':
    print(color1)  # 我希望得到的是   {name:111,age:222}

