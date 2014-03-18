# -*- coding: utf-8 -*-
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
__author__ = 'myth'


class AlchemyEncoder(json.JSONEncoder):
    """
    将sqlalchemy对象转换为dict对象
    使用如下sqlalchemy to json：
    c = YourAlchemyClass()
    print json.dumps(c, cls=AlchemyEncoder)

    # sqlalchemy to dict：
    c = YourAlchemyClass()
    result = AlchemyEncoder().default(c)


    """
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = dict([(c.name, getattr(obj, c.name)) for c in obj.__table__.columns])
            return fields

        return json.JSONEncoder.default(self, obj)


def query_arr_to_dict(results, query):
    """
    将数据库db_session.query查询的结果转换为dict
    :param results: 结果集
    :param query: 结果集返回的列
    :return:
    """

    keys = []
    data = []
    if query and isinstance(query, list):
        for index, column in enumerate(query, start=1):
            if hasattr(column, 'key'):
                keys.append(column.key)
            else:
                keys.append('column%d' % index)

        for row in results:
            data.append(dict(zip(keys, row)))
    else:
        data = results

    return data


def sa_obj_to_dict(obj, filtrate=None, rename=None):
    """
    sqlalchemy 对象转为dict
    :param filtrate: 过滤的字段
    :type filtrate: list or tuple
    :param rename: 需要改名的,改名在过滤之后处理, key为原来对象的属性名称，value为需要更改名称
    :type rename: dict
    :rtype: dict
    """

    if isinstance(obj.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        #该类的相关类型，即直接与间接父类
        cla = obj.__class__.__mro__
        #过滤不需要的父类
        cla = filter(lambda c: hasattr(c, '__table__'), filter(lambda c: isinstance(c, DeclarativeMeta), cla))
        columns = []
        map(lambda c: columns.extend(c.__table__.columns), cla[::-1])
        # columns = obj.__table__.columns
        if filtrate and isinstance(filtrate, (list, tuple)):
            fields = dict(map(lambda c: (c.name, getattr(obj, c.name)), filter(lambda c: not c.name in filtrate, columns)))
        else:
            fields = dict(map(lambda c: (c.name, getattr(obj, c.name)), columns))
        # fields = dict([(c.name, getattr(obj, c.name)) for c in obj.__table__.columns])
        if rename and isinstance(rename, dict):
            #先移除key和value相同的项
            _rename = dict(filter(lambda (k, v): str(k) != str(v), rename.iteritems()))
            # if _rename:
            #     nkeys = _rename.values()
            #     okeys = _rename.keys()
            #     exist = filter(lambda x: x in fields, nkeys)
            #     no_exist = filter(lambda x: not x in fields, okeys)
            #如果原始key不存在，那么新的key对应的值默认为None
            #如果新的key已存在于原始key中，那么原始key的值将被新的key的值覆盖
            # map(lambda (k, v): fields.setdefault(v, fields.pop(k, None)), _rename.iteritems())
            map(lambda (k, v): fields.update({v: fields.pop(k, None)}), _rename.iteritems())
        #
        return fields
    else:
        return {}


def repr_alchemy(alchemy):
    """
    __repr__返回的数据

    """

    repr = '<%r(' % alchemy.__class__.__name__
    columns = []
    if isinstance(alchemy.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        for c in alchemy.__table__.columns:
            value = getattr(alchemy, c.name)
            columns.append('%r=%r' % (c.name, value))
    return repr + ', '.join(columns) + ')>'