# -*- coding: utf-8 -*-
"""
    yinsho.services.CustomerService
    #####################

    yinsho CustomerService module
"""
import hashlib, copy
from flask import json, g
from ..model.customer import *
from ..model.party import *
from ..model.user import *
from ..model.common import *
from .service import BaseService
from datetime import datetime
from ..base import core_inf
class CustomerService(BaseService):
    __model__ = User


    def queryroleparty(self,**kwargs):
        u''' 组织机构查询判断 '''
        print kwargs
        branch_code=kwargs.get('branch_code')
        rst={}
        q = g.db_session.query(Party).join(PartyRole,Party.id==PartyRole.party_id).filter(PartyRole.branch_code == branch_code)
        resi = q.filter(Party.type_code == 'resident').limit(10).all()
        print resi
        comps = q.filter(Party.type_code == 'company').limit(10).all()
        print comps
        resi.extend(comps)
        rst.update({'party':resi})
        return rst

    def create_customer(self, **kwargs):
        u''' 创建客户 '''
        cust = kwargs.get('customer')
        cert = kwargs.get(u'certificate')
        if cert.get('cert_type')==u'身份证' or cert.get('cert_type') == u'51':
            cust.update({'ric':cert.get('cert_no'),\
                         'birthday':datetime.strptime(cust.get('birthday'),'%Y-%m-%d')})
            resident=Resident(**cust)
            customer=Customer(party=resident, cust_type="person")
            #g.db_session.add(customer)
            certification=Certificate(party=resident, cert_type=cert.get('cert_type'), cert_no=cert.get('cert_no'))
            g.db_session.add(certification)
            academic = AcademicRecord(customer=customer,**kwargs.get('academic'))
            emp = EmploymentRecord(customer=customer,**kwargs.get('emp'))
            family = FamilyRecord(customer=customer,**kwargs.get('family'))
            g.db_session.add_all([academic,emp,family])

        g.db_session.commit()

    def query_customers(self, customer_name=None, certificate_number=None):
        u''' 查询客户列表 '''
        q = g.db_session.query(Customer).join(Customer.party).join(Party.certificates)
        if bool(customer_name[0]): q = q.filter(Party.name.like(u'%'+customer_name[0]+'%'))
        if bool(certificate_number): q = q.filter(Party.ric == certificate_number)
        rtn_data = []
        count = 0 # 临时改动 因为数据导过来太多,先只显示几个试试
        for cust in q.all():
            rtn_data.append({'party':cust.party, 'cust_info':cust, 'certificate':cust.party.certificates})
            count = count + 1
            if count > 7:
                break;

        return rtn_data

    def query_customer(self, customer_id):
        u''' 查询单个客户信息 '''
        customer = g.db_session.query(Customer).filter(Customer.party_id == customer_id).first()
        emp = g.db_session.query(EmploymentRecord).filter(EmploymentRecord.customer_id == customer.role_id).first()
        #academic = g.db_session.query(AcademicRecord).filter(AcademicRecord.customer_id == customer.role_id).first()
        family = g.db_session.query(FamilyRecord).filter(FamilyRecord.customer_id == customer.role_id).first()
        per_bus = g.db_session.query(PersonalBusiness).filter(PersonalBusiness.customer_id == customer.role_id).first()
        per_card = g.db_session.query(PersonalCard).filter(PersonalCard.customer_id == customer.role_id).first()
        #customerSocialInsurance = g.db_session.query(CustomerSocialInsurance).filter(CustomerSocialInsurance.customer_id == customer.role_id).first()
        party = customer.party
        certificate = party.certificates[0]
        contact=party.contact
        #,'customerSocialInsurance':customerSocialInsurance
        rtn = {'customer':party,'emp':emp,'family':family,'certificate':certificate,'per_card':per_card,'per_bus':per_bus,'contact':contact}
        return rtn

    def update_customer(self, customer_id, **kwargs):
        u''' 更新客户信息 '''
        # base issue
        cust = kwargs.get('customer')
        cert = kwargs.get('certificate')
        emp = kwargs.get('emp')
        family = kwargs.get('family')
        per_card = kwargs.get('per_card')
        per_bus = kwargs.get('per_bus')
        telephone = kwargs.get('telephone')
        mobile_phone = kwargs.get('mobile_phone')
        state = {'state':u'完善'}
        g.db_session.query(Party).filter(Party.id == customer_id).update(state)
        # 基本信息
        birthday = datetime.strptime(cust.get('birthday') or '1999-10-10', u"%Y-%m-%d")
        cust.update({'ric':cert.get('cert_no'), 'birthday':birthday})
        party_id = cust.get('id')
        #cust.pop('id')
        for k in cust.keys():
            if cust.get(k) in [[],None]:
                cust.pop(k)
        if cust.get('type_code'):
            cust.pop('type_code')
        if cust.get('no'):
            cust.pop('no')
        if cust.get('state'):
            cust.pop('state')
        print cust
        #cust.pop('id_1')
        current_name = cust.get('name')
        cust.pop('name')
        cust.update({'current_name':current_name})
        g.db_session.query(Resident).filter(Resident.id == customer_id).update(cust)

        #证件信息
        cert_id = cert.get('id')
        cert.pop('id')
        cert.pop('party')
        cert.pop('party_id')
        thru_date = datetime.strptime(cert.get('thru_date') or '1999-10-10', u"%Y-%m-%d")
        cert.update({'thru_date':thru_date})
        issue_date = datetime.strptime(cert.get('issue_date') or '1999-10-10', u"%Y-%m-%d")
        cert.update({'issue_date':issue_date})
        g.db_session.query(Certificate).filter(Certificate.id == cert_id).update(cert)

        #工作信息
        emp_id = emp.get('id')
        emp.pop('id')
        emp.pop('customer_id')
        emp.pop('customer')
        begin_job_date =emp.get('begin_job_date')
        if begin_job_date:
            begin_job_date = datetime.strptime(begin_job_date, u"%Y-%m-%d")
        end_date = emp.get('end_date')
        if end_date:
            end_date = datetime.strptime(end_date, u"%Y-%m-%d")
        if emp.get('monthly_income') != None:
            monthly_income = int(emp.get('monthly_income'))
        g.db_session.query(EmploymentRecord).filter(EmploymentRecord.id ==emp_id).update(emp)
        #家庭信息
        family_id = family.get('id')
        family.pop('id')
        family.pop('customer_id')
        family.pop('customer')
        if family.get('house_area') != None:
            house_area = int(family.get('house_area'))
        if family.get('family_year_income') != None:
            family_year_income = int(family.get('family_year_income'))
        if family.get('family_number') != None:
            family_number = int(family.get('family_number'))
        if family.get('family_fixed_assets') != None:
            family_fixed_assets = int(family.get('family_fixed_assets'))
        g.db_session.query(FamilyRecord).filter(FamilyRecord.id == family_id).update(family)

        per_bus_id = per_bus.get('id')
        per_bus.pop('id')
        per_bus.pop('customer_id')
        per_bus.pop('customer')
        g.db_session.query(PersonalBusiness).filter(PersonalBusiness.id == per_bus_id).update(per_bus)

        per_card_id = per_card.get('id')
        per_card.pop('id')
        per_card.pop('customer_id')
        per_card.pop('customer')
        g.db_session.query(PersonalCard).filter(PersonalCard.id == per_card_id).update(per_card)

        telephone_id = telephone.get('id')
        telephone.pop('id')
        telephone.pop('party')
        telephone.pop('type_code')
        g.db_session.query(Phone).filter(Phone.id == telephone_id).update(telephone)

        mobile_phone_id = mobile_phone.get('id')
        mobile_phone.pop('id')
        mobile_phone.pop('party')
        mobile_phone.pop('type_code')
        g.db_session.query(Phone).filter(Phone.id == mobile_phone_id).update(mobile_phone)

        g.db_session.commit()
    def delete_customer(self, customer_id):
        u''' 删除客户信息 '''
        g.db_session.query(Resident).filter(Resident.id == customer_id).delete()
        g.db_session.commit()

    def create_academic_record(self, **kwargs):
        u''' 创建客户学历履历信息 '''
        academic = kwargs.get('academic')
        g.db_session.add(AcademicRecord(**academic))
        g.db_session.commit()

    def query_academic_record(self, customer_id, record_id=None):
        u''' 查询客户学历履历信息 '''
        q = g.db_session.query(AcademicRecord).join(AcademicRecord.customer)
        if bool(customer_id):
            q = q.filter(Customer.role_id == customer_id)
        if bool(record_id):
            q = q.filter(AcademicRecord.id == record_id)

        rtn_data = [a for a in q.all()]
        return rtn_data
    def create_person_customer(self, **kwargs):
        u''' 创建个人客户 '''
        branch_code=kwargs.get('branch_code')
        cert_no = kwargs.get('cert_no1')
        cert_type = kwargs.get('cert_type')
        cust_name = kwargs.get('name')
        state = kwargs.get('state')
        cust_rel = g.db_session.query(Role).join(Resident,Role.party_id == Resident.id).filter(Role.type_code=='customer').filter(Resident.ric == cert_no).first()
        if cust_rel:
            u'''新增个人客户信息添加关联部分'''
            p=g.db_session.query(Party).filter(Party.id == cust_rel.party.id).first()
            roleparty=PartyRole(branch_code=branch_code,party=p)
            g.db_session.add(roleparty)
            
            return {'success':{'state':u'客户存在'}} 
       
        res = Resident(name=cust_name,
                       ric=cert_no,
                       state=state
                       )

        phone = Phone(phone_type = u'电话号码')
        res.contact.append(phone)

        mobile = Phone(phone_type = u'手机号码')
        res.contact.append(mobile)
        g.db_session.add(res)
        cert = Certificate(cert_type=cert_type,cert_no=cert_no,party=res)
        cust = Customer(party=res,cust_type='person')
        # 年收入 类型 biginter
        family = FamilyRecord(customer=cust)
        g.db_session.add(family)
        #工作年限
        emp = EmploymentRecord(customer=cust)
        g.db_session.add(emp)
        per_card = PersonalCard(customer=cust)
        per_bus = PersonalBusiness(customer=cust)
        g.db_session.add_all([per_bus,per_card]);
        g.db_session.flush()
        u'''新增个人客户信息添加关联部分'''
        p=g.db_session.query(Party).filter(Party.id == res.id).first()
        roleparty=PartyRole(branch_code=branch_code,party=p)
        g.db_session.add(roleparty)

        
        """
        branch_code=kwargs.get('branch_code')
        asso_map={'socialInsurance':Directors,
                  'principal':PrincipalPerson,
                  'companyStruct':CompStructure,
                  'controlledCompany':branchInfo,
                  'investmentManagement':customerCommInvest,
                  'capitalStructure':customerCommCapital,
                  'clientCurriculum':customerDoc,
                  'spouseInfo':FamilyRelation,
                  'famrelation':FamilyRelation}
        cert_no = kwargs.get('cert_no1')
        cert_type = kwargs.get('cert_type')
        cust_name = kwargs.get('name')
        associate = kwargs.get('associate')
        party_id = kwargs.get('party_id')
        state = kwargs.get('state')

        cust_rel = g.db_session.query(Role).join(Resident,Role.party_id == Resident.id).filter(Role.type_code=='customer').filter(Resident.ric == cert_no).first()
        if cust_rel:
            if associate:
                ass = asso_map[associate]
                cust = g.db_session.query(Customer).join(Party,Customer.party_id == Party.id).filter(Party.id==party_id).first()
                if associate == "spouseInfo":
                    g.db_session.add(ass(customer=cust,customer_rel=cust_rel,cust_rela='配偶'))
                if associate != "spouseInfo":
                    g.db_session.add(ass(customer=cust,customer_rel=cust_rel))
                g.db_session.commit()
            u'''新增个人客户信息添加关联部分'''
            
            p=g.db_session.query(Party).filter(Party.no == cust_rel.party.no).first()
            roleparty=PartyRole(branch_code=branch_code,party=p)
            g.db_session.add(roleparty)
            
            return {'success':{'cust_no':cust_rel.party.no}} 
        rt = core_inf.trans120199(cert_no,cust_name)
        if int(rt.get('code')) != 0:
            return {'error':rt.get('reason')}
        birthday=rt.get(u'出生日期')
        if birthday:
            birthday = datetime.strptime(birthday,'%Y%m%d')
        res = Resident(marital_status=rt.get(u'婚姻状况'),
                       gender=rt.get(u'性别'),
                       name=cust_name,
                       no=rt.get(u'客户编号'),
                       education=rt.get(u'学历'),
                       ethnicity=rt.get(u'民族'),
                       birthday=birthday,
                       birth_place=rt.get(u'籍贯'),
                       ric=cert_no,
                       state=state
                       )

        phone = Phone( phone_number=rt.get(u'电话号码'),
                       phone_type = u'电话号码')
        res.contact.append(phone)

        mobile = Phone(phone_number=rt.get(u'手机号码'),
                       phone_type = u'手机号码')
        res.contact.append(mobile)
        g.db_session.add(res)
        thru = rt.get(u'证件到期日期')
        if thru:
            thru = datetime.strptime(thru,'%Y%m%d')
        cert = Certificate(cert_type=cert_type,cert_no=cert_no,thru_date=thru,party=res)
        cust = Customer(party=res,cust_type='person')
        # 年收入 类型 biginter
        family = FamilyRecord(family_year_income=rt.get(u'家庭年收入'),
                                main_source=rt.get(u'主要收入来源'),
                                family_address=rt.get(u'地址'),
                                customer=cust)
        g.db_session.add(family)
        #工作年限
        emp = EmploymentRecord(headship=rt.get(u'当前职位'),company=rt.get(u'工作单位'),customer=cust)
        g.db_session.add(emp)
        per_card = PersonalCard(customer=cust)
        per_bus = PersonalBusiness(customer=cust)
        g.db_session.add_all([per_bus,per_card]);
        if associate:
            ass = asso_map[associate]
            own = g.db_session.query(Customer).join(Party,Customer.party_id == Party.id).filter(Party.id==party_id).first()
            #part = g.db_session.query(Party).filter(Party.id==party_id).first()
            g.db_session.add(ass(customer=own,customer_rel=cust))
        g.db_session.commit()
        p_no=rt.get(u'客户编号')
        u'''新增个人客户信息添加关联部分'''
        p=g.db_session.query(Party).filter(Party.no == p_no).first()
        roleparty=PartyRole(branch_code=branch_code,party=p)
        g.db_session.add(roleparty)
        """
            
        return {'success':{'state':u'增加成功','cust_id':res.id}}

    def query_person(self, customer_id):
        u''' 查询单个客户信息 '''
        customer = g.db_session.query(Customer).filter(Customer.party_id == customer_id).first()
        emp = g.db_session.query(EmploymentRecord).filter(EmploymentRecord.customer_id == customer.role_id).first()
        academic = g.db_session.query(AcademicRecord).filter(AcademicRecord.customer_id == customer.role_id).first()
        family = g.db_session.query(FamilyRecord).filter(FamilyRecord.customer_id == customer.role_id).first()
        customerSocialInsurance = g.db_session.query(CustomerSocialInsurance).filter(CustomerSocialInsurance.customer_id == customer.role_id).first()
        party = customer.party
        certificate = party.certificates[0]
        contact=party.contact
        #,'customerSocialInsurance':customerSocialInsurance
        rtn = {'customer':party,'emp':emp,'academic':academic,'family':family,'certificate':certificate,'contact':contact}
        return rtn

    def create_company_customer(self, **kwargs):
        u''' 创建对公客户 '''
        com_no = kwargs.get('org_id1')
        com_credit_no = kwargs.get('credit_no')
        com_name = kwargs.get('name')
        reg_check_result = kwargs.get('reg_check_result')
        branch_code=kwargs.get('branch_code')
        state = '暂存'
        cust_rel = g.db_session.query(Role).join(Company,Role.party_id == Company.id).filter(Role.type_code=='customer').filter(Company.org_id == com_no).first()
        if cust_rel:
            u'''新增对公客户信息添加关联部分'''
            p=g.db_session.query(Party).filter(Party.id == cust_rel.party.id).first()
            roleparty=PartyRole(branch_code=branch_code,party=p)
            g.db_session.add(roleparty)
            return {'success':{'state':u'客户存在'}}
        company = Company(name = com_name,
            org_id = com_no,
            state = state,
            company_cn_name = com_name,
            )
        cust = Customer(party=company, cust_type="company")
        g.db_session.add(cust);
        g.db_session.flush()
        u'''新增个人客户信息添加关联部分'''
        p=g.db_session.query(Party).filter(Party.id == company.id).first()
        roleparty=PartyRole(branch_code=branch_code,party=p)
        g.db_session.add(roleparty)

        """
        branch_code=kwargs.get('branch_code')
        asso_map={'socialInsurance':Directors,
                  'principal':PrincipalPerson,
                  'companyStruct':CompStructure,
                  'controlledCompany':branchInfo,
                  'investmentManagement':customerCommInvest,
                  'capitalStructure':customerCommCapital,
                  'clientCurriculum':customerDoc}

        com_no = kwargs.get('org_id1')
        com_credit_no = kwargs.get('credit_no')
        com_name = kwargs.get('name')
        reg_check_result = kwargs.get('reg_check_result')
        associate = kwargs.get('associate')
        party_id = kwargs.get('party_id')
        state = '暂存'
        cust_rel = g.db_session.query(Role).join(Company,Role.party_id == Company.id).filter(Role.type_code=='customer').filter(Company.org_id == com_no).first()
        if cust_rel:
            if associate:
                ass = asso_map[associate]
                cust = g.db_session.query(Customer).join(Party,Customer.party_id == Party.id).filter(Party.id==party_id).first()
                g.db_session.add(ass(customer=cust,customer_rel=cust_rel))
                g.db_session.commit()
            u'''新增对公客户信息添加关联部分'''
            p=g.db_session.query(Party).filter(Party.no == cust_rel.party.no).first()
            roleparty=PartyRole(branch_code=branch_code,party=p)
            g.db_session.add(roleparty)
            return {'success':{'cust_no':cust_rel.party.no}}

        rt =core_inf.trans120197(com_no,com_name)
        if int(rt.get('code')) != 0:
            return {'error':rt.get('reason')}
        #reg_thru_date = rt.get(u'注册日期')
        #if reg_thru_date:
           # reg_thru_date = datetime.strptime(reg_thru_date,'%Y%m%d')
        if com_credit_no != None:
            tmp = com_no
            com_no = com_credit_no
            com_credit_no = tmp
        company = Company(no = rt.get(u'客户编号'),
            name = com_name,
            company_en_name = rt.get(u'英文名称'),
            #reg_thru_date = reg_thru_date,
            reg_thru_date = rt.get(u'注册日期'),
            reg_state = rt.get(u'注册地代码'),
            company_type = rt.get(u'机构性质'),
            company_kind = rt.get(u'组织形式'),
            industry_class = rt.get(u'行业类别门'),
            industry_large_class = rt.get(u'行业类别大类'),
            industry_small_class = rt.get(u'行业类别中类'),
            industry_mid_class = rt.get(u'行业类别小类'),
            ownership_pattern = rt.get(u'所有制性质'),
            opt_scope = rt.get(u'主营业务范围'),
            reg_amount = int(rt.get(u'注册资本')),
            paid_amount = rt.get(u'实收资本'),
            paid_cur_type = rt.get(u'资本币种'),
            corp_type = rt.get(u'组织机构类别'),
            corp_type_detail = rt.get(u'组织类别细分'),
            corp_type_no = rt.get(u'组织机构类别代码'),
            total_employee = rt.get(u'员工数目'),
            company_status = rt.get(u'机构状态'),
            account_status = rt.get(u'基本户状态'),
            account_approval_no = rt.get(u'基本户开户许可证号'),
            company_holding_type = rt.get(u'企业控股类型'),
            company_capital = rt.get(u'企业规模'),
            reg_phone = rt.get(u'手机号码'),
            phone= rt.get(u'电话号码'),
            reg_address = rt.get(u'注册地址'),
            loc_tax_id = rt.get(u'纳税人识别号（地税）'),
            nat_tax_id = rt.get(u'纳税人识别号（国税）'),
            org_id = com_no,
            state = state,
            company_cn_name = com_name,
            company_reg_id = com_credit_no)
        cust = Customer(party=company, cust_type="company")
        g.db_session.add(cust);
        if associate:
            ass = asso_map[associate]
            own = g.db_session.query(Customer).join(Party,Customer.party_id == Party.id).filter(Party.id==party_id).first()
            #part = g.db_session.query(Party).filter(Party.id==party_id).first()
            g.db_session.add(ass(customer=own,customer_rel=cust))

        g.db_session.commit()
        u'''新增个人客户信息添加关联部分'''
        p_no=rt.get(u'客户编号')
        p=g.db_session.query(Party).filter(Party.no == p_no).first()
        roleparty=PartyRole(branch_code=branch_code,party=p)
        g.db_session.add(roleparty)
        """
        return {'success':{'state':u'增加成功','cust_id':company.id}}

    def query_company_customers(self, customer_name=None):
        u''' 查询对公客户列表 '''
        q = g.db_session.query(Customer).join(Customer.party).filter(Customer.cust_type == 'company')
        if customer_name and  bool(customer_name[0]): q = q.filter(Party.name.like(u'%'+customer_name[0]+'%'))

        rtn_data = []
        count = 0 # 临时改动 因为数据导过来太多,先只显示几个试试
        for cust in q.all():
            rtn_data.append({'party':cust.party, 'cust_info':cust,'certificate':[{'cert_no':cust.party.org_id,'cert_type':u'组织机构代码'}]})
            count = count + 1
            if count > 7:
                break;

        #rtn_data = [{'party':cust.party, 'cust_info':cust} for cust in q.all() ]
        #rtn_data = [{'party':cust.party, 'cust_info':cust,'certificate':[{'cert_no':cust.party.org_id,'cert_type':u'组织机构代码'}]} for cust in q.all() ]
        return rtn_data

    def query_company_customer(self, customer_id):
        u''' 查询单个客户信息 '''
        customer = g.db_session.query(Customer).filter(Customer.party_id == customer_id).first()
        cp = customer.party
        #不可删除
        mmm = cp.company_cn_name
        rtn = cp.__dict__
        if rtn.get('_sa_instance_state'):
            rtn.pop('_sa_instance_state')
        return rtn

    def update_company_customer(self,customer_id,**kwargs):
        state = {'state':u'完善'}
        g.db_session.query(Party).filter(Party.id == customer_id).update(state)
        cust=kwargs
        cust.pop('type_code')
        cust.pop('name')
        cust.pop('no')
        cust.pop('state')
        if cust.get('state'):cust.pop('state')
        if cust.get('from_party'): cust.pop('from_party')
        if cust.get('to_party'):cust.pop('to_party')
        if cust.get('contact'): cust.pop('contact')
        if cust.get('role'): cust.pop('role')
        if cust.get('certificates'):cust.pop('certificates')
        if cust.get('application_transaction'):cust.pop('application_transaction')
        g.db_session.query(Company).filter(Company.id == customer_id).update(cust)
        g.db_session.commit()

    def query_customer_relation(self,**kwargs):
        pass
    def query_persons(self,custNo=None, custName=None, certType=None, certNo=None):

        empty=['null','','undefined']
        if custNo and custNo[0] in empty:
            custNo = None
        if custName and custName[0] in empty:
            custName = None
        if certNo and certNo[0] in empty:
            certNo = None

        #含有客户编号
        if(custNo):
            party = g.db_session.query(Party).filter(Party.no==custNo[0]).first()
            if not party:
                return []
            cust = party.role
            cert =party.certificates[0]
            return [{'party':party,'cust_info':cust,'certificate':cert}]

        q = g.db_session.query(Customer).join(Customer.party).join(Party.certificates)
        if bool(custName): q = q.filter(Party.name.like('%'+custName[0]+'%'))
        if bool(certNo): q = q.filter(Certificate.cert_no == certNo[0])
        rtn_data = [{'party':cust.party, 'cust_info':cust, 'certificate':cust.party.certificates[0]} for cust in q.all() ]
        return rtn_data
    def query_companys(self,custNo=None, custName=None, certType=None, certNo=None):

        empty=['null','','undefined']
        if custNo and custNo[0] in empty:
            custNo = None
        if custName and custName[0] in empty:
            custName = None
        if certNo and certNo[0] in empty:
            certNo = None

        #含有客户编号
        if(custNo):
            party = g.db_session.query(Party).filter(Party.no==custNo[0]).first()
            if not party:
                return []
            cust = party.role
            # 还差信用证
            cert = {'cert_type':'组织机构代码证','cert_no':party.org_id}
            return [{'party':party,'cust_info':cust,'certificate':cert}]

        q = g.db_session.query(Customer).join(Company,Customer.party_id == Company.id).filter(Customer.cust_type=='company')
        if bool(custName):
            q = q.filter(Company.company_cn_name.like('%'+custName[0]+'%'))

        if bool(certNo):
            q = q.filter(Company.org_id == certNo[0].strip() )

        rtn_data = [{'party':cust.party, 'cust_info':cust, 'certificate':{'cert_type':'组织机构代码证','cert_no':cust.party.org_id}} for cust in q.all() ]
        return rtn_data

    def query_asso(self,cust_id,asso):

        asso_map={'socialInsurance':Directors,
                  'principal':PrincipalPerson,
                  'companyStruct':CompStructure,
                  'controlledCompany':branchInfo,
                  'investmentManagement':customerCommInvest,
                  'capitalStructure':customerCommCapital,
                  'clientCurriculum':customerDoc}
        if asso:
            asso = asso[0]

        obj = asso_map[asso]
        party = g.db_session.query(Party).filter(Party.id == cust_id).first()
        role_id = party.role[0].role_id
        objs = g.db_session.query(obj).filter(obj.cust_id == role_id).all()
        return [{'cust':obj.customer_rel.party,asso:obj } for obj in objs ]
        #cust = g.db_session.query(Customer).filter(Customer.role_id == role_id).first()

    def update_socialInsu(self,customer_id,**kwargs):
        cust = kwargs.get('cust')
        soc = kwargs.get('socialInsurance')
        info = {'name':cust.get('name'), 'cert_type':u'身份证', 'cert_no':cust.get('ric') , 'phone':soc.get('phone'), 'con_way':soc.get('con_way'), 'remark':soc.get('remark'),}
        g.db_session.query(Directors).filter(Directors.id == soc.get('id')).update(info)
        g.db_session.commit()


    def update_principal(self,customer_id,**kwargs):
        cust = kwargs.get('cust')
        prin = kwargs.get('principal')
        info = {'name':cust.get('name'),
                'principal_type':prin.get('principal_type'),
                'cert_type':cust.get('cert_type'),
                'cert_no':cust.get('cert_no'),
                'gender':cust.get('gender'),
                'age':cust.get('age'),
                'birthday':cust.get('birthday'),
                'education':prin.get('education'),
                'professional':prin.get('professional'),
                'administrative':prin.get('administrative'),
                'learn_his':prin.get('learn_his'),
                'politics_status':prin.get('politics_status'),
                'headship':prin.get('headship'),
                'duties':prin.get('duties'),
                'inaug_date':prin.get('inaug_date'),
                'birth_place':prin.get('birth_place'),
                'hobby':prin.get('hobby'),
                'birthday_place':prin.get('birthday_place'),
                'now_live_place':prin.get('now_live_place'),
                'work_history':prin.get('work_history'),
                'reward_dis':prin.get('reward_dis'),
                'recent_results':prin.get('recent_results'),
                'bad_remark':prin.get('bad_remark'),
                'have_no':prin.get('have_no'),
                'foreign_family':prin.get('foreign_family'),
                'is_directors_members':prin.get('is_directors_members'),
                'is_cert_copy':prin.get('is_cert_copy'),
                'phone':prin.get('phone'),
                'part_time':prin.get('part_time'),
                'relation_lay':prin.get('relation_lay'),
                'division_labor':prin.get('division_labor'),
                'remark':prin.get('remark'),
                }
        g.db_session.query(PrincipalPerson).filter(PrincipalPerson.id == prin.get('id')).update(info)
        g.db_session.commit()

    def update_contCom(self,customer_id,**kwargs):
        cust=kwargs.get('cust')
        cont=kwargs.get('controlledCompany')
        info = {
               #'comp_cust_id':cust.get('no'),
               #'company_cn_name':cust.get('name'),
               #'branch_per_id':cust.get('no'),
                'branch_cn_name':cust.get('name'),
                'response_name':cont.get('response_name'),
                'contract_name':cont.get('contract_name'),
                'phone':cont.get('phone'),
                'is_inde_accou':cont.get('is_inde_accou'),
                'remark':cont.get('remark'),
                'company_type':cont.get('company_type'),
                'is_effective':cont.get('is_effective'),
                'register_branch':cont.get('register_branch'),
                'register_name':cont.get('register_name'),
                'register_date':cont.get('register_date'),
                'update_date':cont.get('update_date'),
                'company_holding_type':cont.get('company_holding_type'),
                }
        g.db_session.query(branchInfo).filter(branchInfo.id == cont.get('id')).update(info)
        g.db_session.commit()
    def update_invesMang(self,customer_id,**kwargs):
        cust=kwargs.get('cust')
        inve=kwargs.get('investmentManagement')
        info = {#'rel_cust_id':cust.get('no'),
                'invest_cust_name':cust.get('name'),
                'deal_address':inve.get('deal_address'),
                'invest_date':inve.get('invest_date'),
                'invest_type':inve.get('invest_type'),
                'deal_range':inve.get('deal_range'),
                'invest_cur_type':inve.get('invest_cur_type'),
                'invest_amount':inve.get('invest_amount'),
                'fact_invest_amount':inve.get('fact_invest_amount'),
                'stock_percent':inve.get('stock_percent'),
                'invest_desc':inve.get('invest_desc'),
                'remark':inve.get('memo'),
                }
        g.db_session.query(customerCommInvest).filter(customerCommInvest.id == inve.get('id')).update(info)
        g.db_session.commit()
    def update_capitStr(self,customer_id,**kwargs):
        cust = kwargs.get('cust')
        capi = kwargs.get('capitalStructure')
        info = {'stock_holder_name':cust.get('name'),
                'cust_type':capi.get('cust_type'),
                'invest_cur_type':capi.get('invest_cur_type'),
                'id_type':capi.get('id_type'),
                'stock_holder_id_no':capi.get('stock_holder_id_no'),
                'invest_cur':capi.get('invest_cur'),
                'invest_pract':capi.get('invest_pract'),
                'invest_asset':capi.get('invest_asset'),
                'invest_other':capi.get('invest_other'),
                'invest_amount':capi.get('invest_amount'),
                'fact_amount':capi.get('fact_amount'),
                'invest_percentage':capi.get('invest_percentage'),
                'invest_desc':capi.get('invest_desc'),
                'remark':capi.get('memo'),
               }
        g.db_session.query(customerCommCapital).filter(customerCommCapital.id == capi.get('id')).update(info)
        g.db_session.commit()
    def update_clientCurr(self,customer_id,**kwargs):
        cust = kwargs.get('cust')
        clien=kwargs.get('clientCurriculum')
        info = {'cust_id':cust.get('id'),
                'occur_date':clien.get('occur_date'),
                'event_type':clien.get('event_type'),
                'event_name':clien.get('event_name'),
                'event_desc':clien.get('event_desc'),
                'exposed_com':clien.get('exposed_com'),
               }
       # if(cust.get('id') == clie.get('cust_id')):
       #     g.db_session.query(CustomerMemo).filter(CustomerMemo.id == clie.get('id')).update(info)
       # else:
       #     g.db_session.add(info);
       # g.db_session.commit()


    def level_person(self,cust_id):
        cust = g.db_session.query(Customer).join(Party,Party.id==Customer.party_id).filter(Party.id == cust_id).first();
        person_dict = {'age':int(cust.party.no) % 5,
          'headship_academic':cust.role_id%4}
        cust_tgs = g.db_session.query(CustTarget).filter(CustTarget.cust_type=='person').all()
        score = 0
        for cust_tg in cust_tgs:
            tg = cust_tg.target
            score = score + tg.attribute[person_dict[tg.code]].score
        return score*10

    def query_spou(self, customer_id):
        cust = g.db_session.query(FamilyRelation).join(Customer,Customer.role_id == FamilyRelation.cust_id).filter(Customer.party_id == customer_id).filter(FamilyRelation.cust_rela == u'配偶').first()
        if cust != None:
            rtn = {'family':cust, 'customer':cust.customer_rel.party}
            return rtn
        return

    def query_relatives(self, customer_id):
        cust = g.db_session.query(FamilyRelation).join(Customer,Customer.role_id == FamilyRelation.cust_id).filter(Customer.party_id == customer_id).all()
        bill_info_list=[]
        bill_info_list=[{'family':c,'cust_info':c.customer_rel.party} for c in cust]
        return bill_info_list

    def update_relatives(self, **kwargs):
        fam = kwargs.get('fam')
        cust = kwargs.get('cust')
        fam_id = fam.get('id')
        fam.pop('family_id')
        fam.pop('id')
        fam.pop('cust_id')
        fam.pop('customer')
        fam.pop('customer_rel')

        cust_id = cust.get('id')
        cust.pop('id')
        cust.pop('from_party')
        cust.pop('application_transaction')
        cust.pop('to_party')
        cust.pop('contact')
        cust.pop('type_code')
        cust.pop('no')
        cust.pop('role')
        cust.pop('certificates')
        cust.pop('name')
        #phone = kwargs.get('phone')
        #sys = kwargs.get('sys')
        g.db_session.query(FamilyRelation).filter(FamilyRelation.id == fam_id).update(fam)
        g.db_session.query(Resident).filter(Resident.id == cust_id).update(cust)
        #g.db_session.query(Phone).filter(Phone.id == telephone_id).update(telephone)


