# -*- coding: utf-8 -*-
"""
    yinsho.services.DictDataService
    #####################

    yinsho DictDataService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func,text
from sqlalchemy.orm import joinedload_all,joinedload

from ..base import utils
from ..model import Dict_Data
  

class DictDataService():
    """ DictDataService """
    def save(self,**kwargs):
        self.ckyy = ['dict_id','dict_type','dict_key','dict_value']
        newdata =  kwargs.get('newdata')
        data ={}
        for k,v in newdata.items():
            if k in self.ckyy : data[k] = v
        g.db_session.add(Dict_Data(**data))
        return u"添加成功"    

    def delete(self,**kwargs):
        tid = kwargs.get('id')
        if tid :
            g.db_session.query(Dict_Data).filter(Dict_Data.dict_id==tid).delete()
            return u'删除成功'
        else:
            return u'无删除主键'

    def update(self, **kwargs):
        self.ckyy = ['dict_type','dict_key','dict_value']
        newdata =  kwargs.get('updata')
        data ={}
        tid = newdata.get('dict_id')
        if not tid:return u"无更新主键"
        for k,v in newdata.items():
            if k in self.ckyy : data[k] = v
        g.db_session.query(Dict_Data).filter(Dict_Data.dict_id==tid).update(data)
        return u"修改成功"
     

    def simple_select(self,**kwargs):
        self.filterkey = ['dict_type','dict_key','dict_id','dict_value']
        filterdata = kwargs.get('filterdata')
        data={}
        for k,v in filterdata.items():
            if k in self.filterkey: data[k] = v
        q = g.db_session.query(Dict_Data)
        for attr,value in data.items():
            q= q.filter(getattr(Dict_Data,attr)==value)
        return q.all()

    def get_dict(self,**kwargs):
        dict_type = kwargs.get('dict_type')
        rs ={'v2k':{},'k2v':{},'data':[]}
        if dict_type:
            q = g.db_session.query(Dict_Data).filter(Dict_Data.dict_type==dict_type).all()
            for item in q:
                data = {}
                data['key'] = item.dict_key
                data['value'] =item.dict_value
                rs['v2k'][data['value']]=data['key']
                rs['k2v'][data['key']]=data['value']
                rs['data'].append(data)
        return rs
    
    def get_dicts(self,**kwargs):
        l_dict_type = kwargs.get('l_dict_type')
        rs ={}
        if len(l_dict_type)>0:
            q = g.db_session.query(Dict_Data).filter(Dict_Data.dict_type.in_(l_dict_type)).all()
            for item in q:
                data = {}
                data['key'] = item.dict_key
                data['value'] =item.dict_value
                if item.dict_type in rs:
                    rs[item.dict_type]['v2k'][data['value']]=data['key']
                    rs[item.dict_type]['k2v'][data['key']]=data['value']
                    rs[item.dict_type]['data'].append(data)
                else:
                    rs[item.dict_type]={}
                    rs[item.dict_type]['data']=[data]
                    rs[item.dict_type]['v2k']={data['value']:data['key']}
                    rs[item.dict_type]['k2v']={data['key']:data['value']}
        return rs


