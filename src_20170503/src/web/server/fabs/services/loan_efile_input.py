# -*- coding: utf-8 -*-
"""
    yinsho.services.TParaService
    #####################

    yinsho Loan_InputService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func,text
from sqlalchemy.orm import joinedload_all,joinedload

from ..base import utils
from ..model import Loan_Persom_Input,Loan_Public_Input
  

class Loan_Input():
   
    def tsave(self,**kwargs):
        newdata =  kwargs.get('add_date')
        g.db_session.add(Loan_Public_Input(**newdata))
        return u"保存成功"

    
    def tedit(self, **kwargs):
        newdata =  kwargs.get('up_date')
        g.db_session.query(Loan_Public_Input).filter(Loan_Public_Input.id==newdata['id']).update(newdata)
        return u"保存成功"
        
        
    def loanpersonseach(self,**kwargs):
        return u"路径通"
    def tdelt(self,**kwargs):
        newdata =  kwargs.get('item_id')
        g.db_session.query(Loan_Public_Input).filter(Loan_Public_Input.id==newdata).delete()
        return u"保存成功"
  
      
    def save(self,**kwargs):
        newdata =  kwargs.get('add_date')
        g.db_session.add(Loan_Persom_Input(**newdata))
        return u"保存成功"
     
    def edit(self,**kwargs):
        newdata =  kwargs.get('up_date')
        g.db_session.query(Loan_Persom_Input).filter(Loan_Persom_Input.id==newdata['id']).update(newdata)
        return u"保存成功"
    
    def delt(self,**kwargs):
        newdata =  kwargs.get('item_id')
        g.db_session.query(Loan_Persom_Input).filter(Loan_Persom_Input.id==newdata).delete()
        return u"保存成功"
