# -*- coding:utf-8 -*-

import hashlib
import datetime
from flask import json, g
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all
from ..base import utils
from ..model import MboxContent, MboxRecord
from ..model import User, Branch, UserBranch

class MboxService():

    def mbox_send(self,**kwargs):
        u'''发送邮件'''
        content = kwargs.get('a')
        record = kwargs.get('b')
        record.update({'send_user_id':g.web_session.user.role_id,'asready':'未读','send_time':str(datetime.datetime.now())})
        content = MboxContent(**content)
        record = MboxRecord(**record)
        record.mbox = content
        g.db_session.add(record)

    def mbox_send2(self, from_teller_no, to_teller_no, title, body):
        u'''发送邮件'''
        from_teller = g.db_session.query(User).filter(User.user_name == from_teller_no).first()
        to_teller = g.db_session.query(User).filter(User.user_name == to_teller_no).first()

        content = MboxContent(title=title, body=body)
        record = MboxRecord(send_user_id = from_teller.role_id, inbox_user_id = to_teller.role_id, asready = u'未读', send_time=str(datetime.datetime.now()))
        record.mbox = content
        g.db_session.add(record)

    def mbox_query(self):
        u'''查询邮件'''
        records = g.db_session.query(MboxRecord, User).join(User, MboxRecord.send_user_id == User.role_id).filter(MboxRecord.inbox_user_id == g.web_session.user.role_id).all()
        record_list = []
        for record in records:
            row = utils.row_dict(record.MboxRecord)
            row['from_teller_no'] = record.User.user_name
            row['to_teller_no'] = g.web_session.user.user_name

            row['title'] = record.MboxRecord.mbox.title
            row['body'] = record.MboxRecord.mbox.body
            record_list.append(row)
        return record_list

    def mbox_branch(self):
        u'''查询机构'''
        return g.db_session.query(Branch).all()

    def mbox_user(self,**kwargs):
        id = kwargs.get('id')[0]
        u'''查询用户'''
        rst=g.db_session.query(UserBranch).join(User,User.role_id == UserBranch.user_id).filter(UserBranch.branch_id == id).all()
        rst_list=[r.user for r in rst]
        return rst_list

    def mbox_update(self,**kwargs):
        id = kwargs.get('id')[0]
        a={'asready':'已读'}
        g.db_session.query(MboxRecord).filter(MboxRecord.id == id).update(a)

    def mbox_del(self,**kwargs):
        id = kwargs.get('id')[0]
        g.db_session.query(MboxRecord).filter(MboxRecord.id == id).delete()

    def mbox_send_group(self,**kwargs):
        u'''发送邮件'''
        now_user =g.web_session.user
        user_list = []
        type = kwargs.get('type')
        branch = g.db_session.query(UserBranch).filter(UserBranch.user_id == now_user.role_id).first()
        if type == 'loan':
            user_list = g.db_session.query(User).join(UserBranch,UserBranch.user_id == User.role_id).join(UserGroup,UserGroup.user_id == User.role_id).join(Group,Group.id==UserGroup.group_id).filter(Group.group_name == u'客户经理').filter(UserBranch.branch_id == branch.branch_id).all()
            u = g.db_session.query(User).join(UserBranch,UserBranch.user_id == User.role_id).join(UserGroup,UserGroup.user_id == User.role_id).join(Group,Group.id==UserGroup.group_id).filter(Group.group_name == u'客户经理').filter(UserBranch.branch_id == branch.branch_id)
        else:
            user_list = g.db_session.query(User).join(UserBranch,UserBranch.user_id == User.role_id).join(UserGroup,UserGroup.user_id == User.role_id).join(Group,Group.id==UserGroup.group_id).filter(Group.group_name == u'资金部统一授信岗').filter(UserBranch.branch_id == branch.branch_id).all()

        content = kwargs.get('a')
        record = kwargs.get('b')
        record.update({'send_user_id':g.web_session.user.role_id,'asready':'未读','send_time':self.now()})
        for user in user_list:
            record.update({'inbox_user_id':user.role_id})
            mboxcontent = MboxContent(**content)
            mboxrecord = MboxRecord(**record)
            mboxrecord.mbox = mboxcontent
            g.db_session.add(mboxrecord)

    def mbox_query_count(self, role_id):
        u'''查询邮件'''
        count = g.db_session.query(MboxRecord, User).join(User, MboxRecord.send_user_id == User.role_id).filter(MboxRecord.inbox_user_id == role_id, MboxRecord.asready == u'未读').count()
        return count
