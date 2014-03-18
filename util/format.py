# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal, ROUND_DOWN

__author__ = 'myth'


def parse_int(value, default=0):
    """
    整型转换
    :param value:
    :param default:
    :return:
    """

    if not value is None:
        try:
            return int(value)
        except ValueError:
            return default
    else:
        return default


def parse_float(value, default=0l):
    """
    浮点类型转换
    :param value:
    :param default:
    :return:
    """

    if not value is None:
        try:
            return float(value)
        except ValueError:
            return default
    else:
        return default


def parse_date(value, default=None):
    """
     将时间戳转换未datetime对象
    :param value:
    :param default:
    :return:
    """

    if value:
        try:
            return datetime.datetime.fromtimestamp(value)
        except ValueError:
            return default
    else:
        return default


def float_to_decimal(value, hold=2):
    """
    float转换未decimal
    :param value:
    :param hold: 保留位数
    :return:
    """

    result = Decimal(str(value))
    return decimal_format(result, hold)


def decimal_format(value, hold=2):
    """
    Decimal 精度保留
    :param value:
    :param hold: 保留位数
    :return:
    """

    if not hold > 0:
        hold = 2
    # value.quantize(Decimal('.01'), rounding=ROUND_DOWN)
    return value.quantize(Decimal(('.%%0%dd' % hold) % 1), rounding=ROUND_DOWN)