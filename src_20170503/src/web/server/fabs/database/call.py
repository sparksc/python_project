# -*- coding:utf-8 -*-
from importlib import import_module
def load(module, name):
    if module==None:
        return globals().get(name)
    return getattr(import_module(module), name, None)

def call(module, name, **args):
    return load(module, name)(**args)
