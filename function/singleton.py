# -*- coding: utf-8 -*-
__author__ = 'myth'

def singleton1(class_):
    class class_w(class_):
        _instance = None
        def __new__(class_, *args, **kwargs):
            if class_w._instance is None:
                class_w._instance = super(class_w,class_).__new__(class_,*args,**kwargs)
                class_w._instance._sealed = False
            return class_w._instance
        def __init__(self, *args, **kwargs):
            if self._sealed:
                return
            super(class_w, self).__init__(*args, **kwargs)
            self._sealed = True
    class_w.__name__ = class_.__name__
    return class_w

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


#@singleton
class A(object):

#    __metaclass__ = Singleton
    def __init__(self):
        print 'this is a'
        self.good = 1

    def get(self):
        self.good+=1
        return self.good

#@singleton
class B(A):
    def __init__(self):
        print 'this is B'
        self.good=2

    def get(self):
        self.good +=2
        return self.good

    def _get(self):
        return self.good


if __name__ == '__main__':

    a1 = A()
    a2 = A()
    b1 = B()
    b2 = B()
    print '-'*50
    print type(b1)
    print type(a1)
    print b1.get()
    print b2.get()
    print a1.get()
    print a2.get()