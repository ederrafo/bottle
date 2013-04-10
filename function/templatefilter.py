# -*- coding: utf-8 -*-
'''
模板过滤器
'''
from config import HOST, PORT

__author__ = 'myth'


#设置域名
def get_config_domain_name(value):
    domain_name = 'http://%s:%s' % (HOST,PORT)
    if value == 'mat_domain':
        url = '%s' % (domain_name)
    else:
        url = ''
    return url


#设置url
def get_config_domain_url(value,url):

    if url.startswith("http://") or url.startswith("https://"):
        return  url
    else:
        domain_name = get_config_domain_name(value)
        return domain_name.rstrip("/")+'/'+url.lstrip('/')



#设置域名
def get_domain_name(value):
    domain_name = 'http://%s:%s' % (HOST,PORT)
    # domain_name = 'http://www.example.com'
    if value:
        url = '%s%s' % (domain_name,value)
    else:
        url = ''
    return url


#设置url
def get_domain_url(value,url):

    if url.startswith("http://") or url.startswith("https://"):
        return  url
    else:
        domain_name = get_domain_name(value)
        return domain_name.rstrip("/")+'/'+url.lstrip('/')
