# # coding=utf-8
# import os
# from ..colors import colors
#
# print_old = print
#
#
# def print_new(*args, **kwargs):
#     print_old(colors.yellow, *args, **kwargs)
#
#
# def print_hook(isok=False):
#     if isok == True:
#         os.environ['print_hook'] = 'True'
#         global print
#         print = print_new
#         return print_new
#     if isok == False:
#         os.environ['print_hook'] = 'True'
#         return print_old
