# -*- coding: utf-8 -*-
"""
    yinsho.services.CreditServic
    #####################

    yinsho CreditServic module
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
from ..model.contract import Contract
from ..model.task import Task
from ..workflow import task
from ..workflow.parameter import *
from ..database.sqlal import simple_session
from ..base import core_inf 
import time
import decimal
from decimal import Decimal
import datetime
import random
import datetime

class CreditService(BaseService):
    
    def querystatus(self,**kwargs):
        print kwargs
        application_id=kwargs.get('application_id')
        app_status=kwargs.get('app_status')
        at=g.db_session.query(TransactionActivity).join(ApplicationTransaction,TransactionActivity.transaction_id == ApplicationTransaction.transaction_id).filter(ApplicationTransaction.application_id == application_id).all()
        print app_status
        status=g.db_session.query(Activity).filter(Activity.activity_name == app_status).first()
        print status
        act_status=status.activity_status
        if app_status == '投资委员会审议':
           act_status = '审批'
        if at:
           return {'msg':u'投资申请','act_status':act_status}
        else:
           return {'msg':u'投资申请未提交','act_status':act_status}

    def save_discount(self,**kwargs):
        u'''  创建贴现申请信息  '''
        party_id = kwargs.get('party_id')
        product_code = kwargs.get('loan_type_code')
        main_gua = kwargs.get('main_gua')
        quote_report =  kwargs.get('quote_report')
        sur_rep = None
        if quote_report == u'是':
            sur_rep = g.db_session.query(SurveyReport).filter(SurveyReport.party_id==party_id).filter(SurveyReport.product_code == product_code).order_by(desc(SurveyReport.end_date)).first()
            if sur_rep == None:
                return {"error":"无调查报告可以引用"}
            if str(sur_rep.end_date) < str(datetime.datetime.now()):
                return {"error":"调查报告过期"}

        cust = g.db_session.query(Customer).join(Party,Party.id == Customer.party_id).filter(Customer.party_id==party_id).first()
        a = Application(
                        customer_id = cust.role_id,
                        survey_report = sur_rep,
                        product_code = product_code,
                        main_gua_type = main_gua,
                        quote_report = quote_report,
                        status=u'暂存')

        at=ApplicationTransaction(transaction_name=u"%s的贴现申请"%(cust.party.name),application=a,party=cust.party)
        g.db_session.add(at)
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"贴现业务流程").first()
        start(at, start_activity)
        g.db_session.flush() 
        return {'success':True,'id':a.id}



    def saveInfo_discount(self,**kwargs):
        u''' 数据保存 '''
        transaction_info =  kwargs.get('transaction_info')
        application_info =  kwargs.get('application_info')
        product_code = application_info.get('product_code')
        product = g.db_session.query(Product).filter(Product.product_code == product_code).first()
        if application_info.get('survey_report_id'):
            application_info.pop('survey_report_id')
        app_id = application_info.get('id')
        for k in application_info.keys():
            if application_info.get(k) == None:
                application_info.pop(k)
            elif application_info.get(k) == []:
                application_info.pop(k)
        g.db_session.query(Transaction).filter(Transaction.transaction_id==transaction_info.get('transaction_id')).update(\
        {'transaction_timestamp':datetime.datetime.now(),
        'currency_code':transaction_info.get('currency_code') or 'CNY',
        'amount':transaction_info.get('amount')})
        apply_date = application_info.get('apply_date');
        if apply_date:
            application_info.update({'apply_date':datetime.datetime.strptime(apply_date.strip(),'%Y-%m-%d'),'status':u'贴现申请'})
        g.db_session.query(Application).filter(Application.id==app_id).update(application_info)#
        g.db_session.commit()

        return {'application_id':app_id}

    def submit_discount(self,**kwargs):
        u''' 进入流程 '''
        application_info =  kwargs.get('application_info')
        application_id = application_info.get('id')
        rst = g.db_session.query(ApplicationTransaction, Application) \
            .join(Application, Application.id == ApplicationTransaction.application_id)\
            .filter(Application.id == application_id).first()
        at = rst.ApplicationTransaction
        a = rst.Application
        if a is None:
            raise Exception('交易不存在!')
        user = g.web_session.user
        groups = []
        for group in user.user_groups:
            groups.append(group.group.group_name)
        task_list = task.get_task(at)
        flag = True 
        for t in task_list:
            role = get_parameter(t.activity,u"角色")
            if role and role in groups:
                t.user = user
                t.active()
                t.finish()
                flag=False
                g.db_session.query(Application).filter(Application.id == a.id).update({Application.status:t.activity.activity_name})
        g.db_session.flush()
        if flag:
            return {'success':False,'msg':u'您已提交申请'}
        next_step = []
        task_list = task.get_task(at)
        for t in task_list:
              if t.finished==None:
                  role=get_parameter(t.activity,u"角色")
                  rst=g.db_session.query(UserGroup).join(Group,UserGroup.group_id==Group.id).filter(Group.group_name==role).all()
                  users =[{'user_name': r.user.user_name,'name':r.user.name} for r in rst ]
                  next_step.append({'activity':t.activity,'role':role,'users':users})
        return {'success':True,'next_step':next_step}
 
    def save(self,**kwargs):
        u'''  创建贷款申请信息  '''
        party_id = kwargs.get('party_id')
        product_code = kwargs.get('loan_type_code')
        main_gua = kwargs.get('main_gua')
        term = kwargs.get('term')
        bill_kind = kwargs.get('bill_kind')
        '''
        #为了连不上内网的同学使用，暂时先将核心接口注释，需要的可自行打开
        if product_code !='007':
            rt = core_inf.trans120191(kwargs.get('loan_type'),term)
            if int(rt.get('code')) != 0:
                return {'error':rt.get('reason')}
            try:
                pro_rate = Decimal(rt.get(u'产品利率')) / Decimal('1000000')
                product_rate = pro_rate #  pro_rate.to_integral_value()       #str(float(rt.get(u'产品利率'))/100/10000)
            except Exception as e:
                return {'error':u'利率异常'}
            com_rate = Decimal(rt.get(u'合规利率')) #* Decimal('1000')
            compliance_rate = com_rate #com_rate.to_integral_value()
        else:
            product_rate =5.610
            compliance_rate=3.625
        '''
        product_rate =5.610
        compliance_rate=3.625
        cust = g.db_session.query(Customer).join(Party,Party.id == Customer.party_id).filter(Customer.party_id==party_id).first()
        a = Application(product_rate = product_rate,
                        compliance_rate = compliance_rate,
                        customer_id = cust.role_id,
                        product_code = product_code,
                        main_gua_type = main_gua,
                        term_month = int(term),
                        bill_kind = bill_kind,
                        status=u'暂存')
        at=ApplicationTransaction(transaction_name=u"%s的贷款申请"%(cust.party.name),application=a,party=cust.party)
        g.db_session.add(at)
        # Start Application Activity
        if product_code == '705':
             start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"投资流程").first()
        elif product_code =='007':
             start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"承兑汇票签发申请流程").first()
        else:
             start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"贷款申请流程").first()
        start(at, start_activity)

        return {'success':True}

    def submit(self,**kwargs):
        u''' 保存数据 '''
        transaction_info =  kwargs.get('transaction_info')
        application_info =  kwargs.get('application_info')
        product_code = application_info.get('product_code')
        status = kwargs.get('status')
        app_id = application_info.get('id')
        trans_id =''
        for k in application_info.keys():
            if application_info.get(k) == None:
                application_info.pop(k)
            elif application_info.get(k) == []:
                application_info.pop(k) 
        application_info.pop('id')
        if(status !='转贷'):
            at = g.db_session.query(ApplicationTransaction).filter(ApplicationTransaction.application_id==app_id).first()
            g.db_session.query(Transaction).filter(Transaction.transaction_id==transaction_info.get('transaction_id')).update(\
            {'transaction_timestamp':datetime.datetime.now(),
            'currency_code':transaction_info.get('currency_code') or 'CNY',
            'amount':transaction_info.get('amount')})
            apply_date = application_info.get('apply_date');
            if apply_date:
                application_info.update({'apply_date':datetime.datetime.strptime(apply_date.strip(),'%Y-%m-%d'),'status':u'贷款申请'})
            g.db_session.query(Application).filter(Application.id==app_id).update(application_info)#
        else:
            customer = kwargs.get('customer')
            cust = g.db_session.query(Customer).filter(Customer.party_id == customer.get('id')).first()
            for k in transaction_info.keys():
                if transaction_info.get(k) == None:
                    transaction_info.pop(k)
                elif transaction_info.get(k) == []:
                    transaction_info.pop(k)
            transaction_info.pop('transaction_type')
            trans_id = transaction_info.get('transaction_id')
            transaction_info.pop('transaction_id')
            application_info.update({
                'status':u'转贷大表申请',
                'customer_id' : cust.role_id,
                'product_code':product_code,
                'standard_rate':self.convert_big(application_info['standard_rate']) if application_info.has_key('standard_rate') else 0,
                'rate_float':self.convert_big(application_info['rate_float']) if application_info.has_key('rate_float') else 0,
                'execute_rate':self.convert_big(application_info['execute_rate']) if application_info.has_key('execute_rate') else 0,
            })
            a=Application(**application_info)
            at = ApplicationTransaction(transaction_name=cust.party.name+u'的转贷大表申请',amount=transaction_info.get('amount'),currency_code=transaction_info.get('currency_code'),transaction_timestamp=datetime.datetime.now(),application=a)
            g.db_session.add(at)
            start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"转贷大表流程").first()
            g.db_session.query(CommercialHouseCredit).filter(CommercialHouseCredit.transaction_id == trans_id).update({'transaction_id':at.transaction_id,'status':'转贷申请'})
 
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
        g.db_session.flush()
        task_list = task.get_task(at)
        next_step = []
        for t in task_list:
              if t.finished==None:
                  role=get_parameter(t.activity,u"角色")
                  rst=g.db_session.query(UserGroup).join(Group,UserGroup.group_id==Group.id).filter(Group.group_name==role).all() 
                  users =[{'user_name': r.user.user_name,'name':r.user.name} for r in rst ] 
                  next_step.append({'activity':t.activity,'role':role,'users':users})
        return {'next_step':next_step} 

    def same_bus_submit(self,**kwargs):
        form_data = kwargs.get('form_data')
        application = form_data.get('application_info')
        transaction_info = form_data.get('transaction_info')
        product_code = form_data.get('product_code')
        application.update({'product_code':product_code,'status':u'同业申请'})
        transaction_info.update({'transaction_timestamp':datetime.datetime.now(),
            'currency_code':transaction_info.get('currency_code') or 'CNY',}
        )
        
        a = Application(**application)
        at=ApplicationTransaction(transaction_name=u"同业业务申请",application=a,**transaction_info)
        g.db_session.add(at)
        g.db_session.commit()
        #同业列表更新
        if kwargs.get('contracts'):
            for v in kwargs.get('contracts'):
                v.update({'application_id':a.id})
                print v
                ddd = InterbankLend(**v)
                g.db_session.add(ddd)
        g.db_session.commit()
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"同业业务流程").first()
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
        return {'success':True}

    def same_bus_con(self,**kwargs):
        product_code = kwargs.get('product_code')
        if(product_code == '801'):
            name = 'TYCF'
        elif(product_code == '802'):
            name = 'CFTY'
        elif(product_code == '803'):
            name = 'TYCR'
        elif(product_code == '804'):
            name = 'CFTY'
        elif(product_code == '805'):
            name = 'ZQZHG'
        elif(product_code == '806'):
            name = 'ZQNHG'
        elif(product_code == '807'):
            name = 'TYCD'
        elif(product_code == '808'):
            name = 'MZTX'
        elif(product_code == '809'):
            name = 'MDPZTX'
        elif(product_code == '811'):
            name = 'HZTX'
        elif(product_code == '812'):
            name = 'HDPZTX'
        elif(product_code == '813'):
            name = 'XYCK'
        else:
            name = 'FYCK'
        if name != 'TYCD':
            date = time.strftime('%Y%m%d',time.localtime(time.time()))
        else:
            date = time.strftime('%Y',time.localtime(time.time()))
        contract_no = '%s%s'%(name,date)
        contract_no =contract_no + "%"
        print contract_no 
        count=g.db_session.query(Contract).filter(Contract.contract_no.like(contract_no)).count()
        count = count + 1
        #count=g.db_session.query(Contract).count()
        if name != 'TYCD':
            if count<10:
                count = '0%d'%(count)
        else:
            if count<10:
                count = '00%d'%(count)
            else:
                count = '0%d'%(count)
        contract = {}
        contract_no = '%s%s%s'%(name,date,count)
        contract.update({'contract_no':contract_no})
        ddd = Contract(**contract)
        g.db_session.add(ddd)
        g.db_session.commit()
        return contract_no

    def same_branch(self):
        branch = g.db_session.query(Branch).all()
        return branch

    def saveapprove (self,**kwargs):
        application = kwargs.get('application_info')
        transaction =kwargs.get('transaction_info')
        product_code = kwargs.get('product_code')
        #application.update({'product_code':product_code,'status':u'投资申请'})
        application_id=application.get('id')
        if application_id:
           application.pop('id')
        else:
           application.update({'product_code':product_code,'status':u'投资申请'})
        a = Application(**application)
        am=transaction.get('amount')
        at=ApplicationTransaction(transaction_name=u"投资申请",amount=am,application=a)
        if application_id:
           g.db_session.query(Application).filter(Application.id == application_id).update(application)
        else:
           g.db_session.add(at)

    def invest_submit(self,**kwargs):
        application_id=kwargs.get('applicationId')
        at = g.db_session.query(ApplicationTransaction).filter(ApplicationTransaction.application_id == application_id).first()
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"投资流程").first()
        start(at, start_activity)
        g.db_session.commit()

        user = g.web_session.user
        groups = []
        for group in user.user_groups:
            groups.append(group.group.group_name)
        task_list = task.get_task(at)
        flag = True
        for t in task_list:
            role = get_parameter(t.activity,u"角色")
            if role and role in groups:
                t.user = user
                t.active()
                t.finish()
                flag=False
                g.db_session.query(Application).filter(Application.id == application_id).update({Application.status:t.activity.activity_name})
        if flag:
            return {'success':False,'msg':u'您已签署意见'}
        g.db_session.commit()
        task_list = task.get_task(at)
        next_step = []
        for t in task_list:
              if t.finished==None:
                  role=get_parameter(t.activity,u"角色")
                  rst=g.db_session.query(UserGroup).join(Group,UserGroup.group_id==Group.id).filter(Group.group_name==role).all()
                  users =[{'user_name': r.user.user_name,'name':r.user.name} for r in rst ]
                  next_step.append({'activity':t.activity,'role':role,'users':users})
        return {'success':True,'next_step':next_step}
        """
        以前的投资提交方法 。。。。。。。。。。。
        application = kwargs.get('application_info')
        transaction =kwargs.get('transaction_info')
        product_code = kwargs.get('product_code')
        print kwargs
        application.update({'product_code':product_code,'status':u'投资申请'})
        '''
        transaction_info.update({'transaction_timestamp':datetime.datetime.now(),
            'currency_code':transaction_info.get('currency_code') or 'CNY',}
        )
        '''
        application_id=application.get('id')
        if application_id:
           application.pop('id')
        a = Application(**application)
        am=transaction.get('amount')
        #at=ApplicationTransaction(transaction_name=u"投资申请",application=a)
        at=ApplicationTransaction(transaction_name=u"投资申请",amount=am,application=a)
        if application_id:
           g.db_session.query(Application).filter(Application.id == application_id).update(application)
        else:
           g.db_session.add(at)
        g.db_session.commit()
        
        application = kwargs.get('application_info')
        a_id=application.get('id')
        at=ApplicationTransaction(transaction_name=u"投资申请",application_id = a_id)
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"投资流程").first()
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
        return {'success':True}
        """

    def update(self,**kwargs):
        application_info = kwargs.get('application_info')
        transaction_info =  kwargs.get('transaction_info')
        application_id = application_info.get('id')
        transaction_id = transaction_info.get('transaction_id')
        ap = g.db_session.query(Application).filter(Application.id==application_id)
        ap.update(application_info)
        tr = {'currency_code':transaction_info.get('currency_code') or 'CNY','amount':transaction_info.get('amount')}
        g.db_session.query(Transaction).filter(Transaction.transaction_id ==transaction_id).update(tr)
        return {'success':True}

    def query_application_list(self, application_status=None,cust_type=None, cust_name=None, guarantee_type=None, lend_type=None, ld_ratio=None, start_date=None, end_date=None):
        u''' 查询申请列表 '''
        q = g.db_session.query(Application, ApplicationTransaction,TransactionActivity,Activity,Customer, User,Task ,Branch)\
                .join(ApplicationTransaction,ApplicationTransaction.application_id == Application.id)\
                .outerjoin(TransactionActivity, TransactionActivity.transaction_id==ApplicationTransaction.transaction_id) \
                .outerjoin(Activity, Activity.activity_id==TransactionActivity.activity_id)\
                .outerjoin(ApplicationTransaction,ApplicationTransaction.transaction_id==TransactionActivity.transaction_id)\
                .join(Task, Task.transaction_activity_id==TransactionActivity.transaction_activity_id) \
                .outerjoin(Customer,Customer.role_id==Application.customer_id)\
                .outerjoin(Party,Customer.party_id==Party.id)\
                .outerjoin(Branch, Branch.role_id == Application.apply_branch_id)\
                .outerjoin(User, User.role_id == Application.apply_user_id)\
                .filter(TransactionActivity.transaction_activity_type=="task")\
                .order_by(Task.transaction_activity_id.desc())

        status=''
        activity_name=()
        activity_status=()
        application_status=application_status[0]
        if application_status == u'未发送申请书':
            status=u'暂存'
            activity_name = (u'撰写调查报告',u'放款申请')
        elif application_status == u'需补充资料申请书':
            activity_status = (u'需补充资料',)
        elif application_status == u'审议中申请书':
            activity_status(u'审议',)
        elif application_status == u'审议通过申请书' and application_status == u'审批中申请书':
            activity_status(u'审批',)
        elif application_status == u'已归档申请书':
            activity_status = (u'归档',)
        if bool(application_status != u'新增申请'):
            q = q.filter(Application.status==status)
        if cust_type:
            print cust_type
            q = q.filter(Customer.cust_type == cust_type[0])
        if cust_name:
            q = q.filter(Party.name.like('%'+cust_name[0]+'%'))
        if lend_type:
            q = q.filter(Application.product_code==lend_type[0])
        rtn_data = []
        user = g.web_session.user
        groups = []
        for group in user.user_groups:
            groups.append(group.group.group_name)
        application_id_list=[] 
        for a in q.all():
            at = a.TransactionActivity
            if (a.Task.user == user  or (at.finished==None and get_parameter(a.Activity,u"角色") in  groups)) and a.Application.id not in application_id_list :
                t = g.db_session.query(Activity)\
                    .join(TransactionActivity, Activity.activity_id==TransactionActivity.activity_id)\
                    .join(ApplicationTransaction,ApplicationTransaction.transaction_id==TransactionActivity.transaction_id)\
                    .join(Task, Task.transaction_activity_id==TransactionActivity.transaction_activity_id) \
                    .filter(TransactionActivity.finished==None) \
                    .filter(TransactionActivity.transaction_activity_type=="task")\
                    .filter(ApplicationTransaction.application_id==a.Application.id)

                if bool(application_status != u'新增申请'):
                    t = t.filter(Activity.activity_name.in_(activity_name))\
                         .filter(Activity.activity_status.in_(activity_status))
                now_status =''
                acti_status=''
                for activity in t.all():
                    acti_status=activity.activity_status  
                    now_status += activity.activity_name +'\n'     
                detail={
                    'id':a.Application.id,
                    'party':a.Application.customer.party,
                    'product':a.Application.product,
                    'activity_status':acti_status,
                    'activity_page':a.Activity.activity_page,
                    'role':get_parameter(a.Activity,u"角色"),
                    'transaction_id':a.ApplicationTransaction.transaction_id,
                    'application_status':now_status if now_status else a.Application.status,
                    'currency':a.ApplicationTransaction.currency_code if bool(a.ApplicationTransaction) else '',
                    'main_gua_type':a.Application.main_gua_type if bool(a.Application) else '',
                    'amount':a.ApplicationTransaction.amount if bool(a.ApplicationTransaction) else '',
                    'apply_user':a.User.user_name if bool(a.User) else '',
                    'apply_branch':a.Branch.branch_name if bool(a.Branch) else '',
                    'cancelable_flag':False,
                    'write_survey_report_flag':True if bool(a.Application.survey_report_id) else False,
                    'survey_report_id':a.Application.survey_report_id if bool(a.Application.survey_report_id) else '',
                }
                rtn_data.append(detail)
                application_id_list.append(a.Application.id)
        return rtn_data

    def query_sames(self,opponent_name=None,amount=None,status=None):

        rts = g.db_session.query(ApplicationTransaction).join(Application,Application.id==ApplicationTransaction.application_id).filter(Application.product_code.like(u'8%')).all()

        return [{'application_info':it.application,'transaction_info':it,'product':it.application.product } for it in rts]

    def query_invest(self,bus_type=None,pj_type=None,openning_bank=None,open_name=None,account=None,big_num=None):
        rts = g.db_session.query(ApplicationTransaction).join(Application,Application.id==ApplicationTransaction.application_id).filter(Application.product_code.like(u'705%')).all()
        return [{'application_info':it.application,'transaction_info':it,'product':it.application.product} for it in rts]

    def query_application_detail(self, application_id):
        u''' 查询申请详情 '''
        rst = g.db_session.query(Application,Activity,ApplicationTransaction, User, Branch, ApplicationComment)\
                .join(Customer, Customer.role_id == Application.customer_id)\
                .join(ApplicationTransaction,ApplicationTransaction.application_id==Application.id)\
                .outerjoin(TransactionActivity, TransactionActivity.transaction_id==ApplicationTransaction.transaction_id) \
                .outerjoin(Activity, Activity.activity_id==TransactionActivity.activity_id)\
                .outerjoin(User, User.role_id == Application.apply_user_id)\
                .outerjoin(Branch, Branch.role_id == Application.apply_branch_id)\
                .outerjoin(ApplicationComment, ApplicationComment.application_id == Application.id)\
                .outerjoin(Task, Task.transaction_activity_id==TransactionActivity.transaction_activity_id) \
                .filter(TransactionActivity.finished==True) \
                .filter(TransactionActivity.transaction_activity_type=="task") \
                .filter(Application.id==application_id).order_by(Activity.activity_id.desc()).first()

        application_detail = {}
        if bool(rst):
            application_detail = {
                'currency':rst.ApplicationTransaction.currency_code if bool(rst.ApplicationTransaction) else '',
                'amount':rst.ApplicationTransaction.amount if bool(rst.ApplicationTransaction) else '',
                'party':rst.Application.customer.party,
                'product':rst.Application.product,
                'sign_comment_flag':True if bool(rst.ApplicationComment) else False,
                'survey_end_date':rst.Application.survey_report.end_date if bool(rst.Application.survey_report) else '',
                'write_survey_report_flag':True if bool(rst.Application.survey_report_id) else False,
                'archived_flag':False if bool(rst.Application.status != 'archived') else True,
                'activity':rst.Activity,
                
            }
        return application_detail


    def query(self,application_id):
        u''' 贷款查询数据   '''
        rst = g.db_session.query(ApplicationTransaction)\
            .filter(ApplicationTransaction.application_id == application_id).first()
        inter = g.db_session.query(InterbankLend).filter(InterbankLend.application_id == application_id).all()
        inter_list=[]
        if inter:
            for r in inter:
                it = r.__dict__
                #去除转字典生成的项
                if it.get('_sa_instance_state'):
                    it.pop('_sa_instance_state')
                inter_list.append(it)

        application_info = rst.application.__dict__
        transaction_info = rst.__dict__
        app_info = {}
        for k in application_info.keys():
            if application_info.get(k) != None:
                app_info.update({k:application_info.get(k)})
        tran_info = {}
        for k in transaction_info.keys():
            if transaction_info.get(k) != None:
                tran_info.update({k:transaction_info.get(k)})
        product = rst.application.product
        sur_rep = rst.application.survey_report
        cur_resp_end_date = None
        if sur_rep:
            cur_resp_end_date = sur_rep.end_date  
        if app_info.get('_sa_instance_state'):
            app_info.pop('_sa_instance_state')
        if tran_info.get('_sa_instance_state'):
            tran_info.pop('_sa_instance_state')
        rt =  {'transaction_info':tran_info,'application_info':app_info,'product':product,'end_date':cur_resp_end_date,'list':inter_list}
        return rt 

    def products(self,product_type):
        data_ls = []
        product_types = g.db_session.query(ProductType).filter(ProductType.business_type==product_type).all();
        for product_type in product_types:
            products = g.db_session.query(Product).filter(Product.product_type_code==product_type.code).all()
            data_ls.append({"product_type":product_type,"products":products})
        return data_ls


    def query_nodone_deal(self,user):
        u''' 查询贷款待办事务 '''
        done_list = []
        credit_table = []
        groups = []
        for group in user.user_groups:
            groups.append(group.group.group_name)

        application_transaction = ApplicationTransaction.__table__

        result_set = g.db_session.query(Application, Activity \
            ,Transaction.amount,Activity.activity_name \
            ,Transaction.transaction_id, Application.id, Product.product_code, Product.name, Product.product_page) \
            .outerjoin(application_transaction, application_transaction.c.application_id==Application.id) \
            .outerjoin(Transaction, Transaction.transaction_id==ApplicationTransaction.transaction_id) \
            .outerjoin(Product, Product.product_code==Application.product_code) \
            .outerjoin(TransactionActivity, TransactionActivity.transaction_id==ApplicationTransaction.transaction_id) \
            .outerjoin(Activity, Activity.activity_id==TransactionActivity.activity_id) \
            .filter(TransactionActivity.finished==None) \
            .filter(TransactionActivity.transaction_activity_type=="task").all()


        for item in result_set:
            role = get_parameter(item[1],u"角色")
            if role and role in groups:
                party = item[0].customer.party if item[0].customer and item[0].customer.party else Party()
                amount = str(decimal.Decimal(item[2]).quantize(Decimal('0.00'))) if item[2] else '0.00'
                done_list.append({'role':role,'amount':amount,'party_id':party.id,'cust_no':party.no, "cust_name":party.name,'type_code':party.type_code \
                    , "activity":item[1], "transaction_id":item[4], "application_id":item[5] \
                    , "product_code":item[6], "product_name":item[7],'product_page':item[8]})

        data={}
        data['done_list']=done_list
        if u'客户经理' in groups and credit_table == []:
             comms = g.db_session.query(CommercialHouseCredit).filter(CommercialHouseCredit.status == None).all()
             if comms:
                 credit_table=[{'transaction':comm.transaction,'application':comm.transaction.application,'cust':comm.transaction.application.customer,'party':comm.transaction.application.customer.party,'status':comm.status} for comm in comms]
        data['credit_table']=credit_table
        return data

    def query_done_deal(self, user):
        u''' 查询贷款已办事务 '''

        application_transaction = ApplicationTransaction.__table__

        result_set = g.db_session.query(Application, Activity \
            ,Transaction.amount,Activity.activity_name \
            ,Transaction.transaction_id, Application.id, Product.product_code, Product.name, Product.product_page,Task.user_id) \
            .outerjoin(application_transaction, application_transaction.c.application_id==Application.id) \
            .outerjoin(Transaction, Transaction.transaction_id==ApplicationTransaction.transaction_id) \
            .outerjoin(Product, Product.product_code==Application.product_code) \
            .outerjoin(TransactionActivity, TransactionActivity.transaction_id==ApplicationTransaction.transaction_id) \
            .outerjoin(Activity, Activity.activity_id==TransactionActivity.activity_id) \
            .outerjoin(Task, Task.transaction_activity_id==TransactionActivity.transaction_activity_id) \
            .filter(TransactionActivity.finished==True) \
            .filter(TransactionActivity.transaction_activity_type=="task") \
            .filter(Task.user_id==user.role_id).order_by(Activity.activity_id.desc()).all()

        done_list = []
        credit_table = []
        transaction_list = []
        for item in result_set:
            if item[4] not in transaction_list:
                transaction_list.append(item[4])
                amount = str(decimal.Decimal(item[2]).quantize(Decimal('0.00'))) if item[2] else '0.00'
                party = item[0].customer.party if item[0].customer and item[0].customer.party else Party()
                done_list.append({'amount':amount,'party_id':party.id,'cust_no':party.no, "cust_name":party.name,'type_code':party.type_code \
                    , "activity":item[1], "transaction_id":item[4], "application_id":item[5] \
                    , "product_code":item[6], "product_name":item[7],'product_page':item[8]}) 
        """
        comm = g.db_session.query(CommercialHouseCredit).filter(CommercialHouseCredit.transaction_id==trans.transaction_id,CommercialHouseCredit.status !=u'结束').first()
        if comm:
             credit_table.append({'application':comm.transaction.application,'transaction':comm.transaction,'party':comm.transaction.application.customer.party,'cust':comm.transaction.application.customer,'status':comm.status})
        """
        data={}
        data['done_list']=done_list
        data['credit_table']=credit_table
        return data

    def comm_credit(self,application_id):
        u'''加入转贷大表'''
        at,comm= g.db_session.query(ApplicationTransaction,CommercialHouseCredit).outerjoin(CommercialHouseCredit,ApplicationTransaction.transaction_id == CommercialHouseCredit.transaction_id).filter(CommercialHouseCredit.status == None).filter(ApplicationTransaction.application_id == application_id).first()
        if comm:
            return json.dumps({'status':'error','msg':'该贷款已存在'})
        else:
            credit=CommercialHouseCredit(transaction_id=at.transaction_id)
            g.db_session.add(credit)
            g.db_session.commit()
            return json.dumps({'status':'success','msg':'转入成功'})


