# -*- coding: utf-8 -*-
__author__ = 'myth'
from ordereddict import OrderedDict


class PrintJson(object):

    def __init__(self):
        self.line = 0
        self.newline = '\n'
        self.space = '    '
        self.texts = OrderedDict()

    def _special_line(self, line, tote, first=1):
        param = {"first": False, "last": False}
        if line == first:
            param["first"] = True
        if line == tote:
            param["last"] = True
        return param

    def _last_line(self, text, last=True, **kwargs):
        if not last:
            return text + ','
        else:
            return text

    def _add_line(self, text, level=0, **kwargs):

        text = self._last_line(text, **kwargs)
        self._set_line_num()
        self.texts[self.line] = dict(level=level, text=text)

    def _set_line_num(self):
        self.line += 1

    def _new_line(self):
        self._set_line_num()
        self.texts[self.line] = dict(level=0, text='')

    @classmethod
    def print_json(cls, data, is_number=True):
        _type = data.__class__.__name__
        print 'print json is print type %s' % _type
        this = cls()
        name = this._function_name(data)
        if hasattr(this, name):
            param = {"key": None, "value": data, "level": 0, "last": True}
            getattr(this,name)(**param)

        l = len(str(this.line))
        l = 3 if l < 3 else l
        line_num = '%%-%dd' % l
        for d in this.texts:
            lines = this.texts[d]
            row = lines['level'] * this.space + lines['text']
            if is_number:
                print '%s%s' % (line_num % d, row)
            else:
                print row

    def _print_int(self, key='', value=0, level=0, **kwargs):

        if key is None:
            text = '%d' % value
        else:
            text = '"%s": %d' % (key, value)
        self._add_line(text, level=level, **kwargs)

    def _print_long(self, key='', value=0, level=0, **kwargs):

        if key is None:
            text = '%dl' % value
        else:
            text = '"%s": %dl' % (key, value)
        self._add_line(text, level=level, **kwargs)

    def _print_bool(self, key='', value=0, level=0, **kwargs):

        if key is None:
            text = '%s' % value
        else:
            text = '"%s": %s' % (key, value)
        self._add_line(text, level=level, **kwargs)

    def _print_float(self, key='', value=0l, level=0, **kwargs):

        if key is None:
            text = '%d' % value
        else:
            text = '"%s": %d' % (key, value)
        self._add_line(text, level=level, **kwargs)

    def _print_str(self, key='', value='', level=0, **kwargs):
        if key is None:
            text = '%s' % value
        else:
            text = '"%s": "%s"' % (key, value)
        self._add_line(text, level=level, **kwargs)

    def _print_unicode(self, key='', value=u'', level=0, **kwargs):
        if key is None:
            text = '%s' % value
        else:
            text = '"%s": "%s"' % (key, value)
        self._add_line(text, level=level, **kwargs)

    def _print_list(self, key='', value=[], level=0, **kwargs):
        if key is None:
            text = '['
        else:
            text = '"%s": [' % key
        self._set_line_num()
        self.texts[self.line] = dict(level=level, text=text)
        _level = level + 1

        l = len(value)
        for i, v in enumerate(value, start=1):
            name = self._function_name(v)
            if hasattr(self, name):
                _param = self._special_line(i, l)
                param = {"key": None, "value": v, "level": _level}
                param.update(_param)
                getattr(self, name)(**param)

        text = ']'
        self._add_line(text, level=level, **kwargs)

    def _print_dict(self, key=None, value={}, level=0, is_newline=True, **kwargs):
        if isinstance(value, dict):
            self_level = level if is_newline else 0
            if key is None:
                text = '{'
            else:
                text = '"%s": {' % key
            self._set_line_num()
            self.texts[self.line] = dict(level=self_level, text=text)
            _level = level + 1
            l = len(value)
            for i, k in enumerate(value, start=1):
                v = value[k]
                name = self._function_name(v)
                if hasattr(self, name):
                    _param = self._special_line(i, l)
                    param = {"key": k, "value": v, "level": _level}
                    param.update(_param)
                    getattr(self, name)(**param)
            text = '}'
            self._add_line(text, level=level, **kwargs)

    def _function_name(self, obj):
        print_function_type = (int, long, float, bool, list, dict, str, unicode)
        name = obj.__class__.__name__
        if isinstance(obj, print_function_type):
            for _type in print_function_type:
                if isinstance(obj, _type):
                    name = _type.__name__
                    break
        else:
            name = str.__name__

        return '_print_%s' % name

if __name__ == '__main__':

    d = {"canvas":{"width":90,"height":54,"hasRadius":False,"blood":1,"limit":3},"elements":[{"type":"diy_text","index":"0","align":"left","center_x":517.5,"center_y":298,"width":173,"height":58,"left":432,"top":269,"rotate":"0","content":"蔡宜凌","family":"yahei.ttf","size":14,"color":"121,77,27","cmyk":"0,36,78,53","bold":"0","italic":"0","underline":"0","mean":"username","text_align":"left"},{"type":"diy_text","index":1,"align":"left","center_x":688,"center_y":312,"width":100,"height":26,"left":638,"top":300,"rotate":"0","content":"销售主任","family":"yahei.ttf","size":6,"color":"121,77,27","cmyk":"0,36,78,53","bold":"0","italic":"0","underline":"0","mean":"job","text_align":"left"},{"type":"diy_text","index":2,"align":"left","center_x":509.5,"center_y":358.5,"width":155,"height":17,"left":433,"top":351,"rotate":"0","content":"Tel:1824455665","family":"yahei.ttf","size":5,"color":"121,77,27","cmyk":"0,36,78,53","bold":"0","italic":"0","underline":"0","mean":"telphone","text_align":"left"},{"type":"diy_text","index":3,"align":"left","center_x":637.5,"center_y":474,"width":407,"height":22,"left":434,"top":463,"rotate":"0","content":"地址：中国台湾台北市光复北路11巷35号6F","family":"yahei.ttf","size":5,"color":"119,90,36","cmyk":"0,24,70,53","bold":"0","italic":"0","underline":"0","mean":"address","text_align":"left"},{"type":"diy_text","index":4,"align":"left","center_x":570.5,"center_y":389,"width":271,"height":22,"left":436,"top":378,"rotate":"0","content":"Mail：cai10@zhubajie.com","family":"yahei.ttf","size":5,"color":"121,77,27","cmyk":"0,36,78,53","bold":"0","italic":"0","underline":"0","mean":"email","text_align":"left"}],"background":{"type":"diy_background","index":-1,"align":"left","key":"0000000509.jpg","color":"#FFFFFF","src":"http://img1.kywcdn.com/0/000/000/rgb-0000000509.jpg","dpi":["300","300"]}}
    # pj = PrintJson()
    # pj.print_json(d)

    PrintJson.print_json(d)