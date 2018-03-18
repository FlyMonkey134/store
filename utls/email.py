# -*- coding:utf8 -*-

from django.core.mail import send_mail
from account.models import MailRecord
from django.conf import settings
import uuid

def register_mail(user):
    mail = MailRecord()
    mail.user = user
    mail.code = uuid.uuid4()
    mail.email = 0
    mail.save()

    url = u'http://118.31.42.54:8000/account/activation/?code=%s' % mail.code
    subject = u'账号注册'
    html_message = u'<a href="%s">欢迎注册</a>' % url
    from_email = settings.EMAIL_FROM
    send_mail(subject,'',from_email,[user.email],html_message=html_message)
    print(u'邮件发送成功')