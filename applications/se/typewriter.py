# -*- coding: utf-8 -*-
__author__ = 'myth'


def typewriter_view(context,render):
    context.add_css('/css/se/typewriter/style.css')
#    context.add_script('http://html5shiv.googlecode.com/svn/trunk/html5.js')
#    context.add_script('http://cdnjs.cloudflare.com/ajax/libs/jquery/1.8.0/jquery.min.js')
    context.add_script('/js/jquery-1.7.1.min.js')
    context.add_script('/js/se/typewriter/default.js')

    title = u'打字机动画脚本'
    return render('se/typewriter.html',title=title)