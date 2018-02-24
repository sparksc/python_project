# -*- coding:utf-8 -*-

import unittest
from sqlalchemy.orm import joinedload_all
from ..model.permission import *
from ..model.user import *
from ..base import utils
import datetime

import logging

log = logging.getLogger()

class TestNxcrmReport(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()
        init_crm_report_menu_data(self.session)

    def tearDown(self):
        logging.debug("finish!!!")

def add_group_menu_rel(session, groups, m1_1):
    now = datetime.datetime.now()
    for g in groups:
        gm1_1 = GroupMenu(from_date=now)
        gm1_1.group = g
        m1_1.groups.append(gm1_1)
        session.add(m1_1)

def init_crm_report_menu_data(session):
    logging.debug("init crm report menu data !")

    groups = session.query(Group).all()

    #m1_2 = Menu(**{'name':u'活期储蓄账户明细表', 'location':'views/report/DemandDepositInfo.html'})
    #m1_3 = Menu(**{'name':u'客户基本信息报表', 'location':'views/report/CustomerBaseInfo.html'})
    #m1_4 = Menu(**{'name':u'客户详细信息', 'location':'views/report/CustomerDetailInfo.html'})
    #m1_5 = Menu(**{'name':u'理财账户明细表', 'location':'views/report/BankingAccountInfo.html'})
    #m1_6 = Menu(**{'name':u'贷记卡账户明细表', 'location':'views/report/CreditCardAccountInfo.html'})
    #m1_7 = Menu(**{'name':u'定期储蓄账户明细表', 'location':'views/report/DepositInfo.html'})
    #m1_8 = Menu(**{'name':u'电子银行报表', 'location':'views/report/EBankInfo.html'})
    #m1_9 = Menu(**{'name':u'贷款明细报表', 'location':'views/report/LoanDetailInfo.html'})
    #m1_10 = Menu(**{'name':u'活期储蓄账户中间业务签约信息表', 'location':'views/report/SavingAccountInfo.html'})
    #m1_11 = Menu(**{'name':u'员工考核指标查询', 'location':''})
    #m1_12 = Menu(**{'name':u'员工本人考核指标查询', 'location':''})
    #m1_13 = Menu(**{'name':u'员工绩效薪酬查询', 'location':''})
    #m1_14 = Menu(**{'name':u'本人绩效薪酬查询', 'location':''})
    #m1_15 = Menu(**{'name':u'机构指标查询', 'location':'views/report/Jgzb.html'})
    m1_16 = Menu(**{'name':u'存款归属关系新增', 'location':'views/report/Ckgsgxxz.html'})
    m1_17 = Menu(**{'name':u'贷款归属关系新增', 'location':'views/report/Dkgsgxxz.html'})
    m1_18 = Menu(**{'name':u'存款营销录入', 'location':'views/report/Ckyxlr.html'})
    m1_19 = Menu(**{'name':u'存贷挂钩关系录入', 'location':'views/manage/Cdgggxlr.html'})
    m1_20 = Menu(**{'name':u'存贷挂钩关系查询', 'location':'views/manage/CdgggxSearch.html'})
    m1_21 = Menu(**{'name':u'存款归属批量转移', 'location':'views/manage/Ckgsplzy.html'})
    m1_22 = Menu(**{'name':u'贷款归属批量转移', 'location':'views/manage/Dkgsplzy.html'})
    m1_23 = Menu(**{'name':u'存贷挂钩关系录入复核', 'location':'views/manage/CdgggxlrCk.html'})
    m1_24 = Menu(**{'name':u'存款归属单笔维护', 'location':'views/report/Ckgsdbwh.html'})
    m1_25 = Menu(**{'name':u'贷款营销录入', 'location':'views/report/Dkyxlr.html'})
    m1_26 = Menu(**{'name':u'新昌贷款营销录入', 'location':'views/loan_manage_xinchang/Dkyxlr.html'})  
    m1_27 = Menu(**{'name':u'贷款归属单笔维护', 'location':'views/manage/Dkgsdbwh.html'})
    m1_28 = Menu(**{'name':u'存贷款客户核心号和信贷号', 'location':'views/report/Dkkhxdh.html'})

    #m1 = Menu(**{'name':u'客户综合系统报表', 'location':u'', 'children':[m1_2, m1_3, m1_4, m1_5, m1_6, m1_7, m1_8, m1_9, m1_10,m1_11,m1_12,m1_13,m1_14,m1_15,m1_16,m1_17]})
    m1 = Menu(**{'name':u'业绩管理', 'location':u'', 'children':[m1_16,m1_17,m1_18,m1_19,m1_20,m1_21,m1_22,m1_23,m1_24,m1_25,m1_26,m1_27,m1_28]})

    #add_group_menu_rel(session, groups, m1_2)
    #add_group_menu_rel(session, groups, m1_3)
    #add_group_menu_rel(session, groups, m1_4)
    #add_group_menu_rel(session, groups, m1_5)
    #add_group_menu_rel(session, groups, m1_6)
    #add_group_menu_rel(session, groups, m1_7)
    #add_group_menu_rel(session, groups, m1_8)
    #add_group_menu_rel(session, groups, m1_9)
    #add_group_menu_rel(session, groups, m1_10)
    #add_group_menu_rel(session, groups, m1_11)
    add_group_menu_rel(session, groups, m1_16)
    add_group_menu_rel(session, groups, m1_17)
    add_group_menu_rel(session, groups, m1_18)
    add_group_menu_rel(session, groups, m1_19)
    add_group_menu_rel(session, groups, m1_20)
    add_group_menu_rel(session, groups, m1_21)
    add_group_menu_rel(session, groups, m1_22)
    add_group_menu_rel(session, groups, m1_23)
    add_group_menu_rel(session, groups, m1_24)
    add_group_menu_rel(session, groups, m1_25)
    add_group_menu_rel(session, groups, m1_26)
    add_group_menu_rel(session, groups, m1_27)
    add_group_menu_rel(session, groups, m1_28)

    add_group_menu_rel(session, groups, m1)
    """
        指标查询
    """
    m12_2 = Menu(**{'name':u'客户经理按季考核指标', 'location':'views/report/Khjlajzb.html'})
    m12_3 = Menu(**{'name':u'客户经理按年考核指标', 'location':'views/report/Khjlanzb.html'})
    m12_4 = Menu(**{'name':u'综合柜员按年考核指标', 'location':'views/report/Zhgyanzb.html'})
    m12_5 = Menu(**{'name':u'综合柜员按季考核指标', 'location':'views/report/Zhgyajzb.html'})
    m12_6 = Menu(**{'name':u'员工按年考核指标', 'location':'views/report/Yganzb.html'})
    m12_7 = Menu(**{'name':u'员工按季考核指标', 'location':'views/report/Ygajzb.html'})
    m12_8 = Menu(**{'name':u'客户经理本人按季考核指标', 'location':'views/report/Khjlbrajzb.html'})
    m12_9 = Menu(**{'name':u'客户经理本人按年考核指标', 'location':'views/report/Khjlbranzb.html'})
    m12_10 = Menu(**{'name':u'综合柜员本人按年考核指标', 'location':'views/report/Zhgybranzb.html'})
    m12_11 = Menu(**{'name':u'综合柜员本人按季考核指标', 'location':'views/report/Zhgybrajzb.html'})
    m12_12 = Menu(**{'name':u'员工本人按年考核指标', 'location':'views/report/Ygbranzb.html'})
    m12_13 = Menu(**{'name':u'员工本人按季考核指标', 'location':'views/report/Ygbrajzb.html'})
    m12_14 = Menu(**{'name':u'机构指标查询', 'location':'views/report/Jgzb.html'})



    m12 = Menu(**{'name':u'指标查询', 'location':u'', 'children':[m12_2, m12_3,m12_4,m12_5,m12_6,m12_7,m12_8,m12_9,m12_10,m12_11,m12_12,m12_13,m12_14]})

    add_group_menu_rel(session, groups, m12_2)
    add_group_menu_rel(session, groups, m12_3)
    add_group_menu_rel(session, groups, m12_4)
    add_group_menu_rel(session, groups, m12_5)
    add_group_menu_rel(session, groups, m12_6)
    add_group_menu_rel(session, groups, m12_7)
    add_group_menu_rel(session, groups, m12_8)
    add_group_menu_rel(session, groups, m12_9)
    add_group_menu_rel(session, groups, m12_10)
    add_group_menu_rel(session, groups, m12_11)
    add_group_menu_rel(session, groups, m12_12)
    add_group_menu_rel(session, groups, m12_13)
    add_group_menu_rel(session, groups, m12_14)


    add_group_menu_rel(session, groups, m12)
    """
        绩效薪酬
    """
    m14_2 = Menu(**{'name':u'客户经理按季绩效薪酬', 'location':'views/report/Khjlajjxxc.html'})
    m14_3 = Menu(**{'name':u'客户经理按年绩效薪酬', 'location':'views/report/Khjlanjxxc.html'})
    m14_4 = Menu(**{'name':u'综合柜员按年绩效薪酬', 'location':'views/report/Zhgyanjxxc.html'})
    m14_5 = Menu(**{'name':u'综合柜员按季绩效薪酬', 'location':'views/report/Zhgyajjxxc.html'})
    m14_6 = Menu(**{'name':u'员工按年绩效薪酬', 'location':'views/report/Yganjxxc.html'})
    m14_7 = Menu(**{'name':u'员工按季绩效薪酬', 'location':'views/report/Ygajjxxc.html'})
    m14_8 = Menu(**{'name':u'客户经理本人按季绩效薪酬', 'location':'views/report/Khjlbrajjxxc.html'})
    m14_9 = Menu(**{'name':u'客户经理本人按年绩效薪酬', 'location':'views/report/Khjlbranjxxc.html'})
    m14_10 = Menu(**{'name':u'综合柜员本人按年绩效薪酬', 'location':'views/report/Zhgybranjxxc.html'})
    m14_11 = Menu(**{'name':u'综合柜员本人按季绩效薪酬', 'location':'views/report/Zhgybrajjxxc.html'})
    m14_12 = Menu(**{'name':u'员工本人按年绩效薪酬', 'location':'views/report/Ygbranjxxc.html'})
    m14_13 = Menu(**{'name':u'员工本人按季绩效薪酬', 'location':'views/report/Ygbrajjxxc.html'})


    m14 = Menu(**{'name':u'绩效薪酬', 'location':u'', 'children':[m14_2, m14_3,m14_4,m14_5,m14_6,m14_7,m14_8, m14_9,m14_10,m14_11,m14_12,m14_13]})

    add_group_menu_rel(session, groups, m14_2)
    add_group_menu_rel(session, groups, m14_3)
    add_group_menu_rel(session, groups, m14_4)
    add_group_menu_rel(session, groups, m14_5)
    add_group_menu_rel(session, groups, m14_6)
    add_group_menu_rel(session, groups, m14_7)
    add_group_menu_rel(session, groups, m14_8)
    add_group_menu_rel(session, groups, m14_9)
    add_group_menu_rel(session, groups, m14_10)
    add_group_menu_rel(session, groups, m14_11)
    add_group_menu_rel(session, groups, m14_12)
    add_group_menu_rel(session, groups, m14_13)

    add_group_menu_rel(session, groups, m14)

    """
        薪酬参数
    """
    m16_2 = Menu(**{'name':u'员工学历津贴额', 'location':'views/performance_appraisal/base_pay/parameter/edu/index.html'})
    m16_3 = Menu(**{'name':u'员工职称津贴额', 'location':'views/performance_appraisal/base_pay/parameter/pos_name/index.html'})
    m16_4 = Menu(**{'name':u'岗位职级薪酬', 'location':'views/performance_appraisal/base_pay/parameter/pos_lev/index.html'})
    m16_5 = Menu(**{'name':u'员工工龄津贴和保障工资', 'location':'views/performance_appraisal/base_pay/parameter/salary/index.html'})
    m16_6 = Menu(**{'name':u'员工基本薪酬', 'location':'views/report/Ygjbxc.html'})
    m16_7 = Menu(**{'name':u'本人基本薪酬', 'location':'views/report/Brjbxc.html'})
    m16_8 = Menu(**{'name':u'员工薪酬等级薪档表', 'location':'views/tpara/tparadetail.html?para_type_id=7'})
    m16_9 = Menu(**{'name':u'月度实发薪酬', 'location':'views/performance_appraisal/month_salary/monsalary.html'})
    m16_10 = Menu(**{'name':u'本人月度实发薪酬', 'location':'views/performance_appraisal/month_salary/selfmonsalary.html'})



    m16 = Menu(**{'name':u'薪酬参数', 'location':u'', 'children':[m16_2,m16_3,m16_4,m16_5,m16_6,m16_7,m16_8,m16_9,m16_10]})

    add_group_menu_rel(session, groups, m16_2)
    add_group_menu_rel(session, groups, m16_3)
    add_group_menu_rel(session, groups, m16_4)
    add_group_menu_rel(session, groups, m16_5)
    add_group_menu_rel(session, groups, m16_6)
    add_group_menu_rel(session, groups, m16_7)
    add_group_menu_rel(session, groups, m16_8)
    add_group_menu_rel(session, groups, m16_9)
    add_group_menu_rel(session, groups, m16_10)


    add_group_menu_rel(session, groups, m16)


    # system_manager
    m11_2 = Menu(**{'name':u'权限管理', 'location':'views/system_manager/permission/index.html'})
    m11_3 = Menu(**{'name':u'用户管理', 'location':'views/system_manager/branch_group_staff/index.html'})
    #m11_4 = Menu(**{'name':u'指纹管理', 'location':'views/system_manager/#'})
    #m11_5 = Menu(**{'name':u'密码管理', 'location':'views/system_manager/#'})
    #m11_6 = Menu(**{'name':u'网点信息管理', 'location':'views/system_manager/#'})
    #m11_7 = Menu(**{'name':u'自助设备信息管理', 'location':'views/system_manager/#'})
    #m11_8 = Menu(**{'name':u'管片关系管理', 'location':'views/system_manager/#'})
    m11_8 = Menu(**{'name':u'员工状态管理', 'location':'views/system_manage/staff_status.html'})
    m11_9 = Menu(**{'name':u'机构上下级管理','location':'views/branch_manage/index.html'})
    m11_10 = Menu(**{'name':u'页面维护','location':'views/system_manager/pagemaintenance/pagemain.html'})
    m11_11 = Menu(**{'name':u'员工基本信息维护', 'location':'views/performance_appraisal/base_pay/parameter/basic/basic_mess.html'})
    m11_12 = Menu(**{'name':u'岗位维护', 'location':'views/report/Xteng.html'})
    m11_13 = Menu(**{'name':u'员工机构岗位维护', 'location':'views/system_manager/branch_group_user/index.html'})
    m11_14 = Menu(**{'name':u'核心工号关系维护', 'location':'views/system_manager/staff_relation.html'})
    #m11 = Menu(**{'name':u'系统管理', 'location':u'', 'children':[m11_2, m11_3,m11_4 , m11_5 , m11_6 , m11_7 , m11_8 ,m11_9 ,m11_10]})
    m11 = Menu(**{'name':u'系统管理', 'location':u'', 'children':[m11_2, m11_3, m11_8 ,m11_9 ,m11_10,m11_11,m11_12,m11_13,m11_14]})

    add_group_menu_rel(session, groups, m11_2)
    add_group_menu_rel(session, groups, m11_3)
    #add_group_menu_rel(session, groups, m11_4)
    #add_group_menu_rel(session, groups, m11_5)
    #add_group_menu_rel(session, groups, m11_6)
    #add_group_menu_rel(session, groups, m11_7)
    add_group_menu_rel(session, groups, m11_8)
    add_group_menu_rel(session, groups, m11_9)
    add_group_menu_rel(session, groups, m11_10) 
    add_group_menu_rel(session, groups, m11_11)
    add_group_menu_rel(session, groups, m11_12) 
    add_group_menu_rel(session, groups, m11_13)
    add_group_menu_rel(session, groups, m11_14)
    add_group_menu_rel(session, groups, m11)
    
    #绩效考核
    m2_2 = Menu(**{'name':u'绩效合约', 'location':'views/system_manager/performance/per_con/index.html'})
    m2_3 = Menu(**{'name':u'指标库', 'location':'views/target_library/index.html'})
    m2_4 = Menu(**{'name':u'绩效合约查看', 'location':'views/pe_contract_check/index.html'})
    m2 = Menu(**{'name':u'绩效合约', 'location':u'', 'children':[m2_2, m2_3, m2_4]})

    add_group_menu_rel(session, groups, m2_2)
    add_group_menu_rel(session, groups, m2_3)
    add_group_menu_rel(session, groups, m2_4)

    add_group_menu_rel(session, groups, m2)
    
    #指标
    m22_3 = Menu(**{'name':u'手工录入交易替代率','location':'views/performance_appraisal/index_query/parameter/input/hand/index.html'})
    m22_4 = Menu(**{'name':u'百元贷款收息率','location':'views/performance_appraisal/index_query/parameter/input/loan/index.html'})
    m22_6 = Menu(**{'name':u'手机、e银行录入','location':'views/performance_appraisal/index_query/parameter/input/phone/index.html'})
    m22_7 = Menu(**{'name':u'企业网银录入','location':'views/performance_appraisal/index_query/parameter/input/e_bank/index.html'})
    m22_8 = Menu(**{'name':u'机构存贷款数据调整','location':'views/credit/adujstDatapype/index.html'})
    m22_9 = Menu(**{'name':u'风险管理部退出贷款','location':'views/tpara/tparadetail.html?para_type_id=6'})
    m22_5 = Menu(**{'name':u'POS录入','location':'views/report/pos_input.html'})
    m22 = Menu(**{'name':u'数据补录','location':u'', 'children':[m22_3, m22_4, m22_5, m22_6, m22_7,m22_8, m22_9]})

    add_group_menu_rel(session, groups, m22_3)
    add_group_menu_rel(session, groups, m22_4)
    add_group_menu_rel(session, groups, m22_5)
    add_group_menu_rel(session, groups, m22_6)
    add_group_menu_rel(session, groups, m22_7)
    add_group_menu_rel(session, groups, m22_8)
    add_group_menu_rel(session, groups, m22_9)
    add_group_menu_rel(session, groups, m22)

    
    #预约
    m3_1 = Menu(**{'name':u'存款预约新增','location':'views/appoint/newdepappoint.html'})
    m3_2 = Menu(**{'name':u'本人存款预约查询','location':'views/appoint/selfdepappoint.html'})
    m3_3 = Menu(**{'name':u'存款预约查询','location':'views/appoint/alldepappoint.html'})
    m3_5 = Menu(**{'name':u'存款预约审批','location':'views/appoint/opindepappoint.html'})
    m3_4 = Menu(**{'name':u'预约参数设置','location':'views/performance_appraisal/booking_management/parameter/para_set.html'})
    m3 = Menu(**{'name':u'预约管理','location':u'', 'children':[m3_1,m3_2,m3_3,m3_5,m3_4]})

    add_group_menu_rel(session, groups, m3_4)
    add_group_menu_rel(session, groups, m3_5)
    add_group_menu_rel(session, groups, m3_1)
    add_group_menu_rel(session, groups, m3_2)
    add_group_menu_rel(session, groups, m3_3)
    add_group_menu_rel(session, groups, m3)


    m4_1 = Menu(**{'name':u'参数设置','location':'views/tpara/tparatype.html'})
    m4_2 = Menu(**{'name':u'业务量指标参数','location':'views/performance_appraisal/index_query/parameter/parameter/index.html'})
    m4_3 = Menu(**{'name':u'存贷款流失参数','location':'views/report/large_loss.html'})
    m4 = Menu(**{'name':u'参数管理','location':u'', 'children':[m4_1,m4_2,m4_3]})

    add_group_menu_rel(session, groups, m4_1)
    add_group_menu_rel(session, groups, m4_2)
    add_group_menu_rel(session, groups, m4_3)
    add_group_menu_rel(session, groups, m4)




    session.commit()

