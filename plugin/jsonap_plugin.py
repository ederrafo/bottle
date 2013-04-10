# -*- coding: utf-8 -*-
from bottle import response, request
from plugin import Plugin

__author__ = 'Administrator'


class JSONAPIPlugin(Plugin):
    name = 'jsonapi'
    api = 1

    def __init__(self, json_dumps=None):
        # uninstall('json')
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

    def apply(self, callback, context):
        dumps = self.json_dumps
        if not dumps: return callback
        def wrapper(*a, **ka):
            r = callback(*a, **ka)
            # Wrap in callback function for JSONP
            callback_function = request.query.get('callback')
            if not callback_function:
                return r
            else:
                # Attempt to serialize, raises exception on failure
                json_response = dumps(r)
                # Set content type only if serialization succesful
                response.content_type = 'application/json'
                json_response = ''.join([callback_function, '(', json_response, ')'])
                return json_response
        return wrapper