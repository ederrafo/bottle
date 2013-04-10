# -*- coding: utf-8 -*-
__author__ = 'Administrator'

def slicebox_view(context,render):
    title = u'Slicebox - 3D Image Slider'
    return render('css/Slicebox.html',title=title)