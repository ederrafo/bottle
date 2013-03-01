# -*- coding: utf-8 -*-
from function.singleton import singleton
from util.carray import unique

#@singleton
class Context(dict):


    def __init__(self):
#        super(Context, self).__init__(self)
        self.script_list = list()
        self.css_list = list()
#        self['script_list'] = self.script_list
#        self['css_list'] = self.css_list
#        self.script_list = self['script_list']
#        self.css_list = self['css_list']


    def add_css(self,*args):
        css_list = list()
        for css in args:
            if isinstance(css, list):
                css_list.extend(css)
            else:
                css_list.append(css)
        self.css_list.extend(css_list)
        self.css_list = unique(self.css_list)

    def add_script(self,*args):
        script_list = list()
        for script in args:
            if isinstance(script, list):
                script_list.extend(script)
            else:
                script_list.append(script)
        self.script_list.extend(script_list)
        self.script_list = unique(self.script_list)


    #样式的删除方法
    def del_css(self,*args):
        css_list = list()
        for css in args:
            if isinstance(css, list):
                css_list.extend(css)
            else:
                css_list.append(css)
        css_list = unique(css_list)
        css_dict = dict.fromkeys(self.css_list,True)
        [css_dict.pop(i) for i in css_list if css_dict.has_key(i)]
        self.css_list = css_dict.keys()

    #js的删除方法
    def del_script(self,*args):
        script_list = list()
        for script in args:
            if isinstance(script, list):
                script_list.extend(script)
            else:
                script_list.append(script)
        script_list = unique(script_list)
        script_dict = dict.fromkeys(self.script_list,True)
        [script_dict.pop(i) for i in script_list if script_dict.has_key(i)]
        self.script_list = script_dict.keys()



