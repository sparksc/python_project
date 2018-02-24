# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import aliased
import unittest
import json
import logging
from ..model.user import *
from ..model.asset import *
from ..model.liabilities import *
from ..model.credit import *
from ..model.customer import *
from ..model.international import *
from sys import modules
import datetime
logging.basicConfig(level=logging.DEBUG)

class TestCustomerInfo(unittest.TestCase):
    def setUp(self):
        self.session=simple_session()
        Base.metadata.drop_all(self.session.bind)
        Base.metadata.create_all(self.session.bind)

        cny = Currency( currency_code='CNY', currency_name=u'人民币', currency_symbols='cny')

        man=Resident(name=u'张三', ric=u'330602197404040011', family_name=u'张', give_name=u'三', gender=u'男性', birthday=datetime.datetime.now(), ethnicity =u'汉族', politics_status=u"中国共产党", marital_status=u"未婚", monthly_income_of_family=83943949, hobbies_and_interests=u"钓鱼")
        self.customer = Customer(party=man, cust_type="person")

        man6=Resident(name=u'赵六', ric=u'330602197404040012', family_name=u'赵', give_name=u'六', gender=u'男性', birthday=datetime.datetime.now(), ethnicity =u'汉族', politics_status=u"中国共产党", marital_status=u"已婚且有子女", monthly_income_of_family=31445, hobbies_and_interests=u"看书")
        customer6 = Customer(party=man6, cust_type="person")

        man2=Resident(name=u'李四', ric=u'330602197404040022', family_name=u'李', give_name=u'四')
        self.user = User(party = man2)

        self.session.add_all([cny, self.user, self.customer, customer6])

    def test_change_customer_info(self):
        logging.debug("start change customer info")

        d = datetime.datetime.now()
        operating_log = CustomerInfoOptLog(upto_date=d, log_date=d, register_user=self.user, comment="eeeeee") 

        logging.debug("%s"%self.customer.party)

        addr = Address(party= [self.customer.party], address=u"上海市长宁区")
        email = Email(party = [self.customer.party], email_address=u"yinsho@yinsho.com")
        phone = Phone(party = [self.customer.party], phone_type="手机", phone_number = "1888888888")
        phone2 = Phone(party = [self.customer.party], phone_type="手机1", phone_number = "109999999999")

        self.customer.party.ethnicity = u"汉族"
         
        man3=Resident(name=u'王五', ric=u'33060219740xxxxxx2', family_name=u'王', give_name=u'五')

        logging.debug("%s"%dir(self.customer))

        logging.debug("%s"%dir(self.customer.party))
        logging.debug("%s"%dir(self.customer.party.to_party))
        logging.debug("%s"%dir(self.customer.party.from_party))
        self.customer.party.to_party.append(man3)

        ar = AcademicRecord(customer=self.customer, register_log=operating_log, update_log=operating_log)
        er = EmploymentRecord(customer=self.customer, register_log=operating_log, update_log=operating_log)
        cm = CustomerMemo(customer=self.customer, register_log=operating_log, update_log=operating_log)
        cr = CustomerRealty(customer=self.customer, register_log=operating_log, update_log=operating_log)
        cb = CustomerBond(customer=self.customer, register_log=operating_log, update_log=operating_log)
        ct = CustomerStock(customer=self.customer, register_log=operating_log, update_log=operating_log)
        cia = CustomerIntangibleAsset(customer=self.customer, register_log=operating_log, update_log=operating_log)
        cv = CustomerVehicle(customer=self.customer, register_log=operating_log, update_log=operating_log)
        csi = CustomerSocialInsurance(customer=self.customer, register_log=operating_log, update_log=operating_log)
        cci = CustomerCommerialInsurance(customer=self.customer, register_log=operating_log, update_log=operating_log)
        cie = CustomerInvestmentEnterprise(customer=self.customer, register_log=operating_log, update_log=operating_log)
        coa = CustomerOtherAsset(customer=self.customer, register_log=operating_log, update_log=operating_log)
        col = CustomerOtherLiabilities(customer=self.customer, register_log=operating_log, update_log=operating_log)

        self.session.add_all([man3, addr, email, phone, phone2, ar, er, cm, cr, cb, ct, cia, cv, csi, cci , cie , coa , col])

    def tearDown(self):
        #self.session.rollback()
        #Base.metadata.drop_all(self.session.bind)
        self.session.commit() 
    
