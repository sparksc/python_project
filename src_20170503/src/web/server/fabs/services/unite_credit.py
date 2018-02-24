# -*- coding: utf-8 -*-
"""
    yinsho.services.UniteCreditService
    #####################

    yinsho UniteCreditService module
"""
from ..model.party import *
from .service import BaseService
import hashlib, copy
from flask import json, g
from sqlalchemy import and_
from sqlalchemy import desc
from ..model.credit import *
from ..model.transaction import *
from ..model.application import *
from ..model.task import Task
from ..workflow import task
from ..workflow.parameter import *
from ..database.sqlal import simple_session
from ..base import core_inf , utils

import decimal
from decimal import Decimal
import datetime
import random
import datetime

class UniteCreditService(BaseService):

    def test_get_data(self):
        user = g.web_session.user
        if user.user_branches in [[],None]:
            branch_name = None
        else:
            branch_name=user.user_branches[0].branch.branch_name

        untab = UniteCreditTable(credit_date=datetime.datetime.now(),
                                  branch=branch_name,
                                  credit_term=u'1年')
 
        # --- 还需要筛选出 支行 filter(Application.handle_branch.like('XXX%'))
        # ---- 还需筛选出 申请是否有效 filter.(Application.XXX ....)
        custs = g.db_session.query(Customer).filter(Customer.cust_type=='company').all()
                                        #Application,ApplicationTransaction,LendTransaction)\
                                        #.join(Application,Application.customer_id == Customer.role_id)\
                                        #.join(ApplicationTransaction,ApplicationTransaction.application_id ==Application.id)\
                                        #.join(LendTransaction,LendTransaction.application_transaction_id == ApplicationTransaction.transaction_id)\
                                        
        for cust in custs:
            # 客户信息
            print cust.party.name,cust.party.no
            uni_cre = UniteCredit(name=cust.party.name, 
                                    corp_name = cust.party.corp_name,
                                    #most_limt_b=629,
                                    uni_cre_tb=untab)
            
            total_amount = 0
            apps = cust.application
            appl_id_list = []
            for app in apps: 
                ## 抵质押物信息
                for gua_info in app.guarantee_infos:
                    uni_ple = UnitePledge(unt_cre=uni_cre,
                                pledge_good=gua.gty_detail,
                                #pledge_nums=u'306.95平米',
                                #single='2',
                                total=gua.mrge_asse_value,
                                #single_r='2',
                                total_r=gua.mrge_finds_value)
                    g.db_session.add(uni_ple)
                ##保证信息..?
                #添加保证信息

                appl_id_list.append(app.id)

            #合同放款信息
            # 期限信息
            ids =set(appl_id_list)
            print ids
            len_trans = g.db_session.query(LendTransaction).join(ApplicationTransaction,ApplicationTransaction.transaction_id == LendTransaction.application_transaction_id).filter(ApplicationTransaction.application_id.in_(ids)).all()
            for len_tran in len_trans:
                amount = len_tran.amount
                term = u'1年'
                total_amount = total_amount + amount
                # 抵质押物金额
                uni_ple_lon = UnitePledgeLoan(unt_cre=uni_cre,
                                            loan_left=amount,
                                            term=term)
                g.db_session.add(uni_ple_lon)
                #保证金额
                #xxxx

                #票据
                uni_bill = UniteBill(unt_cre = uni_cre,amount=amount)
                g.db_session.add(uni_bill)
            uni_cre.most_limt_b = total_amount
       #g.db_session.commit();


    def unite_credit_create(self):
        #return self.test_get_data()
        u""" 统一授信  """
        #example  企业用户 party_id = 5 乌海市明星焦化有限责任公司
        cust = g.db_session.query(Customer).filter(Customer.party_id == 5).first()
        untab = UniteCreditTable(credit_date=datetime.datetime.now(),
                                  branch=u'大众支行',
                                  credit_term=u'1年')
        # 抵质押物 单位? 记录?
        #----------  1 ------------
        uni_cre = UniteCredit(name=cust.party.name,
                                    corp_name = cust.party.corp_name,
                                    most_limt_b=629,
                                    uni_cre_tb=untab)
        uni_ple1 = UnitePledge(unt_cre=uni_cre,
                    pledge_good=u'商用房',
                    pledge_nums=u'306.95平米',
                    single='2',
                    total='614.05',
                    single_r='2',
                    total_r='614.05')

        uni_ple2 = UnitePledge(unt_cre=uni_cre,
                    pledge_good=u'商用房',
                    pledge_nums=u'276平米',
                    single='1.7',
                    total='470.16',
                    single_r='1.7',
                    total_r='470.16')

        uni_ple_lon1 = UnitePledgeLoan(unt_cre=uni_cre,
                                        loan_left=355,
                                        term=u'1年')
        uni_ple_lon2 = UnitePledgeLoan(unt_cre=uni_cre,
                                        loan_left=274,
                                        term=u'1年')
        g.db_session.add_all([uni_ple1,uni_ple2,uni_ple_lon1,uni_ple_lon2])

        #-----------  2  ------------
        cust = g.db_session.query(Customer).filter(Customer.party_id == 4).first()
        unite_credit = UniteCredit(name=cust.party.name,
                                    corp_name = cust.party.corp_name,
                                    most_limt_b=11000,
                                    uni_cre_tb=untab)
        uni_ple1 = UnitePledge(unt_cre=unite_credit,
                    pledge_good=u'机器设备/电子设备',
                    pledge_nums=u'447台/件',
                    single='',
                    total='3397',
                    single_r='',
                    total_r='3397')
        uni_ple2 = UnitePledge(unt_cre=unite_credit,
                    pledge_good=u'原煤、精煤、中煤',
                    pledge_nums=u'106万吨',
                    single='0.0137',
                    total='14560',
                    single_r='0.0137',
                    total_r='14560')
        uni_ple3 = UnitePledge(unt_cre=unite_credit,
                    pledge_good=u'土地',
                    pledge_nums=u'115840.42平方米',
                    single='0.0137',
                    total='14560',
                    single_r='0.0137',
                    total_r='14560')
        g.db_session.add_all([uni_ple1,uni_ple2,uni_ple3])
        uni_bill = UniteBill(unt_cre = unite_credit,amount=11000)
        g.db_session.add(uni_bill)

        g.db_session.commit()
        unitab = untab #g.db_session.query(UniteCreditTable).first()

        items = [{'uni_cre':cre,'ples':cre.uni_ple,'guas':cre.uni_gua,'ple_loans':cre.uni_ple_loan,'gua_loans':cre.uni_gua_loan,'bills':cre.uni_bill} for cre in unitab.uni_cres]
        rtn = {'uni_cre_tb':unitab,
                'uni_cre_itms':items}

        return rtn

    def query_by_application(self,application_id):
        app = g.db_session.query(Application).filter(Application.id == application_id).first()
        print '-------------', app.unite_credit_tab
        if app.unite_credit_tab in [[],None]:
            return []
        unitab = app.unite_credit_tab[0]
        items = [{'uni_cre':cre,'ples':cre.uni_ple,'guas':cre.uni_gua,'ple_loans':cre.uni_ple_loan,'gua_loans':cre.uni_gua_loan,'bills':cre.uni_bill} for cre in unitab.uni_cres]
        rtn = {'uni_cre_tb':unitab,
                'uni_cre_itms':items}
        app_info = {}
        dc = app.__dict__
        for k in dc:
            if(isinstance(dc.get(k),(str,int,datetime.datetime,unicode))):
                app_info.update({k:dc.get(k)})
        return {'application':app_info,'un_tb':rtn}

    def unite_credit_query(self,uni_id):

        unitab = g.db_session.query(UniteCreditTable).filter(UniteCreditTable.id == uni_id).first()
        items = [{'uni_cre':cre,'ples':cre.uni_ple,'guas':cre.uni_gua,'ple_loans':cre.uni_ple_loan,'gua_loans':cre.uni_gua_loan,'bills':cre.uni_bill} for cre in unitab.uni_cres]
        rtn = {'uni_cre_tb':unitab,
                'uni_cre_itms':items}
        return rtn

    def unite_credit_update(self,**kwargs):

        items =  kwargs.get('items')
        for it in items:
            ele={'finance':it.get('finance'),
                  'most_limt':it.get('most_limt'),
                  'loan':it.get('loan'),
                  'discount':it.get('discount'),
                  'remark':it.get('remark')
                 }
            g.db_session.query(UniteCredit).filter(UniteCredit.id == it.get('id')).update(ele)
        g.db_session.commit()
        return {'success':True}

    def unite_credit_queryList(self,**kwargs):

        unitabs = g.db_session.query(UniteCreditTable).all()
        unis = [ut for ut in unitabs]
        return unis

    def inflow(self,untb_id):
        app = Application(product_code='951',apply_date=datetime.datetime.now(),status=u'授信申请')
        at = ApplicationTransaction(transaction_name=u"统一授信申请",
                                    application=app,
                                    transaction_timestamp=datetime.datetime.now())
        
        g.db_session.add(at)
        g.db_session.commit()
        g.db_session.query(UniteCreditTable).filter(UniteCreditTable.id == untb_id).update({'application_id':app.id})
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"统一授信业务流程").first()

        start(at, start_activity)
        g.db_session.commit()

        user = g.web_session.user
        groups = []
        for group in user.user_groups:
            groups.append(group.group.group_name)

        task_list = task.get_task(at)
        for t in task_list:
            role = get_parameter(t.activity,u"角色")
            if role and role in groups:
                t.user = user
                t.active()
                t.finish()

        g.db_session.commit()
        return {'msg':"进入流程成功"}
