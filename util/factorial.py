# -*- coding: utf-8 -*-
__author__ = 'myth'

"""
阶乘
"""


def factorial(c):
    """
     阶乘   factorial(6)
    :param c: c >= 0
    :type c: int
    :return:
    :rtype: int
    """

    #return (lambda n: reduce(lambda result, current: (current + 1) * result, range(n), 1))(c)
    return (lambda x: lambda n: x(x)(n))(lambda f: lambda n: 1 if n == 0 else n*f(f)(n-1))(c)