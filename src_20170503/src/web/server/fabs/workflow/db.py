# -*- coding:utf-8 -*-
import logging
session=None
def set_session(s):
    global session
    logging.debug("%s"%str(session))
    session=s
    logging.debug("after %s"%str(session))
def get_session():
    logging.debug("get %s"%str(session))
    return session
