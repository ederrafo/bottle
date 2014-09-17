# -*- coding: utf-8 -*-
# from contextlib import contextmanager
from email.encoders import encode_base64
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid, formatdate, formataddr, parseaddr
import smtplib
import sys
# import blinker
import time

__author__ = 'myth'

PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
    text_type = str
else:
    string_types = basestring,
    text_type = unicode


class Message(object):
    """Encapsulates an email message.

    :param subject: 邮件标题
    :param recipients: 电子邮件地址列表
    :param body: 纯文本邮件
    :param html: HTML邮件
    :param sender: 电子邮件发件人地址
    :param cc: 抄送列表
    :param bcc: 密送列表
    :param attachments: 附件实例列表
    :param reply_to: 回复地址
    :param date: 发送日期
    :param charset: 消息的字符集
    :param extra_headers: 额外的标头信息的字典
    :param mail_options: 一个在MAIL FROM命令中使用的ESMTP选项列表
    :param rcpt_options:  在一个RCPT命令中使用的ESMTP选项列表
    """

    def __init__(self, subject=None,
                 recipients=None,
                 body=None,
                 html=None,
                 sender=None,
                 cc=None,
                 bcc=None,
                 attachments=None,
                 reply_to=None,
                 date=None,
                 charset=None,
                 extra_headers=None,
                 mail_options=None,
                 rcpt_options=None):

        sender = sender

        if isinstance(sender, tuple):
            sender = "%s <%s>" % sender

        self._recipients = recipients or []
        self.subject = subject
        self.sender = sender
        self.reply_to = reply_to
        self._cc = cc or []
        self._bcc = bcc or []
        self.body = body
        self.html = html
        self.date = date
        self.msgId = make_msgid()
        self.charset = charset
        self.extra_headers = extra_headers
        self.mail_options = mail_options or []
        self.rcpt_options = rcpt_options or []
        self.attachments = attachments or []

    @property
    def recipients(self):

        if not isinstance(self._recipients, (list, set, tuple)):
            return [self._recipients]
        return self._recipients

    @recipients.setter
    def recipients(self, value):
        self._recipients = value or []

    @property
    def cc(self):

        if not isinstance(self._cc, (list, set, tuple)):
            return [self._cc]
        return self._cc

    @cc.setter
    def cc(self, value):
        self._cc = value or []

    @property
    def bcc(self):

        if not isinstance(self._bcc, (list, set, tuple)):
            return [self._bcc]
        return self._bcc

    @bcc.setter
    def bcc(self, value):
        self._bcc = value or []

    @property
    def send_to(self):
        """
        返回电子邮件地址列表
        """
        return set(self.recipients) | set(self.bcc or ()) | set(self.cc or ())

    def _mimetext(self, text, subtype='plain'):
        """
        Creates a MIMEText object with the given subtype (default: 'plain')
        If the text is unicode, the utf-8 charset is used.
        """
        charset = self.charset or 'utf-8'
        return MIMEText(text, _subtype=subtype, _charset=charset)

    def as_string(self):
        """
        创建电子邮件
        """

        attachments = self.attachments or []

        if len(attachments) == 0 and not self.html:
            # No html content and zero attachments means plain text
            msg = self._mimetext(self.body)
        elif len(attachments) > 0 and not self.html:
            # No html and at least one attachment means multipart
            msg = MIMEMultipart()
            msg.attach(self._mimetext(self.body))
        else:
            # Anything else
            msg = MIMEMultipart()
            alternative = MIMEMultipart('alternative')
            alternative.attach(self._mimetext(self.body, 'plain'))
            alternative.attach(self._mimetext(self.html, 'html'))
            msg.attach(alternative)

        msg['Subject'] = self.subject
        msg['From'] = sanitize_address(self.sender)
        msg['To'] = ', '.join(list(set(sanitize_addresses(self.recipients))))

        msg['Date'] = formatdate(self.date, localtime=True)
        # see RFC 5322 section 3.6.4.
        msg['Message-ID'] = self.msgId

        if self.cc:
            msg['Cc'] = ', '.join(list(set(sanitize_addresses(self.cc))))

        if self.reply_to:
            msg['Reply-To'] = sanitize_address(self.reply_to)

        if self.extra_headers:
            for k, v in self.extra_headers.items():
                msg[k] = v

        for attachment in attachments:
            f = MIMEBase(*attachment.content_type.split('/'))
            f.set_payload(attachment.data)
            encode_base64(f)

            try:
                attachment.filename and attachment.filename.encode('ascii')
            except UnicodeEncodeError:
                filename = attachment.filename
                if not PY3:
                    filename = filename.encode('utf8')
                f.add_header('Content-Disposition', attachment.disposition,
                            filename=('UTF8', '', filename))
            else:
                f.add_header('Content-Disposition', '%s;filename=%s' %
                             (attachment.disposition, attachment.filename))

            for key, value in attachment.headers:
                f.add_header(key, value)

            msg.attach(f)

        return msg.as_string()

    def __str__(self):
        return self.as_string()

    def has_bad_headers(self):
        """Checks for bad headers i.e. newlines in subject, sender or recipients.
        """

        reply_to = self.reply_to or ''
        for val in [self.subject, self.sender, reply_to] + self.recipients:
            for c in '\r\n':
                if c in val:
                    return True
        return False

    def is_bad_headers(self):
        from warnings import warn
        msg = 'is_bad_headers is deprecated, use the new has_bad_headers method instead.'
        warn(DeprecationWarning(msg), stacklevel=1)
        return self.has_bad_headers()

    def send(self, connection):
        """Verifies and sends the message."""

        return connection.send(self)

    def add_recipient(self, recipient):
        """Adds another recipient to the message.

        :param recipient: email address of recipient.
        """

        self.recipients.append(recipient)

    def attach(self,
               filename=None,
               content_type=None,
               data=None,
               disposition=None,
               headers=None):
        """Adds an attachment to the message.

        :param filename: filename of attachment
        :param content_type: file mimetype
        :param data: the raw file data
        :param disposition: content-disposition (if any)
        """
        self.attachments.append(
            Attachment(filename, content_type, data, disposition, headers))


