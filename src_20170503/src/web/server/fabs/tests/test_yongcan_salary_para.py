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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class TestBasicSalary(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()
    
    def test_add_salary_para(self):
        self.add_user_group_para()
        self.add_user_salary_para()

    def add_user_salary_para(self):
        workbook = xlrd.open_workbook('/home/develop' + '/src/sql/execl/lcvel.xls')
        sheet = workbook.sheet_by_index(0)
        for row in range(1, 598):
            cols = list()
            for col in range(0, sheet.ncols):
                cols.append(sheet.cell(row, col).value)

            self.add_user_group(cols)

        self.session.commit()

    def add_user_group_para(self):
        ##增加岗位、职级、等级
        Group_Type1 = self.session.query(GroupType).filter(GroupType.type_code == '1000').filter(GroupType.type_name =='职务').first()
        if not Group_Type1:
            Group_Type1 = GroupType(type_code = '1000', type_name = '职务')
            self.session.add(Group_Type1)
            self.session.flush()

        Group_Type3 = self.session.query(GroupType).filter(GroupType.type_code == '6000').filter(GroupType.type_name == '等级').first()
        if not Group_Type3:
            Group_Type3 = GroupType(type_code = '6000', type_name = '等级')
            self.session.add(Group_Type3)
            self.session.flush()

        name1 = [u'行长(总经理)', u'副行长(主持)', u'副行长', u'行长助理', u'副行长(兼网点主任)', u'二级支行副行长(主持)', u'委派会计主管(副股级)', u'委派会计主管', u'委派风险经理', u'行长助理(兼网点主任)', u'分理处主任',u'客户经理',u'大堂经理',u'大堂经理(享受副股级)',u'助理会计',u'综合柜员',u'一般员工',u'见习人员',u'后勤人员',u'集中加钞员',u'借用人员',u'存款类客户经理',u'派遣柜员',u'大堂引导员',u'外聘客户经理',u'试用期人员',u'外包人员',u'其他人员']
        self.add_group(Group_Type1, name1)

        name3 = [u'特级', u'1级', u'2级', u'3级', u'4级', u'5级', u'6级', u'7级', u'一级', u'二级', u'三级', u'资深客户经理', u'高级客户经理', u'中级客户经理', u'初级客户经理', u'助理客户经理', u'资深柜员', u'高级柜员', u'中级柜员', u'初级柜员', u'助理柜员',u'四级',u'五级',u'六级',u'七级']
        self.add_group(Group_Type3, name3)


    def add_user_group(self, cols):
        cols[1]=str(int(cols[1]))
        if len(cols[1])>6:
            user = self.session.query(User).filter(User.user_name == cols[1]).first()
            if not user:
                return
            position=cols[2]
            grade=cols[3]

            if type(grade) == unicode:
                if str(grade.encode('UTF-8')) == 0:
                    level = ''
                else:
                    grade = grade.encode('UTF-8')

            Group1 = self.session.query(Group).filter(Group.group_type_code == '1000').filter(Group.group_name == position).first()
            if not Group1:
                print "职务类型并没有", position
            #else:
            #    UserGroup1 = self.session.query(UserGroup).filter(UserGroup.user_id == user.role_id).filter(UserGroup.group_id == Group1.id).first()
            #    if not UserGroup1:
            #        UserGroup1 = UserGroup(user_id = user.role_id, group_id = Group1.id, startdate = '20161201')
            #        self.session.add(UserGroup1)
            #        self.session.flush()
            sql='''
            select g.group_name from F_USER a
            join USER_GROUP b
            on a.role_id=b.user_id
            join group g on b.group_id=g.id
            join group_type f on g.group_type_code=f.type_code
            where f.type_code=1000 and a.user_name='%s'
            '''%(cols[1])
            is_position=self.session.execute(sql).fetchone()
            position=position.encode('UTF-8')
            if is_position[0] == position:
                Group3 = self.session.query(Group).filter(Group.group_type_code == '6000').filter(Group.group_name == grade).first()
                if not Group3:
                    print "等级类型并没有", grade
                else:
                    UserGroup3 = self.session.query(UserGroup).filter(UserGroup.user_id == user.role_id).filter(UserGroup.group_id == Group3.id).first()
                    if not UserGroup3:
                        UserGroup3 = UserGroup(user_id = user.role_id, group_id = Group3.id, startdate = '20161201')
                        self.session.add(UserGroup3)
                        self.session.flush()
            else:
                
                zz=str(cols[1])+'\t'+str(cols[0])+'\t'+"旧职务:"+position+'\t'+'新职务:'+is_position[0]
                print zz
        else: 
            position=cols[2]
            if position ==u'支行':
                cols[1]='M'+cols[1]
                print cols[1]
                branch = self.session.query(Branch).filter(Branch.branch_code == cols[1]).first()
                print branch
                if not branch:
                    return
                grade=cols[3]
                if type(grade) == unicode:
                    if str(grade.encode('UTF-8')) == 0:
                        level = ''
                    else:
                        grade = grade.encode('UTF-8')

                print position,cols[1] ,grade
                self.session.query(Branch).filter(Branch.branch_code == cols[1]).update({Branch.deg_level:grade})
            elif position==u'网点':
                branch = self.session.query(Branch).filter(Branch.branch_code == cols[1]).first()
                if not branch:
                    return
                grade=cols[3]
                if type(grade) == unicode:
                    if str(grade.encode('UTF-8')) == 0:
                        level = ''
                    else:
                        grade = grade.encode('UTF-8')
                print position, cols[1],grade
                self.session.query(Branch).filter(Branch.branch_code == cols[1]).update({Branch.deg_level:grade})
            
        self.session.commit()

    def add_group(self, GroupType, lists):
        for v in lists:
            Group1 = self.session.query(Group).filter(Group.group_type_code == GroupType.type_code).filter(Group.group_name == v).first()
            if not Group1:
                Group1 = Group(group_type_code = GroupType.type_code, group_name = v)
                self.session.add(Group1)
                self.session.flush()
