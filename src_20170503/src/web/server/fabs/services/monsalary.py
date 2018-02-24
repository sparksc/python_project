# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all

from ..base import utils
from ..model import T_JGC_SFXC 


class monsalaryService():

    def update(self,**kwargs):
   
        newdata =  kwargs.get('updata')
        data ={}
        tid = newdata.get('para_id')
        if not tid:return u"无更新主键"
        g.db_session.query(T_JGC_SFXC).filter(T_JGC_SFXC.para_id==tid).update(newdata)
        return u"修改成功"


    def save(self,**kwargs):
        self.save_list = ['tjrq','yggh','jgbh']
        newdata =  kwargs.get('ntarget')
        data ={}
        for field in self.save_list:
            value = newdata.get(field)
            if value:
                data[field] = value
            else:
                return u"%s 重新填写" % field
        g.db_session.add(T_JGC_SFXC(**newdata))
        return u"添加成功"
