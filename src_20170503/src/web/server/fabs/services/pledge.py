# -*- coding: utf-8 -*-
import hashlib
import copy
import datetime
import xlrd
from flask import json, g
from ..base import core_inf
from ..model.guarantee import *

from .service import BaseService
from ..database import simple_session

class PledgeService(BaseService):
    def __init__(self):
        self.db_session = simple_session()

    def PaperContract(self,**kwargs):
        print kwargs
        print '-------------'
        return True

    def query(self,pledge_type=None,gty_id=None,gty_cus_name=None):
        q = self.db_session.query(Guarantee)
        if gty_id:
            q = q.filter(Guarantee.gty_id == gty_id[0])
        if pledge_type:
            q = q.filter(Guarantee.pledge_type == pledge_type[0])
        if gty_cus_name:
            q = q.filter(Guarantee.gty_cus_name == gty_cus_name[0])
        return q.limit(20).all()

    def save(self,**kwargs):
        u''' 抵质押保存修改 '''
        gty_info_id = kwargs.get('gty_info_id')
        if gty_info_id:
            kwargs.pop('gty_info_id')
        
        #other= Guarantee(**kwargs)
        gty_type = kwargs.get('pledge_type')
        if gty_type == '抵押-房屋所有权':
             other=MrgeBuilding(**kwargs)
        elif gty_type == '抵押-设备+动产':
             other=MrgeEqpMovable(**kwargs)
        elif gty_type == '抵押-土地使用权':
             other=MrgeLand(**kwargs)
        elif gty_type == '抵押-设备':
             other=MrgeEqp(**kwargs)
        elif gty_type == '抵押-其他':
             other=MrgeOther(**kwargs)
        elif gty_type == '抵押-交通工具':
             other=MrgeVch(**kwargs)
        elif gty_type == '抵押-动产':
             other=MrgeMovable(**kwargs)
        elif gty_type == '质押-个人定期存单':
             other=PawnPerStub(**kwargs)
        elif gty_type == '质押-单位定期存单':
             other=PawnStub(**kwargs)
        elif gty_type == '质押-本行理财产品':
             other=PawnFinance(**kwargs)
        elif gty_type == '质押-账户资金':
             other=PawnSaving(**kwargs)
        elif gty_type == '质押-银行承兑汇票':
             other=PawnAccp(**kwargs)
        elif gty_type == '质押-应收账款':
             other=PawnAccRec(**kwargs)
        elif gty_type == '质押-其他':
             other=PawnOther(**kwargs)
        if gty_info_id:
             gua = GuaranteeRelation(gty_info_id=gty_info_id,guarantee=other)
             self.db_session.add(gua)
        else:
             self.db_session.add(other)
        self.db_session.commit()

    def delete(self,**kwargs):
        u''' 删除抵质押物 '''
        gty_id = kwargs.get('gty_id')[0]
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).delete()
        self.db_session.commit()

    def update(self,**kwargs):
        u''' 修改'''
        gty_id = kwargs.get('gty_id')
        gty_type = kwargs.get('pledge_type')
        kwargs.pop('gty_id')
        kwargs.pop('gty_type')
        kwargs.pop('brw_app_id')
        kwargs.pop('gty_method')
        kwargs.pop('gty_detail')
        kwargs.pop('gty_ct')
        kwargs.pop('gty_amout')
        kwargs.pop('brw_cus_id')
        kwargs.pop('brw_cus_name')
        kwargs.pop('brw_cus_type')
        kwargs.pop('gty_cus_id')
        kwargs.pop('gty_cus_name')
        kwargs.pop('tgty_cus_id')
        kwargs.pop('tgty_cus_name')
        kwargs.pop('bfirst_gty')
        kwargs.pop('bboard_appr')
        kwargs.pop('gty_contract_id')
        kwargs.pop('area')
        kwargs.pop('pre_eval_value')
        kwargs.pop('eval_value')
        kwargs.pop('conf_value')
        kwargs.pop('conf_amount')
        kwargs.pop('except_value')
        kwargs.pop('except_amount')
        kwargs.pop('eval_type')
        kwargs.pop('mrge_rate')
        kwargs.pop('pledge_amount')
        kwargs.pop('reg_org_id')
        kwargs.pop('reg_by')
        kwargs.pop('gty_cus_type')
        kwargs.pop('gty_due_date')
        kwargs.pop('ins_type')
        kwargs.pop('ins_id')
        kwargs.pop('ins_due_date')
        kwargs.pop('ins_percent')
        kwargs.pop('reg_date')
        kwargs.pop('updated_time')
        kwargs.pop('gty_status')
        kwargs.pop('max_gty_amount')
        kwargs.pop('cur_gty_amount')
        kwargs.pop('insp_time')
        kwargs.pop('insp1_id')
        kwargs.pop('insp2_id')
        kwargs.pop('insp_result')
        kwargs.pop('gty_total')
        kwargs.pop('gty_kind')
        kwargs.pop('entitle_id')
        kwargs.pop('entitle_name')
        kwargs.pop('entitle_type')
        kwargs.pop('pledge_type')
        kwargs.pop('pledge_name')
        kwargs.pop('cert_id')
        kwargs.pop('sec_cert_id')
        kwargs.pop('eval_org')
        kwargs.pop('out_reg_org')
        kwargs.pop('out_reg_date')
        kwargs.pop('guarantee_relation')
        kwargs.pop('guarantee')
        print gty_type
        if gty_type == '抵押-房屋所有权':
             self.db_session.query(MrgeBuilding).filter(MrgeBuilding.gty_id == gty_id).update(kwargs)
        elif gty_type == '抵押-土地使用权':
             self.db_session.query(MrgeLand).filter(MrgeLand.gty_id == gty_id).update(kwargs)
        elif gty_type == '抵押-设备':
             self.db_session.query(MrgeEqp).filter(MrgeEqp.gty_id == gty_id).update(kwargs)
        elif gty_type == '抵押-设备+动产':
             self.db_session.query(MrgeEqpMovable).filter(MrgeEqpMovable.gty_id == gty_id).update(kwargs)
        elif gty_type == '抵押-其他':
             self.db_session.query(MrgeOther).filter(MrgeOther.gty_id == gty_id).update(kwargs)
        elif gty_type == '抵押-交通工具':
             self.db_session.query(MrgeVch).filter(MrgeVch.gty_id == gty_id).update(kwargs)
        elif gty_type == '抵押-动产':
             self.db_session.query(MrgeMovable).filter(MrgeMovable.gty_id == gty_id).update(kwargs)
        elif gty_type == '质押-个人定期存单':
             self.db_session.query(PawnPerStub).filter(PawnPerStub.gty_id == gty_id).update(kwargs)
        elif gty_type == '质押-单位定期存单':
             self.db_session.query(PawnStub).filter(PawnStub.gty_id == gty_id).update(kwargs)
        elif gty_type == '质押-本行理财产品':
             self.db_session.query(PawnFinance).filter(PawnFinance.gty_id == gty_id).update(kwargs)
        elif gty_type == '质押-账户资金':
             self.db_session.query(PawnSaving).filter(PawnSaving.gty_id == gty_id).update(kwargs)
        elif gty_type == '质押-银行承兑汇票':
             self.db_session.query(PawnAccp).filter(PawnAccp.gty_id == gty_id).update(kwargs)
        elif gty_type == '质押-应收账款':
             self.db_session.query(PawnAccRec).filter(PawnAccRec.gty_id == gty_id).update(kwargs)
        elif gty_type == '质押-其他':
             self.db_session.query(PawnOther).filter(PawnOther.gty_id == gty_id).update(kwargs)
        self.db_session.commit()

    def upload(self, filepath, gty_id):
        """
            清单录入
        """
        print '导入开始'
        data = xlrd.open_workbook(filepath)
        sheet = data.sheet_by_index(0)
        #行
        nrows = sheet.nrows
        bill_type_sign = ""
        list = []
        print sheet.cell(1,1).value
        if sheet.cell(2,0).value == '序号':
            for r in range(3,nrows):
                if sheet.cell(r,0).value == '':
                    break
                name = sheet.cell(r,1).value
                amount = sheet.cell(r,2).value
                company = sheet.cell(r,3).value
                status = sheet.cell(r,4).value
                location = sheet.cell(r,5).value
                certificate = sheet.cell(r,6).value
                value = sheet.cell(r,7).value
                other_value = sheet.cell(r,8).value
                other = sheet.cell(r,9).value
                list.append({'name':name, 'amount':amount, 'company':company, 'status':status, 'location':location, 'certificate':certificate, 'value':value, 'other_value':other_value, 'other':other})
            for b in list:
                b.update({'gty_id':gty_id})
                b = MrgeMovable_List(**b)
                g.db_session.add(b)
            g.db_session.commit()
            return 'succ'
        if sheet.cell(1,1).value == '票据号码':
            for r in range(2,nrows):
                if sheet.cell(r,0).value == '': 
                    break
                accp_no = sheet.cell(r,1).value
                accp_value = sheet.cell(r,2).value
                reg_date = sheet.cell(r,3).value
                end_date = sheet.cell(r,4).value
                people = sheet.cell(r,5).value
                bank = sheet.cell(r,6).value
                list.append({'accp_no':accp_no, 'accp_value':accp_value, 'reg_date':reg_date, 'end_date':reg_date, 'people':people, 'bank':bank})
            for b in list:
                b.update({'gty_id':gty_id})
                b = PawnAccp_List(**b)
                g.db_session.add(b)
            g.db_session.commit()
            return 'succ'
        else:
            return 'err'

    """
    def save_stub(self,**kwargs):
        u''' 质押-stub 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_stub(self,**kwargs):
        u'''质押-stub 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)
    def save_saving(self,**kwargs):
        u''' 质押-saving 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_saving(self,**kwargs):
        u'''质押-saving 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_nd(self,**kwargs):
        u''' 质押-nd 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_nd(self,**kwargs):
        u'''质押-nd 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_ins(self,**kwargs):
        u''' 质押-ins 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_ins(self,**kwargs):
        u'''质押-ins 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_crd(self,**kwargs):
        u''' 质押-crd 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_crd(self,**kwargs):
        u'''质押-crd 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_fe_saving(self,**kwargs):
        u''' 质押-fe_saving 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_fe_saving(self,**kwargs):
        u'''质押-fe_saving 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_ware_lst(self,**kwargs):
        u''' 质押-ware_lst 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_ware_lst(self,**kwargs):
        u'''质押-ware_lst 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_do(self,**kwargs):
        u''' 质押-do 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_do(self,**kwargs):
        u'''质押-do 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_vch(self,**kwargs):
        u''' 质押-vch 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_vch(self,**kwargs):
        u'''质押-vch 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_vch_qlf(self,**kwargs):
        u''' 质押-vch_qlf 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_vch_qlf(self,**kwargs):
        u'''质押-vch_qlf 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_bond(self,**kwargs):
        u''' 质押-bond 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_bond(self,**kwargs):
        u'''质押-bond 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_ipo_int(self,**kwargs):
        u''' 质押-ipo_int 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_ipo_int(self,**kwargs):
        u'''质押-ipo_int 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_non_ipo_int(self,**kwargs):
        u''' 质押-non_ipo_int 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_non_ipo_int(self,**kwargs):
        u'''质押-non_ipo_int 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_acc_rec(self,**kwargs):
        u''' 质押-acc_rec 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_acc_rec(self,**kwargs):
        u'''质押-acc_rec 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_cvrg(self,**kwargs):
        u''' 质押-cvrg 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_cvrg(self,**kwargs):
        u'''质押-cvrg 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_accp(self,**kwargs):
        u''' 质押-accp 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_accp(self,**kwargs):
        u'''质押-accp 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)

    def save_bill(self,**kwargs):
        u''' 质押-bill 增加 '''
        ddd= Guarantee(**kwargs)
        self.db_session.add(ddd)
        self.db_session.commit()

    def update_bill(self,**kwargs):
        u'''质押-bill 修改'''
        gty_id = kwargs.get('gty_id')
        self.db_session.query(Guarantee).filter(Guarantee.gty_id == gty_id).update(kwargs)
        """
