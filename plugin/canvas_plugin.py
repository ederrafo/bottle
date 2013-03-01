# -*- coding: utf-8 -*-
#from functools import partial
import inspect
import traceback
from bottle import  HTTPError, BaseTemplate
from controllers.context import Context
#from function.templatefilter import get_domain_name
from plugin import Plugin

__author__ = 'myth'


class CanvasPlugin(Plugin):
    ''' 这是画布渲染的插件. '''

    name = 'canvas'
    api = 2

    def __init__(self,keyword='context'):
        self.keyword = keyword

    def apply(self, callback, context):
        # Override global configuration with route-specific values.
        conf = context.config.get('canvas') or {}
        keyword = conf.get('keyword', self.keyword)
        #测试如果原来的回调函数接受一个'context'关键字。
        #忽略它，如果它并不需要一个画布句柄。
        args = inspect.getargspec(context.callback)[0]
        if keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            canvas = Context()

            kwargs[keyword] = canvas
            try:
                self.__(canvas)
                rv = callback(*args, **kwargs)
            except Exception, e:
                print traceback.format_exc(e)
                raise HTTPError(500, "CanvasPlugin Error", e)
            return rv
        return wrapper

    def __(self,canvas):
        #添加模板中的全局变量
        BaseTemplate.defaults.update({'g':{
            'script_list' : canvas.script_list,
            'css_list' : canvas.css_list
        }})






