# -*- coding: utf-8 -*-
"""
    yinsho.services.DepappointService
    #####################

    yinsho DepappointService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func,text
from sqlalchemy.orm import joinedload_all,joinedload

from ..base import utils
from ..model import T_ZJC_GSGX_CK_YY
  

class DepappointService():
    """ DepappointService """
    def save(self,**kwargs):
        self.ckyy = ['para_id','yyrq','jgbh','jgmc','yggh','ygxm','yyckje','khmc','yyblrq','yybljg','yyyxrq','bz','zhjg','zh','khh','dxxh','ck_type','open_date','typ']
        newdata =  kwargs.get('newdata')
        data ={}
        for k,v in newdata.items():
            if k in self.ckyy : data[k] = v
        g.db_session.add(T_ZJC_GSGX_CK_YY(**data))
        return u"预约信息添加成功"    

    def delete(self,**kwargs):
        tid = kwargs.get('id')
        if tid :
            g.db_session.query(T_ZJC_GSGX_CK_YY).filter(T_ZJC_GSGX_CK_YY.para_id==tid).delete()
            return u'删除成功'
        else:
            return u'无删除主键'

    def update(self, **kwargs):
        self.ckyy = ['yyrq','yyckje','khmc','yyblrq','yybljg','bz','ck_type']
        newdata =  kwargs.get('updata')
        data ={}
        tid = newdata.get('para_id')
        if not tid:return u"无更新主键"
        for k,v in newdata.items():
            if k in self.ckyy : data[k] = v
        g.db_session.query(T_ZJC_GSGX_CK_YY).filter(T_ZJC_GSGX_CK_YY.para_id==tid).update(data)
        return u"修改成功"
     
    def exist(self, **kwargs):
        keydata = kwargs.get('keydata')
        khmc = keydata.get('khmc')
        yybljg = keydata.get('yybljg')
        bz = '1'
        flag =  g.db_session.query(T_ZJC_GSGX_CK_YY).filter(and_(T_ZJC_GSGX_CK_YY.yybljg==yybljg,T_ZJC_GSGX_CK_YY.khmc==khmc,T_ZJC_GSGX_CK_YY.bz==bz)).all()
        if flag:
            return False
        else:
            return True

