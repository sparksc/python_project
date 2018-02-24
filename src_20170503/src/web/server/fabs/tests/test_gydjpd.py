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
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '柜员等级指标权重参数').first()
        if not ParaType1:
            paratype1 = T_Para_Type(type_status = '启用', type_name = '柜员等级指标权重参数', type_key = 'GGDJQZ', type_detail= '该参数指明各个在计算总分时所占的比例', type_module = '权重参数')
            self.session.add(paratype1)
            self.session.flush()

        ParaType2 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '柜员等级指标标准值和等级值参数').first()
        if not ParaType2:
            paratype2 = T_Para_Type(type_status = '启用', type_name = '柜员等级指标标准值和等级值参数', type_key = 'DJZBCS', type_detail= '该参数时计算等级时各个指标的参数', type_module = '等级参数')
            self.session.add(paratype2)
            self.session.flush()

        ParaType3 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '柜员等级划分参数').first()
        if not ParaType3:
            paratype3 = T_Para_Type(type_status = '启用', type_name = '柜员等级划分参数', type_key = 'UserLevel', type_detail= '根据柜员总得分来划分柜员等级', type_module = '等级参数')
            self.session.add(paratype3)
            self.session.flush()

       # ParaType4 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '委派会计主管等级指标权重参数').first()
       # if not ParaType4:
       #     paratype1 = T_Para_Type(type_status = '启用', type_name = '委派会计主管等级指标权重参数', type_key = 'WPKJQZ', type_detail= '该参数是指委派会计主管等级指标权重参数', type_module = '权重参数')
       #     self.session.add(paratype1)
       #     self.session.flush()

        ParaType5 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '委派会计主管附加分最高值参数').first()
        if not ParaType5:
            paratype5 = T_Para_Type(type_status = '启用', type_name = '委派会计主管附加分最高值参数', type_key = 'Max_ExtraScore', type_detail= '该参数指委派会计主管附加分最高值参数', type_module = '得分参数')
            self.session.add(paratype5)
            self.session.flush()

        self.session.commit()


    def add_t_para_header(self):
        ###
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '委派会计主管等级指标权重参数').first()

        ParaHeader1 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '序号').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader1:
            paraHeader1 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'int',  header_name = '序号', header_key = 'Num', header_order = '1')
            self.session.add(paraHeader1)

        ParaHeader2 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '指标名称').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader2:
            paraHeader2 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'varchar',  header_name = '指标名称', header_key = 'target_name', header_order = '2')
            self.session.add(paraHeader2)

        ParaHeader3=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '权重').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader3:
            paraHeader3=T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '权重', header_key = 'weight', header_order = '3')
            self.session.add(paraHeader3)
        
        ParaHeader4=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '序号').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader4:
            paraHeader4 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'int',  header_name = '序号', header_key = 'Num', header_order = '1')
            self.session.add(paraHeader4)
            
        ParaHeader5=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '积分最小值（包含）').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader5:
            paraHeader5 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'decimal',  header_name = '积分最小值（包含）', header_key = 'HF_MINSCOE', header_order = '2')
            self.session.add(paraHeader5)

        ParaHeader6=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '积分最大值（不包含）').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader6:
            paraHeader6 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'decimal',  header_name = '积分最大值（不包含）', header_key = 'HF_MAXSCORE', header_order = '3')
            self.session.add(paraHeader6)

        ParaHeader7=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '等级').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader7:
            paraHeader7 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'varchar',  header_name = '等级', header_key = 'Level', header_order = '4')
            self.session.add(paraHeader7)

        ParaHeader8=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '参数名称').filter(T_Para_Header.para_type_id == ParaType5.id).first()
        if not ParaHeader8:
            paraHeader8 = T_Para_Header(para_type_id = ParaType5.id, header_status = '启用', header_type = 'decimal',  header_name = '参数名称', header_key = 'CS_NAME', header_order = '1')
            self.session.add(paraHeader8)

        ParaHeader9=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '参数值（分）').filter(T_Para_Header.para_type_id == ParaType5.id).first()
        if not ParaHeader9:
            paraHeader9 = T_Para_Header(para_type_id = ParaType5.id, header_status = '启用', header_type = 'decimal',  header_name = '参数值（分）', header_key = 'SCORE', header_order = '2')
            self.session.add(paraHeader9)

        self.session.commit()


#    def add_t_para_detail(self, cols, i):
#        ###添加职务工资的详细参数
#        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '固定薪酬职务工资参数').first()
#        ParaHeader1 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '职务').filter(T_Para_Header.para_type_id == ParaType1.id).first()
#        ParaHeader2 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '工资').filter(T_Para_Header.para_type_id == ParaType1.id).first()
#        self.add_t_para_detail_one(ParaType1, ParaHeader1, ParaHeader2, i, cols[0], cols[1])
#
#        self.session.commit()
#
#    def add_t_para_detail_one(self, para_type, para_header_name, para_header_price, order, name, price):
#
#
#        ParaRow = self.session.query(T_Para_Row).filter(T_Para_Row.para_type_id == para_type.id).filter(T_Para_Row.row_num == order).first()
#        if not ParaRow:
#            ParaRow = T_Para_Row(para_type_id = para_type.id, row_num = order, row_status = '启用', row_start_date = '2016-11-07',  row_end_date = '3000-12-31')
#            self.session.add(ParaRow)
#            self.session.flush()
#
#        ParaDetail_name = self.session.query(T_Para_Detail).filter(T_Para_Detail.para_header_id == para_header_name.id).filter(T_Para_Detail.para_row_id == ParaRow.id).first()
#        if not ParaDetail_name:
#            paraDetail_name = T_Para_Detail(para_header_id = para_header_name.id, para_row_id = ParaRow.id, detail_value = name, detail_key = 'name')
#            self.session.add(paraDetail_name)
#            self.session.flush()
#
#        ParaDetail_price = self.session.query(T_Para_Detail).filter(T_Para_Detail.para_header_id == para_header_price.id).filter(T_Para_Detail.para_row_id == ParaRow.id).first()
#        if not ParaDetail_price:
#            paraDetail_price = T_Para_Detail(para_header_id = para_header_price.id, para_row_id = ParaRow.id, detail_value = str(float(price)), detail_key = 'price')
#            self.session.add(paraDetail_price)
#            self.session.flush()
#
