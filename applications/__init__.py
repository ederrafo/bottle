# -*- coding: utf-8 -*-
from applications.map import website_map

from bottle import Bottle, response, request
from bottle import static_file
#from bottle import jinja2_view as view



apps_home = Bottle()

#------------------------------------------------------------------------------------------------------------------------------------------------
'''
@apps_home.hook('before_request')
def a():
    print 'a'*10

@apps_home.hook('before_request')
def b():
    print 'b'*10

@apps_home.hook('after_request')
def enable_cors():
    print '+'*50
    print dir(response)
    response.headers['Access-Control-Allow-Origin'] = '*'

@apps_home.hook('after_request')
def header():
    print '-'*50
    response.headers['Content-Type'] = 'text/html; charset=GBK'
'''
#-----------------------------------------------------------------------------------------------------------------------------------------------

@apps_home.route('/say/<name>')
def sayhello(name,context,render):
    import datetime
    times=datetime.datetime.now()
    return render('index.html',time=times,name=name)


@apps_home.route('/hello/:name')
#@view("index.html")
def index(name='World'):
    return dict(name=name)

@apps_home.route('/')
def home():
    return "Welcome!! <a href='/map'>网站地图</a>"

@apps_home.route('/map')
def map_url(render):
    maps =  website_map()
    return render("map.html",maps=maps)


@apps_home.route('/tetris')
def tetris(context,render):
    context.add_css(['/css/tetris/style.css'])
    context.add_script('/js/jquery-1.7.1.min.js')
    context.add_script('/js/tetris/config.js')
    context.add_script('/js/tetris/achieve.js')
    return render('tetris.html')

@apps_home.route('/battlecity')
def battle_city(context,render):

    context.add_css('/css/battlecity/index.css')

    context.add_script('/js/battlecity/WebPlay.js')

    context.add_script('/js/battlecity/Util/Tick.js')
    context.add_script('/js/battlecity/Util/Timer.js')
    context.add_script('/js/battlecity/Util/Misc.js')

    context.add_script('/js/battlecity/Const.js')
    context.add_script('/js/battlecity/App.js')
    context.add_script('/js/battlecity/Scene.js')
    context.add_script('/js/battlecity/Game.js')

    context.add_script('/js/battlecity/Object/Bonus.js')
    context.add_script('/js/battlecity/Object/Boom.js')
    context.add_script('/js/battlecity/Object/Bullet.js')
    context.add_script('/js/battlecity/Object/Tank.js')
    context.add_script('/js/battlecity/Object/MyTank.js')
    context.add_script('/js/battlecity/Object/NPCTank.js')

    context.add_script('/js/battlecity/UI/UIOpen.js')
    context.add_script('/js/battlecity/UI/UIGame.js')
    context.add_script('/js/battlecity/UI/UIScore.js')
    context.add_script('/js/battlecity/UI/UIOver.js')

    context.add_script('/js/battlecity/Map.dat')

    title = u'方向ASDW 射击IOKL, 确定Enter -- BattleCity'
    return render('battle_city.html',title=title)

@apps_home.route('/login')
def login(context,render):
    context.add_css(['/css/login.css'])
#    context.add_script(['jquery-1.7.1.min.js','forms.js'])
    context.add_script('/js/jquery-1.7.1.min.js')
    context.add_script('/js/forms.js')
#    context.add_script('/js/webdesk/jquery-ui-1.8.16.custom.min.js')
    return render('login.html')

@apps_home.route('/session_test')
def session_test():
    s = request.environ.get('beaker.session')
    if s is None:
        return u'没有打开session功能！！'
    else:
        s['test'] = s.get('test',0) + 1
        s.save()
        return u'''session功能已经打开：<br/>
                    Test counter: %d''' % s['test']
@apps_home.route('/keep_alive')
def keep_alive():
    '''Keep-alive 请求'''

    import time
    yield 'START<br/>'
    time.sleep(3)
    yield 'MIDDLE<br/>'
    time.sleep(5)
    yield 'END<br/>'

###############################################################################
#静态文件路由 ##################################################################
###############################################################################
@apps_home.route('/:path#(images|css|js|docs|fonts)/.+#')
def server_static(path):
    return static_file(path, root = 'static')

@apps_home.route('/:file#(favicon.ico)#')
def favicon(file):
    return static_file(file, root = '')



#@apps_home.route('/js/<path:path>')
#def server_static(path):
#    return static_file(path, root='static/js')
#
#
#@apps_home.route('/css/<path:path>')
#def server_static(path):
#    return static_file(path, root='static/css')
#
#
#@apps_home.route('/images/<path:path>')
#def server_static(path):
#    return static_file(path, root='static/images')

###############################################################################
