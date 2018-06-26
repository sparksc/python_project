# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
import DB2  

import etl.star.util as util
from etl.star.conf import Config

def calc_target( db,detail_id,factscore,flag):
	sql="select weight,target from PE_CONTRACT_DETAIL where id = ? "
	db.cursor.execute(sql,detail_id)
	row=db.cursor.fetchone()
	weight= row[0] if row is not None else 0 
	aimscore= row[1] if row is not None else 0 
	if  weight is None or aimscore is None:
		return False
	if factscore * 100 < 60.0 * aimscore:
		return 0
	else:
		if flag == 1:
			score = 100.0 * factscore / aimscore * weight
		elif flag == 2:
			if factscore * 100 > 110 * aimscore:
				score = 1.1 * weight * 100
			else:
				score = 100.0 * factscore / aimscore * weight
		return score
def balancesql(date,ZBLX,org_code):
	db = util.DBConnect()
	sql="SELECT * FROM t_jgc_jgzb WHERE DATE_ID = ? AND ZBLX = ?  AND ORG_CODE = ? "
	db.cursor.execute(sql,date,ZBLX.encode('gb2312'),org_code)
        row=db.cursor.fetchone()
	return row

def getlastdate(thisdate,pei_freq):
	if pei_freq == 'year':
		thisyear = str(thisdate)[0:4]
		lastyear = str(int(thisyear)-1) + '1231'
		lastdate = int(lastyear)
	elif pei_freq == 'quarter':
		flag = int(str(thisdate)[4:6]) 
		if  flag <= 12 and flag >= 10:
			lastdate = str(thisdate)[0:4] + '0930'
			lastdate = int(lastdate)
		elif flag <= 9 and flag >= 7:
			lastdate = str(thisdate)[0:4] + '0630'
			lastdate = int(lastdate)
		elif flag <= 6 and flag >= 4:
			lastdate = str(thisdate)[0:4] + '0331'
			lastdate = int(lastdate)
		else:
			thisyear = str(thisdate)[0:4]
                	lastyear = str(int(thisyear-1)) + '1231'
                	lastdate = int(lastyear)
	else:
		thisyear = int(str(thisdate)[0:4])
		thismonth = int(str(thisdate)[4:6])
		if thismonth in [5,7,10]:
			lastdate = str(thisdate)[0:4] + '0' + (thismonth-1) +'30'
		elif thismonth in [2,4,6,8,9]:
			lastdate = str(thisdate)[0:4] + '0' + (thismonth-1) +'31'
		elif thsimonth ==11:
			lastdate = str(thisdate)[0:4] + '1031'
		elif thsimonth ==12:
			lastdate = str(thisdate)[0:4] + '1130'
		elif thsimonth ==1:
			lastdate = str(thisdate)[0:4] + '1231'
		elif thsimonth ==3:
			if thisyear%4==0 and thisyear%100!=0 :
				lastdate = str(thisdate)[0:4] + '0229'
			else :
				lastdate = str(thisdate)[0:4] + '0228'
	return lastdate
def getdatesource_base(datetime1,datetime2,this_zblx,last_zblx,org_code):
	row1 = balancesql(datetime1,this_zblx,org_code)
	row2 = balancesql(datetime2,last_zblx,org_code)
	if row1 is None or row2 is None:
		return (False,False)
	else:
		return (row1,row2)
def qualitative(db,etldate,detail_id):
	thisdate = etldate
	sql = """
	select fact,weight from PE_CONTRACT_DETAIL where id = ?
	""" 
	db.cursor.execute(sql,detail_id)
	row=db.cursor.fetchone()
	weight = row[1] if row is not None else 0 
	fact = row[0] if row is not None else 0 
	if row[0] is not None and row[1] is not None:
		score = weight * fact
	else:
		return (False,False)
	return (score,fact)
	
