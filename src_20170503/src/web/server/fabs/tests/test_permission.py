# -*- coding:utf-8 -*-

import unittest
from sqlalchemy.orm import joinedload_all
from ..model.permission import *
from ..model.user import *
from ..base import utils
import datetime

import logging

log = logging.getLogger()

class TestPermission(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()

    def c_test_sql_flush(self):
        user = User(user_name='99999', name='99999')
        self.session.add(user)
        self.session.flush()

        log.debug(user.role_id)
        log.debug(user.__dict__)

    def test_menu_append(self):
        credit_back_append_menu(self.session)

    def btest_menu_group_save(self):
        now = datetime.datetime.now()

        kwargs = {u'menus': [u'1', u'12', u'13', u'18', u'19', u'20', u'21'], u'group_id': 1}

        group_id = kwargs.get('group_id')
        menus = kwargs.get('menus')

        group_menus = self.session.query(GroupMenu).filter(GroupMenu.group_id==group_id).all()

        for item in group_menus:
            item.menu.thru_date = now

        for menu_id in menus:
            gm = GroupMenu(from_date=now)
            gm.group_id = group_id
            gm.menu_id = menu_id
            self.session.add(gm)


    def atest_user_query(self):
        '''
            left join user_branch ub on ub.user_id = us.role_id
            left join branch bc on bc.role_id = ub.branch_id
        '''
        user_group = self.session.query(User.role_id, User.user_name, User.name, Branch.branch_code, Branch.branch_name,  Group.group_name) \
            .outerjoin(UserGroup,UserGroup.user_id==User.role_id) \
            .outerjoin(Group,Group.id==UserGroup.group_id) \
            .outerjoin(UserBranch,UserBranch.user_id==User.role_id) \
            .outerjoin(Branch,Branch.role_id==UserBranch.branch_id) \
            .all()
        user_dict = {}
        for user in user_group:
            per_user = user_dict.get(user[0])
            if per_user:
                per_user['group_name'] = per_user.get('group_name') + ',%s' % user[5]
            else:
                user_dict[user[0]]= {'role_id':user[0], 'user_name':user[1], 'name':user[2], 'branch_code':user[3], 'branch_name':user[4], 'group_name':user[5]}
        log.debug(user_dict)



    def atest_data_init(self):
        """
            select * from f_user us
            left join user_group usg on usg.user_id=us.role_id
            left join "group" gp on gp."id"=usg.group_id
            left join group_menu gpm on gpm.group_id=gp.id
            left join menu me on me.id=gpm.menu_id
            -- where user_name = '00510'
        """
        menus = self.session.query(User,Menu) \
            .outerjoin(UserGroup,UserGroup.user_id==User.role_id) \
            .outerjoin(Group,Group.id==UserGroup.group_id) \
            .outerjoin(GroupMenu,GroupMenu.group_id==Group.id) \
            .outerjoin(Menu,Menu.id==GroupMenu.menu_id) \
            .filter(Menu.parent_id==None) \
            .filter(User.user_name=='8888') \
            .order_by(Menu.id).all()
        log.debug(menus)

        #menus = self.session.query(Menu)\
        #    .options(joinedload_all("children", "children", "children")) \
        #    .filter(Menu.parent_id==None).order_by(Menu.id).all()

        tree = [utils.tree_dump(menu[1]) if menu[1] else [] for menu in menus]
        for re in tree:
            #log.debug(tree)
            log.debug(re)


    def tearDown(self):
        #Base.metadata.drop_all(self.session.bind)
        #Base.metadata.drop_all(self.session.bind)
        logging.debug("finish!!!")

def add_group_menu_rel(session, groups, m1_1):
    now = datetime.datetime.now()
    for g in groups:
        gm1_1 = GroupMenu(from_date=now)
        gm1_1.group = g
        m1_1.groups.append(gm1_1)
        session.add(m1_1)

def credit_back_append_menu(session):
    groups = session.query(Group).all()
    m8_4 = Menu(**{'name':u'展期', 'location':'views/credit/Extension/index.html'})
    m8_5 = Menu(**{'name':u'授信金额调整', 'location':'views/credit/Adjustment/index.html'})
    m8_6 = Menu(**{'name':u'贷款核销', 'location':'views/credit/Auditsale/index.html'})
    m8 = session.query(Menu).filter(Menu.name=='贷后管理').first()
    m8.children.append(m8_4)
    m8.children.append(m8_5)
    m8.children.append(m8_6)
    add_group_menu_rel(session, groups, m8_4)
    add_group_menu_rel(session, groups, m8_5)
    add_group_menu_rel(session, groups, m8_6)
    session.commit()

def init_permission_data(session):
    logging.debug("init permission data !")

    groups = session.query(Group).all()

    m1_1 = Menu(**{'name':u'个人信息管理', 'location':'views/customer/person/personManage.html'})
    m1_2 = Menu(**{'name':u'对公信息管理', 'location':'views/customer/company/companyManage.html'})
    m1 = Menu(**{'name':u'客户信息管理', 'location':u'', 'children':[m1_1,m1_2]})
    add_group_menu_rel(session, groups, m1_1)
    add_group_menu_rel(session, groups, m1_2)
    add_group_menu_rel(session, groups, m1)

    m2_1 = Menu(**{'name':u'个人业务申请', 'location':'views/credit/personCredit/index.html'})
    m2_2_1 = Menu(**{'name':u'贷款业务申请', 'location':'views/credit/companyCredit/index.html'})
    m2_2_2 = Menu(**{'name':u'承兑汇票贴现', 'location':'views/credit/discount/index.html'})
    m2_2_3 = Menu(**{'name':u'承兑汇票签发', 'location':'views/credit/acceptanceBill/accBillManager.html'})
    m2_2 = Menu(**{'name':u'对公业务申请', 'location':'', 'children':[m2_2_1, m2_2_2, m2_2_3]})
    m2_3 = Menu(**{'name':u'同业业务', 'location':'views/credit/sameBusiness/index.html'})
    m2_4 = Menu(**{'name':u'投资业务', 'location':'views/credit/invest/index.html'})
    m2 = Menu(**{'name':u'业务申请', 'location':u'', 'children':[m2_1,m2_2,m2_3,m2_4]})
    add_group_menu_rel(session, groups, m2_1)
    add_group_menu_rel(session, groups, m2_2_1)
    add_group_menu_rel(session, groups, m2_2_2)
    add_group_menu_rel(session, groups, m2_2_3)
    add_group_menu_rel(session, groups, m2_2)
    add_group_menu_rel(session, groups, m2_3)
    add_group_menu_rel(session, groups, m2_4)
    add_group_menu_rel(session, groups, m2)

    m3_1 = Menu(**{'name':u'已审议通过的贷款', 'location':'views/credit/CreditManage/checkCredit.html'})
    m3 = Menu(**{'name':u'审查审批', 'location':u'', 'children':[m3_1]})
    add_group_menu_rel(session, groups, m3)
    add_group_menu_rel(session, groups, m3_1)

    m4 = Menu(**{'name':u'授信额度管理', 'location':u'views/credit/creditInfomation.html'})
    add_group_menu_rel(session, groups, m4)

    m5_1 = Menu(**{'name':u'合同登记', 'location':'views/credit/contractRegistration.html'})
    # m5_2 = Menu(**{'name':u'放款申请', 'location':'views/loan/loanApplication.html'})
    m5 = Menu(**{'name':u'签约支付', 'location':u'', 'children':[m5_1]})
    add_group_menu_rel(session, groups, m5_1)
    # add_group_menu_rel(session, groups, m5_2)
    add_group_menu_rel(session, groups, m5)

    m6_1 = Menu(**{'name':u'担保合同管理', 'location':'views/credit/CreditContract/index.html'})
    m6_2 = Menu(**{'name':u'抵质押物管理', 'location':'views/credit/GuaranteeInformation/guaranty/limitsManager.html'})
    m6 = Menu(**{'name':u'担保管理', 'location':u'', 'children':[m6_1, m6_2]})
    add_group_menu_rel(session, groups, m6_1)
    add_group_menu_rel(session, groups, m6_2)
    add_group_menu_rel(session, groups, m6)

    m8_1_1 = Menu(**{'name':u'诉讼台账', 'location':'views/credit/StandingBook/index.html'})
    m8_1_2 = Menu(**{'name':u'以物抵债台账', 'location':'views/credit/discount/index.html'})
    m8_1_3 = Menu(**{'name':u'逾期贷款台账', 'location':'views/credit/StandingBook/OverdueLoans.html'})
    m8_1_4 = Menu(**{'name':u'欠息贷款台账', 'location':'views/credit/StandingBook/InterestLoans.html'})
    m8_1_5 = Menu(**{'name':u'停息贷款台账', 'location':'views/credit/StandingBook/CeaseInterest.html'})
    m8_1_6 = Menu(**{'name':u'逾期六个月（含）', 'location':'views/credit/StandingBook/Overdue.html'})
    add_group_menu_rel(session, groups, m8_1_1)
    add_group_menu_rel(session, groups, m8_1_2)
    add_group_menu_rel(session, groups, m8_1_3)
    add_group_menu_rel(session, groups, m8_1_4)
    add_group_menu_rel(session, groups, m8_1_5)
    add_group_menu_rel(session, groups, m8_1_6)
    m8_1 = Menu(**{'name':u'台账', 'location':'', 'children':[m8_1_1,m8_1_2,m8_1_3,m8_1_4,m8_1_5,m8_1_6]})
    m8_2 = Menu(**{'name':u'五级分类业务', 'location':'views/credit/FiveLevel/index.html'})
    m8_3_1 = Menu(**{'name':u'以物抵债', 'location':'views/credit/Repossession/index.html'})
    m8_3_2 = Menu(**{'name':u'抵贷资产出租出售', 'location':'views/credit/Repossession/index_rental.html'})
    m8_3 = Menu(**{'name':u'以物抵债', 'location':'', 'children':[m8_3_1,m8_3_2]})
    m8_4 = Menu(**{'name':u'展期', 'location':'views/credit/Extension/index.html'})
    m8_5 = Menu(**{'name':u'授信金额调整', 'location':'views/credit/Adjustment/index.html'})
    m8_6 = Menu(**{'name':u'贷款核销', 'location':'views/credit/Auditsale/index.html'})
    m8_7 = Menu(**{'name':u'借款合同管理', 'location':'views/credit/CreditContract/lend_index.html'})
    m8 = Menu(**{'name':u'贷后管理', 'location':u'', 'children':[m8_1, m8_2, m8_3, m8_4, m8_5,m8_6,m8_7]})
    add_group_menu_rel(session, groups, m8_1)
    add_group_menu_rel(session, groups, m8_2)
    add_group_menu_rel(session, groups, m8_3)
    add_group_menu_rel(session, groups, m8_3_1)
    add_group_menu_rel(session, groups, m8_3_2)
    add_group_menu_rel(session, groups, m8_4)
    add_group_menu_rel(session, groups, m8_5)
    add_group_menu_rel(session, groups, m8_6)
    add_group_menu_rel(session, groups, m8_7)
    add_group_menu_rel(session, groups, m8)

    m9_1 = Menu(**{'name':u'个人客户', 'location':'views/credit/creditLevel/index.html'})
    m9_2 = Menu(**{'name':u'个体经营户', 'location':''})
    m9_3 = Menu(**{'name':u'企业用户', 'location':'views/credit/creditLevel/enterPrise.html'})
    m9 = Menu(**{'name':u'客户信用等级评估', 'location':u'', 'children':[m9_1, m9_2, m9_3 ]})
    add_group_menu_rel(session, groups, m9_1)
    add_group_menu_rel(session, groups, m9_2)
    add_group_menu_rel(session, groups, m9_3)
    add_group_menu_rel(session, groups, m9)

    m10 = Menu(**{'name':u'统一授信', 'location':u'views/uniteCredit/index.html'})
    add_group_menu_rel(session, groups, m10)

    m11_1 = Menu(**{'name':u'跑批', 'location':'views/systemMange/batch.html'})
    m11_2 = Menu(**{'name':u'权限管理', 'location':'views/system_manager/permission/index.html'})
    m11_3 = Menu(**{'name':u'用户管理', 'location':'views/system_manager/users/index.html'})
    # m11_3 = Menu(**{'name':u'参数配置', 'location':'views/system_manager/parameter/index.html'})
    m11 = Menu(**{'name':u'系统管理', 'location':u'', 'children':[ m11_1, m11_2, m11_3]})
    # add_group_menu_rel(session, groups, m11_1)
    add_group_menu_rel(session, groups, m11_1)
    add_group_menu_rel(session, groups, m11_2)
    add_group_menu_rel(session, groups, m11_3)
    add_group_menu_rel(session, groups, m11)


    m12_1 = Menu(**{'name':u'贴现查询', 'location':'views/mainSearch/discountSearch.html'})
    m12 = Menu(**{'name':u'统一查询', 'location':u'', 'children':[m12_1]})
    add_group_menu_rel(session, groups, m12_1)
    add_group_menu_rel(session, groups, m12)



    #session.add_all([m1, m2, m3, m4, m5, m6, m8, m9, m10, m11])
    session.commit()



