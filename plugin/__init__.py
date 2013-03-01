# -*- coding: utf-8 -*-
from bottle import PluginError

__author__ = 'myth'

class Plugin(object):

    def __init__(self,*args, **kwargs):


        pass


    def setup(self, app):
        ''' Make sure that other installed plugins don't affect the same
                keyword argument.'''
        for other in app.plugins:
            if not isinstance(other, self.__class__): continue
            if other.keyword == self.keyword:
                raise PluginError("Found another canvas plugin with "\
                                  "conflicting settings (non-unique keyword 's%')." % self.keyword)


