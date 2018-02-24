# -*- coding:utf-8 -*-

import unittest
from ..database import simple_session, Base
from ..model.branch import Branch,BranchGroup
from ..model.permission import *
from ..base.utils import to_md5
from ..model.user import *
from ..model.t_para import *
import xlrd
import logging
from os import *

class TestBasicSalary(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()
    
    def test_add_salary_para(self):
        self.add_t_para_type()
        self.add_t_para_header()

    def add_t_para_type(self):
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '支行（部）业务经营管理等级指标标准值和等级值参数').first()
        if not ParaType1:
            paratype1 = T_Para_Type(type_status = '启用', type_name = '支行（部）业务经营管理等级指标标准值和等级值参数', type_key = 'ZHYWJYGL', type_detail= '该参数是指支行（部）业务经营管理等级指标标准值和等级值参数', type_module = '等级参数')
            self.session.add(paratype1)
            self.session.flush()

        ParaType2 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '支行（部）业务经营管理等级指标权重参数').first()
        if not ParaType2:
            paratype2 = T_Para_Type(type_status = '启用', type_name = '支行（部）业务经营管理等级指标权重参数', type_key = 'ZHYWJYGLQZ', type_detail= '该参数是指支行（部）业务经营管理等级指标权重参数', type_module = '等级参数')
            self.session.add(paratype2)
            self.session.flush()

        ParaType3 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '支行（部）业务经营管理等级划分参数').first()
        if not ParaType3:
            paratype3 = T_Para_Type(type_status = '启用', type_name = '支行（部）业务经营管理等级划分参数', type_key = 'ZHGLDJHF', type_detail= '该参数是指支行（部）业务经营管理等级划分参数', type_module = '等级参数')
            self.session.add(paratype3)
            self.session.flush()

        ParaType4 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '国际业务部全省排名上升参数').first()
        if not ParaType4:
            paratype4 = T_Para_Type(type_status = '启用', type_name = '国际业务部全省排名上升参数', type_key = 'GJQSPMSS', type_detail= '该参数是指国际业务部全省排名上升参数', type_module = '等级参数')
            self.session.add(paratype4)
            self.session.flush()



        self.session.commit()

    def add_t_para_header(self):
        ###
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '支行（部）业务经营管理等级指标标准值和等级值参数').first()

        ParaHeader1 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '等级值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader1:
            paraHeader1 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'int',  header_name = '等级值', header_key = 'branch_score', header_order = '1')
            self.session.add(paraHeader1)

        ParaHeader2 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '年度日均存款总量（亿元）最小值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader2:
            paraHeader2 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '年度日均存款总量（亿元）最小值', header_key = 'min_ave_dbal_year', header_order = '2')
            self.session.add(paraHeader2)

        ParaHeader3=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '年度日均存款总量（亿元）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader3:
            paraHeader3=T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '年度日均存款总量（亿元）最大值（包含）', header_key = 'max_ave_dbal_year', header_order = '3')
            self.session.add(paraHeader3)
        
        ParaHeader4=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '人均日均存款量（万元）最小值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader4:
            paraHeader4 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '人均日均存款量（万元）最小值', header_key = 'min_ave_dloan', header_order = '4')
            self.session.add(paraHeader4)
            
        ParaHeader5=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '人均日均存款量（万元）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader5:
            paraHeader5 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '人均日均存款量（万元）最大值（包含）', header_key = 'max_ave_dloan', header_order = '5')
            self.session.add(paraHeader5)

        ParaHeader6=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '年度日均贷款总量（亿元）最小值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader6:
            paraHeader6 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '年度日均贷款总量（亿元）最小值', header_key = 'min_ave_dloan_year', header_order = '6')
            self.session.add(paraHeader6)

        ParaHeader7=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '年度日均贷款总量（亿元）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader7:
            paraHeader7 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '年度日均贷款总量（亿元）最大值（包含）', header_key = 'max_ave_dloan_year', header_order = '7')
            self.session.add(paraHeader7)

        ParaHeader8=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '年度人均利润（万元）最小值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader8:
            paraHeader8 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '年度人均利润（万元）最小值', header_key = 'min_ave_profit_year', header_order = '8')
            self.session.add(paraHeader8)

        ParaHeader9=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '年度人均利润（万元）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader9:
            paraHeader9 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '年度人均利润（万元）最大值（包含）', header_key = 'max_ave_profit_year', header_order = '9')
            self.session.add(paraHeader9)

        ParaHeader10=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '年度营业收入（亿元）最小值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader10:
            paraHeader10 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '年度营业收入（亿元）最小值', header_key = 'min_income_year', header_order = '10')
            self.session.add(paraHeader10)

        ParaHeader11=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '年度营业收入（亿元）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader11:
            paraHeader11 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '年度营业收入（亿元）最大值（包含）', header_key = 'max_income_year', header_order = '11')
            self.session.add(paraHeader11)

        ParaHeader12=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '国际结算量（万美元）最小值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader12:
            paraHeader12 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '国际结算量（万美元）最小值', header_key = 'min_inter_set', header_order = '12')
            self.session.add(paraHeader12)

        ParaHeader13=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '国际结算量（万美元）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader13:
            paraHeader13 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '国际结算量（万美元）最大值（包含）', header_key = 'max_inter_set', header_order = '13')
            self.session.add(paraHeader13)

        ParaHeader14=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '电子银行开户数（户）最小值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader14:
            paraHeader14 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'int',  header_name = '电子银行开户数（户）最小值', header_key = 'min_ebank_account_num', header_order = '14')
            self.session.add(paraHeader14)

        ParaHeader15=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '电子银行开户数（户）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader15:
            paraHeader15 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'int',  header_name = '电子银行开户数（户）最大值（包含）', header_key = 'max_ebank_account_num', header_order = '15')
            self.session.add(paraHeader15)

        ParaHeader16=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '贷记卡发卡量（张）最小值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader16:
            paraHeader16 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'int',  header_name = '贷记卡发卡量（张）最小值', header_key = 'min_credit_card_num', header_order = '16')
            self.session.add(paraHeader16)

        ParaHeader17=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '贷记卡发卡量（张）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader17:
            paraHeader17 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'int',  header_name = '贷记卡发卡量（张）最大值（包含）', header_key = 'max_credit_card_num', header_order = '17')
            self.session.add(paraHeader17)

        ParaHeader18=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '贷款户数（户）最小值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader18:
            paraHeader18 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'int',  header_name = '贷款户数（户）最小值', header_key = 'min_loan_num', header_order = '18')
            self.session.add(paraHeader18)

        ParaHeader19=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '贷款户数（户）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader19:
            paraHeader19 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'int',  header_name = '贷款户数（户）最大值（包含）', header_key = 'max_loan_num', header_order = '19')
            self.session.add(paraHeader19)

        ParaHeader20=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '电子银行替代率（%）最小值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader20:
            paraHeader20 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '电子银行替代率（%）最小值', header_key = 'min_ebank_sub_rate', header_order = '20')
            self.session.add(paraHeader20)

        ParaHeader21=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '电子银行替代率（%）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader21:
            paraHeader21 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '电子银行替代率（%）最大值（包含）', header_key = 'max_ebank_sub_rate', header_order = '21')
            self.session.add(paraHeader21)

        ParaHeader22=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '支行贷款户日均贷款挂钩率（%）最小值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader22:
            paraHeader22 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '支行贷款户日均贷款挂钩率（%）最小值', header_key = 'min_branch_ave_hook', header_order = '22')
            self.session.add(paraHeader22)

        ParaHeader23=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '支行贷款日均存贷挂钩率（%）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader23:
            paraHeader23 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '支行贷款日均存贷挂钩率（%）最大值（包含）', header_key = 'max_branch_ave_hook', header_order = '23')
            self.session.add(paraHeader23)

        ParaHeader24=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '四级不良贷款率（%）最小值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader24:
            paraHeader24 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '四级不良贷款率（%）最小值', header_key = 'min_FOR_GRAD_BAD_rate', header_order = '24')
            self.session.add(paraHeader24)

        ParaHeader25=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '四级不良贷款率（%）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader25:
            paraHeader25 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '四级不良贷款率（%）最大值（包含）', header_key = 'max_FOR_GRAD_BAD_rate', header_order = '25')
            self.session.add(paraHeader25)

        ParaType2 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '支行（部）业务经营管理等级指标权重参数').first()

        ParaHeader26=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '序号').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader26:
            paraHeader26 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'int',  header_name = '序号', header_key = 'branch_id', header_order = '1')
            self.session.add(paraHeader26)

        ParaHeader27=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '指标名称').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader27:
            paraHeader27 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '指标名称', header_key = 'branch_target_name', header_order = '2')
            self.session.add(paraHeader27)

        ParaHeader28=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '权重（%）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader28:
            paraHeader28 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '权重（%）', header_key = 'branch_weight', header_order = '3')
            self.session.add(paraHeader28)


        ParaType3 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '支行（部）业务经营管理等级划分参数').first()

        ParaHeader29=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '序号').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader29:
            paraHeader29 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'int',  header_name = '序号', header_key = 'branch_id', header_order = '1')
            self.session.add(paraHeader29)

        ParaHeader30=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '得分最小值').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader30:
            paraHeader30 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'decimal',  header_name = '得分最小值', header_key = 'min_branch_score', header_order = '2')
            self.session.add(paraHeader30)

        ParaHeader31=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '得分最大值').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader31:
            paraHeader31 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'decimal',  header_name = '得分最大值', header_key = 'max_branch_score', header_order = '3')
            self.session.add(paraHeader31)

        ParaHeader32=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '等级').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader32:
            paraHeader32 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'varchar',  header_name = '等级', header_key = 'branch_grade', header_order = '4')
            self.session.add(paraHeader32)


        ParaType4 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '国际业务部全省排名上升参数').first()

        ParaHeader33=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '参数名称').filter(T_Para_Header.para_type_id == ParaType4.id).first()
        if not ParaHeader33:
            paraHeader33=T_Para_Header(para_type_id = ParaType4.id, header_status = '启用', header_type = 'varchar',  header_name = '参数名称', header_key = 'branch_param_name', header_order = '1')
            self.session.add(paraHeader33)

        ParaHeader34=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '排名上升（名）').filter(T_Para_Header.para_type_id == ParaType4.id).first()
        if not ParaHeader34:
            paraHeader34=T_Para_Header(para_type_id = ParaType4.id, header_status = '启用', header_type = 'int',  header_name = '排名上升（名）', header_key = 'add_grade', header_order = '2')
            self.session.add(paraHeader34)






        self.session.commit()

