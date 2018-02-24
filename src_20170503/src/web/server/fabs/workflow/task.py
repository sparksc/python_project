# -*- coding:utf-8 -*-
u"""
任务调用和控制
"""
from ..database import get_session
from ..model.transaction import Transaction, TransactionActivity
from ..model.user import User

def get_task(subject):
    session=get_session(subject)
    if isinstance(subject, Transaction):
        task = session.query(TransactionActivity).filter(TransactionActivity.transaction_id == subject.transaction_id)\
                .filter(TransactionActivity.transaction_activity_type=='task')\
                .filter(TransactionActivity.finished == None).all()
        #task=[ t for t in subject.transaction_activity if t.transaction_activity_type==u'task' and not t.finished]  #TODO: fix it
    if isinstance(subject, User):
        task=subject.task
    return task
