class class_base(type):

    def __str__(slef):
        # print("cls                 :" ,  slef   )
        aaa = slef
        return str(slef.name) + str(slef.age)
        pass


class MyClass(metaclass=class_base):
    name = 111
    age = 111
    aaa=1


print("111                 :", MyClass)
