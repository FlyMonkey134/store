# -*- coding:utf8 -*-
import uuid


class ShopCartCookiesMiddleware(object):

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        response = self.get_response(request)

        if not request.COOKIES.get('my_session'):
            # request.COOKIES['my_session'] = str(uuid.uuid4())

            response.set_cookie('my_session',str(uuid.uuid4()))
            print(request.COOKIES)
        return response