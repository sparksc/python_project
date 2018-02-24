# -*- coding:utf-8 -*-
u"""
测试名单导入功能
"""
import logging, datetime
from .configure import Configure
from ..domain.model import *
from ..domain.namelist import * 
from .test_aml_database import ResetDB

with Configure() as cfg:
    #database = cfg.get_database("aml_database_for_test");
    database = cfg.get_database("aml_database");

#test_ResetDB()

def test_import_namelist():
    global namelist_upfile_path 
    fp = os.path.join(namelist_upfile_path, "公安部发布恐怖分子名单.xls") 
    join_date = datetime.datetime.now()
    operate_teller = 1

    list_type ='黑名单'
    cust_type = '个人'
    for filename in ["公安部发布恐怖分子名单.xls"]:
        read_namelist(fp, filename, cust_type, list_type, join_date, operate_teller)
    
    list_type ='高风险名单'
    for filename in ["BZ法院被执行个人信息表.xlsx", "冻结登记簿.XLS", "失信被执行人_自然人.xlsx", "银监会公布违约个人名单.xlsx"]:
        read_namelist(fp, filename, cust_type, list_type, join_date, operate_teller)

    cust_type = '机构'
    for filename in ["BZ法院被执行单位信息表.xlsx", "失信被执行人_企业.xlsx", "工商吊销名单总表.XLS", "银监会公布违约企业名单.xlsx"]:
        read_namelist(fp, filename, cust_type, list_type, join_date, operate_teller)

test_import_namelist.setup = ResetDB

