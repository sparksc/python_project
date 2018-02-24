# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import defer
from sqlalchemy.orm import with_polymorphic
import unittest

import logging
from ..model.credit import *
from ..model.transaction import *
from ..model.application import *
from ..model.party import *
from ..workflow import task
from ..workflow.parameter import *
from ..model.task import *

import datetime

logging.basicConfig(level=logging.DEBUG)
class TestLoan(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()
        #Base.metadata.drop_all(self.session.bind)
        #Base.metadata.create_all(self.session.bind)

        #self.init_util()
        #self.init_product()
        #self.init_user_group()
        #self.init_customer()
        #self.init_branch()
        #self.init_flow()

    def test_query(self):
        user = self.session.query(User).filter_by(user_name="00510").first()
        self.nodone_deal(user)
        #self.done_deal(user)


    def btest_process_workflow(self):

        log.debug("start process workflow!")

        start_activity = self.session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"贷款申请流程").first()

        #user = self.session.query(User).filter_by(user_name="00540").first()

        cust = self.session.query(Customer).join(Party, Party.id == Customer.role_id).filter(Party.name == u'张三').first()
        logging.debug(cust)
        application_transaction = ApplicationTransaction(transaction_name=u"%s的贷款申请"%(cust.party.name))
        application = Application(**{
            'application_transaction':application_transaction,
            'customer_id' : cust.role_id,
            'product_code': '102'
        })
        start_activity.bind_transaction(application_transaction)

        # 贷款申请					客户经理
        user = self.session.query(User).filter_by(user_name="00510").first()
        self.process_task(application_transaction, user)

        # 预审						支行审查岗
        user = self.session.query(User).filter_by(user_name="00779").first()
        self.nodone_deal(user)

        self.process_task(application_transaction, user)

        # 支行风险评价				支行风险评价岗
        user = self.session.query(User).filter_by(user_name="00540").first()
        self.nodone_deal(user)
        self.process_task(application_transaction, user)

        # 支行审查					支行审查岗
        user = self.session.query(User).filter_by(user_name="00550").first()
        self.nodone_deal(user)
        self.process_task(application_transaction, user)

        # 支行审贷小组审议			支行审贷小组
        user = self.session.query(User).filter_by(user_name="00560").first()
        self.nodone_deal(user)
        self.process_task(application_transaction, user)

        # 支行长审批				支行行长
        user = self.session.query(User).filter_by(user_name="00570").first()
        self.nodone_deal(user)
        self.process_task(application_transaction, user)

        self.session.commit()


    def process_task(self,transation,user):
        groups = []
        for group in user.user_groups:
            groups.append(group.group.group_name)

        task_list = task.get_task(transation)
        for t in task_list:
            role = get_parameter(t.activity,u"角色")
            if role and role in groups:
                t.user = user
                t.finish()

    def atest_workflow_status(self):
        """
            测试已办、待办事务
        """
        roles = ['00530' ,'00540', '00550', '00560', '00570']

        user = self.session.query(User).filter_by(user_name=roles[2]).first()

        self.done_deal(user)       # 已完成

        self.nodone_deal(user) # 未完成


    def nodone_deal(self,user):
        """
            待办事项
            select ta.amount,pt.id,pt.no,pt.name, act.activity_name,ta.transaction_id,ap.id,pd.product_code,pd.name,pd.product_page from application ap
            left join application_transaction apt on apt.application_id=ap.id
            left join party pt on pt.id = ap.customer_id
            left join Product pd on pd.product_code=ap.product_code
            left join transaction ta on ta.transaction_id=apt.transaction_id
            left join transaction_activity taa on taa.transaction_id = apt.transaction_id
            left join activity act on act.activity_id=taa.activity_id
            where taa.transaction_activity_type='task' and taa.finished is not null
        """
        done_list = []
        credit_table = []
        groups = []
        for group in user.user_groups:
            groups.append(group.group.group_name)

        application_transaction = ApplicationTransaction.__table__

        query = self.session.query(Application, Activity \
            ,Transaction.amount,Activity.activity_name \
            ,Transaction.transaction_id, Application.id, Product.product_code, Product.name, Product.product_page) \
            .outerjoin(application_transaction, application_transaction.c.application_id==Application.id) \
            .outerjoin(Transaction, Transaction.transaction_id==ApplicationTransaction.transaction_id) \
            .outerjoin(Product, Product.product_code==Application.product_code) \
            .outerjoin(TransactionActivity, TransactionActivity.transaction_id==ApplicationTransaction.transaction_id) \
            .outerjoin(Activity, Activity.activity_id==TransactionActivity.activity_id) \
            .filter(TransactionActivity.finished==None) \
            .filter(TransactionActivity.transaction_activity_type=="task")

        logging.debug(query)

        result_set = query.all() \

        logging.debug(len(result_set))
        for item in result_set:
            role = get_parameter(item[1],u"角色")
            if role and role in groups:
                logging.debug(role)
                party = item[0].customer.party
                done_list.append({'amount':item[2],'party_id':party.id,'cust_no':party.no, "cust_name":party.name \
                    , "activity_name":item[3], "transaction_id":item[4], "application_id":item[5] \
                    , "product_code":item[6], "product_name":item[7],'product_page':item[8]})

        # TODO: 到期处理
        """
        comm = self.session.query(CommercialHouseCredit).filter(CommercialHouseCredit.transaction_id==tran.transaction_id,CommercialHouseCredit.status !=u'结束').first()
        if comm:
             credit_table.append({'transaction':comm.transaction,'application':comm.transaction.application,'cust':comm.transaction.application.customer,'party':comm.transaction.application.customer.party,'status':comm.status})
        """
        logging.debug(done_list)


    def done_deal(self,user):
        """
            已办事项
            .outerjoin(Party, Party.id==Application.customer_id)
        """
        result_set = self.session.query(Application, Activity \
            ,Transaction.amount,Activity.activity_name \
            ,Transaction.transaction_id, Application.id, Product.product_code, Product.name, Product.product_page,Task.user_id) \
            .outerjoin(ApplicationTransaction, ApplicationTransaction.application_id==Application.id) \
            .outerjoin(Product, Product.product_code==Application.product_code) \
            .outerjoin(TransactionActivity, TransactionActivity.transaction_id==ApplicationTransaction.transaction_id) \
            .outerjoin(Activity, Activity.activity_id==TransactionActivity.activity_id) \
            .outerjoin(Task, Task.transaction_activity_id==TransactionActivity.transaction_activity_id) \
            .filter(TransactionActivity.finished==True) \
            .filter(TransactionActivity.transaction_activity_type=="task") \
            .filter(Task.user_id==user.role_id).all() \

        done_list = []
        for item in result_set:
            party = item[0].customer.party
            done_list.append({'amount':item[2],'party_id':party.id,'cust_no':party.no, "cust_name":party.name \
            , "activity_name":item[3], "transaction_id":item[4], "application_id":item[5] \
            , "product_code":item[6], "product_name":item[7],'product_page':item[8]})

        logging.debug(done_list)


    def init_flow(self):
        """
        Workflow
        """
        log.debug("start init flow!")

        # Lendingproposition
        lendingproposition_task = TaskActivity(activity_name=u"贷款申请", task_assign_module='fabs.workflow.default', task_assign_function='lendingproposition_task', waiting=True)
        self.session.add(lendingproposition_task)
        set_parameter(lendingproposition_task, u"角色", u"客户经理")

        investigate_task = TaskActivity(activity_name=u"预审", task_assign_module='fabs.workflow.default', task_assign_function='investigate_task', waiting=True)
        self.session.add(investigate_task)
        set_parameter(investigate_task, u"角色", u"支行审查岗")

        # 并行
        subbranch_assessment_task = TaskActivity(activity_name=u"支行风险评价", task_assign_module='fabs.workflow.default', task_assign_function='subbranch_assessment_task', waiting=True)
        self.session.add(subbranch_assessment_task)
        set_parameter(subbranch_assessment_task, u"角色", u"支行风险评价岗")

        subbranch_review_task= TaskActivity(activity_name=u"支行审查", task_assign_module='fabs.workflow.default', task_assign_function='subbranch_review_task', waiting=True)
        self.session.add(subbranch_review_task)
        set_parameter(subbranch_review_task, u"角色", u"支行审查岗")


        subbranch_deliberation_task = TaskActivity(activity_name=u"支行审贷小组审议", task_assign_module='fabs.workflow.default', task_assign_function='subbranch_deliberation_task', waiting=True)
        self.session.add(subbranch_deliberation_task)
        set_parameter(subbranch_deliberation_task, u"角色", u"支行审贷小组")


        subbranch_president_task = TaskActivity(activity_name=u"支行长审批", task_assign_module='fabs.workflow.default', task_assign_function='subbranch_president_task', waiting=True)
        self.session.add(subbranch_president_task)
        set_parameter(subbranch_president_task, u"角色", u"支行行长")

        """
        超权限
        """
        # 并行
        ho_review_task = TaskActivity(activity_name=u"总行信贷审查", task_assign_module='fabs.workflow.default', task_assign_function='ho_review_task', waiting=True)


        ho_assessment_task = TaskActivity(activity_name=u"总行风险评价", task_assign_module='fabs.workflow.default', task_assign_function='ho_assessment_task', waiting=True)
        ho_riskowners_task= TaskActivity(activity_name=u"风险负责人审查", task_assign_module='fabs.workflow.default', task_assign_function='ho_riskowners_task', waiting=True)

        riskowners_review_task = TaskActivity(activity_name=u"信贷负责人审查", task_assign_module='fabs.workflow.default', task_assign_function='riskowners_review_task', waiting=True)

        bm_review_task = TaskActivity(activity_name=u"信贷分管行长审查", task_assign_module='fabs.workflow.default', task_assign_function='bm_review_task', waiting=True)

        committee_deliberation_task = TaskActivity(activity_name=u"总行信贷委员会审议", task_assign_module='fabs.workflow.default', task_assign_function='committee_deliberation_task', waiting=True)

        ho_president_task = TaskActivity(activity_name=u"总行行长审批", task_assign_module='fabs.workflow.default', task_assign_function='ho_president_task', waiting=True)



        start = StartActivity(activity_name=u"开始")

        self.session.add_all([lendingproposition_task, investigate_task, subbranch_assessment_task \
            , subbranch_review_task,   subbranch_deliberation_task, subbranch_president_task ])

        flow1 = Flow(from_activity=start, to_activity=lendingproposition_task, have_guard=False)

        #lendingproposition_task             贷款申请
        flow2 = Flow(from_activity=lendingproposition_task, to_activity=investigate_task, have_guard=False)

        #investigate_task                    预审
        #flow3 = Flow(from_activity=investigate_task, to_activity=subbranch_assessment_task, have_guard=False)

        #subbranch_assessment_task           支行风险评价
        #subbranch_review_task               支行审查
        #flow4 = Flow(from_activity=subbranch_assessment_task, to_activity=subbranch_review_task, have_guard=False)

        #subbranch_deliberation_task         支行审贷小组审议
        #flow5 = Flow(from_activity=subbranch_review_task, to_activity=subbranch_deliberation_task, have_guard=False)

        #investigate_task                    预审
        flow3 = Flow(from_activity=investigate_task, to_activity=subbranch_assessment_task, have_guard=False)
        flow4 = Flow(from_activity=investigate_task, to_activity=subbranch_review_task, have_guard=False)
        #                    |
        #                    V
        #subbranch_assessment_task           支行风险评价
        #subbranch_review_task               支行审查
        flow5 = Flow(from_activity=subbranch_assessment_task, to_activity=subbranch_deliberation_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='subbranch_assessment_gurad')
        flow6 = Flow(from_activity=subbranch_review_task, to_activity=subbranch_deliberation_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='subbranch_review_gurad')

        #subbranch_deliberation_task         支行审贷小组审议
        flow7 = Flow(from_activity=subbranch_deliberation_task, to_activity=subbranch_president_task, have_guard=True, guard_module='fabs.workflow.default', guard_function='subbranch_deliberation_guard')

        #subbranch_president_task            支行长审批
        end = EndActivity(activity_name=u"结束", waiting=True)
        flow8 = Flow(from_activity=subbranch_president_task, to_activity=end, have_guard=False)

        #ho_review_task                      总行信贷审查
        #ho_assessment_task                  总行风险评价
        #ho_riskowners_task                  风险负责人审查

        #riskowners_review_task              信贷负责人审查
        #bm_review_task                      信贷分管行长审查
        #committee_deliberation_task         总行信贷委员会审议
        #ho_president_task                   总行行长审批
        #flow11 = Flow(from_activity=subbranch_president_task, to_activity=ho_review_task, have_guard=False)
        #flow12 = Flow(from_activity=subbranch_president_task, to_activity=ho_assessment_task, have_guard=False)
        #flow13 = Flow(from_activity=ho_assessment_task, to_activity=ho_riskowners_task, have_guard=False)

        #flow14 = Flow(from_activity=ho_riskowners_task, to_activity=riskowners_review_task, have_guard=False)
        #flow15 = Flow(from_activity=ho_review_task, to_activity=riskowners_review_task, have_guard=False)

        #flow16 = Flow(from_activity=riskowners_review_task, to_activity=bm_review_task, have_guard=False)

        #flow17 = Flow(from_activity=bm_review_task, to_activity=committee_deliberation_task, have_guard=False)

        #flow18 = Flow(from_activity=committee_deliberation_task, to_activity=ho_president_task, have_guard=False)
        self.session.add_all([flow1,  flow2, flow3, flow4, flow5, flow6, flow7]) #, flow8])
        workflow = Workflow(workflow_name=u"贷款申请流程", start_activity = start)
        self.session.add_all([start, workflow])
        self.session.commit()


    def init_user_group(self):
        """
        USER SESSION
        """
        log.debug("start init user group !")
        auth_type = AuthenticationType(code=u'010001',name=u'LOGIN',description=u'LOGIN')
        self.session.add(auth_type)

        u1 = User(role_id=111,user_name=u'00530'); f1 = Password(user=u1,algorithm=u'MD5',credential=u'qwe123')
        u2 = User(role_id=112,user_name=u'00540'); f2 = Password(user=u2,algorithm=u'MD5',credential=u'qwe123')
        u3 = User(role_id=113,user_name=u'00550'); f3 = Password(user=u3,algorithm=u'MD5',credential=u'qwe123')
        u4 = User(role_id=114,user_name=u'00560'); f4 = Password(user=u4,algorithm=u'MD5',credential=u'qwe123')
        u5 = User(role_id=115,user_name=u'00570'); f5 = Password(user=u5,algorithm=u'MD5',credential=u'qwe123')
        u6 = User(role_id=116,user_name=u'00580'); f6 = Password(user=u6,algorithm=u'MD5',credential=u'qwe123')
        u7 = User(role_id=117,user_name=u'00590'); f7 = Password(user=u7,algorithm=u'MD5',credential=u'qwe123')
        self.session.add_all([f1,f2,f3,f4,f5,f6,f7])


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
        self.session.add_all([g1,g2,g3,g4,g5])
        self.session.add_all(
            [
                UserGroup(user=u1,group=g1),
                UserGroup(user=u2,group=g2),
                UserGroup(user=u3,group=g3),
                UserGroup(user=u4,group=g4),
                UserGroup(user=u5,group=g5),
                UserGroup(user=u6,group=g1),
                UserGroup(user=u7,group=g1)
            ]
        )
        self.session.commit()



    def init_customer(self):
        """
        Customer Info
        """
        logging.debug("start init customer info!")

        user = self.session.query(User).filter(User.user_name=="00530").first()


        man=Resident(name=u'张三', ric=u'330602197404040011', current_name = u'张三', gender=u'男性', birthday=datetime.datetime.now(), ethnicity =u'汉族', politics_status=u"中国共产党", marital_status=u"未婚")
        customer = Customer(party=man, cust_type="person")
        Certificate(party=man, cert_type=u'身份证', cert_no='330602197404040011', issue_date=datetime.datetime.now(), issue_office=u'xxx', thru_date = datetime.date(2055, 1, 1))

        man6=Resident(name=u'赵六', ric=u'330602197404040012', current_name=u'赵六', gender=u'男性', birthday=datetime.datetime.now(), ethnicity =u'汉族', politics_status=u"中国共产党", marital_status=u"已婚且有子女")
        customer6 = Customer(party=man6, cust_type="person")
        Certificate(party=man6, cert_type=u'身份证', cert_no='330602197404040012', issue_date=datetime.datetime.now(), issue_office=u'xxx', thru_date = datetime.date(2055, 1, 1))


        man2=Resident(name=u'李四', ric=u'330602197404040022', current_name=u'李四')
        customer2 = Customer(party=man2, cust_type="person")
        Certificate(party=man2, cert_type=u'身份证', cert_no='330602197404040012', issue_date=datetime.datetime.now(), issue_office=u'xxx', thru_date = datetime.date(2055, 1, 1))
        self.user = User(party = man2)
        self.session.add_all([self.user, customer, customer2, customer6])
        self.session.commit()

        d = datetime.datetime.now()
        operating_log = CustomerInfoOptLog(upto_date=d, log_date=d, register_user=user, comment="eeeeee")

        addr = Address(party= [customer.party], address=u"上海市长宁区")
        email = Email(party = [customer.party], email_address=u"yinsho@yinsho.com")
        phone = Phone(party = [customer.party], phone_type="手机", phone_number = "1888888888")
        phone2 = Phone(party = [customer.party], phone_type="手机1", phone_number = "109999999999")

        customer.party.ethnicity = u"汉族"
        man3=Resident(name=u'王五', ric=u'33060219740xxxxxx2', current_name=u'王五')

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

        pt21 = ProductType(code='21', name='房地产开发贷款', business_type='房地产开发业务')
        pt31 = ProductType(code='31', name='银团贷款', business_type='银团业务')
        pt41 = ProductType(code='41', name='委托贷款', business_type='委托贷款业务')

        pt51 = ProductType(code='51', name='展期及授信额度调整', business_type='展期及授信额度业务')

        self.session.add_all([pt01, pt02, pt03, pt04, pt11, pt12, pt21, pt31, pt41, pt51])

        self.session.add_all([
            Product(product_code="376", product_type=pt02, name="保费贷款",product_page='loanBaseInfo'),
            Product(product_code="379", product_type=pt04, name="保证担保贷款",product_page='loanBaseInfo'),
            Product(product_code="348", product_type=pt04, name="本行存单账户资金质押经营性",product_page='loanBaseInfo'),
            Product(product_code="352", product_type=pt04, name="本行存单账户资金质押经营性（卡）",product_page='loanBaseInfo'),
            Product(product_code="500", product_type=pt02, name="本行存单账户资金质押消费性",product_page='loanBaseInfo'),
            Product(product_code="501", product_type=pt02, name="本行存单账户资金质押消费性（卡）",product_page='loanBaseInfo'),
            Product(product_code="375", product_type=pt04, name="本行理财产品质押经营性",product_page='loanBaseInfo'),
            Product(product_code="502", product_type=pt02, name="本行理财产品质押消费性",product_page='loanBaseInfo'),
            # Product(product_code="503", product_type=pt  , name="承兑质押贷款"),
            Product(product_code="117", product_type=pt04, name="担保公司担保",product_page='guarantee'),
            Product(product_code="360", product_type=pt04, name="担保公司担保（卡）",product_page='guarantee'),
            Product(product_code="519", product_type=pt04, name="个人保证贷款",product_page='loanBaseInfo'),
            Product(product_code="102", product_type=pt01, name="个人第二套住房按揭",product_page='real_estate_development'),
            Product(product_code="114", product_type=pt03, name="个人下岗二次就业贷款",product_page='secondary_mortgage_loans'),
            Product(product_code="113", product_type=pt03, name="个人下岗再就业贷款",product_page='loanBaseInfo'),
            Product(product_code="504", product_type=pt03, name="个人下岗再就业贷款（卡）",product_page='loanBaseInfo'),
            Product(product_code="359", product_type=pt04, name="个人信用及保证（卡）保证担保",product_page='loanBaseInfo'),
            Product(product_code="505", product_type=pt04, name="个人信用及保证（卡）信用担保",product_page='loanBaseInfo'),
            Product(product_code="324", product_type=pt04, name="个人信用及保证贷款保证担保",product_page='loanBaseInfo'),
            Product(product_code="506", product_type=pt04, name="个人信用及保证贷款信用担保",product_page='loanBaseInfo'),
            Product(product_code="123", product_type=pt02, name="个人助学贷款",product_page='loanBaseInfo'),
            Product(product_code="101", product_type=pt01, name="个人住房按揭贷款",product_page='loanBaseInfo'),
            Product(product_code="377", product_type=pt02, name="惠民贷款",product_page='loanBaseInfo'),
            # Product(product_code="543", product_type=pt  , name="基准抵押贷款"),
            Product(product_code="507", product_type=pt04, name="经营性物业租金贷款（卡）保证担保",product_page='loanBaseInfo'),
            Product(product_code="508", product_type=pt04, name="经营性物业租金贷款（卡）抵押担保",product_page='loanBaseInfo'),
            Product(product_code="509", product_type=pt04, name="经营性物业租金贷款保证担保",product_page='loanBaseInfo'),
            Product(product_code="510", product_type=pt04, name="经营性物业租金贷款抵押担保",product_page='loanBaseInfo'),
            Product(product_code="354", product_type=pt04, name="卡授信其他有价单证质押",product_page='loanBaseInfo'),
            Product(product_code="353", product_type=pt04, name="卡授信账户资金质押",product_page='loanBaseInfo'),
            Product(product_code="515", product_type=pt04, name="买入贷款保证担保",product_page='loanBaseInfo'),
            Product(product_code="511", product_type=pt04, name="买入贷款抵押担保",product_page='loanBaseInfo'),
            Product(product_code="110", product_type=pt04, name="其他有价单证质押贷款",product_page='loanBaseInfo'),
            Product(product_code="542", product_type=pt04, name="其他有价单证质押经营性贷款",product_page='loanBaseInfo'),
            Product(product_code="512", product_type=pt04, name="其他有价单证质押经营性贷款（卡）",product_page='loanBaseInfo'),
            Product(product_code="513", product_type=pt02, name="其他有价单证质押消费性贷款",product_page='loanBaseInfo'),
            Product(product_code="514", product_type=pt02, name="其他有价单证质押消费性贷款（卡）",product_page='loanBaseInfo'),
            Product(product_code="521", product_type=pt11, name="企业保证贷款",product_page='loanBaseInfo'),
            Product(product_code="319", product_type=pt11, name="企业动产质押(50)",product_page='loanBaseInfo'),
            Product(product_code="365", product_type=pt11, name="企业动产质押（卡）",product_page='loanBaseInfo'),
            Product(product_code="374", product_type=pt11, name="企业信用及保证(卡)",product_page='loanBaseInfo'),
            Product(product_code="103", product_type=pt01, name="商用房按揭贷款",product_page='loanBaseInfo'),
            Product(product_code="104", product_type=pt01, name="商用房按揭贷款",product_page='loanBaseInfo'),
            Product(product_code="544", product_type=pt01, name="商用房按揭贷款（一次还本）",product_page='loanBaseInfo'),
            Product(product_code="330", product_type=pt04, name="商住房抵押及保证经营性50",product_page='loanBaseInfo'),
            Product(product_code="516", product_type=pt04, name="商住房抵押及保证经营性50（卡）",product_page='loanBaseInfo'),
            Product(product_code="331", product_type=pt04, name="商住房抵押及保证经营性55",product_page='loanBaseInfo'),
            Product(product_code="518", product_type=pt04, name="商住房抵押及保证经营性55（卡）",product_page='loanBaseInfo'),
            Product(product_code="332", product_type=pt04, name="商住房抵押及保证经营性60",product_page='loanBaseInfo'),
            Product(product_code="520", product_type=pt04, name="商住房抵押及保证经营性60（卡）",product_page='loanBaseInfo'),
            Product(product_code="333", product_type=pt04, name="商住房抵押及保证经营性65",product_page='loanBaseInfo'),
            Product(product_code="522", product_type=pt04, name="商住房抵押及保证经营性65（卡）",product_page='loanBaseInfo'),
            Product(product_code="523", product_type=pt02, name="商住房抵押及保证消费性50",product_page='loanBaseInfo'),
            Product(product_code="524", product_type=pt02, name="商住房抵押及保证消费性50（卡）",product_page='loanBaseInfo'),
            Product(product_code="525", product_type=pt02, name="商住房抵押及保证消费性55",product_page='loanBaseInfo'),
            Product(product_code="526", product_type=pt02, name="商住房抵押及保证消费性55（卡）",product_page='loanBaseInfo'),
            Product(product_code="527", product_type=pt02, name="商住房抵押及保证消费性60",product_page='loanBaseInfo'),
            Product(product_code="528", product_type=pt02, name="商住房抵押及保证消费性60（卡）",product_page='loanBaseInfo'),
            Product(product_code="529", product_type=pt02, name="商住房抵押及保证消费性65",product_page='loanBaseInfo'),
            Product(product_code="530", product_type=pt02, name="商住房抵押及保证消费性65（卡）",product_page='loanBaseInfo'),
            Product(product_code="531", product_type=pt03, name="小额下岗二次贷款",product_page='loanBaseInfo'),
            Product(product_code="361", product_type=pt03, name="小额下岗二次贷款（卡）",product_page='loanBaseInfo'),
            Product(product_code="125", product_type=pt11, name="小企业个人保证贷款",product_page='loanBaseInfo'),
            Product(product_code="372", product_type=pt11, name="小企业联保贷款",product_page='loanBaseInfo'),
            Product(product_code="517", product_type=pt11, name="一般担保保证贷款",product_page='loanBaseInfo'),
            Product(product_code="532", product_type=pt11, name="一般抵押贷款",product_page='loanBaseInfo'),
            Product(product_code="371", product_type=pt11, name="异地机器设备抵押30（卡）",product_page='loanBaseInfo'),
            Product(product_code="369", product_type=pt04, name="异地商房抵押55（卡）",product_page='loanBaseInfo'),
            Product(product_code="368", product_type=pt04, name="异地商房抵押60（卡）",product_page='loanBaseInfo'),
            Product(product_code="370", product_type=pt04, name="异地商房抵押65（卡）",product_page='loanBaseInfo'),
            Product(product_code="341", product_type=pt04, name="异地商用房抵押贷款50",product_page='loanBaseInfo'),
            Product(product_code="533", product_type=pt04, name="异地商用房抵押贷款50（卡）",product_page='loanBaseInfo'),
            Product(product_code="342", product_type=pt04, name="异地商用房抵押贷款55",product_page='loanBaseInfo'),
            Product(product_code="534", product_type=pt04, name="异地商用房抵押贷款55（卡）",product_page='loanBaseInfo'),
            Product(product_code="343", product_type=pt04, name="异地商用房抵押贷款60",product_page='loanBaseInfo'),
            Product(product_code="535", product_type=pt04, name="异地商用房抵押贷款60（卡）",product_page='loanBaseInfo'),
            Product(product_code="536", product_type=pt04, name="异地商用房抵押贷款65（卡）",product_page='loanBaseInfo'),
            Product(product_code="345", product_type=pt11, name="异地资产抵押贷款35",product_page='loanBaseInfo'),
            Product(product_code="537", product_type=pt11, name="异地资产抵押贷款35（卡）",product_page='loanBaseInfo'),
            Product(product_code="538", product_type=pt11, name="异地资产抵押贷款40",product_page='loanBaseInfo'),
            Product(product_code="539", product_type=pt11, name="异地资产抵押贷款40（卡）",product_page='loanBaseInfo'),
            Product(product_code="312", product_type=pt11, name="应收账款质押",product_page='loanBaseInfo'),
            Product(product_code="540", product_type=pt04, name="预抵押40-50以内",product_page='loanBaseInfo'),
            Product(product_code="367", product_type=pt04, name="预抵押40-50以内（卡）",product_page='loanBaseInfo'),
            Product(product_code="541", product_type=pt04, name="预抵押40以内",product_page='loanBaseInfo'),
            Product(product_code="366", product_type=pt04, name="预抵押40以内（卡）",product_page='loanBaseInfo'),
            Product(product_code="349", product_type=pt11, name="资产抵押30/50及保证",product_page='loanBaseInfo'),
            Product(product_code="362", product_type=pt11, name="资产抵押30/50及保证（卡）",product_page='loanBaseInfo'),
            Product(product_code="350", product_type=pt11, name="资产抵押35/55及保证",product_page='loanBaseInfo'),
            Product(product_code="363", product_type=pt11, name="资产抵押35/55及保证（卡）",product_page='loanBaseInfo'),
            Product(product_code="351", product_type=pt11, name="资产抵押40/60及保证",product_page='loanBaseInfo'),
            Product(product_code="364", product_type=pt11, name="资产抵押40/60及保证（卡）",product_page='loanBaseInfo'),

            Product(product_code="111", product_type=pt01, name="商用门脸店按揭贷款     ",product_page='loanBaseInfo'),
            Product(product_code="122", product_type=pt02, name="汽车个人消费贷款           ",product_page='car_consume'),
            Product(product_code="118", product_type=pt02, name="装饰装修个人消费贷款     ",product_page='personal_housing_decoration'),
            Product(product_code="119", product_type=pt02, name="旅游个人消费贷款      ",product_page='loanBaseInfo'),
            Product(product_code="121", product_type=pt02, name="耐用品个人消费贷款    ",product_page='loanBaseInfo'),
            Product(product_code="225", product_type=pt02, name="狮卡授信消费贷款",product_page='loanBaseInfo'),
            Product(product_code="330_1", product_type=pt11, name="商住房抵押及保证经营性50",product_page='loanBaseInfo'),
            Product(product_code="516_1", product_type=pt11, name="商住房抵押及保证经营性50（卡）",product_page='loanBaseInfo'),
            Product(product_code="331_1", product_type=pt11, name="商住房抵押及保证经营性55",product_page='loanBaseInfo'),
            Product(product_code="518_1", product_type=pt11, name="商住房抵押及保证经营性55（卡）",product_page='loanBaseInfo'),
            Product(product_code="332_1", product_type=pt11, name="商住房抵押及保证经营性60",product_page='loanBaseInfo'),
            Product(product_code="520_1", product_type=pt11, name="商住房抵押及保证经营性60（卡）",product_page='loanBaseInfo'),
            Product(product_code="333_1", product_type=pt11, name="商住房抵押及保证经营性65",product_page='loanBaseInfo'),
            Product(product_code="522_1", product_type=pt11, name="商住房抵押及保证经营性65（卡）",product_page='loanBaseInfo'),
            Product(product_code="369_1", product_type=pt11, name="异地商房抵押55（卡）",product_page='loanBaseInfo'),
            Product(product_code="368_1", product_type=pt11, name="异地商房抵押60（卡）",product_page='loanBaseInfo'),
            Product(product_code="370_1", product_type=pt11, name="异地商房抵押65（卡）",product_page='loanBaseInfo'),
            Product(product_code="341_1", product_type=pt11, name="异地商用房抵押贷款50",product_page='loanBaseInfo'),
            Product(product_code="533_1", product_type=pt11, name="异地商用房抵押贷款50（卡）",product_page='loanBaseInfo'),
            Product(product_code="342_1", product_type=pt11, name="异地商用房抵押贷款55",product_page='loanBaseInfo'),
            Product(product_code="534_1", product_type=pt11, name="异地商用房抵押贷款55（卡）",product_page='loanBaseInfo'),
            Product(product_code="343_1", product_type=pt11, name="异地商用房抵押贷款60",product_page='loanBaseInfo'),
            Product(product_code="535_1", product_type=pt11, name="异地商用房抵押贷款60（卡）",product_page='loanBaseInfo'),
            Product(product_code="536_1", product_type=pt11, name="异地商用房抵押贷款65（卡）",product_page='loanBaseInfo'),
            Product(product_code="540_1", product_type=pt11, name="预抵押40-50以内",product_page='loanBaseInfo'),
            Product(product_code="367_1", product_type=pt11, name="预抵押40-50以内（卡）",product_page='loanBaseInfo'),
            Product(product_code="541_1", product_type=pt11, name="预抵押40以内",product_page='loanBaseInfo'),
            Product(product_code="366_1", product_type=pt11, name="预抵押40以内（卡）",product_page='loanBaseInfo'),
            Product(product_code="507_1", product_type=pt11, name="经营性物业租金贷款（卡）保证担保",product_page='loanBaseInfo'),
            Product(product_code="508_1", product_type=pt11, name="经营性物业租金贷款（卡）抵押担保",product_page='loanBaseInfo'),
            Product(product_code="509_1", product_type=pt11, name="经营性物业租金贷款保证担保",product_page='loanBaseInfo'),
            Product(product_code="510_1", product_type=pt11, name="经营性物业租金贷款抵押担保",product_page='loanBaseInfo'),
            Product(product_code="354_1", product_type=pt11, name="卡授信其他有价单证质押",product_page='loanBaseInfo'),
            Product(product_code="353_1", product_type=pt11, name="卡授信账户资金质押",product_page='loanBaseInfo'),
            Product(product_code="110_1", product_type=pt11, name="其他有价单证质押贷款",product_page='loanBaseInfo'),
            Product(product_code="542_1", product_type=pt11, name="其他有价单证质押经营性贷款",product_page='loanBaseInfo'),
            Product(product_code="512_1", product_type=pt11, name="其他有价单证质押经营性贷款（卡）",product_page='loanBaseInfo'),
            Product(product_code="348_1", product_type=pt11, name="本行存单账户资金质押经营性",product_page='loanBaseInfo'),
            Product(product_code="352_1", product_type=pt11, name="本行存单账户资金质押经营性（卡）",product_page='loanBaseInfo'),
            Product(product_code="375_1", product_type=pt11, name="本行理财产品质押经营性",product_page='loanBaseInfo'),
            Product(product_code="379_1", product_type=pt11, name="保证担保贷款",product_page='loanBaseInfo'),
            Product(product_code="117_1", product_type=pt11, name="担保公司担保",product_page='loanBaseInfo'),
            Product(product_code="360_1", product_type=pt11, name="担保公司担保（卡）",product_page='loanBaseInfo'),
            Product(product_code="515_1", product_type=pt11, name="买入贷款保证担保",product_page='loanBaseInfo'),
            Product(product_code="511_1", product_type=pt11, name="买入贷款抵押担保",product_page='loanBaseInfo'),
            Product(product_code="189", product_type=pt11, name="卡授信厂房设备抵押10%",product_page='loanBaseInfo'),
            Product(product_code="007", product_type=pt11, name="银行承兑汇票",product_page='acceptance_draft'),
            Product(product_code="008", product_type=pt11, name="银行承兑汇票质押",product_page='loanBaseInfo'),
            Product(product_code="301", product_type=pt51, name="授信额度申请",product_page='loanBaseInfo'),
            Product(product_code="302", product_type=pt51, name="追加授信额度申请",product_page='loanBaseInfo'),
            Product(product_code="150", product_type=pt51, name="对私贷款展期",product_page='loanBaseInfo'),
            Product(product_code="140", product_type=pt51, name="对私授信额度调整",product_page='loanBaseInfo'),
            Product(product_code="701", product_type=pt11, name="财政贴现",product_page='financial_discount'),
            Product(product_code="702", product_type=pt11, name="出口发票融资",product_page='invoice_discounting'),
            Product(product_code="703", product_type=pt11, name="出口托收押汇",product_page='export_collection'),
            Product(product_code="704", product_type=pt11, name="出口押汇",product_page='bill_purchased'),
            Product(product_code="705", product_type=pt11, name="对公-打包贷款",product_page='packaged_loans'),
            Product(product_code="730", product_type=pt11, name="对公—贷款承诺",product_page='loan_commitment'),
            Product(product_code="706", product_type=pt11, name="对公-国内保函",product_page='domestic_detterguarantee'),
            Product(product_code="707", product_type=pt11, name="对公-进口代收押汇",product_page='import__collecting_documentary'),
            Product(product_code="708", product_type=pt11, name="对公-进口押汇表",product_page='import_trade'),
            Product(product_code="709", product_type=pt11, name="对公-开立信用证",product_page='open_ic'),
            Product(product_code="710", product_type=pt11, name="对公-流动资金贷款",product_page='liquidity'),
            Product(product_code="711", product_type=pt11, name="对公-买入票据（福费庭）",product_page='bill_purchased'),
            Product(product_code="712", product_type=pt11, name="对公-贴现-发票详细清单",product_page='invoice_detailed_list'),
            Product(product_code="713", product_type=pt11, name="对公-贴现-票据详细清单",product_page='paper_detailed_list'),
            Product(product_code="714", product_type=pt11, name="对公-委托贷款",product_page='entrusted_loans'),
            Product(product_code="715", product_type=pt11, name="对公-项目贷款表",product_page='project_loan'),
            Product(product_code="716", product_type=pt11, name="对公-最高额贷款",product_page='maximum_loan'),
            Product(product_code="717", product_type=pt04, name="对私-个人经营性贷款",product_page='personal_busines_loans'),
            Product(product_code="718", product_type=pt04, name="对私-个人其他消费贷款",product_page='other_individual_consumption'),
            Product(product_code="719", product_type=pt04, name="对私-个人透支额度",product_page='personal_overdraft'),
            Product(product_code="720", product_type=pt04, name="对私-个人委托贷款",product_page='individual_entrust_loans'),
            Product(product_code="721", product_type=pt04, name="对私-个人住房消费贷款",product_page='house_consume'),
            Product(product_code="722", product_type=pt04, name="对私-公积金按揭贷款",product_page='accumulation_mortgage_loans'),
            Product(product_code="723", product_type=pt04, name="对私-国家助学贷款",product_page='national_student_loan'),
            Product(product_code="724", product_type=pt04, name="对私-商业助学贷款",product_page='commercials_tudent_loans'),
            Product(product_code="725", product_type=pt04, name="对私-一手房按揭贷款",product_page='housing_mortgage_loans'),
            Product(product_code="726", product_type=pt11, name="国际保函",product_page='international_letter_guarantee'),
            Product(product_code="727", product_type=pt11, name="商业承兑汇票贴现",product_page='business_acceptance_draft_discount'),
            Product(product_code="728", product_type=pt11, name="提货担保",product_page='delivery_guarantee'),
            Product(product_code="729", product_type=pt11, name="银行承兑汇票贴现",product_page='acceptance_draft_discount'),
        ])
        self.session.commit()


    def tearDown(self):
        #self.session.rollback()
        #Base.metadata.drop_all(self.session.bind)
        logging.debug("finish!!!")

