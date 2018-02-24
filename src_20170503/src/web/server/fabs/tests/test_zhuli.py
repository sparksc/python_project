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
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '助理会计等级指标权重参数').first()
        if not ParaType1:
            paratype1 = T_Para_Type(type_status = '启用', type_name = '助理会计等级指标权重参数', type_key = 'ZLKJDJ', type_detail= '该参数指助理会计等级指标权重参数', type_module = '权重参数')
            self.session.add(paratype1)
            self.session.flush()

        ParaType2 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '助理会计等级指标标准值和等级值参数').first()
        if not ParaType2:
            paratype2 = T_Para_Type(type_status = '启用', type_name = '助理会计等级指标标准值和等级值参数', type_key = 'ZLKJBZDJ', type_detail= '该参数指助理会计等级指标标准值和等级值参数', type_module = '等级参数')
            self.session.add(paratype2)
            self.session.flush()

        ParaType3 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '助理会计等级划分参数').first()
        if not ParaType3:
            paratype3 = T_Para_Type(type_status = '启用', type_name = '助理会计等级划分参数', type_key = 'ZLKJDJHF', type_detail= '该参数指助理会计等级划分参数', type_module = '等级参数')
            self.session.add(paratype3)
            self.session.flush()

        ParaType4 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '助理会计附加分最高值参数').first()
        if not ParaType4:
            paratype1 = T_Para_Type(type_status = '启用', type_name = '助理会计附加分最高值参数', type_key = 'ZLKJFJF', type_detail= '该参数指助理会计附加分最高值参数', type_module = '得分参数')
            self.session.add(paratype1)
            self.session.flush()

        self.session.commit()

    def add_t_para_header(self):
        ##助理会计等级指标权重参数
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '助理会计等级指标权重参数').first()

        ParaHeader1 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '序号').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader1:
            paraHeader1 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'int',  header_name = '序号', header_key = 'list_num', header_order = '1')
            self.session.add(paraHeader1)

        ParaHeader2 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '指标名称').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader2:
            paraHeader2 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'varchar',  header_name = '指标名称', header_key = 'target_name', header_order = '2')
            self.session.add(paraHeader2)

        ParaHeader3=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '权重（%）').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader3:
            paraHeader3=T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'int',  header_name = '权重（%）', header_key = 'weight', header_order = '3')
            self.session.add(paraHeader3)
        
        ##助理会计等级指标标准值和等级值参数
        ParaType2 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '助理会计等级指标标准值和等级值参数').first()

        ParaHeader4=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '分值').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader4:
            paraHeader4 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'int',  header_name = '分值', header_key = 'score', header_order = '1')
            self.session.add(paraHeader4)
            
        ParaHeader5=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '支行（部）网点数量（个）最小值（包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader5:
            paraHeader5 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '支行（部）网点数量（个）最小值（包含）', header_key = 'net_lownum', header_order = '2')
            self.session.add(paraHeader5)

        ParaHeader6=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '支行（部）网点数量（个）最大值（不包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader6:
            paraHeader6 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '支行（部）网点数量（个）最大值（不包含）', header_key = 'net_highnum', header_order = '3')
            self.session.add(paraHeader6)

        ParaHeader7=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '支行（部）业务差错率排名（名）最小值（包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader7:
            paraHeader7 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '支行（部）业务差错率排名（名）最小值（包含）', header_key = 'mis_lowrank', header_order = '4')
            self.session.add(paraHeader7)

        ParaHeader8=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '支行（部）业务差错率排名（名）最大值（不包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader8:
            paraHeader8 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '支行（部）业务差错率排名（名）最大值（不包含）', header_key = 'mis_highrank', header_order = '5')
            self.session.add(paraHeader8)

        ParaHeader9=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '支行（部）业务总量排名（名）最小值（包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader9:
            paraHeader9 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '支行（部）业务总量排名（名）最小值（包含）', header_key = 'all_lowrank', header_order = '6')
            self.session.add(paraHeader9)

        ParaHeader10=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '支行（部）业务总量排名（名）最大值（不包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader10:
            paraHeader10 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '支行（部）业务总量排名（名）最大值（不包含）', header_key = 'all_highrank', header_order = '7')
            self.session.add(paraHeader10)

        ParaHeader11=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '支行（部）会计基础等级（级）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader11:
            paraHeader11 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'varchar',  header_name = '支行（部）会计基础等级（级）', header_key = 'basic_rank', header_order = '8')
            self.session.add(paraHeader11)

        ParaHeader12=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '助理会计行龄（年）最小值（包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader12:
            paraHeader12 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '助理会计行龄（年）最小值（包含）', header_key = 'lowyear', header_order = '9')
            self.session.add(paraHeader12)

        ParaHeader13=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '助理会计行龄（年）最大值（不包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader13:
            paraHeader13 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '助理会计行龄（年）最大值（不包含）', header_key = 'highyear', header_order = '10')
            self.session.add(paraHeader13)

        ParaHeader14=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '支行（部）内勤人均违规积分分值排名（名）最小值（包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader14:
            paraHeader14 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '支行（部）内勤人均违规积分分值排名（名）最小值（包含）', header_key = 'integration_lowrank', header_order = '11')
            self.session.add(paraHeader14)

        ParaHeader15=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '支行（部）内勤人均违规积分分值排名（名）最大值（不包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader15:
            paraHeader15 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '支行（部）内勤人均违规积分分值排名（名）最大值（不包含）', header_key = 'integration_highrank', header_order = '12')
            self.session.add(paraHeader15)

        ParaHeader16=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '支行（部）电子银行替代率完成率排名（名）最小值（包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader16:
            paraHeader16 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '支行（部）电子银行替代率完成率排名（名）最小值（包含）', header_key = 'etc_lowrank', header_order = '13')
            self.session.add(paraHeader16)

        ParaHeader17=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '支行（部）电子银行替代率完成率排名（名）最大值（不包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader17:
            paraHeader17 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '支行（部）电子银行替代率完成率排名（名）最大值（不包含）', header_key = 'etc_highrank', header_order = '14')
            self.session.add(paraHeader17)

        ParaHeader18=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '助理会计市办业务知识技能达标（级）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader18:
            paraHeader18 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'varchar',  header_name = '助理会计市办业务知识技能达标（级）', header_key = 'knorank', header_order = '15')
            self.session.add(paraHeader18)

        ParaHeader19=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '助理会计文化程度').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader19:
            paraHeader19 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'varchar',  header_name = '助理会计文化程度', header_key = 'edu', header_order = '16')
            self.session.add(paraHeader19)

        ParaHeader20=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '助理会计工作经验（年）最小值（包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader20:
            paraHeader20 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '助理会计工作经验（年）最小值（包含）', header_key = 'low_experience', header_order = '17')
            self.session.add(paraHeader20)

        ParaHeader21=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '助理会计工作经验（年）最大值（不包含）').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader21:
            paraHeader21 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '助理会计工作经验（年）最大值（不包含）', header_key = 'high_experience', header_order = '18')
            self.session.add(paraHeader21)


        ##助理会计等级划分参数

        ParaType3 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '助理会计等级划分参数').first()

        ParaHeader22=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '序号').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader22:
            paraHeader22 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'int',  header_name = '序号', header_key = 'list_num', header_order = '1')
            self.session.add(paraHeader22)
            
        ParaHeader23=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '积分最小值（包含）').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader23:
            paraHeader23 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'decimal',  header_name = '积分最小值（包含）', header_key = 'low_integration', header_order = '2')
            self.session.add(paraHeader23)

        ParaHeader24=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '积分最大值（不包含）').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader24:
            paraHeader24 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'decimal',  header_name = '积分最大值（不包含）', header_key = 'high_integration', header_order = '3')
            self.session.add(paraHeader24)

        ParaHeader25=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '等级').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader25:
            paraHeader25 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'varchar',  header_name = '等级', header_key = 'level', header_order = '4')
            self.session.add(paraHeader25)


        ##助理会计附加分最高值参数

        ParaType4 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '助理会计附加分最高值参数').first()

        ParaHeader26=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '参数名称').filter(T_Para_Header.para_type_id == ParaType4.id).first()
        if not ParaHeader26:
            paraHeader26 = T_Para_Header(para_type_id = ParaType4.id, header_status = '启用', header_type = 'varchar',  header_name = '参数名称', header_key = 'name', header_order = '1')
            self.session.add(paraHeader26)
            
        ParaHeader27=self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '参数值').filter(T_Para_Header.para_type_id == ParaType4.id).first()
        if not ParaHeader27:
            paraHeader27 = T_Para_Header(para_type_id = ParaType4.id, header_status = '启用', header_type = 'decimal',  header_name = '参数值', header_key = 'WD_MaxScore', header_order = '2')
            self.session.add(paraHeader27)


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
