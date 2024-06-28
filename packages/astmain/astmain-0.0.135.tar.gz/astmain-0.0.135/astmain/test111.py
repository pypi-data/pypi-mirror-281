import inspect


def execute_code(code_str, *args, **kwargs):
    """
    安全地执行给定的 Python 代码字符串,并返回函数的返回结果。

    Args:
        code_str (str): 要执行的 Python 代码字符串。
        *args: 要传递给函数的位置参数。
        **kwargs: 要传递给函数的关键字参数。

    Returns:
        tuple: 一个包含以下元素的元组:
            - bool: 代码执行是否成功。
            - Any: 如果代码块有返回语句,则返回相应的返回值;否则返回 None。
            - dict: 如果代码块定义了函数,则返回函数的返回结构;否则返回 None。
            - Any: 如果代码块定义了函数,则返回函数的执行结果;否则返回 None。
    """
    try:
        # 创建一个新的命名空间
        exec_namespace = {}

        # 使用 exec 函数执行代码字符串
        exec(code_str, exec_namespace, exec_namespace)

        # 检查是否有返回值
        success = True
        return_value = exec_namespace.get('return_value', None)

        # 检查是否定义了函数,并获取函数的返回结构和执行结果
        func_return_struct = None
        func_result = None
        for name, obj in exec_namespace.items():
            if callable(obj) and name != 'execute_code':
                try:
                    func_return_struct = inspect.getfullargspec(obj)
                    func_result = obj(*args, **kwargs)
                    break
                except TypeError:
                    # 如果对象不是函数,则跳过
                    pass

        # return success, return_value, func_return_struct, func_result
        return func_result

    except Exception as e:
        # 捕获并处理任何异常
        # print(f"执行代码时发生错误: {e}")
        return f"执行代码时发生错误: {e}"


if __name__ == '__main__':
    # 定义一个函数字符串
    func_def = """
def aaa(x, y=10):
    return x + y
    """

    # 执行函数字符串
    func_result = execute_code(func_def, 655, y=5)
    print(func_result)

