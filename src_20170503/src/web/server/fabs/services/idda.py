# -*- coding: utf-8 -*-
"""
    yinsho.services.iddaService
    #####################

    yinsho IddaService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func,text
from sqlalchemy.orm import joinedload_all,joinedload

from ..base import utils
from ..model import idda 
  

class IddaService():
    """ iddaService """
    "参数类型的保存，所有项都是必填，插入前检查key是否已存在"
    def idda_save(self,**kwargs):
        self.save_list = ['instition_number','business_type','now_state','adjust_time_type','adjust_time','adjust_value']
        newdata =  kwargs.get('newdata')
        data ={}
        for field in self.save_list:
            value = newdata.get(field)
            if value:
                data[field] = value
            else:
                return u"%s 需要填写" % field
        g.db_session.add(idda(**data))
        return u"添加成功"    

    def type_update(self, **kwargs):
        self.save_list = ['instition_number','now_state','business_type','adjust_time_type','adjust_time','adjust_value']
        newdata =  kwargs.get('newdata')
        data ={}
        tid = newdata.get('id')
        if not tid:return u"无更新主键"
        for k,v in newdata.items():
            if k in self.save_list : data[k] = v
        g.db_session.query(idda).filter(idda.id==tid).update(data)
        return u"修改成功"
        
        
    def type_delete(self,**kwargs):
        g.db_session.query(idda).filter(idda.id==kwargs.get('delete_id')).delete()
        return u"删除成功"
