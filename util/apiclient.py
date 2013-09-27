# -*- coding: utf-8 -*-
import collections
import gzip
import urllib
import urllib2

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    import json
except ImportError:
    import simplejson as json


__author__ = 'myth'


_HTTP_GET = 1
_HTTP_POST = 2
# 超时时间（秒）
TIMEOUT = 30
RETURN_TYPE = {"json": 0, "xml": 1, "html": 2, "text": 3}
_METHOD_MAP = {'GET': _HTTP_GET, 'POST': _HTTP_POST}


class APIError(StandardError):
    """
    raise APIError if receiving json message indicating failure.
    """
    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        StandardError.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code, self.error, self.request)


def callback_type(return_type='json'):

    default_type = "json"
    default_value = RETURN_TYPE.get(default_type)
    if return_type:
        if isinstance(return_type, (str, unicode)):
            default_value = RETURN_TYPE.get(return_type.lower(), default_value)
    return default_value


def _encode_params(**kw):
    """
    do url-encode parameters

    >>> _encode_params(a=1, b='R&D')
    'a=1&b=R%26D'
    >>> _encode_params(a=u'\u4e2d\u6587', b=['A', 'B', 123])
    'a=%E4%B8%AD%E6%96%87&b=A&b=B&b=123'
    """
    args = []
    for k, v in kw.iteritems():
        if isinstance(v, basestring):
            qv = v.encode('utf-8') if isinstance(v, unicode) else v
            args.append('%s=%s' % (k, urllib.quote(qv)))
        elif isinstance(v, collections.Iterable):
            for i in v:
                qv = i.encode('utf-8') if isinstance(i, unicode) else str(i)
                args.append('%s=%s' % (k, urllib.quote(qv)))
        else:
            qv = str(v)
            args.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(args)


def _read_body(obj):
    using_gzip = obj.headers.get('Content-Encoding', '') == 'gzip'
    body = obj.read()
    if using_gzip:
        gzipper = gzip.GzipFile(fileobj=StringIO(body))
        fcontent = gzipper.read()
        gzipper.close()
        return fcontent
    return body


class JsonDict(dict):
    """
    general json object that allows attributes to be bound to and also behaves like a dict
    """

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value


def _parse_json(s):
    """
    parse str into JsonDict
    """

    def _obj_hook(pairs):
        """
        convert json object to python object
        """
        o = JsonDict()
        for k, v in pairs.iteritems():
            o[str(k)] = v
        return o
    return json.loads(s, object_hook=_obj_hook)


def _parse_xml(s):
    """
    parse str into xml
    """

    raise NotImplementedError()


def _parse_html(s):
    """
    parse str into html
    """

    raise NotImplementedError()


def _parse_text(s):
    """
    parse str into text
    """

    raise NotImplementedError()


def _http_call(the_url, method, return_type="json", request_suffix=None, **kwargs):
    """
    the_url: 请求地址
    method 请求方法（get，post）
    return_type： 返回格式解析
    request_suffix： 请求地址的后缀，如jsp，net
    kwargs: 请求参数
    """

    params = _encode_params(**kwargs)
    http_url = "%s.%s" (the_url, request_suffix) if request_suffix else the_url
    http_url = '%s?%s' % (http_url, params) if method == _HTTP_GET else http_url
    print http_url
    http_body = None if method == _HTTP_GET else params
    req = urllib2.Request(http_url, data=http_body)

    callback = globals().get('_parse_{0}'.format(return_type))
    if not hasattr(callback, '__call__'):
        print "return '%s' unable to resolve" % return_type
        callback = _parse_json
    try:

        resp = urllib2.urlopen(req, timeout=TIMEOUT)
        body = _read_body(resp)
        r = callback(body)
        if hasattr(r, 'error_code'):
            raise APIError(r.error_code, r.get('error', ''), r.get('request', ''))
        return r
    except urllib2.HTTPError, e:
        try:
            body = _read_body(e)
            r = callback(body)
        except:
            r = None
        if hasattr(r, 'error_code'):
            raise APIError(r.error_code, r.get('error', ''), r.get('request', ''))
        raise e


class HttpObject(object):

    def __init__(self, client, method):
        self.client = client
        self.method = method

    def __getattr__(self, attr):

        def wrap(**kw):
            if attr:
                the_url = '%s/%s' % (self.client.api_url, attr.replace('__', '/'))
            else:
                the_url = self.client.api_url
            return _http_call(the_url, self.method, **kw)
        return wrap


