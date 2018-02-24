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
import xlrd
from ..base import utils
from ..model import Branch,Menu,User,UserBranch,CustHook,AccountHook
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class CusthkService():
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
        self.ckyy = ['manager_no','percentage','start_date','end_date','cust_no','src','typ','cust_in_no','etl_date','org_no','note','hook_type','status']
        newdata =  kwargs.get('newdata')
        check_org = kwargs.get('check_org')
        staff = kwargs.get('staff')

        data ={}
        cust_no = newdata['cust_no']
        teller_no = newdata['manager_no']
        percentage = newdata['percentage']
        org_no = newdata['org_no']
        typ = newdata['typ']
        print '***********'

        a = g.db_session.query(CustHook).filter(CustHook.typ==typ,CustHook.org_no==org_no,CustHook.cust_no == cust_no,CustHook.status == u'待手工').first()
        if(a):
            print '***********'
            g.db_session.query(CustHook).filter(CustHook.typ==typ,CustHook.org_no==org_no,CustHook.cust_no == cust_no,CustHook.status == u'待手工').\
            update({CustHook.manager_no: teller_no, CustHook.status: u'录入待审批',CustHook.percentage:percentage})
        else:
            for k,v in newdata.items():
                if k in self.ckyy : data[k] = v
            data['hook_type']=u'管户'
            data['status']=u'录入待审批'
            data['src']=u'前端录入'
            print '***********'
            g.db_session.add(CustHook(**data))
        return u"ok" 

    def ssave_with_cust_hook(self, **kwargs):
        """
            已经存在待认定关系的手工录入
        """
        cust_hook_id = kwargs.get('cust_hook_id')
        manager_no = kwargs.get('manager_no')
        print str(cust_hook_id), str(manager_no)
        g.db_session.query(CustHook).filter(CustHook.id == cust_hook_id).update({CustHook.manager_no: manager_no, CustHook.status: u'录入待审批',CustHook.percentage:100})
        return u"ok" 


    def ssave(self,**kwargs): #带分润比例的 存款客户号录入
        """
        录入待审批
        """
        sum_percentage = 0
        to_percentage = 100
        datalist=kwargs.get('newdata')
        is_have_to = False
        type_flag = False

        if datalist is None:
            raise Exception(u'上送报文错误!')

        ctts = []
        cust_in_no = ""
        org_no = ""
        typ = ""
        d_manager  = {}     #判断不允许输入相同柜员
        for i in datalist:
            newdata = datalist.get(i)
            data={}
            org_no = newdata['org_no']
            cust_no = newdata['cust_no']
            cust_in_no = newdata['cust_in_no']
            manager_no = newdata['manager_no']
            percentage = newdata['percentage']
            hook_type = newdata['hook_type']
            etl_date = newdata['etl_date']
            cust_in_no = newdata['cust_in_no']
            note = newdata['note']
            typ = newdata['typ']
            datadict = {}
            if hook_type == u'管户':
                type_flag = True

            sum_percentage = sum_percentage + int(percentage)

            if d_manager.has_key(manager_no):
                raise Exception(u'存在相同柜员错误输入!')
            else:
                d_manager[manager_no] = 1

            ctt = {'manager_no':manager_no, 
                   'org_no':org_no, 
                   'percentage':int(percentage), 
                   'hook_type':hook_type, 
                   'cust_no':cust_no,
                   'status':u'录入待审批',
                   'start_date':int(time.strftime("20%y%m%d")), 
                   'end_date':'29991231', 
                   'etl_date':etl_date, 
                   'typ':typ, 
                   'note':note,
                   'cust_in_no':cust_in_no
                   }
            ctts.append(ctt)
        is_other_status = g.db_session.query(CustHook).filter(CustHook.org_no == org_no,CustHook.cust_in_no == cust_in_no,CustHook.status != u'待手工',CustHook.typ == typ).first()
        if is_other_status:
            raise Exception(u'存在其他状态挂钩关系,不允许再次录入!')

        #默认只有1条待认定,默认业务类型唯一每次
        to_cust = g.db_session.query(CustHook).filter(CustHook.org_no == org_no,CustHook.cust_in_no == cust_in_no,CustHook.status == u'待手工',CustHook.typ == typ).first()
        if to_cust:
            is_have_to = True
            to_percentage = to_cust.percentage

        if sum_percentage > to_percentage:
            raise Exception(u'输入的比例大于待认定比例')

        if is_have_to: #包含待认定数据
            atts = []
            for ctt in ctts:
                ctt['src'] = u'批量'
                ctt['start_date'] = to_cust.start_date
                ctt['end_date'] = to_cust.end_date
                ctt['sub_typ'] = to_cust.sub_typ
                ctt['balance'] = to_cust.balance
                ctt['exist_avg_balance'] = to_cust.exist_avg_balance
                ctt['add_avg_balance'] = to_cust.add_avg_balance
                g.db_session.add(CustHook(**ctt))

                if typ in [u'存款',u'理财']:
                    datadict['manager_no'] = manager_no
                    datadict['status'] = u'录入待审批'

                    acct = g.db_session.query(AccountHook).filter(AccountHook.cust_in_no == ctt['cust_in_no'], AccountHook.org_no == ctt['org_no'], AccountHook.typ == ctt['typ'], AccountHook.status == u'待手工', AccountHook.follow_cust == u'客户号优先').all()
                    for at in acct:
                        att = {'manager_no':ctt['manager_no'], 
                               'org_no':at.org_no, 
                               'percentage':ctt['percentage'], 
                               'hook_type':at.hook_type, 
                               'status':u'录入待审批',
                               'follow_cust':u'客户号优先',
                               'etl_date':at.etl_date, 
                               'start_date':at.start_date, 
                               'end_date':at.end_date, 
                               'account_no':at.account_no, 
                               'typ':at.typ, 
                               'note':at.note,
                               'src':u'批量',
                               'sub_typ':at.sub_typ,
                               'card_no':at.card_no,
                               'cust_in_no':at.cust_in_no,
                               'balance':at.balance,
                               'exist_avg_balance':at.exist_avg_balance,
                               'add_avg_balance':at.add_avg_balance
                                }
                        atts.append(att)

            for att in atts:
                    g.db_session.add(AccountHook(**att))

            g.db_session.query(CustHook).filter(CustHook.id == to_cust.id).delete()
            g.db_session.query(AccountHook).filter(AccountHook.cust_in_no == ctt['cust_in_no'], AccountHook.org_no == ctt['org_no'], AccountHook.typ == ctt['typ'], AccountHook.status == u'待手工', AccountHook.follow_cust == u'客户号优先').delete()
            '''
            if to_percentage - sum_percentage > 0:
                to_cust.percentage = to_cust.percentage - sum_percentage

                #减小处理
                datadict['percent'] = to_cust.percentage - sum_percentage
                g.db_session.query(AccountHook).filter(AccountHook.cust_in_no == ctt['cust_in_no'], AccountHook.org_no == ctt['org_no'], AccountHook.typ == ctt['typ'], AccountHook.status == u'待手工', AccountHook.follow_cust == u'客户号优先').update(datadict)
            else:
                g.db_session.query(CustHook).filter(CustHook.id == to_cust.id).delete()
                g.db_session.query(AccountHook).filter(AccountHook.cust_in_no == ctt['cust_in_no'], AccountHook.org_no == ctt['org_no'], AccountHook.typ == ctt['typ'], AccountHook.status == u'待手工', AccountHook.follow_cust == u'客户号优先').delete()
            '''

        else:
            if typ in [u'理财']:
                raise Exception(u'理财必须存在待认定数据才可以录入!')
            for ctt in ctts:
                ctt['src'] = u'前端录入'
                g.db_session.add(CustHook(**ctt))

        hk_typ = g.db_session.query(CustHook).filter(CustHook.org_no == org_no, CustHook.cust_in_no == cust_in_no, CustHook.typ == typ, CustHook.hook_type == u'管户').first()
        if not type_flag and hk_typ is None:
            raise Exception(u'每个客户号至少要有一个主办客户经理,请检查!')
        if type_flag and hk_typ:
            raise Exception(u'每个客户号最多只能有一个主办客户经理,请检查!')

        return u'录入完成'
            
    def delete(self,**kwargs):
        self.ckyy = ['manager_no','percentage','start_date','end_date','cust_no','src','typ','etl_date']
        newdata =  kwargs.get('newdata')
        pid = newdata.get('id')
        org_no = newdata.get('org_no')

        a = g.db_session.query(CustHook).filter(CustHook.id == pid,CustHook.src == u'前端录入').first()
        if(a):
            g.db_session.query(CustHook).filter(CustHook.id == pid).delete()
        else:
            g.db_session.query(CustHook).filter(CustHook.id == pid).update({CustHook.status:u'待手工',CustHook.manager_no:org_no})
        return u"ok" 

    def sdelete(self,**kwargs): #带分润比例的存款客户号删除
        newdata =  kwargs.get('newdata')
        pid = newdata.get('id')
        org_no = newdata.get('org_no')
        cust_no = newdata.get('cust_no')
        manager_no = newdata.get('manager_no')
        percent = newdata.get('percent')
        date_id = newdata.get('date_id')

        old_data = g.db_session.query(CustHook).filter(CustHook.id == pid).first()
        cust_in_no = old_data.cust_in_no

        a = g.db_session.query(CustHook).filter(CustHook.id == pid,CustHook.src == u'前端录入').first()
        if(a):  #若原来记录是非待认定数据,直接删除
            print u'非待认定数据,直接删除'
            g.db_session.execute(" delete from account_hook where org_no = '%s' and manager_no = '%s' and src = '前端录入' and status = '录入待审批' and follow_cust = '客户号优先' and cust_in_no = '%s'"%(org_no,manager_no,a.cust_in_no))
            g.db_session.query(CustHook).filter(CustHook.id == pid).delete()
            print cust_no,org_no,manager_no
        else:   #若原来记录是待认定数据,进一步判断
            print u'为待认定数据'
            t = g.db_session.query(CustHook).filter(CustHook.org_no == org_no,CustHook.cust_no == cust_no,CustHook.status == u'待手工').first()
            if(t):  #若该客户号仍有待认定比例剩余,删除待审批后把比例加回去
                print u'任有待认定比例剩余'
                print t.percentage
                print t.cust_in_no
                per = int(percent) + int(t.percentage)
                g.db_session.execute("delete from account_hook  where cust_in_no = '%s' and org_no='%s' and manager_no='%s' "%(cust_in_no,org_no,manager_no))
                print 'delete ok'
                g.db_session.execute("update account_hook set percentage='%s' where cust_in_no = '%s' and org_no='%s' and status='待手工' "%(per,cust_in_no,org_no))
                g.db_session.query(CustHook).filter(CustHook.id == pid).delete()
                g.db_session.query(CustHook).filter(CustHook.org_no == org_no,CustHook.cust_no == cust_no,CustHook.status == u'待手工').update({CustHook.percentage:per})
            else:   #若没有剩余,直接改状态
                print u'无待认定比例剩余'
                g.db_session.execute("update account_hook set status='待手工',manager_no='%s' where cust_in_no = '%s' and org_no='%s' and manager_no='%s'"%(org_no,cust_in_no,org_no,manager_no))
                g.db_session.query(CustHook).filter(CustHook.id == pid).update({CustHook.status:u'待手工',CustHook.manager_no:org_no,CustHook.hook_type:u'管户'})
        return u"操作成功"

    def update(self,**kwargs):
        self.ckyy = ['manager_no','percentage','start_date','end_date','cust_no','src','typ','etl_date','id']
        newdata =  kwargs.get('newdata')
        pid = newdata.get('id')
        newdata.pop('id');
        print newdata
        g.db_session.query(CustHook).filter(CustHook.id == pid).update(newdata)
        return u"ok"  
 
    def supdate(self,**kwargs): #带分润比例的存款客户号录入修改
        newdata =  kwargs.get('newdata')
        date_id = kwargs.get('date_id')
        pid = newdata.get('id')
        org_no = newdata.get('org_no')
        cust_no = newdata.get('cust_no')
        manager_no = newdata.get('manager_no')
        percentage = newdata.get('percentage')
        typ = newdata.get('typ')
        data ={}
        print date_id

        old = g.db_session.query(CustHook).filter(CustHook.id == pid).first()
        print cust_no, manager_no, typ
        check_manager_no = g.db_session.query(CustHook).filter(CustHook.cust_no == cust_no,CustHook.typ == typ,CustHook.manager_no == manager_no).first()
        if check_manager_no and check_manager_no.id != old.id:
            raise Exception (u'存在相同柜员认定关系!')

        h = g.db_session.query(CustHook).filter(CustHook.id == pid,CustHook.src == u'批量').first()
        if(h):
            t = g.db_session.query(CustHook.cust_no, func.sum(CustHook.percentage).label("percentage")).filter(CustHook.cust_no == cust_no,CustHook.org_no == org_no,CustHook.typ == typ,CustHook.id != pid).group_by(CustHook.cust_no).first()
            if(t):
                per = t.percentage
            else:
                per = 0
            if((int(percentage) + int(per))>100):
                print '占比超过100,前台alert!'
                raise Exception (u'占比超过100%错误!')

        a = g.db_session.query(CustHook).filter(CustHook.id == pid,CustHook.src == u'前端录入').first()
        if(a):
            t = g.db_session.query(CustHook.cust_no, func.sum(CustHook.percentage).label("percentage")).filter(CustHook.cust_no == cust_no,CustHook.org_no == org_no,CustHook.typ == typ,CustHook.id != pid).group_by(CustHook.cust_no).first()
            if(t):
                per = t.percentage
            else:
                per = 0
            if((int(percentage) + int(per))>100):
                print '占比超过100,前台alert!'
                raise Exception (u'占比超过100%错误!')
            else:
                print u'非待认定数据直接修改'
                g.db_session.query(CustHook).filter(CustHook.id == pid).update({CustHook.percentage:percentage,CustHook.manager_no:manager_no})
        else:
            m = g.db_session.query(CustHook).filter(CustHook.org_no == org_no,CustHook.cust_no == cust_no,CustHook.typ == typ,CustHook.status == u'待手工').first()
            if(m):
                if((int(percentage)-int(old.percentage))>int(m.percentage)):
                    raise Exception (u'占比超过100%错误!')
                elif((int(percentage)-int(old.percentage))==int(m.percentage)):
                    print u'待认定数据且修改占比之后待认定无剩余占比'
                    g.db_session.execute("delete from account_hook  where account_no in( select a.account_no from F_BALANCE f join d_account c on c.id=f.account_id join account_hook a on a.ACCOUNT_NO=c.account_no join cust_hook t on t.CUST_IN_NO=f.CST_NO join d_org o on o.ID=f.ORG_ID join d_sales_temp d on d.SALE_CODE=t.MANAGER_NO where f.ACCT_TYPE=1 and date_id='%s' and cust_no='%s') and org_no='%s' and status='待手工' "%(date_id,cust_no,org_no))
                    g.db_session.execute("update account_hook set percentage='%s' where account_no in( select a.account_no from F_BALANCE f join d_account c on c.id=f.account_id join account_hook a on a.ACCOUNT_NO=c.account_no join cust_hook t on t.CUST_IN_NO=f.CST_NO join d_org o on o.ID=f.ORG_ID join d_sales_temp d on d.SALE_CODE=t.MANAGER_NO where f.ACCT_TYPE=1 and date_id='%s' and cust_no='%s') and org_no='%s' and manager_no='%s' "%(date_id,percentage,cust_no,org_no,manager_no))
                    g.db_session.query(CustHook).filter(CustHook.org_no == org_no,CustHook.cust_no == cust_no,CustHook.typ == typ,CustHook.status == u'待手工').delete()
                    g.db_session.query(CustHook).filter(CustHook.id == pid).update({CustHook.percentage:percentage,CustHook.manager_no:manager_no})
                else:
                    print u'待认定数据且修改占比之后待认定有剩余占比'
                    per = int(m.percentage) - int(percentage) + int(old.percentage)
                    g.db_session.execute("update account_hook set percentage='%s' where account_no in( select a.account_no from F_BALANCE f join d_account c on c.id=f.account_id join account_hook a on a.ACCOUNT_NO=c.account_no join cust_hook t on t.CUST_IN_NO=f.CST_NO join d_org o on o.ID=f.ORG_ID join d_sales_temp d on d.SALE_CODE=t.MANAGER_NO where f.ACCT_TYPE=1 and date_id='%s' and cust_no='%s') and org_no='%s' and status='待手工' "%(date_id,per,cust_no,org_no))
                    g.db_session.execute("update account_hook set percentage='%s' where account_no in( select a.account_no from F_BALANCE f join d_account c on c.id=f.account_id join account_hook a on a.ACCOUNT_NO=c.account_no join cust_hook t on t.CUST_IN_NO=f.CST_NO join d_org o on o.ID=f.ORG_ID join d_sales_temp d on d.SALE_CODE=t.MANAGER_NO where f.ACCT_TYPE=1 and date_id='%s' and cust_no='%s') and org_no='%s' and manager_no='%s' "%(date_id,percentage,cust_no,org_no,manager_no))
                    g.db_session.query(CustHook).filter(CustHook.id == pid).update({CustHook.percentage:percentage,CustHook.manager_no:manager_no})
                    g.db_session.query(CustHook).filter(CustHook.org_no == org_no,CustHook.cust_no == cust_no,CustHook.typ == typ,CustHook.status == u'待手工').update({CustHook.percentage:per,CustHook.manager_no:manager_no})
            else:
                per = int(old.percentage) - int(percentage)
                newdata['status'] = u'待手工'
                newdata['percentage'] = per
                newdata['manager_no'] = org_no
                acct_newdata = newdata
                print date_id,cust_no
                print '***************'
                g.db_session.execute("update account_hook set percentage='%s',manager_no='%s' where account_no in( select a.account_no from f_balance f join d_account c on c.id=f.account_id join account_hook a on a.account_no=c.account_no join cust_hook t on t.cust_in_no=f.cst_no join d_org o on o.id=f.org_id join d_sales_temp d on d.sale_code=t.manager_no where f.acct_type=1 and date_id='%s' and cust_no='%s') and org_no='%s' and manager_no='%s' "%(date_id,percentage,manager_no,cust_no,org_no,manager_no))
                g.db_session.query(CustHook).filter(CustHook.id == pid).update({CustHook.percentage:percentage,CustHook.manager_no:manager_no})
                newdata.pop('id')
                #g.db_session.add(CustHook(**newdata))
        return u"ok"  
    
    def account_move(self, **kwargs):
        move_id = kwargs.get('move_id')
        org_no = kwargs.get('move_org_no')
        manager_no = kwargs.get('move_manager_no')
        start_date = kwargs.get('move_start_date')
        end_date = kwargs.get('move_end_date')
        percentage = kwargs.get('move_percentage')

        #进行比例的处理 tbd
        old_data = g.db_session.query(CustHook).filter(CustHook.id == move_id).first();
        g.db_session.add(CustHook(org_no=org_no, manager_no=manager_no, start_date=start_date, end_date=end_date,percentage=percentage))
        g.db_session.query(CustHook).filter(CustHook.id == move_id).delete()
        #g.db_session.query(gsgx_ck).filter(gsgx_ck.para_id == pid).update({gsgx_ck.glrq2:glrq1})
        return u"操作成功"

    def batch_move(self, **kwargs):
        newdata = kwargs.get('newdata')
        updatelist = kwargs.get('update_key')

        for pid  in updatelist:
            q = g.db_session.query(gsgx_ck).filter(gsgx_ck.para_id == pid).update({gsgx_ck.glrq2:newdata['glrq1']})
        for pid in updatelist:
            data = g.db_session.query(gsgx_ck).filter(gsgx_ck.para_id == pid).first();
            datadict = newdata
            datadict['dxbh'] = data.dxbh
            datadict['dxxh'] = data.dxxh
            datadict['fjdxbh'] = data.fjdxbh
            datadict['dxmc'] = data.dxmc
            g.db_session.add(gsgx_ck(**datadict))

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
            manager_no = str(int(sheet.cell(r,0).value))
            org_no = str(int(sheet.cell(r,1).value))
            percentage = sheet.cell(r,2).value
            hook_type = sheet.cell(r,3).value
            start_date = sheet.cell(r,4).value
            end_date = sheet.cell(r,5).value
            status = sheet.cell(r,6).value
            etl_date = sheet.cell(r,7).value
            src = sheet.cell(r,8).value
            cust_no = str(int(sheet.cell(r,9).value))
            typ = sheet.cell(r,10).value
            note = sheet.cell(r,11).value
            temp = {'manager_no':manager_no, 
                    'org_no':org_no, 
                    'percentage':percentage, 
                    'hook_type':hook_type, 
                    'start_date':start_date, 
                    'end_date':end_date, 
                    'status':status, 
                    'etl_date':etl_date, 
                    'src':src, 
                    'cust_no':cust_no, 
                    'typ':typ, 
                    'note':note }
            print temp
            g.db_session.add(CustHook(**temp))        

        return u'导入成功'
    
    def sql2dict(self,sql,cursor):
        cursor.execute( sql )
        r=cursor.fetchone()
        d = {}
        while r:
            d[str(r[0])] = list(r)
            r = cursor.fetchone()
        #current_app.logger.debug(d)
        return d

    def sql2dict_in(self,sql,cursor):
        cursor.execute( sql )
        r=cursor.fetchone()
        d = {}
        while r:
            if str(r[0]) in d:
                d[str(r[0])].append(r[1])
            else:
                d[str(r[0])]=[]
                d[str(r[0])].append(r[1])
            r = cursor.fetchone()
        return d

    def upload_per_cust(self, filepath,):
        """
            对私客户号认定关系批量录入,必须存在待认定否则无法更新
        """
        print '导入开始'
        data = xlrd.open_workbook(filepath)
        sheet = data.sheet_by_index(0)
        #行
        nrows = sheet.nrows
        print u'总行数', str(nrows)
        line = 2 
        try:
            sql = """
                select fu.user_name,bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id
            """
            connection  = g.db_session.bind.raw_connection()
            cursor  = connection.cursor()
            tbs = self.sql2dict(sql,cursor)#员工号:员工号,机构号

            sql = """
                select org_no||'-'||cust_no||'-'||id,id,cust_in_no
                from cust_hook ch
                where ch.typ='存款'
                    and ch.status='待手工' 
            """
            cust_orgs = self.sql2dict(sql,cursor)
            
            acct_sql="""
            select ch.org_no||'-'||ch.cust_no||'-'||ch.id, ah.id　
            from account_hook ah
            join cust_hook ch on ah.org_no=ch.org_no and ah.cust_in_no=ch.cust_in_no
            where ch.typ='存款'  and ch.status='待手工'  and ah.typ = '存款'
            and ah.status='待手工'and ah.follow_cust='客户号优先'
             
            """
            acct_id_list=self.sql2dict_in(acct_sql,cursor)

            usql1 = """
                    update  cust_hook ch 
                        set status='录入待审批'
                            ,manager_no=?
                    where ch.id = ?
            """
            #usql2 = """
            #        update  account_hook ah 
            #            set status='录入待审批'
            #                ,manager_no=?
            #        where ah.org_no=? 
            #            and cust_in_no =? 
            #            and typ = '存款'
            #            and status='待手工'
            #            and follow_cust='客户号优先'
            #"""
            usql2 = """
                update  account_hook ah
                set status='录入待审批'
                ,manager_no=?
                where ah.id = ?
            """
            update_rows1 = []
            update_rows2 = []
            #connection.begin()
            for r in range(2,nrows):
                rlen = len(sheet.row_values(r))
                print u'总列数', str(rlen)

                if rlen != 11:
                    err_message = u'模版错误,请检查列数'
                    raise Exception(err_message)
                temp_id=sheet.cell(r,0).value
                temp_org_no = sheet.cell(r,1).value
                cust_type = sheet.cell(r,3).value
                cust_no = str(sheet.cell(r,4).value).strip()
                temp_manager_no = sheet.cell(r,10).value

                line = line + 1
                print str(line), temp_org_no, cust_type, cust_no, temp_manager_no
                err_message = u'第' + str(line) + u'行,客户号:' + cust_no

                if temp_org_no == '' and temp_manager_no == '' and cust_no == '':
                    continue

                if temp_org_no == '' or temp_manager_no == '' or cust_no == '':
                    err_message = err_message + u'关键字段为空'
                    raise Exception(err_message)

                manager_no = str(int(temp_manager_no)).strip()
                org_no = str(int(temp_org_no)).strip()
                id_1=str(int(temp_id)).strip()
                if manager_no[0:3] != '966' or org_no[0:3] != '966':
                    err_message = err_message + u'机构号,客户经理号码不符合规则!'
                    raise Exception(err_message)

                if len(org_no) != 6 or len(manager_no) !=7:
                    err_message = err_message + u'机构号,客户经理号码长度错误!'
                    raise Exception(err_message)

                if cust_type != u'对私':
                    err_message = err_message + u'不支持的客户类型' + cust_type
                    raise Exception(err_message)
                if manager_no is None or manager_no == "":
                    err_message = err_message + u'客户经理号码未输入'
                    raise Exception(err_message)

                tb = tbs.get(str(manager_no))
                if tb is None :
                    err_message = err_message + u',客户经理号码错误'
                    raise Exception(err_message)
                to_teller_branch = tb[1]


                if str(to_teller_branch) != org_no:
                    err_message = err_message + u',客户经理非本网点'
                    raise Exception(err_message)
                
                kk = str(org_no).strip() + "-" +str(cust_no).strip()+"-"+str(id_1).strip()
                old_data = cust_orgs.get(kk)
                if old_data is None:
                    err_message = err_message + u',不存在待认定关系'
                    raise Exception(err_message)
                update_rows1.append( [manager_no, old_data[1]] )
                acct_date=acct_id_list.get(kk)
                if acct_date is None:#更新account_hook
                    pass
                else:
                    for i in acct_date :
                        update_rows2.append( [manager_no, i])
            cursor.executemany(usql1, update_rows1)
            cursor.executemany(usql2, update_rows2)
            connection.connection.commit()
        except Exception,e:
            connection.connection.rollback()
            #g.db_session.rollback()
            print Exception,':',e
            return str(e)

        return u'导入成功'


    def upload_per_ebank(self, filepath,):
        """
            电子银行认定关系批量录入,必须存在待认定否则无法更新
        """
        print '导入开始'
        data = xlrd.open_workbook(filepath)
        sheet = data.sheet_by_index(0)
        #行
        nrows = sheet.nrows
        line = 2 
        try:
            sql = """
                select fu.user_name,bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id
            """
            connection  = g.db_session.bind.raw_connection()
            cursor  = connection.cursor()
            tbs = self.sql2dict(sql,cursor)#员工号:员工号,机构号

            cust_hook_sql="""
            select org_no||'-'||cust_no,id from cust_hook where typ='电子银行' and status='待手工'
            """
            cust_no_dict=self.sql2dict_in(cust_hook_sql,cursor)#org_no||'-'||cust_no: [id]
            current_app.logger.debug(cust_no_dict)

            update_sql="""
            update cust_hook 
            set status='录入待审批',manager_no=?
            where id=?
            """

            org_cust_no=[]
            for r in range(2,nrows):
                rlen = len(sheet.row_values(r))
                if rlen != 6:
                    err_message = u'模版错误,请检查列数'
                    raise Exception(err_message)

                temp_org_no = sheet.cell(r,0).value
                cust_no = sheet.cell(r,2).value.strip()
                temp_manager_no = sheet.cell(r,5).value
                print str(line), temp_org_no, cust_no, temp_manager_no

                line = line + 1
                err_message = u'第' + str(line) + u'行,客户号:' + cust_no

                if temp_org_no == '' or temp_manager_no == '' or cust_no == '':
                    err_message = err_message + u'关键字段为空'
                    raise Exception(err_message)

                manager_no = str(int(temp_manager_no)).strip()
                org_no = str(int(temp_org_no)).strip()

                if manager_no[0:3] != '966' or org_no[0:3] != '966':
                    err_message = err_message + u'机构号,客户经理号码不符合规则!'
                    raise Exception(err_message)

                if len(org_no) != 6 or len(manager_no) !=7:
                    err_message = err_message + u'机构号,客户经理号码长度错误!'
                    raise Exception(err_message)
                tb=tbs.get(str(manager_no))
                if tb is None :
                    err_message = err_message + u',客户经理号码错误'
                    raise Exception(err_message)
                to_teller_branch=tb[1]

                if str(to_teller_branch) != org_no:
                    err_message = err_message + u'客户经理非本网点'
                    raise Exception(err_message)

                
                old_data=cust_no_dict.get(str(org_no)+'-'+str(cust_no))
                if old_data is None:
                    err_message = err_message + u'不存在待认定关系'
                    raise Exception(err_message)
                for i in old_data:
                    org_cust_no.append([manager_no,i])

            cursor.executemany(update_sql,org_cust_no)
            connection.connection.commit()
        except Exception,e:
            connection.connection.rollback()
            print Exception,':',e
            return str(e)

        return u'导入成功'

    def approve(self,**kwargs):
        updatelist = kwargs.get('update_key')
        datadict = {}

        for pid  in updatelist:
            old_data = g.db_session.query(CustHook).filter(CustHook.id == pid).first()
            datadict['status'] = u'录入已审批'
            datadict['etl_date'] = int(time.strftime("20%y%m%d"))
            g.db_session.query(CustHook).filter(CustHook.id == pid).update(datadict)
            print old_data.typ
            if old_data.typ in [u'存款',u'理财']:
                g.db_session.query(AccountHook).filter(AccountHook.cust_in_no == old_data.cust_in_no,AccountHook.org_no == old_data.org_no, AccountHook.manager_no == old_data.manager_no, AccountHook.typ == old_data.typ, AccountHook.follow_cust == u'客户号优先', AccountHook.status == u'录入待审批').update(datadict)

            if old_data.typ in [u'电子银行']:
                g.db_session.query(CustHook).filter(CustHook.cust_in_no == old_data.cust_in_no,CustHook.org_no == old_data.org_no, CustHook.typ == old_data.typ, CustHook.status == u'录入待审批').update(datadict)
        return u"审批完成"  
        
    def deny(self,**kwargs):
        updatelist = kwargs.get('update_key')
        datadict = {}
        count =0

        for pid  in updatelist:
            print pid
            old_data = g.db_session.query(CustHook).filter(CustHook.id == pid).first()
            org_no = old_data.org_no
            manager_no = old_data.manager_no
            cust_in_no = old_data.cust_in_no
            typ = old_data.typ
            if(old_data.src=='前端录入'):
                g.db_session.query(CustHook).filter(CustHook.id == pid).delete()
            else:
                ch = g.db_session.query(CustHook).filter(CustHook.cust_in_no == old_data.cust_in_no,CustHook.org_no == old_data.org_no, CustHook.typ == old_data.typ, CustHook.status == u'待手工').first()
                if ch :
                    g.db_session.query(CustHook).filter(CustHook.id == ch.id).update({CustHook.percentage:old_data.percentage + ch.percentage})
                    g.db_session.query(CustHook).filter(CustHook.id == old_data.id).delete()

                    if old_data.typ in (u'存款', u'理财'):
                        at = g.db_session.query(AccountHook).filter(AccountHook.cust_in_no == old_data.cust_in_no, AccountHook.org_no == old_data.org_no, AccountHook.typ == old_data.typ, AccountHook.status == u'待手工', AccountHook.follow_cust == u'客户号优先').first()
                        if at :
                            g.db_session.query(AccountHook).filter(AccountHook.id == at.id).update({AccountHook.percentage:old_data.percentage + ch.percentage})
                            g.db_session.query(AccountHook).filter(AccountHook.cust_in_no == old_data.cust_in_no, AccountHook.org_no == old_data.org_no, AccountHook.typ == old_data.typ, AccountHook.status == u'录入待审批', AccountHook.follow_cust == u'客户号优先').delete()
                        else:
                            g.db_session.query(AccountHook).filter(AccountHook.cust_in_no == old_data.cust_in_no, AccountHook.org_no == old_data.org_no, AccountHook.typ == old_data.typ, AccountHook.status == u'录入待审批', AccountHook.follow_cust == u'客户号优先').update({'status':u'待手工','manager_no':old_data.org_no})
                            g.db_session.flush()
                else:
                    datadict['status'] = u'待手工'
                    datadict['manager_no'] = old_data.org_no
                    datadict['hook_type'] = u'管户'
                    g.db_session.query(CustHook).filter(CustHook.id == old_data.id).update(datadict)
                    g.db_session.flush()

                    if old_data.typ in (u'存款', u'理财'):
                        g.db_session.query(AccountHook).filter(AccountHook.cust_in_no == old_data.cust_in_no, AccountHook.manager_no == manager_no, AccountHook.org_no == old_data.org_no, AccountHook.typ == old_data.typ,  AccountHook.status == u'录入待审批',AccountHook.follow_cust == u'客户号优先').update(datadict)
                        g.db_session.flush()

                if old_data.typ in [u'电子银行']:
                    datadict['status'] = u'待手工'
                    datadict['manager_no'] = old_data.org_no
                    g.db_session.query(CustHook).filter(CustHook.cust_in_no == old_data.cust_in_no,CustHook.org_no == old_data.org_no, CustHook.typ == old_data.typ).update(datadict)

        return u"审批完成"  

    #录入审批
    def cust_approve(self,**kwargs):
        updatelist = kwargs.get('update_key')
        datadict = {}
        count =0

        for pid  in updatelist:
            datadict['status'] = u'正常'
            g.db_session.query(CustHook).filter(CustHook.id == pid).update(datadict)
            count = count + 1

        print '审批条数：',str(count)
        return u"已通过"  
        
    def cust_deny(self,**kwargs):
        updatelist = kwargs.get('update_key')
        datadict = {}
        count =0

        for pid  in updatelist:
            datadict['status'] = u'审批不通过'
            g.db_session.query(CustHook).filter(CustHook.id == pid).update(datadict)
            count = count + 1

        print '审批条数：',str(count)
        return u"已否决!"  

    def get_staff_name(self,**kwargs):
        user_name = kwargs.get('user_name') 
        name = ''

        a = g.db_session.query(User).filter(User.user_name == user_name).first()
        if(a):
            name = a
        return name

    def get_manlist(self,**kwargs):
        cust_no = kwargs.get('cust_no')
        org_no = kwargs.get('org_no')
        typ = kwargs.get('typ')
        print cust_no, org_no, typ
        
        asql = g.db_session.query(User)\
             .join(CustHook,(CustHook.manager_no==User.user_name))\
             .filter(CustHook.cust_no == cust_no,CustHook.org_no == org_no,CustHook.hook_type==u'分润', CustHook.typ == typ)
        print asql
        a = asql.all()
        return [{'user_name':i.user_name,'name':i.name} for i in a]

    def change_main(self,**kwargs):
        cust_no = kwargs.get('cust_no')
        org_no = kwargs.get('org_no')
        manager_no = kwargs.get('staff_code')
        typ = kwargs.get('typ')
        
        g.db_session.query(CustHook).filter(CustHook.cust_no==cust_no,CustHook.org_no==org_no,CustHook.hook_type==u'管户', CustHook.typ == typ).update({'hook_type':u'分润'})
        g.db_session.query(CustHook).filter(CustHook.cust_no==cust_no,CustHook.org_no==org_no,CustHook.manager_no==manager_no, CustHook.typ == typ).update({'hook_type':u'管户'})

        cust_hook = g.db_session.query(CustHook).filter(CustHook.cust_no==cust_no,CustHook.org_no==org_no,CustHook.typ == typ).first()
        cust_in_no = cust_hook.cust_in_no

        g.db_session.query(AccountHook).filter(AccountHook.cust_in_no==cust_in_no,AccountHook.org_no==org_no,AccountHook.hook_type==u'管户', AccountHook.typ == typ).update({'hook_type':u'分润'})
        g.db_session.query(AccountHook).filter(AccountHook.cust_in_no==cust_in_no,AccountHook.org_no==org_no, AccountHook.manager_no == manager_no, AccountHook.typ == typ).update({'hook_type':u'管户'})

        return u'更改成功!'
        
    def check_manager(self,**kwargs):
        staff = kwargs.get('staff')
        org_no = kwargs.get('org_no')
        cust_no = kwargs.get('cust_no')
        typ = kwargs.get('typ')

        for manager_no in staff:
            t = g.db_session.query(Branch).join(UserBranch,UserBranch.branch_id==Branch.role_id).join(User,User.role_id==UserBranch.user_id).filter(User.user_name==manager_no,Branch.branch_code==org_no).first()
            if(t==None):
                return 0
        return u'前端录入'

    def check_org(self,**kwargs):
        staff = kwargs.get('staff')
        org = kwargs.get('org')

        a = g.db_session.query(Branch).join(UserBranch,UserBranch.branch_id==Branch.role_id).join(User,User.role_id==UserBranch.user_id).filter(User.user_name==staff).first()
        return a

    def hk_acct(self,**kwargs):
        datalist=kwargs.get('newdata')
        rows = kwargs.get('rows')
        manager_no = kwargs.get('manager_no')
        percentage = kwargs.get('percentage')

        for i in datalist:
            newdata = datalist.get(i)
            org_no = newdata['org_no']
            manager_no = newdata['manager_no']
            percentage = newdata['percentage']
            for j in rows:
                a = g.db_session.query(AccountHook).filter(AccountHook.account_no == j[0],AccountHook.org_no == org_no,AccountHook.status == u'待手工').first()
                if(a):
                    g.db_session.query(AccountHook).filter(AccountHook.account_no == j[0],AccountHook.org_no == org_no,AccountHook.status == u'待手工').update({AccountHook.manager_no:manager_no,AccountHook.status:u'录入待审批',AccountHook.percentage:percentage,AccountHook.follow_cust:u'客户号优先'})
                else:
                    m = g.db_session.query(AccountHook).filter(AccountHook.account_no == j[0],AccountHook.org_no == org_no,AccountHook.status == u'录入待审批').first()
                    if(m):
                        temp = {'manager_no':manager_no, 
                                'org_no':org_no, 
                                'percentage':percentage, 
                                'hook_type':m.hook_type, 
                                'start_date':m.start_date, 
                                'end_date':m.end_date, 
                                'status':m.status, 
                                'etl_date':m.etl_date, 
                                'src':m.src, 
                                'typ':m.typ,
                                'account_no':m.account_no, 
                                'note':m.note, 
                                'sub_typ':m.sub_typ,
                                'card_no':m.card_no,
                                'follow_cust':u'客户号优先'
                                }
                        g.db_session.add(AccountHook(**temp))
        return u"录入成功!"

    def ebk_update(self,**kwargs):
        newdata = kwargs.get('newdata')
        org_no = newdata['org_no']
        cust_no = newdata['cust_no']
        typ = u'电子银行'
        status = u'录入待审批'

        g.db_session.query(CustHook).filter(CustHook.cust_no == cust_no,CustHook.org_no == org_no,CustHook.typ == typ).update(newdata)
        return u'更新成功'

    def ebk_delete(self,**kwargs):
        newdata = kwargs.get('newdata')
        org_no = newdata['org_no']
        cust_no = newdata['cust_no']
        manager_no = newdata['manager_no']
        typ = u'电子银行'
        status = u'录入待审批'

        a = g.db_session.query(CustHook).filter(CustHook.manager_no == manager_no,CustHook.org_no == org_no,CustHook.typ == typ,CustHook.cust_no == cust_no,CustHook.status == status,CustHook.src == u'前端录入').first()
        if(a):
            g.db_session.query(CustHook).filter(CustHook.manager_no == manager_no,CustHook.org_no == org_no,CustHook.typ == typ,CustHook.cust_no == cust_no,CustHook.status == status).delete()
        else:
            g.db_session.query(CustHook).filter(CustHook.manager_no == manager_no,CustHook.org_no == org_no,CustHook.typ == typ,CustHook.cust_no == cust_no,CustHook.status == status).update({'manager_no':org_no,'status':u'待手工'})
        return u'删除成功'
