# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
import time
from flask import json, g
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import joinedload_all
import xlrd
from ..base import utils
from ..model import Branch,Menu,User,UserBranch,AccountHook,ParentHook


class AccthkService():
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
        self.ckyy = ['manager_no','percentage','start_date','follow_cust','end_date','account_no','src','typ','etl_date','org_no']
        newdata =  kwargs.get('newdata')
        data ={}
        acct_no = newdata['account_no']
        teller_no = newdata['manager_no']

        a = g.db_session.query(AccountHook).filter(AccountHook.account_no == acct_no,AccountHook.status == u'待手工').first()
        if(a):
            g.db_session.query(AccountHook).filter(AccountHook.account_no == acct_no,AccountHook.status == u'待手工').\
            update({AccountHook.manager_no: teller_no, AccountHook.status: u'录入待审批'})
        else:
            Data['hook_type']=u'管户'
            data['status']=u'录入待审批'
            data['src']=u'前端录入'
            for k,v in newdata.items():
                if k in self.ckyy : data[k] = v
            g.db_session.add(AccountHook(**data))
        return u"ok" 

    def ssave(self,**kwargs): #带分润比例的 理财,存款帐号录入
        """
        前端录入--录入待审批
        """
        sum_percentage = 0
        to_percentage = 100
        datalist=kwargs.get('newdata')
        is_have_to = False

        if datalist is None:
            raise Exception(u'上送报文错误!')

        #为了支持先录入客户号变成待审批,然后再录入账号的情况
        for i in datalist:
            newdata = datalist.get(i)
            data={}
            org_no = newdata['org_no']
            account_no = newdata['account_no']
            hook_type = newdata['hook_type']
            typ = newdata['typ']

            is_cust_follow = g.db_session.query(AccountHook).filter(or_(AccountHook.account_no == account_no, AccountHook.card_no== account_no), AccountHook.org_no == org_no, AccountHook.status == u'录入待审批', AccountHook.typ == typ, AccountHook.follow_cust == u'客户号优先').first()
            if is_cust_follow:
                g.db_session.query(AccountHook).filter(or_(AccountHook.account_no == account_no, AccountHook.card_no== account_no), AccountHook.org_no == org_no, AccountHook.status == u'录入待审批', AccountHook.typ == typ, AccountHook.follow_cust == u'客户号优先').delete()
                g.db_session.flush()

        #默认只有1条待认定
        atts = []
        account_no = ""
        org_no = ""
        d_manager = {}
        for i in datalist:
            newdata = datalist.get(i)
            data={}
            org_no = newdata['org_no']
            account_no = newdata['account_no']
            cust_in_no = newdata['cust_in_no']
            manager_no = newdata['manager_no']
            percentage = newdata['percentage']
            hook_type = newdata['hook_type']
            etl_date = newdata['etl_date']
            cust_in_no = newdata['cust_in_no']
            note = newdata['note']
            typ = newdata['typ']

            sum_percentage = sum_percentage + int(percentage)

            if d_manager.has_key(manager_no):
                raise Exception(u'存在相同柜员错误输入!')
            else:
                d_manager[manager_no] = 1

            att = {'manager_no':manager_no, 
                   'org_no':org_no, 
                   'percentage':int(percentage), 
                   'hook_type':hook_type, 
                   'status':u'录入待审批',
                   'follow_cust':u'账号优先',
                   'start_date':int(time.strftime("20%y%m%d")), 
                   'etl_date':etl_date, 
                   'end_date':'29991231', 
                   'account_no':account_no, 
                   'typ':typ, 
                   'note':note,
                   'cust_in_no':cust_in_no
                   }
            atts.append(att)

        is_other_status = g.db_session.query(AccountHook).filter(AccountHook.org_no == org_no,AccountHook.account_no == account_no,AccountHook.status != u'待手工').first()
        if is_other_status:
            raise Exception(u'存在其他状态挂钩关系,不允许再次录入!')

        is_other_status = g.db_session.query(AccountHook).filter(AccountHook.org_no == org_no,AccountHook.card_no == account_no,AccountHook.status != u'待手工').first()
        if is_other_status:
            raise Exception(u'存在其他状态挂钩关系,不允许再次录入!')

        to_acct = g.db_session.query(AccountHook).filter(AccountHook.org_no == org_no,AccountHook.account_no == account_no,AccountHook.status == u'待手工').first()
        if to_acct:
            is_have_to = True
            to_percentage = to_acct.percentage

        if sum_percentage > to_percentage:
            raise Exception(u'输入的比例大于待认定比例')

        if is_have_to: #包含待认定数据
            for att in atts:
                att['src'] = u'批量'
                att['start_date'] = to_acct.start_date
                att['end_date'] = to_acct.end_date
                att['sub_typ'] = to_acct.sub_typ
                att['card_no'] = to_acct.card_no
                att['balance'] = to_acct.balance
                att['exist_avg_balance'] = to_acct.exist_avg_balance
                att['add_avg_balance'] = to_acct.add_avg_balance
                g.db_session.add(AccountHook(**att))

            if to_percentage - sum_percentage > 0:
                to_acct.percentage = to_acct.percentage - sum_percentage
            else:
                g.db_session.query(AccountHook).filter(AccountHook.id == to_acct.id).delete()
        else:
            for att in atts:
                att['src'] = u'前端录入'
                g.db_session.add(AccountHook(**att))

        return u'录入完成'

    def delete(self,**kwargs):
        self.ckyy = ['manager_no','percentage','start_date','end_date','account_no','src','typ','etl_date']
        newdata =  kwargs.get('newdata')
        pid = newdata.get('id')
        org_no = newdata.get('org_no')

        a = g.db_session.query(AccountHook).filter(AccountHook.id == pid,AccountHook.src == u'前端录入').first()
        if(a):
            g.db_session.query(AccountHook).filter(AccountHook.id == pid).delete()
        else:
            g.db_session.query(AccountHook).filter(AccountHook.id == pid).update({AccountHook.status:u'待手工',AccountHook.manager_no:org_no})
        return u"ok" 

    def sdelete(self,**kwargs): #带分润比例的理财,存款账户删除
        newdata =  kwargs.get('newdata')
        pid = newdata.get('id')
        org_no = newdata.get('org_no')
        account_no = newdata.get('account_no')
        percent = newdata.get('percent')
        print percent,'<<<<<<<<<'

        a = g.db_session.query(AccountHook).filter(AccountHook.id == pid,AccountHook.src == u'前端录入').first()
        if(a):
            g.db_session.query(AccountHook).filter(AccountHook.id == pid).delete()
        else:
            t = g.db_session.query(AccountHook).filter(AccountHook.org_no == org_no,AccountHook.account_no == account_no,AccountHook.status == u'待手工').first()
            if(t):
                g.db_session.query(AccountHook).filter(AccountHook.id == pid).delete()
                g.db_session.query(AccountHook).filter(AccountHook.id == t.id).update({AccountHook.percentage:percent + t.percentage})
            else:
                g.db_session.query(AccountHook).filter(AccountHook.id == pid).update({AccountHook.status:u'待手工',AccountHook.manager_no:org_no,AccountHook.follow_cust:u'客户号优先'})
        return u"ok"

    def parent_delete(self,**kwargs): #汇集户录入界面待审批记录删除
        newdata =  kwargs.get('newdata')
        pid = newdata.get('id')
        org_no = newdata.get('org_no')
        account_no = newdata.get('account_no')
        percent = newdata.get('percent')

        g.db_session.query(ParentHook).filter(ParentHook.id == pid).delete()
        return u"ok"

    def update(self,**kwargs):
        self.ckyy = ['manager_no','percentage','start_date','end_date','account_no','src','typ','etl_date','id']
        newdata =  kwargs.get('newdata')
        pid = newdata.get('id')
        newdata.pop('id');
        data ={}
        g.db_session.query(AccountHook).filter(AccountHook.id == pid).update(newdata)
        return u"ok"  

    def supdate(self,**kwargs): #带分润比例的理财,存款账户录入修改
        newdata =  kwargs.get('newdata')
        pid = newdata.get('id')
        org_no = newdata.get('org_no')
        manager_no = newdata.get('manager_no')
        account_no = newdata.get('account_no')
        percentage = newdata.get('percentage')
        typ = newdata.get('typ')
        data ={}

        old = g.db_session.query(AccountHook).filter(AccountHook.id == pid).first()

        """
        防止同一个柜员录入2次检查
        """
        print account_no, manager_no, typ,org_no
        check_manager_no = g.db_session.query(AccountHook).filter(AccountHook.account_no == account_no,AccountHook.typ == typ,AccountHook.manager_no == manager_no).first()
        if check_manager_no and check_manager_no.id != old.id:
            raise Exception (u'存在相同柜员认定关系!')
        
        a = g.db_session.query(AccountHook).filter(AccountHook.id == pid,AccountHook.src == u'前端录入').first()
        if(a):
            t = g.db_session.query(AccountHook.account_no, func.sum(AccountHook.percentage).label("percentage")).filter(AccountHook.account_no == account_no,AccountHook.org_no == org_no,AccountHook.typ == typ,AccountHook.id != pid).group_by(AccountHook.account_no).first()
            if(t):
                per = t.percentage
            else:
                per = 0
            if((int(percentage) + int(per))>100):
                raise Exception (u'占比超过100%错误!')
            else:
                g.db_session.query(AccountHook).filter(AccountHook.id == pid).update({AccountHook.percentage:percentage,AccountHook.manager_no:manager_no})
        else:
            m = g.db_session.query(AccountHook).filter(AccountHook.org_no == org_no,AccountHook.account_no == account_no,AccountHook.typ == typ,AccountHook.status.in_([u'待手工'])).first()
            if(m):
                if((int(percentage)-int(old.percentage))>int(m.percentage)):
                    raise Exception (u'占比超过100%错误!')
                elif((int(percentage)-int(old.percentage))==int(m.percentage)):
                    g.db_session.query(AccountHook).filter(AccountHook.org_no == org_no,AccountHook.account_no == account_no,AccountHook.typ == typ,AccountHook.status.in_([u'待手工'])).delete()
                    g.db_session.query(AccountHook).filter(AccountHook.id == pid).update({AccountHook.percentage:percentage,AccountHook.manager_no:manager_no})
                else:
                    per = int(m.percentage) - int(percentage) + int(old.percentage)
                    g.db_session.query(AccountHook).filter(AccountHook.id == pid).update({AccountHook.percentage:percentage,AccountHook.manager_no:manager_no})
                    g.db_session.query(AccountHook).filter(AccountHook.org_no == org_no,AccountHook.account_no == account_no,AccountHook.typ == typ,AccountHook.status.in_([u'待手工'])).update({AccountHook.percentage:per,AccountHook.manager_no:manager_no})
            else:
                per = int(old.percentage) - int(percentage)
                if per<0:
                    raise Exception (u'占比错误,请检查!')
                newdata['status'] = u'待手工'
                newdata['percentage'] = per
                newdata['manager_no'] = manager_no
                newdata.pop('id')
                g.db_session.query(AccountHook).filter(AccountHook.id == pid).update({AccountHook.percentage:percentage,AccountHook.manager_no:manager_no})
                if per>0: #当剩余占比大于0时插入一条待认定记录 by cchen 2017-04-05 
                    g.db_session.add(AccountHook(**newdata))

        return u"ok"  
    
    def account_move(self, **kwargs):
        move_id = kwargs.get('move_id')
        org_no = kwargs.get('move_org_no')
        manager_no = kwargs.get('move_manager_no')
        start_date = kwargs.get('move_start_date')
        end_date = kwargs.get('move_end_date')
        percentage = kwargs.get('move_percentage')

        #进行比例的处理 TBD
        old_data = g.db_session.query(AccountHook).filter(AccountHook.id == move_id).first();
        g.db_session.add(AccountHook(org_no=org_no, manager_no=manager_no, start_date=start_date, end_date=end_date,percentage=percentage))
        g.db_session.query(AccountHook).filter(AccountHook.id == move_id).delete()
        #g.db_session.query(Gsgx_ck).filter(Gsgx_ck.para_id == pid).update({Gsgx_ck.glrq2:glrq1})
        return u"操作成功"

    def batch_move(self, **kwargs):
        newdata = kwargs.get('newdata')
        updatelist = kwargs.get('update_key')

        for pid  in updatelist:
            q = g.db_session.query(Gsgx_ck).filter(Gsgx_ck.para_id == pid).update({Gsgx_ck.glrq2:newdata['glrq1']})
        for pid in updatelist:
            data = g.db_session.query(Gsgx_ck).filter(Gsgx_ck.para_id == pid).first();
            datadict = newdata
            datadict['dxbh'] = data.dxbh
            datadict['dxxh'] = data.dxxh
            datadict['fjdxbh'] = data.fjdxbh
            datadict['dxmc'] = data.dxmc
            g.db_session.add(Gsgx_ck(**datadict))

        return u'移交成功'

    def upload(self, filepath,):
        """
            批量录入
        """
        print '导入开始'
        data = xlrd.open_workbook(filepath)
        sheet = data.sheet_by_index(0)
        #行
        nrows = sheet.nrows
        bill_type_sign = ""
        list = []
        for r in range(1,nrows):
            MANAGER_NO = str(int(sheet.cell(r,0).value))
            ORG_NO = str(int(sheet.cell(r,1).value))
            PERCENTAGE = sheet.cell(r,2).value
            HOOK_TYPE = sheet.cell(r,3).value
            START_DATE = sheet.cell(r,4).value
            END_DATE = sheet.cell(r,5).value
            STATUS = sheet.cell(r,6).value
            ETL_DATE = sheet.cell(r,7).value
            SRC = sheet.cell(r,8).value
            ACCOUNT_NO = str(int(sheet.cell(r,9).value))
            TYP = sheet.cell(r,10).value
            NOTE = sheet.cell(r,11).value
            temp = {'manager_no':MANAGER_NO, 
                    'org_no':ORG_NO, 
                    'percentage':PERCENTAGE, 
                    'hook_type':HOOK_TYPE, 
                    'start_date':START_DATE, 
                    'end_date':END_DATE, 
                    'status':STATUS, 
                    'etl_date':ETL_DATE, 
                    'src':SRC, 
                    'account_no':ACCOUNT_NO, 
                    'typ':TYP, 
                    'note':NOTE }
            print temp
            g.db_session.add(AccountHook(**temp))        

        return u'导入成功'   

    def approve(self,**kwargs):
        updatelist = kwargs.get('update_key')
        start_date = kwargs.get('start_date')
        datadict = {}

        for pid  in updatelist:
            datadict['status'] = u'录入已审批'
            datadict['etl_date'] = int(time.strftime("20%y%m%d"))
            g.db_session.query(AccountHook).filter(AccountHook.id == pid).update(datadict)
        return u"审批完成"  

    def deny(self,**kwargs):
        """
        一次必须100%录入完毕，不支持分次录入
        """

        updatelist = kwargs.get('update_key')
        for pid  in updatelist:
            g.db_session.query(AccountHook).filter(AccountHook.id == pid).delete()

        """
            a = g.db_session.query(AccountHook).filter(AccountHook.id == pid).first()
            if(a.src=='前端录入'):
                g.db_session.query(AccountHook).filter(AccountHook.id == pid).delete()
                count = count + 1
            else:
                m = g.db_session.query(AccountHook).filter(AccountHook.org_no == a.org_no,AccountHook.account_no == a.account_no,AccountHook.typ == a.typ,AccountHook.status == u'待手工').first()
                if(m):      #有待手工
                    per = int(m.percentage) + int(a.percentage)
                    g.db_session.query(AccountHook).filter(AccountHook.id == m.id).update({AccountHook.percentage:per})
                    g.db_session.query(AccountHook).filter(AccountHook.id == a.id).delete()
                else:
                    print a.id,'******'
                    g.db_session.query(AccountHook).filter(AccountHook.id == a.id).update({AccountHook.manager_no:a.org_no, AccountHook.follow_cust:u'客户号优先', AccountHook.status:u'待手工'})
                    g.db_session.flush()
         """

        return u"审批完成"  
    
    #更改存款账户优先级
    def switch_pri(self,**kwargs):
        updatelist = kwargs.get('update_key')
        datadict = {}
        count =0

        for pid  in updatelist:
            datadict['follow_cust'] = u'账号优先'
            g.db_session.query(AccountHook).filter(AccountHook.id == pid).update(datadict)
            count = count + 1

            print '修改条数：',str(count)
        return u'修改完成'
  
    #录入审批
    def acct_approve(self,**kwargs):
        updatelist = kwargs.get('update_key')
        datadict = {}
        count =0
        print updatelist

        for pid  in updatelist:
            datadict['status'] = u'正常'
            g.db_session.query(AccountHook).filter(AccountHook.id == pid).update(datadict)
            count = count + 1
        print '审批条数：',str(count)
        return u"已通过"  
        
    def acct_deny(self,**kwargs):
        updatelist = kwargs.get('update_key')
        datadict = {}
        count =0

        for pid  in updatelist:
            datadict['status'] = u'审批不通过'
            print pid
            g.db_session.query(AccountHook).filter(AccountHook.id == pid).update(datadict)
            count = count + 1

        print '审批条数：',str(count)
        return u"已否决"  
    
    def check_manager(self,**kwargs):
        staff = kwargs.get('staff')
        org_no = kwargs.get('org_no')
        account_no = kwargs.get('account_no')
        typ = kwargs.get('typ')

        for manager_no in staff:
            t = g.db_session.query(Branch).join(UserBranch,UserBranch.branch_id==Branch.role_id).join(User,User.role_id==UserBranch.user_id).filter(User.user_name==manager_no,Branch.branch_code==org_no).first()
            if(t==None):
                return 0

        return u'前端录入'

    def parent_save(self,**kwargs): #带分润比例的 汇集户主账户录入
        """
        前端录入--录入待审批
        """
        datalist=kwargs.get('newdata')

        if datalist is None:
            raise Exception(u'上送报文错误!')

        atts = []
        account_no = ""
        org_no = ""
        d_manager = {}
        for i in datalist:
            newdata = datalist.get(i)
            data={}
            org_no = newdata['org_no']
            account_no = newdata['account_no']
            cust_in_no = newdata['cust_in_no']
            manager_no = newdata['manager_no']
            percentage = newdata['percentage']
            hook_type = newdata['hook_type']
            etl_date = newdata['etl_date']
            cust_in_no = newdata['cust_in_no']
            note = newdata['note']
            typ = newdata['typ']


            if d_manager.has_key(manager_no):
                raise Exception(u'存在相同柜员错误输入!')
            else:
                d_manager[manager_no] = 1

            att = {'manager_no':manager_no, 
                   'org_no':org_no, 
                   'percentage':int(percentage), 
                   'hook_type':hook_type, 
                   'status':u'录入待审批',
                   'follow_cust':u'账号优先',
                   'start_date':int(time.strftime("20%y%m%d")), 
                   'etl_date':etl_date, 
                   'end_date':'29991231', 
                   'account_no':account_no, 
                   'typ':typ, 
                   'note':note,
                   'cust_in_no':cust_in_no
                   }
            atts.append(att)

        is_other_status = g.db_session.query(ParentHook).filter(ParentHook.account_no == account_no,ParentHook.status != u'失效').first()
        if is_other_status:
            raise Exception(u'存在其他状态挂钩关系,不允许再次录入!')

        for att in atts:
            att['src'] = u'前端录入'
            g.db_session.add(ParentHook(**att))

        return u'录入完成'

    def parent_approve(self,**kwargs):
        updatelist = kwargs.get('update_key')
        start_date = kwargs.get('start_date')
        datadict = {}

        for pid  in updatelist:
            datadict['status'] = u'录入已审批'
            datadict['etl_date'] = int(time.strftime("20%y%m%d"))
            g.db_session.query(ParentHook).filter(ParentHook.id == pid).update(datadict)

        return u"审批完成"  

    def parent_deny(self,**kwargs):
        updatelist = kwargs.get('update_key')
        for pid  in updatelist:
            g.db_session.query(ParentHook).filter(ParentHook.id == pid).delete()

        return u"审批完成"  
    
