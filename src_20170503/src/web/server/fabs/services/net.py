# -*- coding: utf-8 -*-
"""
    yinsho.services.PermissionService
    #####################

    yinsho UsersService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all

from ..base import utils
# from ..model import Permission, Menu, User, UserGroup, Group, GroupMenu, Branch, UserBranch
from ..model import Menu, User, UserGroup, Group, GroupMenu, Branch, UserBranch ,Net


class NetService():
    """ Net Service  """

    # TODO: Move to the net db_session object


    def nets(self):
       return g.db_session.query(Net).order_by(Net.net_id).all()

    def net_del(self,**kwargs):
        net_id = kwargs.get('net_id')
        g.db_session.query(Net).filter(Net.net_id==net_id).delete()
        return u'删除成功'       

    def net_edit_save(self, **kwargs):
       net_id = kwargs.get('net_id')
       net_name = kwargs.get('net_name')
       net_address = kwargs.get('net_address')
       net_tel = kwargs.get('net_tel')
       net=g.db_session.query(Net).filter(Net.net_id==net_id).delete()
       g.db_session.add(Net(net_id=net_id,net_name=net_name,net_address=net_address,net_tel=net_tel))
       return u"保存成功"

    def net_add_save(self, **kwargs):
       net_id = kwargs.get('net_id')
       net_name = kwargs.get('net_name')
       net_address = kwargs.get('net_address')
       net_tel = kwargs.get('net_tel')
       nets=g.db_session.query(Net).filter(Net.net_id==net_id)
       for net in nets:
         if net:
            return u"该网点已存在！"
       g.db_session.add(Net(net_id=net_id,net_name=net_name,net_address=net_address,net_tel=net_tel))
       return u"保存成功"



