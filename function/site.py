# -*- coding: utf-8 -*-
from util.carray import unique
from function.globalenv import global_env

def add_global_css(*args):
    css_list = list()
    for css in args:
        if isinstance(css, list):
            css_list.extend(css)
        else:
            css_list.append(css)
    global_env.css_list.extend(css_list)
    global_env.css_list = unique(global_env.css_list)

def add_global_script(*args):
    script_list = list()
    for script in args:
        if isinstance(script, list):
            script_list.extend(script)
        else:
            script_list.append(script)
    global_env.script_list.extend(script_list)
    global_env.script_list = unique(global_env.script_list)

#样式的删除方法
def del_global_css(*args):
    css_list = list()
    for css in args:
        if isinstance(css, list):
            css_list.extend(css)
        else:
            css_list.append(css)
    css_list = unique(css_list)
    css_dict = dict.fromkeys(global_env.css_list,True)
    [css_dict.pop(i) for i in css_list if css_dict.has_key(i)]
    global_env.css_list = css_dict.keys()

#js的删除方法
def del_global_script(*args):
    script_list = list()
    for script in args:
        if isinstance(script, list):
            script_list.extend(script)
        else:
            script_list.append(script)
    script_list = unique(script_list)
    script_dict = dict.fromkeys(global_env.script_list,True)
    [script_dict.pop(i) for i in script_list if script_dict.has_key(i)]
    global_env.script_list = script_dict.keys()
    