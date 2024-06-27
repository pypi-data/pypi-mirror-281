# coding=utf-8
import re


# 没有完善
def num(xxx):
    """ EXPLAIN : 数据转数字_没有完善
        EXAMPLE :  print("result                 :", __.to.num("-111.222"))
    """
    try:
        res = "".join(re.findall(r'[0-9.-]', xxx))
        return float(res)
    except Exception as error:
        return 0


if __name__ == '__main__':
    print("result                 :", num("-111.222"))
