# -*- coding:utf-8 -*-
#!/bin/python  
import traceback
import os,sys
import DB2  
import csv
import calendar
import subprocess
from sys import path
import multiprocessing
from multiprocessing import Process,Queue,Pool
import os,  random  
import time as systime
#print sys.path
import time as thistime
import datetime as thisdatetime
from datetime import timedelta,datetime
from decimal import *
from etl.star.dim import *
from etl.base.conf import *
import etl.base.util as util
import etl.base.logger as logger
from etl.star import hookstar 
from etl.star import fix_seq as fixseq
from etl.star import odsload as ods_load 
from etl.star import etl_hook as etlhook
from etl.star import ccrdstar as ccrd_star
from etl.star import etl_people as etlpeople
from etl.star import ebillsstar as ebills_star
from etl.star import etl_contract as etlcontract
from etl.star import etl_account as financialsale
from etl.base.singleton import singleton
from etl.base.conf import Config,DSN,USER,PASSWD
from etl.star.update import insert_fbalance_cancel as fbalance
from etl.star.update import update_loan_yearpdt as loanyearpdt
from etl.star.update import update_balance_manage_load as manage_id 
from etl.star.update import update_contract_manage_load as contract_id 
from etl.star.update import update_credit_card_manage_load as credit_id 
from etl.star.update import update_hook as updatehook
import etl.star.update.update_hook_balance as uhb
from etl.star.report import dep as dep
from etl.star.report import dep_month as dep_month
from etl.star.report import loan as loan
from etl.star.report import ebank as ebank
from etl.star.report import creditcard as creditcard
from etl.star.report import report_init as reportinit
from etl.star.report import posatm as posatm 
from etl.star.report import insert as insert 
from etl.star.report import cny as cny 
from etl.star.dwhis import  hook_back
from etl.star.model import EBILLS_HOOK_ALL as ebills_hook 

path.append(r'/home/dsadm/bin')

condecimal = getcontext()
tfile = "/tmp/balance_manage_id.del"
loadfile = "/tmp/export_hook.sql"
load_sh = "/tmp/export_hook.sh"
logfile = "/tmp/export_hook.log"

def process_info():
    from etl.base.logger import info
    msg = os.popen("ps -ef|grep python|grep -v grep |grep -v gun|grep -v report_proxy|grep -v WebSphere ")
    for m in msg:
        info(u"当前执行的Python进程:\n%s\n"%(m))

def backup_files():
    petldate = Config().etldate
    if etl_task_check(petldate,"数据备份") == False: return 
    try:
        hook_back(Config().etldate)

        if  os.path.exists(loadfile):os.remove(loadfile)
        newfile = open(loadfile,'w')
        newfile.write("connect to %s user %s using %s;"%(DSN,USER,PASSWD))
        targetfile = "/home/develop/src/etl/star/update/bakhook/ACCOUNT_HOOK_%s_%s_ALL.del"%(Config().etldate,systime.strftime("%Y%m%d%H",systime.localtime()))
        export_sql = """\n export to %s of del modified by decplusblank datesiso select * from ydw.account_hook;"""%targetfile
        newfile.write(export_sql)
        targetfile = "/home/develop/src/etl/star/update/bakhook/CUST_HOOK_%s_%s_ALL.del"%(Config().etldate,systime.strftime("%Y%m%d%H",systime.localtime()))
        export_sql = """\n export to %s of del modified by decplusblank datesiso select * from ydw.cust_hook;"""%targetfile
        newfile.write(export_sql)
        newfile.write("\n terminate;")
        newfile.close()

        if  os.path.exists(load_sh):os.remove(load_sh)
        runbat = open(load_sh,'w')
        runbat.write("\n db2 -tvf %s"%loadfile)
        runbat.write("\n exit")
        runbat.close()

        os.system("sh "+ load_sh)
        etl_task_finish(petldate,"数据备份")
    except Exception as e:
        etl_task_finish(petldate,"数据备份","失败",str(e))
        traceback.print_exc()
        raise e

