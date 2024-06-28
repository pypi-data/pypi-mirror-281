class color2():
    name = 111
    age = 222

    def __getinitargs__(self):
        pass

    def __getstate__(self):
        pass

    def __class_getitem__(cls, item):
        pass

    def __set_name__(self, owner, name):
        pass

    def __module__(self):
        pass

    def __new__(cls, *args, **kwargs):
        pass

    def __file__(self):
        pass

    def __annotations__(self):
        pass

    def __prepare__(cls, name, bases, **kwds):
        return {'__annotations__': {}}

    def __init__(self, instance_attr):
        super().__setattr__(111, 222)
        print("111                 :", 111)
        self.instance_attr = instance_attr

    def __str__(self):
        return f"Color2(name={self.name}, age={self.age})"

    def __repr__(self):
        return f"Color2(name={self.name}, age={self.age})"

    def __class__(self):
        return 1111111


class color2():
    name = 111
    age = 222


print(color2)
