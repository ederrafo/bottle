# -*- coding: utf-8 -*-
__author__ = 'myth'


def category3d_view(context,render):

    context.add_css('/css/se/category3d/style.css')
    context.add_script('/js/se/category3d/meny.js')
    context.add_script('/js/se/category3d/default.js')

    title = u'Css Jquery 3D效果菜单'
    return render('se/category3d.html',title=title)

