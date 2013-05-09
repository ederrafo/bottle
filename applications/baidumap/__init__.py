# -*- coding: utf-8 -*-
from bottle import Bottle

__author__ = 'Administrator'

apps_baidumap = Bottle()

@apps_baidumap.route('/')
@apps_baidumap.route('/index')
def index(render):
    return  render('baidumap/index.html')