def etl_run(fun, msg, etldate):
    if etl_task_check(etldate,msg) == False: return 
    try:
        d1 = datetime.now()
        info("star %s :%s-%s "%(msg,str(etldate),datetime.now()))
        fun(etldate)
        info("end %s:%s-%s "%(msg,str(etldate),datetime.now()-d1))
        etl_task_finish(etldate,msg)
    except Exception as e:
        etl_task_finish(etldate,msg,"失败",str(e))
        traceback.print_exc()
        raise e

def etl_run2(fun, msg, startdate, etldate):
    if etl_task_check(etldate,msg) == False: return 
    try:
        d1 = datetime.now()
        info("star %s :%s-%s "%(msg,str(etldate),datetime.now()))
        fun(startdate, etldate)
        info("end %s:%s-%s "%(msg,str(etldate),datetime.now()-d1))
        etl_task_finish(etldate,msg)
    except Exception as e:
        etl_task_finish(etldate,msg,"失败",str(e))
        traceback.print_exc()
        raise e

def etl_run3(fun, msg, startdate , etldate, p1):
    if etl_task_check(etldate,msg) == False: return 
    try:
        d1 = datetime.now()
        info("star %s :%s-%s "%(msg,str(etldate),datetime.now()))
        fun(startdate, etldate, p1)
        info("end %s:%s-%s "%(msg,str(etldate),datetime.now()-d1))
        etl_task_finish(etldate,msg)
    except Exception as e:
        etl_task_finish(etldate,msg,"失败",str(e))
        traceback.print_exc()
        raise e


def call_sale_rela_proc(etldate):
    try :
        db = util.DBConnect()
        OUT_SQLCODE = 1
        OUT_MSG=''
        msg = db.cursor.callproc("P_D_SALE_MANAGE_RELA",[str(Config().etldate),OUT_SQLCODE,OUT_MSG])
        if msg[1]!= 0:
            print "error msg:%s"%msg[2]
            raise Exception("调用Manage失败")
        db.conn.commit()
    finally:
        db.closeDB()


def calc_sale_manage(etldate):
    """
    执行 分割d_manage 的存储过程
    """
    #info("star 执行 分割d_manage 的存储过程:%s-%s "%(str(etldate),datetime.now()-d1))
    print "分割d_manage 的存储过程:",etldate
    file=open('/tmp/runflag.txt','w')
    file.write('True')
    file.close()
    systime.sleep(180)                     #休眠等待分割完成
    file=open('/tmp/runok.txt','r')
    lines = file.readline()
    i=0
    while i<3:
        if 'OK' in lines:
            file=open('/tmp/runok.txt','w')
            file.write('True')
            file.close()
            break
        else:
            i=i+1
            systime.sleep(60)
    if i==3:
        print "over time =",datetime.now()-d1
        return False

    #info("end 执行 分割d_manage 的存储过程:%s-%s "%(str(etldate),datetime.now()-d1))

def update_hook_fun(etldate):
    """
    即时生效 
    """
    updatehook.run(etldate)

def update_hook_fun2(etldate):
    """
    更新录入已审批状态以及hook表中的余额和积数,处理hook表中错误的数据
    """
    print "update_hook_fun2 start"
    updatehook.syn_hook_batch_id(etldate)
    updatehook.merge_cust_hook_percentage('存款')   #转移产生
    updatehook.merge_cust_hook_percentage('理财')
    updatehook.merge_account_hook_percentage()
    updatehook.delete_cust_no_first()
    uhb.update_balance(int(etldate))
    print "update_hook_fun2 finished"

def update_sql():
    try:
        db = util.DBConnect()
        print "DELETE D_AC_MAP"
        sql_d = """
        DELETE FROM D_AC_MAP
        """
        db.cursor.execute(sql_d)
        db.conn.commit()
        print "INSERT D_AC_MAP"
        sql_i = """
        INSERT INTO D_AC_MAP
        SELECT  DISTINCT A.ACID,A.SUBJECT_CODE,A.SUBJ_CLASS,A.SUBJ_TYPE FROM D_ACCOUNT_TYPE A
        WHERE A.ACID IS NOT NULL
        """
        db.cursor.execute(sql_i)
        db.conn.commit()
        print "INSERT D_AC_MAP OK"
    finally:
        db.closeDB()

