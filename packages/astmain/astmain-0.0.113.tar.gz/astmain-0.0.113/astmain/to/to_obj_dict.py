class to_obj_dict:
    """ EXPLAIN :  日志追加记录函数
        EXAMPLE :
                    obj1 = to_obj_dict({"aaa": "111", "bbb": 222})    # obj1 = to_obj_dict(dict(aaa=111))
                    obj1.bbb = 333
                    print("obj1.aaa                 :", obj1["aaa"])  # "111"
                    print("obj1.bbb                 :", obj1.bbb)     # 222
                    print("obj1                     :", obj1)         # {'aaa': '111', 'bbb': 222}
    """
    def __init__(self, data):
        self.data = data

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __getitem__(self, key):
        return self.data[key]

    def __setattr__(self, name, value):
        if name == 'data':
            super().__setattr__(name, value)
        else:
            self.data[name] = value

    def __delattr__(self, name):
        try:
            del self.data[name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return f"{type(self).__name__}({self.data})"


if __name__ == '__main__':

    obj1 = to_obj_dict({"aaa": "111", "bbb": 222})    # obj1 = to_obj_dict(dict(aaa=111))
    obj1.bbb = 333
    print("obj1.aaa                 :", obj1["aaa"])  # "111"
    print("obj1.bbb                 :", obj1.bbb)     # 222
    print("obj1                     :", obj1)         # {'aaa': '111', 'bbb': 222}

#     print(obj1)  输出   "{aaa:111}"
