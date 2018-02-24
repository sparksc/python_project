# -*- coding: utf-8 -*-
"""
    yinsho.services.PermissionService
    #####################

    yinsho UsersService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func,text
from sqlalchemy.orm import joinedload_all,joinedload

from ..base import utils
from ..model import Menu, User, UserGroup, Group, GroupMenu, Branch, UserBranch, PerCon, Target ,Pe_contract_detail
  

class PerformanceService():
    """ Performance Service  """

    # TODO: Move to the net db_session object


    def load(self):
        results = g.db_session.query(PerCon,User).\
                    join(User,User.role_id==PerCon.pe_pic).all()
        items = []
        for p,u in results:
            items.append({'id':p.id,'pe_type':p.pe_type,'pe_object':p.pe_object,'pe_pic':u.name,'pe_freq':p.pe_freq,'date':p.date,'score':p.score})    
        return items    
 
    def add(self,**kwargs):
        contract_id = kwargs.get('contract_id')
        pe_pei_id = kwargs.get('pe_pei_id')
        g.db_session.add(Pe_contract_detail(contract_id=contract_id,pe_pei_id=pe_pei_id))
        return u"添加成功"    

    def save(self, **kwargs):
        item_weight = kwargs.get('item_weight')
        item_target = kwargs.get('item_target')
        item_id = kwargs.get('item_id')
        target_id = kwargs.get('target_id')
        g.db_session.query(Pe_contract_detail).filter(and_(Pe_contract_detail.contract_id==item_id,Pe_contract_detail.pe_pei_id==target_id)).update({Pe_contract_detail.weight:item_weight,Pe_contract_detail.target:item_target})
        return u"设定成功"
    
    def find(self,**kwargs):
        item_id = kwargs.get('item_id')
        target_pcd_results = g.db_session.query(Target,Pe_contract_detail)\
              .join(Pe_contract_detail,Pe_contract_detail.pe_pei_id==Target.pei_id)\
              .filter(Pe_contract_detail.contract_id==item_id).all()
        items=[]
        for target,pcd in target_pcd_results:
            items.append({'target_id':target.pei_id,'target_name':target.name,'target_type':target.TYPE,'target_data_src':target.data_src,'pcd_weight':pcd.weight,'pcd_target':pcd.target,'target_desc':target.desc,'pcd_fact':pcd.fact,'pcd_score':pcd.score})
        return items
    
    def targets(self,**kwargs):
        item_id = kwargs.get('item_id')
        item_freq = kwargs.get('item_freq')
        item_type = kwargs.get('item_type')
        items = g.db_session.query(Target).from_statement(text('SELECT * FROM (SELECT PEI_ID,PEI_FREQ,TYPE,NAME,DEPT,OBJECT_TYPE,DESC,DATA_SRC,IS_MANUAL_INPUT,IS_ENABLED FROM PE_PEI_DEF DEF WHERE NOT EXISTS (SELECT PEI_ID FROM PE_CONTRACT_DETAIL DET WHERE DET.PE_PEI_ID=DEF.PEI_ID AND DET.CONTRACT_ID=:contract_id)) A WHERE A.PEI_FREQ=:pei_freq AND A.OBJECT_TYPE=:object_type order by PEI_ID')).\
               params(contract_id=item_id,pei_freq=item_freq,object_type=item_type).all()
        return items
   
    def objects(self):
        branches = g.db_session.query(Branch).order_by(Branch.branch_code).all()
        return [{"branch_code":b.branch_code,"branch_name":b.branch_name,"role_id":b.role_id,"parent_id":b.parent_id} for b in branches]
    
    def persons(self,**kwargs):
        branch_name = kwargs.get('branch_name')
        users = g.db_session.query(User).\
        join(UserBranch,UserBranch.user_id==User.role_id).\
        join(Branch,Branch.role_id==UserBranch.branch_id).\
        filter(Branch.branch_name==branch_name).order_by(User.user_name).all()
        return [{"role_id":u.role_id,"user_name":u.user_name,"name":u.name} for u in users]

    def _del(self,**kwargs):
        item_id = kwargs.get('item_id')
        print item_id
        g.db_session.query(PerCon).filter(PerCon.id==item_id).delete()
        return u'删除成功'       

    def edit_save(self, **kwargs):
        item_type = kwargs.get('item_type')
        item_object = kwargs.get('item_object')
        item_person = kwargs.get('item_person')
        item_time = kwargs.get('item_time')
        item_id = kwargs.get('item_id')
        now = datetime.datetime.now()
        g.db_session.query(PerCon).filter(PerCon.id==item_id).update({PerCon.pe_type:item_type,PerCon.pe_object:item_object,PerCon.pe_pic:item_person,PerCon.pe_freq:item_time})
        return u"编辑成功"

    def add_save(self, **kwargs):
        item_type = kwargs.get('item_type')
        item_object = kwargs.get('item_object')
        item_person = kwargs.get('item_person')
        item_time = kwargs.get('item_time')
        item_date = kwargs.get('item_date')
        g.db_session.add(PerCon(pe_type=item_type,pe_object=item_object,pe_pic=item_person,pe_freq=item_time,DATE=item_date))
        return u"保存成功"