def get_star_day():
    try:
        fixseq.sequence()
        db = util.DBConnect()
        sql="select py_date_id,date_id from p_etl_date"
        db.cursor.execute(sql)
        row = db.cursor.fetchall()
        pyday = int(row[0][0])
        etlday = int(row[0][1])
        print pyday,etlday
        if pyday >= etlday:
            msg = "当前PyEtl已跑到%d日，终止ETL调度任务"%( pyday ) 
            info(msg)
            raise Exception(msg)
        else:
            #return util.daycalc(pyday,1)
            return pyday
    finally:
        db.closeDB()

def get_last_day():
    file=open('rundate.txt','r')
    lines = file.readline()
    file.close()
    if len(lines) > 1:
        lastday = int (lines)
        print "last run date is :",lastday
    else:
        lastday = 18991231
    return lastday

def update_py_date(etldate):
    try:
        db=util.DBConnect()
        etldate = util.daycalc(etldate,1)
        next_date = util.daycalc(etldate,1)
        sql="""
        UPDATE YDW.P_ETL_DATE SET  PY_DATE_ID=?, PY_NEXT_DATE_ID=?  WHERE  JOB_SEQ =1
        """
        db.cursor.execute(sql,int(etldate),int(next_date))
        db.conn.commit()
    finally:
        db.closeDB()

def etl_task_finish(etldate,name, status="成功", msg="结束"):
    process_info()
    try:
        db=util.DBConnect()
        sql="select * from p_etl_task where date_id=? and task_name = ? "
        db.cursor.execute(sql,int(etldate),name)
        rows = db.cursor.fetchall()
        if len(rows) > 1 :
            raise Exception("任务名不能重复")

        if len(rows) == 0  :
            raise Exception("任务没有启动")
        else:
            qstatus = rows[0][0]
            if qstatus  == "成功" : 
                raise Exception("任务已完成")
            else:
                s = str(datetime.now())
                usql = "update p_etl_task set status = ?, msg = ? ,end_time = ?  where date_id=? and task_name = ? "
                db.cursor.execute(usql, status, msg, s,int(etldate), name)
                db.conn.commit()
            return True
    finally:
        db.closeDB()

def etl_task_check(etldate,name):
    try:
        db=util.DBConnect()
        sql="select status from p_etl_task where date_id=? and task_name = ? "
        db.cursor.execute(sql,int(etldate),name)
        rows = db.cursor.fetchall()
        if len(rows) > 1 :
            raise Exception("任务名不能重复")

        if len(rows) == 0  :
            insertsql = "insert into p_etl_task(date_id,task_name,status,start_time) values (?,?,?,?)"
            s = str(datetime.now())
            db.cursor.execute(insertsql, int(etldate), name, "启动", s)
            db.conn.commit()
            process_info()
        else:
            status = rows[0][0]
            process_info()
            if status  == "成功" : 
                nn = "%s已完成，跳过该任务"%(name)
                print nn
                info(nn)
                return False
            else:
                dsql = "delete from  p_etl_task where date_id=? and task_name = ? "
                db.cursor.execute(dsql, int(etldate), name)
                s = str(datetime.now())
                insertsql = "insert into p_etl_task(date_id,task_name,status,start_time) values (?,?,?,?)"
                db.cursor.execute(insertsql, int(etldate), name, "启动", s)
                db.conn.commit()
            return True
    finally:
        db.closeDB()

