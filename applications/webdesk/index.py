# coding: utf8
#webdesk app

#from applications.webdesk import apps_webdesk
from bottle import Bottle

apps_webdesk = Bottle()

@apps_webdesk.route('/')
@apps_webdesk.route('/index')
def index(context,render):

    context.add_css('/css/jquery-ui-1.8.16.custom.css')
    context.add_css('/css/webdesk.css')

    context.add_script('/js/webdesk/jquery-1.7.1.min.js')
    context.add_script('/js/webdesk/jquery-ui-1.8.16.custom.min.js')
    context.add_script('/js/webdesk/jquery.transform-0.9.3.min.js')
    context.add_script('/js/webdesk/jquery.animate-shadow-min.js')
    context.add_script('/js/webdesk/webdesk.js')

    title = u'Extreme WebDesk'
    return render('webdesk/index.html',title=title)

@apps_webdesk.route('/desenho')
def desenho(render):
    return render('webdesk/desenho.html')