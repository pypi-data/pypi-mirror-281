import inspect


def eval_func_str(code_str, *args, **kwargs):
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
            if callable(obj) and name != 'eval_func_str':
                try:
                    func_return_struct = inspect.getfullargspec(obj)
                    func_result = obj(*args, **kwargs)
                    break
                except TypeError:
                    # 如果对象不是函数,则跳过
                    pass
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
    # func_result = eval_func_str(func_def, 111, y=222)
    func_result = eval_func_str("""
def aaa(x, y=10):
    return x + y
    """, 111, y=222)
    print(func_result)



    """
    源码 https://poe.com/chat/3dr2ydmer07bb7f2znn
import inspect

def execute_code(code_str, *args, **kwargs):
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
        
        return success, return_value, func_return_struct, func_result
    
    except Exception as e:
        # 捕获并处理任何异常
        print(f"执行代码时发生错误: {e}")
        return False, None, None, None
    
    
    
    """

