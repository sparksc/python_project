# -*- coding: utf-8 -*-
"""
    yinsho.api
    ##################
    yinsho api application package
"""

#from gevent import monkey;monkey.patch_all()
import os, sys, uuid
import logging
import traceback
from logging.handlers import RotatingFileHandler,TimedRotatingFileHandler
from flask import Flask,jsonify,flash,request, current_app, g, session as web_session
from functools import wraps
from datetime import timedelta

from ..base.extensions  import db_session #, socketio
from ..base.helpers import JSONEncoder
from ..base import settings, factory

from ..services import UsersService


def create_app():
    app = factory.create_app(__name__,__path__)

    configure_before_handlers(app)
    configure_extensions(app)

    app.json_encoder = JSONEncoder
    return app

usersService = UsersService()

def route(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)


    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            result = {}

            try:
                token = request.headers.get('x-session-token')
                if not token or not usersService.auth(token):
                    sc = 401
                    raise Exception("登录超时，请重新登录！")
                # usersService.auth(token)
            except Exception as e:
                sc = 401
                result = { "error":e[0] } #), "status_code":e[0] }
                return jsonify(result), sc

            user_name = g.web_session.user.user_name
            print request.url

            try:
                if usersService.is_init_password(user_name):
                    sc = 461
                    raise Exception(u'请修改初始密码,防止密码泄漏!')
            except Exception as e:
                current_app.logger.error(traceback.format_exc())
                result = { "error":e[0] } #), "status_code":e[0] }
                return jsonify(result), sc

            try:

                rv = f(*args, **kwargs)
                if isinstance(rv, tuple):
                    sc = rv[1]
                    rv = rv[0]
                result = dict(
                    data=rv
                )

                g.db_session.commit()
            except Exception as e:
                current_app.logger.exception("Exception Logged")
                sc = 500
                result = { "error":e[0] } #), "status_code":e[0] }
                try:
                    if g.db_session :g.db_session.rollback()
                except Exception,e1:
                    traceback.print_exc()
            return jsonify(result), sc
        return f

    return decorator

def configure_extensions(app):
    #socketio.init_app(app)
    pass


def configure_before_handlers(app):

    @app.before_request
    def before_request():
        g.db_session = db_session
        #web_session.permanent = True
        #app.permanent_session_lifetime = timedelta(hours=5)
        token = request.headers.get('x-session-token')
        if token:
            try:
                user_session = usersService.auth(token)
                if user_session:
                    g.web_session = user_session
            except Exception as e:
                current_app.logger.exception("Exception Logged")
                sc = 401
                result = { "error":e[0] } #), "status_code":e[0] }
                return jsonify(result), sc

    @app.after_request
    def after_request(response):
        try:
            if g.db_session : g.db_session.remove()
        except Exception,e:
            traceback.print_exc()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,x-session-token')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    @app.teardown_request
    def teardown_request(exception):
        pass
        #if g.db_session :
        #    g.db_session.commit()
        #    g.db_session.close()

app = create_app()




