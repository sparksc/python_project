# -*- coding: utf-8 -*-
"""
    yinsho.services.TParaService
    #####################

    yinsho adjusttypeService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func,text
from sqlalchemy.orm import joinedload_all,joinedload

from ..base import utils
from ..model import T_CQK_TYPE
  

class AdjusttypeS():
    """ adjusttypeService """
   
    def type_save(self,**kwargs):
        self.save_list = ['times','timestype','institution','businesstype','adjustnum','adjuststate']
        newdata =  kwargs.get('newdata')
        data ={}
        for field in self.save_list:
            value = newdata.get(field)
            if value:
                data[field] = value
            else:
                return u"%s 重新填写" % field
        g.db_session.add(T_CQK_TYPE(**data))
        return u"添加成功"    

    
    def type_update(self, **kwargs):
        self.save_list = ['times','timestype','businesstype','adjustnum','adjuststate']
        newdata =  kwargs.get('updata')
        data ={}
        tid = newdata.get('id')
        if not tid:return u"无更新主键"
        for k,v in newdata.items():
            if k in self.save_list : data[k] = v
        g.db_session.query(T_CQK_TYPE).filter(T_CQK_TYPE.id==tid).update(data)
        return u"修改成功"
        
        
    def type_delete(self,**kwargs):
        g.db_session.query(T_CQK_TYPE).filter(T_CQK_TYPE.id==kwargs.get('delete_id')).delete()
        return u"删除成功"
  
      
     
