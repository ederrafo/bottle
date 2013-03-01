# -*- coding: utf-8 -*-
import traceback
from bottle import Bottle
from config import IS_RELOADER
from function.classloader import ClassLoader

__author__ = 'myth'


apps_tool = Bottle()


@apps_tool.route('/<action>')
def action(action,context,render):
    try:
        obj = ClassLoader.getObject('applications.tool.%s.%s_view' % (action,action),reloader=IS_RELOADER)
        data = ClassLoader.applyFunc(obj,None,context=context,render=render)
    except Exception,e:
        print traceback.format_exc()
        data = u'服务器内部错误！！'

    return data