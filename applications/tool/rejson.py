# -*- coding: utf-8 -*-
from bottle import response

__author__ = 'myth'

'''
提交json
'''

def rejson_view(context,render):
    #todo

    context.add_script('/js/jquery-1.7.1.min.js')
    context.add_script('/js/artDialog.js')


    title = u'在线json提交'

    response.set_header("Access-Control-Allow-Origin", "*")
    response.set_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    response.set_header("Access-Control-Allow-Headers", "text/plain")
    response.set_header("Access-Control-Max-Age", "86400")


    return render('tool/rejson.html',title=title)