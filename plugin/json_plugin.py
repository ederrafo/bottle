# -*- coding: utf-8 -*-
from bottle import response
from plugin import Plugin

__author__ = 'Administrator'




class JsonsPlugin(Plugin):
    ''' 这是画布渲染的插件. '''

    name = 'josns'
    api = 2

    def __init__(self, json_dumps=None):
        if not json_dumps:
            try:from json import dumps as json_dumps
            except ImportError: # pragma: no cover
                try: from simplejson import dumps as json_dumps
                except ImportError:
                    try: from django.utils.simplejson import dumps as json_dumps
                    except ImportError:
                        def json_dumps(data):
                            raise ImportError("JSON support requires Python 2.6 or simplejson.")
        self.json_dumps = json_dumps

    def apply(self, callback, route):
        dumps = self.json_dumps
        if not dumps: return callback
        def wrapper(*a, **ka):
            rv = callback(*a, **ka)
            if isinstance(rv, (dict,list)):
                #Attempt to serialize, raises exception on failure
                json_response = dumps(rv)
                #Set content type only if serialization succesful
                response.content_type = 'application/json'
                return json_response
            return rv
        return wrapper