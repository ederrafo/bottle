# -*- coding: utf-8 -*-
from functools import partial
import inspect
import traceback
from bottle import jinja2_template, HTTPError, BaseTemplate
from function.templatefilter import get_domain_name, get_domain_url
from plugin import Plugin

__author__ = 'myth'


'''
模板插件
'''


class TemplatePlugin(Plugin):
    ''' This plugin applies the :func:`view` decorator to all routes with a
        `template` config parameter. If the parameter is a tuple, the second
        element must be a dict with additional options (e.g. `template_engine`)
        or default variables for the template. '''
    name = 'render'
    api  = 2

    def __init__(self,keyword='render'):
        self.keyword = keyword

    def apply(self, callback, context):
        # Override global configuration with route-specific values.
        conf = context.config.get('render') or {}
        keyword = conf.get('keyword', self.keyword)
        #测试如果原来的回调函数接受一个'context'关键字。
        #忽略它，如果它并不需要一个画布句柄。
        args = inspect.getargspec(context.callback)[0]
        if keyword not in args:
            return callback

        def wrapper(*args, **kwargs):

            kwargs[keyword] = self.__()
            try:
                rv = callback(*args, **kwargs)
            except Exception, e:
#                print traceback.format_exc(e)
                raise HTTPError(500, "CanvasPlugin Error", e)
            return rv
        return wrapper



    def __(self):
        '''
        设置模板过滤器
        :return:返回模板
        '''
        #将自定义的Filter加入字典中
        #cache_size：
        #           缓存大小，缺省为50，即如果加载超过50个模板，那么则保留最近使用过多50个模板，其它会被删除。
        #           如果换成大小设为0，那么所有模板都会在使用时被重 编译。如果不希望清除缓存，可以将此值设为-1.
        settings = dict(filters = {"get_domain_name":get_domain_name,"get_domain_url":get_domain_url},cache_size=0)

        #自动将template_settings作为关键字参数传入jinja2_template中，这样使用时不必每次都加这个参数
        template = partial(jinja2_template,template_settings = settings)

        #添加模板中的全局变量
        if not BaseTemplate.defaults.has_key('g'):
            BaseTemplate.defaults.update({'g':{}})

        return template