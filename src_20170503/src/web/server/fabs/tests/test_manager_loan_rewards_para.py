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
        #self.add_t_para_type()
        self.add_t_para_header()

    def add_t_para_type(self):
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '客户经理贷款奖励金额参数').first()
        if not ParaType1:
            paratype1 = T_Para_Type(type_status = '启用', type_name = '客户经理贷款奖励金额参数', type_key = 'KHJLDKJLJECS', type_detail= '该参数是指定客户经理贷款奖励金额计算', type_module = '效酬参数')
            self.session.add(paratype1)
            self.session.flush()

        ParaType2 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '客户经理贷款奖励折算参数').first()
        if not ParaType2:
            paratype2 = T_Para_Type(type_status = '启用', type_name = '客户经理贷款奖励折算参数', type_key = 'KHJLDKJLZSCS', type_detail= '该参数是指定客户经理贷款奖励折算计算', type_module = '效酬参数')
            self.session.add(paratype2)
            self.session.flush()

        self.session.commit()

    def add_t_para_header(self):
        ##客户经理贷款奖励金额参数
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '客户经理贷款奖励金额参数').first()

        ParaHeader1 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '不良贷款最小占比').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader1:
            ParaHeader1 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '不良贷款最小占比', header_key = 'price', header_order = '1')
            self.session.add(ParaHeader1)
            self.session.flush()

        ParaHeader2 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '不良贷款最大占比').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader2:
            ParaHeader2 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '不良贷款最大占比', header_key = 'price', header_order = '2')
            self.session.add(ParaHeader2)
            self.session.flush()

        ParaHeader3 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '考察项').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader3:
            ParaHeader3 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'varchar',  header_name = '考察项', header_key = 'name', header_order = '3')
            self.session.add(ParaHeader3)
            self.session.flush()
        
        ParaHeader4 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '最小考察项目数量').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader4:
            ParaHeader4 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '最小考察项目数量', header_key = 'price', header_order = '4')
            self.session.add(ParaHeader4)
            self.session.flush()

        ParaHeader5 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '在全行平均数上浮比例').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader5:
            ParaHeader5 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '在全行平均数上浮比例', header_key = 'price', header_order = '5')
            self.session.add(ParaHeader5)
            self.session.flush()

        ParaHeader6 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '奖励金额').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader6:
            ParaHeader6 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '奖励金额', header_key = 'price', header_order = '6')
            self.session.add(ParaHeader6)
            self.session.flush()

        self.add_t_para_detail_rate(ParaType1, ParaHeader1, ParaHeader2, ParaHeader3, ParaHeader4, ParaHeader5, ParaHeader6, 1, 0, 0.3, '月均责任管贷余额,管贷户数,当年新增户数,当年新增责任贷款额', 2, 30, 3000)
        self.add_t_para_detail_rate(ParaType1, ParaHeader1, ParaHeader2, ParaHeader3, ParaHeader4, ParaHeader5, ParaHeader6, 2, 0.3, 0.5, '月均责任管贷余额,管贷户数,当年新增户数,当年新增责任贷款额', 2, 20, 2000)

        ###客户经理贷款奖励折算参数
        ParaType2 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '客户经理贷款奖励折算参数').first()

        ParaHeader7 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '考察项').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader7:
            ParaHeader7 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'varchar',  header_name = '考察项', header_key = 'name', header_order = '1')
            self.session.add(ParaHeader7)
            self.session.flush()

        ParaHeader8 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '折算类型').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader8:
            ParaHeader8 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'varchar',  header_name = '折算类型', header_key = 'name', header_order = '2')
            self.session.add(ParaHeader8)
            self.session.flush()

        ParaHeader9 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '折算值').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader9:
            ParaHeader9 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '折算值', header_key = 'price', header_order = '3')
            self.session.add(ParaHeader9)
            self.session.flush()

        self.add_t_para_detail_convert(ParaType2, ParaHeader7, ParaHeader8, ParaHeader9, 1, '月均责任管贷余额', '公司类贷款', 70)
        self.add_t_para_detail_convert(ParaType2, ParaHeader7, ParaHeader8, ParaHeader9, 2, '管带户数', '公司类贷款', 15)
        self.add_t_para_detail_convert(ParaType2, ParaHeader7, ParaHeader8, ParaHeader9, 3, '当年新增户数', '公司类贷款', 15)
        self.add_t_para_detail_convert(ParaType2, ParaHeader7, ParaHeader8, ParaHeader9, 4, '当年新增责任贷款余额', '公司类贷款', 70)
        self.add_t_para_detail_convert(ParaType2, ParaHeader7, ParaHeader8, ParaHeader9, 5, '当年日均责任贷款余额', '公司类贷款', 70)

        self.session.commit()

    def add_t_para_detail_rate(self, para_type, para_header1, para_header2, para_header3, para_header4, para_header5, para_header6, order, min_rate, max_rate, values, value_count, percent, money):
        if not para_type:
            return
        if not para_header1:
            return
        if not para_header2:
            return
        if not para_header3:
            return
        if not para_header4:
            return
        if not para_header5:
            return
        if not para_header6:
            return
        if order < 0: 
            return
        if len(str(percent)) == 0: 
            return
        if len(str(money)) == 0: 
            return

        ParaRow = self.session.query(T_Para_Row).filter(T_Para_Row.para_type_id == para_type.id).filter(T_Para_Row.row_num == order).first()
        if not ParaRow:
            ParaRow = T_Para_Row(para_type_id = para_type.id, row_num = order, row_status = '启用', row_start_date = '2017-01-07',  row_end_date = '3000-12-31')
            self.session.add(ParaRow)
            self.session.flush()

        ParaDetail1 = self.session.query(T_Para_Detail).filter(T_Para_Detail.para_header_id == para_header1.id).filter(T_Para_Detail.para_row_id == ParaRow.id).first()
        if not ParaDetail1:
            paraDetail1 = T_Para_Detail(para_header_id = para_header1.id, para_row_id = ParaRow.id, detail_value = str(float(min_rate)), detail_key = 'price')
            self.session.add(paraDetail1)
            self.session.flush()

        ParaDetail2 = self.session.query(T_Para_Detail).filter(T_Para_Detail.para_header_id == para_header2.id).filter(T_Para_Detail.para_row_id == ParaRow.id).first()
        if not ParaDetail2:
            paraDetail2 = T_Para_Detail(para_header_id = para_header2.id, para_row_id = ParaRow.id, detail_value = str(float(max_rate)), detail_key = 'price')
            self.session.add(paraDetail2)
            self.session.flush()

        ParaDetail3 = self.session.query(T_Para_Detail).filter(T_Para_Detail.para_header_id == para_header3.id).filter(T_Para_Detail.para_row_id == ParaRow.id).first()
        if not ParaDetail3:
            paraDetail3 = T_Para_Detail(para_header_id = para_header3.id, para_row_id = ParaRow.id, detail_value = values, detail_key = 'name')
            self.session.add(paraDetail3)
            self.session.flush()

        ParaDetail4 = self.session.query(T_Para_Detail).filter(T_Para_Detail.para_header_id == para_header4.id).filter(T_Para_Detail.para_row_id == ParaRow.id).first()
        if not ParaDetail4:
            paraDetail4 = T_Para_Detail(para_header_id = para_header4.id, para_row_id = ParaRow.id, detail_value = str(int(value_count)), detail_key = 'price')
            self.session.add(paraDetail4)
            self.session.flush()

        ParaDetail5 = self.session.query(T_Para_Detail).filter(T_Para_Detail.para_header_id == para_header5.id).filter(T_Para_Detail.para_row_id == ParaRow.id).first()
        if not ParaDetail5:
            paraDetail5 = T_Para_Detail(para_header_id = para_header5.id, para_row_id = ParaRow.id, detail_value = str(float(percent)), detail_key = 'price')
            self.session.add(paraDetail5)
            self.session.flush()

        ParaDetail6 = self.session.query(T_Para_Detail).filter(T_Para_Detail.para_header_id == para_header6.id).filter(T_Para_Detail.para_row_id == ParaRow.id).first()
        if not ParaDetail6:
            paraDetail6 = T_Para_Detail(para_header_id = para_header6.id, para_row_id = ParaRow.id, detail_value = str(float(money)), detail_key = 'price')
            self.session.add(paraDetail6)
            self.session.flush()

    def add_t_para_detail_convert(self, para_type, para_header1, para_header2, para_header3, order, key, c_type, c_value):
        if not para_type:
            return
        if not para_header1:
            return
        if not para_header2:
            return
        if not para_header3:
            return
        if order < 0: 
            return
        if len(key) == 0: 
            return
        if len(c_type) == 0: 
            return
        if len(str(c_value)) == 0: 
            return

        ParaRow = self.session.query(T_Para_Row).filter(T_Para_Row.para_type_id == para_type.id).filter(T_Para_Row.row_num == order).first()
        if not ParaRow:
            ParaRow = T_Para_Row(para_type_id = para_type.id, row_num = order, row_status = '启用', row_start_date = '2017-01-07',  row_end_date = '3000-12-31')
            self.session.add(ParaRow)
            self.session.flush()

        ParaDetail1 = self.session.query(T_Para_Detail).filter(T_Para_Detail.para_header_id == para_header1.id).filter(T_Para_Detail.para_row_id == ParaRow.id).first()
        if not ParaDetail1:
            paraDetail1 = T_Para_Detail(para_header_id = para_header1.id, para_row_id = ParaRow.id, detail_value = str(key), detail_key = 'name')
            self.session.add(paraDetail1)
            self.session.flush()

        ParaDetail2 = self.session.query(T_Para_Detail).filter(T_Para_Detail.para_header_id == para_header2.id).filter(T_Para_Detail.para_row_id == ParaRow.id).first()
        if not ParaDetail2:
            paraDetail2 = T_Para_Detail(para_header_id = para_header2.id, para_row_id = ParaRow.id, detail_value = str(c_type), detail_key = 'name')
            self.session.add(paraDetail2)
            self.session.flush()

        ParaDetail3 = self.session.query(T_Para_Detail).filter(T_Para_Detail.para_header_id == para_header3.id).filter(T_Para_Detail.para_row_id == ParaRow.id).first()
        if not ParaDetail3:
            paraDetail3 = T_Para_Detail(para_header_id = para_header3.id, para_row_id = ParaRow.id, detail_value = str(float(c_value)), detail_key = 'price')
            self.session.add(paraDetail3)
            self.session.flush()
