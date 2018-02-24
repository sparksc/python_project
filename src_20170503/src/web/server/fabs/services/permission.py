# -*- coding: utf-8 -*-
"""
    yinsho.services.PermissionService
    #####################

    yinsho UsersService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all
from sqlalchemy.orm import load_only
from sqlalchemy.orm import subqueryload,Load

from ..base import utils
# from ..model import Permission, Menu, User, UserGroup, Group, GroupMenu, Branch, UserBranch
from ..model import Menu, User, UserGroup, Group, GroupMenu, Branch, UserBranch, Password,Factor,GroupType,GroupData

from ..base.utils import to_md5

class PermissionService():
    """ Permission Service  """

    # TODO: Move to the user db_session object
    def menu_dump(self):
        #menus = g.db_session.query(Menu).\
        #    options(joinedload_all("children", "children", "children")).\
        #    filter(Menu.parent_id==None).order_by(Menu.id).all()
        #return [utils.tree_dump(menu) for menu in menus]
        menus = g.db_session.query(Menu).\
            options(joinedload_all("children", "children", "children")).\
            filter(Menu.parent_id!=None).order_by(Menu.id).all()
        return [utils.row_dict(menu) for menu in menus]

    def group_menu_select(self, **kwargs):
        menus = g.db_session.query(Menu.id, Menu.name, Group.id, Group.group_name) \
            .outerjoin(GroupMenu, and_(GroupMenu.menu_id==Menu.id, GroupMenu.group_id==kwargs.get('group_id'))) \
            .outerjoin(Group, (GroupMenu.group_id==Group.id)) \
            .order_by(Menu.id).all()
        menu_select = []
        for menu in menus:
            menu_select.append({'menu_id':menu[0], 'menu_name':menu[1], 'group_id':menu[2], 'group_name':menu[3]})
        return menu_select

    def group_menus_save(self, **kwargs):
        group_id = kwargs.get('group_id')
        menus = kwargs.get('menus')

        now = datetime.datetime.now()

        g.db_session.query(GroupMenu).filter(GroupMenu.group_id == group_id).delete()

        for menu_id in menus:
            gm = GroupMenu(from_date=now)
            gm.group_id = group_id
            gm.menu_id = menu_id
            g.db_session.add(gm)

        g.db_session.commit()

        return u"保存成功"

    def user_permission_group_select(self,**kwargs):
        q = g.db_session.query(Group.id,Group.group_name,UserGroup.id) \
            .join(GroupType,and_(GroupType.type_code==Group.group_type_code,GroupType.type_name=='用户权限组')) \
            .outerjoin(UserGroup,and_(UserGroup.group_id==Group.id,UserGroup.user_id==kwargs.get('user_id'))) \
            .order_by(Group.id).all()

        permission_group_select = []
        for grp in q:
            permission_group_select.append({'group_id':grp[0], 'group_name':grp[1],'usergroup_id':grp[2]})
        return permission_group_select    
 
    def user_permission_group_save(self,**kwargs):
        user_id = kwargs.get('user_id')
        groups = kwargs.get('groups')
        old_groups=kwargs.get('old_groups')

        now = datetime.datetime.now().strftime('%Y%m%d')

        #print groups
        g.db_session.query(UserGroup).filter(UserGroup.user_id == user_id).filter(UserGroup.group_id.in_(old_groups)).delete(synchronize_session=False)

        for group_id in groups:
            gm = UserGroup(startdate=now)
            gm.group_id = group_id
            gm.user_id = user_id
            g.db_session.add(gm)

        g.db_session.commit()

        return u"保存成功"

    def user_menu_dump(self,user_name):
        q = g.db_session.query(User,Menu) \
            .outerjoin(UserGroup,UserGroup.user_id==User.role_id) \
            .outerjoin(Group,Group.id==UserGroup.group_id) \
            .outerjoin(GroupMenu,GroupMenu.group_id==Group.id) \
            .outerjoin(Menu,Menu.id==GroupMenu.menu_id) \
            .filter(Menu.parent_id==None) \
            .filter(User.user_name==user_name) \
            .order_by(Menu.id)
        menus = q.all()
        return [utils.tree_dump(menu[1]) if menu[1] else [] for menu in menus]

    def user_permission_menu_dump(self,user_name):
        q = g.db_session.query(User,Menu,Group) \
            .outerjoin(UserGroup,UserGroup.user_id==User.role_id) \
            .outerjoin(Group,Group.id==UserGroup.group_id) \
            .outerjoin(GroupMenu,GroupMenu.group_id==Group.id) \
            .outerjoin(Menu,Menu.id==GroupMenu.menu_id) \
            .filter(Menu.parent_id==None) \
            .filter(User.user_name==user_name) \
            .order_by(Menu.id)
        menus = q.options(Load(Menu).subqueryload('children')).all()
        
        merge_menus = []
        seen = []
        group_ids = []
        #print "----------------------XXXXXXXXXXXXXXXXXXXXXXXXX--",menus[0]
        for qo in menus:
            menu = qo[1]
            if menu is None:continue
            #print "----------------------XXXXXXXXXXXXXXXXXXXXXXXXX--",qo[1],qo[2]
            group_id = qo[2].id
            if group_id not in group_ids: 
                group_ids.append(group_id)
            if menu.id in seen:
                continue
            merge_menus.append(menu)
            seen.append(menu.id)
        group_menus = self.group_menus_ids(group_ids)
        print "group_menus",group_menus.extend([m.id for m in merge_menus])
        merge_menus = self.merge_menus(merge_menus,group_menus)
        return merge_menus

    def group_menus_ids(self,group_ids):
        q = g.db_session.query(GroupMenu).filter(GroupMenu.group_id.in_(group_ids)).options(load_only("menu_id"))
        group_menus = q.all()
        return [gm.menu_id for gm in group_menus]

    def merge_menus(self,menus,g_menus):
        #递归查找
        rt = []
        for  m in menus: 
            if m.id not in g_menus:
                continue
            m_dict = self.row2dict(m)
            childs = self.merge_menus(m.children,g_menus)
            if childs:
                m_dict["children"] =  childs
            rt.append(m_dict)
        return rt
        #imenus = []
        #for m in menus:
        #    m_dict = self.row2dict(m)
        #    m_dict["children"] = [self.row2dict(c) for c in m.children if c.id in g_menus]
        #    imenus.append(m_dict)
        #return imenus

    def row2dict(self,row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = getattr(row, column.name)
        return d

    def users(self, **kwargs):
        user_group = g.db_session.query(User.role_id, User.user_name, User.name \
                , Branch.branch_code, Branch.branch_name,  Group.group_name) \
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
        return user_dict
	    
    def user_groups(self, user_id):
        print "ug"
        print self.user_branches(user_id)
        user_group_result = g.db_session.query(Group,UserGroup.group_id).outerjoin(UserGroup, and_(UserGroup.group_id==Group.id, UserGroup.user_id==user_id)).all()
        user_group = []
        for group,group_id in user_group_result:
            user_group.append({'group_id':group.id, 'group_name':group.group_name, 'user_group_id':group_id})
        return user_group

    def user_groups_save(self, **kwargs):
        user_id = kwargs.get('user_id')
        group_ids = kwargs.get('group_ids')
        g.db_session.query(UserGroup).filter(UserGroup.user_id==user_id).delete()
        for group_id in group_ids:
            g.db_session.add(UserGroup(user_id=user_id,group_id=group_id))
        return u"保存成功"

    def groups_permission(self,**kwargs):
        import time
        search_name=kwargs.get('group_name')
        print (search_name,"111111111111111111111111111111111111111111111111111111111111111111111111")
        branches = None
        if search_name:
            branches = g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name=='用户权限组',Group.group_name.like('%'+search_name+'%')).all()
        else:
            branches = g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name=='用户权限组').order_by(Group.id).all()
        return [{"id":b.id,"group_name":b.group_name} for b in branches]
        #return branches

    def groups(self,**kwargs):
        import time
        search_name=kwargs.get('group_name')
        branches = None
        if search_name:
            branches = g.db_session.query(Group).filter(Group.group_name.like('%'+search_name+'%')).all()
        else:
            branches = g.db_session.query(Group).order_by(Group.id).all()
        return [{"id":b.id,"group_name":b.group_name} for b in branches]
        
    def user_branches(self,user_id):
        user_branches = g.db_session.query(Branch).join(UserBranch,UserBranch.branch_id==Branch.role_id) \
        .filter(UserBranch.user_id==user_id).all()
        return [utils.tree_dump(branch) for branch in user_branches]

    def para_menu_save(self,**kwargs):
        menudata= kwargs.get('menudata')
        parent_menu_name = menudata.get('parent_menu') 
        parent_menu = g.db_session.query(Menu).filter(Menu.name==parent_menu_name).all()
        data = {}
        data['location'] = menudata.get('url')
        data['name'] = menudata.get('name')
        if len(parent_menu)>0:
            data['parent_id'] = parent_menu[0].id
            menus = g.db_session.query(Menu).filter(Menu.name==data['name']).all()
            if len(menus):
                return u"已加入菜单，不可重复插入，请检查"
            else:
                g.db_session.add(Menu(**data))
        else:
            menu = [Menu(**data)]
            parent = Menu(name=parent_menu_name,location=u'')
            g.db_session.add(menu[0])
            g.db_session.flush()
            g.db_session.add(parent)
            #data['parent_id'] = parent.id
        return u"添加成功，请配置访问权限"
    def menu_update(self,**kwargs):
        menudata= kwargs.get('newdata')
        self.qfield = ['id','name','location','parent_id']                 
        data = {}
        tid = menudata.get('id')
        data[self.qfield[1]]=menudata.get('pagename')
        data[self.qfield[2]]=menudata.get('url')
        data[self.qfield[3]]=menudata.get('parentid')
        g.db_session.query(Menu).filter(Menu.id==tid).update(data)
        return u"修改成功"
    def menu_save(self,**kwargs):
        g.db_session.add(Menu(**kwargs))
        return u"添加成功"
    def user_update(self,**kwargs):
        userdata=kwargs.get('newdata')
        g.db_session.query(User).filter(User.role_id==userdata.get('uid')).update({'user_name':userdata.get('staff_no'),'name':userdata.get('staff_name')})
        g.db_session.query(UserBranch).filter(UserBranch.user_id==userdata.get('uid')).update({'branch_id':userdata.get('oid')})
        g.db_session.query(Password).filter(Password.factor_id==userdata.get('fid')).update({'credential':userdata.get('password')})
        return u"修改成功"
    def init_user_pwd(self,**kwargs):
        userdata=kwargs.get('newdata')
        staff_no= userdata.get('staff_no')
        user = g.db_session.query(User).filter(User.user_name == staff_no).first()
        factor = g.db_session.query(Factor).filter(Factor.user_id == user.role_id).first()
        print staff_no
        passwd_sql = g.db_session.query(Password).filter(Password.factor_id == factor.factor_id).update({'credential':to_md5("qwe123")})
        return u"重置密码成功"
    def user_save(self,**kwargs):
        userdata=kwargs.get('newdata')
        print userdata,'-----------------'
        
        nuser = User()
        nuser.user_name=userdata.get('staff_no')
        nuser.name=userdata.get('staff_name')
        g.db_session.add(nuser)
        g.db_session.flush()
        nrid=nuser.role_id
        print nuser.role_id,'+++'
         
        nuserbranch = UserBranch()
        nuserbranch.user_id=nrid
        nuserbranch.branch_id=userdata.get('oid')
        g.db_session.add(nuserbranch)
        g.db_session.flush()
       
        npassword = Password()
        npassword.algorithm='MD5'
        npassword.credential=userdata.get('password')
        g.db_session.add(npassword)
        g.db_session.flush()
        nfid=npassword.factor_id
        g.db_session.query(Factor).filter(Factor.factor_id==nfid).update({'user_id':nrid})
         
        return u"添加成功"

    def save_permission_list(self,**kwargs):
        gid = kwargs.get('group_id')
        allg = kwargs.get('all')
        addg = kwargs.get('add')
        delg = kwargs.get('del')
        print gid, allg, addg, delg
        now = datetime.datetime.now()

        g.db_session.query(GroupMenu).filter(GroupMenu.group_id == gid).delete()

        for menu_id in allg:
            gm = GroupMenu(from_date=now)
            gm.group_id = gid
            gm.menu_id = menu_id
            g.db_session.add(gm)

        g.db_session.commit()
        return "保存成功"

    def get_permission_list(self,**kwargs):
        menus = g.db_session.query(Menu.id, Menu.name, Menu.parent_id, GroupMenu.group_id) \
            .outerjoin(GroupMenu, and_(GroupMenu.menu_id==Menu.id)) \
            .order_by(Menu.id).all()

        return self.make_menu_tree(menus, kwargs.get('group_id'))

    def init_menu_true(self, menus):
        nodes = {}
        node_list = []
        node_tlst = []
        node_push = []
        for menu in menus:
            n_id = menu[0]
            p_id = menu[2]
            g_id = int(menu[3]) if menu[3] else -1
            if not nodes.has_key(n_id):
                nodes[n_id] = {'node_code': menu[0], 'node_name': menu[1], 'parent_code': menu[2], 'node_group': [], 'childs': []}
            nodes[n_id]['node_group'].append(g_id)
            if n_id not in node_push:
                node_tlst.append(nodes[n_id])
                node_push.append(n_id)
        for node in node_tlst:
            p_id = node['parent_code']
            if nodes.has_key(p_id):
                nodes[p_id]['childs'].append(node)
            else:
                node_list.append(node)
        return (node_list)

    def check_node(self, nodes, group_id):
        for node in nodes:
            if len(node['childs']) > 0:
                self.check_node(node['childs'], group_id)
            else:
                node['checked'] = True if group_id in node['node_group'] else False

    def make_menu_tree(self, menus, group_id):
        node_list = self.init_menu_true(menus)
        self.check_node(node_list, group_id)
        return node_list

    def groupdata_save(self,**kwargs):
        newdata =  kwargs.get('add_date')
        gd = g.db_session.query(GroupData).filter(and_(GroupData.group_id==newdata['group_id'],GroupData.data_type==newdata['data_type'])).first()
        if gd:
            return u"已存在该岗位在该模块的权限"
        g.db_session.add(GroupData(**newdata))
        return u'添加成功'

    def groupdata_edit(self,**kwargs):
        newdata =  kwargs.get('up_date')
        #gd = g.db_session.query(GroupData).filter(and_(GroupData.group_id==newdata['group_id'],GroupData.data_type==newdata['data_type'])).first()
        #if gd:
            #return u"已存在该岗位在该模块的权限"
        g.db_session.query(GroupData).filter(GroupData.id==newdata['id']).update(newdata)
        return u'编辑成功'

    def groupdata_delete(self,**kwargs):
        id = kwargs.get('id')
        g.db_session.query(GroupData).filter(GroupData.id==id).delete()
        return u'删除成功'
