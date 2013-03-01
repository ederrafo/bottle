# -*- coding: utf-8 -*-
'''
from functools import partial
from bottle import jinja2_template
from controllers.context import Context

def run():


    #定义一个时间格式转换的Filter
    def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
        return value.strftime(format)
     
    #将自定义的Filter加入字典中
    settings = dict(filters = {"datetimeformat":datetimeformat})
     
    #自动将template_settings作为关键字参数传入jinja2_template中，这样使用时不必每次都加这个参数
    template = partial(jinja2_template,template_settings = settings)



'''