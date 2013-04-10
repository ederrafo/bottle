# -*- coding: utf-8 -*-

#import bottle
from applications.api.editor import api_tool
from applications.se import apps_se
from beaker.middleware import SessionMiddleware
from bottle import Bottle, HooksPlugin
from plugin.canvas_plugin import CanvasPlugin
from plugin.json_plugin import JsonsPlugin
from plugin.jsonap_plugin import JSONAPIPlugin
from plugin.template_plugin import TemplatePlugin
from applications import apps_home
#from applications.webdesk import apps_webdesk
from applications.webdesk.index import apps_webdesk
from applications.tool import apps_tool



#路由配置
DEFAULT_MODULES = (
                    (apps_webdesk,"/webdesk"),
                    (apps_tool,"/tool"),
                    (apps_se,"/se"),
                    (api_tool,"/api"),
                    (apps_home,"/"),
                )

#session配置
SESSION_OPTS = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

def create_app(config=None, modules=None,session = False):
    if modules is None:
        modules = DEFAULT_MODULES

    app = Bottle()

    # 插件安装
    canvas = CanvasPlugin()
    template = TemplatePlugin()
    jsons = JsonsPlugin()
    jsonp = JSONAPIPlugin()
#    hooks = HooksPlugin()
#    hooks.add('before_request',__)
    plugins = [canvas,template,jsons,jsonp]#,hooks
#    jinja2_template =
    # 添加子模块
    for route in modules:
        if len(route) == 2:
            for plugin in plugins:
                route[0].install(plugin)
            if route[1]== '' or route[1]== '/':
                app.merge(route[0])
            else:
                app.mount(*route)
        else:
            print u'路由格式错误！！'
#            raise HTTPError(500, "Database Error")

    #忽略尾部的反斜杠
    app = StripPathMiddleware(app)

    #添加session功能
    if session:
        app = SessionMiddleware(app, SESSION_OPTS)
    return app





#app = SessionMiddleware(bottle.app(), session_opts)


class StripPathMiddleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.app(e,h)

