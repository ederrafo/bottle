# -*- coding: utf-8 -*-
import sys
from util.setting.color import CLUT

__author__ = 'myth'


"""
带颜色的输出
"""


def print_all():
    """
    Print all 256 xterm color codes.
    """
    for short, rgb in CLUT:
        sys.stdout.write('\033[48;5;%sm%s:%s' % (short, short, rgb))
        sys.stdout.write("\033[0m  ")
        sys.stdout.write('\033[38;5;%sm%s:%s' % (short, short, rgb))
        sys.stdout.write("\033[0m\n")


def print_c(out_str, color='', is_bg=False):
    """
    待颜色的输出
    :param out_str:
    :param color:
    :param is_bg:
    :return:
    """

    if color is None:
        print out_str
    else:

        color = color.lower()
        colors = dict(c[::-1] for c in CLUT)

        _color = colors.get(color, None)
        _format = "\033[%d;5;%sm%r\033[0m"

        bg_color = 48
        fg_color = 38

        if _color:
            print _format % (bg_color if is_bg else fg_color, _color, out_str)
        else:
            print out_str


# if __name__ == '__main__':
def run():

    # print_all()
    print_c(u'这是一个测试', color='d7ff00')
    print_c('这是一个测试', color='d7ff00')
    print_c(1, color='d7ff00')
    print_c(True, color='d7ff00')
    print_c([1, u'啊', '啊'], color='d7ff00')
    print_c({'a': u'啊', 'b': '啊'}, color='d7ff00')
    print_c(str(u'测试'.encode("utf-8")), color='d7ff00')
