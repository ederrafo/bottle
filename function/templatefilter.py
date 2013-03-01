# -*- coding: utf-8 -*-
'''
模板过滤器
'''
from function.config import PORT, HOST

__author__ = 'myth'



#设置域名
def get_domain_name(value):
    domain_name = 'http://%s:%s' % (HOST,PORT)
    if value == 'mat_domain':
        url = '%s' % (domain_name)
    else:
        url = ''
    return url


#设置url
def get_domain_url(value,url):
    domain_name = get_domain_name(value)
    if url.startswith("http://") or url.startswith("https://"):
        return  url
    else:
        return domain_name.rstrip("/")+'/'+url.lstrip('/')
