# -*- coding: utf-8 -*-
import sys
import traceback
import types

__author__ = 'myth'


class ClassLoader(object):


    def __init__(self):
        pass

    @classmethod
    def __get_mod(cls,modulePath,reloader=False):
        try:
            if reloader:
                if sys.modules.has_key(modulePath):
                    sys.modules.pop(modulePath)
            aMod = sys.modules[modulePath]
            if not isinstance(aMod, types.ModuleType):
                raise KeyError
        except KeyError:
            # The last [''] is very important!
            try:
                aMod = __import__(modulePath, globals(), locals(), [''])
                sys.modules[modulePath] = aMod
            except:
                print traceback.format_exc()
        return aMod
    @classmethod
    def __get_func(cls,fullFuncName,reloader=False):
        """Retrieve a function object from a full dotted-package name."""

        # Parse out the path, module, and function
        lastDot = fullFuncName.rfind(u".")
        funcName = fullFuncName[lastDot + 1:]
        modPath = fullFuncName[:lastDot]
        aMod = cls.__get_mod(modPath,reloader=reloader)
        aFunc = getattr(aMod, funcName)

        # Assert that the function is a *callable* attribute.
        assert callable(aFunc), u"%s is not callable." % fullFuncName

        # Return a reference to the function itself,
        # not the results of the function.
        return aFunc
    @classmethod
    def __get_Class(cls,fullClassName, parentClass=None,reloader=False):
        """Load a module and retrieve a class (NOT an instance).

        If the parentClass is supplied, className must be of parentClass
        or a subclass of parentClass (or None is returned).
        """
        aClass = cls.__get_func(fullClassName,reloader=reloader)

        # Assert that the class is a subclass of parentClass.
        if parentClass is not None:
            if not issubclass(aClass, parentClass):
                raise TypeError(u"%s is not a subclass of %s" %
                                (fullClassName, parentClass))

        # Return a reference to the class itself, not an instantiated object.
        return aClass
    @classmethod
    def applyFunc(cls,obj,strFunc,*arrgs,**kwargs):
        if strFunc is None:
            objFunc = obj
        else:
            objFunc = getattr(obj, strFunc)
        return apply(objFunc,arrgs,kwargs)
    @classmethod
    def getObject(cls,fullClassName,reloader=False):
        clazz = cls.__get_Class(fullClassName,reloader=reloader)
#        return clazz() #返回对象
        return  clazz #返回方法或者类


#--------------------------------------------------------------test-----------------------------------------------------



class T(object):
    def __init__(self):
        pass

    def call(self,arg1=None,arg2=None):
        print 'this is class function.',arg1,arg2
        return True


def F(arg1=None,arg2=None):
    print 'this is function.',arg1,arg2
    return True


if __name__ == '__main__':


    t = ClassLoader.getObject('function.classloader.T')
    #_t = ClassLoader.applyFunc(t,'call','arg1','arg2') #返回对象
    _t = ClassLoader.applyFunc(t(),'call','arg1','arg2') #返回方法或者类
    print _t
    print '-'*50

    #f = ClassLoader.getObject('function.classloader.F')#返回对象。此时方法直接被调用
    f = ClassLoader.getObject('function.classloader.F')#返回方法或者类。此时方法没有被调用，需要使用f(),才会被调用
    f()
    apply(f,('aa','bb'))
    apply(f,[],dict(arg2='aa',arg1='bb'))
    _f = ClassLoader.applyFunc(f,None,arg2='aa',arg1='bb')
    print _f