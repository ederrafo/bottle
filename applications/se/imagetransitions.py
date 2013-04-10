# -*- coding: utf-8 -*-
__author__ = 'Administrator'


def imagetransitions_view(context,render):
    title = u'Experimental CSS3 Animations for (3D) Image Transitions'
    return render('css/ImageTransitions.html',title=title)