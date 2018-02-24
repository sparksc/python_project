# -*- coding:utf-8 -*-
from ..database import get_session
from ..model.transaction import ParameterString, ParameterInteger
import logging
from ..database.logger import *

#TODO:refactor

log = logging.getLogger(__name__)

def add_parameter(activity, name, value):
    session=get_session(activity)
    if isinstance(value, int):
        p=ParameterInteger(name=name, value=value, activity=activity)
    else:
        p=ParameterString(name=name, value=unicode(value), activity=activity)
    session.add(p)

def update_parameter(parameter, value):
    session=get_session(parameter)
    if (isinstance(value, int) and isinstance(parameter, ParameterInteger)) or (not isinstance(value, int) and isinstance(parameter, ParameterString)):
        parameter.value=value
    else:
        session.delete(parameter)
        add_parameter(parameter.activity, name, value)

def find_parameter(activity, name):
    for p in activity.parameter:
        if p.name==name:
            return p
    return None

def set_parameter(activity, name, value):
    p=find_parameter(activity, name)
    if p:
        update_parameter(p, value)
    else:
        add_parameter(activity, name, value)

def get_parameter(activity, name):
    p=find_parameter(activity, name)
    if p:
        return p.value
    else:
        raise Exception(u'无此参数:%s'%name)
