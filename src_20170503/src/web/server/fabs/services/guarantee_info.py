# -*- coding: utf-8 -*-
import hashlib
import copy
import datetime
from flask import json, g

from ..model.guarantee import *
from ..model.contract import *
from ..model.party import *

from .service import BaseService
from ..database import simple_session

class GuaranteeInfoService(BaseService):

    def query_party(self,customer_name):
        u''' 查询party--借款人类型  '''
        party = g.db_session.query(Party).filter(Party.name == customer_name).first()
        rst={}
        rst.update({'party':party})
        return rst

    def query_allinfo(self,all_contract_no):
        u''' 引用查询合同编号 '''
        contract= g.db_session.query(Contract).filter(Contract.contract_no == all_contract_no).first()
        if contract:
            guarantee_info= g.db_session.query(GuaranteeContractRelation).filter(GuaranteeContractRelation.contract_id == contract.contract_id).first()
            all_contract= g.db_session.query(GuaranteeContractRelation).filter(GuaranteeContractRelation.contract_id == contract.contract_id).all()
            info = g.db_session.query(GuaranteeInfo,GuaranteeRelation).outerjoin(GuaranteeRelation,GuaranteeRelation.gty_info_id==GuaranteeInfo.id).filter(GuaranteeInfo.id == guarantee_info.gty_info_id).first()
            rst={}
            rst.update({'guarantee_info':info.GuaranteeInfo})
            if info.GuaranteeRelation:
               rst.update({'guarantee':info.GuaranteeRelation.guarantee})
            rst.update({'contract_id':contract.contract_id})
            rst.update({'contract':all_contract})
            rst.update({'msg':u'合同号存在'})
            return rst
        else:
            return {'msg':u'合同号不存在'}
    def save_contract(self,contract_id,**kwargs):
        u''' 添加引用信息 '''
        guarantee_info=kwargs.get('guarantee_info')
        guarantee=kwargs.get('guarantee')
        if guarantee:
           gty_type=guarantee.get('pledge_type')
           guarantee.pop('gty_id')
           guarantee.pop('gty_type')
           guarantee.pop('brw_app_id')
           guarantee.pop('gty_method')
           guarantee.pop('gty_detail')
           guarantee.pop('gty_ct')
           guarantee.pop('gty_amout')
           guarantee.pop('brw_cus_id')
           guarantee.pop('brw_cus_name')
           guarantee.pop('brw_cus_type')
           guarantee.pop('gty_cus_id')
           guarantee.pop('gty_cus_name')
           guarantee.pop('tgty_cus_id')
           guarantee.pop('tgty_cus_name')
           guarantee.pop('bfirst_gty')
           guarantee.pop('bboard_appr')
           guarantee.pop('gty_contract_id')
           guarantee.pop('area')
           guarantee.pop('pre_eval_value')
           guarantee.pop('eval_value')
           guarantee.pop('conf_value')
           guarantee.pop('conf_amount')
           guarantee.pop('except_value')
           guarantee.pop('except_amount')
           guarantee.pop('eval_type')
           guarantee.pop('mrge_rate')
           guarantee.pop('pledge_amount')
           guarantee.pop('reg_org_id')
           guarantee.pop('reg_by')
           guarantee.pop('gty_cus_type')
           guarantee.pop('gty_due_date')
           guarantee.pop('ins_type')
           guarantee.pop('ins_id')
           guarantee.pop('ins_due_date')
           guarantee.pop('ins_percent')
           guarantee.pop('reg_date')
           guarantee.pop('updated_time')
           guarantee.pop('gty_status')
           guarantee.pop('max_gty_amount')
           guarantee.pop('cur_gty_amount')
           guarantee.pop('insp_time')
           guarantee.pop('insp1_id')
           guarantee.pop('insp2_id')
           guarantee.pop('insp_result')
           guarantee.pop('gty_total')
           guarantee.pop('gty_kind')
           guarantee.pop('entitle_id')
           guarantee.pop('entitle_name')
           guarantee.pop('entitle_type')
           guarantee.pop('pledge_type')
           guarantee.pop('pledge_name')
           guarantee.pop('cert_id')
           guarantee.pop('sec_cert_id')
           guarantee.pop('eval_org')
           guarantee.pop('out_reg_org')
           guarantee.pop('out_reg_date')
           guarantee.pop('guarantee_relation')
           if gty_type == '抵押-房产':
               other=MrgeBuilding(**guarantee)
           elif gty_type == '抵押-土地':
               other=MrgeLand(**guarantee)
           elif gty_type == '抵押-设备':
               other=MrgeEqp(**guarantee)
           elif gty_type == '抵押-其他':
               other=MrgeOther(**guarantee)
           elif gty_type == '抵押-交通工具':
               other=MrgeVch(**guarantee)
           elif gty_type == '抵押-动产':
               other=MrgeMovable(**guarantee)
           elif gty_type == '质押-个人定期存单':
               other=PawnPerStub(**guarantee)
           elif gty_type == '质押-单位定期存单':
               other=PawnStub(**guarantee)
           elif gty_type == '质押-本行理财产品':
               other=PawnFinance(**guarantee)
           elif gty_type == '质押-账户资金':
               other=PawnSaving(**guarantee)
           elif gty_type == '质押-银行承兑汇票':
               other=PawnAccp(**guarantee)
           elif gty_type == '质押-应收账款':
               other=PawnAccRec(**guarantee)
           elif gty_type == '质押-其他':
               other=PawnOther(**guarantee)
        guarantee_info.pop('guarantee_contract_relation')
        guarantee_info.pop('guarantee_relation')
        guarantee_info.pop('id')
        guarantee_info.pop('application')
        gua = GuaranteeInfo(**guarantee_info)
        g.db_session.add(gua)
        contract=GuaranteeContractRelation(guarantee_info=gua,contract_id=contract_id)
        if guarantee:
           guarantee=GuaranteeRelation(guarantee_info=gua,guarantee=other)
        return True

    def InfoSave(self,**kwargs):
        u''' 抵质押物保存 '''
        infoid=kwargs.get('id')
        kwargs.pop('guarantee_contract_relation')
        kwargs.pop('guarantee_relation')
        kwargs.pop('id')
        kwargs.pop('application')
        kwargs.pop('contract_no')
        g.db_session.query(GuaranteeInfo).filter(GuaranteeInfo.id == infoid).update(kwargs)
        return True

    def InfoSaves(self,**kwargs):
        u''' 抵质押物保存 完善字段 '''
        infoid=kwargs.get('id')
        aa=kwargs.get('state')
        print '***************'
        print aa
        state = {'state':u'完善'}
        g.db_session.query(GuaranteeInfo).filter(GuaranteeInfo.id == infoid).update(state)
        return True

    def save(self,**kwargs):
        u''' 添加抵质押信息 '''
        gua = GuaranteeInfo(**kwargs)
        g.db_session.add(gua)
        return {'msg':u'添加成功','guarantee_info_id':gua.id}

    def query(self,guarantee_info_id):
        u''' 查询抵质押信息 '''
        info = g.db_session.query(GuaranteeInfo,GuaranteeRelation).outerjoin(GuaranteeRelation,GuaranteeRelation.gty_info_id==GuaranteeInfo.id).filter(GuaranteeInfo.id == guarantee_info_id).first()
        rst={}
        rst.update({'guarantee_info':info.GuaranteeInfo})
        if info.GuaranteeRelation:
             rst.update({'guarantee':info.GuaranteeRelation.guarantee})
        return rst

    def query_infos(self,application_id):
        u''' 查询抵质押信息 '''
        rst = g.db_session.query(GuaranteeInfo,Contract).outerjoin(GuaranteeContractRelation,GuaranteeContractRelation.gty_info_id==GuaranteeInfo.id).outerjoin(Contract,Contract.contract_id==GuaranteeContractRelation.contract_id).filter(GuaranteeInfo.application_id == application_id).order_by(GuaranteeInfo.id).all()
        guarantee_info_list=[]
        guarantee_info_list=[{'guarantee_info':r.GuaranteeInfo,'contract':r.Contract} for r in rst]
        return guarantee_info_list


    def detele(self,guarantee_info_id):
        u''' 删除抵质押信息 '''
        g.db_session.query(GuaranteeInfo).filter(GuaranteeInfo.id == guarantee_info_id).delete()
        return {'msg':u'删除成功'}

    def query_method(self):
        u'''查询抵质押物数据 '''
        rst=g.db_session.query(GuaranteeMethod).all()

        return rst



