# -*- coding: utf-8 -*-
import time
from bottle import Bottle

__author__ = 'myth'

api_tool = Bottle()
@api_tool.route('/status')
def api_status():

    return {'status':'online', 'servertime':time.time()}