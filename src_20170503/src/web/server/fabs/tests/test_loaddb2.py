# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import aliased
import unittest
import json
import time
import logging
from sys import modules
import datetime
import random
from ..model.customer import *
from ..model.party import *
from ..model.common import *
from ..model.user import *
from ..model.common import *
#from ..database.logger import  log
from db2_utils import DB2
log = logging.getLogger()
#log = logging.getLogger()
#log.basicConfig(level=logging.DEBUG)

class TestLoadInfo(unittest.TestCase):

    def setUp(self):
        log.debug("执行setup")
        self.session=simple_session()
        #Base.metadata.create_all(self.session.bind) 
    def convert(self,field_type,field_name):
        if  field_type == None:
            return None
        #log.debug(type(field_type))
        #log.debug(field_type)
        #log.debug(field_name)
        field_type = field_type.strip()
        if field_type == '' :
            return None
        if(len(field_type) > 1):
            while field_type[0] == '0':
                field_type=field_type[1:]
        return self.arg_map.get(field_type+field_name)
        
        #com = self.session.query(CommonArgs).filter(CommonArgs.field_type==field_type).filter(CommonArgs.field_name==field_name).first()  
        #if com:
        #    pass#log.debug(com.value)
        #else:
        #    return None;
        #return com.value

    def loadCustomerinfo(self):   
        args = self.session.query(CommonArgs).all()
        self.arg_map={}
        for arg in args:
            self.arg_map.update({arg.field_type+arg.field_name:arg.value})

        db2= DB2()
        db2.db_conn()
        db2.exesql("select * from CUS_PER","CUS_PER")
        i = 1
        while db2.is_end() == False:
            cert_type = db2.get_byName("ID_TYPE")
            man = Resident( no=db2.get_byName("CUS_ID").strip(),
                            name=db2.get_byName("PER_NAME"),
                            ric=db2.get_byName("ID_NO").strip() if cert_type not in [None,'','52','53','54','55','99'] else None,
                            current_name=db2.get_byName("PER_NAME"),
                            gender=self.convert(db2.get_byName("SEX").strip(),'SEX') if db2.get_byName("SEX") else None,
                            birthday=db2.get_byName("DOB"),
                            birth_place=db2.get_byName("BIRTH_PLACE"),
                            education=self.convert(db2.get_byName("EDUCATION"),'EDUCATION'),
                            degree=self.convert(db2.get_byName("DEGREE"),'DEGREE'),
                            ethnicity=self.convert(db2.get_byName("NATIONALITY"),'NATIONALITY'),
                            health_status=self.convert(db2.get_byName("HEALTH_STATUS"),'HEALTH_STATUS'),
                            job=self.convert(db2.get_byName("OCCUPATION"),'OCCUPATION'),
                            politics_status=self.convert(db2.get_byName("POLITICAL_STATUS").strip(),'POLITICAL_STATUS') if db2.get_byName("POLITICAL_STATUS") else None ,
                            marital_status=self.convert(db2.get_byName("MARRIAGE_STATUS"),'MARRIAGE_STATUS'))

            customer = Customer(party=man,cust_type="person")
            
            cert = Certificate(party=man,
                               cert_no=db2.get_byName("ID_NO"),
                               cert_type=self.convert(db2.get_byName("ID_TYPE"),'ID_TYPE'),
                               thru_date=db2.get_byName("ID_EXPIRED_DATE"))
            self.session.add(cert)
            phone = Phone(phone_type=u'电话号码',phone_number=db2.get_byName("PHONE"))
            phone.party.append(man)
            #family_phone = Phone(phone_type=u'',phone_number=db2.get_byName("FAMILY_PHONE"))
            #family_phone.party.append(man)
            mobile_phone = Phone(phone_type=u'手机号码',phone_number=db2.get_byName("MOBILE_PHONE"))
            mobile_phone.party.append(man)
            #log.debug(db2.get_byName("EMAIL"))
            email_address=Email(email_address=db2.get_byName("EMAIL"))
            email_address.party.append(man)
            
            self.session.add_all([phone,mobile_phone,email_address])                
            employ = EmploymentRecord(customer=customer,
                                      company=db2.get_byName("COM_NAME"),
                                      company_type=self.convert(db2.get_byName("COM_TYPE"),'COM_TYPE'),
                                      company_field=self.convert(db2.get_byName("COM_FIELD"),'COM_FIELD'),
                                      company_phone=db2.get_byName("COM_TEL"),
                                      company_fax=db2.get_byName("COM_FAX"),
                                      company_addr=db2.get_byName("COM_ADDRESS"),
                                      company_addr_postcode=db2.get_byName("COM_ZIP_CODE"),
                                      debt_status=db2.get_byName("PER_OWES"),
                                      has_card_info=self.convert(db2.get_byName("PER_CREDIT_CARD"),'PER_CREDIT_CARD'),
                                      salary_account=db2.get_byName("SAL_ACC_ID"),
                                      salary_bank=db2.get_byName("SAL_BANK_NAME"),
                                      headship=self.convert(db2.get_byName("JOB_TITLE"),'JOB_TITLE'),
                                      important_event=db2.get_byName("JOB_EVENT"),
                                      our_bank_info=db2.get_byName("PER_OPEN_ACOUNT"),
                                      monthly_income=db2.get_byName("MONTH_INCOME"),
                                      payroll_status=self.convert(db2.get_byName("BWAGE"),'BWAGE'))
            self.session.add(employ)
            per_bus = PersonalBusiness(customer=customer,
                                       #operate_type=db2.get_byName("OPT_FASHION"),
                                       operate_type=self.convert(db2.get_byName("OPT_FASHION"),'OPT_FASHION'),
                                       cust_type=self.convert(db2.get_byName("CUS_KIND"),'CUS_KIND'),
                                       c_profession=self.convert(db2.get_byName("CUS_FIELD"),'CUS_FIELD'),
                                       enterprise_size=self.convert(db2.get_byName("OPT_CAPITAL"),'OPT_CAPITAL'),
                                       partnership=db2.get_byName("RELDEGREE"))
            self.session.add(per_bus)
            per_card=PersonalCard(customer=customer,
                                  loan_card=db2.get_byName("LOAN_ID"),
                                  industry_top=db2.get_byName("CLASS_1"), 
                                  industry_big=db2.get_byName("CLASS_2"),
                                  industry_mid=db2.get_byName("CLASS_3"),
                                  industry_small=db2.get_byName("CLASS_GB"),
                                  relation_us=self.convert(db2.get_byName("REL_DESC"),'REL_DESC'))
            self.session.add(per_card)
            family = FamilyRecord(customer=customer,
                                  family_address=db2.get_byName("ADDRESS"),
                                  family_postcode=db2.get_byName("ZIP_CODE"),
                                  family_number=db2.get_byName("FAMILY_TOTAL"),
                                  family_fixed_assets=db2.get_byName("FAMILY_CAPITAL"),
                                  family_tel=db2.get_byName("FAMILY_PHONE"),
                                  family_year_income=db2.get_byName("FAM_YEARLY_INCOME"),
                                  main_source=db2.get_byName("INCOME_SOURCE"),
                                  house_area=db2.get_byName("MORTGAGE_AERA"),
                                  live_status=self.convert(db2.get_byName("LIVE_INFO"),'LIVE_INFO'),
                                  family_culture=db2.get_byName("BREEDING"),
                                  investment_out_info=db2.get_byName("PER_INVESTMENT"),
                                  guarantee_out_info=db2.get_byName("PER_GURANTEE"))
            self.session.add(family)
            '''
            customer = Customer(comment=db2.get_byName("MEMO"),
                                register_org_id=db2.get_byName("REG_ORG_ID"),
                                register_user_id=db2.get_byName("REG_OPT_ID"),
                                upto_date=db2.get_byName("UPDATED_TIME"),
                                log_date=db2.get_byName("REG_DATE"))
            '''
            academicrecord = AcademicRecord(customer=customer,
                                     department=db2.get_byName("PROFESSION_TYPE"))
            self.session.add(academicrecord)
            
            
            log.debug(str(i))
            #log.debug(customer.role_id)

            i = i + 1
            db2.get_next()
            self.session.flush()
            #log.debug(customer.role_id)
        db2.close()
        self.session.commit()

        #self.customer = Customer(party=man,cust_type="person")
        #self.session.add_all([cert,employ,family,academicrecord])
        #log.debug('hhh') phone,family_phone,mobile_phone,email_address,
        #log.debug(self.customer.__dict__)

    def loadCompany(self):
        args = self.session.query(CommonArgs).all()
        self.arg_map={}
        for arg in args:
            self.arg_map.update({arg.field_type+arg.field_name:arg.value})

        db2= DB2()
        db2.db_conn()
        db2.exesql("select * from CUS_COM","CUS_COM")
        i = 1
        while db2.is_end() == False:
            com = Company(no=db2.get_byName("CUS_ID").strip(),
                          name=db2.get_byName("CN_COM_NAME"),
                          company_cn_name=db2.get_byName("CN_COM_NAME"),
                          company_en_name=db2.get_byName("EN_COM_NAME"),
                          company_famous_name=db2.get_byName("HB_COM_NAME"),
                          #company_pro=db2.get_byName("COM_PRO"),
                          #law_duty=db2.get_byName("COM_LAW_DUTY"),
                          loan_card_no=db2.get_byName("LOAN_ID"),
                          cust_aptitude=db2.get_byName("COM_APTITUDE"),
                          cust_field=self.convert(db2.get_byName("CUS_FIELD"),'CUS_FIELD'),
                          cust_kind=self.convert(db2.get_byName("CUS_KIND"),'CUS_KIND'),
                          org_id=db2.get_byName("ORG_ID"),
                          crop_type=self.convert(db2.get_byName("CORP_TYPE"),'CORP_TYPE'),
                          corp_name=db2.get_byName("REP_NAME"),
                          corp_id_num=db2.get_byName("REP_PERSON_ID"),
                          corp_credit_card=self.convert(db2.get_byName("REP_CREDIT_CARD"),'REP_CREDIT_CARD'),
                          company_reg_id=db2.get_byName("COM_REG_ID"),
                          company_reg_date=db2.get_byName("COM_REG_DATE"),
                          reg_thru_date=db2.get_byName("COM_EXPIRED_DATE"),
                          reg_check_result=self.convert(db2.get_byName("REG_CHECK_RESULT"),'REG_CHECK_RESULT'),
                          last_check_date=db2.get_byName("LAST_CHECK_DATE"),
                          nat_tax_id=db2.get_byName("NAT_TAX_ID"),
                          loc_tax_id=db2.get_byName("LOC_TAX_ID"),
                          reg_cur_type=self.convert(db2.get_byName("REG_CUR_TYPE"),'REG_CUR_TYPE'),
                          reg_amount=db2.get_byName("REG_CAPITAL"),
                          paid_cur_type=db2.get_byName("PAID_CAP_CUR_TYPE"),
                          paid_amount=db2.get_byName("PAID_CAPITAL"),
                          #account_approval_no=db2.get_byName("ACC_PERMIT"),
                          reg_country=self.convert(db2.get_byName("REG_COUNTRY"),'REG_COUNTRY'),
                          reg_state=db2.get_byName("REG_STATE"),
                          reg_address=db2.get_byName("REG_ADDRESS"),
                          bus_address=db2.get_byName("CURRENT_ADDRESS"),
                          reg_phone=db2.get_byName("COM_PHONE"),
                          company_area=db2.get_byName("OPT_AERA"),
                          company_opt_owner=db2.get_byName("OPT_OWNER"),
                          company_own_relation=db2.get_byName("ATTACHED_TO"),
                          industry_small_class=db2.get_byName("CLASS_GB"), 
                          industry_class=db2.get_byName("CLASS_1"),
                          industry_large_class=db2.get_byName("CLASS_2"),
                          company_kind=self.convert(db2.get_byName("OPT_TYPE"),'OPT_TYPE'),
                          company_capital=self.convert(db2.get_byName("OPT_CAPITAL"),'OPT_CAPITAL'),
                          total_employee=db2.get_byName("TOTAL_EMPLOYEE"),
                          opt_field=db2.get_byName("OPT_FIELD"),
                          base_bank=self.convert(db2.get_byName("BASE_BANK"),'BASE_BANK'),
                          bank_account_no=db2.get_byName("ACC_ID"),
                          init_account_date=db2.get_byName("INIT_ACC_TIME"),
                          init_loan_date=db2.get_byName("INIT_LOAN_TIME"), 
                          #loan_card_pwd=db2.get_byName("LOAN_CARD_PWD"),
                          loan_card_status=self.convert(db2.get_byName("BLOAN_CARD"),'BLOAN_CARD'),
                          local_field=db2.get_byName("BLOCAL"),
                          company_cust=self.convert(db2.get_byName("BGROUP"),'BGROUP'),
                          company_manage=self.convert(db2.get_byName("GROUP_MANAGE"),'GROUP_MANAGE'),
                          company_financing=self.convert(db2.get_byName("GROUP_FINANCING"),'GROUP_FINANCING'),
                          import_export=self.convert(db2.get_byName("BIMPORT_EXPORT"),'BIMPORT_EXPORT'),
                          special_business=db2.get_byName("SP_BUSINESS"),
                          special_licence=self.convert(db2.get_byName("SP_LICENCE"),'SP_LICENCE'),
                          special_start_date=db2.get_byName("SP_START_DATE"),
                          special_thru_date=db2.get_byName("SP_EXPIRED_DATE"),
                          real_type=self.convert(db2.get_byName("REAL_TYPE"),'REAL_TYPE'),
                          ela_flag=self.convert(db2.get_byName("BFLAG1"),'BFLAG1'),
                          important_flag_10=self.convert(db2.get_byName("BFLAG2"),'BFLAG2'),
                          important_flag_22=self.convert(db2.get_byName("BFLAG3"),'BFLAG3'),
                          important_flag_60=self.convert(db2.get_byName("BFLAG4"),'BFLAG4'),
                          fin_rep_type=db2.get_byName("FIN_REP_TYPE"), 
                          rating_type=self.convert(db2.get_byName("IN_RATING_METHOD"),'IN_RATING_METHOD'),
                          in_credit_class=self.convert(db2.get_byName("IN_CREDIT_CLASS"),'IN_CREDIT_CLASS'),
                          out_credit_class=self.convert(db2.get_byName("OUT_CREDIT_CLASS"),'OUT_CREDIT_CLASS'),
                          out_rating_date=db2.get_byName("OUT_RATING_DATE"),
                          out_org=db2.get_byName("AUT_ORG"),
                          relation_desc=self.convert(db2.get_byName("REL_DESC"),'REL_DESC'),
                          relation_corp=self.convert(db2.get_byName("REL_DEGREE"),'REL_DEGREE'),
                          hold_stock_flag=self.convert(db2.get_byName("BHOLD_STOCK"),'BHOLD_STOCK'),
                          hold_stock_amount=db2.get_byName("HOLD_STOCK"),
                          bank_cust_type=self.convert(db2.get_byName("BANK_CUS_TYPE"),'BANK_CUS_TYPE'),
                          risk_flag=self.convert(db2.get_byName("RISK_FLAG"),'RISK_FLAG'),
                          blacklist_flag=self.convert(db2.get_byName("BLACKLIST_FLAG"),'BLACKLIST_FLAG'),
                          prod_equip=db2.get_byName("PROD_EQUIP"),
                          year_prod=db2.get_byName("YEAR_PROD"),
                          fact_prod=db2.get_byName("FACT_PROD"),
                          register_branch=db2.get_byName("REG_ORG_ID"),
                          register_name=db2.get_byName("REG_BY_ID"),
                          register_date=db2.get_byName("REG_DATE"),
                          company_opt_type=self.convert(db2.get_byName("OPT_NATURE"),'OPT_NATURE'),
                          company_house_area=db2.get_byName("HOUSE_AREA"),
                          company_house_owner=db2.get_byName("HOUSE_OWNER"),
                          opt_scope=db2.get_byName("OPT_SCOPE"),
                          company_fashion=self.convert(db2.get_byName("OPT_FASHION"),'OPT_FASHION'),
                          industry_mid_class=db2.get_byName("CLASS_3"),
                          company_credit_code=db2.get_byName("INSTITUTION_CREDIT_CODE"),
                          account_approval_no=db2.get_byName("ACCOUNT_APPROVAL_NO"),
                          customer_type=self.convert(db2.get_byName("CUS_VARIETY"),'CUS_VARIETY'),
                          corp_type=db2.get_byName("ORG_TYPE"),
                          corp_type_detail=db2.get_byName("ORG_TYPE_DETAIL"),
                          account_status=self.convert(db2.get_byName("ORG_STATE"),'ORG_STATE'),
                          asset_liability_date=db2.get_byName("ASSET_LIABILITY_DATE"),
                          asset_amount=db2.get_byName("ASSET"),
                          liability_amount=db2.get_byName("LIABILITY"))
            cust = Customer(party=com,cust_type="company")
            self.session.add(cust)
            db2.get_next()
            self.session.flush()
            log.debug(i)
            i = i + 1

        db2.close()
        self.session.commit()
    #行业信息
    def industryType(self):
        db2= DB2()
        db2.db_conn()
        db2.exesql("select * from INDUSTRY_TYPE","INDUSTRY_TYPE")
        i = 0
        while (db2.is_end() == False):
            idus = IndustryType(industry_d = db2.get_byName('INDUSTRY_ID').strip(),
                        class_a = db2.get_byName('CLASS_A').strip(),
                        type_1=db2.get_byName('TYPE1').strip(),
                        type_2=db2.get_byName('TYPE2').strip(),
                        type_3=db2.get_byName('TYPE3').strip(),
                        type_name=db2.get_byName('TYPE_NAME').strip(),
                        type_desc=db2.get_byName('TYPE_DESC').strip())

            self.session.add(idus)
            db2.get_next()
            i = i + 1
        log.debug(i)


    def loadPartyRole(self):
        db2 = DB2()
        db2.db_conn()
        db2.exesql("select * from CUS_LOAN_REL ","CUS_LOAN_REL")
        show = 0
        while db2.is_end() == False:
            no = db2.get_byName('CUS_ID')
            branch_code = db2.get_byName('LOAN_BRANCH_ID')
            party_id = self.session.query(Party.id).filter(Party.no.like(no.strip()+'%')).first()
            party_role = PartyRole(party_id=party_id,branch_code=branch_code.strip())
            #if branch_code:
            #    branch_code = branch_code.strip()
            #    party_role = PartyRole(party=com,branch_code=branch_code) 
            self.session.add(party_role)
            db2.get_next()
            show = show + 1
            log.debug(show)
        db2.close()
        self.session.commit()

    def loadComCapital(self):
        db2 = DB2()
        db2.db_conn()
        db2.exesql("select * from CUS_COM_CAPITAL","CUS_COM_CAPITAL")
        count = 0
        q = self.session.query(Customer.role_id).join(Party,Party.id==Customer.party_id)
        record = []
        while db2.is_end() == False:
            cus_no =  db2.get_byName("CUS_ID").strip()+'%'
            stock_no = db2.get_byName("STOCK_CUS_ID").strip()+'%'
            cust_id = q.filter(Party.no.like(cus_no)).first()
            stock_cust_id = q.filter(Party.no.like(stock_no)).first()
            if cust_id == None or stock_cust_id == None:
                record.append([cus_no,stock_no])
                count = count + 1
                log.debug(str(count)+'error'+cus_no+'--'+stock_no)
                db2.get_next()
                continue
            cust_com_capital = customerCommCapital(cust_id = cust_id,
                            stock_cust_id = stock_cust_id,
                            stock_holder_name = db2.get_byName("STOCK_HOLDER_NAME"),
                            cust_type= db2.get_byName("STOCK_HOLDER_NAME"),
                            id_type= db2.get_byName("ID_TYPE"),
                            stock_holder_id_no= db2.get_byName("STOCK_HOLDER_ID_NO").strip(),
                            invest_type= db2.get_byName("INVEST_TYPE"),
                            invest_cur_type= db2.get_byName("INVEST_CUR_TYPE"),
                            invest_cur= db2.get_byName("INVEST_CUR"),
                            invest_pract= db2.get_byName("INVEST_PRACT"),
                            invest_asset= db2.get_byName("INVEST_ASSET"),
                            invest_other= db2.get_byName("INVEST_OTHER"),
                            invest_amount= db2.get_byName("INVEST_AMOUNT"),
                            fact_amount= db2.get_byName("ACT_AMOUNT"),
                            invest_percentage= db2.get_byName("INVEST_PERCENTAGE"),
                            invest_desc= db2.get_byName("INVEST_DESC"),
                            remark= db2.get_byName("MEMO"),
                            flag= db2.get_byName("BFLAG"))
            self.session.add(cust_com_capital)
            self.session.flush()
            db2.get_next()
            count = count + 1
            log.debug(count)
        log.debug(record)
        db2.close()
        self.session.commit()

    def loadComRel(self):
        u''' 001 母子公司 002 子母公司 004 资本组成  202 董事  203 主要负责人 301,302,303,304,999 个人与个人之间关系(父母,夫妻等等)  '''
        rel_map={'001':branchInfo,
                 '202':Directors,
                 '203':PrincipalPerson,
                 '301':FamilyRelation,
                 '302':FamilyRelation,
                 '303':FamilyRelation,
                 '304':FamilyRelation,
                 '999':FamilyRelation,
                  }
        db2 = DB2()
        db2.db_conn()
        db2.exesql("select * from CUS_REL","CUS_REL")
        q = self.session.query(Customer).join(Party,Party.id==Customer.party_id)
        record = []
        count = 0
        while db2.is_end() == False:
            cus_no =  db2.get_byName("CUS_ID").strip()+'%'
            rel_no = db2.get_byName("REL_CUS_ID").strip()+'%'
            rel_type = db2.get_byName("REL_TYPE").strip()
            cust = q.filter(Party.no.like(cus_no)).first()
            rel_cust = q.filter(Party.no.like(rel_no)).first()
            if cust == None or rel_cust == None or rel_type in ['',None]:
                record.append([cus_no,rel_no])
                count = count + 1
                log.debug(str(count)+'error'+cus_no+'--'+rel_no)
                db2.get_next()
                continue
            if rel_map.get(rel_type):
                obj = rel_map.get(rel_type) 
                tb = obj(customer=cust,customer_rel=rel_cust)
                self.session.add(tb)
            db2.get_next()
            count = count + 1
            log.debug(count)
        log.debug(record)
        db2.close()
        self.session.commit()

    def testMain(self):
        #个人客户信息
        self.loadCustomerinfo()
        #对公客户信息
        self.loadCompany()
        #客户 机构关联信息
        self.loadPartyRole()
        #公司资本构成
        self.loadComCapital()
        #客户关联信息
        self.loadComRel()

    def tearDown(self):
        #self.session.commit() 
        log.debug("Over")


