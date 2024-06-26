# coding=utf-8
# debug = False
debug = True

real_print = print
def print(*args, **kwargs):
    if debug:
        real_print(*args, **kwargs)

