# -*- coding: utf-8 -*-
"""
    yinsho.base.helpers
    ~~~~~~~~~~~~~~~~
    yinsho helpers module
"""

import pkgutil
import importlib
import datetime
import collections
import hashlib
import uuid
import json
from sqlalchemy import Numeric
from flask import Blueprint
from flask.json import JSONEncoder as BaseJSONEncoder

from sqlalchemy.ext.declarative import DeclarativeMeta

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


def configure_blueprints(app, package_name, package_path):
    """Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.
    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    """
    rv = []
    pkgs = ["teller_Volume_Adjust","countexam_basevol_hander","hall_manager_hander","counter_fine_amount","ebills_manager","branch_funong_card","international_level","burank","bank_pe_input","handmain","chooseservice","delegate_hand","delegate_form","account_form","account_rank","user_level","user_extrascore","insurance","addharvest","branch_grade_report","org_level","teller_level","man_gradejdg","staff_count_input","staff_sal_input","staff_sal_hzinput", "village_input","atm_input","loan_efile_input","dkkhxdh","cdgggx","monsalary","idda","adjusttype","tpara","position","staffrelation","basicsalary","gsgxck","depappoint","users","permission","nxmanagement","net","performance","targetpermission","contract_check","con_check","branchmanagepermission","bgu","parameterpermission","hand_input","bank_input","parasetpermission","dkgsgxxzpermission","pos_input","large_loss","dictdata","eduallowance","bgs","reportmag","accthk","custhk","custHookMag","dep_stock_mtf_input","manaddsco", "mbox", "postmanagepermission","ebank_replace"]
    for _, name, _ in pkgutil.iter_modules(package_path):
        if name in pkgs:
            m = importlib.import_module('%s.%s' % (package_name, name))
            for item in dir(m):
                item = getattr(m, item)
                if isinstance(item, Blueprint):
                    app.register_blueprint(item)
                rv.append(item)
    return rv


class JSONEncoder(BaseJSONEncoder):
    """Custom :class:`JSONEncoder` which respects objects that include the
    :class:`JsonSerializer` mixin.
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
        elif hasattr(obj, 'asdict') and callable(getattr(obj, 'asdict')):
            return obj.asdict()
        #elif isinstance(obj, collections.Mapping):
        #    return dict(map(convert, obj.iteritems()))
        elif isinstance(obj, collections.Iterable):
            return type(obj)(map(convert, obj))
	#elif isinstance(obj,Numeric):
	 #   return float(obj)
        elif isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x not in ['metadata', 'query', 'query_class']]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.strftime('%Y-%m-%dT%H:%M:%S')
                    elif isinstance(data, datetime.date):
                        fields[field] = data.strftime('%Y-%m-%d')
                    elif isinstance(data, datetime.time):
                        fields[field] = data.strftime('%H:%M:%S')
                    else:
                        fields[field] = None
            # a json-encodable dict
            return fields
        else:
            return super(JSONEncoder, self).default(obj)




class JsonSerializer(object):
    """A mixin that can be used to mark a SQLAlchemy model class which
    implements a :func:`to_json` method. The :func:`to_json` method is used
    in conjuction with the custom :class:`JSONEncoder` class. By default this
    mixin will assume all properties of the SQLAlchemy model are to be visible
    in the JSON output. Extend this class to customize which properties are
    public, hidden or modified before being being passed to the JSON serializer.
    """

    __json_public__ = None
    __json_hidden__ = None
    __json_modifiers__ = None

    def get_field_names(self):
        for p in self.__mapper__.iterate_properties:
            yield p.key

    def to_json(self):
        field_names = self.get_field_names()

        public = self.__json_public__ or field_names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()

        rv = dict()
        for key in public:
            rv[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            value = getattr(self, key)
            rv[key] = modifier(value, self)
        for key in hidden:
            rv.pop(key, None)
        return rv


def format_date(obj,pattern='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(obj,pattern)

def format_str(obj,pattern='%Y-%m-%d %H:%M:%S'):
    if isinstance(obj,datetime.datetime):
        return obj.strftime(pattern)
    return obj

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

def req_parse(items,modifiers):
    ditems = dict([(k, v) for k, v in items])
    format_warp(ditems,modifiers)
    return ditems

def req_parse1(items,modifiers):
    ditems = dict([(k, v) for k, v in items])
    format_warp(ditems,modifiers)
    return ditems

def format_warp(items,modifiers):
    for key ,value in items.items():
        if key in modifiers.keys():
            items[key] = modifiers.get(key)(value,items)


def encrypt(password):
    return hashlib.md5(password).hexdigest().upper()

def generate_uuid():
    return uuid.uuid1().hex.upper()


def generate_auth_token(secret_key, uid, expiration = 600):
    s = Serializer(secret_key, expires_in = expiration)
    return s.dumps({ 'id': uid })

def get_auth_id(secret_key,token):
    s = Serializer(secret_key)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    return data['id']