class APIClient(object):
    """
    使用方法：
        比如：api 请求地址为：http://api.open.zbjdev.com/kuaiyinserv/kuaiyin/billaddress
             请求方式为： GET
             需要的参数为：user_id 用户的UID
                         is_all 是否查询所有数据，0为默认邮寄地址 1为全部邮寄地址
                         access_token 平台认证
             返回数据为：json

        那么此时使用如下：
        domain = "api.open.zbjdev.com"
        #如果是https请求，需要将is_https设置为True
        client = APIClient(domain)
        data = {"user_id": "14035462", "is_all": 1, "access_token": "a856e0c38c7009b40eb71da692a38519e6f2487b"}
        # 如果是post请求，请将get方法改为post方法
        result = client.kuaiyinserv.kuaiyin.billaddress.get(return_type="json", **data)
        #等同于
        # result = client.kuaiyinserv__kuaiyin__billaddress__get(return_type="json", **data)
        # result = client.kuaiyinserv__kuaiyin__billaddress(return_type="json", **data)
    """

    def __init__(self, domain, is_https=False):

        http = "http"
        if domain.startswith("http://") or domain.startswith("https://"):
            http, domain = domain.split("://")
        else:
            if is_https:
                http = "https"

        self.api_url = ('%s://%s' % (http, domain)).rstrip("/")
        self.get = HttpObject(self, _HTTP_GET)
        self.post = HttpObject(self, _HTTP_POST)

    def __getattr__(self, attr):
        if '__' in attr:

            method = self.get
            if attr[-6:] == "__post":
                attr = attr[:-6]
                method = self.post

            elif attr[-5:] == "__get":
                attr = attr[:-5]

            if attr[:2] == '__':
                attr = attr[2:]
            return getattr(method, attr)
        return _Callable(self, attr)


class _Executable(object):

    def __init__(self, client, method, path):
        self._client = client
        self._method = method
        self._path = path

    def __call__(self, **kw):
        method = _METHOD_MAP[self._method]
        return _http_call('%s/%s' % (self._client.api_url, self._path), method, **kw)

    def __str__(self):
        return '_Executable (%s %s)' % (self._method, self._path)

    __repr__ = __str__


class _Callable(object):

    def __init__(self, client, name):
        self._client = client
        self._name = name

    def __getattr__(self, attr):
        if attr == 'get':
            return _Executable(self._client, 'GET', self._name)
        if attr == 'post':
            return _Executable(self._client, 'POST', self._name)
        name = '%s/%s' % (self._name, attr)
        return _Callable(self._client, name)

    def __str__(self):
        return '_Callable (%s)' % self._name

    __repr__ = __str__


def test_APIClient():

    # import doctest
    # doctest.testmod()

    domain = "api.open.zbjdev.com"

    #如果是https请求，需要将is_https设置为True
    client = APIClient(domain)
    data = {"user_id": "14035462", "is_all": 1, "access_token": "4c0aa52e4baf39f1b348f79b9b804aa906fef34d"}
    # 如果是post请求，请将get方法改为post方法
    # print client.kuaiyinserv__kuaiyin__billaddress(return_type="json", **data)
    # print client.kuaiyinserv__kuaiyin__billaddress__get(return_type="json", **data)

    print "test ---------------------- 1"
    result = client.kuaiyinserv__kuaiyin__billaddress__post(return_type="json", **data)
    print result

    print "test ---------------------- 2"
    result = client.kuaiyinserv.kuaiyin.billaddress.post(return_type="json", **data)
    print result

    domain = "api.open.zbjdev.com/kuaiyinserv/kuaiyin/billaddress"
    client = APIClient(domain)
    print "test ---------------------- 3"
    result = client.__post(return_type="json", **data)
    print result


def test_logistics():

    domain = "https://api.kuaidi100.com/api"

    #如果是https请求，需要将is_https设置为True
    client = APIClient(domain)

    data = {"id": "45f2d1f2sds", "com": "yunda", "nu": "1500066330925"}
    result = client.__get(**data)
    print result
    print result["message"]
    print result.get("message")
    print result.message

if __name__ == '__main__':

    # test_APIClient()

    test_logistics()