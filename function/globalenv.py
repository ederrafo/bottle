# -*- coding: utf-8 -*-

class GlobalEvn(object):
    def __init__(self):
        self.current_env = None

    def get_env(self):
        return self.current_env

    def set_env(self, env):
        self.current_env = env

    def __getattr__(self, name):
        if name == 'current_env':
            return self.current_env
        return getattr(self.current_env, name)

    def __setattr__(self, name, value):
        if name == 'current_env':
            object.__setattr__(self, 'current_env', value)
        else:
            self.current_env.__setattr__(name, value)

global_env = GlobalEvn()

