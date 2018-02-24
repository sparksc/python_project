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
        self.add_t_para_type(self):
        self.add_t_para_header(self):
        self.add_basic_salary_para(self):
        self.add_user_group_para()
        self.add_user_salary_para()

    def add_basic_salary_para(self):
        workbook = xlrd.open_workbook(environ['HOME'] + '/trunk/doc/salary.xlsx')
        sheet = workbook.sheet_by_index(0)
        i = 1
        for row in range(3, 14):
            cols = list()
            for col in range(0, sheet.ncols):
                cols.append(sheet.cell(row, col).value)

            print cols 
            self.add_t_para_detail(cols, i)
            i = i + 1

    def add_user_salary_para(self):
        workbook = xlrd.open_workbook(environ['HOME'] + '/trunk/doc/level.xlsx')
        sheet = workbook.sheet_by_index(0)
        for row in range(2, 422):
            cols = list()
            for col in range(0, sheet.ncols):
                cols.append(sheet.cell(row, col).value)

            print cols 
            self.add_user_group(cols)

        self.session.commit()

    def add_user_group_para(self):
        ##增加岗位、职级、等级
        Group_Type1 = self.session.query(GroupType).filter(GroupType.type_code == '8000').filter(GroupType.type_name =='岗位').first()
        if not Group_Type1:
            Group_Type1 = GroupType(type_code = '8000', type_name = '岗位')
            self.session.add(Group_Type1)
            self.session.flush()

        Group_Type2 = self.session.query(GroupType).filter(GroupType.type_code == '7000').filter(GroupType.type_name == '职级').first()
        if not Group_Type2:
            Group_Type2 = GroupType(type_code = '7000', type_name = '职级')
            self.session.add(Group_Type2)
            self.session.flush()

        Group_Type3 = self.session.query(GroupType).filter(GroupType.type_code == '600').filter(GroupType.type_name == '等级').first()
        if not Group_Type3:
            Group_Type3 = GroupType(type_code = '6000', type_name = '等级')
            self.session.add(Group_Type3)
            self.session.flush()

        name1 = [u'总经理岗位', u'副总经理岗位', u'部室分理处岗位', u'管理类岗位', u'操作类岗位', '支行行长岗位', '支行副行长岗位', '分理处主任岗位', '会计主管岗位', '客户经理岗位', '柜员岗位']
        self.add_group(Group_Type1, name1)

        name2 = [u'一档', u'二档', u'三档', u'四档', u'五档']
        self.add_group(Group_Type2, name2)

        name3 = [u'一级', u'二级', u'三级', u'四级', u'见习', u'二星级', u'三星级', u'四星级', u'五星级', u'资深', u'高级', u'中级', u'初级']
        self.add_group(Group_Type3, name3)
        self.session.commit()

    def add_user_group(self, cols):
        user = self.session.query(User).filter(User.name == cols[3]).first()
        if not user:
            return
        
        if str(cols[4].encode('UTF-8')) == 0:
            position = ''
        else:
            position = cols[4] + u'岗位'

        if len(str(cols[6])) == 0:
            grade = ''
        elif int(cols[6]) == 1:
            grade = '一档'
        elif int(cols[6]) == 2: 
            grade = '二档'
        elif int(cols[6]) == 3: 
            grade = '三档'
        elif int(cols[6]) == 4: 
            grade = '四档'
        elif int(cols[6]) == 5: 
            grade = '五档'
        else:
            grade = ''

        if type(cols[5]) == unicode:
            if str(cols[5].encode('UTF-8')) == 0:
                level = ''
            else:
                level = cols[5]
        else:
            level = ''

        print position, level, grade

        Group1 = self.session.query(Group).filter(Group.group_type_code == '6000').filter(Group.group_name == position).first()
        if not Group1:
            print "岗位类型并没有", position
        else:
            UserGroup1 = self.session.query(UserGroup).filter(UserGroup.user_id == user.role_id).filter(UserGroup.group_id == Group1.id).first()
            if not UserGroup1:
                UserGroup1 = UserGroup(user_id = user.role_id, group_id = Group1.id, startdate = '20161107')
                self.session.add(UserGroup1)
                self.session.flush()

        Group2 = self.session.query(Group).filter(Group.group_type_code == '7000').filter(Group.group_name == grade).first()
        if not Group2:
            print "职级类型并没有", grade
        else:
            UserGroup2 = self.session.query(UserGroup).filter(UserGroup.user_id == user.role_id).filter(UserGroup.group_id == Group2.id).first()
            if not UserGroup2:
                UserGroup2 = UserGroup(user_id = user.role_id, group_id = Group2.id, startdate = '20161107')
                self.session.add(UserGroup2)
                self.session.flush()

        Group3 = self.session.query(Group).filter(Group.group_type_code == '8000').filter(Group.group_name == level).first()
        if not Group3:
            print "等级类型并没有", level
        else:
            UserGroup3 = self.session.query(UserGroup).filter(UserGroup.user_id == user.role_id).filter(UserGroup.group_id == Group3.id).first()
            if not UserGroup3:
                UserGroup3 = UserGroup(user_id = user.role_id, group_id = Group3.id, startdate = '20161107')
                self.session.add(UserGroup3)
                self.session.flush()



    def add_t_para_type(self):
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '固定薪酬职务工资参数').first()
        if not ParaType1:
            paratype1 = T_Para_Type(type_status = '启用', type_name = '固定薪酬职务工资参数', type_key = 'GDXCZWGZ', type_detail= '该参数是指定固定薪酬职务工资', type_module = '薪酬参数')
            self.session.add(paratype1)
            self.session.flush()

        ParaType2 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '固定薪酬职级工资参数').first()
        if not ParaType2:
            paratype2 = T_Para_Type(type_status = '启用', type_name = '固定薪酬职级工资参数', type_key = 'GDXCZJGZ', type_detail= '该参数是指定固定薪酬职级工资', type_module = '薪酬参数')
            self.session.add(paratype2)
            self.session.flush()

        ParaType3 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '固定薪酬等级工资参数').first()
        if not ParaType3:
            paratype3 = T_Para_Type(type_status = '启用', type_name = '固定薪酬等级工资参数', type_key = 'GDXCDJGZ', type_detail= '该参数是指定固定薪酬等级工资', type_module = '薪酬参数')
            self.session.add(paratype3)
            self.session.flush()

        self.session.commit()

    def add_t_para_header(self):
        ###职务工资参数添加
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '固定薪酬职务工资参数').first()

        ParaHeader1 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '职务').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader1:
            paraHeader1 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'varchar',  header_name = '职务', header_key = 'name', header_order = '1')
            self.session.add(paraHeader1)
            self.session.flush()

        ParaHeader2 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '工资').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        if not ParaHeader2:
            paraHeader2 = T_Para_Header(para_type_id = ParaType1.id, header_status = '启用', header_type = 'decimal',  header_name = '工资', header_key = 'price', header_order = '2')
            self.session.add(paraHeader2)
            self.session.flush()
        

        ###职级工资参数添加
        ParaType2 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '固定薪酬职级工资参数').first()

        ParaHeader3 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '职级').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader3:
            paraHeader3 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'varchar',  header_name = '职级', header_key = 'name', header_order = '1')
            self.session.add(paraHeader3)
            self.session.flush()

        ParaHeader4 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '工资').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        if not ParaHeader4:
            paraHeader4 = T_Para_Header(para_type_id = ParaType2.id, header_status = '启用', header_type = 'decimal',  header_name = '工资', header_key = 'price', header_order = '2')
            self.session.add(paraHeader4)


        ###等级工资参数添加
        ParaType3 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '固定薪酬等级工资参数').first()

        ParaHeader5 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '等级').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader5:
            paraHeader5 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'varchar',  header_name = '等级', header_key = 'name', header_order = '1')
            self.session.add(paraHeader5)
            self.session.flush()

        ParaHeader6 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '工资').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        if not ParaHeader6:
            paraHeader6 = T_Para_Header(para_type_id = ParaType3.id, header_status = '启用', header_type = 'decimal',  header_name = '工资', header_key = 'price', header_order = '2')
            self.session.add(paraHeader6)

        self.session.commit()

    def add_t_para_detail(self, cols, i):
        ###添加职务工资的详细参数
        ParaType1 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '固定薪酬职务工资参数').first()
        ParaHeader1 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '职务').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        ParaHeader2 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '工资').filter(T_Para_Header.para_type_id == ParaType1.id).first()
        self.add_t_para_detail_one(ParaType1, ParaHeader1, ParaHeader2, i, cols[0], cols[1])

        ###添加职级工资的详细参数
        ParaType2 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '固定薪酬职级工资参数').first()
        ParaHeader3 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '职级').filter(T_Para_Header.para_type_id == ParaType2.id).first()
        ParaHeader4 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '工资').filter(T_Para_Header.para_type_id == ParaType2.id).first()

        if i == 1:
            order = i
        else:
            order = (i - 1) * 5 + 1

        position = cols[0]
        self.add_t_para_detail_one(ParaType2, ParaHeader3, ParaHeader4, order, (position + u'一档'), cols[2])
        self.add_t_para_detail_one(ParaType2, ParaHeader3, ParaHeader4, order + 1, (position + u'二档'), cols[3])
        self.add_t_para_detail_one(ParaType2, ParaHeader3, ParaHeader4, order + 2, (position + u'三档'), cols[4])
        self.add_t_para_detail_one(ParaType2, ParaHeader3, ParaHeader4, order + 3, (position + u'四档'), cols[5])
        self.add_t_para_detail_one(ParaType2, ParaHeader3, ParaHeader4, order + 4, (position + u'五档'), cols[6])

        ###添加等级工资的详细参数
        ParaType3 = self.session.query(T_Para_Type).filter(T_Para_Type.type_name == '固定薪酬等级工资参数').first()
        ParaHeader5 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '等级').filter(T_Para_Header.para_type_id == ParaType3.id).first()
        ParaHeader6 = self.session.query(T_Para_Header).filter(T_Para_Header.header_name == '工资').filter(T_Para_Header.para_type_id == ParaType3.id).first()

        if position == u'客户经理':
            level1 =  position + u'资深'
            level2 =  position + u'高级'
            level3 =  position + u'中级'
            level4 =  position + u'初级'
            level5 =  position + u'见习'
        elif position ==  u'柜员':
            level1 =  position + u'五星级'
            level2 =  position + u'四星级'
            level3 =  position + u'三星级'
            level4 =  position + u'二星级'
            level5 =  position + u'见习'
        else:
            level1 =  position + u'一级'
            level2 =  position + u'二级'
            level3 =  position + u'三级'
            level4 =  position + u'四级'
            level5 =  position + u'见习'

        self.add_t_para_detail_one(ParaType3, ParaHeader5, ParaHeader6, order, level1, cols[7])
        self.add_t_para_detail_one(ParaType3, ParaHeader5, ParaHeader6, order + 1, level2, cols[8])
        self.add_t_para_detail_one(ParaType3, ParaHeader5, ParaHeader6, order + 2, level3, cols[9])
        self.add_t_para_detail_one(ParaType3, ParaHeader5, ParaHeader6, order + 3, level4, cols[10])
        self.add_t_para_detail_one(ParaType3, ParaHeader5, ParaHeader6, order + 4, level5, cols[11])

        self.session.commit()

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
            return

        ParaRow = self.session.query(T_Para_Row).filter(T_Para_Row.para_type_id == para_type.id).filter(T_Para_Row.row_num == order).first()
        if not ParaRow:
            ParaRow = T_Para_Row(para_type_id = para_type.id, row_num = order, row_status = '启用', row_start_date = '2016-11-07',  row_end_date = '3000-12-31')
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

    def add_group(self, GroupType, lists):
        for v in lists:
            print v
            Group1 = self.session.query(Group).filter(Group.group_type_code == GroupType.type_code).filter(Group.group_name == v).first()
            if not Group1:
                Group1 = Group(group_type_code = GroupType.type_code, group_name = v)
                self.session.add(Group1)
                self.session.flush()
