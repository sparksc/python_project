# -*- coding: utf-8 -*-
"""
    yinsho.base.extensions
    ##################
    yinsho extensions module
"""
from ..database import scope_session
#from flask.ext.socketio import SocketIO


db_session = scope_session()
#socketio = SocketIO()
