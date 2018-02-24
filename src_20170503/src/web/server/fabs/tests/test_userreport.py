# -*- coding:utf-8 -*-

import unittest
from ..model.mbox import *
from ..model.user import User
import datetime
from test_org_level_para import TestBasicSalary as org
from ..services.userreport import *

import logging


ur = UserReport()
log = logging.getLogger()

class TestReport(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()
        logging.debug("***begin!!!****"+str(ur))

    def tearDown(self):
        logging.debug("~~~finish!!!~~~")

    def test_get_report(self):
        logging.debug("test_get_report begin!!!+++++"+str(ur))
        #data = ur.dep_balance(([(u'5', u'9660217', u'2016'), (u'4', u'9660087', u'2017')],))
        #data = ur.manage_dep_avg_bal(([(u'5', u'9660217', u'2016'), (u'4', u'9660087', u'2017')],))
        #data = ur.manage_loan_avg_bal(([(u'5', u'9660731', u'2016'), (u'8', u'9660727', u'2016'), (u'5', u'9660450', u'2013'), (u'8', u'9660753', u'2016'), (u'5', u'9661285', u'2016'), (u'9', u'9660422', u'2016'), (u'5', u'9660105', u'2016')],))
        #data = ur.manage_loan_num(([(u'5', u'9660217', u'2016'), (u'4', u'9660087', u'2017')],))
        #data = ur.manage_avg_dep_loan_percent(([(u'5', u'9660731', u'2016'), (u'8', u'9660727', u'2016'), (u'5', u'9660450', u'2013'), (u'8', u'9660753', u'2016'), (u'5', u'9661285', u'2016'), (u'9', u'9660422', u'2016'), (u'5', u'9660105', u'2016')],))
        #data = ur.manage_avg_dep_loan_percent(([(u'5', u'9660108', u'2016'),  (u'5', u'9660296', u'2016')],))
        #data = ur.manage_bad_bal_percent(([(u'5', u'9660217', u'2016'), (u'4', u'9660087', u'2017'), (u'1', u'9660756', u'2017'), (u'5', u'9661222', u'2016')],))
        #data = ur.dep_avg_all('2016','966020',True)
        #data = ur.loan_avg_all('2016','966101',True)
        #data = ur.ebank_num('2016','966100',True)
        #data = ur.loan_num('2016','966100',True)
        #data = ur.bad_bal_percent('2016','966010',True)
        #data = ur.card_num('2016','966020',True)
        #data = ur.avg_dep_percent('2016','966101',True)
        #data = ur.avg_dep_loan_percent('2016','966022')#,True)
        #data = ur.org_num('966021')
        #data = ur.org_list('966021',True)
        #data = org.test_add_salary_para
        #data = ur.get_year_day()
        #data = ur.international_num('2017','966010',True)
        #data = ur.teller_num('2016')
        data = ur.org_ranking('2016')
        #data = ur.branch_org('966122')
        #data = ur.ebank_percent('2016','966010',True)
        #logging.debug("test_get_report end!!!&&&&"+str(data))
        logging.debug("test_get_report end!!!&&&&")
