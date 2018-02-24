# -*- coding: utf-8 -*-
"""
    yinsho.services.UserRelationService
    #####################

    yinsho UserRelationService module
"""
import datetime
from flask import json, g,current_app
from sqlalchemy import and_, func,text
from sqlalchemy.orm import joinedload_all,joinedload

from ..base import utils
from ..model import Role,UserRelation,User,UserGroup,GroupType,Branch,Group,UserBranch,GroupHis,Password,Factor,Authentication,UserSession,AccountHook,CustHook,D_DATE
  
from ..base.utils import to_md5

class UserRelationService():
    """ UserRelationService """
    def update(self,**kwargs):
        #self.ckyy = ['user_code','user_sop_code','user_cms_code','is_khjl','is_zhgy','is_kjzg','is_zhhz','is_xdkj','is_flczr','user_name','xl','zc','rhnx','gznx','gwxs','gwzj','card_type','card_num'] 
        
        self.ckyy = ['staff_sop_code','staff_cms_code','is_khjl','is_zhgy','is_kjzg','is_zhhz']
        newdata =  kwargs.get('newdata')
        tid = newdata[8]
        data ={}
        for i in range(6):
            if newdata[i+2] == u'是':
                newdata[i+2] = 1
            if newdata[i+2] == u'否':
                newdata[i+2] = 0
            if newdata[i+2] is not None: 
                data[self.ckyy[i]]=newdata[i+2]
