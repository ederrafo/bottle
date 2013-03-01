# -*- coding: utf-8 -*-
__author__ = 'myth'
'''
在线编辑工具
'''

def editor_view(context,render):

#    context.add_script('/js/jquery-1.7.1.min.js')
#    context.add_script('/js/lib/editor/ace.js')

    title = u'在线编辑工具'
    return render('tool/editor_online.html',title=title)