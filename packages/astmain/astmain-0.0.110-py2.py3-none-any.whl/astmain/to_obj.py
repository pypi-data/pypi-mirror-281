from typing import Any, Dict


class to_obj_class:
    def __init__(self, data: Dict[str, Any]):
        self.__data = data

    def __getattr__(self, name: str) -> Any:
        try:
            return self.__data[name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __getitem__(self, key: str) -> Any:
        return self.__data[key]

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_to_obj_class__"):
            super().__setattr__(name, value)
        else:
            self.__data[name] = value

    def __setitem__(self, key: str, value: Any) -> None:
        self.__data[key] = value

    def __dir__(self) -> list:
        return list(self.__data.keys()) + super().__dir__()


def to_obj(data: Dict[str, Any]) -> to_obj_class:
    """
    将字典转换为可以使用 obj["key"] 和 obj.key 访问的对象.

    Args:
        data (Dict[str, Any]): 需要转换的字典数据.

    Returns:
        DictAccessProxy: 转换后的对象.
    """
    return to_obj_class(data)


if __name__ == '__main__':
    bbb = dict(aaa=111, vvv=111)
    bbb = to_obj(bbb)
    print("111                 :", bbb.aaa)
    print("111                 :", bbb.vvv)
    # print("111                 :", bbb["aaa"])