def depositadd(db,org_code,etldate,detail_id,pei_freq):#存款净增
	thisyeardate = etldate
	lastdate = getlastdate(thisyeardate,pei_freq)
	(row1,row2)=getdatesource_base(thisyeardate,lastdate,u'机构存款余额',u'机构存款余额',org_code)
	if row1 == False or row2 == False:
		return (False,False)
	else:
		thisyearbalance = row1[3]
		lastyearbalance = row2[3]
	factbalance = thisyearbalance-lastyearbalance
	score = calc_target(db,detail_id,factbalance,1)
	return (score,factbalance)
def avg_daily_dep_add(db,org_code,etldate,detail_id,pei_freq):#日均存款增加额
	thisyeardate = etldate
	lastdate = getlastdate(thisyeardate,pei_freq)
	(row1,row2)=getdatesource_base(thisyeardate,lastdate,u'机构存款年积数',u'机构存款年积数',org_code)
	if row1 == False or row2 == False:
		return (False,False)
	else:
		thisyearbalance = row1[3]*1.0/row1[4]
		lastyearbalance = row2[3]*1.0/row2[4]
	factbalance = thisyearbalance-lastyearbalance
	score = calc_target(db,detail_id,factbalance,1)
	return (score,factbalance)
def lowcost_add(db,org_code,etldate,detail_id,pei_freq):#低成本存款净增
	thisyeardate = etldate
	lastdate = getlastdate(thisyeardate,pei_freq)
	(row1,row2)=getdatesource_base(thisyeardate,lastdate,u'机构低成本存款余额',u'机构低成本存款余额',org_code)
	if row1 == False or row2 == False:
		return (False,False)
	else:
		thisyearbalance = row1[3]
		lastyearbalance = row2[3]
	factbalance = thisyearbalance-lastyearbalance
	score = calc_target(db,detail_id,factbalance,1)
	return (score,factbalance)
def avg_daily_loan_add(db,org_code,etldate,detail_id,pei_freq):#日均贷款增加额
	thisyeardate = etldate
	lastdate = getlastdate(thisyeardate,pei_freq)
	(row1,row2)=getdatesource_base(thisyeardate,lastdate,u'机构贷款年积数',u'机构贷款年积数',org_code)
	if row1 == False or row2 == False:
		return (False,False)
	else:
		thisyearbalance = row1[3]*1.0/row1[4]
		lastyearbalance = row2[3]*1.0/row2[4]
	factbalance = thisyearbalance-lastyearbalance
	score = calc_target(db,detail_id,factbalance,1)
	return (score,factbalance)
def loanadd(db,org_code,etldate,detail_id,pei_freq):#贷款净增
	thisyeardate = etldate
	lastdate = getlastdate(thisyeardate,pei_freq)
	(row1,row2)=getdatesource_base(thisyeardate,lastdate,u'机构贷款余额',u'机构贷款余额',org_code)
	if row1 == False or row2 == False:
		return (False,False)
	else:
		thisyearbalance = row1[3]
		lastyearbalance = row2[3]
	factbalance = thisyearbalance-lastyearbalance
	score = calc_target(db,detail_id,factbalance,1)
	return (score,factbalance)
def personal_loan_num(db,org_code,etldate,detail_id,pei_freq):#个人贷款户数
	thisyeardate = etldate
	lastdate = getlastdate(thisyeardate,pei_freq)
	(row1,row2)=getdatesource_base(thisyeardate,lastdate,u'机构对私贷款户数',u'机构对私贷款户数',org_code)
	if row1 == False or row2 == False:
		return (False,False)
	else:
		thisyearbalance = row1[3]
		lastyearbalance = row2[3]
	factbalance = thisyearbalance-lastyearbalance
	score = calc_target(db,detail_id,factbalance,1)
	return (score,factbalance)