#        for k,v in newdata.items():
#            if k in self.ckyy : data[k] = v
#        g.db_session.add(UserRelation(**data))
        g.db_session.query(UserRelation).filter(UserRelation.id==tid).update(data)
        return u"修改成功"    
    def newupdate(self,**kwargs):
        newdata = kwargs.get('newdata')
        if(newdata[5] is None):
            return u'部门信息请填写完整'
        if(newdata[7] is None):
            return u'工种信息请填写完整'
         
        if(newdata[3] is None):
            if(newdata[14] is not None):
                g.db_session.query(UserGroup).filter(UserGroup.id==newdata[14]).delete()
        if(newdata[6] is None):
            if(newdata[15] is not None):
                g.db_session.query(UserGroup).filter(UserGroup.id==newdata[15]).delete()
        if(newdata[8] is None):
            if(newdata[17] is not None):
                g.db_session.query(UserGroup).filter(UserGroup.id==newdata[17]).delete()
        if(newdata[9] is None):
            if(newdata[18] is not None):
                g.db_session.query(UserGroup).filter(UserGroup.id==newdata[18]).delete()

        data = {}
        uid = newdata[12] #f_user:role_id
        old_user = g.db_session.query(User).filter(User.role_id==uid).first()	#原柜员信息

        data['user_name']=newdata[1]
        data['name']=newdata[2]
        data['work_status']=newdata[11]
        data['id_number']=newdata[4]
        data['is_safe']=newdata[10]
        data['is_test']=newdata[20]
        data['is_virtual']=newdata[21]
        data['edu']=newdata[22]
        data['is_headman']=newdata[23]
        g.db_session.query(User).filter(User.role_id==uid).update(data)

        data= {}
        bid = newdata[13]
        old_user_branch = g.db_session.query(UserBranch).filter(UserBranch.id==bid).first()
        old_branch = g.db_session.query(Branch).filter(Branch.role_id == old_user_branch.branch_id).first() #原机构信息

        data['branch_id']=newdata[5]
        new_branch = g.db_session.query(Branch).filter(Branch.role_id==newdata[5]).first() #新机构信息
        g.db_session.query(UserBranch).filter(UserBranch.id==bid).update(data)

        data={}
        ugid = newdata[14]
        group_name=newdata[3]
        data['user_id']=uid
        data['startdate']=newdata[0]
        p = g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name==u'人员性质').filter(Group.group_name==group_name).first()
        if p:
            data['group_id']=p.id
            if ugid:
                g.db_session.query(UserGroup).filter(UserGroup.id==ugid).update(data)
            else:
                g.db_session.add(UserGroup(**data))

        data={}
        ugid = newdata[15]
        #group_name=newdata[6]
        data['group_id']=newdata[6]
        data['user_id']=uid
        data['startdate']=newdata[0]
        if ugid:
            g.db_session.query(UserGroup).filter(UserGroup.id==ugid).update(data)
        else:
            g.db_session.add(UserGroup(**data))
        #p = g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name==u'部别').filter(Group.group_name==group_name).first()
        #if p :
        #    data['group_id']=p.id
        #    if ugid:
        #        g.db_session.query(UserGroup).filter(UserGroup.id==ugid).update(data)
        #    else:
        #        g.db_session.add(UserGroup(**data))


        data={}
        ugid = newdata[17]
        group_name=newdata[8]
        data['user_id']=uid
        data['startdate']=newdata[0]
        p = g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name==u'等级').filter(Group.group_name==group_name).first()
        if p :
            data['group_id']=p.id
            if ugid:
                g.db_session.query(UserGroup).filter(UserGroup.id==ugid).update(data)
            else:
                g.db_session.add(UserGroup(**data))

        data={}
        ugid = newdata[16]
        group_name=newdata[7]
        data['user_id']=uid
        data['startdate']=newdata[0]
        p = g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name==u'职务').filter(Group.group_name==group_name).first()
        if p :
            data['group_id']=p.id
            if ugid:
                g.db_session.query(UserGroup).filter(UserGroup.id==ugid).update(data)
            else:
                g.db_session.add(UserGroup(**data))

        data={}
        data['user_id']=uid
        data['startdate']=newdata[0]
        g.db_session.query(UserGroup).filter(UserGroup.user_id==uid).update({"startdate":newdata[0]})

        #不允许客户经理改为非客户经理,柜员变更成客户经理不允许有跨网点业绩
        teller_group_name = g.db_session.execute("select gr.group_name from user_group ug, group gr where ug.group_id = gr.id and gr.group_type_code = '2000' and ug.user_id = '%s'"%(uid)).fetchone()
        data={}
        ugid = newdata[18]
        group_name=newdata[9]
        data['user_id']=uid
        data['startdate']=newdata[0]
        p = g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name==u'客户经理类别').filter(Group.group_name==group_name).first()

        top_branch = g.db_session.query(Branch).filter(Branch.branch_code == '966000').first() #总行
        #跨支行调动,不能原来有业绩，前五位不同
        if old_branch.branch_code[1:-1] != new_branch.branch_code[1:-1]:
            account_count = g.db_session.query(AccountHook).filter(AccountHook.manager_no == old_user.user_name).count()
            if account_count > 0:
                raise Exception(u'跨支行调动不允许有业绩,请先移交!')

            cust_count = g.db_session.query(CustHook).filter(CustHook.manager_no == old_user.user_name).count()
            if cust_count > 0:
                raise Exception(u'跨支行调动不允许有业绩,请先移交!')

        #支行内调动,前五位相同
        if old_branch.branch_code != new_branch.branch_code and old_branch.branch_code[1:-1] == new_branch.branch_code[1:-1]:
            cust_count = g.db_session.query(CustHook).filter(CustHook.manager_no == old_user.user_name).count()
            if cust_count > 0:
                raise Exception(u'有客户认定业绩,请先移交!')

            if p.group_name == u'非客户经理':
                account_count = g.db_session.query(AccountHook).filter(AccountHook.manager_no == old_user.user_name, AccountHook.follow_cust == u'客户号优先').count()
                if account_count > 0:
                    raise Exception(u'该员工有跨客户优先业绩,请先移交!')


        """ 20161206日 人力要求删除此判断
        if (teller_group_name[0] == u'客户经理' or teller_group_name[0] == u'外聘客户经理') and p.group_name == u'非客户经理':
            raise Exception(u'不允许客户经理调整为非客户经理!')
        """

        if teller_group_name[0] == u'非客户经理' and (p.group_name == u'客户经理' or p.group_name == u'外聘客户经理'):	#检查是否只有本网点业绩
            account_count = g.db_session.query(AccountHook).filter(AccountHook.manager_no == old_user.user_name, AccountHook.org_no != new_branch.branch_code).count()
            if account_count > 0:
                raise Exception(u'该员工有跨网点业绩,请先移交!')

        cust_count = g.db_session.query(CustHook).filter(CustHook.manager_no == old_user.user_name, CustHook.org_no != new_branch.branch_code).count()
        if cust_count > 0:
            raise Exception(u'该员工有跨网点业绩,请先移交!')
        if p :
            data['group_id']=p.id
            if ugid:
                g.db_session.query(UserGroup).filter(UserGroup.id==ugid).update(data)
            else:
                g.db_session.add(UserGroup(**data))
        #g.db_session.query(User).filter(User.user_name==data['user_name']).update(data)
        return u"修改成功"
    def delete(self,**kwargs):
        newdata =  kwargs.get('newdata')
        tid = newdata[8]
        g.db_session.query(UserRelation).filter(UserRelation.id==tid).delete()
        return u'删除成功'

    def tsave(self, **kwargs):
        newda= kwargs.get('add_date')
        if(newda['x4'] is None):
            return u'员工信息请填写完整'
        if(newda['x2'] is None):
            return u'部门信息请填写完整'
        if(newda['x2'] is None):
            return u'职务工种信息请填写完整'
        
        nuser = User()
        nuser.user_name=newda['x4']
        nuser.name=newda['x5']
        nuser.work_status=newda['x12']
        nuser.id_number=newda['x7']
        nuser.is_safe=newda['x11']
        nuser.is_test=newda['x13']
        nuser.is_virtual=newda['x14']
        nuser.edu=newda['x15']
        nuser.is_headman=newda['x16']
        print nuser.is_test
        qm = g.db_session.query(User).filter(User.user_name==newda['x4']).first()
        if(qm):
            return u'员工号已存在，请修改！'
        else:
            g.db_session.add(nuser)
            g.db_session.flush()
        data= {}
        #p=g.db_session.query(Branch).filter(Branch.branch_code==newda['x2']).first()
        data['branch_id']=newda['x2']#p.role_id
        data['user_id']=nuser.role_id
        g.db_session.add(UserBranch(**data))
        
        data={}
        #group_name=newda['x3']
        data['user_id']=nuser.role_id
        data['startdate']=newda['x1']
        #qm = g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name==u'部别').filter(Group.group_name==group_name).first()
        #if(qm):
        data['group_id']=newda['x3']#qm.id
        g.db_session.add(UserGroup(**data))
        
        data={}
        group_name=newda['x6']
        data['user_id']=nuser.role_id
        data['startdate']=newda['x1']
        qm = g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name==u'人员性质').filter(Group.group_name==group_name).first()
        if(qm):
            data['group_id']=qm.id
            g.db_session.add(UserGroup(**data))
       
       
        data={}
        group_name=newda['x9']
        data['user_id']=nuser.role_id
        data['startdate']=newda['x1']
        qm = g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name==u'等级').filter(Group.group_name==group_name).first()
        if(qm):
            data['group_id']=qm.id
            g.db_session.add(UserGroup(**data))

        data={}
        group_name=newda['x8']
        data['user_id']=nuser.role_id
        data['startdate']=newda['x1']
        qm = g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name==u'职务').filter(Group.group_name==group_name).first()
        if(qm):
            data['group_id']=qm.id
            g.db_session.add(UserGroup(**data))
        data={}
        group_name=newda['x10']
        data['user_id']=nuser.role_id
        data['startdate']=newda['x1']
        qm = g.db_session.query(Group).join(GroupType,GroupType.type_code==Group.group_type_code).filter(GroupType.type_name==u'客户经理类别').filter(Group.group_name==group_name).first()
        if(qm):
            data['group_id']=qm.id
            g.db_session.add(UserGroup(**data))
        
        #新增该员工的系统账户
        nrid=nuser.role_id
        npassword = Password()
        npassword.algorithm='MD5'
        npassword.credential=to_md5("qwe123")
        g.db_session.add(npassword)
        g.db_session.flush()
        nfid=npassword.factor_id
        g.db_session.query(Factor).filter(Factor.factor_id==nfid).update({'user_id':nrid})
        
        return u"保存成功"
    
    
    def tdelt(self, **kwargs):
        delda= kwargs.get('del_date')

        old_user = g.db_session.query(User).filter(User.role_id==delda[12]).first()	#原柜员信息
        account_count = g.db_session.query(AccountHook).filter(AccountHook.manager_no == old_user.user_name).count()
        if account_count > 0:
            raise Exception(u'有业绩不允许删除,请先移交!')

        cust_count = g.db_session.query(CustHook).filter(CustHook.manager_no == old_user.user_name).count()
        if cust_count > 0:
            raise Exception(u'有业绩不允许删除,请先移交!')

        if(delda[14] is not None):
            g.db_session.query(UserGroup).filter(UserGroup.id==delda[14]).delete()
        if(delda[15] is not None):
            g.db_session.query(UserGroup).filter(UserGroup.id==delda[15]).delete()
        if(delda[16] is not None):
            g.db_session.query(UserGroup).filter(UserGroup.id==delda[16]).delete()
        if(delda[17] is not None):
            g.db_session.query(UserGroup).filter(UserGroup.id==delda[17]).delete()
        if(delda[18] is not None):
            g.db_session.query(UserGroup).filter(UserGroup.id==delda[18]).delete()
        if(delda[13] is not None):
            g.db_session.query(UserBranch).filter(UserBranch.id==delda[13]).delete()
        if(delda[12] is not None):
            #删除账户表
            f_id = g.db_session.query(Factor).filter(Factor.user_id==delda[12]).first().factor_id
            g.db_session.query(Password).filter(Password.factor_id==f_id).delete()
            g.db_session.query(Factor).filter(Factor.user_id==delda[12]).delete()
            #Session记录表
            g.db_session.query(UserSession).filter(UserSession.user_id==delda[12]).delete()
            g.db_session.query(Authentication).filter(Authentication.user_id==delda[12]).delete()
            #f_user
            g.db_session.query(UserGroup).filter(UserGroup.user_id==delda[12]).delete()
            g.db_session.query(User).filter(User.role_id==delda[12]).delete()
        return u"删除成功" 
    def save(self, **kwargs):
        kwargs.pop('0')
        for i in kwargs:
            if kwargs.get(i) == u'是':
                kwargs[i] = 1
            if kwargs.get(i) == u'否':
                kwargs[i] = 0
        g.db_session.add(UserRelation(**kwargs))
        #self.ckyy = ['yyrq','yyckje','khmc','yyblrq','yybljg','bz','ck_type']
        #newdata =  kwargs.get('updata')
        #data ={}
        #tid = newdata.get('id')
        #if not tid:return u"无更新主键"
        #for k,v in newdata.items():
        #    if k in self.ckyy : data[k] = v
        #g.db_session.query(UserRelation).filter(UserRelation.id==tid).update(data)
        return u"保存成功"
     

    def simple_select(self,**kwargs):
        self.filterkey = ['staff_code','id','is_khjl','is_zhgy','is_zhhz','is_xdkj','is_flczr','staff_cms_code','staff_sop_code','card_num']
        filterdata = kwargs.get('filterdata')
        data={}
        for k,v in filterdata.items():
            if k in self.filterkey: data[k] = v
        q = g.db_session.query(UserRelation)
        for attr,value in data.items():
            q= q.filter(getattr(UserRelation,attr)==value)
        return q.all()

    '''修改后插入历史表'''
    def update_his(self, **kwargs):
        olddata =  kwargs.get('olddata')
        g.db_session.add(GroupHis(**olddata))
        return u"保存成功"
    def edit_his(self, **kwargs):
        olddata=kwargs.get('his_data')
        current_app.logger.debug('olddata')
        current_app.logger.debug(olddata)
        g.db_session.query(GroupHis).filter(GroupHis.id==olddata['id']).update(olddata)
        return u"编辑成功"
    def delete_his(self, **kwargs):
        olddata=kwargs.get('his_data')
        g.db_session.query(GroupHis).filter(GroupHis.id==olddata['id']).delete()
        return u"删除成功" 

