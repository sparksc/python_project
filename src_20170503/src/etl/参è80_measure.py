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
import etl.performance.measureutil as mutil

measures={
	u"存款净增":mutil.depositadd,   #存款净增
	u"日均存款增加额":mutil.avg_daily_dep_add, #日均存款增加额
	u"低成本存款净增":mutil.lowcost_add, #低成本存款净增
	u"日均贷款增加额":mutil.avg_daily_loan_add, #日均贷款增加额
	u"贷款净增":mutil.loanadd, #贷款净增
	u"个人贷款户数":mutil.personal_loan_num, # 个人贷款户数
	u"企业贷款户数":mutil.business_loan_num, # 企业贷款户数
	u"五级不良率":mutil.five_bad_rate, #五级不良率
	u"表内外不良贷款下降额":mutil.bnw_bl_dk_xje, #表内外不良贷款下降额
	u"易贷卡增量":mutil.ydk_add, #易贷卡增量
	u"活卡率":mutil.live_card_rate, #活卡率
	u"信用卡增量":mutil.creditcard_add_num, #信用卡增量
	u"手机银行动户率":mutil.phone_bank_moveaccount_rate, #手机银行动户率
	u"企业网银户数":mutil.enjl_num,#企业网银户数
	u"手机银行户数":mutil.phone_bank_num,#手机银行户数
	u"电子银行交易替代率":mutil.ebank_trade_rep_rate, #电子银行交易替代率
	u"百元贷款收息率":mutil.century_loan_interest_rate,#百元贷款收息率
	u"表内外应收利息":mutil.inoutsheet_interest, #表内外应收利息
	u"贷款利息收入":mutil.loan_interest, #贷款利息收入
		
}
	
def measure_calc(measurename,org_code,etldate,detail_id,pei_freq,meatype):
        db = util.DBConnect()
        try :
		if meatype == u'定性'.encode('gb2312') :
			(score,fact) =  mutil.qualitative(db,etldate,detail_id)
		else:
			fun = measures.get(measurename.decode('gb2312'))
			if fun is None :
				raise Exception(u"绩效指标未定义:%s"%(measurename.decode('gb2312')))
			if pei_freq  == u'年'.encode('gb2312') :
				(score,fact) = fun(db,org_code,etldate,detail_id,'year')
			else:
				(score,fact) = fun(db,org_code,etldate,detail_id,'quarter')
                usql = " update PE_CONTRACT_DETAIL d set d.score = ?,d.fact= ? where id = ?"		
		if (fact == False and isinstance(fact,bool)) or fact == None  or (score == False and isinstance(score,bool))  or score == None :
                	db.cursor.execute(usql,0.0,0.0,detail_id)
		else:	
                	db.cursor.execute(usql,score,fact,detail_id)
                db.conn.commit()
        finally :
                db.closeDB()

"""
查找合约的详细信息
PE_CONTRACT合约信息表
PE_CONTRACT_DETAIL 合约详细信息
PE_PEI_DEF  指标定义

""" 
def clac_contract_detail(db,etldate):
	sql = u"""
		select 
			def.name, c.pe_object,d.id,c.id,def.pei_freq,def.type
  		from PE_CONTRACT c
		inner join PE_CONTRACT_DETAIL d on d.contract_id = c.id
		inner join PE_PEI_DEF def on def.PEI_ID=d.pe_pei_id
 		--where   
			--def.type = '定量'
			--and pei_freq='年'
			--c.pe_object = '3409373113' and 
			--c.date_id=?
		 ORDER BY PE_OBJECT
	"""
	db.cursor.execute( sql.encode('gb2312') )
	row = db.cursor.fetchone()
	data = []
	while row :
		data.append( row )
		measure_calc( row[0],row[1],etldate,row[2],row[4],row[5])
		row = db.cursor.fetchone() 
	#db.conn.commit()

"""
计算绩效合约总分
"""
def clac_contract_scrore(db,etldate):
        db1 = util.DBConnect()
	sql="""
	select sum(d.score),p.id,def.PEI_FREQ from PE_CONTRACT_DETAIL d
   	inner join PE_CONTRACT p on d.contract_id = p.id 
   	inner join PE_PEI_DEF def on def.pei_id = d.pe_pei_id
   	group by p.id,def.PEI_FREQ
	"""
	upsql="""
	update PE_CONTRACT set score = ?,date = ? where id = ?
	"""
	db.cursor.execute(sql)
	row = db.cursor.fetchone()
	while row:
		score = row[0]	if row[0] is not None else 0
		date = util.tostrdate(etldate)
		pe_id = row[1]
		db1.cursor.execute( upsql,score,date,pe_id)
		row = db.cursor.fetchone()
	db1.conn.commit()
	db1.closeDB()
		
def measure_clacs(etldate):
	try :
		db = util.DBConnect()
		clac_contract_detail(db,etldate)
		clac_contract_scrore(db,etldate)
		db.conn.commit()
	finally :
		db.closeDB()

if __name__=='__main__':
	Config().etldate=20160214
	etldate = Config().etldate
	measure_clacs(etldate)