def business_loan_num(db,org_code,etldate,detail_id,pei_freq):#企业贷款户数
	thisyeardate = etldate
	lastdate = getlastdate(thisyeardate,pei_freq)
	(row1,row2)=getdatesource_base(thisyeardate,lastdate,u'机构对公贷款户数',u'机构对公贷款户数',org_code)
	if row1 == False or row2 == False:
		return (False,False)
	else:
		thisyearbalance = row1[3]
		lastyearbalance = row2[3]
	factbalance = thisyearbalance-lastyearbalance
	score = calc_target(db,detail_id,factbalance,1)
	return (score,factbalance)
def five_bad_rate(db,org_code,etldate,detail_id,pei_freq):#五级不良率
	"""
	1、年度的五级如何计算？
	2、计算后如何计算指标的分值？
	"""
	thisyeardate = etldate
        lastdate = getlastdate(thisyeardate,pei_freq)
	sql="select weight,target from PE_CONTRACT_DETAIL where id = ? "
	db.cursor.execute(sql,detail_id)
	row=db.cursor.fetchone()
	weight= row[0] if row is not None else 0 
	aimscore= row[1] if row is not None else 0 
	(row1,row2) = getdatesource_base(thisyeardate,lastdate,u'机构不良贷款余额',u'机构不良贷款余额',org_code)
	(row3,row4) = getdatesource_base(thisyeardate,lastdate,u'机构贷款余额',u'机构贷款余额',org_code)
	if row1 == False or row2 == False or row3 == False or row4==False:
		return (False,False)
	else:
		factbalance = (row2[3]-row1[3])/(row4[3]-row3[3])*100
		if  aimscore is not None:
			if factbalance *100 < aimscore *100:
				score = weight * 100
			else:
				score = 0
		else:
			return (False,False)
	return (score,factbalance)		
def bnw_bl_dk_xje(db,org_code,etldate,detail_id,pei_freq):#表内外不良贷款下降额
	thisyeardate = etldate
	lastdate = getlastdate(thisyeardate,pei_freq)
	(row1,row2)=getdatesource_base(thisyeardate,lastdate,u'表内外不良贷款',u'表内外不良贷款',org_code)
	if row1 == False or row2 == False:
		return (False,False)
	else:
		thisyearbalance = row1[3]
		lastyearbalance = row2[3]
	factbalance = lastyearbalance-thisyearbalance
	score = calc_target(db,detail_id,factbalance,2)
	return (score,factbalance)
def ydk_add(db,org_code,etldate,detail_id,pei_freq):#易贷卡增量
	thisyeardate = etldate
	row = balancesql(thisyeardate,u"机构易贷卡存量卡数",org_code)
	if row is None:
		return (False,False)
	else:
		factbalance = row[3]
	score = calc_target(db,detail_id,factbalance,2)
	return (score,factbalance)
def live_card_rate(db,org_code,etldate,detail_id,pei_freq):#活卡率
	thisyeardate = etldate
	sql="select weight,target from PE_CONTRACT_DETAIL where id = ? "
        db.cursor.execute(sql,detail_id)
        row=db.cursor.fetchone()
        weight= row[0] if row is not None else 0 
        aimscore= row[1] if row is not None else 0 
	row = balancesql(thisyeardate,u"活卡率",org_code)
	if row is None:
		return (False,False)
	else:
		factvalue = row[3]
	if factvalue *100 < aimscore * 100:
		score = 0
	else:
		score = 100 * weight
	return (score,factvalue)
def creditcard_add_num(db,org_code,etldate,detail_id,pei_freq):#信用卡增量
	return (None,None)
def phone_bank_moveaccount_rate(db,org_code,etldate,detail_id,pei_freq):#手机银行动户率
	thisyeardate = etldate
	sql="select weight,target from PE_CONTRACT_DETAIL where id = ? "
        db.cursor.execute(sql,detail_id)
        row=db.cursor.fetchone()
        weight= row[0] if row is not None else 0
        aimscore= row[1] if row is not None else 0
	row = balancesql(thisyeardate,u"总手机动户率",org_code)
	if row is None:
                return (False,False)
        else:
                factvalue = row[3]
        if factvalue *100 < aimscore * 100:
                score = 0
        else:
                score = 100 * weight
        return (score,factvalue)
	
	return (None,None)
