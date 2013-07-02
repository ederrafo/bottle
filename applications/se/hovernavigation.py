# -*- coding: utf-8 -*-
__author__ = 'Administrator'


def hovernavigation_view(context,render):

    context.add_css('/css/se/hovernavigation/default.css')
    context.add_css('/css/se/hovernavigation/component.css')

    context.add_script('/js/se/hovernavigation/modernizr.custom.js')

    title = u'css3图标悬停导航菜单'
    return render('se/hovernavigation.html',title=title)