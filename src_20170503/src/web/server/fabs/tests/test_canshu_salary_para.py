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
    
    def test_add_basic_salary_para(self):
        workbook = xlrd.open_workbook(environ['HOME'] + '/src/sql/execl/new_salary.xlsx')
        sheet = workbook.sheet_by_index(0)
        i = 143
        for row in range(2, 59):
            cols = list()
            for col in range(0, sheet.ncols):
                cols.append(sheet.cell(row, col).value)

            print cols 
            i=self.add_t_para_detail(cols, i)

    def add_t_para_detail(self, cols, i):
        ###添加职务工资的详细参数
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '固定薪酬职务工资参数').first()
        ParaHeader1 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '职务').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        ParaHeader2 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '工资').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        dute=cols[1].split(',')
        if cols[2]=='':
            for due_i in dute:
                dute_a=due_i
                self.add_t_para_detail_one(ParaType1, ParaHeader1, ParaHeader2, i, dute_a, cols[3])
                i=i+1
        else:
            for due_i in dute:
                dute_a=due_i+'-'+cols[2]
                self.add_t_para_detail_one(ParaType1, ParaHeader1, ParaHeader2, i, dute_a, cols[3])
                i=i+1

        ###添加等级工资的详细参数

        ParaType2 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '固定薪酬等级工资参数').first()
        ParaHeader3 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '等级').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        ParaHeader4 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '工资').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if cols[2]=='':
            for due_i in dute:
                dute_a=due_i
                self.add_t_para_detail_one(ParaType2, ParaHeader3, ParaHeader4, i, dute_a, cols[4])
                i=i+1

        else:
            for due_i in dute:
                dute_a=due_i+'-'+cols[2]
                self.add_t_para_detail_one(ParaType2, ParaHeader3, ParaHeader4, i, dute_a, cols[4])
                i=i+1

        self.session.commit()
        return i

    def add_t_para_detail_one(self, para_type, para_header_name, para_header_price, order, name, price):
        if not para_type:
            return
        if not para_header_name:
            return
        if not para_header_price:
            return
        if order < 0: 
            return
        if len(name) == 0: 
            return
        if len(str(price)) == 0: 
            price=0

        ParaRow = self.session.query(T_Para_Row).filter(T_Para_Row.para_type_id == para_type.id).filter(T_Para_Row.row_num == order).first()
        if not ParaRow:
            ParaRow = T_Para_Row(para_type_id = para_type.id, row_num = order, row_status = '启用', row_start_date = '2016-12-01',  row_end_date = '3000-12-31')
            self.session.add(ParaRow)
            self.session.flush()

        ParaDetail_name = self.session.query(T_Para_Detail).filter(T_Para_Detail.para_header_id == para_header_name.id).filter(T_Para_Detail.para_row_id == ParaRow.id).first()
        if not ParaDetail_name:
            paraDetail_name = T_Para_Detail(para_header_id = para_header_name.id, para_row_id = ParaRow.id, detail_value = name, detail_key = 'name')
            self.session.add(paraDetail_name)
            self.session.flush()

        ParaDetail_price = self.session.query(T_Para_Detail).filter(T_Para_Detail.para_header_id == para_header_price.id).filter(T_Para_Detail.para_row_id == ParaRow.id).first()
        if not ParaDetail_price:
            paraDetail_price = T_Para_Detail(para_header_id = para_header_price.id, para_row_id = ParaRow.id, detail_value = str(float(price)), detail_key = 'price')
            self.session.add(paraDetail_price)
            self.session.flush()

