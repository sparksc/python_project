# -*- coding:utf-8 -*-
from ..domain.transformat import Transformat
from .configure import Configure
import logging

with Configure() as cfg:
        database = cfg.get_database('aml_database')

def test_dict_transformat():
	mdict = {"department":{"age":3, "name":"经济"}, "departments":[{"age":2, "name":"show"}, {"age":1, "name":"john"}, {"age":0, "name":"maky"}]}
	Transformat(mdict).to_xls
	Transformat(mdict).to_json



def test_datasource_transformat():
        result = database.session.execute('''select third_branch_code, account_owner_no, account_owner_name, sys_aml_date_id, SYS_AML_LEVEL, null as first_evaluate_person, null as second_evaluate_person, aml_status, valid_customer From d_account_owner where third_branch_code !='无' and VALID_CUSTOMER='有效' and sys_aml_date_id!=0 and  role_type_code = 'CUSTOMER' ''').fetchmany(5)
        resultList = [dict(zip(row.keys(), row)) for row in result]
        beanParams = dict({
                'mlist':resultList,
                'mbranch':1001,
                'myear':2015,
                'mpage':1
                })
        srcFilePath = "../../resource/xlst/customer_classification.xls"
        destFilePath = "/tmp/customer_classification_out.xls"
        Transformat(beanParams, srcFilePath,  destFilePath).to_xls


