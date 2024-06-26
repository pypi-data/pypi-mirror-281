import json

#   已解决raise JSONDecodeError(“Expecting value”, s, err.value) from None              https://blog.csdn.net/yuan2019035055/article/details/127824881
def JSON(xxx):
    # 定义一个 JSON 字符串
    json_string = '{"name": "John Doe", "age": 35, "email": "john.doe@example.com"}'

    # 将 JSON 字符串转换为 Python 字典
    my_dict = json.loads(xxx)
    print(type(my_dict))

    return my_dict


if __name__ == '__main__':
    xxx = '{"name": "John Doe", "age": 35, "email": "john.doe@example.com"}'
    print("111                 :", JSON(xxx))
    pass
