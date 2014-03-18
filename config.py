# -*- coding: utf-8 -*-
from util.address import get_ip_address

__author__ = 'Administrator'

IS_DEBUG = True
IS_SESSION = False
IS_RELOADER = True


HOST = '127.0.0.1'#get_ip_address('eth0')
# HOST = get_ip_address('eth0')
PORT = 8080

DOMAIN = "mytool.zhubajie.com"


#session配置
SESSION_OPTS = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

#日志配置信息
LOG_CONFIG = {
    'PRINT_LEVEL':'DEBUG',
    'LOG_LEVEL':'INFO',
    'LOG_FILE':'demo.log',
    'LOG_FORMAT':'%(asctime)s [%(levelname)s]: %(message)s',
    }