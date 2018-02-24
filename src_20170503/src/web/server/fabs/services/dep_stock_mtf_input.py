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
from ..model import Branch,Menu,User,UserBranch,Dep_Stock_Mtf_Input


class DepstockmtfinputService():
    """ Target Service  """

    def save(self,**kwargs):
        self.ckyy = ['org_code','org_name','be_year','fee','staff_code','staff_name','input_level']
        newdata =  kwargs.get('newdata')
        data ={}
        for k,v in newdata.items():
            if k in self.ckyy : 
                if k=='fee':
                    v=float(v)*100
            data[k] = v
        g.db_session.add(Dep_Stock_Mtf_Input(**data))
        return u"ok" 

    def delete(self,**kwargs):
        self.ckyy = ['org_code','org_name','be_year','fee','staff_code','staff_name','input_level','id']
        newdata =  kwargs.get('newdata')
        pid = newdata.get('id')
        #g.db_session.add(Dep_Stock_Mtf_Input(**data))
        g.db_session.query(Dep_Stock_Mtf_Input).filter(Dep_Stock_Mtf_Input.id == pid).delete()
        return u"ok" 

    def update(self,**kwargs):
        self.ckyy = ['org_code','org_name','be_year','fee','staff_code','staff_name','input_level','id']
        newdata =  kwargs.get('newdata')
        pid = newdata.get('id')
        newdata.pop('id');
        data ={}
        #for k,v in newdata.items():
        #    if k in self.ckyy : data[k] = v
        if newdata['fee']:
            newdata['fee']=float(newdata['fee'])*100
        g.db_session.query(Dep_Stock_Mtf_Input).filter(Dep_Stock_Mtf_Input.id == pid).update(newdata)
        return u"ok"  
    

