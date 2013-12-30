# -*- coding: utf-8 -*-
__author__ = 'myth'


def vil2lxwf_view(context, render):

    # context.add_css('/css/se/category3d/style.css')
    # context.add_script('/js/se/category3d/meny.js')
    # context.add_script('/js/se/category3d/default.js')

    title = u'星空'
    return render('se/vil2lxwf.html',title=title)