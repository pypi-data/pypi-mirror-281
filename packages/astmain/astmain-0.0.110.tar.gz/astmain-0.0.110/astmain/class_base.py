# 基础元类      https://gvanrossum.com/reference/datamodel.html#metaclasses
class class_base(type):
    def __str__(self):
        # 遍历所有的类属性
        my_str = ""
        for key, value in self.__dict__.items():
            if (not key.startswith('__')) and not (key.endswith('__')):
                my_str += f'{key}:{value},'
                # print("           key:", key, "        value:", value, )
        return "{" + my_str + "}"
