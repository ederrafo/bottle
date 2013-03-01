# -*- coding: utf-8 -*-
__author__ = 'myth'

'''
JFuncDiagraph 函数作图器
'''


def drafting_view(context,render):


    context.add_script('/js/jquery-1.7.1.min.js')
    context.add_script('/js/lib/JFuncDiagraph/jquery_my_extend.js')
    context.add_script('/js/lib/JFuncDiagraph/jquery.easing.js')
    context.add_script('/js/lib/JFuncDiagraph/JFuncDiagraph.js')
    context.add_css('/css/lib/JFuncDiagraph/style.css')


    title = u'JFuncDiagraph 函数作图器'
    return render('tool/drafting.html',title=title)