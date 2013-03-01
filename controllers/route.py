# -*- coding: utf-8 -*-
import sys
import types

__author__ = 'myth'


class Route(object):



    def __init__(self):
        pass


    def send_message_to_route_action(self,action):
        print 'good'
        pass




def json(aa):
    print 'json %s' % aa



if __name__ == '__main__':


#    route = Route()
#    route.send_message_to_route_action('json')
    from function.classloader import ClassLoader

    route = ClassLoader.getObject("controllers.route.json")
    print '~'*50
#    route('this')
    print '!'*50
    b = ClassLoader.applyFunc(route,'send_message_to_route_action',['json'])
    print b