class Attachment(object):
    """Encapsulates file attachment information.

    :versionadded: 0.3.5

    :param filename: filename of attachment
    :param content_type: file mimetype
    :param data: the raw file data
    :param disposition: content-disposition (if any)
    """

    def __init__(self, filename=None, content_type=None, data=None,
                 disposition=None, headers=None):
        self.filename = filename
        self.content_type = content_type
        self.data = data
        self.disposition = disposition or 'attachment'
        self.headers = headers or {}


class BadHeaderError(Exception):
    pass


class MailUnicodeDecodeError(UnicodeDecodeError):
    def __init__(self, obj, *args):
        self.obj = obj
        UnicodeDecodeError.__init__(self, *args)

    def __str__(self):
        original = UnicodeDecodeError.__str__(self)
        return '%s. You passed in %r (%s)' % (original, self.obj, type(self.obj))


class _MailMixin(object):

    # @contextmanager
    # def record_messages(self):
    #     """Records all messages. Use in unit tests for example::
    #
    #         with mail.record_messages() as outbox:
    #             response = app.test_client.get("/email-sending-view/")
    #             assert len(outbox) == 1
    #             assert outbox[0].subject == "testing"
    #
    #     You must have blinker installed in order to use this feature.
    #     :versionadded: 0.4
    #     """
    #
    #     if not email_dispatched:
    #         raise RuntimeError("blinker must be installed")
    #
    #     outbox = []
    #
    #     def _record(message, app):
    #         outbox.append(message)
    #
    #     email_dispatched.connect(_record)
    #
    #     try:
    #         yield outbox
    #     finally:
    #         email_dispatched.disconnect(_record)

    def send(self, message):
        """Sends a single message instance. If TESTING is True the message will
        not actually be sent.

        :param message: a Message instance.
        """

        with self.connect() as connection:
            reulst = message.send(connection)
        return reulst

    def send_message(self, *args, **kwargs):
        """Shortcut for send(msg).

        Takes same arguments as Message constructor.

        :versionadded: 0.3.5
        """

        self.send(Message(*args, **kwargs))

    def connect(self):
        """Opens a connection to the mail host."""
        try:
            return Connection(self.config)
        except KeyError:
            raise RuntimeError("The curent application was not configured with Mail")


