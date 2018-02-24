# -*- coding: utf-8 -*-
"""
    yinsho.services.dkkhxdhService
    #####################

    yinsho dkkhxdhService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func,text
from sqlalchemy.orm import joinedload_all,joinedload

from ..base import utils
from ..model import LOAN_CUS_CORE_CREDIT
  

class DkkhxdhService():
    """ dkkhxdhService """
   
    def khh_save(self,**kwargs):
        self.save_list = ['account_name','third_org_code','third_org_name','cust_seq','cust_seq2']
        newdata =  kwargs.get('newdata')
	print (newdata)
        data ={}
	CUST_SEQ=''
	ACCOUNT_CLASSIFY=''
	sql="select CUST_SEQ from D_ACCOUNT where CUST_SEQ=:CUST_SEQ and ACCOUNT_CLASSIFY=:ACCOUNT_CLASSIFY"
	s = text(sql)
        for field in self.save_list:
            value = newdata.get(field)
            if value:
	    	if(field=='cust_seq'):
		    para = newdata.get(field)
		    if g.db_session.execute(s,{'CUST_SEQ':para,'ACCOUNT_CLASSIFY':'P'}).fetchone() or g.db_session.execute(s,{'CUST_SEQ':para,'ACCOUNT_CLASSIFY':'L'}).fetchone() != None:
		        data[field] = value
		    else:
		        return u"%s 检验不存在" % field
		if(field=='cust_seq2'):
		    para = newdata.get(field)
		    if g.db_session.execute(s,{'CUST_SEQ':para,'ACCOUNT_CLASSIFY':'P'}).fetchone() or g.db_session.execute(s,{'CUST_SEQ':para,'ACCOUNT_CLASSIFY':'L'}).fetchone() != None:
		        data[field] = value
		    else:
		        return u"%s 检验不存在" % field
                data[field] = value
            else:
                return u"%s 重新填写" % field
        g.db_session.add(LOAN_CUS_CORE_CREDIT(**data))
        return u"添加成功"    

    
    def khh_update(self, **kwargs):
        self.save_list = ['account_name','third_org_code','third_org_name','cust_seq','cust_seq2']
        newdata =  kwargs.get('updata')
        data ={}
        CUST_SEQ=''
	ACCOUNT_CLASSIFY=''
	sql="select CUST_SEQ from D_ACCOUNT where CUST_SEQ=:CUST_SEQ and ACCOUNT_CLASSIFY=:ACCOUNT_CLASSIFY"
	s = text(sql) 
        tid = newdata.get('id')
        if not tid:return u"无更新主键"
        for k,v in newdata.items():
	    v = newdata.get(k)
            if k in self.save_list: 
                if v:
	    	    if(k == 'cust_seq'):
		        para = newdata.get(k)
		        if g.db_session.execute(s,{'CUST_SEQ':para,'ACCOUNT_CLASSIFY':'P'}).fetchone() or g.db_session.execute(s,{'CUST_SEQ':para,'ACCOUNT_CLASSIFY':'L'}).fetchone() != None:
		            data[k] = v
		        else:
  	                    return u"%s 检验不存在" % k
	            if(k == 'cust_seq2'):
		        para = newdata.get(k)
		        if g.db_session.execute(s,{'CUST_SEQ':para,'ACCOUNT_CLASSIFY':'P'}).fetchone() or g.db_session.execute(s,{'CUST_SEQ':para,'ACCOUNT_CLASSIFY':'L'}).fetchone() != None:
		            data[k] = v
		        else:
		            return u"%s 检验不存在" % k
                    data[k] = v
                else:
                    return u"%s 重新填写" % k 
        g.db_session.query(LOAN_CUS_CORE_CREDIT).filter(LOAN_CUS_CORE_CREDIT.id==tid).update(data)
        return u"修改成功"
        
        
    def khh_delete(self,**kwargs):
        g.db_session.query(LOAN_CUS_CORE_CREDIT).filter(LOAN_CUS_CORE_CREDIT.id==kwargs.get('delete_id')).delete()
        return u"删除成功"
  
      
     