def enjl_num(db,org_code,etldate,detail_id,pei_freq):#企业网银户数
	thisyeardate = etldate
	lastdate = getlastdate(thisyeardate,pei_freq)
	(row1,row2)=getdatesource_base(thisyeardate,lastdate,u'企业网银户数',u'企业网银户数',org_code)
	if row1 == False or row2 == False:
		return (False,False)
	else:
		thisyearbalance = row1[3]
		lastyearbalance = row2[3]
	factbalance = thisyearbalance - lastyearbalance
	score = calc_target(db,detail_id,factbalance,2)
	return (score,factbalance)
def phone_bank_num(db,org_code,etldate,detail_id,pei_freq):#手机银行户数
	thisyeardate = etldate
	lastdate = getlastdate(thisyeardate,pei_freq)
	(row1,row2)=getdatesource_base(thisyeardate,lastdate,u'手机银行户数',u'手机银行户数',org_code)
	if row1 == False or row2 == False:
		return (False,False)
	else:
		thisyearbalance = row1[3]
		lastyearbalance = row2[3]
	factbalance = thisyearbalance - lastyearbalance
	score = calc_target(db,detail_id,factbalance,2)
	return (score,factbalance)
def ebank_trade_rep_rate(db,org_code,etldate,detail_id,pei_freq):#电子银行替代率
	sql="select weight,target from PE_CONTRACT_DETAIL where id = ? "
        db.cursor.execute(sql,detail_id)
        row=db.cursor.fetchone()
        weight= row[0] if row is not None else 0 
        aimscore= row[1] if row is not None else 0 
	sql="SELECT A.DRRQ,A.JYTDL FROM T_JGC_JXKH_LR_QM A where A.JGBH=? and SJLX='6' and A.DRRQ = ?"
	drrq = util.tostrdate(etldate)	
	db.cursor.execute(sql,str(org_code),drrq)
	row=db.cursor.fetchone()
	if row is not None and aimscore is not None:
		if row[1]*100 < aimscore*100:
			score = 0
		else:
			score = 100*weight
	else:
		return (False,False)
	return (score,row[1])

def century_loan_interest_rate(db,org_code,etldate,detail_id,pei_freq):#百元贷款收息
	sql="select weight,target from PE_CONTRACT_DETAIL where id = ? "
        db.cursor.execute(sql,detail_id)
        row=db.cursor.fetchone()
        weight= row[0] if row is not None else 0 
        aimscore= row[1] if row is not None else 0 
	sql="SELECT A.DRRQ,A.BYTDL FROM T_JGC_JXKH_LR_QM A where A.JGBH=? and SJLX='7' and A.DRRQ = ?"
	drrq = util.tostrdate(etldate)	
	db.cursor.execute(sql,org_code,drrq)
	row=db.cursor.fetchone()
	if row is not None and aimscore is not None:
		if row[1]*100 < aimscore*100:
			score = 0
		else:
			score = 100*weight
	else:
		return (False,False)
	return (score,row[1])

def inoutsheet_interest(db,org_code,etldate,detail_id,pei_freq):#表内外应收利息
	return (None,None)
def loan_interest(db,org_code,etldate,detail_id,pei_freq):#贷款利息收入
	thisyeardate = etldate
	lastdate = getlastdate(thisyeardate,pei_freq)
	(row1,row2)=getdatesource_base(thisyeardate,lastdate,u'贷款利息收入',u'贷款利息收入',org_code)
	if row1 == False or row2 == False:
		return (False,False)
	else:
		thisyearbalance = row1[3]
		lastyearbalance = row2[3]
	factbalance = thisyearbalance - lastyearbalance
	score = calc_target(db,detail_id,factbalance,2)
	return (score,factbalance)