class _Mail(object):
    def __init__(self, server, username, password, port, use_tls, use_ssl,
                 default_sender, debug, max_emails, suppress, timeout=None):
        self.server = server
        self.username = username
        self.password = password
        self.port = port
        self.use_tls = use_tls
        self.use_ssl = use_ssl
        self.default_sender = default_sender
        self.debug = debug
        self.max_emails = max_emails
        self.suppress = suppress
        self.timeout = timeout or 30


class Mail(_MailMixin):
    """Manages email messaging

    :param app: Flask instance
    """

    def __init__(self, config=None):
        if config is not None:
            self.config = self.init_config(config)
        else:
            self.config = None

    def init_config(self, config):
        """Initializes your mail settings from the application settings.

        You can use this if you want to set up your Mail instance
        at configuration time.

        :param app: Flask application instance
        """

        state = _Mail(
            config.get('MAIL_SERVER', '127.0.0.1'),
            config.get('MAIL_USERNAME'),
            config.get('MAIL_PASSWORD'),
            config.get('MAIL_PORT', 25),
            config.get('MAIL_USE_TLS', False),
            config.get('MAIL_USE_SSL', False),
            config.get('MAIL_DEFAULT_SENDER'),
            int(config.get('MAIL_DEBUG', False)),
            config.get('MAIL_MAX_EMAILS'),
            config.get('MAIL_SUPPRESS_SEND'),
            config.get('TIMEOUT'))

        return state

    def check_account(self):
        connect = self.connect()
        smtp = connect._init_smtp_server()
        try:
            print smtp.login(self.username, self.password)
        finally:
            if smtp:
                smtp.quit()

    def __getattr__(self, name):
        return getattr(self.config, name, None)


class Connection(object):
    """Handles connection to host."""

    def __init__(self, mail):
        self.mail = mail

    def __enter__(self):
        if self.mail.suppress:
            self.host = None
        else:
            self.host = self.configure_host()

        self.num_emails = 0

        return self

    def __exit__(self, exc_type, exc_value, tb):
        if self.host:
            self.host.quit()

    def _init_smtp_server(self):
        """
        初始化连接邮件服务器
        """
        if self.mail.use_ssl:
            host = smtplib.SMTP_SSL(self.mail.server, self.mail.port, timeout=self.mail.timeout)
        else:
            host = smtplib.SMTP(self.mail.server, self.mail.port, timeout=self.mail.timeout)
        return host

    def configure_host(self):
        # if self.mail.use_ssl:
        #     host = smtplib.SMTP_SSL(self.mail.server, self.mail.port)
        # else:
        #     host = smtplib.SMTP(self.mail.server, self.mail.port)
        host = self._init_smtp_server()

        host.set_debuglevel(int(self.mail.debug))

        if self.mail.use_tls:
            host.starttls()
        if self.mail.username and self.mail.password:
            host.login(self.mail.username, self.mail.password)

        return host

    def send(self, message, envelope_from=None):
        """Verifies and sends message.

        :param message: Message instance.
        :param envelope_from: Email address to be used in MAIL FROM command.
        """
        assert message.recipients, "No recipients have been added"

        assert message.sender, (
                "The message does not specify a sender and a default sender "
                "has not been configured")

        if message.has_bad_headers():
            raise BadHeaderError

        if message.date is None:
            message.date = time.time()

        if self.host:
            result = self.host.sendmail(sanitize_address(envelope_from or message.sender),
                                        message.send_to,
                                        message.as_string(),
                                        message.mail_options,
                                        message.rcpt_options)
        # email_dispatched.send(message)

        self.num_emails += 1

        if self.num_emails == self.mail.max_emails:
            self.num_emails = 0
            if self.host:
                self.host.quit()
                self.host = self.configure_host()
        return result

    def send_message(self, *args, **kwargs):
        """Shortcut for send(msg).

        Takes same arguments as Message constructor.

        :versionadded: 0.3.5
        """

        self.send(Message(*args, **kwargs))


