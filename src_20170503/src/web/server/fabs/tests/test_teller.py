#_*_coding:utf-8_*_

import unittest
from ..database import simple_session, Base
from ..model.branch import Branch,BranchGroup
from ..model.permission import *
from ..base.utils import to_md5
from ..model.user import *
from ..model.mbox import MboxRecord
import xlrd
import xlwt
import logging
from os import environ
import sys
reload(sys)
sys.setdefaultencoding('utf8')

log = logging.getLogger()
class TestTeller(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()
        #init_teller_position()
        #init_teller_data()

    def add_user(self):
        branch = self.session.query(Branch)
        group = self.session.query(Group)
        usr = User(user_name="00480",name=u"郄晓玉")
        log.debug(usr)
        self.session.add(usr)
        ps = Password(user=usr,algorithm=u'MD5',credential=u'1')
        self.session.add(ps)

        # 用户 ---  机构    关联
        brc = branch.filter(Branch.branch_code=="047325").first()
        usr_brc = UserBranch(user=usr,branch=brc)
        self.session.add(usr_brc)
        #usr_grp=UserGroup(user=usr,group=2)
        #usr_grp1=UserGroup(user=usr,group=17)
        #session.add(usr_grp,usr_grp1)
        self.session.commit()
    def init_teller_position(self):
        #岗位
        self.session.query(GroupMenu).delete()
        self.session.query(UserGroup).delete()
        self.session.query(Group).delete()

        excel = xlrd.open_workbook(environ['HOME'] + '/src/doc/岗位表.xls')
        sheet = excel.sheet_by_index(0)
        menus = self.session.query(Menu)
        nrows = sheet.nrows
        for r in range(1,nrows):
            g = sheet.cell(r,1).value
            grp = Group(group_name = g)
            self.session.add(grp)
            #
            for menu in menus:
                gm = GroupMenu(group_id = grp.id, menu_id = menu.id, from_date = datetime.datetime.today(), thru_date = None)
                self.session.add(gm)
        self.session.commit()

    def test_update_new_staff_data(self):
        staff_branch = xlrd.open_workbook(environ['HOME'] + '/src/doc/new_staff.xls')
        sheet = staff_branch.sheet_by_index(3)
        nrows = sheet.nrows
        #f = xlwt.Workbook()
        #sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)
        #row0 = [u'员工编号',u'员工姓名',u'身份证号',u'人员性质',u'部门',u'职务工种',u'客户经理类别',u'安全员标志',u'修改后安全标志',u'原安全标志',u'在职状态']
        #for i in range(0,len(row0)):
        #    sheet1.write(0,i,row0[i])
        #branch = self.session.query(Branch)
        #n = 1
        for r in range(2,nrows):
            v1=str(int(sheet.cell(r,1).value))  #员工编号
            v2=sheet.cell(r,2).value.strip()   #员工姓名
            v3=sheet.cell(r,3).value.strip()    #人员性质
            v4=sheet.cell(r,4).value.strip()    #身份证号码
            v5=sheet.cell(r,5).value.strip()    #机构
            v6=sheet.cell(r,6).value.strip()    #部门
            v7=sheet.cell(r,7).value.strip()    #职务工种
            v8=sheet.cell(r,8).value.strip()    #试聘标志
            v10=sheet.cell(r,10).value.strip()  #客户经理类别
            v11=sheet.cell(r,11).value.strip()  #安全标志
            v12=sheet.cell(r,12).value.strip()  #在职状态
            
            user_name = self.session.query(User).filter(User.name == v2).first()
            ryxz = self.session.query(Group).join(UserGroup,UserGroup.group_id == Group.id).join(User,User.role_id == UserGroup.user_id).filter(Group.group_name == v3).filter(User.name == v2).filter(Group.group_type_code == '4000').first()
            id_number = self.session.query(User).filter(User.id_number == v4).filter(User.name == v2).first()
            org_name = self.session.query(Branch).join(UserBranch,UserBranch.branch_id == Branch.role_id).join(User,User.role_id == UserBranch.user_id).filter(User.name == v2).filter(Branch.branch_name == v5).first()
            bm = self.session.query(Group).join(UserGroup,UserGroup.group_id == Group.id).join(User,User.role_id == UserGroup.user_id).filter(User.name == v2).filter(Group.group_name == v6).filter(Group.group_type_code == '3000').first()
            zwgz = self.session.query(Group).join(UserGroup,UserGroup.group_id == Group.id).join(User,User.role_id == UserGroup.user_id).filter(User.name == v2).filter(Group.group_name == v7).filter(Group.group_type_code == '1000').first()
            is_test = self.session.query(User).filter(User.name == v2).filter(User.is_test == v8).first()
            khjllb = self.session.query(Group).join(UserGroup,UserGroup.group_id == Group.id).join(User,User.role_id == UserGroup.user_id).filter(User.name == v2).filter(Group.group_name == v10).filter(Group.group_type_code == '2000').first()
            is_safe = self.session.query(User).filter(User.name == v2).filter(User.is_safe == v11).first()
            work_status = self.session.query(User).filter(User.name == v2).filter(User.work_status == v12).first()
            
            #将Excel表中内容更新到数据库
            if not user_name:
                continue
            if not bm:
                gid=self.session.query(UserGroup.id).join(User,User.role_id==UserGroup.user_id).join(Group,Group.id==UserGroup.group_id).filter(Group.group_type_code=='3000').filter(User.user_name==v1).first()
                group_id=self.session.query(UserGroup.group_id).join(User,User.role_id==UserGroup.user_id).join(Group,Group.id==UserGroup.group_id).filter(Group.group_name==v6).first()
                if group_id and gid:
                    gid=gid[0]
                    group_id=group_id[0]
                    self.session.query(UserGroup).filter(UserGroup.id==gid).update({UserGroup.group_id:group_id,UserGroup.startdate:'20161031'})
                    self.session.commit()
            if not ryxz:
                gid=self.session.query(UserGroup.id).join(User,User.role_id==UserGroup.user_id).join(Group,Group.id==UserGroup.group_id).filter(Group.group_type_code=='4000').filter(User.user_name==v1).first()
                group_id=self.session.query(UserGroup.group_id).join(User,User.role_id==UserGroup.user_id).join(Group,Group.id==UserGroup.group_id).filter(Group.group_name==v3).first()
                if group_id and gid:
                    gid=gid[0]
                    group_id=group_id[0]
                    self.session.query(UserGroup).filter(UserGroup.id==gid).update({UserGroup.group_id:group_id,UserGroup.startdate:'20161031'})
                    self.session.commit()
            if not id_number:
                self.session.query(User).filter(User.user_name==v1).update({User.id_number:v4})
                self.session.commit()
            if not org_name:
                branch_id=self.session.query(UserBranch.branch_id).join(User,User.role_id==UserBranch.user_id).join(Branch,Branch.role_id==UserBranch.branch_id).filter(Branch.branch_name==v5).first()
                bid=self.session.query(UserBranch.id).join(User,User.role_id==UserBranch.user_id).join(Branch,Branch.role_id==UserBranch.branch_id).filter(User.name==v2).first()
                if branch_id and bid:
                    bid=bid[0]
                    branch_id=branch_id[0]
                    self.session.query(UserBranch).filter(UserBranch.id==bid).update({UserBranch.branch_id:branch_id})
                    self.session.commit()
            if not bm:
                gid=self.session.query(UserGroup.id).join(User,User.role_id==UserGroup.user_id).join(Group,Group.id==UserGroup.group_id).filter(Group.group_type_code=='3000').filter(User.user_name == v1).first()
                group_id=self.session.query(UserGroup.group_id).join(User,User.role_id==UserGroup.user_id).join(Group,Group.id==UserGroup.group_id).filter(Group.group_name==v6).first()
                if group_id and gid:
                    gid=gid[0]
                    group_id=group_id[0]
                    self.session.query(UserGroup).filter(UserGroup.id==gid).update({UserGroup.group_id:group_id,UserGroup.startdate:'20161031'})
                    self.session.commit()
            if not zwgz:
                gid=self.session.query(UserGroup.id).join(User,User.role_id==UserGroup.user_id).join(Group,Group.id==UserGroup.group_id).filter(User.user_name == v1).filter(Group.group_type_code=='1000').first()
                group_id=self.session.query(UserGroup.group_id).join(User,User.role_id==UserGroup.user_id).join(Group,Group.id==UserGroup.group_id).filter(Group.group_name==v7).filter(Group.group_type_code=='1000').first()
                if group_id and gid:
                    gid=gid[0]
                    group_id=group_id[0]
                    self.session.query(UserGroup).filter(UserGroup.id==gid).update({UserGroup.group_id:group_id,UserGroup.startdate:'20161031'})
                    self.session.commit()
            if not is_test:
                self.session.query(User).filter(User.user_name==v1).update({User.is_test:v8})
                self.session.commit()
            if not khjllb:
                gid=self.session.query(UserGroup.id).join(User,User.role_id==UserGroup.user_id).join(Group,Group.id==UserGroup.group_id).filter(Group.group_name == v10).filter(User.user_name==v1).filter(Group.group_type_code=='2000').first()
                group_id=self.session.query(UserGroup.group_id).join(User,User.role_id==UserGroup.user_id).join(Group,Group.id==UserGroup.group_id).filter(Group.group_name==v10).filter(Group.group_type_code=='2000').first()
                if group_id and gid:
                    gid=gid[0]
                    group_id=group_id[0]
                    self.session.query(UserGroup).filter(UserGroup.id==gid).update({UserGroup.group_id:group_id,UserGroup.startdate:'20161031'})
                    self.session.commit()
            if not is_safe:
                self.session.query(User).filter(User.user_name==v1).update({User.is_safe:v11})
                self.session.commit()
            if not work_status:
                self.session.query(User).filter(User.user_name==v1).update({User.work_status:v12})
                self.session.commit()
            ''' 
            #Excel表中内容与数据库比对并展示到另一个Excel表中
            ryxz1 = self.session.query(Group.group_name).join(UserGroup,UserGroup.group_id == Group.id).join(User,User.role_id == UserGroup.user_id).filter(User.user_name == v1).filter(Group.group_type_code == '4000').first()
            org_name1 = self.session.query(Branch.branch_name).join(UserBranch,UserBranch.branch_id == Branch.role_id).join(User,User.role_id == UserBranch.user_id).filter(User.user_name == v1).first()
            bm1 = self.session.query(Group.group_name).join(UserGroup,UserGroup.group_id == Group.id).join(User,User.role_id == UserGroup.user_id).filter(User.user_name == v1).filter(Group.group_type_code == '3000').first()
            zwgz1 = self.session.query(Group.group_name).join(UserGroup,UserGroup.group_id == Group.id).join(User,User.role_id == UserGroup.user_id).filter(User.name == v2).filter(Group.group_type_code == '1000').first()
            is_test1 = self.session.query(User.is_test).filter(User.name==v2).first()
            khjllb1 = self.session.query(Group.group_name).join(UserGroup,UserGroup.group_id == Group.id).join(User,User.role_id == UserGroup.user_id).filter(User.name == v2).filter(Group.group_type_code == '2000').first()
            is_safe1 = self.session.query(User.is_safe).filter(User.name==v2).first()
            work_status1 = self.session.query(User.work_status).filter(User.user_name == v1).first()
            if 1: 
                sheet1.write(n,0,v1)
                sheet1.write(n,1,v2)
            if not ryxz:
                sheet1.write(n,3,v3)
                sheet1.write(n,4,ryxz1)
            if not id_number:
                sheet1.write(n,2,v4)
            if not org_name:
                sheet1.write(n,5,v5)
                sheet1.write(n,6,org_name1)
            if not bm:
                sheet1.write(n,7,v6)
                sheet1.write(n,8,bm1)
            if not zwgz:
                sheet1.write(n,9,v7)
                sheet1.write(n,10,zwgz1)
            if not is_test:
                sheet1.write(n,11,v8)
                sheet1.write(n,12,is_test1)
            if not khjllb:
                sheet1.write(n,13,v10)
                sheet1.write(n,14,khjllb1)
            if not is_safe:
                sheet1.write(n,15,v11)
                sheet1.write(n,16,is_safe1)
            if not work_status:
                sheet1.write(n,17,v12)
                sheet1.write(n,18,work_status1)
            n = n+1
        f.save(environ['HOME'] + '/src/doc/update.xls')    
        '''
    def add_teller_data(self):
        teller_branch = xlrd.open_workbook(environ['HOME'] + '/src/doc/虚拟员工表.xls')
        sheet = teller_branch.sheet_by_index(0)
        nrows = sheet.nrows

        branch = self.session.query(Branch)

        for r in range(1,nrows):
            v1=sheet.cell(r,1).value.strip()    #柜员名称
            v2=sheet.cell(r,2).value.strip()    #柜员号
            v3=sheet.cell(r,3).value.strip()    #人员性质 4000
            v4=sheet.cell(r,4).value.strip()    #身份证
            v5=sheet.cell(r,5).value.strip()    #所属机构
            v7=sheet.cell(r,7).value.strip()    #部门 3000
            v8=sheet.cell(r,8).value.strip()    #职务 1000
            v9=sheet.cell(r,9).value.strip()    #客户经理类型 2000
            v10=sheet.cell(r,10).value.strip()  #安全员标志
            v11=sheet.cell(r,11).value.strip()  #在职状态
            v12=sheet.cell(r,12).value.strip()  #是否虚拟柜员
            v13=sheet.cell(r,13).value.strip()  #用户权限组 5000

            if v1 in ['',None] or v5 in ['',None]:
                continue

            # 用户 添加 添加PAD电话号码
            user = self.session.query(User).filter(User.user_name == v2).first()
            if user:
                continue

            usr = User(user_name=v2, name=v1, work_status=v11, id_number=v4, is_safe=v10, is_virtual=v12)
            ps = Password(user=usr,algorithm=u'MD5',credential=to_md5('qwe123'))
            self.session.add(ps)
            self.session.flush()

            # 用户 ---  机构    关联
            print v2.strip(), v3, v5
            brc = branch.filter(Branch.branch_code==v5).first()
            usr_brc = UserBranch(user=usr,branch=brc)
            self.session.add(usr_brc)
            self.session.flush()

            #人员性质
            group3 = self.session.query(Group).filter(Group.group_name == v3).filter(Group.group_type_code == '4000').first()
            if group3:
                usr_grp=UserGroup(user=usr,group=group3,startdate='20160101')
                self.session.add(usr_grp)
                self.session.flush()

            group7 = self.session.query(Group).filter(Group.group_name == v7).filter(Group.group_type_code == '3000').first()
            if group7:
                usr_grp=UserGroup(user=usr,group=group7,startdate='20160101')
                self.session.add(usr_grp)
                self.session.flush()

            group8 = self.session.query(Group).filter(Group.group_name == v8).filter(Group.group_type_code == '1000').first()
            if group8:
                usr_grp=UserGroup(user=usr,group=group8,startdate='20160101')
                self.session.add(usr_grp)
                self.session.flush()

            group9 = self.session.query(Group).filter(Group.group_name == v9).filter(Group.group_type_code == '2000').first()
            if group9:
                usr_grp=UserGroup(user=usr,group=group9,startdate='20160101')
                self.session.add(usr_grp)
                self.session.flush()

            group13 = self.session.query(Group).filter(Group.group_name == v13).filter(Group.group_type_code == '5000').first()
            if group13:
                usr_grp=UserGroup(user=usr,group=group13,startdate='20160101')
                self.session.add(usr_grp)
                self.session.flush()

            self.session.commit()


    def init_teller_data(self):
        group_type_xls = xlrd.open_workbook(environ['HOME'] + '/src/doc/组分类表.xls')
        group_sheet = group_type_xls.sheet_by_index(0)
        group_nrows = group_sheet.nrows

        teller_branch = xlrd.open_workbook(environ['HOME'] + '/src/doc/员工表.xls')
        sheet = teller_branch.sheet_by_index(0)
        nrows = sheet.nrows

        self.session.query(Password).delete()
        self.session.query(Factor).delete()

        self.session.query(UserSession).delete()
        self.session.query(Authentication).delete()
        self.session.query(UserGroup).delete()
        self.session.query(UserBranch).delete()
        self.session.query(BranchGroup).delete()
        self.session.query(GroupMenu).delete()
        self.session.query(MboxRecord).delete()
        self.session.query(Group).delete()
        self.session.query(GroupType).delete()
        self.session.query(GroupHis).delete()

        self.session.query(User).delete()

        branch = self.session.query(Branch)

        for r in range(1,group_nrows):  #用户组分类
            v0=group_sheet.cell(r,0).value.strip()    #code
            v1=group_sheet.cell(r,1).value.strip()    #name
            group_type = GroupType(type_code=v0, type_name=v1)
            self.session.add(group_type)
            self.session.flush()

        count = 0
        for r in range(1,nrows):        #用户组处理
            count = count + 1
            v3=sheet.cell(r,3).value.strip()    #人员性质 4000
            v5=sheet.cell(r,5).value.strip()    #所属机构
            v7=sheet.cell(r,7).value.strip()    #部门 3000
            v8=sheet.cell(r,8).value.strip()    #职务 1000
            v9=sheet.cell(r,9).value.strip()    #客户经理类型 2000
            v13=sheet.cell(r,13).value.strip()  #用户权限组 5000

            group33 = self.session.query(Group).filter(Group.group_name == v3).filter(Group.group_type_code == '4000').first()
            if not group33:
                group3 = Group(group_name = v3, group_type_code = '4000')
                self.session.add(group3)
                self.session.flush()

            group77 = self.session.query(Group).filter(Group.group_name == v7).filter(Group.group_type_code == '3000').first()
            if not group77:
                group7 = Group(group_name = v7, group_type_code = '3000')
                self.session.add(group7)
                self.session.flush()
                brc = branch.filter(Branch.branch_code==v5).first()
                branch_group = self.session.query(BranchGroup).filter(BranchGroup.branch_id == brc.role_id).filter(BranchGroup.group_id == group7.id ).first()
                if not branch_group:
                    branch_group_add = BranchGroup(branch_id = brc.role_id, group_id = group7.id)
                    self.session.add(branch_group_add)
                    self.session.flush()

            group88 = self.session.query(Group).filter(Group.group_name == v8).filter(Group.group_type_code == '1000').first()
            if not group88:
                group8 = Group(group_name = v8, group_type_code = '1000')
                self.session.add(group8)
                self.session.flush()

            group99 = self.session.query(Group).filter(Group.group_name == v9).filter(Group.group_type_code == '2000').first()
            if not group99:
                group9 = Group(group_name = v9, group_type_code = '2000')
                self.session.add(group9)
                self.session.flush()

            group1313 = self.session.query(Group).filter(Group.group_name == v13).filter(Group.group_type_code == '5000').first()
            if not group1313:
                group13 = Group(group_name = v13, group_type_code = '5000')
                self.session.add(group13)
                self.session.flush()



        #用户权限组菜单设置
        group_ms = self.session.query(Group).filter(Group.group_type_code == '5000').all()
        menus = self.session.query(Menu)
        for group_m in group_ms:
            for menu in menus:
                gm = GroupMenu(group_id = group_m.id, menu_id = menu.id, from_date = datetime.datetime.today(), thru_date = None)
                self.session.add(gm)
                self.session.flush()


        for r in range(1,nrows):
            v1=sheet.cell(r,1).value.strip()    #柜员名称
            v2=str(int(sheet.cell(r,2).value))    #柜员号
            v3=sheet.cell(r,3).value.strip()    #人员性质 4000
            v4=sheet.cell(r,4).value.strip()    #身份证
            v5=sheet.cell(r,5).value.strip()    #所属机构
            v7=sheet.cell(r,7).value.strip()    #部门 3000
            v8=sheet.cell(r,8).value.strip()    #职务 1000
            v9=sheet.cell(r,9).value.strip()    #客户经理类型 2000
            v10=sheet.cell(r,10).value.strip()  #安全员标志
            v11=sheet.cell(r,11).value.strip()  #在职状态
            v12=sheet.cell(r,12).value.strip()  #是否虚拟柜员
            v13=sheet.cell(r,13).value.strip()  #用户权限组 5000

            if v1 in ['',None] or v5 in ['',None]:
                continue
            # 用户 添加 添加PAD电话号码
            usr = User(user_name=v2, name=v1, work_status=v11, id_number=v4, is_safe=v10, is_virtual=v12)
            ps = Password(user=usr,algorithm=u'MD5',credential=to_md5('qwe123'))
            self.session.add(ps)
            self.session.flush()

            # 用户 ---  机构    关联
            print v1.strip()
            brc = branch.filter(Branch.branch_code==v5).first()
            usr_brc = UserBranch(user=usr,branch=brc)
            self.session.add(usr_brc)
            self.session.flush()

            #人员性质
            group3 = self.session.query(Group).filter(Group.group_name == v3).filter(Group.group_type_code == '4000').first()
            if group3:
                usr_grp=UserGroup(user=usr,group=group3,startdate='20160101')
                self.session.add(usr_grp)
                self.session.flush()

            group7 = self.session.query(Group).filter(Group.group_name == v7).filter(Group.group_type_code == '3000').first()
            if group7:
                usr_grp=UserGroup(user=usr,group=group7,startdate='20160101')
                self.session.add(usr_grp)
                self.session.flush()

            group8 = self.session.query(Group).filter(Group.group_name == v8).filter(Group.group_type_code == '1000').first()
            if group8:
                usr_grp=UserGroup(user=usr,group=group8,startdate='20160101')
                self.session.add(usr_grp)
                self.session.flush()

            group9 = self.session.query(Group).filter(Group.group_name == v9).filter(Group.group_type_code == '2000').first()
            if group9:
                usr_grp=UserGroup(user=usr,group=group9,startdate='20160101')
                self.session.add(usr_grp)
                self.session.flush()

            group13 = self.session.query(Group).filter(Group.group_name == v13).filter(Group.group_type_code == '5000').first()
            if group13:
                usr_grp=UserGroup(user=usr,group=group13,startdate='20160101')
                self.session.add(usr_grp)
                self.session.flush()

            self.session.commit()

        role_id=role_id[0]
