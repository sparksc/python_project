# -*- coding:utf-8 -*-
from .configure import Configure
import time


class WebSession(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(WebSession, cls).__new__(cls, *args, **kwargs)
            cls._instance._session = {}
        return cls._instance

    def __init__(self):
        self.load_config();

    def load_config(self):
        with Configure() as cfg:
            self.session_time = cfg['session_time']

    def display(self):
        pass

    def add(self, sid):
        self._session.update({sid: time.time()})

    def remove(self, sid):
        if sid in self._session:
            self._session.pop(sid)

    def is_exist(self, sid):
        print sid
        if self._session.has_key(sid):
            old_time = self._session[sid]
            now_time = time.time()
            if now_time - old_time > self.session_time:
                self._session.pop(sid)
                return False
            self._session.update({sid:now_time})
            return True
        return False
        
    def has_login(self, request):
        if not request.cookies.has_key('sid') or not websession.is_exist(request.cookies['sid'].value):
            return False
        return True

websession = WebSession()