def sanitize_addresses(addresses):
    return map(lambda e: sanitize_address(e), addresses)


def sanitize_address(addr, encoding='utf-8'):
    if isinstance(addr, string_types):
        addr = parseaddr(force_text(addr))
    nm, addr = addr

    try:
        nm = Header(nm, encoding).encode()
    except UnicodeEncodeError:
        nm = Header(nm, 'utf-8').encode()
    try:
        addr.encode('ascii')
    except UnicodeEncodeError:  # IDN
        if '@' in addr:
            localpart, domain = addr.split('@', 1)
            localpart = str(Header(localpart, encoding))
            domain = domain.encode('idna').decode('ascii')
            addr = '@'.join([localpart, domain])
        else:
            addr = Header(addr, encoding).encode()
    return formataddr((nm, addr))


def force_text(s, encoding='utf-8', errors='strict'):
    """
    Similar to smart_text, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    """
    if isinstance(s, text_type):
        return s

    try:
        if not isinstance(s, string_types):
            if hasattr(s, '__unicode__'):
                s = s.__unicode__()
            else:
                if PY3:
                    if isinstance(s, bytes):
                        s = text_type(s, encoding, errors)
                    else:
                        s = text_type(s)
                else:
                    s = text_type(bytes(s), encoding, errors)
        else:
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(s, Exception):
            raise MailUnicodeDecodeError(s, *e.args)
        else:
            s = ' '.join([force_text(arg, encoding, errors) for arg in s])
    return s


# signals = blinker.Namespace()
#
# email_dispatched = signals.signal("email-dispatched", doc="""
# Signal sent when an email is dispatched. This signal will also be sent
# in testing mode, even though the email will not actually be sent.
# """)


if __name__ == '__main__':
    msg = Message()
    msg.sender = 'wangyu@zhubajie.com'
    msg.recipients = '1446740010@qq.com'
    msg.cc = 'tt@qq.com'
    msg.subject = u'这是一个测试邮件'
    msg.body = u'邮件内容，text格式'

    # print msg.as_string()

    # config.get('MAIL_SERVER', '127.0.0.1'),
    #         config.get('MAIL_USERNAME'),
    #         config.get('MAIL_PASSWORD'),
    #         config.get('MAIL_PORT', 25),
    #         config.get('MAIL_USE_TLS', False),
    #         config.get('MAIL_USE_SSL', False),
    #         config.get('MAIL_DEFAULT_SENDER'),
    #         int(config.get('MAIL_DEBUG', False)),
    #         config.get('MAIL_MAX_EMAILS'),
    #         config.get('MAIL_SUPPRESS_SEND'))
    config = {
        "MAIL_SERVER": "smtp.exmail.qq.com",
        "MAIL_USERNAME": "wangyu@zhubajie.com",
        "MAIL_PASSWORD": "xxxxxx",
        "MAIL_PORT": 25, #465
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": False, #True
        "MAIL_DEFAULT_SENDER": "",
        "MAIL_DEBUG": True,
        "MAIL_MAX_EMAILS": '',
        "MAIL_SUPPRESS_SEND": "",
        "TIMEOUT": 5
    }

    mail = Mail(config)
    # connect = mail.connect()
    # smtp = connect._init_smtp_server()
    # print smtp.login('wangyu@zhubajie.com', 'wy14753698')
    # print smtp.verify('tt@qq.com')
    mail.check_account()
    result = mail.send(msg)
    print '#'*50
    # print result
