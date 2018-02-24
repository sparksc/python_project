# -*- coding: utf-8 -*-
"""
yinsho.services.SeimService
#####################

yinsho SeimService module
"""
import os,sys
os.getcwd().split('src')[0]
sys.path.append(os.getcwd().split('src')[0]+'src/sqs/sqs/scripts')
sys.path.append(os.getcwd().split('src')[0]+'src/sqs/')
import datetime
import time
from flask import json, g,current_app
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all

from ..base import utils
from ..model import Branch,Menu,User,UserBranch,AccountHook,CustHookBatch,CustHook
from decimal import Decimal
from ..services.mbox import *
from ..services.gsgxck import GsgxckService
from utils import config
from objectquery import ObjectQuery
from querybase import QueryBase
from config import *


class ChooseService(ObjectQuery):
    def __init__(self):
        config_report = open(os.getcwd().split('src')[0]+"src/sqs/config_report.json")
        self.report_conf = json.load(config_report)
    def choose_depcpremove(self,**kwargs):#存款客户号
        self.args={}
        params=kwargs.get('params')
        self.args=params
        QueryBase.__init__(self,None,self.args,self.report_conf)
        flag_status=kwargs.get('flag_status')
        condition=kwargs.get('condition')
        real_params={}
        filterstr=""
        for i in params:
            if params[i]==None or params[i]==u"" or i in ['manager','org_tar','login_teller_no','login_branch_no']:
                continue
            elif i=='note':
                filterstr = filterstr + " and c.note like " + " '%%%s%%' "%(params[i])
            elif i=='notnote':
                for n1 in params[i].replace("，",",").split(","):
                    filterstr = filterstr + " and c.note not like " + " '%%%s%%'"%(n1)
            elif i=='ORG_NO':
                vvv = self.dealfilterlist(params[i])
                filterstr = filterstr +" and c.org_no in ( %s ) "%(vvv)
            else:
                filterstr = filterstr+" and c.%s = '%s'"%(i,params[i])
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['transfer'],'c.manager_no','c.org_no', None)) 
        sql1 =u"""
        select c.id
        from cust_hook c
        join f_user u on u.user_name=c.manager_no
        join branch o on o.branch_code=c.org_no
        join d_cust_info i on i.cust_no=c.cust_in_no
        where c.typ='存款' %s
        order by id desc
        """%(filterstr)
        
        row1 = g.db_session.execute(sql1).fetchall()
        list_row1=[]
        row1_dict={}
        for i in row1:
            list_row1.append(i[0])
        gsgxckService=GsgxckService()
        if flag_status==u'预提交':
            row1_dict['update_key']=list_row1
            result=gsgxckService.batch_cust_move_before2(**row1_dict)
            return result
        if flag_status==u'提交':
            row1_dict={'update_key':list_row1}
            row1_dict.update(condition)
            result=gsgxckService.batch_account_move_sum_with_hook(**row1_dict)
            return result
        if flag_status==u'保存':
            row1_dict={'update_key':list_row1}
            row1_dict.update(condition)
            result=gsgxckService.batch_cust_move2(**row1_dict)
            return result
        if flag_status==u'撤销':
            row1_dict={'update_key':list_row1}
            result=gsgxckService.batch_cust_move_delete2(**row1_dict)
            return result

    def choose_ebankpremove(self,**kwargs):#电子银行
        self.args={}
        params=kwargs.get('params')
        self.args=params
        QueryBase.__init__(self,None,self.args,self.report_conf)
        flag_status=kwargs.get('flag_status')
        condition=kwargs.get('condition')
        current_app.logger.debug(params,flag_status,condition)
        real_params={}
        filterstr=""
        for i in params:
            if params[i]==None or params[i]==u"" or i in ['manager','org_tar','login_teller_no','login_branch_no']:
                continue
            #elif i=='login_teller_no':
            #    if self.deal_teller_transfer_auth(params[i]) == True:
            #        filterstr = filterstr+" and c.manager_no = '%s'"%(params[i])
            #elif i== 'login_branch_no':
            #    bb = self.deal_branch_query_auth(params[i])
            #    if bb != False:
            #        filterstr = filterstr+" and c.org_no in ( %s )"%bb
            elif i=='note':
                filterstr = filterstr + " and c.note like " + " '%%%s%%' "%(params[i])
            elif i=='notnote':
                for n1 in params[i].replace("，",",").split(","):
                    filterstr = filterstr + " and c.note not like " + " '%%%s%%'"%(n1)
            elif i=='ORG_NO' or i=='org_no':
                vvv = self.dealfilterlist(params[i])
                filterstr = filterstr +" and c.org_no in ( %s ) "%(vvv)
            else:
                filterstr = filterstr+" and c.%s = '%s'"%(i,params[i])
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['transfer'],'c.manager_no','c.org_no', None)) 
        sql1 =u"""
        select c.id
        from cust_hook c
        join branch o on o.branch_code=c.org_no
        join f_user u on u.user_name=c.manager_no
        join d_cust_info d on d.cust_no=c.cust_in_no
        where typ='电子银行' %s
        """%(filterstr)
        current_app.logger.debug(sql1)
        row1 = g.db_session.execute(sql1).fetchall()
        list_row1=[]
        row1_dict={}
        for i in row1:
            list_row1.append(i[0])
        gsgxckService=GsgxckService()
        if flag_status==u'预提交':
            row1_dict['update_key']=list_row1
            result=gsgxckService.batch_cust_move_before2(**row1_dict)
            return result
        if flag_status==u'提交':
            row1_dict={'update_key':list_row1}
            row1_dict.update(condition)
            result=gsgxckService.batch_account_move_sum_with_hook(**row1_dict)
            return result
        if flag_status==u'保存':
            row1_dict={'update_key':list_row1}
            row1_dict.update(condition)
            result=gsgxckService.batch_cust_move2(**row1_dict)
            return result
        if flag_status==u'撤销':
            row1_dict={'update_key':list_row1}
            result=gsgxckService.batch_cust_move_delete2(**row1_dict)
            return result


    def choose_loanpremove(self,**kwargs):#贷款移交
        self.args={}
        params=kwargs.get('params')
        self.args=params
        QueryBase.__init__(self,None,self.args,self.report_conf)
        flag_status=kwargs.get('flag_status')
        condition=kwargs.get('condition')
        is_all=kwargs.get('loan_move_all')
        current_app.logger.debug(params,flag_status,condition)
        real_params={}
        filterstr=""
        for i in params:
            if params[i]==None or params[i]==u"" or i in ['manager','org_tar','login_teller_no','login_branch_no']:
                continue
            elif i=='note':
                filterstr = filterstr + " and c.note like " + " '%%%s%%' "%(params[i])
            elif i=='notnote':
                for n1 in params[i].replace("，",",").split(","):
                    filterstr = filterstr + " and c.note not like " + " '%%%s%%'"%(n1)
            elif i=='ORG_NO' or i=='org_no':
                vvv = self.dealfilterlist(params[i])
                filterstr = filterstr +" and c.org_no in ( %s ) "%(vvv)
            elif i == 'CST_TYP':
                if params[i] == u'对公':
                    filterstr = filterstr + " and  left(c.cust_in_no,2)='82' "
                if params[i] == u'对私':
                    filterstr = filterstr + " and  left(c.cust_in_no,2)='81' "
            else:
                filterstr = filterstr+" and c.%s = '%s'"%(i,params[i])
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['transfer'],'c.manager_no','c.org_no', None)) 
        sql1 =u"""
        select c.id
        from cust_hook c
        join f_user u on u.user_name=c.manager_no
        join branch o on o.branch_code=c.org_no
        join d_cust_info i on i.cust_no=c.cust_in_no
        where c.typ='贷款' %s
        order by c.add_avg_balance desc
        """%(filterstr)
        current_app.logger.debug(sql1)
        row1 = g.db_session.execute(sql1).fetchall()
        list_row1=[]
        row1_dict={}
        for i in row1:
            list_row1.append(i[0])
        gsgxckService=GsgxckService()
        if flag_status==u'预提交':
            row1_dict['update_key']=list_row1
            result=gsgxckService.batch_cust_move_before2(**row1_dict)
            return result
        if flag_status==u'提交':
            row1_dict={'update_key':list_row1}
            row1_dict.update(condition)
            result=gsgxckService.batch_account_move_sum_with_hook(**row1_dict)
            return result
        if flag_status==u'保存':
            row1_dict={'update_key':list_row1}
            row1_dict.update(condition)
            if is_all =='1':
                result=gsgxckService.batch_cust_move_all2(**row1_dict)
                return result
            else:
                result=gsgxckService.batch_cust_move2(**row1_dict)
                return result
        if flag_status==u'撤销':
            row1_dict={'update_key':list_row1}
            result=gsgxckService.batch_cust_move_delete2(**row1_dict)
            return result

