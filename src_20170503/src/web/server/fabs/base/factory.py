# -*- coding: utf-8 -*-
"""
    yinsho.base.facotry
    ##################
    yinsho factory module
"""

#from gevent import monkey;monkey.patch_all()
import os, sys, uuid
import logging
from logging.handlers import RotatingFileHandler,TimedRotatingFileHandler
from flask import Flask,jsonify, g #,flash,request,session,url_for,make_response,redirect
import settings

from .middleware import HTTPMethodOverrideMiddleware
from .helpers import configure_blueprints
from .extensions import db_session




def create_app(package_name, package_path):

    app = Flask(__name__)
    config = get_configuration()
    configure_app(app, config)
    #configure_error_handlers(app)
    configure_logging(app)
    #configure_extensions(app)
    configure_blueprints(app, package_name, package_path)

    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    return app



def get_configuration():
    mode = os.environ.get('MODE')
    try:
        if mode == 'PRODUCTION':
            from .settings import ProdConfig
            return ProdConfig
        elif mode == 'TESTING':
            from .settings import TestConfig
            return TestConfig
        else:
            from .settings import DevConfig
            return DevConfig
    except ImportError, e:
        from .setting import Config
        return Config

def configure_app(app, config=None):

    app.config.from_object(config)
    #app.config.from_envvar('APP_CONFIG', silent=True)


def configure_error_handlers(app):

    @app.errorhandler(404)
    def request_not_found(error):
        return jsonify(error=('Sorry, request not found'))

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify(error=('Sorry, not allowed'))

    @app.errorhandler(Exception)
    @app.errorhandler(500)
    def server_error(error):
        return jsonify(error=('Sorry, an error has occurred'))


    @app.errorhandler(400) #ERR::BAD REQUEST
    @app.errorhandler(401) #ERR::UNAUTHORIZED
    def unauthorized(error):
        return jsonify(error=("Login required")),401


def configure_logging(app):

    debug_log = os.path.join(app.root_path, app.config['DEBUG_LOG'])
    debug_file_handler = RotatingFileHandler(debug_log, maxBytes=10000000, backupCount=1,encoding='utf8')

    debug_file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(app.config['FORMATTER_LOG'] )
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(app.root_path, app.config['ERROR_LOG'])

    error_file_handler = RotatingFileHandler(error_log, maxBytes=10000000, backupCount=1, encoding='utf8')

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)




