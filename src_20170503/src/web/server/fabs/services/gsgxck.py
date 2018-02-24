# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
import time
from flask import json, g,current_app
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all

from ..base import utils
from ..model import Branch,Menu,User,UserBranch,AccountHook,CustHookBatch,CustHook
from decimal import Decimal
from ..services.mbox import *


class GsgxckService():
    """ Target Service  """

    def add_save(self, **kwargs):
        drrq = kwargs.get('add_khrq')
        jgbh = kwargs.get('add_jgbh')
        dxbh = kwargs.get('add_zhbh')
        dxxh = kwargs.get('add_zhxh')
        gldxbh = kwargs.get('add_ygh')
        fjdxbh = kwargs.get('add_khh')
        glje1 = kwargs.get('add_gsbl')
        glrq1 = kwargs.get('add_glqsrq')
        glrq2 = kwargs.get('add_gljsrq')
        dxmc = kwargs.get('add_khmc')
        ck_type = kwargs.get('add_cklx')
        newflag = 0
        g.db_session.add(Gsgx_ck(drrq=drrq,jgbh=jgbh,dxbh=dxbh,dxxh=dxxh,gldxbh=gldxbh,fjdxbh=fjdxbh,glje1=glje1,glrq1=glrq1,glrq2=glrq2,dxmc=dxmc,ck_type=ck_type,newflag=newflag))
        return u"保存成功"

    def save(self,**kwargs):
        self.ckyy = ['drrq','jgbh','dxbh','dxxh','gldxbh','fjdxbh','glje1','glrq1','glrq2','dxmc','ck_type','newflag']
        newdata =  kwargs.get('newdata')
        data ={}
        for k,v in newdata.items():
            if k in self.ckyy : data[k] = v
        g.db_session.add(Gsgx_ck(**data))
        return u"ok" 

    def update(self,**kwargs):
        self.ckyy = ['drrq','jgbh','dxbh','dxxh','gldxbh','fjdxbh','glje1','glrq1','glrq2','dxmc','ck_type','newflag','para_id']
        newdata =  kwargs.get('newdata')
        pid = newdata.get('para_id')
        newdata.pop('para_id');
        data ={}
        #for k,v in newdata.items():
        #    if k in self.ckyy : data[k] = v
        g.db_session.query(Gsgx_ck).filter(Gsgx_ck.para_id == pid).update(newdata)
        return u"ok"  
    
    def account_move(self, **kwargs):
        move_id = kwargs.get('move_id')
        org_no = kwargs.get('move_org_no')
        manager_no = kwargs.get('move_manager_no')
        start_date = kwargs.get('move_start_date')
        end_date = kwargs.get('move_end_date')
        percentage = kwargs.get('move_percentage')
        status = '待审批'

        #进行比例的处理 日期待处理 TBD
        old_data = g.db_session.query(AccountHook).filter(AccountHook.id == move_id).first()
        e_start_date = start_date[0:4] + start_date[5:7] + start_date[8:10]
        e_end_date = end_date[0:4] + end_date[5:7] + end_date[8:10]
        g.db_session.add(AccountHook(org_no=org_no,manager_no=manager_no,start_date=int(e_start_date),end_date=int(e_end_date),percentage=percentage,hook_type=old_data.hook_type,status=status,src=old_data.src,typ=old_data.typ,note=old_data.note,account_no=old_data.account_no,etl_date=old_data.etl_date))
        g.db_session.query(AccountHook).filter(AccountHook.id == move_id).delete()
        return u"操作成功"

    def get_top(self, **kwargs):
        id = kwargs.get('id')
        if id:
            top = g.db_session.query(AccountHook).filter(AccountHook.id == id).all()
        return top

    def get_top_cust(self, **kwargs):
        id = kwargs.get('id')
        if id:
            top = g.db_session.query(CustHook).filter(CustHook.id == id).all()
        return top

    """
    same type
    """
    def batch_account_move_before2(self, **kwargs):
        updatelist = kwargs.get('update_key')

        for pid  in updatelist:
            old_data  = g.db_session.query(AccountHook).filter(AccountHook.id == pid).first()
            datadict = {}
            status = u'预提交审批'
            datadict['status'] = status
            g.db_session.query(AccountHook).filter(AccountHook.id == pid).update(datadict)

        return u'预提交成功'

    def batch_account_move_before(self, **kwargs):
        updatelist = kwargs.get('update_key')
        g.db_session.query(AccountHook).filter(AccountHook.id.in_(updatelist)).update({'status':u'预提交审批'}, synchronize_session=False)
        return u'预提交成功'

    """
        账号全部预提交
    """
    def batch_account_move_before_all(self, **kwargs):
        query_params = kwargs.get('query_params')

        print type(query_params), query_params
        ahs_sql = g.db_session.query(AccountHook)
        count = 0
        for k,v in query_params.items():
            count = count + 1
            print v 
            if not v:
                query_params.pop(k)

            if k == u'note':
                query_params.pop(k)
                ahs_sql = ahs_sql.filter(AccountHook.note.like('%'+v+'%'))

        ahs_sql.filter_by(**query_params).update({'status': u'预提交审批'})
        print count
        return u'预提交成功'

    def batch_account_move_delete2(self, **kwargs):
        updatelist = kwargs.get('update_key')

        for pid  in updatelist:
            old_data  = g.db_session.query(AccountHook).filter(AccountHook.id == pid).first()
            datadict = {}
            status = u'正常'
            datadict['status'] = status
            g.db_session.query(AccountHook).filter(AccountHook.id == pid).update(datadict)

        return u'撤销成功'
    def batch_account_move_delete(self, **kwargs):
        updatelist = kwargs.get('update_key')
        g.db_session.query(AccountHook).filter(AccountHook.id.in_(updatelist)).update({'status':u'正常'}, synchronize_session=False)
        return u'撤销成功'

    """
        账号全部预提交删除
    """
    def batch_account_move_all_delete(self, **kwargs):
        query_params = kwargs.get('query_params')

        print type(query_params), query_params
        ahs_sql = g.db_session.query(AccountHook)
        count = 0
        for k,v in query_params.items():
            count = count + 1
            print v 
            if not v:
                query_params.pop(k)

            if k == u'note':
                query_params.pop(k)
                ahs_sql = ahs_sql.filter(AccountHook.note.like('%'+v+'%'))

        ahs_sql.filter_by(**query_params).update({'status': u'正常'})
        print count
        return u'撤销成功'

    def batch_account_move(self, **kwargs):
        updatelist = kwargs.get('update_key')
        note = kwargs.get('note')
        from_teller_no = kwargs.get('from_teller_no')
        to_teller_no = kwargs.get('to_teller_no')
        typ = kwargs.get('typ')
        str_amount = kwargs.get('amount')
        if str_amount is not None:
            amt = str_amount.replace(',', '')
        else:
            amt = 0

        count = 0
        sum = 0
        
        amount = int(Decimal(str(amt)).quantize(Decimal("0.00")) * 100)

        if from_teller_no == to_teller_no:
            raise Exception(u'接收柜员和转出柜员一样!')

        to_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(to_teller_no)).fetchone()
        from_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(from_teller_no)).fetchone()
        cust_hook_batch = CustHookBatch(from_branch_no=from_teller_branch[0],to_branch_no=to_teller_branch[0],from_teller_no=from_teller_no, to_teller_no = to_teller_no, total_count=count, total_amount=amount, typ=typ, note=note, hook_typ=u'账号', deal_status = u'待审批', start_date = int(time.strftime("20%y%m%d")))
        g.db_session.add(cust_hook_batch)
        g.db_session.flush()

        #取接收人的岗位类型
        to_teller = g.db_session.execute("select gr.group_name from f_user fu, user_group ug, group gr where ug.user_id = fu.role_id and ug.group_id = gr.id and gr.group_type_code = '2000' and fu.user_name = '%s'"%(to_teller_no)).fetchone()
        to_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(to_teller_no)).fetchone()

        for pid  in updatelist:
            old_data  = g.db_session.query(AccountHook).filter(AccountHook.id == pid).first()
            if to_teller_branch[0] != old_data.org_no:
                raise Exception(u'不允许跨网点转移')
            if (to_teller[0] == u'客户经理' or to_teller[0] == u'外聘客户经理') and to_teller_branch[0] != old_data.org_no:
                raise Exception(u'客户经理不允许跨网点转移')

            """
            更改为一次更新
            datadict = {}
            status = u'待审批'
            datadict['status'] = status
            datadict['batch_id'] = cust_hook_batch.id
            g.db_session.query(AccountHook).filter(AccountHook.id == pid).update(datadict)
            """

            count = count + 1
            typ = old_data.typ

        g.db_session.query(AccountHook).filter(AccountHook.id.in_(updatelist)).update({'status':u'待审批', 'batch_id': cust_hook_batch.id}, synchronize_session=False)
        cust_hook_batch.total_count = count

        return u'移交成功'

    """
        全部移交按钮
    """
    def batch_account_move_all(self, **kwargs):
        note = kwargs.get('note')
        from_teller_no = kwargs.get('from_teller_no')
        to_teller_no = kwargs.get('to_teller_no')
        str_amount = kwargs.get('amount')

        query_params = kwargs.get('query_params')

        print type(query_params), query_params
        ahs_sql = g.db_session.query(AccountHook)
        for k,v in query_params.items():
            count = count + 1
            print v 
            if not v:
                query_params.pop(k)

            if k == u'note':
                query_params.pop(k)
                ahs_sql = ahs_sql.filter(AccountHook.note.like('%'+v+'%'))

        old_datas = ahs_sql.filter_by(**query_params).all()

        if str_amount is not None:
            amt = str_amount.replace(',', '')
        else:
            amt = 0

        count = 0
        amount = int(Decimal(str(amt)).quantize(Decimal("0.00")) * 100)
        if from_teller_no == to_teller_no:
            raise Exception(u'接收柜员和转出柜员一样!')

        to_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(to_teller_no)).fetchone()
        from_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(from_teller_no)).fetchone()
        cust_hook_batch = CustHookBatch(from_branch_no=from_teller_branch[0],to_branch_no=to_teller_branch[0],from_teller_no=from_teller_no, to_teller_no = to_teller_no, total_count=count, total_amount=amount, typ=typ, note=note, hook_typ=u'账号', deal_status = u'待审批', start_date=int(time.strftime("20%y%m%d")))
        g.db_session.add(cust_hook_batch)
        g.db_session.flush()

        #取接收人的岗位类型
        to_teller = g.db_session.execute("select gr.group_name from f_user fu, user_group ug, group gr where ug.user_id = fu.role_id and ug.group_id = gr.id and gr.group_type_code = '2000' and fu.user_name = '%s'"%(to_teller_no)).fetchone()
        to_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(to_teller_no)).fetchone()

        for old_data in old_datas:
            if to_teller_branch[0] != old_data.org_no:
                raise Exception(u'不允许跨网点转移')
            if (to_teller[0] == u'客户经理' or to_teller[0] == u'外聘客户经理') and to_teller_branch[0] != old_data.org_no:
                raise Exception(u'客户经理不允许跨网点转移')

            count = count + 1

        ahs_sql.filter_by(**query_params).update({'status': u'待审批', 'batch_id':cust_hook_batch.id})
        cust_hook_batch.total_count = count

        return u'移交成功'

    """
    审批--包括账号转移审批和客户转移审批
    """
    def batch_account_move_check(self, **kwargs):
        l = []
        per = 0
        updatelist = kwargs.get('update_key')
        reason = kwargs.get('reason')
        deal_status = kwargs.get('deal_status')

        print updatelist
        slist = updatelist
        if deal_status == u'同意':
            g.db_session.query(CustHookBatch).filter(CustHookBatch.id.in_(slist)).update({'deal_status':u'同意','status':u'正常', 'check_date':int(time.strftime("20%y%m%d"))}, synchronize_session=False)
            g.db_session.query(CustHook).filter(CustHook.batch_id.in_(slist)).update({'etl_date': int(time.strftime("20%y%m%d")), 'status': u'已审批'}, synchronize_session=False)
            g.db_session.query(AccountHook).filter(AccountHook.batch_id.in_(slist)).update({'etl_date': int(time.strftime("20%y%m%d")), 'status': u'已审批'} ,synchronize_session=False)  #下月生效
        else:
            g.db_session.query(AccountHook).filter(AccountHook.batch_id.in_(slist)).update({'status':u'正常'}, synchronize_session=False)
            g.db_session.query(CustHookBatch).filter(CustHookBatch.id.in_(slist)).update({'deal_status':u'不同意','status':u'正常', 'check_date':int(time.strftime("20%y%m%d"))}, synchronize_session=False)
            g.db_session.query(CustHook).filter(CustHook.batch_id.in_(slist)).update({'status':u'正常'}, synchronize_session=False)

        #每一批次发送信息
        """
        mbox = MboxService()
        title = u"批次号:" + str(slist) + u"审批结果:" + deal_status
        body = u"批次号:" + str(slist) + u"审批结果:" + deal_status
        mbox.mbox_send2(c.from_teller_no, c.to_teller_no, title, body)
        mbox.mbox_send2(c.to_teller_no, c.from_teller_no, title, body)
        """

        return u'审批成功'

    """
    审批--包括账号转移审批和客户转移审批
    """
    def batch_account_move_check2(self, **kwargs):
        l = []
        per = 0
        updatelist = kwargs.get('update_key')
        reason = kwargs.get('reason')
        deal_status = kwargs.get('deal_status')

        for pid  in updatelist:
            c = g.db_session.query(CustHookBatch).filter(CustHookBatch.id == pid).first()
            if c.hook_typ == u'账号':
                if deal_status == u'同意':
                    g.db_session.query(CustHookBatch).filter(CustHookBatch.id == pid).update({'deal_status':u'同意','status':u'正常', 'check_date':int(time.strftime("20%y%m%d"))})
                    g.db_session.query(AccountHook).filter(AccountHook.batch_id==pid).update({'etl_date': int(time.strftime("20%y%m%d")), 'status': u'已审批'})  #下月生效
                else:
                    g.db_session.query(AccountHook).filter(AccountHook.batch_id == pid).update({'status':u'正常', 'check_date':int(time.strftime("20%y%m%d"))})
                    g.db_session.query(CustHookBatch).filter(CustHookBatch.id == pid).update({'deal_status':u'不同意','status':u'正常'})
            elif c.hook_typ == u'客户号':
                a = g.db_session.query(CustHook).filter(CustHook.batch_id==pid).all()
                if deal_status == u'同意':
                    for aa in a:
                        g.db_session.query(AccountHook).filter(AccountHook.batch_id == pid).update({'etl_date': int(time.strftime("20%y%m%d")), 'status': u'已审批'})
                    g.db_session.query(CustHookBatch).filter(CustHookBatch.id == pid).update({'deal_status':u'同意','status':u'正常', 'check_date':int(time.strftime("20%y%m%d"))})
                    g.db_session.query(CustHook).filter(CustHook.batch_id == pid).update({'etl_date': int(time.strftime("20%y%m%d")), 'status': u'已审批'})
                else:
                    for aa in a:
                        g.db_session.query(AccountHook).filter(AccountHook.batch_id == pid).update({'status': u'正常'})
                    g.db_session.query(CustHook).filter(CustHook.batch_id == pid).update({'status':u'正常'})
                    g.db_session.query(CustHookBatch).filter(CustHookBatch.id == pid).update({'deal_status':u'不同意','status':u'正常', 'check_date':int(time.strftime("20%y%m%d"))})
            elif c.hook_typ == u'全部移交':
                if deal_status == u'同意':
                    g.db_session.query(CustHookBatch).filter(CustHookBatch.id == pid).update({'deal_status':u'同意','status':u'正常', 'check_date':int(time.strftime("20%y%m%d"))})
                    g.db_session.query(CustHook).filter(CustHook.batch_id == pid).update({'etl_date': int(time.strftime("20%y%m%d")), 'status': u'已审批'})
                    g.db_session.query(AccountHook).filter(AccountHook.batch_id==pid).update({'etl_date': int(time.strftime("20%y%m%d")), 'status': u'已审批'})  #下月生效
                else:
                    g.db_session.query(AccountHook).filter(AccountHook.batch_id == pid).update({'status':u'正常'})
                    g.db_session.query(CustHookBatch).filter(CustHookBatch.id == pid).update({'deal_status':u'不同意','status':u'正常', 'check_date':int(time.strftime("20%y%m%d"))})
                    g.db_session.query(CustHook).filter(CustHook.batch_id == pid).update({'status':u'正常'})
            else:
                raise Exception(u'挂钩关系错误')

            #每一批次发送信息
            mbox = MboxService()
            title = u"批次号:" + str(c.id) + u"审批结果:" + deal_status
            body = u"批次号:" + str(c.id) + u"业务种类:"+ c.hook_typ + u"转移到员工:" +c.to_teller_no + u",审批结果:" + deal_status
            mbox.mbox_send2(c.from_teller_no, c.to_teller_no, title, body)
            mbox.mbox_send2(c.to_teller_no, c.from_teller_no, title, body)

        return u'审批成功'

    def batch_account_move_sum_with_hook(self, **kwargs):
        updatelist = kwargs.get('update_key')
        typ = kwargs.get('typ')
        follow_cust = kwargs.get('follow_cust')
        query_date = kwargs.get('query_date')
        org_no = kwargs.get('org_no')

        total_sum = 0
        total_exist_avg_amount = 0 
        total_balance = 0
        total_add_avg_amount = 0

        hook_ids = ""
        for pid  in updatelist:
            hook_id = str(pid) + ","
            hook_ids =  hook_ids + hook_id 
            total_sum = total_sum + 1

        hook_ids = hook_ids[:-1]
        hook_ids = hook_ids.split(',')
        print hook_ids

        org_temp = ""
        staff_temp = ""
        if follow_cust == u'账号优先':
            account_hooks = g.db_session.query(AccountHook).filter(AccountHook.id.in_(hook_ids)).all()
            for a in account_hooks:
                if a.exist_avg_balance is not None:
                    total_exist_avg_amount = total_exist_avg_amount + int(a.exist_avg_balance)
                if a.balance is not None:
                    total_balance = total_balance + int(a.balance)
                if a.add_avg_balance is not None:
                    total_add_avg_amount = total_add_avg_amount + int(a.add_avg_balance)

                if staff_temp == "":
                    staff_temp = a.manager_no
                else:
                    if staff_temp != a.manager_no:
                        raise Exception(u'不允许同时转移多于1个员工业绩')

                if org_temp == "":
                    org_temp = a.org_no
                else:
                    if org_temp != a.org_no:
                        raise Exception(u'不允许同时转移多于1个机构业绩')

        elif follow_cust == u'客户号优先':
            cust_hooks = g.db_session.query(CustHook).filter(CustHook.id.in_(hook_ids)).all()
            for c in cust_hooks:
                if c.exist_avg_balance is not None:
                    total_exist_avg_amount = total_exist_avg_amount + int(c.exist_avg_balance)
                if c.balance is not None:
                    total_balance = total_balance + int(c.balance)
                if c.add_avg_balance is not None:
                    total_add_avg_amount = total_add_avg_amount + int(c.add_avg_balance)

                if staff_temp == "":
                    staff_temp = c.manager_no
                else:
                    if staff_temp != c.manager_no:
                        raise Exception(u'不允许同时转移多于1个员工业绩')
                if org_temp == "":
                    org_temp = c.org_no
                else:
                    if org_temp != c.org_no:
                        raise Exception(u'不允许同时转移多于1个机构业绩')
        else:
            raise Exception(u'错误的优先级别类型')

        total_exist_avg_amount1 = '{:,}'.format(Decimal(total_exist_avg_amount).quantize(Decimal("0.00"))/100)
        total_balance1 = '{:,}'.format(Decimal(total_balance).quantize(Decimal("0.00"))/100)
        total_add_avg_amount1 = '{:,}'.format(Decimal(total_add_avg_amount).quantize(Decimal("0.00"))/100)
        return {'total_sum':total_sum, 'total_balance':total_balance1, 'total_add_avg_amount':total_add_avg_amount1, 'total_exist_avg_amount':total_exist_avg_amount1,'staff':staff_temp}

    """
    全部移交按钮计算
    """
    def batch_account_move_sum_with_hook_all(self, **kwargs):
        typ = kwargs.get('typ')
        follow_cust = kwargs.get('follow_cust')
        query_date = kwargs.get('query_date')
        org_no = kwargs.get('org_no')
        query_params = kwargs.get('query_params')

        print type(query_params), query_params

        org_temp = ""
        staff_temp = ""
        total_sum = 0
        total_exist_avg_amount = 0 
        total_balance = 0
        total_add_avg_amount = 0
        if follow_cust == u'账号优先':
            ahs_sql = g.db_session.query(AccountHook)
            for k,v in query_params.items():
                if not v:
                    query_params.pop(k)
                if k == u'note':
                    query_params.pop(k)
                    ahs_sql = ahs_sql.filter(AccountHook.note.like('%'+v+'%'))
            ahs = ahs_sql.filter_by(**query_params).all()

            for a in ahs:
                if a.exist_avg_balance is not None:
                    total_exist_avg_amount = total_exist_avg_amount + int(a.exist_avg_balance)
                if a.balance is not None:
                    total_balance = total_balance + int(a.balance)
                if a.add_avg_balance is not None:
                    total_add_avg_amount = total_add_avg_amount + int(a.add_avg_balance)

                if staff_temp == "":
                    staff_temp = a.manager_no
                else:
                    if staff_temp != a.manager_no:
                        raise Exception(u'不允许同时转移多于1个员工业绩')
                if org_temp == "":
                    org_temp = a.org_no
                else:
                    if org_temp != a.org_no:
                        raise Exception(u'不允许同时转移多于1个机构业绩')
        elif follow_cust == u'客户号优先':
            ahs_sql = g.db_session.query(CustHook)
            for k,v in query_params.items():
                if not v:
                    query_params.pop(k)
                if k == u'note':
                    query_params.pop(k)
                    ahs_sql = ahs_sql.filter(CustHook.note.like('%'+v+'%'))
            ahs = ahs_sql.filter_by(**query_params).all()

            for c in ahs:
                if c.exist_avg_balance is not None:
                    total_exist_avg_amount = total_exist_avg_amount + int(c.exist_avg_balance)
                if c.balance is not None:
                    total_balance = total_balance + int(c.balance)
                if c.add_avg_balance is not None:
                    total_add_avg_amount = total_add_avg_amount + int(c.add_avg_balance)

                if staff_temp == "":
                    staff_temp = c.manager_no
                else:
                    if staff_temp != c.manager_no:
                        raise Exception(u'不允许同时转移多于1个员工业绩')
                if org_temp == "":
                    org_temp = c.org_no
                else:
                    if org_temp != c.org_no:
                        raise Exception(u'不允许同时转移多于1个机构业绩')
        else:
            raise Exception(u'错误的优先级别类型')

        print count
        total_exist_avg_amount1 = '{:,}'.format(Decimal(total_exist_avg_amount).quantize(Decimal("0.00"))/100)
        total_balance1 = '{:,}'.format(Decimal(total_balance).quantize(Decimal("0.00"))/100)
        total_add_avg_amount1 = '{:,}'.format(Decimal(total_add_avg_amount).quantize(Decimal("0.00"))/100)
        return {'total_sum':total_sum, 'total_balance':total_balance1, 'total_add_avg_amount':total_add_avg_amount1, 'total_exist_avg_amount':total_exist_avg_amount1,'staff':staff_temp}

    def batch_account_move_sum_with_hook2(self, **kwargs):
        """
        通过F_BALANCE汇总存款、理财、贷款的存量日均、当前日均和余额字段
        暂时只支持所有typ均为一种业务类型
        如果是汇总客户经理所有,请不要使用
        """
        updatelist = kwargs.get('update_key')
        #stafflist = kwargs.get('staff_no')
        typ = kwargs.get('typ')
        follow_cust = kwargs.get('follow_cust')
        query_date = kwargs.get('query_date')
        org_no = kwargs.get('org_no')
        print typ, query_date,follow_cust,org_no
        
        acct_hook_ids = ""
        total_sum = 0
        for pid  in updatelist:
            hook_id = str(pid) + ","
            acct_hook_ids =  acct_hook_ids + hook_id 
            total_sum = total_sum + 1

        acct_hook_ids = acct_hook_ids[:-1]
        print acct_hook_ids
        if typ == u'存款' and follow_cust == u'账号优先':
            amounts = g.db_session.execute("select nvl(sum(f1.YEAR_PDT/100)/ dd.YEAR_DAYS,0),nvl(sum(f.BALANCE/100),0),nvl(sum(f.YEAR_PDT/100)/ d.BEG_YEAR_DAYS,0) from F_BALANCE f join D_DATE d on f.DATE_ID=d.ID left join F_BALANCE f1 on f1.DATE_ID=d.L_YEAREND_ID and f1.ACCT_TYPE=1 and f1.ACCOUNT_ID=f.ACCOUNT_ID join D_ACCOUNT a on f.ACCOUNT_ID=a.ID join account_hook ah on a.account_no = ah.account_no and ah.id in (%s) join D_DATE dd on dd.ID=d.L_YEAREND_ID where f.DATE_ID='%s' and f.ACCT_TYPE=1 group by dd.YEAR_DAYS,d.BEG_YEAR_DAYS"%(acct_hook_ids, query_date)).fetchone()
        elif typ == u'存款' and follow_cust == u'客户号优先':
            amounts = g.db_session.execute("select nvl(sum(f1.YEAR_PDT/100)/ dd.YEAR_DAYS,0),nvl(sum(f.BALANCE/100),0),nvl(sum(f.YEAR_PDT/100)/ d.BEG_YEAR_DAYS,0) from F_BALANCE f \
                            join D_DATE d on f.DATE_ID=d.ID left  \
                            join F_BALANCE f1 on f1.DATE_ID=d.L_YEAREND_ID  and f1.ACCT_TYPE=1 and f1.ACCOUNT_ID=f.ACCOUNT_ID  \
                            join D_ACCOUNT a on f.ACCOUNT_ID=a.ID   \
                            join account_hook ah on ah.account_no = a.account_no  and ah.FOLLOW_CUST = '客户号优先' \
                            join cust_hook ch on ah.cust_in_no = ch.cust_in_no and ah.ORG_NO = ch.ORG_NO and ch.id in (%s) \
                            join D_DATE dd on dd.ID=d.L_YEAREND_ID where f.DATE_ID='%s' and f.ACCT_TYPE=1 group by dd.YEAR_DAYS,d.BEG_YEAR_DAYS"%(acct_hook_ids, query_date)).fetchone()
        elif typ == u'贷款' and follow_cust == u'客户号优先':
            amounts = g.db_session.execute("select nvl(sum(f1.YEAR_PDT/100)/ dd.YEAR_DAYS,0),nvl(sum(f.BALANCE/100),0),nvl(sum(f.YEAR_PDT/100)/ d.BEG_YEAR_DAYS,0) from F_BALANCE f \
            join D_DATE d on f.DATE_ID=d.ID \
            left join F_BALANCE f1 on f1.DATE_ID=d.L_YEAREND_ID and f1.ACCT_TYPE=4 and f1.ACCOUNT_ID=f.ACCOUNT_ID \
            join D_ORG o on f.ORG_ID=o.ID and o.ORG0_CODE='%s' \
            join D_DATE dd on dd.ID=d.L_YEAREND_ID  \
            join cust_hook ch on ch.CUST_IN_NO = f.cst_no and ch.id in (%s) \
            where f.DATE_ID='%s'  and  f.ACCT_TYPE=4 \
            group by dd.YEAR_DAYS,d.BEG_YEAR_DAYS"%(org_no, acct_hook_ids, query_date)).fetchone()
        elif typ == u'理财' and follow_cust == u'账号优先':
            amounts = g.db_session.execute("select nvl(sum(f1.YEAR_PDT/100)/ dd.YEAR_DAYS,0),nvl(sum(case when a.CLOSE_DATE_ID>f.DATE_ID then f.BALANCE/100 else 0 end),0),nvl(sum(f.YEAR_PDT/100)/ d.BEG_YEAR_DAYS,0) from F_BALANCE f \
            join D_DATE d on f.DATE_ID=d.ID \
            left join F_BALANCE f1 on f1.DATE_ID=d.L_YEAREND_ID and f1.ACCT_TYPE=8 and f1.ACCOUNT_ID=f.ACCOUNT_ID \
            join D_ACCOUNT a on f.ACCOUNT_ID=a.ID \
            join ACCOUNT_HOOK ah on ah.ACCOUNT_NO = a.ACCOUNT_NO and ah.id in (%s) \
            join D_DATE dd on dd.ID=d.L_YEAREND_ID \
            where f.DATE_ID='%s' and f.ACCT_TYPE=8 \
            group by dd.YEAR_DAYS,d.BEG_YEAR_DAYS"%(acct_hook_ids, query_date)).fetchone()
        elif typ == u'理财' and follow_cust == u'客户号优先':
            amounts = g.db_session.execute("select nvl(sum(f1.YEAR_PDT/100)/ dd.YEAR_DAYS,0),nvl(sum(case when a.CLOSE_DATE_ID>f.DATE_ID then f.BALANCE/100 else 0 end),0),nvl(sum(f.YEAR_PDT/100)/ d.BEG_YEAR_DAYS,0) from F_BALANCE f \
            join D_DATE d on f.DATE_ID=d.ID \
            left join F_BALANCE f1 on f1.DATE_ID=d.L_YEAREND_ID and f1.ACCT_TYPE=8 and f1.ACCOUNT_ID=f.ACCOUNT_ID \
            join D_ACCOUNT a on f.ACCOUNT_ID=a.ID   \
            join ACCOUNT_HOOK ah on ah.ACCOUNT_NO = a.ACCOUNT_NO  and ah.FOLLOW_CUST = '客户号优先'\
            join CUST_HOOK ch on ch.CUST_IN_NO = ah.CUST_IN_NO and ah.ORG_NO = ch.ORG_NO and ch.id in (%s) \
            join D_DATE dd on dd.ID=d.L_YEAREND_ID  \
            where f.DATE_ID='%s' and f.ACCT_TYPE=8 \
            group by dd.YEAR_DAYS,d.BEG_YEAR_DAYS"%(acct_hook_ids, query_date)).fetchone()
        else:
            raise Exception(u'暂不支持的挂钩汇总类型')
        print amounts,'<<<<<<<<<<'
        if amounts is None:
            total_exist_avg_amount = '0.0'
            total_balance = '0.0'
            total_add_avg_amount = '0.0'
        else:
            total_exist_avg_amount = '{:,}'.format(Decimal(int(amounts[0])).quantize(Decimal("0.00")))
            total_balance = '{:,}'.format(Decimal(int(amounts[1])).quantize(Decimal("0.00")))
            total_add_avg_amount = '{:,}'.format(Decimal(int(amounts[2])).quantize(Decimal("0.00")))
        print total_exist_avg_amount, total_balance, total_add_avg_amount
        return {'total_sum':total_sum, 'total_balance':total_balance, 'total_add_avg_amount':total_add_avg_amount, 'total_exist_avg_amount':total_exist_avg_amount}

    """
    客户号移交审批部分
    """
    def batch_cust_move_before(self, **kwargs):
        updatelist = kwargs.get('update_key')

        for pid  in updatelist:
            old_data  = g.db_session.query(CustHook).filter(CustHook.id == pid).first()
            datadict = {}
            status = u'预提交审批'
            datadict['status'] = status
            g.db_session.query(CustHook).filter(CustHook.id == pid).update(datadict)
            if old_data.typ == u'电子银行':
                g.db_session.query(CustHook).filter(CustHook.cust_in_no == old_data.cust_in_no,CustHook.org_no == old_data.org_no, CustHook.typ == u'电子银行',CustHook.manager_no==old_data.manager_no).update(datadict)

        return u'预提交成功'

    """
    客户号移交审批部分2
    """
    def batch_cust_move_before2(self, **kwargs):
        updatelist = kwargs.get('update_key')
        g.db_session.query(CustHook).filter(CustHook.id.in_(updatelist)).update({'status':u'预提交审批'}, synchronize_session=False)

        #电子银行如何特殊处理 TBD

        """
        old_data  = g.db_session.query(CustHook).filter(CustHook.id == pid).first()

        for pid  in updatelist:
            datadict = {}
            status = u'预提交审批'
            datadict['status'] = status
            g.db_session.query(CustHook).filter(CustHook.id == pid).update(datadict)
            if old_data.typ == u'电子银行':
                g.db_session.query(CustHook).filter(CustHook.cust_in_no == old_data.cust_in_no,CustHook.org_no == old_data.org_no, CustHook.typ == u'电子银行').update(datadict)
         """

        return u'预提交成功'

    """
        客户全部预提交
    """
    def batch_cust_move_before_all(self, **kwargs):
        query_params = kwargs.get('query_params')

        print type(query_params), query_params
        ahs_sql = g.db_session.query(CustHook)
        count = 0
        for k,v in query_params.items():
            count = count + 1
            print v 
            if not v:
                query_params.pop(k)

            if k == u'note':
                query_params.pop(k)
                ahs_sql = ahs_sql.filter(CustHook.note.like('%'+v+'%'))

        ahs_sql.filter_by(**query_params).update({'status': u'预提交审批'})
        print count
        return u'预提交成功'


    def batch_cust_move_delete(self, **kwargs):
        updatelist = kwargs.get('update_key')

        for pid in updatelist:
            old_data  = g.db_session.query(CustHook).filter(CustHook.id == pid).first()
            datadict = {}
            status = u'正常'
            datadict['status'] = status
            g.db_session.query(CustHook).filter(CustHook.id == pid).update(datadict)
            if old_data.typ == u'电子银行':
                g.db_session.query(CustHook).filter(CustHook.cust_in_no == old_data.cust_in_no,CustHook.org_no == old_data.org_no,CustHook.manager_no==old_data.manager_no).update(datadict)

        return u'撤销成功'

    def batch_cust_move_delete2(self, **kwargs):
        updatelist = kwargs.get('update_key')
        g.db_session.query(CustHook).filter(CustHook.id.in_(updatelist)).update({'status':u'正常'}, synchronize_session=False)
        return u'撤销成功'

    """
        客户全部预提交删除
    """
    def batch_cust_move_before_all_delete(self, **kwargs):
        query_params = kwargs.get('query_params')

        print type(query_params), query_params
        ahs_sql = g.db_session.query(CustHook)
        for k,v in query_params.items():
            print v 
            print k == u'note'
            if not v:
                query_params.pop(k)

            if k == u'note':
                query_params.pop(k)
                ahs_sql = ahs_sql.filter(CustHook.note.like('%'+v+'%'))

        ahs_sql.filter_by(**query_params).update({'status': u'正常'})
        return u'撤销成功'



    def batch_cust_move(self, **kwargs):
        updatelist = kwargs.get('update_key')
        note = kwargs.get('note')
        from_teller_no = kwargs.get('from_teller_no')
        to_teller_no = kwargs.get('to_teller_no')
        typ = kwargs.get('typ')

        str_amount = kwargs.get('amount')
        if str_amount is not None:
            amt = str_amount.replace(',', '')
        else:
            amt = 0

        if from_teller_no == to_teller_no:
            raise Exception(u'接收柜员和转出柜员一样!')

        count = 0
        sum = 0
        amount = int(Decimal(str(amt)).quantize(Decimal("0.00")) * 100)
        to_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(to_teller_no)).fetchone()
        from_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(from_teller_no)).fetchone()
        cust_hook_batch = CustHookBatch(from_branch_no=from_teller_branch[0],to_branch_no=to_teller_branch[0],from_teller_no=from_teller_no, to_teller_no = to_teller_no, total_count=count, total_amount=amount, typ=typ, note=note, hook_typ=u'客户号', deal_status = u'待审批', start_date = int(time.strftime("20%y%m%d")))
        g.db_session.add(cust_hook_batch)
        g.db_session.flush()
        #取接收人的岗位类型
        to_teller = g.db_session.execute("select gr.group_name from f_user fu, user_group ug, group gr where ug.user_id = fu.role_id and ug.group_id = gr.id and gr.group_type_code = '2000' and fu.user_name = '%s'"%(to_teller_no)).fetchone()

        account_hooks_id = set()
        ebank_cust_hooks_id = set()
        for pid  in updatelist:
            old_data  = g.db_session.query(CustHook).filter(CustHook.id == pid).first()
            if to_teller_branch[0] != old_data.org_no:
                raise Exception(u'业绩不允许跨网点转移')
            if (to_teller[0] == u'客户经理' or to_teller[0] == u'外聘客户经理') and to_teller_branch[0] != old_data.org_no:
                raise Exception(u'客户经理不允许跨网点转移')
            """
            更改为一次提交
            datadict = {}
            status = u'待审批'
            datadict['status'] = status
            datadict['batch_id'] = cust_hook_batch.id
            g.db_session.query(CustHook).filter(CustHook.id == pid).update(datadict)
            g.db_session.query(AccountHook).filter(AccountHook.manager_no == old_data.manager_no,AccountHook.org_no == old_data.org_no,AccountHook.typ == old_data.typ,AccountHook.follow_cust == u'客户号优先',AccountHook.cust_in_no == old_data.cust_in_no).update(datadict)
            if old_data.typ == u'电子银行':
                g.db_session.query(CustHook).filter(CustHook.cust_in_no == old_data.cust_in_no,CustHook.org_no == old_data.org_no, CustHook.typ == u'电子银行').update(datadict)
            """
            
            accs = g.db_session.query(AccountHook).filter(AccountHook.manager_no == old_data.manager_no,AccountHook.org_no == old_data.org_no,AccountHook.typ == old_data.typ,AccountHook.follow_cust == u'客户号优先',AccountHook.cust_in_no == old_data.cust_in_no).all()
            for acc in accs:
                account_hooks_id.add(acc.id)

            if old_data.typ == u'电子银行':
                ebanks = g.db_session.query(CustHook).filter(CustHook.cust_in_no == old_data.cust_in_no,CustHook.org_no == old_data.org_no, CustHook.typ == u'电子银行',CustHook.manager_no==old_data.manager_no).all()
                for ebank in ebanks:
                    ebank_cust_hooks_id.add(ebank.id)

            count = count + 1
            typ = old_data.typ
        print "batch_cust_move:ebank_cust_hooks_id", ebank_cust_hooks_id
        print "batch_cust_move:account_hooks_id", account_hooks_id
        ebank_cust_hooks_id=list(ebank_cust_hooks_id)
        account_hooks_id=list(account_hooks_id)
        g.db_session.query(CustHook).filter(CustHook.id.in_(updatelist)).update({'status':u'待审批', 'batch_id':cust_hook_batch.id}, synchronize_session=False)
        g.db_session.query(CustHook).filter(CustHook.id.in_(ebank_cust_hooks_id)).update({'status':u'待审批', 'batch_id':cust_hook_batch.id}, synchronize_session=False)
        g.db_session.query(AccountHook).filter(AccountHook.id.in_(account_hooks_id)).update({'status':u'待审批', 'batch_id':cust_hook_batch.id}, synchronize_session=False)
        cust_hook_batch.total_count = count

        return u'移交成功'


    def batch_cust_move2(self, **kwargs):
        updatelist = kwargs.get('update_key')
        note = kwargs.get('note')
        from_teller_no = kwargs.get('from_teller_no')
        to_teller_no = kwargs.get('to_teller_no')
        typ = kwargs.get('typ')

        str_amount = kwargs.get('amount')
        if str_amount is not None:
            amt = str_amount.replace(',', '')
        else:
            amt = 0

        if from_teller_no == to_teller_no:
            raise Exception(u'接收柜员和转出柜员一样!')

        count = 0
        sum = 0
        amount = int(Decimal(str(amt)).quantize(Decimal("0.00")) * 100)
        to_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(to_teller_no)).fetchone()
        from_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(from_teller_no)).fetchone()
        cust_hook_batch = CustHookBatch(from_branch_no=from_teller_branch[0],to_branch_no=to_teller_branch[0],from_teller_no=from_teller_no, to_teller_no = to_teller_no, total_count=count, total_amount=amount, typ=typ, note=note, hook_typ=u'客户号', deal_status = u'待审批', start_date = int(time.strftime("20%y%m%d")))
        g.db_session.add(cust_hook_batch)
        g.db_session.flush()
        #取接收人的岗位类型
        to_teller = g.db_session.execute("select gr.group_name from f_user fu, user_group ug, group gr where ug.user_id = fu.role_id and ug.group_id = gr.id and gr.group_type_code = '2000' and fu.user_name = '%s'"%(to_teller_no)).fetchone()

        account_hooks_id = set()

        old_data=g.db_session.query(CustHook).filter(CustHook.id.in_(updatelist)).filter(CustHook.org_no!=to_teller_branch[0]).first()
        if old_data:
            raise Exception(u'业绩不允许跨网点转移')
        count=len(updatelist)
        print "batch_cust_move:account_hooks_id", account_hooks_id
        updatelist_list=[]
        for i in updatelist:
            updatelist_list.append(int(i))
        updatelist_list=tuple(updatelist_list)
        if len(updatelist_list)==1:
            g.db_session.execute(u"""merge into Account_Hook ac
            using(select manager_no,org_no,typ,cust_in_no from CUST_HOOK where id in (%s))cu
            on (ac.follow_cust = '客户号优先' and ac.manager_no=cu.manager_no and ac.org_no=cu.org_no and ac.typ=cu.typ and ac.cust_in_no=cu.cust_in_no)
            when matched then update set ac.status='待审批',ac.batch_id=%d """%(updatelist_list[0],cust_hook_batch.id))
        else:
             g.db_session.execute(u"""merge into Account_Hook ac
            using(select manager_no,org_no,typ,cust_in_no from CUST_HOOK where id in %s)cu
            on (ac.follow_cust = '客户号优先' and ac.manager_no=cu.manager_no and ac.org_no=cu.org_no and ac.typ=cu.typ and ac.cust_in_no=cu.cust_in_no)
            when matched then update set ac.status='待审批',ac.batch_id=%d """%(updatelist_list,cust_hook_batch.id))
           
        g.db_session.query(CustHook).filter(CustHook.id.in_(updatelist)).update({'status':u'待审批', 'batch_id':cust_hook_batch.id}, synchronize_session=False)
        cust_hook_batch.total_count = count

        return u'移交成功'




    def batch_cust_move_all(self, **kwargs):
        """
        贷款移交的时候同时移交其其它业务
        """
        updatelist = kwargs.get('update_key')
        note = kwargs.get('note')
        from_teller_no = kwargs.get('from_teller_no')
        to_teller_no = kwargs.get('to_teller_no')
        typ = kwargs.get('typ')
        org_no = kwargs.get('org_no')

        if from_teller_no == to_teller_no:
            raise Exception(u'接收柜员和转出柜员一样!')

        count = 0
        sum = 0
        amount = 0
        to_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(to_teller_no)).fetchone()
        from_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(from_teller_no)).fetchone()
        cust_hook_batch = CustHookBatch(from_branch_no=from_teller_branch[0],to_branch_no=to_teller_branch[0],from_teller_no=from_teller_no, to_teller_no = to_teller_no, total_count=count, total_amount=amount, typ=typ, note=note, hook_typ=u'客户号', deal_status = u'待审批', start_date = int(time.strftime("20%y%m%d")))
        g.db_session.add(cust_hook_batch)
        g.db_session.flush()

        #取接收人的岗位类型
        to_teller = g.db_session.execute("select gr.group_name from f_user fu, user_group ug, group gr where ug.user_id = fu.role_id and ug.group_id = gr.id and gr.group_type_code = '2000' and fu.user_name = '%s'"%(to_teller_no)).fetchone()
        account_hooks_id = []
        ebank_cust_hooks_id = []
        for pid  in updatelist:
            old_data  = g.db_session.query(CustHook).filter(CustHook.id == pid).first()
            if to_teller_branch[0] != old_data.org_no:
                raise Exception(u'业绩不允许跨网点转移')

            if old_data.typ == u'贷款' and not (to_teller[0] == u'客户经理' or to_teller[0] == u'外聘客户经理'):
                raise Exception(u'贷款接收人不能是非客户经理')

            if (to_teller[0] == u'客户经理' or to_teller[0] == u'外聘客户经理') and to_teller_branch[0] != old_data.org_no:
                raise Exception(u'客户经理不允许跨网点转移')

            datadict = {}
            templist=g.db_session.query(CustHook).filter(CustHook.manager_no == old_data.manager_no,CustHook.org_no == old_data.org_no,CustHook.cust_in_no == old_data.cust_in_no)
            for tid in templist:
                """ 更改为一次更新
                status = u'待审批'
                datadict['status'] = status
                datadict['batch_id'] = cust_hook_batch.id
                g.db_session.query(CustHook).filter(CustHook.id == tid.id).update(datadict)
                g.db_session.query(AccountHook).filter(AccountHook.manager_no == old_data.manager_no,AccountHook.org_no == old_data.org_no,AccountHook.cust_in_no == old_data.cust_in_no).update(datadict)
                """
                ebank_cust_hooks_id.append(tid.id)
                count = count + 1

            accs = g.db_session.query(AccountHook).filter(AccountHook.manager_no == old_data.manager_no,AccountHook.org_no == old_data.org_no,AccountHook.cust_in_no == old_data.cust_in_no).all()
            for acc in accs:
                account_hooks_id.append(acc.id)
            typ = old_data.typ

        print "batch_cust_move:ebank_cust_hooks_id", ebank_cust_hooks_id
        print "batch_cust_move:account_hooks_id", account_hooks_id
        g.db_session.query(CustHook).filter(CustHook.id.in_(updatelist)).update({'status':u'待审批', 'batch_id':cust_hook_batch.id}, synchronize_session=False)
        g.db_session.query(CustHook).filter(CustHook.id.in_(ebank_cust_hooks_id)).update({'status':u'待审批', 'batch_id':cust_hook_batch.id}, synchronize_session=False)
        g.db_session.query(AccountHook).filter(AccountHook.id.in_(account_hooks_id)).update({'status':u'待审批', 'batch_id':cust_hook_batch.id}, synchronize_session=False)
        cust_hook_batch.total_count = count

        return u'移交成功'


    def batch_cust_move_all2(self, **kwargs):
        """
        贷款移交的时候同时移交其其它业务
        """
        updatelist = kwargs.get('update_key')
        note = kwargs.get('note')
        from_teller_no = kwargs.get('from_teller_no')
        to_teller_no = kwargs.get('to_teller_no')
        typ = kwargs.get('typ')
        org_no = kwargs.get('org_no')

        if from_teller_no == to_teller_no:
            raise Exception(u'接收柜员和转出柜员一样!')

        count = 0
        sum = 0
        amount = 0
        to_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(to_teller_no)).fetchone()
        from_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(from_teller_no)).fetchone()
        cust_hook_batch = CustHookBatch(from_branch_no=from_teller_branch[0],to_branch_no=to_teller_branch[0],from_teller_no=from_teller_no, to_teller_no = to_teller_no, total_count=count, total_amount=amount, typ=typ, note=note, hook_typ=u'客户号', deal_status = u'待审批', start_date = int(time.strftime("20%y%m%d")))
        g.db_session.add(cust_hook_batch)
        g.db_session.flush()

        #取接收人的岗位类型
        to_teller = g.db_session.execute("select gr.group_name from f_user fu, user_group ug, group gr where ug.user_id = fu.role_id and ug.group_id = gr.id and gr.group_type_code = '2000' and fu.user_name = '%s'"%(to_teller_no)).fetchone()
        account_hooks_id = []
        ebank_cust_hooks_id = []
        old_data=g.db_session.query(CustHook).filter(CustHook.id.in_(updatelist)).filter(CustHook.org_no!=to_teller_branch[0]).first()
        if old_data:
            raise Exception(u'业绩不允许跨网点转移')
        custhook_typ=g.db_session.query(CustHook.typ).filter(CustHook.id.in_(updatelist)).all()
        for i in custhook_typ:
            if i[0]== u'贷款' and not (to_teller[0] == u'客户经理' or to_teller[0] == u'外聘客户经理'):
                raise Exception(u'贷款接收人不能是非客户经理')
        
        updatelist_list=[]
        count=len(updatelist)
        for i in updatelist:
            updatelist_list.append(int(i))
        updatelist_list=tuple(updatelist_list)
        if len(updatelist_list)==1:
            g.db_session.execute(u"""merge into Account_Hook ac
            using(select manager_no,org_no,cust_in_no from CUST_HOOK where id in (%s))cu
            on ( ac.manager_no=cu.manager_no and ac.org_no=cu.org_no and ac.cust_in_no=cu.cust_in_no)
            when matched then update set ac.status='待审批',ac.batch_id=%d """%(updatelist_list[0],cust_hook_batch.id))
        else:
             g.db_session.execute(u"""merge into Account_Hook ac
            using(select manager_no,org_no,cust_in_no from CUST_HOOK where id in %s)cu
            on (ac.manager_no=cu.manager_no and ac.org_no=cu.org_no and ac.cust_in_no=cu.cust_in_no)
            when matched then update set ac.status='待审批',ac.batch_id=%d """%(updatelist_list,cust_hook_batch.id))
           
        if len(updatelist_list)==1:
            g.db_session.execute(u"""merge into CUST_HOOK ac
            using(select manager_no,org_no,cust_in_no from CUST_HOOK where id in (%s))cu
            on (ac.manager_no=cu.manager_no and ac.org_no=cu.org_no and ac.cust_in_no=cu.cust_in_no)
            when matched then update set ac.status='待审批',ac.batch_id=%d """%(updatelist_list[0],cust_hook_batch.id))
        else:
             g.db_session.execute(u"""merge into CUST_HOOK ac
            using(select manager_no,org_no,cust_in_no from CUST_HOOK where id in %s)cu
            on (ac.manager_no=cu.manager_no and ac.org_no=cu.org_no and ac.cust_in_no=cu.cust_in_no)
            when matched then update set ac.status='待审批',ac.batch_id=%d """%(updatelist_list,cust_hook_batch.id))
 
        cust_hook_batch.total_count = count

        return u'移交成功'



    """
    审批
    """
    def batch_cust_move_check(self, **kwargs):
        updatelist = kwargs.get('update_key')
        batch_id = kwargs.get('batch_id')
        reason = kwargs.get('reason')
        deal_status = kwargs.get('deal_status')
        to_teller_no = kwargs.get('to_teller_no')
        for pid  in updatelist:
            c = g.db_session.query(custHookBatch).filter(custHookBatch.id == pid).first()
            a = g.db_session.query(CustHook).filter(CustHook.batch_id==pid).all()

            g.db_session.query(custHookBatch).filter(custHookBatch.id == pid).update({'reason':reason,'deal_status':deal_status})
            if deal_status == u'同意':
                g.db_session.query(CustHookBatch).filter(CustHookBatch.id == pid).update({'deal_status':u'同意','status':u'正常'})
                for i in a:
                    t = g.db_session.query(CustHook).filter(CustHook.cust_no==i.cust_no,CustHook.org_no==i.org_no,CustHook.manager_no==c.to_teller_no).first()
                    if(t):
                        per = int(t.percentage) + int(i.percentage)
                        t = g.db_session.query(CustHook).filter(CustHook.Cust_no==i.Cust_no,CustHook.org_no==i.org_no,CustHook.manager_no==c.to_teller_no).update({CustHook.percentage:per})
                        g.db_session.query(CustHook).filter(CustHook.cust_no==i.cust_no,CustHook.org_no==i.org_no,CustHook.manager_no==c.from_teller_no).delete()
            else:
                g.db_session.query(CustHook).filter(CustHook.batch_id == pid).update({'status':u'正常'})
                g.db_session.query(CustHookBatch).filter(CustHookBatch.id == pid).update({'deal_status':u'不同意','status':u'正常'})

        return u'审批成功'

    def batch_cust_move_sum(self, **kwargs):
        updatelist = kwargs.get('update_key')
        amount = kwargs.get('amount')

        total_count = 0
        total_amount = 0
        for pid  in updatelist:
            old_data  = g.db_session.query(CustHook).filter(CustHook.id == pid).first()
            total_count = total_count + 1
        if(amount):
            for i in amount:
                total_amount = total_amount + float(i)

        ta = Decimal(int(total_amount)).quantize(Decimal("0.00"))
        tas = '{:,}'.format(ta)
        return {'total_count':total_count, 'total_amount':tas}

    def staff_all_hook_batch_move(self, **kwargs):
        note = kwargs.get('note')
        from_teller_no = kwargs.get('from_teller_no')
        from_branch_no = kwargs.get('from_branch_no')
        to_teller_no = kwargs.get('to_teller_no')
        print "from_branch_no",from_branch_no
        print "to_teller_no",to_teller_no
        if from_teller_no == to_teller_no:
            raise Exception(u"接收柜员和移交柜员不能相同")

        count = 0
        sum = 0
        amount = 0
        to_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(to_teller_no)).fetchone()
        #from_teller_branch = g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(from_teller_no)).fetchone()
        to_teller_group = g.db_session.execute("select gr.group_name from f_user fu, user_group ug, group gr where ug.user_id = fu.role_id and ug.group_id = gr.id and gr.group_type_code = '2000' and fu.user_name = '%s'"%(to_teller_no)).fetchone()
        cust_hook_batch = CustHookBatch(from_branch_no=from_branch_no,to_branch_no=to_teller_branch[0],from_teller_no=from_teller_no, to_teller_no = to_teller_no, total_count=count, total_amount=amount, typ=u"全部移交", note=note, hook_typ=u'全部移交', deal_status = u'待审批', start_date = int(time.strftime("20%y%m%d")))
        g.db_session.add(cust_hook_batch)
        g.db_session.flush()

        if from_branch_no != to_teller_branch[0]:
            raise Exception(u'全部业绩移交不允许跨网点')

        org_temp = ""
        staff_temp = ""
        account_hooks = g.db_session.query(AccountHook).filter(AccountHook.manager_no == from_teller_no, AccountHook.status.in_([u'预提交审批', u'正常']), AccountHook.org_no == from_branch_no).all()
        for a in account_hooks:
            if a.follow_cust == u'账号优先':
                count = count + 1
            if org_temp == "":
                org_temp = a.org_no
            else:
                if org_temp != a.org_no:
                    raise Exception(u'存在不同机构业绩')

            if a.typ == u'贷款' and not (to_teller_group[0] == u'客户经理' or to_teller_group[0] == u'外聘客户经理'):
                raise Exception(u'有贷款业务接收人不能是非客户经理')

            if (to_teller_group[0] == u'客户经理' or to_teller_group[0] == u'外聘客户经理') and to_teller_branch[0] != a.org_no:
                raise Exception(u'客户经理不允许跨网点转移')

        cust_hooks = g.db_session.query(CustHook).filter(CustHook.manager_no == from_teller_no, CustHook.status.in_([u'预提交审批', u'正常']), CustHook.org_no == from_branch_no).all()    #预提交审批
        for a in cust_hooks:
            count = count + 1
            if org_temp == "":
                org_temp = a.org_no
            else:
                if org_temp != a.org_no:
                    raise Exception(u'存在不同机构业绩')

            if from_branch_no != to_teller_branch[0]:
                raise Exception(u'全部业绩移交不允许跨网点')

            if a.typ == u'贷款' and not (to_teller_group[0] == u'客户经理' or to_teller_group[0] == u'外聘客户经理'):
                raise Exception(u'有贷款业务接收人不能是非客户经理')

            if (to_teller_group[0] == u'客户经理' or to_teller_group[0] == u'外聘客户经理') and to_teller_branch[0] != a.org_no:
                raise Exception(u'客户经理不允许跨网点转移')

        if count==0:
            raise Exception(u'此机构下无此员工的数据或此员工所在的机构下的数据已全部移交,请检查')
        cust_hook_batch.total_count = count

        datadict = {}
        datadict['status'] = u'待审批'
        datadict['batch_id'] = cust_hook_batch.id
        g.db_session.query(AccountHook).filter(AccountHook.manager_no == from_teller_no, AccountHook.status.in_([u'预提交审批', u'正常']),AccountHook.org_no == from_branch_no).update(datadict, synchronize_session=False)
        g.db_session.query(CustHook).filter(CustHook.manager_no == from_teller_no, CustHook.status.in_([u'预提交审批', u'正常']), CustHook.org_no == from_branch_no).update(datadict, synchronize_session=False)

    def staff_all_hook_batch_move_cancel(self, **kwargs):
        from_teller_no = kwargs.get('from_teller_no')
        to_teller_no = kwargs.get('to_teller_no')

        c = g.db_session.query(CustHookBatch).filter(CustHookBatch.from_teller_no == from_teller_no, CustHookBatch.to_teller_no == to_teller_no, CustHookBatch.status == u'待审批').all()
        if len(c) > 1:
            raise Exception(u'存在多条待认定数据,错误!')

        g.db_session.query(CustHookBatch).filter(CustHookBatch.id == pid).update({'deal_status':u'已撤销','status':u'正常'})
        g.db_session.query(CustHook).filter(CustHook.batch_id == pid).update({'status':u'正常'})
        g.db_session.query(AccountHook).filter(AccountHook.batch_id == pid).update({'status':u'正常'})
