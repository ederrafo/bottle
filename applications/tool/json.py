# -*- coding: utf-8 -*-
__author__ = 'myth'
#from applications.tool import  apps_tool
#from bottle import Bottle
#
#
#apps_tool = Bottle()
'''
用于在线json解析
'''

#@apps_tool.route('/json')
def json_view(context,render):
    context.add_css('/css/lib/json-handle/jsonH.css')
    context.add_script('/js/jquery-1.7.1.min.js')
    context.add_script('/js/lib/json-handle/jh.js')
    context.add_script('/js/lib/json-handle/JSON.js')
    context.add_script('/js/lib/json-handle/treeNav.js')
    context.add_script('/js/lib/json-handle/nav.js')
    context.add_script('/js/lib/json-handle/jsonH.js')
    context.add_script('/js/lib/json-handle/setting.js')
#    context.add_script('/js/lib/json-handle/pageInit.js')

    title = u'在线JSON校验格式化工具'
    return render('tool/json.html',title=title)