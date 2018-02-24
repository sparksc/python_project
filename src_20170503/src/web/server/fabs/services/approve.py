# -*- coding: utf-8 -*-
"""
    yinsho.services.ApproveService
    #####################

    yinsho ApproveService module
"""

from flask import json, g
from ..model.customer import *
from ..model.party import *
from ..model.guarantee import *
from ..model.contract import *
from ..model.application import *
from ..model.approve import *
from ..model.credit import *
from ..model.branch import *
from ..model.user import *
from ..workflow import task
from ..workflow.parameter import *
from .service import BaseService
from ..base.xlsutil import write_cell
import xlwt
import xlrd
from xlutils.copy import copy
import datetime,time

class ApproveService(BaseService):
    __model__ = User
    
    def approve_flag(self,application_id, **kwargs):  
        u''' 签署结果 信息必填判断'''
        application_status=kwargs.get('application_status')
        if application_status:
           kwargs.pop('application_status')
        u''' 撰写调查报告部分判断'''
        st = g.db_session.query(GuaranteeInfo).filter(GuaranteeInfo.application_id == application_id).first()
        survey = g.db_session.query(Application).filter(Application.id == application_id).first()
        ta=g.db_session.query(ApplicationTransaction).filter(ApplicationTransaction.application_id == application_id).first()
        con=g.db_session.query(TransactionContractRelation).join(LendTransaction,TransactionContractRelation.transaction_id == LendTransaction.transaction_id).filter(LendTransaction.application_transaction_id == ta.transaction_id).all()
        if application_status == '放款申请':
           pay_if = None
        print con
        for j in con:
           print '*******'
           print j
           pay=g.db_session.query(Payment).join(Debt,Payment.debt_id == Debt.id).filter(Debt.contract_id == j.contract_id).first()
           print pay
           if pay != None:
              pay_if = pay
              
        if application_status:
           if application_status == '撰写调查报告':
              if st == None:
                 return {'error':u'担保信息未填写'}
              if st.state == None:
                 return {'error':u'请完善担保信息'}
              if survey.survey_report_id == None:
                 return {'error':u'请提交调查报告'}
           if application_status == '放款申请':
              info=g.db_session.query(GuaranteeContractRelation).join(GuaranteeInfo,GuaranteeContractRelation.gty_info_id == GuaranteeInfo.id).filter(GuaranteeInfo.application_id == application_id).all()
              gty=g.db_session.query(GuaranteeInfo).filter(GuaranteeInfo.application_id == application_id).all()
              for i in gty:
                  if i.register_number == None:
                     return {'error':u'请检查并补全担保登记证号'}
                  if i.register_date == None:
                     return {'error':u'请检查并补全担保登记日期'}
              if info == None:
                 return {'error':u'请先生成担保合同'}
              if pay_if == None:
                 return {'error':u'未支付，请支付'}
        return {'success':u'正确'}
         

    def approve(self, application_id, **kwargs):
        u''' 审查审批 '''
        at = g.db_session.query(ApplicationTransaction).filter(ApplicationTransaction.application_id == application_id).first()
        a = at.application
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
                kwargs.update({
                    'application':a,
                    'user':user,
                    'transaction_activity':t,
                    'comment_date':datetime.datetime.now()
                })
                g.db_session.add(ApplicationComment(**kwargs))
                t.user = user
                flag=False
                t.active()
                t.finish()
                g.db_session.query(Application).filter(Application.id == application_id).update({Application.status:t.activity.activity_name})
        if flag:
            return {'success':False,'msg':u'您已签署意见'} 
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

    def get_next(self,application_id):
        at = g.db_session.query(ApplicationTransaction).filter(ApplicationTransaction.application_id == application_id).first()
        task_list = task.get_task(at)
        next_step = []
        for t in task_list:
              if t.finished==None:
                  role=get_parameter(t.activity,u"角色")
                  rst=g.db_session.query(UserGroup).join(Group,UserGroup.group_id==Group.id).filter(Group.group_name==role).all() 
                  users =[{'user_name': r.user.user_name,'name':r.user.name} for r in rst ] 
                  next_step.append({'activity':t.activity,'role':role,'users':users})
        return {'next_step':next_step} 


    def approve_info(self, application_id):
        u''' 审批历史 '''

        rst = g.db_session.query(ApplicationComment).filter(ApplicationComment.application_id == application_id).order_by(ApplicationComment.comment_date).all()
        rtn_value = [{'comment':r, 'activity':r.transaction_activity.activity,'role':get_parameter(r.transaction_activity.activity,u"角色"),'user':r.user} for r in rst]
        return rtn_value

    def save_report(self,application_id):
        u'''生成审批表'''
        rst = g.db_session.query(ApplicationTransaction,LendTransaction).outerjoin(LendTransaction,ApplicationTransaction.transaction_id == LendTransaction.application_transaction_id).filter(ApplicationTransaction.application_id ==application_id).first()
        lend_trans = rst.LendTransaction
        app=rst.ApplicationTransaction.application
        trans = rst.ApplicationTransaction
        cust=app.customer
        if cust:
            party=cust.party
        homedir = os.getcwd()
        xls_path=homedir+'/fabs/static/approval_report/'
        if app.product_code[:1] == '8':
            rb = xlrd.open_workbook(xls_path+'same_business_approve.xls',formatting_info=True)
            wb = copy(rb)
            wb.encoding = 'utf-8'
            sh = wb.get_sheet(0)
            write_cell(sh, 0, 1, unicode('%s'%(time.strftime(u'%Y年%m月%d日',time.localtime(time.time()))))) 
            write_cell(sh, 1, 4, unicode('%s'%(app.product.name)))
            write_cell(sh, 1, 5, unicode('%s'%(app.opponent_name)))
            write_cell(sh, 1, 6, unicode('%s元'%(trans.amount)))
            write_cell(sh, 3, 8, unicode('%s'%(g.web_session.user.name)))
            rst = self.approve_info(application_id)
            for r in rst:
                 if r.get('role') == u'资金部负责人':
                      write_cell(sh, 3,9, unicode('%s  %s'%(r.get('comment').comment_type,r.get('comment').comment if  r.get('comment').comment else '')))
                 if r.get('role') == u'资金部风险岗':
                      write_cell(sh, 3,10, unicode('%s  %s'%(r.get('comment').comment_type,r.get('comment').comment if  r.get('comment').comment else '')))
                 if r.get('role') == u'分管同业副行长':
                      write_cell(sh, 3,11, unicode('%s  %s'%(r.get('comment').comment_type,r.get('comment').comment if  r.get('comment').comment else '')))
            report_filename = xls_path+'same_business_approve_%s.xls'%(application_id)
            wb.save(report_filename)
            file_path = 'static/approval_report/same_business_approve_%s.pdf '%(application_id)
        elif app.product_code == '705':
            rb = xlrd.open_workbook(xls_path+'invest_approve.xls',formatting_info=True)
            wb = copy(rb)
            wb.encoding = 'utf-8'
            sh = wb.get_sheet(0)
            write_cell(sh, 0, 1, unicode('%s'%(time.strftime(u'%Y年%m月%d日',time.localtime(time.time())))))
            write_cell(sh, 1, 4, unicode('%s'%(app.bus_type)))
            write_cell(sh, 1, 6, unicode('%s'%(app.openning_bank)))
            write_cell(sh, 1, 7, unicode('%s元'%(trans.amount)))
            write_cell(sh, 1, 8, unicode('%s'%(app.open_name)))
            write_cell(sh, 1, 9, unicode('%s'%(app.account)))
            write_cell(sh, 1, 10, unicode('%s'%(app.big_num)))
            rst = self.approve_info(application_id)
            for r in rst:
                 if r.get('role') == u'资金部负责人':
                      write_cell(sh,3 ,11, unicode('%s  %s'%(r.get('comment').comment_type, r.get('comment').comment if  r.get('comment').comment else '')))
                 if r.get('role') == u'财务部负责人':
                      write_cell(sh, 3,12, unicode('%s  %s'%(r.get('comment').comment_type, r.get('comment').comment if r.get('comment').comment else '')))
                 if r.get('role') == u'总行风险负责人':
                      write_cell(sh, 3,13, unicode('%s  %s'%(r.get('comment').comment_type, r.get('comment').comment if r.get('comment').comment else '')))
                 if r.get('role') == u'分管资金副行长':
                      write_cell(sh,3 ,14, unicode('%s  %s'%(r.get('comment').comment_type,r.get('comment').comment if r.get('comment').comment else '')))
                 if r.get('role') == u'投资审议委员会':
                      write_cell(sh, 4,15, unicode('%s  %s'%(r.get('comment').comment_type,r.get('comment').comment if r.get('comment').comment else '' )))
                 if r.get('role') == u'总行行长':
                      write_cell(sh, 3,16, unicode('%s  %s'%(r.get('comment').comment_type,r.get('comment').comment if r.get('comment').comment else '')))


            report_filename = xls_path+'invest_approve_%s.xls'%(application_id)
            wb.save(report_filename) 
            file_path = 'static/approval_report/invest_approve_%s.pdf '%(application_id)
        else:     
            rb = xlrd.open_workbook(xls_path+'branch_approval.xls',formatting_info=True)
            wb = copy(rb)
            wb.encoding = 'utf-8'
            sh = wb.get_sheet(0)
            write_cell(sh, 1, 3, unicode('%s'%(party.name)))
            if party.type_code == 'company':
                 write_cell(sh, 3, 3, unicode('%s'%(party.corp_name)))
            if party.type_code == 'resident':
                 write_cell(sh, 3, 3, unicode('%s'%(party.name)))
            write_cell(sh, 3, 5, unicode('%s'%(app.product.name)))
            write_cell(sh, 5, 5, unicode('%s'%(lend_trans.execute_rate)))
            write_cell(sh, 1, 8, unicode('%s-%s'%(lend_trans.from_date,lend_trans.thur_date)))
            write_cell(sh, 4, 8, unicode('%s'%(lend_trans.amount)))
            write_cell(sh, 1, 9, unicode('%s'%(lend_trans.main_gua_type)))
            rst = self.approve_info(application_id)
            for r in rst:
                 if r.get('role') == u'支行审贷小组':
                      write_cell(sh, 1,12, unicode('%s  %s'%(r.get('comment').comment_type,r.get('comment').comment if  r.get('comment').comment else '')))
                 if r.get('role') == u'支行行长':
                      write_cell(sh, 1,18, unicode('%s  %s'%(r.get('comment').comment_type,r.get('comment').comment if  r.get('comment').comment else '')))
            
            report_filename = xls_path+'%s.xls'%(application_id)
            wb.save(report_filename)
            file_path = 'static/approval_report/branch_approval_%s.pdf '%(application_id)
        os.system('unoconv -f pdf -o ../web/fabs/%s %s '%(file_path,report_filename))
        #if os.path.exists('%s/../web/fabs/%s'%(homedir,file_path)):
        return {'success':True,'src':file_path}


 
        return {'success':True }       

    def bat_approve(self,**kwargs):
        u''' 审查审批 '''
        application = kwargs.get('application')
        for app in application:
            a = app.get('application')
            self.approve(a.get('id'))
            g.db_session.query(CommercialHouseCredit).filter(CommercialHouseCredit.application_id==a.get('id')).update({'status':'审批'})
        g.db_session.commit()
        return {'success':True}

    def query_risk(self,application_id):
        u'''查询风险评价内容 '''
        risk_info =g.db_session.query(RiskApprove).filter(RiskApprove.application_id==application_id).first() 
        if risk_info:
            risk_info = risk_info.__dict__
            if risk_info.get('_sa_instance_state'):
                   risk_info.pop('_sa_instance_state')        
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
                flag=False
        return{'risk_info':risk_info,'flag':flag}        



    def save_risk(self,**kwargs):
        u''' 保存风险评价内容'''
        risk_approve=RiskApprove(**kwargs)
        g.db_session.add(risk_approve)
        g.db_session.commit()        
        return {'id':risk_approve.id}
     
    def update_risk(self,**kwargs):
        u''' 更新风险评价内容'''
        id = kwargs.get('id')
        kwargs.pop('id')
        g.db_session.query(RiskApprove).filter(RiskApprove.id==id).update(kwargs)
        g.db_session.commit()        
        return {'success':True}


    def save_risk_report(self,risk_id):
        u'''生成风险评价表'''
        rst = g.db_session.query(RiskApprove).filter(RiskApprove.id ==risk_id).first()
        at=g.db_session.query(ApplicationTransaction).filter(ApplicationTransaction.application_id ==rst.application_id).first()
        trans=at
        app=at.application
        homedir = os.getcwd() 
        xls_path=homedir+'/fabs/static/approval_report/'
        rb = xlrd.open_workbook(xls_path+'risk_approve_%s.xls'%(rst.cust_type),formatting_info=True)
        wb = copy(rb)
        sh = wb.get_sheet(0)
        if rst.cust_type=='resident':
              write_cell(sh, 1, 3, unicode('%s'%(app.customer.party.name)))
              write_cell(sh, 1, 4, unicode('%s'%(app.main_gua_type)))
              write_cell(sh, 1, 6, unicode('%s'%(trans.amount)))
              write_cell(sh, 1, 7, unicode('%s'%(app.term_month)))
              write_cell(sh, 1, 8, unicode('%s'%(app.purpose_type)))

              write_cell(sh, 2, 10, unicode('%s'%(rst.id_flag)))
              write_cell(sh, 2, 12, unicode('%s'%(rst.age_flag)))
              write_cell(sh, 2, 14, unicode('%s'%(rst.income_flag)))
              write_cell(sh, 2, 16, unicode('%s'%(rst.payment_flag)))
              write_cell(sh, 2, 18, unicode('%s'%(rst.policy_flag)))
              write_cell(sh, 2, 20, unicode('%s'%(rst.relation_flag)))
              write_cell(sh, 5, 3, unicode('%s'%(rst.purpose_flag)))
              write_cell(sh, 5, 5, unicode('%s'%(rst.credit_inv_flag)))
              write_cell(sh, 5, 8, unicode('%s'%(rst.guarantee_flag)))
              write_cell(sh, 5, 10, unicode('%s'%(rst.warr_per_flag)))
              write_cell(sh, 5, 12, unicode('%s'%(rst.risk_memo)))
              write_cell(sh, 3, 16, unicode('%s'%(rst.remark)))
        if rst.cust_type=='company':
              write_cell(sh, 1, 2, unicode('%s'%(app.customer.party.name)))
              write_cell(sh, 1, 3, unicode('%s'%(app.main_gua_type)))
              write_cell(sh, 1, 7, unicode('%s'%(trans.amount)))
              write_cell(sh, 1, 8, unicode('%s'%(app.term_month)))
              write_cell(sh, 1, 9, unicode('%s'%(app.purpose_type)))
              write_cell(sh, 2, 12, unicode('%s'%(rst.id_flag)))
              write_cell(sh, 2, 14, unicode('%s'%(rst.main_flag)))
              write_cell(sh, 2, 16, unicode('%s'%(rst.product_policy_flag)))
              write_cell(sh, 2, 18, unicode('%s'%(rst.ela_flag)))
              write_cell(sh, 2, 20, unicode('%s'%(rst.customer_rel_flag)))
              write_cell(sh, 2, 22, unicode('%s'%(rst.relation_flag)))
              write_cell(sh, 5, 4, unicode('%s'%(rst.debt_rate)))
              write_cell(sh, 5, 7, unicode('%s'%(rst.current_ratio)))
              write_cell(sh, 5, 10, unicode('%s'%(rst.quick_ratio)))
              write_cell(sh, 5, 14, unicode('%s'%(rst.protection_degree)))
              write_cell(sh, 5, 17, unicode('%s'%(rst.purpose_flag)))
              write_cell(sh, 5, 19, unicode('%s'%(rst.credit_inv_flag)))
              write_cell(sh, 5, 22, unicode('%s'%(rst.guarantee_flag)))
              write_cell(sh, 5, 23, unicode('%s'%(rst.warr_per_flag)))
              write_cell(sh, 8, 2, unicode('%s'%(rst.risk_memo)))
              write_cell(sh, 6, 6, unicode('%s'%(rst.remark)))
              
        report_filename = xls_path+'risk_%s.xls'%(risk_id)
        wb.save(report_filename)
        file_path = 'static/approval_report/risk_%s.pdf '%(risk_id)
        os.system('unoconv -f pdf -o ../web/fabs/%s %s '%(file_path,report_filename))
        g.db_session.query(RiskApprove).filter(RiskApprove.id == risk_id).update({'file_path':file_path})
        return {'success':True,'src':file_path}


    def query_examine(self,application_id):
        u'''查询审查内容 '''
        examine_info =g.db_session.query(ExamineApprove).filter(ExamineApprove.application_id==application_id).first() 
        if examine_info:
            examine_info = examine_info.__dict__
            if examine_info.get('_sa_instance_state'):
                   examine_info.pop('_sa_instance_state')
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
                flag=False      
        return{'examine_info':examine_info,'flag':flag}

    def save_examine(self,**kwargs):
        u''' 保存审查内容'''
        examine_approve=ExamineApprove(**kwargs)
        g.db_session.add(examine_approve)
        g.db_session.commit()        
        return {'id':examine_approve.id}
     
    def update_examine(self,**kwargs):
        u''' 更新审查内容'''
        id = kwargs.get('id')
        kwargs.pop('id')
        g.db_session.query(ExamineApprove).filter(ExamineApprove.id==id).update(kwargs)
        g.db_session.commit()        
        return {'success':True}


    def save_examine_report(self,examine_id):
        u'''生成风险评价表'''
        rst = g.db_session.query(ExamineApprove).filter(ExamineApprove.id ==examine_id).first()
        at=g.db_session.query(ApplicationTransaction).filter(ApplicationTransaction.application_id ==rst.application_id).first()
        trans=at
        app=at.application
        user=g.web_session.user
        branch = g.db_session.query(UserBranch).filter(UserBranch.user_id == user.role_id).first()
        homedir = os.getcwd() 
        xls_path=homedir+'/fabs/static/approval_report/'
        rb = xlrd.open_workbook(xls_path+'examine_approve.xls',formatting_info=True)
        wb = copy(rb)
        sh = wb.get_sheet(0)
        write_cell(sh, 1, 1, unicode('%s'%(app.customer.party.name)))
        write_cell(sh, 3, 1, unicode('%s元'%(trans.amount)))
        write_cell(sh, 0, 2, unicode('%s申请的审查意见'%(rst.credit_type)))
        write_cell(sh, 0, 4, unicode("""根据 %s （支行/分行）提供的对 %s ，贷款金额 %f  万元,%s贷前调查报告及相关资料，根据《乌海银行%s管理办法及操作细则》相关制度有关规定，对该笔贷款进行了审查，意见如下："""%(branch.branch.branch_name,app.customer.party.name,float(trans.amount)/10000,rst.credit_type,rst.credit_type)))
        write_cell(sh, 0, 6, unicode('%s'%(rst.remark)))
        report_filename = xls_path+'examine_%s.xls'%(examine_id)
        wb.save(report_filename)
        file_path = 'static/approval_report/examine_%s.pdf '%(examine_id)
        os.system('unoconv -f pdf -o ../web/fabs/%s %s '%(file_path,report_filename))
        g.db_session.query(ExamineApprove).filter(ExamineApprove.id == examine_id).update({'file_path':file_path})
        return {'success':True,'src':file_path}

