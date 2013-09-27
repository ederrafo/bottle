# -*- coding: utf-8 -*-
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
__author__ = 'myth'


class AlchemyEncoder(json.JSONEncoder):
    """
    c = YourAlchemyClass()
    print json.dumps(c, cls=AlchemyEncoder)
    """
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = dict([(c.name, getattr(obj, c.name)) for c in obj.__table__.columns])
            return fields

        return json.JSONEncoder.default(self, obj)