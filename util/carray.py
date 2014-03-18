# -*- coding: utf-8 -*-
import copy
try:
    #need ordereddict
    from ordereddict import OrderedDict
except:
    try:
        from collections import OrderedDict
    except:
        OrderedDict = dict


def unique(seq, constant=True):
    """list去重

    :param seq: 需去重的list
    :return: 去重后的list
    """
    noDupes = []

    #防止list的物理地址不变化
    if constant:
        #深拷贝 拷贝对象及其子对象
        _seq = copy.deepcopy(seq)
        for i, e in enumerate(_seq):
            if not noDupes.count(e):
                noDupes.append(e)
            else:
                seq.pop(i)
        return seq
    else:
        [noDupes.append(i) for i in seq if not noDupes.count(i)]
        return noDupes


def arr_to_dict(arr, key='id', unique=True, isAttr=False, ordered=False):
    """
    数组转换为字典
    """
    result = {}
    if ordered and isinstance(OrderedDict, type):
        result = OrderedDict()
    if arr:
        for row in arr:
            if isAttr:
                assert hasattr(row, key)
                val = getattr(row, key)
            else:
                assert key in row
                val = row[key]

            if unique:
                result[val] = row
            else:
                if val in result:
                    result[val].append(row)
                else:
                    result[val] = [row]
    return result