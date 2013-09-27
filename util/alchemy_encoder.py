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