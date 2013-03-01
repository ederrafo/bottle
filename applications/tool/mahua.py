# -*- coding: utf-8 -*-
__author__ = 'myth'


'''
一个在线编辑markdown文档的编辑器,
详情参考：http://mahua.jser.me/
'''

def mahua_view(context,render):

    context.add_script('/js/lib/ace/ace.js')
    context.add_script('/js/lib/ace/keybinding-vim.js')
    context.add_css('/css/mahua/mahua.css')


    title = u'MaHua 在线markdown编辑器'
    return render('tool/mahua.html',title=title)