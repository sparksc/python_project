# -*- coding:utf-8 -*-
from ..model.transaction import *
def process_init(session):
    status_type=StatusType(status_type_name=u'交易活动状态', status_type_describe=u'交易活动的基本状态')
    session.add(status_type)
    session.add_all([
        Status(status_id=1, status_type=status_type, status_name=u'活动', status_describe=u'表示交易活动已经被激活，正在活动中'),
        Status(status_id=2, status_type=status_type, status_name=u'结束', status_describe=u'表示交易活动已经结束'),
        ])
