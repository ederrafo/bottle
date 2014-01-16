# -*- coding: utf-8 -*-
import os
from bottle import run
from config import IS_SESSION, IS_RELOADER, IS_DEBUG, HOST, PORT, LOG_CONFIG
from controllers import create_app
from util import log
from util.profiling import profile_func

__author__ = 'Administrator'


@profile_func()
def main():
    log.set_config(**LOG_CONFIG)
    app = create_app(session=IS_SESSION)
    #bottle.TEMPLATE_PATH=['/web2py/applications/myapp/views/demo/']
    # print '%s:%d' % (HOST,PORT)
    run(app, host=HOST, port=PORT, reloader=IS_RELOADER,debug=IS_DEBUG)

if __name__ == '__main__':
    # log.set_config(**LOG_CONFIG)
    # app = create_app(session=IS_SESSION)
    # #bottle.TEMPLATE_PATH=['/web2py/applications/myapp/views/demo/']
    # # print '%s:%d' % (HOST,PORT)
    # run(app, host=HOST, port=PORT, reloader=IS_RELOADER,debug=IS_DEBUG)
    main()
else:
    # Mod WSGI launch
    os.chdir(os.path.dirname(__file__))
    log.set_config(**LOG_CONFIG)
    application = create_app(session=IS_SESSION)
