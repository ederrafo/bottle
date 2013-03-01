# -*- coding: utf-8 -*-
__author__ = 'myth'

'''
用于rest接口测试
'''

def rest_view(context,render):

    context.add_script('/js/jquery-1.7.1.min.js')
    context.add_script('/js/artDialog.js')


    title = u'在线rest接口测试'
    return render('tool/rest.html',title=title)