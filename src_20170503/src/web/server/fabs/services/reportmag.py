# -*- coding: utf-8 -*-
"""
    yinsho.services.TParaService
    #####################

    yinsho TParaService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func,text
from sqlalchemy.orm import joinedload_all,joinedload

from ..base import utils
from ..model import Menu,T_reportmag
  

class reportmagService():
    """ TParaService """
    def type_save(self,**kwargs):
        self.save_list = ['report_name','report_script']
        newdata =  kwargs.get('newdata')
        data ={}
        for field in self.save_list:
            value = newdata.get(field)
            if value:
                data[field] = value
            else:
                return u"%s 需要填写" % field
        g.db_session.add(T_reportmag(**data))
        return u"添加成功"    
    def type_update(self, **kwargs):
        self.save_list = ['report_name','report_script']
        newdata =  kwargs.get('updata')
        data ={}
        tid = newdata.get('id')
        if not tid:return u"无更新主键"
        for k,v in newdata.items():
            if k in self.save_list : data[k] = v
        g.db_session.query(T_reportmag).filter(T_reportmag.id==tid).update(data)
        return u"修改成功"
    def menu_save(self, **kwargs):
        self.save_list = ['location','name']
        newdata =  kwargs.get('menudata')
        data ={}
        q=g.db_session.query(Menu).filter(Menu.name==u'客户经理绩效佣金报表')
        result=q.first()
     
        for k,v in newdata.items():
            if k in self.save_list : data[k] = v
        data['parent_id']=result.id
        g.db_session.add(Menu(**data))
        return u"修改成功"
        
