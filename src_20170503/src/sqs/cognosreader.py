#-*- coding:utf-8 -*-
import xml.sax
import xml.sax.handler
import httplib
import json
import traceback
import cookielib
import zlib
import urllib
import urllib2
import re
from singleton import *
import utils

@singleton
class CognosReader():
    def __init__(self,debug=False):
        self.httpHandler = urllib2.HTTPHandler(debuglevel = debug)
        self.cookie = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(self.httpHandler,urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(self.opener)
        self.init_base_headers()
        self.seen_context = {}

    def init_base_headers(self):
        self.base_headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'192.168.100.39',
            'Upgrade-Insecure-Requests':1,
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
            }

    def content_request(self, url):
        request = urllib2.Request(url,'',self.base_headers)
        response = self.opener.open(request)
        return self.parse_response(response)

    def context_request(self, url):
        ctx_cookie = self.get_context(url)
        if ctx_cookie is not None:
            self.cookie = ctx_cookie
        request = urllib2.Request(url,'',self.base_headers)
        response = self.opener.open(request)
        self.save_context(response)
        return response

    def save_context(self,response):
        async_url = response.geturl()
        session_id = utils.get_session_key(async_url)
        self.seen_context[session_id] = self.cookie

    def get_context(self,url):
        session_id = utils.get_session_key(url)
        return self.seen_context.get(session_id)
    
    def parse_response(self,response):
        content = response.read()
        gzipped = response.headers.get('Content-Encoding')
        if gzipped:
            dec_content = zlib.decompress(content, 16+zlib.MAX_WBITS)
            content = dec_content.decode('gbk')
        return content

    def get_message(self, url):
        content = self.content_request(url)
        return content