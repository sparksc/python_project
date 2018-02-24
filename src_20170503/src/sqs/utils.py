#-*- coding:utf-8 -*-

import re

def get_session_key(url):
    match = re.search(r"(?P<session_id>\b[A-F0-9]{8}(?:-[A-F0-9]{4}){3}-[A-Z0-9]{12}\b)", url, re.IGNORECASE)
    if match:
        session_id = match.group("session_id")
    else:
        session_id = None
    return session_id

def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            v.decode('utf8')
        out_dict[k] = v
    return out_dict