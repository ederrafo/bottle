# -*- coding: utf-8 -*-
import re
from slimit import minify
from ckstyle.doCssCheck import doCheck
from ckstyle.doCssCompress import doCompress
from ckstyle.reporter.ReporterUtil import ReporterUtil


def css_compress():
    css = open('/home/myth/work/python_work/bottle/static/css/jquery-ui-1.8.16.custom.css' , 'r' ).read()

    # remove comments - this will break a lot of hacks :-P
    css = re.sub( r'\s*/\*\s*\*/', "$$HACK1$$", css ) # preserve IE<6 comment hack
    css = re.sub( r'/\*[\s\S]*?\*/', "", css )
    css = css.replace( "$$HACK1$$", '/**/' ) # preserve IE<6 comment hack

    # url() doesn't need quotes
    css = re.sub( r'url\((["\'])([^)]*)\1\)', r'url(\2)', css )

    # spaces may be safely collapsed as generated content will collapse them anyway
    css = re.sub( r'\s+', ' ', css )

    # shorten collapsable colors: #aabbcc to #abc
    css = re.sub( r'#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3(\s|;)', r'#\1\2\3\4', css )

    # fragment values can loose zeros
    css = re.sub( r':\s*0(\.\d+([cm]m|e[mx]|in|p[ctx]))\s*;', r':\1;', css )

    _css = ''
    for rule in re.findall( r'([^{]+){([^}]*)}', css ):

        # we don't need spaces around operators
        selectors = [re.sub( r'(?<=[\[\(>+=])\s+|\s+(?=[=~^$*|>+\]\)])', r'', selector.strip() ) for selector in rule[0].split( ',' )]

        # order is important, but we still want to discard repetitions
        properties = {}
        porder = []
        for prop in re.findall( '(.*?):(.*?)(;|$)', rule[1] ):
            key = prop[0].strip().lower()
            if key not in porder: porder.append( key )
            properties[ key ] = prop[1].strip()

        # output rule if it contains any declarations
        if properties:
            _css += "%s{%s}" % ( ','.join( selectors ), ''.join(['%s:%s;' % (key, properties[key]) for key in porder])[:-1] )

    return _css


def js_compress(context):
    js_text = minify(context, mangle=True, mangle_toplevel=True)
    return js_text

if __name__ == '__main__':
#    css = open('/home/myth/work/python_work/bottle/static/css/jquery-ui-1.8.16.custom.css','r').read()

    css = '''
    .test-zero-px {
    width: 0px;
}
.test-zero {
    width: 0;
    padding: 1px 0px;
}
.test-zero-dot-one-px {
    width: 0.1px;
}
.test-padding {
    padding: 1px 0px;
}
.test-padding-start-with-zero {
    padding: 0 1px 0 1px;
}
    '''
    _checker, message = doCompress(css,'/home/myth/tmp/test.css')
    js = open('/home/myth/work/python_work/bottle/static/js/forms.js','r').read()

    print js_compress(js)
    print '@'*50
    checker = doCheck(css)
    print _checker
    if checker.hasError():
        reporter = ReporterUtil.getReporter('text', checker)
        reporter.doReport()
        print reporter.export()


    print checker
    print message
    print '-'*50
    print css_compress()


