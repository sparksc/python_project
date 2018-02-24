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
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '网点业务经营管理等级指标标准值和等级值参数').first()
        if not ParaType1:
            paratype1 = T_Para_Type(type_status = '启用', type_name = '网点业务经营管理等级指标标准值和等级值参数', type_key = 'WDDJCS', type_detail= '该参数是指网点业务经营管理等级指标标准值和等级值参数', type_module = '等级参数')
            self.session.add(paratype1)
            self.session.flush()

        ParaType2 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '网点经营管理等级指标权重参数').first()
        if not ParaType2:
            paratype2 = T_Para_Type(type_status = '启用', type_name = '网点经营管理等级指标权重参数', type_key = 'WDDJQZ', type_detail= '该参数是指网点经营管理等级指标权重参数', type_module = '权重参数')
            self.session.add(paratype2)
            self.session.flush()

        ParaType3 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '网点业务经营管理等级划分参数').first()
        if not ParaType3:
            paratype3 = T_Para_Type(type_status = '启用', type_name = '网点业务经营管理等级划分参数', type_key = 'WDGLDJHF', type_detail= '该参数是指网点业务经营管理等级划分参数', type_module = '等级参数')
            self.session.add(paratype3)
            self.session.flush()


        self.session.commit()

    def add_t_para_header(self):
        ###
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '网点业务经营管理等级指标标准值和等级值参数').first()
        ParaType2 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '网点经营管理等级指标权重参数').first()
        ParaType3 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '网点业务经营管理等级划分参数').first()

        ParaHeader1 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '等级值').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader1:
            paraHeader1 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'int',  header_name = '等级值', header_key = 'WDDJ_Value', header_order = '1')
            self.session.add(paraHeader1)

        ParaHeader2 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '年度日均存款总量（亿元）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader2:
            paraHeader2 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '年度日均存款总量（亿元）最大值（包含）', header_key = 'YCK_MaxTotal', header_order = '2')
            self.session.add(paraHeader2)

        ParaHeader3=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '年度日均存款总量（亿元）最小值（不包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader3:
            paraHeader3=T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '年度日均存款总量（亿元）最小值（不包含）', header_key = 'YCK_MinTotal', header_order = '3')
            self.session.add(paraHeader3)
        
        ParaHeader4=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '人均日均存款量（万元）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader4:
            paraHeader4 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '人均日均存款量（万元）最大值（包含）', header_key = 'RJCK_Max', header_order = '4')
            self.session.add(paraHeader4)
            
        ParaHeader5=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '人均日均存款量（万元）最小值（不包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader5:
            paraHeader5 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '人均日均存款量（万元）最小值（不包含）', header_key = 'RJCK_Min', header_order = '5')
            self.session.add(paraHeader5)

        ParaHeader6=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '年度日均贷款总量（亿元）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader6:
            paraHeader6 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '年度日均贷款总量（亿元）最大值（包含）', header_key = 'YDK_MaxTotal', header_order = '6')
            self.session.add(paraHeader6)

        ParaHeader7=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '年度日均贷款总量（亿元）最小值（不包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader7:
            paraHeader7 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '年度日均贷款总量（亿元）最小值（不包含）', header_key = 'YDK_MinTotal', header_order = '7')
            self.session.add(paraHeader7)

        ParaHeader8=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '电子银行开户数（户）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader8:
            paraHeader8 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'bigint',  header_name = '电子银行开户数（户）最大值（包含）', header_key = 'DZBank_MaxCount', header_order = '8')
            self.session.add(paraHeader8)

        ParaHeader9=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '电子银行开户数（户）最小值（不包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader9:
            paraHeader9 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'bigint',  header_name = '电子银行开户数（户）最小值（不包含）', header_key = 'DZBank_MinCount', header_order = '9')
            self.session.add(paraHeader9)

        ParaHeader10=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '电子银行替代率（%）最大数（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader10:
            paraHeader10 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '电子银行替代率（%）最大数（包含）', header_key = 'DZBank_MaxRate', header_order = '10')
            self.session.add(paraHeader10)

        ParaHeader11=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '电子银行替代率（%）最小数（不包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader11:
            paraHeader11 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '电子银行替代率（%）最小数（不包含）', header_key = 'DZBank_MinRate', header_order = '11')
            self.session.add(paraHeader11)

        ParaHeader12=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '贷款户数（户）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader12:
            paraHeader12 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'bigint',  header_name = '贷款户数（户）最大值（包含）', header_key = 'DK_MaxCount', header_order = '12')
            self.session.add(paraHeader12)

        ParaHeader13=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '贷款户数（户）最小值（不包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader13:
            paraHeader13 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'bigint',  header_name = '贷款户数（户）最小值（不包含）', header_key = 'DK_MinCount', header_order = '13')
            self.session.add(paraHeader13)

        ParaHeader14=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '网点贷款户日均存贷挂钩率（%）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader14:
            paraHeader14 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '网点贷款户日均存贷挂钩率（%）最大值（包含）', header_key = 'RJCK_MaxRate', header_order = '14')
            self.session.add(paraHeader14)

        ParaHeader15=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '网点贷款户日均存贷挂钩率（%）最小值（不包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader15:
            paraHeader15 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '网点贷款户日均存贷挂钩率（%）最小值（不包含）', header_key = 'RJCK_MinRate', header_order = '15')
            self.session.add(paraHeader15)

        ParaHeader16=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '四级不良贷款率（%）最大值（包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader16:
            paraHeader16 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '四级不良贷款率（%）最大值（包含）', header_key = 'SJBL_MaxRate', header_order = '16')
            self.session.add(paraHeader16)

        ParaHeader17=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '四级不良贷款率（%）最小值（不包含）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader17:
            paraHeader17 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '四级不良贷款率（%）最小值（不包含）', header_key = 'SJBL_MinRate', header_order = '17')
            self.session.add(paraHeader17)

        ParaHeader18=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '序号').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader18:
            paraHeader18 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'int',  header_name = '序号', header_key = 'WDQZXH', header_order = '1')
            self.session.add(paraHeader18)

        ParaHeader19=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '指标名称').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader19:
            paraHeader19 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'varchar',  header_name = '指标名称', header_key = 'QDQZ_Name', header_order = '2')
            self.session.add(paraHeader19)

        ParaHeader20=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '权重').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader20:
            paraHeader20= T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '权重', header_key = 'WD_GWeight', header_order = '3')
            self.session.add(paraHeader20)

        ParaHeader21=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '序号').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader21:
            paraHeader21=T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'int',  header_name = '序号', header_key = 'WD_ListNum', header_order = '1')
            self.session.add(paraHeader21)

        ParaHeader22=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '得分最大值（包含）').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader22:
            paraHeader22=T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'decimal',  header_name = '得分最大值（包含）', header_key = 'WD_MaxScore', header_order = '2')
            self.session.add(paraHeader22)

        ParaHeader23=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '得分最小值（不包含）').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader23:
            paraHeader23=T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'decimal',  header_name = '得分最小值（不包含）', header_key = 'WD_MinScore', header_order = '3')
            self.session.add(paraHeader23)

        ParaHeader24=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '等级').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader24:
            paraHeader24=T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'varchar',  header_name = '等级', header_key = 'WD_Level', header_order = '4')
            self.session.add(paraHeader24)



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
