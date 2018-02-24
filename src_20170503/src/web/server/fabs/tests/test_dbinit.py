# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import aliased
import unittest
import json
import time
import logging
from ..model.user import *
from ..model.branch import *
from sys import modules
import datetime
import random

import test_nxcrm_report
import test_tpara

log = logging.getLogger()

class TestInitDb(unittest.TestCase):


    def setUp(self):
        log.debug("start setup XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!")
        self.session=simple_session()
        NXBase.metadata.drop_all(self.session.bind)
        NXBase.metadata.create_all(self.session.bind)
        # self.init_util()
        # self.init_guarantee_method()
        # self.init_product()
        self.init_user_group()
        # self.init_customer()
        # #self.init_branch()
        # self.init_flow()
        # # 对公报表
        # test_report.init_report_data(self.session)

        # # 行业类型
        # test_industry_type.init_industry_data(self.session)

        # # 权限组
        # test_permission.init_permission_data(self.session)
        test_nxcrm_report.init_crm_report_menu_data(self.session)
        #test_tpara.init_para(self.session)

    def test_test(self):
        print 'aaaa'

    def subbranch_flow(self):
        log.debug("start loan subbranch process workflow!")

        start_activity = self.session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"贷款申请流程").first()

        #user = self.session.query(User).filter_by(user_name="00540").first()

        cust = self.session.query(Customer).join(Party, Party.id == Customer.party_id).filter(Party.name == u'李顺义').first()
        application = Application(customer_id=cust.role_id,product_code='101')
        application_transaction = ApplicationTransaction(transaction_name=u"%s的贷款申请"%(cust.party.name),amount = '20000',application=application)
        start_activity.bind_transaction(application_transaction)

        # 贷款申请					客户经理
        user = self.session.query(User).filter_by(user_name="00530").first()
        self.process_task(application_transaction, user)

        # 预审						支行审查岗
        user = self.session.query(User).filter_by(user_name="00779").first()
        self.process_task(application_transaction, user)

        # 撰写调查报告			                客户经理
        user = self.session.query(User).filter_by(user_name="00530").first()
        self.process_task(application_transaction, user)


        # 支行风险评价				支行风险评价岗
        user = self.session.query(User).filter_by(user_name="00140").first()
        self.process_task(application_transaction, user)

        # 支行审查			        支行审查岗
        user = self.session.query(User).filter_by(user_name="00779").first()
        self.process_task(application_transaction, user)

        # 支行审贷小组审议			支行审贷小组
        user = self.session.query(User).filter_by(user_name="00779").first()
        logging.debug(user.role_id)
        self.process_task(application_transaction, user)

        user = self.session.query(User).filter_by(user_name="00513").first()
        logging.debug(user.role_id)
        self.process_task(application_transaction, user)

        user = self.session.query(User).filter_by(user_name="00530").first()
        logging.debug(user.role_id)
        self.process_task(application_transaction, user)

        # 支行长审议				支行行长
        user = self.session.query(User).filter_by(user_name="00136").first()
        self.process_task(application_transaction, user)

        # 放款申请				客户经理
        user = self.session.query(User).filter_by(user_name="00530").first()
        self.process_task(application_transaction, user)

        # 支行长审批				支行行长
        #user = self.session.query(User).filter_by(user_name="00136").first()
        #self.process_task(application_transaction, user)

        # 放款   				客户经理
        user = self.session.query(User).filter_by(user_name="00530").first()
        self.process_task(application_transaction, user)

    def subbranch_commercial_house_credit(self):
        start_activity = self.session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"转贷大表流程").first()

        cust = self.session.query(Customer).join(Party, Party.id == Customer.party_id).filter(Party.name == u'李顺义').first()
        application = Application(customer_id=cust.role_id,product_code='523',status=u'放款')
        application_transaction = ApplicationTransaction(transaction_name=u"%s的转大表申请"%(cust.party.name),amount = '2000000',application=application)
        start_activity.bind_transaction(application_transaction)
        credit=CommercialHouseCredit(transaction_id=application_transaction.transaction_id, status=u'转贷申请')
        self.session.add(credit)
        self.session.commit()

        # 大表申请 客户经理
        user = self.session.query(User).filter_by(user_name="00510").first()
        self.process_task(application_transaction, user)

        # 风险审查
        user = self.session.query(User).filter_by(user_name="00140").first()
        self.process_task(application_transaction, user)

        # 支行审查
        user = self.session.query(User).filter_by(user_name="00779").first()
        self.process_task(application_transaction, user)

        # 支行审贷小组
        user = self.session.query(User).filter_by(user_name="00513").first()
        self.process_task(application_transaction, user)

        # 支行长审查
        user = self.session.query(User).filter_by(user_name="00136").first()
        self.process_task(application_transaction, user)

        # 放款申请
        user = self.session.query(User).filter_by(user_name="00510").first()
        self.process_task(application_transaction, user)

        # 预审
        user = self.session.query(User).filter_by(user_name="00779").first()
        self.process_task(application_transaction, user)

        # 调查报告
        user = self.session.query(User).filter_by(user_name="00510").first()
        self.process_task(application_transaction, user)

        # 支行长审批
        user = self.session.query(User).filter_by(user_name="00136").first()
        self.process_task(application_transaction, user)

        # 放款
        user = self.session.query(User).filter_by(user_name="00510").first()
        self.process_task(application_transaction, user)


    def ho_flow(self):
        log.debug("start ho process workflow!")

        start_activity = self.session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"承兑汇票签发申请流程").first()

        cust = self.session.query(Customer).join(Party, Party.id == Customer.party_id).filter(Party.name == u'刘永霞').first()
        application = Application(customer_id=cust.role_id,product_code='007',bill_type='敞口')
        application_transaction = ApplicationTransaction(transaction_name=u"%s的贷款申请"%(cust.party.name),amount = '20000000',application=application)
        start_activity.bind_transaction(application_transaction)

        # 贷款申请					客户经理
        user = self.session.query(User).filter_by(user_name="00140").first()
        self.process_task(application_transaction, user)

        # 预审						支行审查岗
        user = self.session.query(User).filter_by(user_name="00779").first()
        self.process_task(application_transaction, user)

        # 撰写调查报告			                客户经理
        user = self.session.query(User).filter_by(user_name="00140").first()
        self.process_task(application_transaction, user)

        # 支行风险评价				支行风险评价岗
        #user = self.session.query(User).filter_by(user_name="00140").first()
        #self.process_task(application_transaction, user)

        # 支行审查			        支行审查岗
        #user = self.session.query(User).filter_by(user_name="00779").first()
        #self.process_task(application_transaction, user)

        # 支行审贷小组审议			支行审贷小组
        user = self.session.query(User).filter_by(user_name="00513").first()
        logging.debug(user.role_id)
        self.process_task(application_transaction, user)

        # 支行长审议				支行行长
        user = self.session.query(User).filter_by(user_name="00136").first()
        self.process_task(application_transaction, user)

        # 风险评价				风险评价岗
        user = self.session.query(User).filter_by(user_name="91014").first()
        self.process_task(application_transaction, user)

        # 审查岗审批				总行审查岗
        user = self.session.query(User).filter_by(user_name="00149").first()
        self.process_task(application_transaction, user)

        # 风险负责人审查   		        风险负责人
        user = self.session.query(User).filter_by(user_name="00477").first()
        self.process_task(application_transaction, user)

        # 信贷负责人审查   			信贷负责人
        user = self.session.query(User).filter_by(user_name="00335").first()
        self.process_task(application_transaction, user)

        #分管信贷副行长                         分管信贷副行长
        user = self.session.query(User).filter_by(user_name="00002").first()
        self.process_task(application_transaction, user)

        # 信贷负责人汇报董事长 信贷负责人
        user = self.session.query(User).filter_by(user_name="00335").first()
        self.process_task(application_transaction, user)

        # 总行审贷委   	   		        总行审贷委
        user = self.session.query(User).filter_by(user_name="00005").first()
        self.process_task(application_transaction, user)

        #总行行长                               总行行长
        user = self.session.query(User).filter_by(user_name="00002").first()
        self.process_task(application_transaction, user)

        # 放款申请				客户经理
        user = self.session.query(User).filter_by(user_name="00140").first()
        self.process_task(application_transaction, user)

        # 支行长初审				支行行长
        user = self.session.query(User).filter_by(user_name="00136").first()
        self.process_task(application_transaction, user)

         #信贷负责人终审   			信贷负责人
        user = self.session.query(User).filter_by(user_name="00335").first()
        self.process_task(application_transaction, user)

        # 放款   				客户经理
        user = self.session.query(User).filter_by(user_name="00140").first()
        self.process_task(application_transaction, user)

    def extension_flow(self):
        log.debug("start extension process workflow!")

        start_activity = self.session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"贷款展期申请流程").first()

        cust = self.session.query(Customer).join(Party, Party.id == Customer.party_id).filter(Party.name == u'刘永霞').first()
        application = Application(customer_id=cust.role_id,product_code='316',bill_type='敞口')
        application_transaction = ApplicationTransaction(transaction_name=u"%s的贷款申请"%(cust.party.name),amount = '20000000',application=application)
        start_activity.bind_transaction(application_transaction)

        # 贷款申请					客户经理
        user = self.session.query(User).filter_by(user_name="00140").first()
        self.process_task(application_transaction, user)

        # 预审						支行审查岗
        user = self.session.query(User).filter_by(user_name="00779").first()
        self.process_task(application_transaction, user)

        # 撰写调查报告			                客户经理
        user = self.session.query(User).filter_by(user_name="00140").first()
        self.process_task(application_transaction, user)

        # 支行风险评价				支行风险评价岗
        #user = self.session.query(User).filter_by(user_name="00140").first()
        #self.process_task(application_transaction, user)

        # 支行审查			        支行审查岗
        #user = self.session.query(User).filter_by(user_name="00779").first()
        #self.process_task(application_transaction, user)

        # 支行审贷小组审议			支行审贷小组
        user = self.session.query(User).filter_by(user_name="00513").first()
        logging.debug(user.role_id)
        self.process_task(application_transaction, user)

        # 支行长审议				支行行长
        user = self.session.query(User).filter_by(user_name="00136").first()
        self.process_task(application_transaction, user)

        # 风险评价				风险评价岗
        user = self.session.query(User).filter_by(user_name="91014").first()
        self.process_task(application_transaction, user)

        # 审查岗审批				总行审查岗
        user = self.session.query(User).filter_by(user_name="00149").first()
        self.process_task(application_transaction, user)

        # 风险负责人审查   		        风险负责人
        user = self.session.query(User).filter_by(user_name="00477").first()
        self.process_task(application_transaction, user)

        # 信贷负责人审查   			信贷负责人
        user = self.session.query(User).filter_by(user_name="00335").first()
        self.process_task(application_transaction, user)

        #分管信贷副行长                         分管信贷副行长
        user = self.session.query(User).filter_by(user_name="00002").first()
        self.process_task(application_transaction, user)

        # 信贷负责人汇报董事长 信贷负责人
        user = self.session.query(User).filter_by(user_name="00335").first()
        self.process_task(application_transaction, user)

        # 总行审贷委   	   		        总行审贷委
        user = self.session.query(User).filter_by(user_name="00005").first()
        self.process_task(application_transaction, user)

        #总行行长                               总行行长
        user = self.session.query(User).filter_by(user_name="00002").first()
        self.process_task(application_transaction, user)

        # 放款申请				客户经理
        user = self.session.query(User).filter_by(user_name="00140").first()
        self.process_task(application_transaction, user)

        # 支行长初审				支行行长
        user = self.session.query(User).filter_by(user_name="00136").first()
        self.process_task(application_transaction, user)

         #信贷负责人终审   			信贷负责人
        user = self.session.query(User).filter_by(user_name="00335").first()
        self.process_task(application_transaction, user)

        # 放款   				客户经理
        user = self.session.query(User).filter_by(user_name="00140").first()
        self.process_task(application_transaction, user)

    def bank_flow(self):
        log.debug("start bank process workflow!")
        start_activity = self.session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"同业业务流程").first()
        #user = self.session.query(User).filter_by(user_name="00540").first()
        cust = self.session.query(Customer).join(Party, Party.id == Customer.party_id).filter(Party.name == u'李顺义').first()
        application = Application(customer_id=cust.role_id,product_code='805')
        application_transaction = ApplicationTransaction(transaction_name=u"%s的贷款申请"%(cust.party.name),amount = '99999',application=application)
        start_activity.bind_transaction(application_transaction)

        # 同业业务申请 客户经理
        user = self.session.query(User).filter_by(user_name="01000").first()
        self.process_task(application_transaction, user)

        # 资金部风险岗审查
        user = self.session.query(User).filter_by(user_name="01001").first()
        self.process_task(application_transaction, user)

        # 资金负责人审查 资金部负责人
        user = self.session.query(User).filter_by(user_name="01002").first()
        self.process_task_comment(application_transaction, user, u'同意')
        #self.process_task_comment(application_transaction, user, u"不同意")

        #同业分管行长
        user = self.session.query(User).filter_by(user_name="00009").first()
        self.process_task_comment(application_transaction, user, u'同意')
        #self.process_task_comment(application_transaction, user, u"不同意")

        #同业资料整理
        user = self.session.query(User).filter_by(user_name="01000").first()
        self.process_task(application_transaction, user)

    def transfer_discount_flow(self):
        log.debug("start transfer_discount process workflow!")
        start_activity = self.session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"同业业务流程").first()

        cust = self.session.query(Customer).join(Party, Party.id == Customer.party_id).filter(Party.name == u'李顺义').first()
        application = Application(customer_id=cust.role_id,product_code='808')
        application_transaction = ApplicationTransaction(transaction_name=u"%s的贷款申请"%(cust.party.name),amount = '999999999',application=application)
        start_activity.bind_transaction(application_transaction)

        # 同业业务申请 客户经理
        user = self.session.query(User).filter_by(user_name="01000").first()
        self.process_task(application_transaction, user)

        # 资金部风险岗审查
        user = self.session.query(User).filter_by(user_name="01001").first()
        self.process_task(application_transaction, user)

        #营业部转贴现
        user = self.session.query(User).filter_by(user_name="01008").first()
        self.process_task(application_transaction, user)

        #营业部转贴现
        user = self.session.query(User).filter_by(user_name="01009").first()
        self.process_task(application_transaction, user)

        # 资金负责人审查 资金部负责人
        user = self.session.query(User).filter_by(user_name="01002").first()
        self.process_task(application_transaction, user)

        #同业分管行长
        user = self.session.query(User).filter_by(user_name="00009").first()
        self.process_task(application_transaction, user)

        #同业资料整理
        user = self.session.query(User).filter_by(user_name="01000").first()
        self.process_task(application_transaction, user)

    def discount_flow(self):
        log.debug("start discount process workflow!")
        start_activity = self.session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"贴现业务流程").first()

        cust = self.session.query(Customer).join(Party, Party.id == Customer.party_id).filter(Party.name == u'乌海市明星焦化有限责任公司').first()
        application = Application(customer_id=cust.role_id,product_code='023',quote_report=u'是')
        application_transaction = ApplicationTransaction(transaction_name=u"%s的贴现申请"%(cust.party.name),amount = '19999',application=application)
        start_activity.bind_transaction(application_transaction)

        # 申请 客户经理
        user = self.session.query(User).filter_by(user_name="00541").first()
        self.process_task(application_transaction, user)

        '''
        # 预审						支行审查岗
        user = self.session.query(User).filter_by(user_name="00779").first()
        self.process_task(application_transaction, user)

        # 撰写调查报告			                客户经理
        user = self.session.query(User).filter_by(user_name="00530").first()
        self.process_task(application_transaction, user)


        # 支行风险评价				支行风险评价岗
        user = self.session.query(User).filter_by(user_name="00140").first()
        self.process_task(application_transaction, user)

        # 支行审查			        支行审查岗
        user = self.session.query(User).filter_by(user_name="00779").first()
        self.process_task(application_transaction, user)

        # 支行审贷小组审议			支行审贷小组
        user = self.session.query(User).filter_by(user_name="00779").first()
        logging.debug(user.role_id)
        self.process_task(application_transaction, user)

        user = self.session.query(User).filter_by(user_name="00513").first()
        logging.debug(user.role_id)
        self.process_task(application_transaction, user)

        user = self.session.query(User).filter_by(user_name="00530").first()
        logging.debug(user.role_id)
        self.process_task(application_transaction, user)

        # 支行长审议				支行行长
        user = self.session.query(User).filter_by(user_name="00136").first()
        self.process_task(application_transaction, user)
        '''

        #票据信息录入
        user = self.session.query(User).filter_by(user_name="00541").first()
        self.process_task(application_transaction, user)

        #贴现验票
        user = self.session.query(User).filter_by(user_name="00140").first()
        self.process_task(application_transaction, user)

        #支行长审批
        user = self.session.query(User).filter_by(user_name="00136").first()
        self.process_task(application_transaction, user)

        #放款
        user = self.session.query(User).filter_by(user_name="00541").first()
        self.process_task(application_transaction, user)

    def invest_flow(self):
        log.debug("start invest process workflow!")
        start_activity = self.session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"投资流程").first()

        #user = self.session.query(User).filter_by(user_name="00540").first()

        cust = self.session.query(Customer).join(Party, Party.id == Customer.party_id).filter(Party.name == u'乌海市三金煤制品有限责任公司').first()
        application = Application(customer_id=cust.role_id,product_code='705')
        application_transaction = ApplicationTransaction(transaction_name=u"%s的投资申请"%(cust.party.name),amount = '19999',application=application)
        start_activity.bind_transaction(application_transaction)

        # 申请
        user = self.session.query(User).filter_by(user_name="01000").first()
        self.process_task(application_transaction, user)

        # 投资风险
        user = self.session.query(User).filter_by(user_name="01001").first()
        self.process_task(application_transaction, user)

        # 投资审议小组
        user = self.session.query(User).filter_by(user_name="01001").first()
        self.process_task(application_transaction, user)

        # 财务部负责人
        user = self.session.query(User).filter_by(user_name="01003").first()
        self.process_task(application_transaction, user)

        #风险负责人审查
        user = self.session.query(User).filter_by(user_name="00477").first()
        self.process_task(application_transaction, user)

        #资金负责人
        user = self.session.query(User).filter_by(user_name="01002").first()
        self.process_task(application_transaction, user)

        #资金分管行长
        user = self.session.query(User).filter_by(user_name="00009").first()
        self.process_task(application_transaction, user)

        #投资审议委员会
        user = self.session.query(User).filter_by(user_name="01004").first()
        self.process_task(application_transaction, user)

        #投资信息录入
        user = self.session.query(User).filter_by(user_name="01000").first()
        self.process_task(application_transaction, user)

        #投资信息复核
        user = self.session.query(User).filter_by(user_name="01010").first()
        self.process_task(application_transaction, user)

        #资金负责人审批
        user = self.session.query(User).filter_by(user_name="01002").first()
        self.process_task(application_transaction, user)

        #分管行长审批
        user = self.session.query(User).filter_by(user_name="00009").first()
        self.process_task(application_transaction, user)

        #总行长审批
        user = self.session.query(User).filter_by(user_name="00002").first()
        self.process_task(application_transaction, user)

        #投资资料整理
        user = self.session.query(User).filter_by(user_name="01000").first()
        self.process_task(application_transaction, user)

    def credit_granting_flow(self):
        log.debug("start credit granting process workflow!")
        start_activity = self.session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"统一授信业务流程").first()

        cust = self.session.query(Customer).join(Party, Party.id == Customer.party_id).filter(Party.name == u'乌海市三金煤制品有限责任公司').first()
        application = Application(customer_id=cust.role_id)
        application_transaction = ApplicationTransaction(transaction_name=u"%s的授信业务申请"%(cust.party.name),amount = '19999',application=application)
        start_activity.bind_transaction(application_transaction)

        # 客户经理申请
        user = self.session.query(User).filter_by(user_name="00510").first()
        self.process_task(application_transaction, user)

        # 支行审贷委
        user = self.session.query(User).filter_by(user_name="00513").first()
        self.process_task(application_transaction, user)

        # 支行长
        user = self.session.query(User).filter_by(user_name="00136").first()
        self.process_task(application_transaction, user)

        # 总行授信审查
        user = self.session.query(User).filter_by(user_name="00149").first()
        self.process_task(application_transaction, user)

        # 总行审贷委
        user = self.session.query(User).filter_by(user_name="00005").first()
        self.process_task(application_transaction, user)

        # 总行长
        user = self.session.query(User).filter_by(user_name="00002").first()
        self.process_task(application_transaction, user)

    def credit_class_flow(self):
        log.debug("start credit class process workflow!")
        start_activity = self.session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"五级分类业务流程").first()

        cust = self.session.query(Customer).join(Party, Party.id == Customer.party_id).filter(Party.name == u'乌海市三金煤制品有限责任公司').first()
        application = Application(customer_id=cust.role_id)
        application_transaction = ApplicationTransaction(transaction_name=u"%s的五级分类业务申请"%(cust.party.name),amount = '19999',application=application)
        start_activity.bind_transaction(application_transaction)

        # 客户经理申请
        user = self.session.query(User).filter_by(user_name="00510").first()
        self.process_task(application_transaction, user)

        # 支行审贷委
        user = self.session.query(User).filter_by(user_name="00513").first()
        self.process_task(application_transaction, user)

        # 支行长
        user = self.session.query(User).filter_by(user_name="00136").first()
        self.process_task(application_transaction, user)

        # 总行信贷部审查
        user = self.session.query(User).filter_by(user_name="00149").first()
        self.process_task(application_transaction, user)

        # 分管行长审查
        user = self.session.query(User).filter_by(user_name="00002").first()
        self.process_task(application_transaction, user)

        # 总行审贷委
        user = self.session.query(User).filter_by(user_name="00005").first()
        self.process_task(application_transaction, user)

        # 总行长
        user = self.session.query(User).filter_by(user_name="00002").first()
        self.process_task(application_transaction, user)

    def repossession_flow(self):
        log.debug("start repossession process workflow!")
        start_activity = self.session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"抵贷资产流程").first()

        cust = self.session.query(Customer).join(Party, Party.id == Customer.party_id).filter(Party.name == u'乌海市三金煤制品有限责任公司').first()
        application = Application(customer_id=cust.role_id)
        application_transaction = ApplicationTransaction(transaction_name=u"%s的抵贷资产申请"%(cust.party.name),amount = '19999',application=application)
        start_activity.bind_transaction(application_transaction)

        # 客户经理申请
        user = self.session.query(User).filter_by(user_name="00510").first()
        self.process_task(application_transaction, user)

        # 支行审贷委
        user = self.session.query(User).filter_by(user_name="00513").first()
        self.process_task(application_transaction, user)

        # 支行长
        user = self.session.query(User).filter_by(user_name="00136").first()
        self.process_task(application_transaction, user)

        # 总行风险评价
        user = self.session.query(User).filter_by(user_name="91014").first()
        self.process_task(application_transaction, user)

        # 总行信贷部审查
        user = self.session.query(User).filter_by(user_name="00149").first()
        self.process_task(application_transaction, user)

        # 财务部审查
        user = self.session.query(User).filter_by(user_name="01003").first()
        self.process_task(application_transaction, user)

        # 风险部审查
        user = self.session.query(User).filter_by(user_name="00477").first()
        self.process_task(application_transaction, user)

        # 分管行长审查
        user = self.session.query(User).filter_by(user_name="00002").first()
        self.process_task(application_transaction, user)

        # 总行审贷委
        user = self.session.query(User).filter_by(user_name="00005").first()
        self.process_task(application_transaction, user)

        # 总行长
        user = self.session.query(User).filter_by(user_name="00002").first()
        self.process_task(application_transaction, user)
    def process_task(self,transaction,user):
        groups = []
        for group in user.user_groups:
            groups.append(group.group.group_name)

        task_list = task.get_task(transaction)
        for t in task_list:
            role = get_parameter(t.activity,u"角色")
            if role and role in groups:

                logging.debug('#################################### %s %s ' % (user.user_name,role))
                t.user = user
                t.active()
                self.session.add(ApplicationComment(comment_type="同意",application=t.transaction.application,transaction_activity_id=t.transaction_activity_id,user=user))
                t.finish()
                self.session.query(Application).filter(Application.id == transaction.application_id).update({Application.status:t.activity.activity_name})
            self.session.commit()
        #task_list = task.get_task(user)

    def process_task_comment(self,transaction,user,comment):
        groups = []
        for group in user.user_groups:
            groups.append(group.group.group_name)

        task_list = task.get_task(transaction)
        for t in task_list:
            role = get_parameter(t.activity,u"角色")
            if role and role in groups:

                logging.debug('#################################### %s %s ' % (user.user_name,role))
                t.user = user
                logging.debug('#################################### %s %s active ok' % (user.user_name,role))
                t.active()
                self.session.add(ApplicationComment(comment_type=comment,application=t.transaction.application,transaction_activity_id=t.transaction_activity_id,user=user))
                t.finish()
                self.session.query(Application).filter(Application.id == transaction.application_id).update({Application.status:t.activity.activity_name})
            self.session.commit()


    def init_flow(self):
        """
        Workflow
        """
        log.debug("start init flow!")

        # Lendingproposition
        lendingproposition_task = TaskActivity(activity_name=u"贷款申请",activity_status=u'审议',activity_page=u'index', task_assign_module='fabs.workflow.default', task_assign_function='lendingproposition_task', waiting=True)
        self.session.add(lendingproposition_task)
        set_parameter(lendingproposition_task, u"角色", u"客户经理")

        chcproposition_task = TaskActivity(activity_name=u"转贷大表申请",activity_status=u'审议', activity_page=u'index',task_assign_module='fabs.workflow.default', task_assign_function='chcproposition_task', waiting=True)
        self.session.add(chcproposition_task)
        set_parameter(chcproposition_task, u"角色", u"客户经理")

        investigate_task = TaskActivity(activity_name=u"预审",activity_status=u'审议', activity_page=u'preAprove', task_assign_module='fabs.workflow.default', task_assign_function='investigate_task', waiting=True)
        self.session.add(investigate_task)
        set_parameter(investigate_task, u"角色", u"支行审查岗")

        write_report_task = TaskActivity(activity_name=u"撰写调查报告",activity_status=u'审议',activity_page=u'writeReport', task_assign_module='fabs.workflow.default', task_assign_function='write_report_task', waiting=True)
        self.session.add(write_report_task)
        set_parameter(write_report_task, u"角色", u"客户经理")

        # 并行
        subbranch_assessment_task = TaskActivity(activity_name=u"支行风险评价",activity_status=u'审议',activity_page=u'riskApprove', task_assign_module='fabs.workflow.default', task_assign_function='subbranch_assessment_task', waiting=True)
        self.session.add(subbranch_assessment_task)
        set_parameter(subbranch_assessment_task, u"角色", u"支行风险评价岗")

        subbranch_review_task= TaskActivity(activity_name=u"支行审查",activity_status=u'审议',activity_page=u'examineApprove', task_assign_module='fabs.workflow.default', task_assign_function='subbranch_review_task', waiting=True)
        self.session.add(subbranch_review_task)
        set_parameter(subbranch_review_task, u"角色", u"支行审查岗")


        subbranch_deliberation_task = TaskActivity(activity_name=u"支行审贷小组审议",activity_status=u'审议',activity_page=u'groupApprove', task_assign_module='fabs.workflow.default', task_assign_function='subbranch_deliberation_task', waiting=True)
        self.session.add(subbranch_deliberation_task)
        set_parameter(subbranch_deliberation_task, u"角色", u"支行审贷小组")


        subbranch_president_task = TaskActivity(activity_name=u"支行长审议", activity_status=u'审议',activity_page=u'groupApprove',task_assign_module='fabs.workflow.default', task_assign_function='subbranch_president_task', waiting=True)
        self.session.add(subbranch_president_task)
        set_parameter(subbranch_president_task, u"角色", u"支行行长")

        loan_application_task = TaskActivity(activity_name=u"放款申请",activity_status=u'审批',activity_page=u'loanApplication', task_assign_module='fabs.workflow.default', task_assign_function='loan_application_task', waiting=True)
        self.session.add(loan_application_task)
        set_parameter(loan_application_task, u"角色", u"客户经理")

        subbranch_approve_task = TaskActivity(activity_name=u"支行长审批",activity_status=u'审批',activity_page=u'loanApplication', task_assign_module='fabs.workflow.default', task_assign_function='subbranch_approve_task', waiting=True)
        self.session.add(subbranch_approve_task)
        set_parameter(subbranch_approve_task, u"角色", u"支行行长")

        credit_loan_task = TaskActivity(activity_name=u"放款", activity_status=u'审批结束',activity_page=u'loan',task_assign_module='fabs.workflow.default', task_assign_function='credit_loan_task', waiting=True)
        self.session.add(credit_loan_task)
        set_parameter(credit_loan_task, u"角色", u"客户经理")

        """
        超权限
        """
        # 并行
        ho_review_task = TaskActivity(activity_name=u"总行信贷审查", activity_status=u'审议',activity_page=u'groupApprove',task_assign_module='fabs.workflow.default', task_assign_function='ho_review_task', waiting=True)
        self.session.add(ho_review_task)
        set_parameter(ho_review_task, u"角色", u"总行审查岗")

        ho_assessment_task = TaskActivity(activity_name=u"总行风险评价",activity_status=u'审议',activity_page=u'groupApprove' ,task_assign_module='fabs.workflow.default', task_assign_function='ho_assessment_task', waiting=True)
        self.session.add(ho_assessment_task)
        set_parameter(ho_assessment_task, u"角色", u"总行风险评价岗")

        ho_riskowners_task= TaskActivity(activity_name=u"风险负责人审查",activity_status=u'审议',activity_page=u'groupApprove' ,task_assign_module='fabs.workflow.default', task_assign_function='ho_riskowners_task', waiting=True)
        self.session.add(ho_riskowners_task)
        set_parameter(ho_riskowners_task, u"角色", u"总行风险负责人")


        riskowners_review_task = TaskActivity(activity_name=u"信贷负责人审查",activity_status=u'审议',activity_page=u'groupApprove' ,task_assign_module='fabs.workflow.default', task_assign_function='riskowners_review_task', waiting=True)
        self.session.add(riskowners_review_task)
        set_parameter(riskowners_review_task, u"角色", u"总行审查负责人")

        riskowners_chairman_review_task = TaskActivity(activity_name=u"信贷负责人汇报董事长",activity_page=u'groupApprove',activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='riskowners_chairman_review_task', waiting=True)
        self.session.add(riskowners_chairman_review_task)
        set_parameter(riskowners_chairman_review_task, u"角色", u"总行审查负责人")

        bm_review_task = TaskActivity(activity_name=u"信贷分管行长审查",activity_status=u'审议',activity_page=u'groupApprove' ,task_assign_module='fabs.workflow.default', task_assign_function='bm_review_task', waiting=True)
        self.session.add(bm_review_task)
        set_parameter(bm_review_task, u"角色", u"分管信贷副行长")

        committee_deliberation_task = TaskActivity(activity_name=u"总行信贷委员会审议",activity_status=u'审议', activity_page=u'groupApprove',task_assign_module='fabs.workflow.default', task_assign_function='committee_deliberation_task', waiting=True)
        self.session.add(committee_deliberation_task)
        set_parameter(committee_deliberation_task, u"角色", u"总行审贷委")

        ho_president_task = TaskActivity(activity_name=u"总行行长审批",activity_status=u'审批',activity_page=u'loanApplication' ,task_assign_module='fabs.workflow.default', task_assign_function='ho_president_task', waiting=True)
        self.session.add(ho_president_task)
        set_parameter(ho_president_task, u"角色", u"总行行长")

        subbranch_first_approve_task=TaskActivity(activity_name=u"支行行长预审批",activity_status=u'审批',activity_page=u'loanApplication', task_assign_module='fabs.workflow.default', task_assign_function='subbranch_first_approve_task', waiting=True)
        self.session.add(subbranch_first_approve_task)
        set_parameter(subbranch_first_approve_task, u"角色", u"支行行长")

        ho_review_approve_task=TaskActivity(activity_name=u"信贷负责人审批",activity_status=u'审批',activity_page=u'loanApplication', task_assign_module='fabs.workflow.default', task_assign_function='ho_review_approve_task', waiting=True)
        self.session.add(ho_review_approve_task)
        set_parameter(ho_review_approve_task, u"角色", u"总行审查负责人")

        ho_approve_task = TaskActivity(activity_name=u"总行行长终审",activity_status=u'审批', activity_page=u'loanApplication',task_assign_module='fabs.workflow.default', task_assign_function='ho_approve_task', waiting=True)
        self.session.add(ho_approve_task)
        set_parameter(ho_approve_task, u"角色", u"总行行长")

        bank_ho_approve_task = TaskActivity(activity_name=u"总行行长同业业务终审",activity_status=u'审批', task_assign_module='fabs.workflow.default', task_assign_function='bank_ho_approve_task', waiting=True)
        self.session.add(bank_ho_approve_task)
        set_parameter(bank_ho_approve_task, u"角色", u"总行行长")

        invest_ho_approve_task = TaskActivity(activity_name=u"总行行长资金业务终审",activity_status=u'审批', task_assign_module='fabs.workflow.default', task_assign_function='invest_ho_approve_task', waiting=True)
        self.session.add(invest_ho_approve_task)
        set_parameter(invest_ho_approve_task, u"角色", u"总行行长")


        accountant_check_task = TaskActivity(activity_name=u"会计验票", task_assign_module='fabs.workflow.default', task_assign_function='accountant_check_task', waiting=True)
        self.session.add(accountant_check_task)
        set_parameter(accountant_check_task, u"角色", u"会计部")

        entering_info_task = TaskActivity(activity_name=u"录入信息",activity_status=u'审批', task_assign_module='fabs.workflow.default', task_assign_function='entering_info_task', waiting=True)
        self.session.add(entering_info_task)
        set_parameter(entering_info_task, u"角色", u"客户经理")


        invest_application_task=TaskActivity(activity_name=u"投资申请",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='invest_application_task', waiting=True)
        self.session.add(invest_application_task)
        set_parameter(invest_application_task, u"角色", u"投资交易岗")


        invest_review_task=TaskActivity(activity_name=u"资金部投资业务风险审核",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='invest_review_task', waiting=True)
        self.session.add(invest_review_task)
        set_parameter(invest_review_task, u"角色", u"资金部风险岗")

        bank_review_task=TaskActivity(activity_name=u"资金部同业业务风险审核",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='bank_review_task', waiting=True)
        self.session.add(bank_review_task)
        set_parameter(bank_review_task, u"角色", u"资金部风险岗")

        capital_riskowners_task=TaskActivity(activity_name=u"资金部负责人资金业务审查",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='capital_riskowners_task', waiting=True)
        self.session.add(capital_riskowners_task)
        set_parameter(capital_riskowners_task, u"角色", u"资金部负责人")

        bank_capital_charge_task=TaskActivity(activity_name=u"资金部负责人同业业务审查",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='bank_capital_charge_task', waiting=True)
        self.session.add(bank_capital_charge_task)
        set_parameter(bank_capital_charge_task, u"角色", u"资金部负责人")

        invest_term_deliberation_task = TaskActivity(activity_name=u"投资审议小组审议",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='invest_term_deliberation_task', waiting=True)
        self.session.add(invest_term_deliberation_task)
        set_parameter(invest_term_deliberation_task, u"角色", u"投资审议小组")

        finance_riskowners_task=TaskActivity(activity_name=u"财务部负责人审查",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='finance_riskowners_task', waiting=True)
        self.session.add(finance_riskowners_task)
        set_parameter(finance_riskowners_task, u"角色", u"财务部负责人")

        invest_deliberation_task=TaskActivity(activity_name=u"投资委员会审议",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='invest_deliberation_task', waiting=True)
        self.session.add(invest_deliberation_task)
        set_parameter(invest_deliberation_task, u"角色", u"投资审议委员会")

        invest_entering_task=TaskActivity(activity_name=u"投资录入信息",activity_status=u'审批', task_assign_module='fabs.workflow.default', task_assign_function='invest_entering_task', waiting=True)
        self.session.add(invest_entering_task)
        set_parameter(invest_entering_task, u"角色", u"投资交易岗")

        invest_enering_review_task=TaskActivity(activity_name=u"投资录入信息复核",activity_status=u'审批', task_assign_module='fabs.workflow.default', task_assign_function='invest_enering_review_task', waiting=True)
        self.session.add(invest_enering_review_task)
        set_parameter(invest_enering_review_task, u"角色", u"投资交易复核岗")

        finance_riskowners_approve_task=TaskActivity(activity_name=u"资金部负责人审批",activity_status=u'审批', task_assign_module='fabs.workflow.default', task_assign_function='finance_riskowners_approve_task', waiting=True)
        self.session.add(finance_riskowners_approve_task)
        set_parameter(finance_riskowners_approve_task, u"角色", u"资金部负责人")

        invest_bm_review_task = TaskActivity(activity_name=u"资金分管行长审查",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='invest_bm_review_task', waiting=True)
        self.session.add(invest_bm_review_task)
        set_parameter(invest_bm_review_task, u"角色", u"分管资金副行长")

        bank_invest_bm_review_task = TaskActivity(activity_name=u"资金分管行长投资业务审批",activity_status=u'审批', task_assign_module='fabs.workflow.default', task_assign_function='invest_bm_review_task', waiting=True)
        self.session.add(bank_invest_bm_review_task)
        set_parameter(bank_invest_bm_review_task, u"角色", u"分管资金副行长")

        invest_data_check=TaskActivity(activity_name=u"投资资料整理",activity_status=u'审批结束', task_assign_module='fabs.workflow.default', task_assign_function='invest_data_check', waiting=True)
        self.session.add(invest_data_check)
        set_parameter(invest_data_check, u"角色", u"投资交易岗")

        bank_application_task=TaskActivity(activity_name=u"同业业务申请",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='bank_application_task', waiting=True)
        self.session.add(bank_application_task)
        set_parameter(bank_application_task, u"角色", u"同业交易岗")

        bank_bm_review_task = TaskActivity(activity_name=u"同业分管行长审查",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='bank_bm_review_task', waiting=True)
        self.session.add(bank_bm_review_task)
        set_parameter(bank_bm_review_task, u"角色", u"分管同业副行长")

        branch_transfer_discount_task = TaskActivity(activity_name=u"营业部转贴现审查",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='branch_transfer_discount_task', waiting=True)
        self.session.add(branch_transfer_discount_task)
        set_parameter(branch_transfer_discount_task, u"角色", u"营业部转贴现岗")

        branch_transfer_discount_review_task = TaskActivity(activity_name=u"营业部转贴现负责人审查",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='branch_transfer_discount_review_task', waiting=True)
        self.session.add(branch_transfer_discount_review_task)
        set_parameter(branch_transfer_discount_review_task, u"角色", u"营业部转贴现负责人")

        bank_trade_data_check=TaskActivity(activity_name=u"同业业务资料整理", activity_status=u'审批结束',task_assign_module='fabs.workflow.default', task_assign_function='bank_trade_data_check', waiting=True)
        self.session.add(bank_trade_data_check)
        set_parameter(bank_trade_data_check, u"角色", u"同业交易岗")

        lending_discount_task = TaskActivity(activity_name=u"贴现申请",activity_status=u'审议', activity_page=u'discountAppInfo', task_assign_module='fabs.workflow.default', task_assign_function='lending_discount_task', waiting=True)
        self.session.add(lending_discount_task)
        set_parameter(lending_discount_task, u"角色", u"客户经理")

        discount_investigate_task = TaskActivity(activity_name=u"贴现预审",activity_status=u'审议', activity_page=u'discountPreAprove', task_assign_module='fabs.workflow.default', task_assign_function='discount_investigate_task', waiting=True)
        self.session.add(discount_investigate_task)
        set_parameter(discount_investigate_task, u"角色", u"支行审查岗")

        discount_write_report_task = TaskActivity(activity_name=u"贴现撰写调查报告",activity_status=u'审议',activity_page=u'discountWriteReport', task_assign_module='fabs.workflow.default', task_assign_function='discount_write_report_task', waiting=True)
        self.session.add(discount_write_report_task)
        set_parameter(discount_write_report_task, u"角色", u"客户经理")

        # 并行
        discount_subbranch_assessment_task = TaskActivity(activity_name=u"贴现支行风险评价",activity_status=u'审议',activity_page=u'discountRiskApprove', task_assign_module='fabs.workflow.default', task_assign_function='discount_subbranch_assessment_task', waiting=True)
        self.session.add(discount_subbranch_assessment_task)
        set_parameter(discount_subbranch_assessment_task, u"角色", u"支行风险评价岗")

        discount_subbranch_review_task= TaskActivity(activity_name=u"贴现支行审查",activity_status=u'审议',activity_page=u'discountExamineApprove', task_assign_module='fabs.workflow.default', task_assign_function='discount_subbranch_review_task', waiting=True)
        self.session.add(discount_subbranch_review_task)
        set_parameter(discount_subbranch_review_task, u"角色", u"支行审查岗")


        discount_subbranch_deliberation_task = TaskActivity(activity_name=u"贴现支行审贷小组审议",activity_status=u'审议',activity_page=u'discountGroupApprove', task_assign_module='fabs.workflow.default', task_assign_function='discount_subbranch_deliberation_task', waiting=True)
        self.session.add(discount_subbranch_deliberation_task)
        set_parameter(discount_subbranch_deliberation_task, u"角色", u"支行审贷小组")

        discount_subbranch_president_task = TaskActivity(activity_name=u"贴现支行长审议", activity_status=u'审议',activity_page=u'discountGroupApprove',task_assign_module='fabs.workflow.default', task_assign_function='discount_subbranch_president_task', waiting=True)
        self.session.add(discount_subbranch_president_task)
        set_parameter(discount_subbranch_president_task, u"角色", u"支行行长")

        discount_info_input= TaskActivity(activity_name=u"贴现信息录入",activity_status=u'审批', activity_page=u'discountBill', task_assign_module='fabs.workflow.default', task_assign_function='discount_info_input', waiting=True)
        self.session.add(discount_info_input)
        set_parameter(discount_info_input, u"角色", u"客户经理")

        discount_approve_task = TaskActivity(activity_name=u"贴现支行长审批",activity_status=u'审批',activity_page=u'discountBill', task_assign_module='fabs.workflow.default', task_assign_function='discount_approve_task', waiting=True)
        self.session.add(discount_approve_task)
        set_parameter(discount_approve_task, u"角色", u"支行行长")

        discount_loan_task = TaskActivity(activity_name=u"贴现放款", activity_status=u'审批结束',activity_page=u'discountLoanTask',task_assign_module='fabs.workflow.default', task_assign_function='discount_loan_task', waiting=True)
        self.session.add(discount_loan_task)
        set_parameter(discount_loan_task, u"角色", u"客户经理")

        check_ticket_task = TaskActivity(activity_name=u"贴现验票",activity_status=u'审批', activity_page=u'discountLoanTask', task_assign_module='fabs.workflow.default', task_assign_function='check_ticket_task', waiting=True)
        self.session.add(check_ticket_task)
        set_parameter(check_ticket_task, u"角色", u"客户经理")

        credit_granting_apply_task = TaskActivity(activity_name=u"统一授信申请",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='credit_granting_apply_task', waiting=True)
        self.session.add(credit_granting_apply_task)
        set_parameter(credit_granting_apply_task, u"角色", u"客户经理")

        credit_granting_subbranch_deliberation_task = TaskActivity(activity_name=u"支行审贷小组授信审议",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='credit_granting_subbranch_deliberation_task', waiting=True)
        self.session.add(credit_granting_subbranch_deliberation_task)
        set_parameter(credit_granting_subbranch_deliberation_task, u"角色", u"支行审贷小组")

        credit_granting_subbranch_president_task = TaskActivity(activity_name=u"支行长授信审议",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='credit_granting_subbranch_president_task', waiting=True)
        self.session.add(credit_granting_subbranch_president_task)
        set_parameter(credit_granting_subbranch_president_task, u"角色", u"支行行长")

        ho_credit_granting_review_task = TaskActivity(activity_name=u"总行授信审查",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='ho_credit_granting_review_task', waiting=True)
        self.session.add(ho_credit_granting_review_task)
        set_parameter(ho_credit_granting_review_task, u"角色", u"总行审查岗")

        credit_granting_committee_deliberation_task = TaskActivity(activity_name=u"总行信贷委员会授信审议",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='credit_granting_committee_deliberation_task', waiting=True)
        self.session.add(credit_granting_committee_deliberation_task)
        set_parameter(credit_granting_committee_deliberation_task, u"角色", u"总行审贷委")

        ho_credit_granting_president_task = TaskActivity(activity_name=u"总行行长授信审批",activity_status=u'审批', task_assign_module='fabs.workflow.default', task_assign_function='ho_credit_granting_president_task', waiting=True)
        self.session.add(ho_credit_granting_president_task)
        set_parameter(ho_credit_granting_president_task, u"角色", u"总行行长")

        credit_granting_end_task = TaskActivity(activity_name=u"统一授信查看", activity_status=u'审批',task_assign_module='fabs.workflow.default', task_assign_function='credit_granting_end_task', waiting=True)
        self.session.add(credit_granting_end_task)
        set_parameter(credit_granting_end_task, u"角色", u"客户经理")

        credit_class_apply_task = TaskActivity(activity_name=u"五级分类申请",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='credit_class_apply_task', waiting=True)
        self.session.add(credit_class_apply_task)
        set_parameter(credit_class_apply_task, u"角色", u"客户经理")

        credit_class_subbranch_deliberation_task = TaskActivity(activity_name=u"支行审贷小组五级分类审议",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='credit_class_subbranch_deliberation_task', waiting=True)
        self.session.add(credit_class_subbranch_deliberation_task)
        set_parameter(credit_class_subbranch_deliberation_task, u"角色", u"支行审贷小组")

        credit_class_subbranch_president_task = TaskActivity(activity_name=u"支行长五级分类审议", activity_status=u'审议',task_assign_module='fabs.workflow.default', task_assign_function='credit_class_subbranch_president_task', waiting=True)
        self.session.add(credit_class_subbranch_president_task)
        set_parameter(credit_class_subbranch_president_task, u"角色", u"支行行长")

        ho_credit_class_review_task = TaskActivity(activity_name=u"总行五级分类审查",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='ho_credit_class_review_task', waiting=True)
        self.session.add(ho_credit_class_review_task)
        set_parameter(ho_credit_class_review_task, u"角色", u"总行审查岗")

        ho_credit_class_bm_review_task = TaskActivity(activity_name=u"信贷分管行长五级分类审批",activity_status=u'审批', task_assign_module='fabs.workflow.default', task_assign_function='ho_credit_class_bm_review_task', waiting=True)
        self.session.add(ho_credit_class_bm_review_task)
        set_parameter(ho_credit_class_bm_review_task, u"角色", u"分管信贷副行长")

        ho_credit_class_committee_deliberation_task = TaskActivity(activity_name=u"总行信贷委员会五级分类审议",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='ho_credit_class_committee_deliberation_task', waiting=True)
        self.session.add(ho_credit_class_committee_deliberation_task)
        set_parameter(ho_credit_class_committee_deliberation_task, u"角色", u"总行审贷委")

        ho_credit_class_president_task = TaskActivity(activity_name=u"总行行长五级分类审批",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='ho_credit_class_president_task', waiting=True)
        self.session.add(ho_credit_class_president_task)
        set_parameter(ho_credit_class_president_task, u"角色", u"总行行长")

        repossession_apply_task = TaskActivity(activity_name=u"抵贷资产申请",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='repossession_apply_task', waiting=True)
        self.session.add(repossession_apply_task)
        set_parameter(repossession_apply_task, u"角色", u"客户经理")

        repossession_subbranch_deliberation_task = TaskActivity(activity_name=u"支行审贷小组抵贷资产审议",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='repossession_subbranch_deliberation_task', waiting=True)
        self.session.add(repossession_subbranch_deliberation_task)
        set_parameter(repossession_subbranch_deliberation_task, u"角色", u"支行审贷小组")

        repossession_subbranch_president_task = TaskActivity(activity_name=u"支行长抵贷资产审议", activity_status=u'审议',task_assign_module='fabs.workflow.default', task_assign_function='repossession_subbranch_president_task', waiting=True)
        self.session.add(repossession_subbranch_president_task)
        set_parameter(repossession_subbranch_president_task, u"角色", u"支行行长")

        repossession_finance_charge_task=TaskActivity(activity_name=u"财务部负责人抵贷资产审查",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='repossession_finance_charge_task', waiting=True)
        self.session.add(repossession_finance_charge_task)
        set_parameter(repossession_finance_charge_task, u"角色", u"财务部负责人")

        repossession_ho_assessment_task = TaskActivity(activity_name=u"总行风险抵贷资产评价",activity_status=u'审议',activity_page=u'groupApprove' ,task_assign_module='fabs.workflow.default', task_assign_function='repossession_ho_assessment_task', waiting=True)
        self.session.add(repossession_ho_assessment_task)
        set_parameter(repossession_ho_assessment_task, u"角色", u"总行风险评价岗")

        repossession_ho_riskowners_task= TaskActivity(activity_name=u"风险负责人抵贷资产审查",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='repossession_ho_riskowners_task', waiting=True)
        self.session.add(repossession_ho_riskowners_task)
        set_parameter(repossession_ho_riskowners_task, u"角色", u"总行风险负责人")

        repossession_ho_loan_charge_task = TaskActivity(activity_name=u"信贷负责人抵贷资产审查",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='repossession_ho_loan_charge_task', waiting=True)
        self.session.add(repossession_ho_loan_charge_task)
        set_parameter(repossession_ho_loan_charge_task, u"角色", u"总行审查负责人")

        repossession_ho_credit_bm_review_task = TaskActivity(activity_name=u"信贷分管行长抵贷资产审批",activity_status=u'审批', task_assign_module='fabs.workflow.default', task_assign_function='repossession_ho_credit_bm_review_task', waiting=True)
        self.session.add(repossession_ho_credit_bm_review_task)
        set_parameter(repossession_ho_credit_bm_review_task, u"角色", u"分管信贷副行长")

        repossession_ho_credit_committee_deliberation_task = TaskActivity(activity_name=u"总行信贷委员会抵贷资产审议",activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='repossession_ho_credit_committee_deliberation_task', waiting=True)
        self.session.add(repossession_ho_credit_committee_deliberation_task)
        set_parameter(repossession_ho_credit_committee_deliberation_task, u"角色", u"总行审贷委")

        repossession_ho_credit_class_president_task = TaskActivity(activity_name=u"总行行长抵贷资产审批",activity_status=u'审批', task_assign_module='fabs.workflow.default', task_assign_function='repossession_ho_credit_class_president_task', waiting=True)
        self.session.add(repossession_ho_credit_class_president_task)
        set_parameter(repossession_ho_credit_class_president_task, u"角色", u"总行行长")

        repossession_standingbook_task = TaskActivity(activity_name=u"抵贷资产台账登记",activity_status=u'审批', task_assign_module='fabs.workflow.default', task_assign_function='repossession_standingbook_task', waiting=True)
        self.session.add(repossession_standingbook_task)
        set_parameter(repossession_standingbook_task, u"角色", u"客户经理")

        #签发
        acceptance_lending_task = TaskActivity(activity_name=u"签发申请",activity_status=u'审议',activity_page=u'acceptanceAppInfo', task_assign_module='fabs.workflow.default', task_assign_function='acceptance_lending_task', waiting=True)
        self.session.add(acceptance_lending_task)
        set_parameter(acceptance_lending_task, u"角色", u"客户经理")

        acceptance_investigate_task= TaskActivity(activity_name=u"签发预审",activity_status=u'审议', activity_page=u'acceptancePreApprove', task_assign_module='fabs.workflow.default', task_assign_function='acceptance_investigate_task', waiting=True)
        self.session.add(acceptance_investigate_task)
        set_parameter(acceptance_investigate_task, u"角色", u"支行审查岗")

        acceptance_write_report_task = TaskActivity(activity_name=u"签发撰写调查报告",activity_status=u'审议',activity_page=u'acceptanceWriteReport', task_assign_module='fabs.workflow.default', task_assign_function='acceptance_write_report_task', waiting=True)
        self.session.add(acceptance_write_report_task)
        set_parameter(acceptance_write_report_task, u"角色", u"客户经理")

        acceptance_subbranch_assessment_task = TaskActivity(activity_name=u"签发支行风险评价",activity_status=u'审议',activity_page=u'acceptanceRiskApprove', task_assign_module='fabs.workflow.default', task_assign_function='acceptance_subbranch_assessment_task', waiting=True)
        self.session.add(acceptance_subbranch_assessment_task)
        set_parameter(acceptance_subbranch_assessment_task, u"角色", u"支行风险评价岗")

        acceptance_subbranch_review_task= TaskActivity(activity_name=u"签发支行审查",activity_status=u'审议',activity_page=u'acceptanceExamineApprove', task_assign_module='fabs.workflow.default', task_assign_function='acceptance_subbranch_review_task', waiting=True)
        self.session.add(acceptance_subbranch_review_task)
        set_parameter(acceptance_subbranch_review_task, u"角色", u"支行审查岗")

        acceptance_subbranch_deliberation_task = TaskActivity(activity_name=u"签发支行审贷小组审议",activity_status=u'审议',activity_page=u'acceptanceGroupApprove', task_assign_module='fabs.workflow.default', task_assign_function='acceptance_subbranch_deliberation_task', waiting=True)
        self.session.add(acceptance_subbranch_deliberation_task)
        set_parameter(acceptance_subbranch_deliberation_task, u"角色", u"支行审贷小组")


        acceptance_subbranch_president_task = TaskActivity(activity_name=u"签发支行长审议", activity_status=u'审议',activity_page=u'acceptanceGroupApprove',task_assign_module='fabs.workflow.default', task_assign_function='acceptance_subbranch_president_task', waiting=True)
        self.session.add(acceptance_subbranch_president_task)
        set_parameter(acceptance_subbranch_president_task, u"角色", u"支行行长")

        acceptance_loan_application_task = TaskActivity(activity_name=u"签发放款申请",activity_status=u'审批',activity_page=u'acceptanceLoanApplication', task_assign_module='fabs.workflow.default', task_assign_function='acceptance_loan_application_task', waiting=True)
        self.session.add(acceptance_loan_application_task)
        set_parameter(acceptance_loan_application_task, u"角色", u"客户经理")

        acceptance_subbranch_approve_task = TaskActivity(activity_name=u"签发支行长审批",activity_status=u'审批',activity_page=u'acceptanceLoanApplication', task_assign_module='fabs.workflow.default', task_assign_function='acceptance_subbranch_approve_task', waiting=True)
        self.session.add(acceptance_subbranch_approve_task)
        set_parameter(acceptance_subbranch_approve_task, u"角色", u"支行行长")

        acceptance_credit_loan_task = TaskActivity(activity_name=u"签发放款", activity_status=u'审批结束',activity_page=u'acceptanceLoan',task_assign_module='fabs.workflow.default', task_assign_function='acceptance_credit_loan_task', waiting=True)
        self.session.add(acceptance_credit_loan_task)
        set_parameter(acceptance_credit_loan_task, u"角色", u"客户经理")

        """
        超权限
        """
        # 并行
        acceptance_ho_review_task = TaskActivity(activity_name=u"签发总行信贷审查", activity_status=u'审议',activity_page=u'acceptanceGroupApprove',task_assign_module='fabs.workflow.default', task_assign_function='acceptance_ho_review_task', waiting=True)
        self.session.add(acceptance_ho_review_task)
        set_parameter(acceptance_ho_review_task, u"角色", u"总行审查岗")

        acceptance_ho_assessment_task = TaskActivity(activity_name=u"签发总行风险评价",activity_status=u'审议',activity_page=u'acceptanceGroupApprove' ,task_assign_module='fabs.workflow.default', task_assign_function='acceptance_ho_assessment_task', waiting=True)
        self.session.add(acceptance_ho_assessment_task)
        set_parameter(acceptance_ho_assessment_task, u"角色", u"总行风险评价岗")

        acceptance_ho_riskowners_task= TaskActivity(activity_name=u"签发风险负责人审查",activity_status=u'审议',activity_page=u'acceptanceGroupApprove' ,task_assign_module='fabs.workflow.default', task_assign_function='acceptance_ho_riskowners_task', waiting=True)
        self.session.add(acceptance_ho_riskowners_task)
        set_parameter(acceptance_ho_riskowners_task, u"角色", u"总行风险负责人")

        acceptance_riskowners_review_task = TaskActivity(activity_name=u"签发信贷负责人审查",activity_status=u'审议',activity_page=u'acceptanceGroupApprove' ,task_assign_module='fabs.workflow.default', task_assign_function='acceptance_riskowners_review_task', waiting=True)
        self.session.add(acceptance_riskowners_review_task)
        set_parameter(acceptance_riskowners_review_task, u"角色", u"总行审查负责人")

        acceptance_riskowners_chairman_review_task = TaskActivity(activity_name=u"签发信贷负责人汇报董事长",activity_page=u'acceptanceGroupApprove',activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='acceptance_riskowners_chairman_review_task', waiting=True)
        self.session.add(acceptance_riskowners_chairman_review_task)
        set_parameter(acceptance_riskowners_chairman_review_task, u"角色", u"总行审查负责人")

        acceptance_bm_review_task = TaskActivity(activity_name=u"签发信贷分管行长审查",activity_status=u'审议',activity_page=u'acceptanceGroupApprove' ,task_assign_module='fabs.workflow.default', task_assign_function='acceptance_bm_review_task', waiting=True)
        self.session.add(acceptance_bm_review_task)
        set_parameter(acceptance_bm_review_task, u"角色", u"分管信贷副行长")

        acceptance_committee_deliberation_task = TaskActivity(activity_name=u"签发总行信贷委员会审议",activity_status=u'审议', activity_page=u'acceptanceGroupApprove',task_assign_module='fabs.workflow.default', task_assign_function='acceptance_committee_deliberation_task', waiting=True)
        self.session.add(acceptance_committee_deliberation_task)
        set_parameter(acceptance_committee_deliberation_task, u"角色", u"总行审贷委")

        acceptance_ho_president_task = TaskActivity(activity_name=u"签发总行行长审批",activity_status=u'审批',activity_page=u'acceptanceGroupApprove' ,task_assign_module='fabs.workflow.default', task_assign_function='acceptance_ho_president_task', waiting=True)
        self.session.add(acceptance_ho_president_task)
        set_parameter(acceptance_ho_president_task, u"角色", u"总行行长")

        acceptance_subbranch_first_approve_task=TaskActivity(activity_name=u"签发支行行长预审批",activity_status=u'审批',activity_page=u'acceptanceLoanApplication', task_assign_module='fabs.workflow.default', task_assign_function='acceptance_subbranch_first_approve_task', waiting=True)
        self.session.add(acceptance_subbranch_first_approve_task)
        set_parameter(acceptance_subbranch_first_approve_task, u"角色", u"支行行长")

        acceptance_ho_review_approve_task=TaskActivity(activity_name=u"签发信贷负责人审批",activity_status=u'审批',activity_page=u'acceptanceLoanApplication', task_assign_module='fabs.workflow.default', task_assign_function='acceptance_ho_review_approve_task', waiting=True)
        self.session.add(acceptance_ho_review_approve_task)
        set_parameter(acceptance_ho_review_approve_task, u"角色", u"总行审查负责人")

        #展期业务
        extension_lendingproposition_task = TaskActivity(activity_name=u"贷款展期申请",activity_status=u'审议',activity_page=u'extensionPage', task_assign_module='fabs.workflow.default', task_assign_function='extension_lendingproposition_task', waiting=True)
        self.session.add(extension_lendingproposition_task)
        set_parameter(extension_lendingproposition_task, u"角色", u"客户经理")

        extension_investigate_task = TaskActivity(activity_name=u"展期预审",activity_status=u'审议', activity_page=u'extensionPage', task_assign_module='fabs.workflow.default', task_assign_function='extension_investigate_task', waiting=True)
        self.session.add(extension_investigate_task)
        set_parameter(extension_investigate_task, u"角色", u"支行审查岗")

        extension_write_report_task = TaskActivity(activity_name=u"展期撰写调查报告",activity_status=u'审议',activity_page=u'extensionPage', task_assign_module='fabs.workflow.default', task_assign_function='extension_write_report_task', waiting=True)
        self.session.add(extension_write_report_task)
        set_parameter(extension_write_report_task, u"角色", u"客户经理")

        extension_subbranch_deliberation_task = TaskActivity(activity_name=u"展期支行审贷小组审议",activity_status=u'审议',activity_page=u'extensionPage', task_assign_module='fabs.workflow.default', task_assign_function='extension_subbranch_deliberation_task', waiting=True)
        self.session.add(extension_subbranch_deliberation_task)
        set_parameter(extension_subbranch_deliberation_task, u"角色", u"支行审贷小组")

        extension_subbranch_president_task = TaskActivity(activity_name=u"展期支行长审议", activity_status=u'审议',activity_page=u'extensionPage',task_assign_module='fabs.workflow.default', task_assign_function='extension_subbranch_president_task', waiting=True)
        self.session.add(extension_subbranch_president_task)
        set_parameter(extension_subbranch_president_task, u"角色", u"支行行长")

        extension_loan_application_task = TaskActivity(activity_name=u"展期放款申请",activity_status=u'审批',activity_page=u'extensionPage', task_assign_module='fabs.workflow.default', task_assign_function='loan_application_task', waiting=True)
        self.session.add(extension_loan_application_task)
        set_parameter(extension_loan_application_task, u"角色", u"客户经理")

        extension_subbranch_approve_task = TaskActivity(activity_name=u"展期支行长审批",activity_status=u'审批',activity_page=u'extensionPage', task_assign_module='fabs.workflow.default', task_assign_function='subbranch_approve_task', waiting=True)
        self.session.add(extension_subbranch_approve_task)
        set_parameter(extension_subbranch_approve_task, u"角色", u"支行行长")

        extension_credit_loan_task = TaskActivity(activity_name=u"展期放款", activity_status=u'审批结束',activity_page=u'extensionPage',task_assign_module='fabs.workflow.default', task_assign_function='credit_loan_task', waiting=True)
        self.session.add(extension_credit_loan_task)
        set_parameter(extension_credit_loan_task, u"角色", u"客户经理")

        """
        超权限
        """
        # 并行
        extension_ho_review_task = TaskActivity(activity_name=u"展期总行信贷审查", activity_status=u'审议',activity_page=u'extensionPage',task_assign_module='fabs.workflow.default', task_assign_function='ho_review_task', waiting=True)
        self.session.add(extension_ho_review_task)
        set_parameter(extension_ho_review_task, u"角色", u"总行审查岗")

        extension_ho_assessment_task = TaskActivity(activity_name=u"展期总行风险评价",activity_status=u'审议',activity_page=u'extensionPage' ,task_assign_module='fabs.workflow.default', task_assign_function='ho_assessment_task', waiting=True)
        self.session.add(extension_ho_assessment_task)
        set_parameter(extension_ho_assessment_task, u"角色", u"总行风险评价岗")

        extension_ho_riskowners_task= TaskActivity(activity_name=u"展期风险负责人审查",activity_status=u'审议',activity_page=u'extensionPage' ,task_assign_module='fabs.workflow.default', task_assign_function='ho_riskowners_task', waiting=True)
        self.session.add(extension_ho_riskowners_task)
        set_parameter(extension_ho_riskowners_task, u"角色", u"总行风险负责人")

        extension_riskowners_review_task = TaskActivity(activity_name=u"展期信贷负责人审查",activity_status=u'审议',activity_page=u'extensionPage' ,task_assign_module='fabs.workflow.default', task_assign_function='riskowners_review_task', waiting=True)
        self.session.add(extension_riskowners_review_task)
        set_parameter(extension_riskowners_review_task, u"角色", u"总行审查负责人")

        extension_riskowners_chairman_review_task = TaskActivity(activity_name=u"展期信贷负责人汇报董事长",activity_page=u'extensionPage',activity_status=u'审议', task_assign_module='fabs.workflow.default', task_assign_function='riskowners_chairman_review_task', waiting=True)
        self.session.add(extension_riskowners_chairman_review_task)
        set_parameter(extension_riskowners_chairman_review_task, u"角色", u"总行审查负责人")

        extension_bm_review_task = TaskActivity(activity_name=u"展期信贷分管行长审查",activity_status=u'审议',activity_page=u'extensionPage' ,task_assign_module='fabs.workflow.default', task_assign_function='bm_review_task', waiting=True)
        self.session.add(extension_bm_review_task)
        set_parameter(extension_bm_review_task, u"角色", u"分管信贷副行长")

        extension_committee_deliberation_task = TaskActivity(activity_name=u"展期总行信贷委员会审议",activity_status=u'审议', activity_page=u'extensionPage',task_assign_module='fabs.workflow.default', task_assign_function='committee_deliberation_task', waiting=True)
        self.session.add(extension_committee_deliberation_task)
        set_parameter(extension_committee_deliberation_task, u"角色", u"总行审贷委")

        extension_ho_president_task = TaskActivity(activity_name=u"展期总行行长审批",activity_status=u'审批',activity_page=u'extensionPage' ,task_assign_module='fabs.workflow.default', task_assign_function='ho_president_task', waiting=True)
        self.session.add(extension_ho_president_task)
        set_parameter(extension_ho_president_task, u"角色", u"总行行长")

        extension_subbranch_first_approve_task=TaskActivity(activity_name=u"展期支行行长预审批",activity_status=u'审批',activity_page=u'extensionPage', task_assign_module='fabs.workflow.default', task_assign_function='subbranch_first_approve_task', waiting=True)
        self.session.add(extension_subbranch_first_approve_task)
        set_parameter(extension_subbranch_first_approve_task, u"角色", u"支行行长")

        extension_ho_review_approve_task=TaskActivity(activity_name=u"展期信贷负责人审批",activity_status=u'审批',activity_page=u'extensionPage', task_assign_module='fabs.workflow.default', task_assign_function='ho_review_approve_task', waiting=True)
        self.session.add(extension_ho_review_approve_task)
        set_parameter(extension_ho_review_approve_task, u"角色", u"总行审查负责人")

        #授信卡授信调整
        adjustment_loan_application_task = TaskActivity(activity_name=u"授信调整申请",activity_status=u'审批',activity_page=u'adjustmentPage', task_assign_module='fabs.workflow.default', task_assign_function='adjustment_loan_application_task', waiting=True)
        self.session.add(adjustment_loan_application_task)
        set_parameter(adjustment_loan_application_task, u"角色", u"客户经理")

        adjustment_ho_review_approve_task=TaskActivity(activity_name=u"授信调整信贷负责人审批",activity_status=u'审批',activity_page=u'extensionPage', task_assign_module='fabs.workflow.default', task_assign_function='adjustment_ho_review_approve_task', waiting=True)
        self.session.add(adjustment_ho_review_approve_task)
        set_parameter(adjustment_ho_review_approve_task, u"角色", u"总行审查负责人")

        adjustment_credit_loan_task = TaskActivity(activity_name=u"授信调整放款", activity_status=u'审批结束',activity_page=u'adjustmentPage',task_assign_module='fabs.workflow.default', task_assign_function='adjustment_credit_loan_task', waiting=True)
        self.session.add(adjustment_credit_loan_task)
        set_parameter(adjustment_credit_loan_task, u"角色", u"客户经理")

        end = EndActivity(activity_name=u"归档", waiting=True)
        abort = EndActivity(activity_name=u"终止", waiting=True)

        self.session.add_all([lendingproposition_task, chcproposition_task, investigate_task, subbranch_assessment_task \
            , subbranch_review_task,   subbranch_deliberation_task, subbranch_president_task ])

        start = StartActivity(activity_name=u"开始贷款")

        #lendingproposition_task             贷款申请
        flow1 = Flow(from_activity=start, to_activity=lendingproposition_task, have_guard=False)

        #investigate_task                    预审
        flow2 = Flow(from_activity=lendingproposition_task, to_activity=investigate_task, have_guard=False)

        flow3 = Flow(from_activity=investigate_task, to_activity=write_report_task, have_guard=False)

        #总行流程不再需要支行风险评价和支行审查

        flow4 = Flow(from_activity=write_report_task, to_activity=subbranch_assessment_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='subbranch_amount_gurad')
        flow5 = Flow(from_activity=write_report_task, to_activity=subbranch_review_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='subbranch_amount_gurad')
        #                    |
        #                    V
        flow6 = Flow(from_activity=subbranch_assessment_task, to_activity=subbranch_deliberation_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='subbranch_assessment_gurad')
        flow7 = Flow(from_activity=subbranch_review_task, to_activity=subbranch_deliberation_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='subbranch_review_gurad')
        flow1001 = Flow(from_activity=write_report_task, to_activity=subbranch_deliberation_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='ho_amount_gurad')

        #subbranch_president_task            支行长审批
        # 未实现三个人审议
        #flow8 = Flow(from_activity=subbranch_deliberation_task, to_activity=subbranch_president_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='subbranch_deliberation_guard')
        flow8 = Flow(from_activity=subbranch_deliberation_task, to_activity=subbranch_president_task, have_guard=False)

        #loan_application_task               放款申请
        flow9 = Flow(from_activity=subbranch_president_task, to_activity=loan_application_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='subbranch_amount_gurad')
        #ho_review_task                      总行信贷审查
        flow12 = Flow(from_activity=subbranch_president_task, to_activity=ho_review_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='ho_amount_gurad')
        #ho_assessment_task                  总行风险评价
        flow13 = Flow(from_activity=subbranch_president_task, to_activity=ho_assessment_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='ho_amount_gurad')

        #subbranch_approve_task              支行长审批
        flow10 = Flow(from_activity=loan_application_task, to_activity=subbranch_approve_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='subbranch_prove_amount_gurad')

        #credit_loan_task                    客户经理放款
        flow11 = Flow(from_activity=subbranch_approve_task ,to_activity=credit_loan_task, have_guard=False)

        #ho_review_task                      总行信贷审查
        #ho_assessment_task                  总行风险评价
        #ho_riskowners_task                  风险负责人审查

        #riskowners_review_task              信贷负责人审查
        #bm_review_task                      信贷分管行长审查
        #committee_deliberation_task         总行信贷委员会审议
        #ho_president_task                   总行行长审批

        #ho_riskowners_task                  风险负责人审查
        flow14 = Flow(from_activity=ho_assessment_task, to_activity=ho_riskowners_task, have_guard=False)
        #riskowners_review_task              信贷负责人审查
        flow15 = Flow(from_activity=ho_riskowners_task, to_activity=riskowners_review_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='ho_assessment_gurad')
        # 信贷负责人审查
        flow16 = Flow(from_activity=ho_review_task, to_activity=riskowners_review_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='ho_review_gurad')
        #bm_review_task                      信贷分管行长审查
        flow17 = Flow(from_activity=riskowners_review_task, to_activity=bm_review_task, have_guard=False)

        #committee_deliberation_task         总行信贷委员会审议
        flow18 = Flow(from_activity=bm_review_task, to_activity=riskowners_chairman_review_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='investigate_credit_application_gurad')
        flow180 = Flow(from_activity=riskowners_chairman_review_task, to_activity=committee_deliberation_task, have_guard=False)
        #ho_president_task                    总行行长审批
        flow19 = Flow(from_activity=committee_deliberation_task, to_activity=ho_president_task, have_guard=False)
        #loan_application_task                放款申请
        flow20 = Flow(from_activity=ho_president_task, to_activity=loan_application_task, have_guard=False)

        #subbranch_first_approve_task         支行行长预审批
        flow21 = Flow(from_activity=loan_application_task, to_activity=subbranch_first_approve_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='ho_amount_gurad')

        #ho_review_approve_task               总行信贷部审批
        flow22 = Flow(from_activity=subbranch_first_approve_task, to_activity=ho_review_approve_task, have_guard=False)
        #ho_approve_task                      总行行长终审
        flow23 = Flow(from_activity=ho_review_approve_task, to_activity=credit_loan_task, have_guard=False)
        #放款
      #  flow24 = Flow(from_activity=ho_approve_task, to_activity=credit_loan_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='investigate_credit_application_gurad')

        # 贴现流转 --> 验票岗
        #flow25 = Flow(from_activity=write_report_task, to_activity=check_ticket_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='ticket_application_gurad')
        # 贴现流转 --> 会计部
        #flow26 = Flow(from_activity=write_report_task, to_activity=accountant_check_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='ticket_application_gurad')

        #验票岗流转 -->客户经理录入信息
        #flow27 = Flow(from_activity=check_ticket_task, to_activity=entering_info_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='ticket_approve_gurad')
        #会计部流转 -->客户经理录入信息
        #flow28 = Flow(from_activity=accountant_check_task, to_activity=entering_info_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='accountant_approve_gurad')

        #客户经理提交给支行长审批
        #flow29 = Flow(from_activity=entering_info_task, to_activity=subbranch_approve_task, have_guard=False)

        #分管行长 直接返回客户经理放款
        flow30 = Flow(from_activity=bm_review_task, to_activity=loan_application_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='investigate_comm_application_gurad')


        #flow99 = Flow(from_activity=credit_loan_task, to_activity=end, have_guard=False)

        self.session.add_all([flow1,flow2,flow3,flow4,flow5,flow6,flow7,flow8,flow9,flow10,flow11,flow12,flow13,flow14,flow15,flow16,flow17,flow18,flow19,flow20,flow21,flow22,flow23,flow30,flow180,flow1001])
        workflow = Workflow(workflow_name=u"贷款申请流程", start_activity = start)
        self.session.add_all([start, workflow])
        self.session.commit()


        start = StartActivity(activity_name=u"开始投资")
        #投资申请
        flow30 = Flow(from_activity=start, to_activity=invest_application_task, have_guard=False)
        #投资风险岗
        flow31 = Flow(from_activity=invest_application_task, to_activity=invest_review_task, have_guard=False)

        #投资审议小组
        flow32 = Flow(from_activity=invest_review_task, to_activity=invest_term_deliberation_task, have_guard=False)

        # 提交风险部
        flow33 = Flow(from_activity=invest_term_deliberation_task, to_activity=ho_riskowners_task, have_guard=False)

        # 提交财务部
        flow34 = Flow(from_activity=invest_term_deliberation_task, to_activity=finance_riskowners_task, have_guard=False)

        #财务部 --> 资金部负责人
        flow35 = Flow(from_activity=finance_riskowners_task, to_activity=capital_riskowners_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='finance_invest_gurad')

        #风险部 --> 资金部负责人
        flow36 = Flow(from_activity=ho_riskowners_task, to_activity= capital_riskowners_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='riskowners_invest_gurad')

        # 资金负责人 -->分管行长
        flow37 = Flow(from_activity= capital_riskowners_task, to_activity=invest_bm_review_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_no_abort')
        #否决权
        flow3701 = Flow(from_activity= capital_riskowners_task, to_activity=abort, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_abort')
        #分管行长 --> 投资审议委员会 否决
        flow38 = Flow(from_activity=invest_bm_review_task, to_activity=invest_deliberation_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_no_abort')
        flow3801 = Flow(from_activity=invest_bm_review_task, to_activity=abort, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_abort')

        #投资审议委员会--> 投资交易岗
        flow39 = Flow(from_activity=invest_deliberation_task, to_activity=invest_entering_task, have_guard=False)

        #客户经理提交给资金部负责人
        flow40 = Flow(from_activity=invest_entering_task, to_activity=invest_enering_review_task, have_guard=False)
        #增加资金录入信息复核
        flow41 = Flow(from_activity=invest_enering_review_task, to_activity=finance_riskowners_approve_task, have_guard=False)
        #资金分管行长审批
        flow42 = Flow(from_activity=finance_riskowners_approve_task, to_activity=bank_invest_bm_review_task, have_guard=False)

        #资金风管行长 --> 总行行长审批
        flow43 = Flow(from_activity=bank_invest_bm_review_task, to_activity=invest_ho_approve_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_no_abort')
        flow4301 = Flow(from_activity=bank_invest_bm_review_task, to_activity=abort, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_abort')
        #总行长 --> 投资交易岗
        flow44 = Flow(from_activity=invest_ho_approve_task, to_activity=invest_data_check, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_no_abort')
        flow4401 = Flow(from_activity=invest_ho_approve_task, to_activity=abort, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_abort')

        self.session.add_all([flow31,flow32,flow33,flow34,flow35,flow36,flow37,flow3701,flow38,flow3801,flow39,flow40,flow41,flow42,flow43,flow4301,flow44,flow4401])
        workflow = Workflow(workflow_name=u"投资流程", start_activity = start)
        self.session.add_all([start, workflow])
        self.session.commit()

        #转贷大表申请
        start = StartActivity(activity_name=u"转贷大表开始")
        flow101 = Flow(from_activity=start, to_activity=chcproposition_task, have_guard=False)

        #并行
        flow102 = Flow(from_activity=chcproposition_task, to_activity=subbranch_assessment_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='chc_credit_application_gurad')
        flow103 = Flow(from_activity=chcproposition_task, to_activity=subbranch_review_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='chc_credit_application_gurad')
        #转贷大表预审
        flow104 = Flow(from_activity=loan_application_task, to_activity=investigate_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='chc_credit_application_gurad')

        #调查报告到支行长审批
        flow105 = Flow(from_activity=write_report_task, to_activity=subbranch_approve_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='chc_credit_application_gurad')

        self.session.add_all([flow101,flow102,flow103,flow104,flow105])
        workflow = Workflow(workflow_name=u"转贷大表流程", start_activity = start)
        self.session.add_all([start, workflow])
        self.session.commit()

        start = StartActivity(activity_name=u"开始同业业务")
        #同业交易岗申请
        flow201 = Flow(from_activity=start, to_activity=bank_application_task, have_guard=False)
        #申请->资金风险岗
        flow202 = Flow(from_activity=bank_application_task, to_activity=bank_review_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_gurad')

        #资金部风险岗审查->资金负责人
        flow203 = Flow(from_activity=bank_review_task, to_activity=bank_capital_charge_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_no_transfer_discount_application_gurad')

        #转贴现业务需要经过营业部
        flow204= Flow(from_activity=bank_review_task, to_activity=branch_transfer_discount_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_transfer_discount_application_gurad')
        flow205= Flow(from_activity=branch_transfer_discount_task, to_activity=branch_transfer_discount_review_task, have_guard=False)
        flow206= Flow(from_activity=branch_transfer_discount_review_task, to_activity=bank_capital_charge_task, have_guard=False)

        #资金部风险岗审查->同业分管行长审查
        flow207= Flow(from_activity=bank_capital_charge_task, to_activity=bank_bm_review_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_no_abort')
        flow20701= Flow(from_activity=bank_capital_charge_task, to_activity=abort, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_abort')

        #同业分管行长审查->同业交易岗
        flow208= Flow(from_activity=bank_bm_review_task, to_activity=bank_trade_data_check, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_bm_amount_gurad')
        flow20801= Flow(from_activity=bank_bm_review_task, to_activity=abort, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_abort')
        flow209= Flow(from_activity=bank_bm_review_task, to_activity=bank_ho_approve_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_ho_amount_gurad')
        #总行长终审->同业交易岗
        flow210= Flow(from_activity=bank_ho_approve_task, to_activity=bank_trade_data_check, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_no_abort')
        flow21001= Flow(from_activity=bank_ho_approve_task, to_activity=abort, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_abort')

        self.session.add_all([flow201,flow202,flow203,flow204,flow205,flow206,flow207,flow20701,flow208,flow20801,flow209,flow210,flow21001])
        workflow = Workflow(workflow_name=u"同业业务流程", start_activity = start)
        self.session.add_all([start, workflow])
        self.session.commit()

        start = StartActivity(activity_name=u"开始贴现")
        #贴现业务申请
        flow301 = Flow(from_activity=start, to_activity=lending_discount_task, have_guard=False)
        #申请->贴现审查
        flow302 = Flow(from_activity=lending_discount_task, to_activity=discount_investigate_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='discount_application_no_quote_report')
        flow303 = Flow(from_activity=lending_discount_task, to_activity=discount_info_input, have_guard=True, guard_module='fabs.workflow.default', guard_function='discount_application_quote_report')

        flow304 = Flow(from_activity=discount_investigate_task, to_activity=discount_write_report_task, have_guard=False)

        flow305 = Flow(from_activity=discount_write_report_task, to_activity=discount_subbranch_assessment_task, have_guard=False)
        flow306 = Flow(from_activity=discount_write_report_task, to_activity=discount_subbranch_review_task, have_guard=False)
        flow307 = Flow(from_activity=discount_subbranch_assessment_task, to_activity=discount_subbranch_deliberation_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='discount_subbranch_assessment_gurad')
        flow308 = Flow(from_activity=discount_subbranch_review_task, to_activity=discount_subbranch_deliberation_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='discount_subbranch_review_gurad')
        flow309 = Flow(from_activity=discount_subbranch_deliberation_task, to_activity=discount_subbranch_president_task, have_guard=False)

        #贴现审查->贴现信息录入
        flow310 = Flow(from_activity=discount_subbranch_president_task, to_activity=discount_info_input, have_guard=False)
        flow311 = Flow(from_activity=discount_info_input, to_activity=discount_approve_task, have_guard=False)
        #贴现放款
        flow312 = Flow(from_activity=discount_approve_task, to_activity=discount_loan_task, have_guard=False)
        self.session.add_all([flow301,flow302,flow303,flow304,flow305,flow306,flow307,flow308,flow309,flow310,flow311,flow312])
        workflow = Workflow(workflow_name=u"贴现业务流程", start_activity = start)
        self.session.add_all([start, workflow])
        self.session.commit()

        start = StartActivity(activity_name=u"开始签发")
        #签发申请
        flow701 = Flow(from_activity=start, to_activity=acceptance_lending_task, have_guard=False)
        flow702 = Flow(from_activity=acceptance_lending_task, to_activity=acceptance_investigate_task, have_guard=False)
        #签发预审
        flow703 = Flow(from_activity=acceptance_investigate_task, to_activity=acceptance_write_report_task, have_guard=False)

        #签发撰写调查报告
        flow704 = Flow(from_activity=acceptance_write_report_task, to_activity=acceptance_subbranch_assessment_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='acceptance_subbranch_amount_gurad')
        flow705 = Flow(from_activity=acceptance_write_report_task, to_activity=acceptance_subbranch_review_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='acceptance_subbranch_amount_gurad')

        flow7001 = Flow(from_activity=acceptance_write_report_task, to_activity=acceptance_subbranch_deliberation_task, have_guard=True,guard_module='fabs.workflow.default',guard_function='acceptance_ho_amount_gurad')
        #签发支行风险评价岗
        flow706 = Flow(from_activity=acceptance_subbranch_assessment_task, to_activity=acceptance_subbranch_deliberation_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='acceptance_subbranch_assessment_gurad')
        #签发支行审查岗
        flow707 = Flow(from_activity=acceptance_subbranch_review_task, to_activity=acceptance_subbranch_deliberation_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='acceptance_subbranch_review_gurad')
        #签发支行审贷小组审议
        flow708 = Flow(from_activity=acceptance_subbranch_deliberation_task, to_activity=acceptance_subbranch_president_task, have_guard=False)

        #支行审议->签发放款申请
        flow709 = Flow(from_activity=acceptance_subbranch_president_task, to_activity=acceptance_loan_application_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='acceptance_subbranch_amount_gurad')
        #签发总行信贷审查
        flow712 = Flow(from_activity=acceptance_subbranch_president_task, to_activity=acceptance_ho_review_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='acceptance_ho_amount_gurad')
        #签发总行风险评价
        flow713 = Flow(from_activity=acceptance_subbranch_president_task, to_activity=acceptance_ho_assessment_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='acceptance_ho_amount_gurad')
        #签发支行长审批
        flow710 = Flow(from_activity=acceptance_loan_application_task, to_activity=acceptance_subbranch_approve_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='acceptance_subbranch_prove_amount_gurad')

        #签发客户经理放款
        flow711 = Flow(from_activity=acceptance_subbranch_approve_task ,to_activity=acceptance_credit_loan_task, have_guard=False)

        #总行信贷审查
        #总行风险评价
        #风险负责人审查

        #信贷负责人审查
        #信贷分管行长审查
        #总行信贷委员会审议
        #总行行长审批

        #签发风险负责人审查
        flow714 = Flow(from_activity=acceptance_ho_assessment_task, to_activity=acceptance_ho_riskowners_task, have_guard=False)
        #签发信贷负责人审查
        flow715 = Flow(from_activity=acceptance_ho_riskowners_task, to_activity=acceptance_riskowners_review_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='acceptance_ho_assessment_gurad')
        #签发信贷负责人审查
        flow716 = Flow(from_activity=acceptance_ho_review_task, to_activity=acceptance_riskowners_review_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='acceptance_ho_review_gurad')
        #签发信贷分管行长审查
        flow717 = Flow(from_activity=acceptance_riskowners_review_task, to_activity=acceptance_bm_review_task, have_guard=False)

        #签发总行信贷委员会审议
        flow718 = Flow(from_activity=acceptance_bm_review_task, to_activity=acceptance_riskowners_chairman_review_task, have_guard=False)

        flow7180 = Flow(from_activity=acceptance_riskowners_chairman_review_task, to_activity=acceptance_committee_deliberation_task, have_guard=False)
        #签发总行行长审批
        flow719 = Flow(from_activity=acceptance_committee_deliberation_task, to_activity=acceptance_ho_president_task, have_guard=False)
        #签发放款申请
        flow720 = Flow(from_activity=acceptance_ho_president_task, to_activity=acceptance_loan_application_task, have_guard=False)

        #签发支行行长预审批
        flow721 = Flow(from_activity=acceptance_loan_application_task, to_activity=acceptance_subbranch_first_approve_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='acceptance_ho_amount_gurad')

        #签发总行信贷部审批
        flow722 = Flow(from_activity=acceptance_subbranch_first_approve_task, to_activity=acceptance_ho_review_approve_task, have_guard=False)
        #签发总行行长终审
        flow723 = Flow(from_activity=acceptance_ho_review_approve_task, to_activity=acceptance_credit_loan_task, have_guard=False)

        self.session.add_all([flow701,flow702,flow703,flow704,flow705,flow706,flow707,flow708,flow709,flow710,flow711,flow712,flow713,flow714,flow715,flow716,flow717,flow718,flow719,flow720,flow721,flow722,flow723,flow7180,flow7001])
        workflow = Workflow(workflow_name=u"承兑汇票签发申请流程", start_activity = start)
        self.session.add_all([start, workflow])
        self.session.commit()


        start = StartActivity(activity_name=u"开始统一授信")
        #统一授信业务申请
        flow401 = Flow(from_activity=start, to_activity=credit_granting_apply_task, have_guard=False)
        #申请->支行审贷小组授信审议
        flow402 = Flow(from_activity=credit_granting_apply_task, to_activity=credit_granting_subbranch_deliberation_task, have_guard=False)
        #审议->支行长审批
        flow403 = Flow(from_activity=credit_granting_subbranch_deliberation_task, to_activity=credit_granting_subbranch_president_task, have_guard=False)
        #支行长审批->总行授信审查
        flow404 = Flow(from_activity=credit_granting_subbranch_president_task, to_activity=ho_credit_granting_review_task, have_guard=False)
        #总行授信审查->总行审贷委员会授信审查
        flow405 = Flow(from_activity=ho_credit_granting_review_task, to_activity=credit_granting_committee_deliberation_task, have_guard=False)
        #总行审贷委员会授信审查->总行长授信审批
        flow406 = Flow(from_activity=credit_granting_committee_deliberation_task, to_activity=ho_credit_granting_president_task, have_guard=False)
        self.session.add_all([flow401,flow402,flow403,flow404,flow405,flow406])
        workflow = Workflow(workflow_name=u"统一授信业务流程", start_activity = start)
        self.session.add_all([start, workflow])
        self.session.commit()

        start = StartActivity(activity_name=u"开始五级分类")
        flow501 = Flow(from_activity=start, to_activity=credit_class_apply_task, have_guard=False)
        flow502 = Flow(from_activity=credit_class_apply_task, to_activity=credit_class_subbranch_deliberation_task, have_guard=False)
        flow503 = Flow(from_activity=credit_class_subbranch_deliberation_task, to_activity=credit_class_subbranch_president_task, have_guard=False)
        flow504 = Flow(from_activity=credit_class_subbranch_president_task, to_activity=ho_credit_class_review_task, have_guard=False)
        flow505 = Flow(from_activity=ho_credit_class_review_task, to_activity=ho_credit_class_bm_review_task, have_guard=False)
        flow506 = Flow(from_activity=ho_credit_class_bm_review_task, to_activity=ho_credit_class_committee_deliberation_task, have_guard=False)
        flow507 = Flow(from_activity=ho_credit_class_committee_deliberation_task, to_activity=ho_credit_class_president_task, have_guard=False)
        self.session.add_all([flow501,flow502,flow503,flow504,flow505,flow506,flow507])
        workflow = Workflow(workflow_name=u"五级分类业务流程", start_activity = start)
        self.session.add_all([start, workflow])
        self.session.commit()

        start = StartActivity(activity_name=u"开始抵贷资产申请")
        flow601 = Flow(from_activity=start, to_activity=repossession_apply_task, have_guard=False)
        flow602 = Flow(from_activity=repossession_apply_task, to_activity=repossession_subbranch_deliberation_task, have_guard=False)
        flow603 = Flow(from_activity=repossession_subbranch_deliberation_task, to_activity=repossession_subbranch_president_task, have_guard=False)
        flow604 = Flow(from_activity=repossession_subbranch_president_task, to_activity=repossession_ho_assessment_task, have_guard=False)
        flow605 = Flow(from_activity=repossession_ho_assessment_task, to_activity=repossession_finance_charge_task, have_guard=False)
        flow606 = Flow(from_activity=repossession_ho_assessment_task, to_activity=repossession_ho_loan_charge_task, have_guard=False)
        flow607 = Flow(from_activity=repossession_finance_charge_task, to_activity=repossession_ho_riskowners_task, have_guard=False)
        flow608 = Flow(from_activity=repossession_ho_loan_charge_task, to_activity=repossession_ho_riskowners_task, have_guard=False)
        flow609 = Flow(from_activity=repossession_ho_riskowners_task, to_activity=repossession_ho_credit_bm_review_task, have_guard=False)
        flow610 = Flow(from_activity=repossession_ho_credit_bm_review_task, to_activity=repossession_ho_credit_committee_deliberation_task, have_guard=False)
        flow611 = Flow(from_activity=repossession_ho_credit_committee_deliberation_task, to_activity=repossession_ho_credit_class_president_task, have_guard=False)
        flow612 = Flow(from_activity=repossession_ho_credit_class_president_task, to_activity=repossession_standingbook_task, have_guard=False)
        self.session.add_all([flow601,flow602,flow603,flow604,flow605,flow606,flow607,flow608,flow609,flow610,flow611,flow612])
        workflow = Workflow(workflow_name=u"抵贷资产流程", start_activity = start)
        self.session.add_all([start, workflow])
        self.session.commit()

    
        start = StartActivity(activity_name=u"开始贷款展期")
        #展期申请
        flow801 = Flow(from_activity=start, to_activity=extension_lendingproposition_task, have_guard=False)
        flow802 = Flow(from_activity=extension_lendingproposition_task, to_activity=extension_investigate_task, have_guard=False)
        #展期预审
        flow803 = Flow(from_activity=extension_investigate_task, to_activity=extension_write_report_task, have_guard=False)

        #展期撰写调查报告
        flow804 = Flow(from_activity=extension_write_report_task, to_activity=extension_subbranch_deliberation_task, have_guard=False)
        #展期支行审贷小组审议
        flow805 = Flow(from_activity=extension_subbranch_deliberation_task, to_activity=extension_subbranch_president_task, have_guard=False)

        #展期总行信贷审查
        flow806 = Flow(from_activity=extension_subbranch_president_task, to_activity=extension_ho_review_task, have_guard=False)
        #展期总行风险评价
        flow807 = Flow(from_activity=extension_subbranch_president_task, to_activity=extension_ho_assessment_task, have_guard=False)
        #展期支行长审批
        flow808 = Flow(from_activity=extension_loan_application_task, to_activity=extension_subbranch_approve_task, have_guard=False)

        #展期风险负责人审查
        flow809 = Flow(from_activity=extension_ho_assessment_task, to_activity=extension_ho_riskowners_task, have_guard=False)
        #展期信贷负责人审查
        flow810 = Flow(from_activity=extension_ho_riskowners_task, to_activity=extension_riskowners_review_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='extension_ho_assessment_gurad')
        #展期信贷负责人审查
        flow811 = Flow(from_activity=extension_ho_review_task, to_activity=extension_riskowners_review_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='extension_ho_review_gurad')
        #展期信贷分管行长审查
        flow812 = Flow(from_activity=extension_riskowners_review_task, to_activity=extension_bm_review_task, have_guard=False)

        #展期总行信贷委员会审议
        flow813 = Flow(from_activity=extension_bm_review_task, to_activity=extension_riskowners_chairman_review_task, have_guard=False)
        flow814 = Flow(from_activity=extension_riskowners_chairman_review_task, to_activity=extension_committee_deliberation_task, have_guard=False)
        #展期总行行长审批
        flow815 = Flow(from_activity=extension_committee_deliberation_task, to_activity=extension_ho_president_task, have_guard=False)
        #展期放款申请
        flow816 = Flow(from_activity=extension_ho_president_task, to_activity=extension_loan_application_task, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_no_abort')
        #否决权
        flow8161 = Flow(from_activity=extension_ho_president_task, to_activity=abort, have_guard=True,guard_module='fabs.workflow.default', guard_function='bank_application_abort')

        #展期支行行长预审批
        flow817 = Flow(from_activity=extension_loan_application_task, to_activity=extension_subbranch_first_approve_task, have_guard=False)

        #展期总行信贷部审批
        flow818 = Flow(from_activity=extension_subbranch_first_approve_task, to_activity=extension_ho_review_approve_task, have_guard=False)
        #展期总行行长终审
        flow819 = Flow(from_activity=extension_ho_review_approve_task, to_activity=extension_credit_loan_task, have_guard=False)

        self.session.add_all([flow801,flow802,flow803,flow804,flow805,flow806,flow807,flow808,flow809,flow810,flow811,flow812,flow813,flow814,flow815,flow816,flow817,flow818,flow819,flow8161])
        workflow = Workflow(workflow_name=u"贷款展期申请流程", start_activity = start)
        self.session.add_all([start, workflow])
        self.session.commit()

        start = StartActivity(activity_name=u"开始授信调整")
        #展期申请
        flow881 = Flow(from_activity=start, to_activity=extension_lendingproposition_task, have_guard=False)
        flow882 = Flow(from_activity=extension_lendingproposition_task, to_activity=adjustment_ho_review_approve_task, have_guard=False)
        flow883 = Flow(from_activity=adjustment_ho_review_approve_task, to_activity=adjustment_credit_loan_task, have_guard=False)
        self.session.add_all([flow881,flow882,flow883])
        workflow = Workflow(workflow_name=u"授信调整流程", start_activity = start)
        self.session.add_all([start, workflow])
        self.session.commit()


    def init_user_group(self):
        """
        USER SESSION
        """

        log.debug("start init user group !")
        auth_type = AuthenticationType(code=u'010001',name=u'LOGIN',description=u'LOGIN')
        self.session.add(auth_type)
        '''
        bran_grp_tell = test_loaddb.BranGrpTell()
        bran_grp_tell.func(self.session)
        '''

        u1 = User(user_name=u'00530',name=u'王鑫'); f1 = Password(user=u1,algorithm=u'MD5',credential=u'qwe123')
        u2 = User(user_name=u'00511',name=u'王琛'); f2 = Password(user=u2,algorithm=u'MD5',credential=u'qwe123')
        u3 = User(user_name=u'00140',name=u'李建峰'); f3 = Password(user=u3,algorithm=u'MD5',credential=u'qwe123')
        u4 = User(user_name=u'00510',name=u'王一琛'); f4 = Password(user=u4,algorithm=u'MD5',credential=u'qwe123')
        u5 = User(user_name=u'00541',name=u'郝晶'); f5 = Password(user=u5,algorithm=u'MD5',credential=u'qwe123')
        u6 = User(user_name=u'00779',name=u'郭强'); f6 = Password(user=u6,algorithm=u'MD5',credential=u'qwe123')
        u7 = User(user_name=u'00513',name=u'陈芳'); f7 = Password(user=u7,algorithm=u'MD5',credential=u'qwe123')
        u8 = User(user_name=u'00136',name=u'井清泉'); f8 = Password(user=u8,algorithm=u'MD5',credential=u'qwe123')

        self.session.add_all([f1,f2,f3,f4,f5,f6,f7,f8])

        u11 = User(user_name=u'00149',name=u'苗小梅'); f11 = Password(user=u11,algorithm=u'MD5',credential=u'qwe123')
        u12 = User(user_name=u'00335',name=u'宋文'); f12 = Password(user=u12,algorithm=u'MD5',credential=u'qwe123')
        u13 = User(user_name=u'91014',name=u'陈续红'); f13 = Password(user=u13,algorithm=u'MD5',credential=u'qwe123')
        u14 = User(user_name=u'00477',name=u'郑茂萍'); f14 = Password(user=u14,algorithm=u'MD5',credential=u'qwe123')
        u15 = User(user_name=u'00005',name=u'魏霞'); f15 = Password(user=u15,algorithm=u'MD5',credential=u'qwe123')
        u16 = User(user_name=u'00003',name=u'王广智'); f16 = Password(user=u16,algorithm=u'MD5',credential=u'qwe123')
        u17 = User(user_name=u'00009',name=u'何玉娥'); f17 = Password(user=u17,algorithm=u'MD5',credential=u'qwe123')
        u18 = User(user_name=u'00002',name=u'崔洪杰'); f18 = Password(user=u18,algorithm=u'MD5',credential=u'qwe123')

        self.session.add_all([f11,f12,f13,f14,f15,f16,f17,f18])

        u21 = User(user_name=u'01000'); f21 = Password(user=u21,algorithm=u'MD5',credential=u'qwe123')
        u22 = User(user_name=u'01001'); f22 = Password(user=u22,algorithm=u'MD5',credential=u'qwe123')
        u23 = User(user_name=u'01002'); f23 = Password(user=u23,algorithm=u'MD5',credential=u'qwe123')
        u24 = User(user_name=u'01003'); f24 = Password(user=u24,algorithm=u'MD5',credential=u'qwe123')
        u25 = User(user_name=u'01004'); f25 = Password(user=u25,algorithm=u'MD5',credential=u'qwe123')
        u26 = User(user_name=u'01005'); f26 = Password(user=u26,algorithm=u'MD5',credential=u'qwe123')
        u27 = User(user_name=u'01006'); f27 = Password(user=u27,algorithm=u'MD5',credential=u'qwe123')
        u28 = User(user_name=u'01007'); f28 = Password(user=u28,algorithm=u'MD5',credential=u'qwe123')
        u29 = User(user_name=u'01008'); f29 = Password(user=u29,algorithm=u'MD5',credential=u'qwe123')
        u30 = User(user_name=u'01009'); f30 = Password(user=u30,algorithm=u'MD5',credential=u'qwe123')
        u31 = User(user_name=u'01010'); f31 = Password(user=u31,algorithm=u'MD5',credential=u'qwe123')
        self.session.add_all([f21,f22,f23,f24,f25,f26,f27,f28,f29,f30,f31])

        #贷款申请					客户经理
        #预审						支行审查岗
        #支行风险评价				支行风险评价岗
        #支行审查					支行审查岗
        #支行审贷小组审议			支行审贷小组
        #支行长审批				    支行行长

        g1 = Group(group_name=u"客户经理")
        g2 = Group(group_name=u"支行风险评价岗")
        g3 = Group(group_name=u"支行审查岗")
        g4 = Group(group_name=u"支行审贷小组")
        g5 = Group(group_name=u"支行行长")
        g6 = Group(group_name=u"总行审查岗")
        g7 = Group(group_name=u"总行审查负责人")
        g8 = Group(group_name=u"总行风险评价岗")
        g9 = Group(group_name=u"总行风险负责人")
        g10 = Group(group_name=u"总行审贷委")
        g11 = Group(group_name=u"分管信贷副行长")
        g12 = Group(group_name=u"总行行长")

        g13=Group(group_name=u"验票岗")
        g14=Group(group_name=u"会计部")

        g15=Group(group_name=u"投资交易岗")
        g16=Group(group_name=u"资金部风险岗")
        g17=Group(group_name=u"资金部负责人")
        g18=Group(group_name=u"财务部负责人")
        g19=Group(group_name=u"投资审议委员会")
        g20=Group(group_name=u"投资审议小组")
        g21 = Group(group_name=u"分管资金副行长")

        g22 = Group(group_name=u"同业交易岗")
        g23 = Group(group_name=u"营业部转贴现岗")
        g24 = Group(group_name=u"营业部转贴现负责人")
        g25 = Group(group_name=u"分管同业副行长")
        g26 = Group(group_name=u"投资交易复核岗")
	g27 = Group(group_name=u"综合柜员")

        self.session.add_all(
            [
                UserGroup(user=u1,group=g1),
                UserGroup(user=u2,group=g1),
                UserGroup(user=u3,group=g1),
                UserGroup(user=u4,group=g1),
                UserGroup(user=u5,group=g1),
                UserGroup(user=u3,group=g2),
                UserGroup(user=u6,group=g3),
                UserGroup(user=u6,group=g4),
                UserGroup(user=u1,group=g4),
                UserGroup(user=u7,group=g4),
                UserGroup(user=u8,group=g5),
                UserGroup(user=u11,group=g6),
                UserGroup(user=u12,group=g7),
                UserGroup(user=u13,group=g8),
                UserGroup(user=u14,group=g9),

                UserGroup(user=u15,group=g10),
                UserGroup(user=u16,group=g10),
                UserGroup(user=u12,group=g10),
                UserGroup(user=u14,group=g10),
                UserGroup(user=u17,group=g10),
                UserGroup(user=u18,group=g11),
                UserGroup(user=u18,group=g12),


                UserGroup(user=u1,group=g13),
                UserGroup(user=u2,group=g13),
                UserGroup(user=u3,group=g13),
                UserGroup(user=u4,group=g13),
                UserGroup(user=u5,group=g13),
                UserGroup(user=u7,group=g14),

                UserGroup(user=u21,group=g15),
                UserGroup(user=u22,group=g16),
                UserGroup(user=u23,group=g17),
                UserGroup(user=u24,group=g18),
                UserGroup(user=u14,group=g19),
                UserGroup(user=u12,group=g19),
                UserGroup(user=u17,group=g19),
                UserGroup(user=u18,group=g19),
                UserGroup(user=u25,group=g19),
                UserGroup(user=u26,group=g19),
                UserGroup(user=u27,group=g19),
                UserGroup(user=u28,group=g19),
                UserGroup(user=u21,group=g20),
                UserGroup(user=u22,group=g20),
                UserGroup(user=u23,group=g20),
                UserGroup(user=u17,group=g21),
                UserGroup(user=u17,group=g25),
                UserGroup(user=u21,group=g22),
                UserGroup(user=u29,group=g23),
                UserGroup(user=u30,group=g24),
                UserGroup(user=u31,group=g26),
		UserGroup(user=u4,group=g27),
            ]
        )
        
        b1 = Branch(branch_code=u"000000", branch_name=u"乌海银行")
        b2 = Branch(branch_code=u"000004", branch_name=u"科技部")
        b3 = Branch(branch_code=u"047301", branch_name=u"胜利街支行")
        b4 = Branch(branch_code=u"047308", branch_name=u"海南支行")
        b5 = Branch(branch_code=u"047702", branch_name=u"鄂尔多斯营业部")

        self.session.add_all(
            [
                UserBranch(user=u1, branch=b2),
                UserBranch(user=u2, branch=b3),
                UserBranch(user=u3, branch=b2),
                UserBranch(user=u4, branch=b4),
                UserBranch(user=u5, branch=b1),
                UserBranch(user=u6, branch=b2),
                UserBranch(user=u7, branch=b2),
                UserBranch(user=u8, branch=b1),

                UserBranch(user=u11,branch=b1),
                UserBranch(user=u12,branch=b1),
                UserBranch(user=u13,branch=b1),
                UserBranch(user=u14,branch=b5),
                UserBranch(user=u15,branch=b1),
                UserBranch(user=u16,branch=b1),
                UserBranch(user=u17,branch=b1),
                UserBranch(user=u18,branch=b1),
            ]
        )

        self.session.commit()

    def init_customer(self):
        """
        Customer Info
        """
        logging.debug("start init customer info!")

        user = self.session.query(User).filter(User.user_name=="00510").first()


        man=Resident(no='100012874',state=u'完善',name=u'李顺义', ric=u'150303195802220015', current_name = u'李顺义', gender=u'男性', birthday=datetime.datetime.now(), ethnicity =u'汉族', politics_status=u"群众", marital_status=u"已婚")
        customer = Customer(party=man, cust_type="person")
        branch=self.session.query(Branch).join(UserBranch,Branch.role_id == UserBranch.branch_id).filter(UserBranch.user_id == user.role_id).first()
        party_role = PartyRole(party=man,branch_code=branch.branch_code)
        self.session.add(party_role)
        Certificate(party=man, cert_type=u'身份证', cert_no='150303195802220015', issue_date=datetime.datetime.now(), issue_office=u'xxx', thru_date = datetime.date(2055, 1, 1))

        man6=Resident(no='100002753',state=u'完善',name=u'张晓东', ric=u'152724198208030015', current_name=u'张晓东', gender=u'男性', birthday=datetime.datetime.now(), ethnicity =u'汉族', politics_status=u"中国共产党")
        customer6 = Customer(party=man6, cust_type="person")
        Certificate(party=man6, cert_type=u'身份证', cert_no='152724198208030015', issue_date=datetime.datetime.now(), issue_office=u'xxx', thru_date = datetime.date(2055, 1, 1))


        man2=Resident(no='100060148',name=u'刘永霞', ric=u'152822197310035726', current_name=u'刘永霞', gender=u'女性', birthday=datetime.datetime.strptime('1973-10-03','%Y-%m-%d'), ethnicity =u'汉族')
        customer2 = Customer(party=man2, cust_type="person")
        Certificate(party=man2, cert_type=u'身份证', cert_no='152822197310035726', issue_date=datetime.datetime.now(), issue_office=u'xxx', thru_date = datetime.date(2055, 1, 1))
        self.user = User(party = man2)
        self.session.add_all([self.user, customer, customer2, customer6])
        self.session.commit()

        company=Company(no='500000077',name=u'乌海市三金煤制品有限责任公司',company_cn_name=u'乌海市三金煤制品有限责任公司',org_id='X2728906-X',company_type=u'私营', cust_kind=u'工业', company_capital=u'小型企业', cust_field=u'生产流通', company_kind=u'有限责任公司', industry_class=u'B-采掘业', industry_large_class=u'B06-煤炭开采和洗选业' ,industry_small_class=u'B0610-烟煤和无烟煤开采洗选' ,industry_mid_class=u'B061-烟煤和无烟煤开采洗选',law_duty=u'有限责任公司',crop_type=u'企业法人',corp_name=u'李俊俊', corp_id_num='150105751024603', corp_credit_card=u'否', loan_card_no='512010000010167', reg_check_result=u'年审合格', reg_thru_date='2030-05-24',last_check_date='2013-06-06',nat_tax_id=u'150304X2728906X', loc_tax_id='150304X2728906X',base_bank=u'我行',in_credit_class='C',local_field=u'否',company_cust=u'否',special_licence=u'否',import_export=u'否',rating_type=u'工业(化工)',relation_desc=u'无关联关系',fin_rep_type=u'通用类', relation_corp=u'非常密切',risk_flag=u'否',blacklist_flag=u'否',init_loan_date=u'2006-08-24',register_date=u'2007-10-23',register_name=u'00309-刘云平',register_branch=u'乌达支行',asset_liability_date='201405',company_status=u'正常',asset_amount='32680000',liability_amount='12240000', company_reg_date=u'2000-05-25',company_fashion=u'批发',reg_cur_type=u'人民币', paid_cur_type=u'人民币', reg_amount='13000000', paid_amount='13000000', reg_country=u'中国', reg_state=u'150304-乌达区',reg_address=u'内蒙古自治区乌海市乌达区乌阿公路六公里处', bus_address=u'乌海市乌达区乌阿公路六公里处', res_person=u'李俊俊',reg_headship=u'董事长',reg_id_num=u'150105751024603', company_opt_owner=u'国有', company_opt_type=u'国有出让', company_area=u'40609',company_house_owner=u'国有',opt_scope=u'精煤',opt_field=u'洗精煤',prod_equip=u'跳汏式洗煤机')
        customer = Customer(party=company, cust_type="company")
        self.session.add(customer)
        self.session.commit()
        company=Company(no='500000154',name=u'乌海市明星焦化有限责任公司',company_cn_name=u'乌海市明星焦化有限责任公司',org_id='73614527-X',company_type=u'股份', cust_kind=u'工业', company_capital=u'小型企业', cust_field=u'生产流通', company_kind=u'有限责任公司', industry_class=u'C-制造业', industry_large_class=u'C25-石油加工、炼焦和核燃料加工业' ,industry_small_class=u'C252-炼焦' ,industry_mid_class=u'C2520-炼焦',law_duty=u'有限责任公司',crop_type=u'企业法人',corp_name=u'刘占华', corp_id_num='150302470217151', corp_credit_card=u'否', loan_card_no='512020000039182', reg_check_result=u'年审合格', reg_thru_date='2027-03-27',last_check_date='2007-03-27',nat_tax_id=u'15030373614527X', loc_tax_id='15030373614527X',base_bank=u'我行',in_credit_class='C',local_field=u'否',company_cust=u'否',special_licence=u'否',import_export=u'否',rating_type=u'工业(化工)',relation_desc=u'无关联关系',fin_rep_type=u'通用类', relation_corp=u'非常密切',risk_flag=u'否',blacklist_flag=u'否',init_loan_date=u'2006-12-19',register_date=u'2007-10-28',register_name=u'00149-苗小梅',register_branch=u'海南支行',asset_liability_date='201405',company_status=u'正常',asset_amount='32680000',liability_amount='0', company_reg_date=u'2000-05-25',company_fashion=u'批发',reg_cur_type=u'人民币', paid_cur_type=u'人民币', reg_amount='13000000', paid_amount='13000000', reg_country=u'中国', reg_address=u'内蒙古自治区乌海市海南区', bus_address=u'乌海市海南区', res_person=u'李俊俊',reg_headship=u'董事长',reg_id_num=u'150105751024603', company_opt_owner=u'国有', company_opt_type=u'国有出让', company_area=u'40609',company_house_owner=u'国有',opt_scope=u'精煤',opt_field=u'洗精煤',prod_equip=u'跳汏式洗煤机' )
        party_role = PartyRole(party=company,branch_code=branch.branch_code)
        self.session.add(party_role)

        customer = Customer(party=company, cust_type="company")
        self.session.add(customer)
        self.session.commit()

        d = datetime.datetime.now()
        operating_log = CustomerInfoOptLog(upto_date=d, log_date=d, register_user=user, comment="eeeeee")

        addr = Address(party= [customer.party], address=u"上海市长宁区")
        email = Email(party = [customer.party], email_address=u"yinsho@yinsho.com")
        phone = Phone(party = [customer.party], phone_type="手机", phone_number = "1888888888")
        phone2 = Phone(party = [customer.party], phone_type="手机1", phone_number = "109999999999")

        customer.party.ethnicity = u"汉族"
        man3=Resident(no='100059277',name=u'李会齐', ric=u'150302196202212028', current_name=u'李会齐',gender=u'女性', birthday=datetime.datetime.strptime('1962-02-21','%Y-%m-%d'), ethnicity =u'汉族', politics_status=u'群众')
        customer = Customer(party=man3, cust_type="person")
        Certificate(party=man3, cert_type=u'身份证', cert_no='150302196202212028', issue_date=datetime.datetime.now(), issue_office=u'xxx', thru_date = datetime.date(2055, 1, 1))

        customer.party.to_party.append(man3)

        ar = AcademicRecord(customer=customer, register_log=operating_log, update_log=operating_log)
        er = EmploymentRecord(customer=customer)
        cm = CustomerMemo(customer=customer, register_log=operating_log, update_log=operating_log)
        cr = CustomerRealty(customer=customer, register_log=operating_log, update_log=operating_log)
        cb = CustomerBond(customer=customer, register_log=operating_log, update_log=operating_log)
        ct = CustomerStock(customer=customer, register_log=operating_log, update_log=operating_log)
        cia = CustomerIntangibleAsset(customer=customer, register_log=operating_log, update_log=operating_log)
        cv = CustomerVehicle(customer=customer, register_log=operating_log, update_log=operating_log)
        csi = CustomerSocialInsurance(customer=customer, register_log=operating_log, update_log=operating_log)
        cci = CustomerCommerialInsurance(customer=customer, register_log=operating_log, update_log=operating_log)
        cie = CustomerInvestmentEnterprise(customer=customer, register_log=operating_log, update_log=operating_log)
        coa = CustomerOtherAsset(customer=customer, register_log=operating_log, update_log=operating_log)
        col = CustomerOtherLiabilities(customer=customer, register_log=operating_log, update_log=operating_log)

        self.session.add_all([man3, addr, email, phone, phone2, ar, er, cm, cr, cb, ct, cia, cv, csi, cci , cie , coa , col])
        self.session.commit()




    def init_branch(self):
        """
        Branch
        """
        log.debug("start init branch!")
        c = Company(company_cn_name=u"xxx银行xxx分行")
        b = Branch(party=c, branch_code='1000', branch_name=u"xxx分行")
        ub = UserBranch(user=self.user, branch=b)
        addr = Address(party=[c], province=u"浙江省", city=u"杭州市", address=u"留和路188号")
        self.session.add_all([c, b, ub])

    def init_util(self):
        """
        Util
        """
        log.debug("start init util!")
        cny = Currency( currency_code='CNY', currency_name=u'人民币', currency_symbols='cny')
        self.session.add(cny)
        self.session.commit()

    def init_guarantee_method(self):
        """
            担保类型
        """
        log.debug("start init guarantee_method!")
        gm01=GuaranteeMethod(name='质押',detail='个人定期存单',detail_page='pawn_per_stub_a')
        gm02=GuaranteeMethod(name='质押',detail='单位定期存单',detail_page='pawn_stub_a')
        gm03=GuaranteeMethod(name='质押',detail='本行理财产品',detail_page='pawn_finance_a')
        gm04=GuaranteeMethod(name='质押',detail='账户资金',detail_page='pawn_saving_a')
        gm05=GuaranteeMethod(name='质押',detail='银行承兑汇票',detail_page='pawn_accp_a')
        gm06=GuaranteeMethod(name='质押',detail='应收账款',detail_page='pawn_acc_rec_a')
        gm07=GuaranteeMethod(name='质押',detail='其他',detail_page='pawn_other_a')

        gm08=GuaranteeMethod(name='抵押',detail='房屋所有权',detail_page='mrge_building_a')
        gm09=GuaranteeMethod(name='抵押',detail='土地使用权',detail_page='mrge_land_a')
        gm10=GuaranteeMethod(name='抵押',detail='设备',detail_page='mrge_eqp_a')
        gm11=GuaranteeMethod(name='抵押',detail='动产',detail_page='mrge_movable_a')
        gm12=GuaranteeMethod(name='抵押',detail='设备+动产',detail_page='mrge_eqp_movable_a')
        gm13=GuaranteeMethod(name='抵押',detail='交通工具',detail_page='mrge_vch_a')
        gm14=GuaranteeMethod(name='抵押',detail='其他',detail_page='mrge_other_a')

        self.session.add_all([gm01,gm02,gm03,gm04,gm05,gm06,gm07,gm08,gm09,gm10,gm11,gm12,gm13,gm14])

    def init_product(self):
        """
        Product
        """
        log.debug("start init product!")
        pt01 = ProductType(code='01', name='个人按揭贷款贷款', business_type='个人业务')
        pt02 = ProductType(code='02', name='个人消费贷款', business_type='个人业务')
        pt03 = ProductType(code='03', name='个人下岗贷款', business_type='个人业务')
        pt04 = ProductType(code='04', name='个人经营性贷款', business_type='个人业务')

        pt11 = ProductType(code='11', name='企业流动资金贷款', business_type='对公业务')
        pt12 = ProductType(code='12', name='企业票据融资', business_type='对公业务')

        pt13 = ProductType(code='13', name='银团贷款', business_type='对公业务')
        pt14 = ProductType(code='14', name='房地产开发贷款', business_type='对公业务')

        pt19 = ProductType(code='19', name='贴现业务', business_type='贴现业务')
        pt20 = ProductType(code='20', name='承兑汇票', business_type='承兑汇票')
        pt41 = ProductType(code='41', name='委托贷款', business_type='对公业务')
        pt42 = ProductType(code='42', name='委托贷款', business_type='个人业务')

        pt51 = ProductType(code='51', name='展期及授信额度调整', business_type='展期及授信额度业务')
        pt91 = ProductType(code='91', name='同业业务', business_type='同业')
        pt92 = ProductType(code='92', name='投资业务', business_type='投资')
        pt95 = ProductType(code='95', name='授信业务', business_type='授信')
        pt96 = ProductType(code='96', name='五级分类', business_type='五级分类')
        pt97 = ProductType(code='97', name='以物抵债', business_type='以物抵债')
        pt99 = ProductType(code='99', name='其他', business_type='其他')

        self.session.add_all([pt01, pt02, pt03, pt04, pt11, pt12, pt13,pt14,pt19,pt20,pt41,pt42, pt51])

        self.session.add_all([

            Product(main_gua_type="质押", product_code="001", product_type=pt99, name="小企业动产抵押贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="质押", product_code="002", product_type=pt99, name="小企业资产抵押贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="质押", product_code="007", product_type=pt20, name="签发银行承兑汇票",product_page='acceptance_baseInformation'),
            Product(main_gua_type="质押", product_code="008", product_type=pt11, name="银行承兑汇票质押",product_page='loanBaseInfo'),
            Product(main_gua_type="质押", product_code="010", product_type=pt99, name="010贴现",product_page='loanBaseInfo'),
            Product(product_code="023", product_type=pt19, name="承兑汇票贴现",product_page='discount'),
            Product(product_code="027", product_type=pt99, name="企业资产抵押及其他保证贷款",product_page='discount'),
            Product(product_code="040", product_type=pt99, name="对公授信额度调整",product_page='discount'),
            Product(product_code="050", product_type=pt99, name="对公贷款展期",product_page='discount'),
            Product(product_code="080", product_type=pt99, name="小企业担保公司贷款（二）",product_page='discount'),
            Product(product_code="081", product_type=pt99, name="账户资金质押贷款",product_page='discount'),
            Product(product_code="082", product_type=pt99, name="本行存单质押贷款（二）",product_page='discount'),
            Product(main_gua_type="抵押", product_code="101", product_type=pt01, name="个人住房按揭贷款",product_page='housing_mortgage_loans'),
            Product(main_gua_type="抵押", product_code="102", product_type=pt01, name="个人第二套住房按揭",product_page='real_estate_development'),
            Product(main_gua_type="抵押", product_code="107", product_type=pt99, name="其他商用房抵押贷款",product_page='commercial_housing_mortgage_loans'),
            Product(main_gua_type="抵押", product_code="103", product_type=pt01, name="商用房按揭贷款",product_page='commercial_housing_mortgage_loans'),
            Product(main_gua_type="抵押", product_code="104", product_type=pt99, name="商用房按揭贷款",product_page='commercial_housing_mortgage_loans'),
            Product(main_gua_type="抵押", product_code="105", product_type=pt99, name="个人住房抵押贷款",product_page='commercial_housing_mortgage_loans'),
            Product(main_gua_type="抵押", product_code="106", product_type=pt99, name="商用门脸店抵押贷款",product_page='commercial_housing_mortgage_loans'),
            Product(main_gua_type="抵押", product_code="108", product_type=pt99, name="本行存单质押贷款",product_page='commercial_housing_mortgage_loans'),
            Product(main_gua_type="抵押", product_code="109", product_type=pt99, name="他行存单质押贷款",product_page='commercial_housing_mortgage_loans'),
            Product(main_gua_type="质押", product_code="110", product_type=pt99, name="其他有价单证质押贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="544", product_type=pt01, name="商用房按揭贷款（一次还本）",product_page='commercial_housing_mortgage_loans'),
            Product(main_gua_type="抵押", product_code="111", product_type=pt99, name="商用门脸店按揭贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="140", product_type=pt99, name="对私授信额度调整",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="150", product_type=pt99, name="对私贷款展期",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="151", product_type=pt99, name="商用门脸抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="152", product_type=pt99, name="商用门脸抵押45%",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="153", product_type=pt99, name="商用门脸抵押50%",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="154", product_type=pt99, name="卡授信商用门脸抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="155", product_type=pt99, name="卡授信商用门脸抵押45%",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="156", product_type=pt99, name="卡授信商用门脸抵押50%",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="157", product_type=pt99, name="住宅楼抵押55%",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="158", product_type=pt99, name="住宅楼抵押60%",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="159", product_type=pt99, name="住宅楼抵押65%",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="160", product_type=pt99, name="住宅楼抵押70%",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="165", product_type=pt99, name="卡授信住宅楼抵押70%",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="167", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="168", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="169", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="170", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="171", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="172", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="173", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="175", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="176", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="177", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="178", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="179", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="180", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="181", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="182", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="183", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="184", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="185", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="186", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="187", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="188", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="195", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="197", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="199", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="207", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="208", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="209", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="210", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="211", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="212", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="213", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="214", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="215", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="216", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="217", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="218", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="219", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="221", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="220", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="224", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),

            Product(main_gua_type="抵押", product_code="321", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="320", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="322", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="334", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="335", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="336", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="340", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="337", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="344", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="352", product_type=pt99, name="异地商房抵押60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="355", product_type=pt99, name="异地商房抵押60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="356", product_type=pt99, name="异地商房抵押60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="357", product_type=pt99, name="异地商房抵押60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="358", product_type=pt99, name="异地商房抵押60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="359", product_type=pt99, name="异地商房抵押60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="360", product_type=pt99, name="异地商房抵押60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="362", product_type=pt99, name="异地商房抵押60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="365", product_type=pt99, name="异地商房抵押60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="366", product_type=pt99, name="异地商房抵押60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="367", product_type=pt99, name="异地商房抵押60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="368", product_type=pt99, name="异地商房抵押60",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="374", product_type=pt99, name="企业信用既保证",product_page='loanBaseInfo'),
            Product(main_gua_type="质押", product_code="375", product_type=pt04, name="本行理财产品质押经营性",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="377", product_type=pt02, name="惠民贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="378", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="379", product_type=pt99, name="保证担保贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="质押", product_code="500", product_type=pt02, name="本行存单账户资金质押消费性",product_page='loanBaseInfo'),
            Product(main_gua_type="质押", product_code="502", product_type=pt02, name="本行理财产品质押消费性",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="503", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="511", product_type=pt04, name="买入贷款抵押担保",product_page='loanBaseInfo'),
            Product(main_gua_type="质押", product_code="513", product_type=pt02, name="其他有价单证质押消费性贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="515", product_type=pt04, name="买入贷款保证担保",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="516", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="517", product_type=pt11, name="一般担保保证贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="518", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="519", product_type=pt04, name="个人保证贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="520", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="521", product_type=pt11, name="企业保证贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="522", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="523", product_type=pt02, name="商住房抵押及保证消费性50",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="524", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="529", product_type=pt02, name="商住房抵押及保证消费性65",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="530", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="533", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="540", product_type=pt04, name="预抵押40-50以内",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="541", product_type=pt04, name="预抵押40以内",product_page='loanBaseInfo'),
            Product(main_gua_type="质押", product_code="542", product_type=pt04, name="其他有价单证质押经营性贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="543", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="376", product_type=pt02, name="保费贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="123", product_type=pt02, name="个人助学贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="122", product_type=pt99, name="汽车个人消费贷款",product_page='car_consume'),
            Product(main_gua_type="保证", product_code="118", product_type=pt99, name="装饰装修个人消费贷款",product_page='personal_housing_decoration'),
            Product(main_gua_type="保证", product_code="535", product_type=pt99, name="装饰装修个人消费贷款",product_page='personal_housing_decoration'),
            Product(main_gua_type="保证", product_code="373", product_type=pt99, name="装饰装修个人消费贷款",product_page='personal_housing_decoration'),
            Product(main_gua_type="保证", product_code="229", product_type=pt99, name="装饰装修个人消费贷款",product_page='personal_housing_decoration'),
            Product(main_gua_type="保证", product_code="120", product_type=pt99, name="装饰装修个人消费贷款",product_page='personal_housing_decoration'),
            Product(main_gua_type="保证", product_code="124", product_type=pt99, name="装饰装修个人消费贷款",product_page='personal_housing_decoration'),
            Product(main_gua_type="保证", product_code="119", product_type=pt99, name="旅游个人消费贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="121", product_type=pt99, name="耐用品个人消费贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="225", product_type=pt99, name="狮卡授信消费贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="226", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="227", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="#", product_code="228", product_type=pt99, name="其他商用房抵押40%以下",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="525", product_type=pt02, name="商住房抵押及保证消费性55",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="527", product_type=pt02, name="商住房抵押及保证消费性60",product_page='loanBaseInfo'),

            Product(main_gua_type="保证", product_code="113", product_type=pt03, name="个人下岗再就业贷款",product_page='personal_again_work_loan'),
            Product(main_gua_type="保证", product_code="114", product_type=pt03, name="个人下岗二次就业贷款",product_page='secondary_employment'),
            Product(main_gua_type="保证", product_code="531", product_type=pt03, name="小额下岗二次贷款",product_page='loanBaseInfo'),

            Product(main_gua_type="保证", product_code="324", product_type=pt04, name="个人信用及保证贷款保证担保",product_page='loanBaseInfo'),
            Product(main_gua_type="信用", product_code="506", product_type=pt04, name="个人信用及保证贷款信用担保",product_page='loanBaseInfo'),
            Product(main_gua_type="质押", product_code="348", product_type=pt04, name="本行存单账户资金质押经营性",product_page='loanBaseInfo'),
            #Product(main_gua_type="质押", product_code="354", product_type=pt04, name="卡授信其他有价单证质押",product_page='loanBaseInfo'),
            #Product(main_gua_type="质押", product_code="353", product_type=pt04, name="卡授信账户资金质押",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="509", product_type=pt04, name="经营性物业租金贷款保证担保",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="510", product_type=pt04, name="经营性物业租金贷款抵押担保",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="117", product_type=pt04, name="担保公司担保",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="330", product_type=pt04, name="商住房抵押及保证经营性50",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="331", product_type=pt04, name="商住房抵押及保证经营性55",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="332", product_type=pt04, name="商住房抵押及保证经营性60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="333", product_type=pt04, name="商住房抵押及保证经营性65",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="341", product_type=pt04, name="异地商用房抵押贷款50",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="342", product_type=pt04, name="异地商用房抵押贷款55",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="343", product_type=pt04, name="异地商用房抵押贷款60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="536", product_type=pt04, name="异地商用房抵押贷款65",product_page='loanBaseInfo'),

            Product(main_gua_type="质押", product_code="348_1", product_type=pt11, name="本行存单账户资金质押经营性",product_page='loanBaseInfo'),
            Product(main_gua_type="质押", product_code="375_1", product_type=pt11, name="本行理财产品质押经营性",product_page='loanBaseInfo'),
            #Product(main_gua_type="质押", product_code="110_1", product_type=pt11, name="其他有价单证质押贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="质押", product_code="542_1", product_type=pt11, name="其他有价单证质押经营性贷款",product_page='loanBaseInfo'),
            #Product(main_gua_type="质押", product_code="354_1", product_type=pt11, name="卡授信其他有价单证质押",product_page='loanBaseInfo'),
            #Product(main_gua_type="质押", product_code="353_1", product_type=pt11, name="卡授信账户资金质押",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="509_1", product_type=pt11, name="经营性物业租金贷款保证担保",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="510_1", product_type=pt11, name="经营性物业租金贷款抵押担保",product_page='loanBaseInfo'),
            #Product(main_gua_type="保证", product_code="379_1", product_type=pt11, name="保证担保贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="117_1", product_type=pt11, name="担保公司担保",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="330_1", product_type=pt11, name="商住房抵押及保证经营性50",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="331_1", product_type=pt11, name="商住房抵押及保证经营性55",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="332_1", product_type=pt11, name="商住房抵押及保证经营性60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="333_1", product_type=pt11, name="商住房抵押及保证经营性65",product_page='loanBaseInfo'),
            #Product(main_gua_type="抵押", product_code="369_1", product_type=pt11, name="异地商房抵押55",product_page='loanBaseInfo'),
            #Product(main_gua_type="抵押", product_code="370_1", product_type=pt11, name="异地商房抵押65",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="341_1", product_type=pt11, name="异地商用房抵押贷款50",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="342_1", product_type=pt11, name="异地商用房抵押贷款55",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="343_1", product_type=pt11, name="异地商用房抵押贷款60",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="536_1", product_type=pt11, name="异地商用房抵押贷款65",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="540_1", product_type=pt11, name="预抵押40-50以内",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="541_1", product_type=pt11, name="预抵押40以内",product_page='loanBaseInfo'),
            Product(main_gua_type="质押", product_code="312", product_type=pt11, name="应收账款质押",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="125", product_type=pt11, name="小企业个人保证贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="372", product_type=pt11, name="小企业联保贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="532", product_type=pt11, name="一般抵押贷款",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="319", product_type=pt11, name="企业动产质押(50)",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="318", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="317", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="316", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),

            Product(main_gua_type="抵押", product_code="231", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="230", product_type=pt99, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            #Product(main_gua_type="抵押", product_code="189", product_type=pt11, name="卡授信厂房设备抵押10%",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="349", product_type=pt11, name="资产抵押30/50及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="350", product_type=pt11, name="资产抵押35/55及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="351", product_type=pt11, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="345", product_type=pt11, name="异地资产抵押贷款35",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="538", product_type=pt11, name="异地资产抵押贷款40",product_page='loanBaseInfo'),
            #Product(main_gua_type="抵押", product_code="371", product_type=pt11, name="异地机器设备抵押30",product_page='loanBaseInfo'),
            Product(main_gua_type="保证", product_code="515_1", product_type=pt11, name="买入贷款保证担保",product_page='loanBaseInfo'),
            Product(main_gua_type="抵押", product_code="511_1", product_type=pt11, name="买入贷款抵押担保",product_page='loanBaseInfo'),

            Product(product_code="714", product_type=pt41, name="对公委托贷款",product_page='entrusted_loans'),
            #Product(product_code="720", product_type=pt41, name="个人委托贷款",product_page='individual_entrust_loans'),

            #Product(main_gua_type="#", product_code="301", product_type=pt51, name="授信额度申请",product_page='loanBaseInfo'),
            #Product(main_gua_type="#", product_code="302", product_type=pt51, name="追加授信额度申请",product_page='loanBaseInfo'),

            Product(product_code="703", product_type=pt13, name="银团贷款",product_page='loanBaseInfo'),
            Product(product_code="704", product_type=pt14, name="房地产开发贷款",product_page='real_estate_development'),
            Product(product_code="705", product_type=pt92, name="投资",product_page='loanBaseInfo'),

            Product(product_code="801", product_type=pt91, name="同业存放",product_page='tradeapproval'),
            Product(product_code="802", product_type=pt91, name="存放同业",product_page='tradeapproval'),
            Product(product_code="803", product_type=pt91, name="同业拆入",product_page='sameIn'),
            Product(product_code="804", product_type=pt91, name="拆放同业",product_page='sameOut'),

            Product(product_code="805", product_type=pt91, name="债券正回购",product_page='creditleding'),
            Product(product_code="806", product_type=pt91, name="债券逆回购",product_page='nocreditleding'),
            Product(product_code="807", product_type=pt91, name="同业存单发行",product_page='loanBaseInfo'),
            Product(product_code="808", product_type=pt91, name="买断式转贴现买入",product_page='turnDiscount'),
            Product(product_code="809", product_type=pt91, name="买断式转贴现卖出",product_page='turnDiscount'),
            Product(product_code="811", product_type=pt91, name="回购式转贴现买入",product_page='turnDiscount'),
            Product(product_code="812", product_type=pt91, name="回购式转贴现卖出",product_page='turnDiscount'),
            Product(product_code="813", product_type=pt91, name="协议存款",product_page='tradeapproval'),
            Product(product_code="814", product_type=pt91, name="非银存款",product_page='tradeapproval'),

            #Product(product_code="901", product_type=pt92, name="投资",product_page='loanBaseInfo'),
            Product(product_code="951", product_type=pt95, name="统一授信",product_page='loanBaseInfo'),
            Product(product_code="961", product_type=pt96, name="五级分类",product_page='loanBaseInfo'),
            Product(product_code="971", product_type=pt97, name="以物抵债",product_page='loanBaseInfo'),
            Product(product_code="972", product_type=pt97, name="展期",product_page='loanBaseInfo'),
            Product(product_code="973", product_type=pt97, name="授信卡金额调整",product_page='loanBaseInfo'),
            Product(product_code="974", product_type=pt97, name="贷款核销",product_page='loanBaseInfo'),
            #Product(product_code="810", product_type=pt91, name="回购式转贴现买入",product_page='loanBaseInfo'),
            #Product(product_code="811", product_type=pt91, name="回购式转贴现卖出",product_page='loanBaseInfo'),

          #  Product(product_code="704", product_type=pt11, name="出口押汇",product_page='bill_purchased'),
          #  Product(product_code="705", product_type=pt11, name="打包贷款",product_page='packaged_loans'),
          #  Product(product_code="730", product_type=pt11, name="贷款承诺",product_page='loan_commitment'),
          #  Product(product_code="706", product_type=pt11, name="国内保函",product_page='domestic_detterguarantee'),
          #  Product(product_code="707", product_type=pt11, name="进口代收押汇",product_page='import__collecting_documentary'),
          #  Product(product_code="708", product_type=pt11, name="进口押汇表",product_page='import_trade'),
          #  Product(product_code="709", product_type=pt11, name="开立信用证",product_page='open_ic'),
          #  Product(product_code="710", product_type=pt13, name="流动资金贷款",product_page='liquidity'),
          #  Product(product_code="711", product_type=pt11, name="买入票据（福费庭）",product_page='bill_purchased'),
          #  Product(product_code="715", product_type=pt11, name="项目贷款表",product_page='project_loan'),
          #  Product(product_code="716", product_type=pt11, name="最高额贷款",product_page='maximum_loan'),
          #  Product(product_code="717", product_type=pt04, name="个人经营性贷款",product_page='personal_busines_loans'),
          #  Product(product_code="718", product_type=pt04, name="个人其他消费贷款",product_page='other_individual_consumption'),
          #  Product(product_code="719", product_type=pt04, name="个人透支额度",product_page='personal_overdraft'),
          #  Product(product_code="721", product_type=pt04, name="个人住房消费贷款",product_page='house_consume'),
          #  Product(product_code="722", product_type=pt04, name="公积金按揭贷款",product_page='accumulation_mortgage_loans'),
          #  Product(product_code="723", product_type=pt04, name="国家助学贷款",product_page='national_student_loan'),
          #  Product(product_code="724", product_type=pt04, name="商业助学贷款",product_page='commercials_tudent_loans'),
          #  Product(product_code="725", product_type=pt04, name="一手房按揭贷款",product_page='housing_mortgage_loans'),
          #  Product(product_code="726", product_type=pt11, name="国际保函",product_page='international_letter_guarantee'),
          #  Product(product_code="728", product_type=pt11, name="提货担保",product_page='delivery_guarantee'),
        ])
        self.session.commit()

    def init_report_data(self):
        rt1 = ReportType(name="2003版资产负债表",cotes=2)
        rt2 = ReportType(name="2003版损益表",cotes=1)
        rt3 = ReportType(name="2003版现金流量",cotes=1)
        rt4 = ReportType(name="财务指标",cotes=1)
        rt5 = ReportType(name="2007版资产负债",cotes=2)
        rt6 = ReportType(name="2007版损益",cotes=1)
        rt7 = ReportType(name="2007版现金流量",cotes=1)
        rt8 = ReportType(name="事业单位资产负债",cotes=2)
        rt9 = ReportType(name="事业单位现金流量",cotes=1)

        self.session.add_all([rt1,rt2,rt3,rt4,rt5,rt6,rt7,rt8,rt9])

        r1 = Report(report_name="资产负债表",report_type=rt1)
        r2 = Report(report_name="损益表",report_type=rt2)
        r3 = Report(report_name="现金流量表",report_type=rt3)
        r4 = Report(report_name="财务指标值表",report_type=rt4)
        r5 = Report(report_name="财务指标值表",report_type=rt4)
        r6 = Report(report_name="资产负债表（新）",report_type=rt5)
        r7 = Report(report_name="损益表（新）",report_type=rt6)
        r8 = Report(report_name="现金流量表（新）",report_type=rt7)
        r9 = Report(report_name="资产负债表（事业单位）",report_type=rt8)
        r10 = Report(report_name="收入支出表（事业单位）",report_type=rt9)

        self.session.add_all([r1,r2,r3,r4,r5,r6,r7,r8,r9,r10])



        """
            SELECT     'ReportItems(item_id='||substr(item_id,3)||', item_name=u"'|| item_name ||'", report_type='||
            case
            when r.rpt_type='01' then 'r1'
            when r.rpt_type='02' then 'r2'
            when r.rpt_type='03' then 'r3'
            when r.rpt_type='04' then 'r4'
            when r.rpt_type='04' then 'r5'
            when r.rpt_type='07' then 'r6'
            when r.rpt_type='08' then 'r7'
            when r.rpt_type='09' then 'r8'
            when r.rpt_type='10' then 'r9'
            when r.rpt_type='11' then 'r10'
            end
            ||') ,'
            ,r.* from rpt_items r order by rpt_type, item_id;

        """

        self.session.add_all([
            ReportItems(item_id=1000000, item_name=u"资产", report=r1) ,
            ReportItems(item_id=1000001, item_name=u"资产总计", report=r1) ,
            ReportItems(item_id=1010000, item_name=u"流动资产", report=r1) ,
            ReportItems(item_id=1010001, item_name=u"流动资产合计", report=r1) ,
            ReportItems(item_id=1010100, item_name=u"货币资金", report=r1) ,
            ReportItems(item_id=1010200, item_name=u"短期投资净额", report=r1) ,
            ReportItems(item_id=1010210, item_name=u"短期投资", report=r1) ,
            ReportItems(item_id=1010220, item_name=u"资产跌价准备", report=r1) ,
            ReportItems(item_id=1010300, item_name=u"应收票据", report=r1) ,
            ReportItems(item_id=1010400, item_name=u"应收股利", report=r1) ,
            ReportItems(item_id=1010500, item_name=u"应收利息", report=r1) ,
            ReportItems(item_id=1010600, item_name=u"应收账款净额", report=r1) ,
            ReportItems(item_id=1010610, item_name=u"应收账款", report=r1) ,
            ReportItems(item_id=1010620, item_name=u"坏帐准备", report=r1) ,
            ReportItems(item_id=1010700, item_name=u"预付账款", report=r1) ,
            ReportItems(item_id=1010800, item_name=u"期货保证金", report=r1) ,
            ReportItems(item_id=1010900, item_name=u"应收补贴款", report=r1) ,
            ReportItems(item_id=1011000, item_name=u"应收出口退税", report=r1) ,
            ReportItems(item_id=1011100, item_name=u"其他应收款", report=r1) ,
            ReportItems(item_id=1011200, item_name=u"存货净值", report=r1) ,
            ReportItems(item_id=1011210, item_name=u"存货", report=r1) ,
            ReportItems(item_id=1011211, item_name=u"存货原材料", report=r1) ,
            ReportItems(item_id=1011212, item_name=u"存货产成品", report=r1) ,
            ReportItems(item_id=1011220, item_name=u"存货跌价准备", report=r1) ,
            ReportItems(item_id=1011300, item_name=u"待摊费用", report=r1) ,
            ReportItems(item_id=1011400, item_name=u"待处理流动资产净损失", report=r1) ,
            ReportItems(item_id=1011500, item_name=u"一年期长期债券投资", report=r1) ,
            ReportItems(item_id=1011600, item_name=u"其他流动资产", report=r1) ,
            ReportItems(item_id=1020000, item_name=u"长期投资", report=r1) ,
            ReportItems(item_id=1020001, item_name=u"长期投资合计", report=r1) ,
            ReportItems(item_id=1020100, item_name=u"长期投资", report=r1) ,
            ReportItems(item_id=1020110, item_name=u"长期股权投资", report=r1) ,
            ReportItems(item_id=1020120, item_name=u"长期债券投资", report=r1) ,
            ReportItems(item_id=1020200, item_name=u"合并价差", report=r1) ,
            ReportItems(item_id=1030000, item_name=u"固定资产", report=r1) ,
            ReportItems(item_id=1030001, item_name=u"固定资产合计", report=r1) ,
            ReportItems(item_id=1030100, item_name=u"固定资产净额", report=r1) ,
            ReportItems(item_id=1030110, item_name=u"固定资产净值", report=r1) ,
            ReportItems(item_id=1030111, item_name=u"固定资产原价", report=r1) ,
            ReportItems(item_id=1030112, item_name=u"累计折旧", report=r1) ,
            ReportItems(item_id=1030120, item_name=u"固定资产值减值准备", report=r1) ,
            ReportItems(item_id=1030200, item_name=u"工程物资", report=r1) ,
            ReportItems(item_id=1030300, item_name=u"在建工程", report=r1) ,
            ReportItems(item_id=1030400, item_name=u"固定资产清理", report=r1) ,
            ReportItems(item_id=1030500, item_name=u"待处理固定资产净损失", report=r1) ,
            ReportItems(item_id=1040000, item_name=u"无形资产及其他资产", report=r1) ,
            ReportItems(item_id=1040001, item_name=u"无形及其他资产合计", report=r1) ,
            ReportItems(item_id=1040100, item_name=u"无形资产", report=r1) ,
            ReportItems(item_id=1040110, item_name=u"无形资产土地使用权", report=r1) ,
            ReportItems(item_id=1040200, item_name=u"递延资产", report=r1) ,
            ReportItems(item_id=1040210, item_name=u"递延资产固定资产修理", report=r1) ,
            ReportItems(item_id=1040220, item_name=u"递延资产固定资产改良支出", report=r1) ,
            ReportItems(item_id=1040300, item_name=u"其他长期资产", report=r1) ,
            ReportItems(item_id=1040310, item_name=u"其他长期资产特准储备物资", report=r1) ,
            ReportItems(item_id=1050000, item_name=u"递延税项", report=r1) ,
            ReportItems(item_id=1050001, item_name=u"递延税项借项", report=r1) ,
            ReportItems(item_id=2000000, item_name=u"负债及所有者权益", report=r1) ,
            ReportItems(item_id=2000001, item_name=u"负债合计", report=r1) ,
            ReportItems(item_id=2010000, item_name=u"流动负债", report=r1) ,
            ReportItems(item_id=2010001, item_name=u"流动负债合计", report=r1) ,
            ReportItems(item_id=2010100, item_name=u"短期借款", report=r1) ,
            ReportItems(item_id=2010200, item_name=u"应付票据", report=r1) ,
            ReportItems(item_id=2010300, item_name=u"应付账款", report=r1) ,
            ReportItems(item_id=2010400, item_name=u"预收账款", report=r1) ,
            ReportItems(item_id=2010500, item_name=u"应付工资", report=r1) ,
            ReportItems(item_id=2010600, item_name=u"应付福利费", report=r1) ,
            ReportItems(item_id=2010700, item_name=u"应付股利", report=r1) ,
            ReportItems(item_id=2010800, item_name=u"应交税金", report=r1) ,
            ReportItems(item_id=2010900, item_name=u"其他应交款", report=r1) ,
            ReportItems(item_id=2011000, item_name=u"其他应付款", report=r1) ,
            ReportItems(item_id=2011100, item_name=u"预提费用", report=r1) ,
            ReportItems(item_id=2011200, item_name=u"预计负债", report=r1) ,
            ReportItems(item_id=2011300, item_name=u"一年内到期的长期负债", report=r1) ,
            ReportItems(item_id=2011400, item_name=u"其他流动负债", report=r1) ,
            ReportItems(item_id=2020000, item_name=u"长期负债", report=r1) ,
            ReportItems(item_id=2020001, item_name=u"长期负债合计", report=r1) ,
            ReportItems(item_id=2020100, item_name=u"长期借款", report=r1) ,
            ReportItems(item_id=2020200, item_name=u"应付债券", report=r1) ,
            ReportItems(item_id=2020300, item_name=u"长期应付款", report=r1) ,
            ReportItems(item_id=2020400, item_name=u"专项应付款", report=r1) ,
            ReportItems(item_id=2020500, item_name=u"其他长期负债", report=r1) ,
            ReportItems(item_id=2020520, item_name=u"特准储备基金", report=r1) ,
            ReportItems(item_id=2030000, item_name=u"递延税项", report=r1) ,
            ReportItems(item_id=2030100, item_name=u"递延税项贷项", report=r1) ,
            ReportItems(item_id=3000000, item_name=u"少数股东权益", report=r1) ,
            ReportItems(item_id=3000001, item_name=u"少数股东权益", report=r1) ,
            ReportItems(item_id=4000000, item_name=u"所有者权益", report=r1) ,
            ReportItems(item_id=4000001, item_name=u"所有者权益合计", report=r1) ,
            ReportItems(item_id=4010000, item_name=u"实收资本", report=r1) ,
            ReportItems(item_id=4010100, item_name=u"国家资本", report=r1) ,
            ReportItems(item_id=4010200, item_name=u"集体资本", report=r1) ,
            ReportItems(item_id=4010300, item_name=u"法人资本", report=r1) ,
            ReportItems(item_id=4010310, item_name=u"国有法人资本", report=r1) ,
            ReportItems(item_id=4010320, item_name=u"集体法人资本", report=r1) ,
            ReportItems(item_id=4010400, item_name=u"个人资本", report=r1) ,
            ReportItems(item_id=4010500, item_name=u"外商资本", report=r1) ,
            ReportItems(item_id=4020000, item_name=u"资本公积", report=r1) ,
            ReportItems(item_id=4030000, item_name=u"盈余公积", report=r1) ,
            ReportItems(item_id=4030100, item_name=u"法定盈余公积", report=r1) ,
            ReportItems(item_id=4030200, item_name=u"公益金", report=r1) ,
            ReportItems(item_id=4030300, item_name=u"补充流动资本", report=r1) ,
            ReportItems(item_id=4040000, item_name=u"未确认的投资损失", report=r1) ,
            ReportItems(item_id=4050000, item_name=u"未分配利润", report=r1) ,
            ReportItems(item_id=4060000, item_name=u"外币报表折算差额", report=r1) ,
            ReportItems(item_id=5000000, item_name=u"负债和所有者权益总计", report=r1) ,
            ReportItems(item_id=6000100, item_name=u"未结清对外担保余额", report=r1) ,
            ReportItems(item_id=1000000, item_name=u"主营业务收入", report=r2) ,
            ReportItems(item_id=1010100, item_name=u"出口产品销售收入", report=r2) ,
            ReportItems(item_id=1010200, item_name=u"进口产品销售收入", report=r2) ,
            ReportItems(item_id=1020000, item_name=u"折扣与折让", report=r2) ,
            ReportItems(item_id=2010000, item_name=u"主营业务收入净额", report=r2) ,
            ReportItems(item_id=2020000, item_name=u"主营业务成本", report=r2) ,
            ReportItems(item_id=2020100, item_name=u"出口产品销售成本", report=r2) ,
            ReportItems(item_id=2030000, item_name=u"主营业务税金及附加", report=r2) ,
            ReportItems(item_id=2040000, item_name=u"经营费用", report=r2) ,
            ReportItems(item_id=2050000, item_name=u"其他费用", report=r2) ,
            ReportItems(item_id=2060000, item_name=u"递延收益", report=r2) ,
            ReportItems(item_id=2070000, item_name=u"代购代销收入", report=r2) ,
            ReportItems(item_id=2080000, item_name=u"其他收入", report=r2) ,
            ReportItems(item_id=3010000, item_name=u"主营业务利润", report=r2) ,
            ReportItems(item_id=3020000, item_name=u"其他业务利润", report=r2) ,
            ReportItems(item_id=3030000, item_name=u"营业费用", report=r2) ,
            ReportItems(item_id=3040000, item_name=u"管理费用", report=r2) ,
            ReportItems(item_id=3050000, item_name=u"财务费用", report=r2) ,
            ReportItems(item_id=3060000, item_name=u"其他费用", report=r2) ,
            ReportItems(item_id=4010000, item_name=u"营业利润", report=r2) ,
            ReportItems(item_id=4020000, item_name=u"投资收益", report=r2) ,
            ReportItems(item_id=4030000, item_name=u"期货收益", report=r2) ,
            ReportItems(item_id=4040000, item_name=u"补贴收入", report=r2) ,
            ReportItems(item_id=4040100, item_name=u"补贴前亏损的企业补贴收入", report=r2) ,
            ReportItems(item_id=4050000, item_name=u"营业外收入", report=r2) ,
            ReportItems(item_id=4050100, item_name=u"处置固定资产净收益", report=r2) ,
            ReportItems(item_id=4050200, item_name=u"非货币性交易收益", report=r2) ,
            ReportItems(item_id=4050300, item_name=u"出售无形资产收益", report=r2) ,
            ReportItems(item_id=4050400, item_name=u"罚款净收入", report=r2) ,
            ReportItems(item_id=4060000, item_name=u"其他收入", report=r2) ,
            ReportItems(item_id=4060100, item_name=u"用以前年度含量工资节余弥补利润", report=r2) ,
            ReportItems(item_id=4070000, item_name=u"营业外支出", report=r2) ,
            ReportItems(item_id=4070100, item_name=u"处置固定资产净损失", report=r2) ,
            ReportItems(item_id=4070200, item_name=u"债务重组损失", report=r2) ,
            ReportItems(item_id=4070300, item_name=u"罚款支出", report=r2) ,
            ReportItems(item_id=4070400, item_name=u"捐赠支出", report=r2) ,
            ReportItems(item_id=4080000, item_name=u"其他支出", report=r2) ,
            ReportItems(item_id=4080100, item_name=u"结转的含量工资包干节余", report=r2) ,
            ReportItems(item_id=4090000, item_name=u"以前年度损益调整", report=r2) ,
            ReportItems(item_id=5010000, item_name=u"利润总额", report=r2) ,
            ReportItems(item_id=5020000, item_name=u"所得税", report=r2) ,
            ReportItems(item_id=5030000, item_name=u"少数股东损益", report=r2) ,
            ReportItems(item_id=5040000, item_name=u"未确认的投资损失", report=r2) ,
            ReportItems(item_id=6010000, item_name=u"净利润", report=r2) ,
            ReportItems(item_id=6020000, item_name=u"年初未分配利润", report=r2) ,
            ReportItems(item_id=6030000, item_name=u"盈余公积补亏", report=r2) ,
            ReportItems(item_id=6040000, item_name=u"其他调整因素", report=r2) ,
            ReportItems(item_id=7010000, item_name=u"可供分配的利润", report=r2) ,
            ReportItems(item_id=7020000, item_name=u"单项留用的利润", report=r2) ,
            ReportItems(item_id=7030000, item_name=u"补充流动资本", report=r2) ,
            ReportItems(item_id=7040000, item_name=u"提取法定盈余公积", report=r2) ,
            ReportItems(item_id=7050000, item_name=u"提取法定公益金", report=r2) ,
            ReportItems(item_id=7060000, item_name=u"提取职工奖励及福利基金", report=r2) ,
            ReportItems(item_id=7070000, item_name=u"提取储备基金", report=r2) ,
            ReportItems(item_id=7080000, item_name=u"提取企业发展基金", report=r2) ,
            ReportItems(item_id=7090000, item_name=u"利润归还投资", report=r2) ,
            ReportItems(item_id=7100000, item_name=u"其他", report=r2) ,
            ReportItems(item_id=8010000, item_name=u"可供投资者分配的利润", report=r2) ,
            ReportItems(item_id=8020000, item_name=u"应付优先股股利", report=r2) ,
            ReportItems(item_id=8030000, item_name=u"提取任意盈余公积", report=r2) ,
            ReportItems(item_id=8040000, item_name=u"应付普通股股利", report=r2) ,
            ReportItems(item_id=8050000, item_name=u"转作资本的普通股股利", report=r2) ,
            ReportItems(item_id=8060000, item_name=u"其他", report=r2) ,
            ReportItems(item_id=9010000, item_name=u"未分配利润", report=r2) ,
            ReportItems(item_id=9010100, item_name=u"应由以后年度税前利润弥补的亏损", report=r2) ,
            ReportItems(item_id=1000000, item_name=u"经营活动产生的现金流量", report=r3) ,
            ReportItems(item_id=1010000, item_name=u"销售商品、提供劳务收到的现金", report=r3) ,
            ReportItems(item_id=1020000, item_name=u"收到的税费返还", report=r3) ,
            ReportItems(item_id=1030000, item_name=u"收到的其他与经营活动有关的现金", report=r3) ,
            ReportItems(item_id=1040000, item_name=u"经营活动现金流入小计", report=r3) ,
            ReportItems(item_id=1050000, item_name=u"购买商品、接受劳务支付的现金", report=r3) ,
            ReportItems(item_id=1060000, item_name=u"支付给职工以及为职工支付的现金", report=r3) ,
            ReportItems(item_id=1070000, item_name=u"支付的各项税费", report=r3) ,
            ReportItems(item_id=1080000, item_name=u"支付的其他与经营活动有关的现金", report=r3) ,
            ReportItems(item_id=1090000, item_name=u"经营活动现金流出小计", report=r3) ,
            ReportItems(item_id=1100000, item_name=u"经营活动产生的现金流量净额", report=r3) ,
            ReportItems(item_id=2000000, item_name=u"投资活动产生的现金流量", report=r3) ,
            ReportItems(item_id=2010000, item_name=u"收回投资所收到的现金", report=r3) ,
            ReportItems(item_id=2020000, item_name=u"取得投资收益所收到的现金", report=r3) ,
            ReportItems(item_id=2030000, item_name=u"处置固定、无形和其他长期资产所收回的现金净额", report=r3) ,
            ReportItems(item_id=2040000, item_name=u"收到的其他与投资活动有关的现金", report=r3) ,
            ReportItems(item_id=2050000, item_name=u"投资活动现金流入小计", report=r3) ,
            ReportItems(item_id=2060000, item_name=u"购建固定资产、无形资产和其他长期资产所支付的现金", report=r3) ,
            ReportItems(item_id=2070000, item_name=u"投资所支付的现金", report=r3) ,
            ReportItems(item_id=2080000, item_name=u"支付的其他与投资活动有关的现金", report=r3) ,
            ReportItems(item_id=2090000, item_name=u"投资活动现金流出小计", report=r3) ,
            ReportItems(item_id=2100000, item_name=u"投资活动产生的现金流量净额", report=r3) ,
            ReportItems(item_id=3000000, item_name=u"筹资活动产生的现金流量", report=r3) ,
            ReportItems(item_id=3010000, item_name=u"吸收投资所收到的现金", report=r3) ,
            ReportItems(item_id=3020000, item_name=u"借款所收到的现金", report=r3) ,
            ReportItems(item_id=3030000, item_name=u"收到的其他与筹资活动有关的现金", report=r3) ,
            ReportItems(item_id=3040000, item_name=u"筹资活动现金流入小计", report=r3) ,
            ReportItems(item_id=3050000, item_name=u"偿还债务所支付的现金", report=r3) ,
            ReportItems(item_id=3060000, item_name=u"分配股利、利润或偿付利息所支付的现金", report=r3) ,
            ReportItems(item_id=3070000, item_name=u"支付的其他与筹资活动有关的现金", report=r3) ,
            ReportItems(item_id=3080000, item_name=u"筹资活动现金流出小计", report=r3) ,
            ReportItems(item_id=3090000, item_name=u"筹资活动产生的现金流量净额", report=r3) ,
            ReportItems(item_id=4000000, item_name=u"汇率变动对现金的影响", report=r3) ,
            ReportItems(item_id=5000000, item_name=u"现金及现金等价物净增加额", report=r3) ,
            ReportItems(item_id=5010000, item_name=u"将净利润调节为经营活动现金流量：", report=r3) ,
            ReportItems(item_id=5010100, item_name=u"净利润", report=r3) ,
            ReportItems(item_id=5010101, item_name=u"计提的资产减值准备", report=r3) ,
            ReportItems(item_id=5010102, item_name=u"固定资产折旧", report=r3) ,
            ReportItems(item_id=5010103, item_name=u"无形资产摊销", report=r3) ,
            ReportItems(item_id=5010104, item_name=u"长期待摊费用摊销", report=r3) ,
            ReportItems(item_id=5010105, item_name=u"待摊费用减少", report=r3) ,
            ReportItems(item_id=5010106, item_name=u"预提费用增加", report=r3) ,
            ReportItems(item_id=5010107, item_name=u"处置固定资产、无形资产和其他长期资产的损失", report=r3) ,
            ReportItems(item_id=5010108, item_name=u"固定资产报废损失", report=r3) ,
            ReportItems(item_id=5010110, item_name=u"财务费用", report=r3) ,
            ReportItems(item_id=5010111, item_name=u"投资损失", report=r3) ,
            ReportItems(item_id=5010112, item_name=u"递延税款贷项", report=r3) ,
            ReportItems(item_id=5010113, item_name=u"存货的减少", report=r3) ,
            ReportItems(item_id=5010114, item_name=u"经营性应收项目的减少", report=r3) ,
            ReportItems(item_id=5010115, item_name=u"经营性应付项目的增加", report=r3) ,
            ReportItems(item_id=5010116, item_name=u"其他", report=r3) ,
            ReportItems(item_id=5010117, item_name=u"经营活动产生的现金流量净额", report=r3) ,
            ReportItems(item_id=5020000, item_name=u"不涉及现金收支的投资和筹资活动：", report=r3) ,
            ReportItems(item_id=5020100, item_name=u"债务转为资本", report=r3) ,
            ReportItems(item_id=5020200, item_name=u"一年内到期的可转换公司债券", report=r3) ,
            ReportItems(item_id=5020300, item_name=u"融资租入固定资产", report=r3) ,
            ReportItems(item_id=5020400, item_name=u"其他", report=r3) ,
            ReportItems(item_id=5030000, item_name=u"现金及现金等价物净增加情况：", report=r3) ,
            ReportItems(item_id=5030100, item_name=u"现金的期末余额", report=r3) ,
            ReportItems(item_id=5030200, item_name=u"现金的期初余额", report=r3) ,
            ReportItems(item_id=5030300, item_name=u"现金等价物的期末余额", report=r3) ,
            ReportItems(item_id=5030400, item_name=u"现金等价物的期初余额", report=r3) ,
            ReportItems(item_id=5030500, item_name=u"现金及现金等价物净增加额", report=r3) ,
            ReportItems(item_id=1000000, item_name=u"盈利能力分析指标", report=r4) ,
            ReportItems(item_id=1010000, item_name=u"销售利润率", report=r4) ,
            ReportItems(item_id=1020000, item_name=u"营业利润率", report=r4) ,
            ReportItems(item_id=1030000, item_name=u"税前利润率", report=r4) ,
            ReportItems(item_id=1040000, item_name=u"销售净利润率", report=r4) ,
            ReportItems(item_id=1050000, item_name=u"成本费用利润率", report=r4) ,
            ReportItems(item_id=1060000, item_name=u"资产收益率", report=r4) ,
            ReportItems(item_id=1070000, item_name=u"净资产收益率", report=r4) ,
            ReportItems(item_id=1100000, item_name=u"总资产报酬率", report=r4) ,
            ReportItems(item_id=1110000, item_name=u"投资收益率", report=r4) ,
            ReportItems(item_id=1120000, item_name=u"主营收入现金率", report=r4) ,
            ReportItems(item_id=1130000, item_name=u"毛利率", report=r4) ,
            ReportItems(item_id=1140000, item_name=u"投资收益现金率", report=r4) ,
            ReportItems(item_id=2000000, item_name=u"营运能力分析指标", report=r4) ,
            ReportItems(item_id=2010000, item_name=u"总资产周转率(次)", report=r4) ,
            ReportItems(item_id=2020000, item_name=u"固定资产周转率(次)", report=r4) ,
            ReportItems(item_id=2030000, item_name=u"应收帐款周转率(次)", report=r4) ,
            ReportItems(item_id=2040000, item_name=u"存货周转率(次)", report=r4) ,
            ReportItems(item_id=2050000, item_name=u"权益报酬率", report=r4) ,
            ReportItems(item_id=2060000, item_name=u"商品销售率", report=r4) ,
            ReportItems(item_id=2070000, item_name=u"流动资产周转率(次)", report=r4) ,
            ReportItems(item_id=3000000, item_name=u"长期偿债能力分析指标", report=r4) ,
            ReportItems(item_id=3010000, item_name=u"资产负债比率", report=r4) ,
            ReportItems(item_id=3020000, item_name=u"负债与所有者权益比率", report=r4) ,
            ReportItems(item_id=3030000, item_name=u"负债与有形净资产比率", report=r4) ,
            ReportItems(item_id=3040000, item_name=u"利息保障倍数", report=r4) ,
            ReportItems(item_id=3050000, item_name=u"长期投资占净资产比率", report=r4) ,
            ReportItems(item_id=3060000, item_name=u"长期债务与营运资金比率", report=r4) ,
            ReportItems(item_id=3070000, item_name=u"净资产与期末贷款余额比率", report=r4) ,
            ReportItems(item_id=3080000, item_name=u"资本固定化比率", report=r4) ,
            ReportItems(item_id=3090000, item_name=u"固定资产净值率", report=r4) ,
            ReportItems(item_id=3100000, item_name=u"长期投资与长期资本比率", report=r4) ,
            ReportItems(item_id=3110000, item_name=u"长期资产适合率", report=r4) ,
            ReportItems(item_id=3120000, item_name=u"总资本化比率", report=r4) ,
            ReportItems(item_id=4000000, item_name=u"短期偿债能力分析指标", report=r4) ,
            ReportItems(item_id=4010000, item_name=u"流动比率", report=r4) ,
            ReportItems(item_id=4020000, item_name=u"速动比率", report=r4) ,
            ReportItems(item_id=4030000, item_name=u"现金比率", report=r4) ,
            ReportItems(item_id=4040000, item_name=u"营运资金", report=r4) ,
            ReportItems(item_id=4050000, item_name=u"现金流动负债比率", report=r4) ,
            ReportItems(item_id=4060000, item_name=u"担保比率", report=r4) ,
            ReportItems(item_id=4070000, item_name=u"投资性现金流动负债比率", report=r4) ,
            ReportItems(item_id=5000000, item_name=u"增长比率", report=r4) ,
            ReportItems(item_id=5010000, item_name=u"净利润增长率", report=r4) ,
            ReportItems(item_id=5020000, item_name=u"总资产增长率", report=r4) ,
            ReportItems(item_id=5030000, item_name=u"总负债增长率", report=r4) ,
            ReportItems(item_id=5040000, item_name=u"资产净值增长率", report=r4) ,
            ReportItems(item_id=5050000, item_name=u"营业收入增长率", report=r4) ,
            ReportItems(item_id=5060000, item_name=u"利润增长率", report=r4) ,
            ReportItems(item_id=6000000, item_name=u"经济实力", report=r4) ,
            ReportItems(item_id=6010000, item_name=u"实有净资产", report=r4) ,
            ReportItems(item_id=6020000, item_name=u"有形长期资产", report=r4) ,
            ReportItems(item_id=1000000, item_name=u"资产", report=r6) ,
            ReportItems(item_id=1000001, item_name=u"资产总计", report=r6) ,
            ReportItems(item_id=1010000, item_name=u"流动资产", report=r6) ,
            ReportItems(item_id=1010001, item_name=u"流动资产合计", report=r6) ,

            ReportItems(item_id=1010100, item_name=u"货币资金", report=r6) ,
            ReportItems(item_id=1010200, item_name=u"交易性金融资产", report=r6) ,
            ReportItems(item_id=1010300, item_name=u"应收票据", report=r6) ,
            ReportItems(item_id=1010400, item_name=u"应收账款", report=r6) ,
            ReportItems(item_id=1010500, item_name=u"预付账款", report=r6) ,
            ReportItems(item_id=1010600, item_name=u"应收利息", report=r6) ,
            ReportItems(item_id=1010700, item_name=u"应收股利", report=r6) ,
            ReportItems(item_id=1010800, item_name=u"其他应收款", report=r6) ,
            ReportItems(item_id=1010900, item_name=u"存货", report=r6) ,
            ReportItems(item_id=1011000, item_name=u"一年内到期的非流动资产", report=r6) ,
            ReportItems(item_id=1011100, item_name=u"其他流动资产", report=r6) ,

			ReportItems(item_id=1020000, item_name=u"非流动资产", report=r6) ,
            ReportItems(item_id=1020001, item_name=u"非流动资产合计", report=r6) ,
            ReportItems(item_id=1020100, item_name=u"可供出售的金融资产", report=r6) ,
            ReportItems(item_id=1020200, item_name=u"持有至到期投资", report=r6) ,
            ReportItems(item_id=1020300, item_name=u"长期股权投资", report=r6) ,
            ReportItems(item_id=1020400, item_name=u"长期应收款", report=r6) ,
            ReportItems(item_id=1020500, item_name=u"投资性房地产", report=r6) ,
            ReportItems(item_id=1020600, item_name=u"固定资产", report=r6) ,
            ReportItems(item_id=1020700, item_name=u"在建工程", report=r6) ,
            ReportItems(item_id=1020800, item_name=u"工程物资", report=r6) ,
            ReportItems(item_id=1020900, item_name=u"固定资产清理", report=r6) ,
            ReportItems(item_id=1021000, item_name=u"生产性生物资产", report=r6) ,
            ReportItems(item_id=1021100, item_name=u"油气资产", report=r6) ,
            ReportItems(item_id=1021200, item_name=u"无形资产", report=r6) ,
            ReportItems(item_id=1021300, item_name=u"开发支出", report=r6) ,
            ReportItems(item_id=1021400, item_name=u"商誉", report=r6) ,
            ReportItems(item_id=1021500, item_name=u"长期待摊费用", report=r6) ,
            ReportItems(item_id=1021600, item_name=u"递延所得税资产", report=r6) ,
            ReportItems(item_id=1021700, item_name=u"其他非流动资产", report=r6) ,





            ReportItems(item_id=2000000, item_name=u"负债", report=r6) ,
            ReportItems(item_id=2000001, item_name=u"负债总计", report=r6) ,



            ReportItems(item_id=2010000, item_name=u"流动负债", report=r6) ,

            ReportItems(item_id=2010001, item_name=u"流动负债合计", report=r6) ,


            ReportItems(item_id=2010100, item_name=u"短期借款", report=r6) ,
            ReportItems(item_id=2010200, item_name=u"交易性金融负债", report=r6) ,
            ReportItems(item_id=2010300, item_name=u"应付票据", report=r6) ,
            ReportItems(item_id=2010400, item_name=u"应付账款", report=r6) ,
            ReportItems(item_id=2010500, item_name=u"预收账款", report=r6) ,
            ReportItems(item_id=2010600, item_name=u"应付利息", report=r6) ,
            ReportItems(item_id=2010700, item_name=u"应付职工薪酬", report=r6) ,
            ReportItems(item_id=2010800, item_name=u"应交税费", report=r6) ,
            ReportItems(item_id=2010900, item_name=u"应付股利", report=r6) ,
            ReportItems(item_id=2011000, item_name=u"其他应付款", report=r6) ,
			ReportItems(item_id=2011100, item_name=u"一年内到期的非流动负债", report=r6) ,
            ReportItems(item_id=2011200, item_name=u"其他流动负债", report=r6) ,

			ReportItems(item_id=2020000, item_name=u"非流动负债", report=r6) ,
            ReportItems(item_id=2020001, item_name=u"非流动负债合计", report=r6) ,


            ReportItems(item_id=2020100, item_name=u"长期借款", report=r6) ,
            ReportItems(item_id=2020200, item_name=u"应付债券", report=r6) ,
            ReportItems(item_id=2020300, item_name=u"长期应付款", report=r6) ,
            ReportItems(item_id=2020400, item_name=u"专项应付款", report=r6) ,
            ReportItems(item_id=2020500, item_name=u"预计负债", report=r6) ,
            ReportItems(item_id=2020600, item_name=u"递延所得税负债", report=r6) ,
            ReportItems(item_id=2020700, item_name=u"其他非流动负债", report=r6) ,

            ReportItems(item_id=3000000, item_name=u"所有者权益合计", report=r6) ,
            ReportItems(item_id=3000001, item_name=u"负债和所有者权益合计", report=r6) ,
            ReportItems(item_id=3010100, item_name=u"实收资本（或股本）", report=r6) ,
            ReportItems(item_id=3010200, item_name=u"资本公积", report=r6) ,
            ReportItems(item_id=3010300, item_name=u"减：库存股", report=r6) ,
            ReportItems(item_id=3010400, item_name=u"盈余公积", report=r6) ,
            ReportItems(item_id=3010500, item_name=u"未分配利润", report=r6) ,

            ReportItems(item_id=1000000, item_name=u"一、营业收入", report=r7) ,
            ReportItems(item_id=1010100, item_name=u"减：营业成本", report=r7) ,
            ReportItems(item_id=1010200, item_name=u"营业税金及附加", report=r7) ,
            ReportItems(item_id=1010300, item_name=u"销售费用", report=r7) ,
            ReportItems(item_id=1010400, item_name=u"管理费用", report=r7) ,
            ReportItems(item_id=1010500, item_name=u"财务费用", report=r7) ,
            ReportItems(item_id=1010600, item_name=u"资产减值损失", report=r7) ,
            ReportItems(item_id=1010700, item_name=u"加：公允价值变动净收益（损失以“—”填列）", report=r7) ,
            ReportItems(item_id=1010800, item_name=u"投资净收益（损失以“—”填列）", report=r7) ,
            ReportItems(item_id=1010900, item_name=u"其中，对联营企业和合营企业的投资收益", report=r7) ,
            ReportItems(item_id=2000000, item_name=u"二、营业利润（损失以“—”填列）", report=r7) ,
            ReportItems(item_id=2010100, item_name=u"加：营业外收入", report=r7) ,
            ReportItems(item_id=2010200, item_name=u"减：营业外支出", report=r7) ,
            ReportItems(item_id=2010300, item_name=u"其中，非流动资产损失", report=r7) ,
            ReportItems(item_id=3000000, item_name=u"三、利润总额（损失以“—”填列）", report=r7) ,
            ReportItems(item_id=3010100, item_name=u"减：所得税费用", report=r7) ,
            ReportItems(item_id=4000000, item_name=u"四、净利润（损失以“—”填列）", report=r7) ,
            ReportItems(item_id=4010100, item_name=u"（一）基本每股收益", report=r7) ,
            ReportItems(item_id=4010200, item_name=u"（二）稀释每股收益", report=r7) ,

            ReportItems(item_id=1000000, item_name=u"一、经营活动产生的现金流量：", report=r8) ,
            ReportItems(item_id=1010100, item_name=u"销售商品、提供劳务收到的现金", report=r8) ,
            ReportItems(item_id=1010200, item_name=u"收到的税费返还", report=r8) ,
            ReportItems(item_id=1010300, item_name=u"收到其他与经营活动有关的现金", report=r8) ,
            ReportItems(item_id=1010400, item_name=u"经营活动现金流入小计", report=r8) ,
            ReportItems(item_id=1010500, item_name=u"购买商品、接受劳务支付的现金", report=r8) ,
            ReportItems(item_id=1010600, item_name=u"支付给职工以及为职工支付的现金", report=r8) ,
            ReportItems(item_id=1010700, item_name=u"支付的各项税费", report=r8) ,
            ReportItems(item_id=1010800, item_name=u"支付其他与经营活动有关的现金", report=r8) ,
            ReportItems(item_id=1010900, item_name=u"经营活动现金流出小计", report=r8) ,
            ReportItems(item_id=1011000, item_name=u"经营活动产生的现金流量净额", report=r8) ,

            ReportItems(item_id=2000000, item_name=u"二、投资活动产生的现金流量：", report=r8) ,
            ReportItems(item_id=2010100, item_name=u"收回投资收到的现金", report=r8) ,
            ReportItems(item_id=2010200, item_name=u"取得投资收益收到的现金", report=r8) ,
            ReportItems(item_id=2010300, item_name=u"处置固定资产、无形资产和其他长期资产收回的现金净额", report=r8) ,
            ReportItems(item_id=2010400, item_name=u"处置子公司及其他营业单位收到的现金净额", report=r8) ,
            ReportItems(item_id=2010500, item_name=u"收到其他与投资活动有关的现金", report=r8) ,
            ReportItems(item_id=2010600, item_name=u"投资活动现金流入小计", report=r8) ,
            ReportItems(item_id=2010700, item_name=u"购建固定资产、无形资产和其他长期资产支付的现金", report=r8) ,
            ReportItems(item_id=2010800, item_name=u"投资所支付的现金", report=r8) ,
            ReportItems(item_id=2010900, item_name=u"取得子公司及其他营业单位支付的现金净额", report=r8) ,
            ReportItems(item_id=2011000, item_name=u"支付其他与投资活动有关的现金", report=r8) ,
            ReportItems(item_id=2011100, item_name=u"投资活动现金流出小计", report=r8) ,
            ReportItems(item_id=2011200, item_name=u"投资活动产生的现金流量净额", report=r8) ,

            ReportItems(item_id=3000000, item_name=u"三、筹资活动产生的现金流量：", report=r8) ,
            ReportItems(item_id=3010100, item_name=u"吸收投资收到的现金", report=r8) ,
            ReportItems(item_id=3010200, item_name=u"取得借款收到的现金", report=r8) ,
            ReportItems(item_id=3010300, item_name=u"收到其他与筹资活动有关的现金", report=r8) ,
            ReportItems(item_id=3010400, item_name=u"筹资活动现金流入小计", report=r8) ,
            ReportItems(item_id=3010500, item_name=u"偿还债务支付的现金", report=r8) ,
            ReportItems(item_id=3010600, item_name=u"分配股利、利润或偿付利息支付的现金", report=r8) ,
            ReportItems(item_id=3010700, item_name=u"支付其他与筹资活动有关的现金", report=r8) ,
            ReportItems(item_id=3010800, item_name=u"筹资活动现金流出小计", report=r8) ,
            ReportItems(item_id=3010900, item_name=u"筹资活动产生的现金流量净额", report=r8) ,

            ReportItems(item_id=4000000, item_name=u"四、汇率变动对现金及现金等价物的影响", report=r8) ,
            ReportItems(item_id=5000000, item_name=u"五、现金及现金等价物净增加额", report=r8) ,
            ReportItems(item_id=5010000, item_name=u"加：期初现金及现金等价物余额", report=r8) ,
            ReportItems(item_id=6000000, item_name=u"六、 期末现金及现金等价物余额", report=r8) ,
            ReportItems(item_id=6010000, item_name=u"现金流量表补充资料如下：", report=r8) ,
            ReportItems(item_id=6010100, item_name=u"1.将净利润调节为经营活动现金流量：", report=r8) ,
            ReportItems(item_id=6010200, item_name=u"净利润", report=r8) ,
            ReportItems(item_id=6010201, item_name=u"加：资产减值准备", report=r8) ,
            ReportItems(item_id=6010202, item_name=u"　　固定资产折旧、油气资产折耗、生产性生物资产折旧", report=r8) ,
            ReportItems(item_id=6010203, item_name=u"　　无形资产摊销", report=r8) ,
            ReportItems(item_id=6010204, item_name=u"　　长期待摊费用摊销", report=r8) ,
            ReportItems(item_id=6010205, item_name=u"　　待摊费用减少（减：增加）", report=r8) ,
            ReportItems(item_id=6010206, item_name=u"　　预提费用增加（减：减少）", report=r8) ,
            ReportItems(item_id=6010207, item_name=u"　　处置固定资产、无形资产和其他长期资产的损失（收益以“-”号填列）", report=r8) ,
            ReportItems(item_id=6010208, item_name=u"　　固定资产报废损失（收益以“-”号填列）", report=r8) ,
            ReportItems(item_id=6010209, item_name=u"　　公允价值变动损失（收益以“-”号填列）", report=r8) ,
            ReportItems(item_id=6010210, item_name=u"　　财务费用（收益以“-”号填列）", report=r8) ,
            ReportItems(item_id=6010211, item_name=u"　　投资损失（收益以“-”号填列）", report=r8) ,
            ReportItems(item_id=6010212, item_name=u"　　递延所得税资产减少（增加以“-”号填列）", report=r8) ,
            ReportItems(item_id=6010300, item_name=u"递延所得税负债增加（减少以“-”号填列）", report=r8) ,
            ReportItems(item_id=6010301, item_name=u"　　存货的减少（增加以“-”号填列）", report=r8) ,
            ReportItems(item_id=6010302, item_name=u"　　经营性应收项目的减少（增加以“-”号填列）", report=r8) ,
            ReportItems(item_id=6010303, item_name=u"　　经营性应付项目的增加（减少以“-”号填列）", report=r8) ,
            ReportItems(item_id=6010400, item_name=u"其他", report=r8) ,
            ReportItems(item_id=6010500, item_name=u"经营活动产生的现金流量净额", report=r8) ,
            ReportItems(item_id=6020000, item_name=u"2.不涉及现金收支的重大投资和筹资活动：", report=r8) ,
            ReportItems(item_id=6020100, item_name=u"债务转为资本", report=r8) ,
            ReportItems(item_id=6020200, item_name=u"一年内到期的可转换公司债券", report=r8) ,
            ReportItems(item_id=6020300, item_name=u"融资租入固定资产", report=r8) ,
            ReportItems(item_id=6020400, item_name=u"其他", report=r8) ,
            ReportItems(item_id=6030100, item_name=u"3.现金及现金等价物净变动情况：", report=r8) ,
            ReportItems(item_id=6030200, item_name=u"现金的期末余额", report=r8) ,
            ReportItems(item_id=6030300, item_name=u"减：现金的期初余额", report=r8) ,
            ReportItems(item_id=6030400, item_name=u"加：现金等价物的期末余额", report=r8) ,
            ReportItems(item_id=6030500, item_name=u"减：现金等价物的期初余额", report=r8) ,
            ReportItems(item_id=6030600, item_name=u"现金及现金等价物净增加额", report=r8) ,
            ReportItems(item_id=1000000, item_name=u"一、资产类", report=r9) ,
            ReportItems(item_id=1010100, item_name=u"现金", report=r9) ,
            ReportItems(item_id=1010200, item_name=u"银行存款", report=r9) ,
            ReportItems(item_id=1010300, item_name=u"应收票据", report=r9) ,
            ReportItems(item_id=1010400, item_name=u"应收账款", report=r9) ,
            ReportItems(item_id=1010500, item_name=u"预付账款", report=r9) ,
            ReportItems(item_id=1010600, item_name=u"其他应收款", report=r9) ,
            ReportItems(item_id=1010700, item_name=u"材料", report=r9) ,
            ReportItems(item_id=1010800, item_name=u"产成品", report=r9) ,
            ReportItems(item_id=1010900, item_name=u"对外投资", report=r9) ,
            ReportItems(item_id=1011000, item_name=u"固定资产", report=r9) ,
            ReportItems(item_id=1011100, item_name=u"无形资产", report=r9) ,
            ReportItems(item_id=1011200, item_name=u"资产合计：", report=r9) ,
            ReportItems(item_id=2000000, item_name=u"五、支出类", report=r9) ,
            ReportItems(item_id=2010100, item_name=u"拨出经费", report=r9) ,
            ReportItems(item_id=2010200, item_name=u"拨出专款", report=r9) ,
            ReportItems(item_id=2010300, item_name=u"专款支出", report=r9) ,
            ReportItems(item_id=2010400, item_name=u"事业支出", report=r9) ,
            ReportItems(item_id=2010500, item_name=u"经营支出", report=r9) ,
            ReportItems(item_id=2010600, item_name=u"成本费用", report=r9) ,
            ReportItems(item_id=2010700, item_name=u"销售税金", report=r9) ,
            ReportItems(item_id=2010800, item_name=u"上缴上级支出", report=r9) ,
            ReportItems(item_id=2010900, item_name=u"对附属单位补助", report=r9) ,
            ReportItems(item_id=2011000, item_name=u"结转自筹基建", report=r9) ,
            ReportItems(item_id=2011100, item_name=u"支出合计：", report=r9) ,
            ReportItems(item_id=2011200, item_name=u"资产部类总计：", report=r9) ,
            ReportItems(item_id=3000000, item_name=u"二、负债类", report=r9) ,
            ReportItems(item_id=3010100, item_name=u"借记款项", report=r9) ,
            ReportItems(item_id=3010200, item_name=u"应付票据", report=r9) ,
            ReportItems(item_id=3010300, item_name=u"应付账款", report=r9) ,
            ReportItems(item_id=3010400, item_name=u"预收账款", report=r9) ,
            ReportItems(item_id=3010500, item_name=u"其他应付款", report=r9) ,
            ReportItems(item_id=3010600, item_name=u"应缴预算款", report=r9) ,
            ReportItems(item_id=3010700, item_name=u"应缴财政专户款", report=r9) ,
            ReportItems(item_id=3010800, item_name=u"应交税金", report=r9) ,
            ReportItems(item_id=3010900, item_name=u"负债合计：", report=r9) ,
            ReportItems(item_id=4000000, item_name=u"三、净资产类", report=r9) ,
            ReportItems(item_id=4010100, item_name=u"事业基金", report=r9) ,
            ReportItems(item_id=4010200, item_name=u"其中：一般基金", report=r9) ,
            ReportItems(item_id=4010300, item_name=u"投资基金", report=r9) ,
            ReportItems(item_id=4010400, item_name=u"固定基金", report=r9) ,
            ReportItems(item_id=4010500, item_name=u"专用基金", report=r9) ,
            ReportItems(item_id=4010600, item_name=u"事业结余", report=r9) ,
            ReportItems(item_id=4010700, item_name=u"经营结余", report=r9) ,
            ReportItems(item_id=4010800, item_name=u"净资产合计：", report=r9) ,
            ReportItems(item_id=5000000, item_name=u"四、收入类", report=r9) ,
            ReportItems(item_id=5010100, item_name=u"财政补助收入", report=r9) ,
            ReportItems(item_id=5010200, item_name=u"上级补助收入", report=r9) ,
            ReportItems(item_id=5010300, item_name=u"拨入专款", report=r9) ,
            ReportItems(item_id=5010400, item_name=u"事业收入", report=r9) ,
            ReportItems(item_id=5010500, item_name=u"经营收入", report=r9) ,
            ReportItems(item_id=5010600, item_name=u"附属单位缴款", report=r9) ,
            ReportItems(item_id=5010700, item_name=u"其他收入", report=r9) ,
            ReportItems(item_id=5010800, item_name=u"收入合计：", report=r9) ,
            ReportItems(item_id=5010900, item_name=u"负债部类总计：", report=r9) ,
            ReportItems(item_id=1000000, item_name=u"财政补助收入", report=r10) ,
            ReportItems(item_id=1010100, item_name=u"上级补助收入", report=r10) ,
            ReportItems(item_id=1010200, item_name=u"附属单位缴款", report=r10) ,
            ReportItems(item_id=1010300, item_name=u"事业收入", report=r10) ,
            ReportItems(item_id=1010400, item_name=u"其中：预算外资金收入", report=r10) ,
            ReportItems(item_id=1010500, item_name=u"其他收入", report=r10) ,
            ReportItems(item_id=1010600, item_name=u"小计", report=r10) ,
            ReportItems(item_id=1010700, item_name=u"经营收入", report=r10) ,
            ReportItems(item_id=1010800, item_name=u"小计", report=r10) ,
            ReportItems(item_id=1010900, item_name=u"拨入专款", report=r10) ,
            ReportItems(item_id=1011000, item_name=u"小计", report=r10) ,
            ReportItems(item_id=1011100, item_name=u"总计", report=r10) ,
            ReportItems(item_id=1011200, item_name=u"拨出经费", report=r10) ,
            ReportItems(item_id=1011300, item_name=u"上缴上级支出", report=r10) ,
            ReportItems(item_id=1011400, item_name=u"对附属单位补助", report=r10) ,
            ReportItems(item_id=1011500, item_name=u"事业支出", report=r10) ,
            ReportItems(item_id=1011600, item_name=u"其中：财政补助支出", report=r10) ,
            ReportItems(item_id=1011700, item_name=u"预算外资金支出", report=r10) ,
            ReportItems(item_id=1011800, item_name=u"销售税金", report=r10) ,
            ReportItems(item_id=1011900, item_name=u"结转自筹基建", report=r10) ,
            ReportItems(item_id=1012000, item_name=u"小计", report=r10) ,
            ReportItems(item_id=1012100, item_name=u"经营支出", report=r10) ,
            ReportItems(item_id=1012200, item_name=u"销售税金", report=r10) ,
            ReportItems(item_id=1012300, item_name=u"小计", report=r10) ,
            ReportItems(item_id=1012400, item_name=u"拨出专款", report=r10) ,
            ReportItems(item_id=1012500, item_name=u"专款支出", report=r10) ,
            ReportItems(item_id=1012600, item_name=u"小计", report=r10) ,
            ReportItems(item_id=1012700, item_name=u"总计", report=r10) ,
            ReportItems(item_id=1020100, item_name=u"事业结余", report=r10) ,
            ReportItems(item_id=1020200, item_name=u"1.正常收入结余", report=r10) ,
            ReportItems(item_id=1020300, item_name=u"2.收回以前年度事业支出", report=r10) ,
            ReportItems(item_id=1030100, item_name=u"经营结余", report=r10) ,
            ReportItems(item_id=1030200, item_name=u"以前年度经营亏损（一）", report=r10) ,
            ReportItems(item_id=1030300, item_name=u"结余分配", report=r10) ,
            ReportItems(item_id=1030400, item_name=u"1.应交所得税", report=r10) ,
            ReportItems(item_id=1030500, item_name=u"2.提取专用基金", report=r10) ,
            ReportItems(item_id=1030600, item_name=u"3.转入事业基金", report=r10) ,
            ReportItems(item_id=1030700, item_name=u"4.其他", report=r10)
        ])

        self.session.commit()

    def tearDown(self):
        #self.session.rollback()
        #Base.metadata.drop_all(self.session.bind)
        self.session.commit()



