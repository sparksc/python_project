# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all
import xlrd
from ..base import utils
from ..model import Branch,Menu,User,UserBranch,Manager_Add_Sco


class ManagerAddScoService():
    """ Target Service  """

    def save(self,**kwargs):
        self.ckyy = ['syear','smouth','staff_code','staff_name','org_code','org_name','score','typ']
        newdata =  kwargs.get('newdata')
        data ={}
        for k,v in newdata.items():
            if k in self.ckyy :
                if k=='score':
                    v=float(v)*100
                data[k] = v
                print k,v,data[k]
        g.db_session.add(Manager_Add_Sco(**data))
        return u"ok" 

    def delete(self,**kwargs):
        self.ckyy = ['syear','smouth','staff_code','staff_name','org_code','org_name','score','typ','id']
        newdata =  kwargs.get('newdata')
        pid = newdata.get('id')
        #g.db_session.add(CustHook(**data))
        g.db_session.query(Manager_Add_Sco).filter(Manager_Add_Sco.id == pid).delete()
        return u"ok" 

    def update(self,**kwargs):
        self.ckyy = ['syear','smouth','staff_code','staff_name','org_code','org_name','score','typ','id']
        newdata =  kwargs.get('newdata')
        pid = newdata.get('id')
        newdata.pop('id');
        data ={}
        #for k,v in newdata.items():
        #    if k in self.ckyy : data[k] = v
        if newdata['score']:
            newdata['score']=float(newdata['score'])*100
        g.db_session.query(Manager_Add_Sco).filter(Manager_Add_Sco.id == pid).update(newdata)
        return u"ok"  
    

