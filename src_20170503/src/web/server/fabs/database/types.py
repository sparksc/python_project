# -*- coding:utf-8 -*-
from .sqlal import current_engine
import sqlalchemy


dialect_name = current_engine.dialect.name


def Text(size):
    if dialect_name=='oracle':
        return sqlalchemy.Text(size)
    else:
        return sqlalchemy.String(size)
