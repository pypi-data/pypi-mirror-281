# 基础元类
class class_base(type):
    def __str__(self):
        # 遍历所有的类属性
        my_str = ""
        for key, value in self.__dict__.items():
            # print("           key:", key, "        value:", value, )
            if (not key.startswith('__')) and not (key.endswith('__')):
                my_str += f'{key}:{value},'
        return "{" + my_str + "}"


class MyClass(metaclass=class_base):
    name = 111
    age = 111
    aaa = 111


print("2222                 :", MyClass)
