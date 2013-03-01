# -*- coding: utf-8 -*-
import copy


def unique(seq,constant=True):
    """list去重

    :param seq: 需去重的list
    :return: 去重后的list
    """
    noDupes = []

    #防止list的物理地址不变化
    if constant:
        #深拷贝 拷贝对象及其子对象
        _seq =  copy.deepcopy(seq)
        for i,e in enumerate(_seq):
            if not noDupes.count(e):
                noDupes.append(e)
            else:
                seq.pop(i)
        return seq
    else:
        [noDupes.append(i) for i in seq if not noDupes.count(i)]
        return noDupes