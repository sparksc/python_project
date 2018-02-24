# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all

from ..base import utils
from ..model import Branch,Menu,User,UserBranch,CustHook,CustHookBatch,HookSingleMove,AccountHook,EbankOrg


class custHookMagService():
    """ Target Service  """
    #单笔分润,新增分润审批记录(帐号)
    def single_move(self, **kwargs):
        movedata = kwargs.get('movedata')
        data = {}
        data['typ'] = movedata['type']
        data['move_id'] = movedata['move_id']
        data['account_no'] = movedata['account_no']
        data['from_teller'] = movedata['from_teller']
        data['to_teller'] = movedata['to_teller']
        data['percentage'] = movedata['percentage']
        data['balance'] = movedata['balance']
        data['org_no'] = movedata['org_no']
        data['date_id'] = str(movedata['date_id'])
        data['status'] = '待审批'

        g.db_session.add(HookSingleMove(**data))
        return u"已提交审批"
    
    #单笔分润,新增分润审批记录(客户号)
    def single_move_cust(self, **kwargs):
        movedata = kwargs.get('movedata')
        data = {}
        data['typ'] = movedata['type']
        data['move_id'] = movedata['move_id']
        data['cust_no'] = movedata['cust_no']
        data['from_teller'] = movedata['from_teller']
        data['to_teller'] = movedata['to_teller']
        data['percentage'] = movedata['percentage']
        data['balance'] = movedata['balance']
        data['org_no'] = movedata['org_no']
        data['date_id'] = str(movedata['date_id'])
        data['status'] = '待审批'

        g.db_session.add(HookSingleMove(**data))
        return u"已提交审批"

    #分润审批(帐号)
    def single_approve(self, **kwargs):
        updatelist = kwargs.get('update_key')
        note = kwargs.get('note')
        status = kwargs.get('status')
        
        for pid in updatelist:
            m = g.db_session.query(HookSingleMove).filter(HookSingleMove.id == pid).first()
            hook_percent = g.db_session.query(AccountHook).filter(AccountHook.id == m.move_id).first().percentage

            if status == u'同意':#审批通过,改变中间表记录状态
                g.db_session.query(HookSingleMove).filter(HookSingleMove.id == pid).update({'status':u'同意'})
                accthk = g.db_session.query(AccountHook).filter(AccountHook.id == m.move_id).first()
                #改变原挂钩关系占比并判断是否需要新增挂钩记录
                if int(m.percentage) == int(hook_percent):
                    g.db_session.query(AccountHook).filter(AccountHook.id == m.move_id).update({'manager_no':m.to_teller})
                else:#挂钩表中新增一条分润记录
                    data = {}
                    p = int(hook_percent) - int(m.percentage)
                    g.db_session.query(AccountHook).filter(AccountHook.id == m.move_id).update({"percentage":p})
                    data['manager_no'] = m.to_teller
                    data['org_no'] = accthk.org_no
                    data['percentage'] = m.percentage
                    data['hook_type'] = accthk.hook_type
                    data['start_date'] = accthk.start_date
                    data['end_date'] = accthk.end_date
                    data['status'] =  accthk.status
                    data['etl_date'] = accthk.etl_date
                    data['src'] = accthk.src
                    data['typ'] = accthk.typ
                    data['account_no'] = accthk.account_no
                    data['note'] = accthk.note
                    data['sub_typ'] = accthk.sub_typ
                    data['card_no'] = accthk.card_no
                    data['follow_cust'] = accthk.follow_cust
                    data['balance'] = accthk.balance
                    g.db_session.add(AccountHook(**data))
            else:#审批不通过
                g.db_session.query(HookSingleMove).filter(HookSingleMove.id == pid).update({'status':u'不同意'})
        return u'审批完成'

    #分润审批(客户号) 其中客户号下面的帐号要一并分润
    def single_approve_cust(self, **kwargs):
        updatelist = kwargs.get('update_key')
        note = kwargs.get('note')
        status = kwargs.get('status')
        
        for pid in updatelist:
            m = g.db_session.query(HookSingleMove).filter(HookSingleMove.id == pid).first()
            hook_percent = g.db_session.query(CustHook).filter(CustHook.id == m.move_id).first().percentage

            if status == u'同意':#审批通过,改变中间表记录状态
                g.db_session.query(HookSingleMove).filter(HookSingleMove.id == pid).update({'status':u'同意'})
                custhk = g.db_session.query(CustHook).filter(CustHook.id == m.move_id).first()
                #改变原挂钩关系占比并判断是否需要新增挂钩记录
                if int(m.percentage) == int(hook_percent):
                    g.db_session.query(CustHook).filter(CustHook.id == m.move_id).update({'manager_no':m.to_teller})
                else:#挂钩表中新增一条分润记录
                    data = {}
                    p = int(hook_percent) - int(m.percentage)
                    g.db_session.query(CustHook).filter(CustHook.id == m.move_id).update({"percentage":p})
                    data['manager_no'] = m.to_teller
                    data['org_no'] = custhk.org_no
                    data['percentage'] = m.percentage
                    data['hook_type'] = custhk.hook_type
                    data['start_date'] = custhk.start_date
                    data['end_date'] = custhk.end_date
                    data['status'] =  custhk.status
                    data['etl_date'] = custhk.etl_date
                    data['src'] = custhk.src
                    data['typ'] = custhk.typ
                    data['cust_no'] = custhk.cust_no
                    data['note'] = custhk.note
                    data['sub_typ'] = custhk.sub_typ
                    data['balance'] = custhk.balance
                    g.db_session.add(CustHook(**data))
            else:#审批不通过
                g.db_session.query(HookSingleMove).filter(HookSingleMove.id == pid).update({'status':u'不同意'})
        return u'审批完成'

    def cust_move(self, **kwargs):
        move_id = kwargs.get('move_id')
        org_no = kwargs.get('move_org_no')
        manager_no = kwargs.get('move_manager_no')
        start_date = kwargs.get('move_start_date')
        end_date = kwargs.get('move_end_date')
        percentage = kwargs.get('move_percentage')

        print 'type:', type(percentage)

        #进行比例的处理 TBD
        old_data = g.db_session.query(CustHook).filter(CustHook.id == move_id).first()
        e_start_date = start_date[0:4] + start_date[5:7] + start_date[8:10]
        e_end_date = end_date[0:4] + end_date[5:7] + end_date[8:10]
        g.db_session.add(CustHook(org_no=org_no,manager_no=manager_no,start_date=int(e_start_date),end_date=int(e_end_date),percentage=percentage,hook_type=old_data.hook_type,status=old_data.status,src=old_data.src,typ=old_data.typ,note=old_data.note,cust_no=old_data.cust_no,etl_date=old_data.etl_date))
        g.db_session.query(CustHook).filter(CustHook.id == move_id).delete()
        return u"操作成功"

    def batch_cust_move_before(self, **kwargs):
        updatelist = kwargs.get('update_key')
        from_teller_no = kwargs.get('from_teller_no')
        to_teller_no = kwargs.get('to_teller_no')

        count = 0
        sum = 0
        typ = u'存款'
        cust_hook_batch = custHookBatch(from_teller_no=from_teller_no, to_teller_no = to_teller_no, total_count=count, total_amount=sum, typ=typ, note=note, hook_typ=u'客户', deal_status=u'预提交审批')
        g.db_session.add(cust_hook_batch)
        g.db_session.flush()

        for pid  in updatelist:
            old_data  = g.db_session.query(CustHook).filter(CustHook.id == pid).first()
            datadict = {}
            status = u'预提交审批'
            datadict['status'] = status
            datadict['batch_id'] = cust_hook_batch.id
            g.db_session.query(CustHook).filter(CustHook.id == pid).update(datadict)

            count = count + 1
            sum = sum + old_data.balance
            count = count + 1
            typ = old_data.typ

        cust_hook_batch.total_amount = sum
        cust_hook_batch.total_count = count
        cust_hook_batch.typ = typ

        return u'移交预处理成功'

    def batch_cust_move_delete(self, **kwargs):
        batch_id = kwargs.get('batch_id')

        g.db_session.query(custHookBatch).filter(custHookBatch.id == batch_id).update({'reason':u'个人撤销', 'deal_status': u'已撤销'})
        g.db_session.query(CustHook).filter(CustHook.batch_id == batch_id).update({'status':u'预提交审批'})

        return u'撤销成功'

    def batch_cust_move(self, **kwargs):
        batch_id = kwargs.get('batch_id')

        g.db_session.query(custHookBatch).filter(custHookBatch.id == batch_id).update({'reason':u'个人撤销', 'deal_status': u'待审批'})
        g.db_session.query(CustHook).filter(CustHook.batch_id == batch_id).update({'status':u'待审批'})

        return u'移交成功'

    def get_top(self, **kwargs):
        id = kwargs.get('id')
        if id:
            top = g.db_session.query(CustHook).filter(CustHook.id == id).all()
        return top

    def distribute2(self, **kwargs):
        updatelist = kwargs.get('update_key')
        newdata =  kwargs.get('newdata')
        count = 0
        print newdata

        for pid in updatelist:
            old = g.db_session.query(CustHook).filter(CustHook.id == pid).first()
            org_no = newdata.get('org_no')
            cust_in_no = old.cust_in_no

            print old.id, org_no, cust_in_no
            """
            依次判断该客户在该网点是否存在电子银行/贷款/存款挂钩关系,按照电子银行/贷款/存款优先级认定该分配记录,若都没有认定关系,则状态变为待手工.
            """
            ebk = g.db_session.query(CustHook).filter(CustHook.org_no == org_no, CustHook.cust_in_no == cust_in_no, CustHook.typ == u'电子银行', CustHook.status == u'正常').first()
            loan = g.db_session.query(CustHook).filter(CustHook.org_no == org_no, CustHook.cust_in_no == cust_in_no, CustHook.typ == u'贷款', CustHook.status == u'正常').first()
            dep = g.db_session.query(CustHook).filter(CustHook.org_no == org_no, CustHook.cust_in_no == cust_in_no, CustHook.typ == u'存款', CustHook.status == u'正常').first()
            if ebk:
                newdata['manager_no'] = ebk.manager_no
                newdata['status'] = u'正常'
                g.db_session.query(CustHook).filter(CustHook.id == pid).update(newdata)

            elif loan:
                newdata['manager_no'] = loan.manager_no
                newdata['status'] = u'正常'
                g.db_session.query(CustHook).filter(CustHook.id == pid).update(newdata)

            elif dep:
                newdata['manager_no'] = dep.manager_no
                newdata['status'] = u'正常'
                g.db_session.query(CustHook).filter(CustHook.id == pid).update(newdata)

            else:
                newdata['manager_no'] = org_no
                newdata['status'] = u'待手工'
                g.db_session.query(CustHook).filter(CustHook.id == pid).update(newdata)
            count = count + 1
        
        print '审批条数：',str(count)
        return u"分配成功!"  

    def distribute(self, **kwargs):
        updatelist = kwargs.get('update_key')
        newdata =  kwargs.get('newdata')
        count = 0

        for pid in updatelist:
            old = g.db_session.query(EbankOrg).filter(EbankOrg.id == pid).first()
            org_no = newdata.get('org_no')
            cust_in_no = old.cust_in_no

            print old.id, org_no, cust_in_no
            """
            依次判断该客户在该网点是否存在电子银行/贷款/存款挂钩关系,按照电子银行/贷款/存款优先级认定该分配记录,若都没有认定关系,则状态变为待手工.
            """
            ebk = g.db_session.query(CustHook).filter(CustHook.org_no == org_no, CustHook.cust_in_no == cust_in_no, CustHook.typ == u'电子银行', CustHook.status == u'正常').first()
            loan = g.db_session.query(CustHook).filter(CustHook.org_no == org_no, CustHook.cust_in_no == cust_in_no, CustHook.typ == u'贷款', CustHook.status == u'正常').first()
            dep = g.db_session.query(CustHook).filter(CustHook.org_no == org_no, CustHook.cust_in_no == cust_in_no, CustHook.typ == u'存款', CustHook.status == u'正常').first()
            data = {}
            if ebk:
                g.db_session.query(EbankOrg).filter(EbankOrg.id == pid).update({'status': u'正常'})
                continue
            elif loan:
                data['manager_no'] = loan.manager_no
                data['status'] = u'正常'
            elif dep:
                data['manager_no'] = dep.manager_no
                data['status'] = u'正常'
            else:
                data['manager_no'] = org_no
                data['status'] = u'待手工'
            count = count + 1

            data['org_no'] = org_no
            data['percentage'] = 100
            data['hook_type'] = u'管户'
            data['start_date'] = old.start_date
            data['end_date'] = old.end_date
            data['etl_date'] = old.etl_date
            data['src'] = old.src
            data['typ'] = old.typ
            data['cust_no'] = old.cust_no
            data['note'] = old.note
            data['sub_typ'] = old.sub_typ
            data['cust_in_no'] = old.cust_in_no
            g.db_session.add(CustHook(**data))

            g.db_session.query(EbankOrg).filter(EbankOrg.id == pid).update({'status': u'正常'})
        
        return u"分配成功!"  