def run2(etldate):
    d1=datetime.now()
    etl_run(update_hook_fun, "即时生效", etldate)
    etl_run3(etlpeople.starrun, "更新客户信息etl_people", etldate, etldate, 'OCR')
    etl_run3(financialsale.runstar, "处理理财数据,承兑汇票,核销清单,逾期还款清单", etldate, etldate, 'FTBHB')
    etl_run2(etlcontract.run_etl, "处理丰收e支付、贷款合同、支付宝快捷支付和信用卡不良", etldate, etldate)
    etl_run(ccrd_star.starrun, "福农卡相关", etldate)
    etl_run(updatehook.input_pass, "录入审批当天生效,应该在自动挂钩前", etldate)
    #etl_run3(etlhook.starun, "新增挂钩关系etl_hook2", etldate, etldate, None)
    #调整挂钩比例挂钩程序
    etl_run(hookstar.starun, "新增挂钩,自动挂钩关系etl_hook2", etldate)
    etl_run2(fbalance.insert_close, "补齐f_balance销户的存款账号1", etldate, etldate)
    etl_run2(insert.man_dep, "补齐f_balance销户的存款账号2", etldate, etldate)
    etl_run2(loanyearpdt.update_yearpdt, "更新贷款year_pdt字段", etldate, etldate)
    etl_run(manage_id.starrun, "存贷款等manage_id", etldate)
    etl_run(contract_id.starrun, "处理电子银行相关manage_id", etldate)
    etl_run(credit_id.starrun, "信用卡credict_manage_id", etldate)
    etl_run(call_sale_rela_proc, "call_sale_rela_proc", etldate)
    #etl_run(calc_sale_manage, "执行分割d_manage 的存储过程", etldate)
    etl_run(update_hook_fun2, "更新录入已审批状态以及月初移交生效", etldate)

    if etldate%100 == 8:
        ldate=int(util.daycalc(etldate,0-etldate%100))
        ldate=int(util.daycalc(ldate,1-ldate%100))
        this_month_end = int(util.daycalc(etldate,1))
        last_one_day =int(util.daycalc(etldate,-1))
    else:
        ldate=int(util.daycalc(etldate,1-etldate%100))
        last_one_day =int(util.daycalc(etldate,-1))
        last_month_end = int(util.daycalc(ldate,-1))
        #ldate=etldate
        wady,monthRange = calendar.monthrange(int(str(etldate)[0:4]),int(str(etldate)[4:6]))
        this_month_end = int(util.daycalc(ldate,monthRange-1))

    print last_one_day,this_month_end,last_month_end
    etl_run2(reportinit.report_init, "初始化指标报表人员信息", ldate, etldate)
    etl_run(dep_month.sum_dep_report, "客户经理存款指标报表-按月", etldate)
    etl_run2(dep.man_dep, "客户经理存款指标报表", ldate, etldate)
    etl_run2(loan.man_loan, "客户经理贷款指标报表", ldate, etldate)
    etl_run2(ebank.man_dep, "客户经理其他指标报表", ldate, etldate)
    etl_run2(creditcard.man_creditcard, "客户经理信用卡指标报表", ldate, etldate)
    etl_run2(cny.cny, "外币折人名币", etldate, etldate)
    etl_run3(ebills_hook.mergeods, "国际业务每天汇全量", last_one_day, etldate, 'EBILLS')
    etl_run(ebills_star.starrun, "国际业务详情", etldate)
    etl_run(ods_load.starrun, "ods全量等", etldate)
    if int(etldate) == this_month_end:
        etl_run3(financialsale.runstar, "国际业务结算量按月客户", ldate, etldate, 'CORP')
        print '国际业务结算量按月客户'
    update_sql()

    fixseq.sequence()
    process_info()

def run(etldate):
    try:
        run2(etldate)
    except Exception as e:
        traceback.print_exc()
        raise e

if __name__=='__main__':
    process_info()
    etlday = get_star_day() #得到开始时间
    etlday = int(etlday)
    Config().etldate = etlday
    Config().stretldate = util.tostrdate(etlday)
    msg = "**********************start run py etl :%d******************************"%(etlday)
    info(msg)
    print msg
    backup_files() #跑之前先备份ACCOUNT_HOOK 和CUST_HOOK表
    run(etlday)
    msg = "**********************finish run py etl :%d******************************"%(etlday)
    info(msg)
    print msg
    update_py_date(etlday)
