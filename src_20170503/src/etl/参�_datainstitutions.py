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
	
class Datainstitutions():
	def __init__(self,etldate=None):
		self.db =util.DBConnect()
		self.etldate=etldate
		self.stretldate =util.tostrdate(self.etldate) 
		self.para=util.get_common_parameter(self.db)
		if etldate is not None : self.para['TJRQ']=etldate
	'''
	机构存款年积数
	''' 
	def jgcknjs(self):
		self.delete_jgzb_row(u'机构存款年积数')
		#TODO科目暂时这么写	
		sql =u'''
		select %s  DATE_ID,third_org_code ,'机构存款年积数' ZBLX,sum(f.credit_balance*0.01) je1,days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1 je2
from  v_jgc_jghz f
where   f.account_classify='G'  
  and  subj_code in ('2001','2002','2003','2004','2005','2006','2007','2011','2014','2017')
  and   f.credit_balance !=0  
  and f.date_id>=substr(%s,1,4)||'0101'
  and f.date_id<=%s
group by third_org_code 
	'''%(self.para['TJRQ'],self.para['TJRQ'],self.para['TJQSRQ'],self.para['TJRQ'],self.para['TJRQ'])			

		self.insert_jgzb_row(sql)




	"""
	机构存款余额
	"""
	def jgckye(self):
		self.delete_jgzb_row(u"机构存款余额")	
		sql2=u"""
		select %s DATE_ID,third_org_code,'机构存款余额' ZBLX,sum(f.credit_balance*0.01) je1,days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1 je2
from  v_jgc_jghz f
where   f.account_classify='G'  
  and  SUBJ_CODE in ('2001','2002','2003','2004','2005','2006','2007','2011','2014','2017')
  and   f.credit_balance !=0  
  and f.date_id=%s
group by third_org_code
		"""%(self.para['TJRQ'],self.para['TJRQ'],self.para['TJQSRQ'],self.para['TJRQ'])	


		self.insert_jgzb_row(sql2)




	"""
	机构贷款年积数
	"""
	def jgdknjs(self):
                self.delete_jgzb_row(u"机构贷款年积数")
		#TODO科目暂时这么写     
                sql =u'''
	select %s DATE_ID,third_org_code,'机构贷款年积数' ZBLX,sum(f.debit_balance-(f.credit_balance))*0.01 je1,days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1 je2
from  v_jgc_jghz f
where f.account_classify='G'  
 and f.subj_code in ('1301','1302','1303','1304','1305','1306')
and (f.credit_balance!=0 or f.debit_balance!=0)
  and f.date_id>=%s
  and f.date_id<=%s
group by third_org_code 
        '''%(self.para['TJRQ'],self.para['TJRQ'],self.para['TJQSRQ'],self.para['TJQSRQ'],self.para['TJRQ'])
		self.insert_jgzb_row(sql)


	"""
	机构贷款余额
	"""
	def jgdkye(self):
		self.delete_jgzb_row(u"机构贷款余额")
                sql2=u"""
		select %s DATE_ID,third_org_code,'机构贷款余额' ZBLX,sum(f.debit_balance-(f.credit_balance)*-1)*0.01 je1,days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1 je2
from v_jgc_jghz f
where date_id=%s 
and f.account_classify='G'
and f.subj_code in ('1301','1302','1303','1304','1305','1306')
and (f.credit_balance!=0 or f.debit_balance!=0)
group by f.third_org_code

                """%(self.para['TJRQ'],self.para['TJRQ'],self.para['TJQSRQ'],self.para['TJRQ'])
		self.insert_jgzb_row(sql2)

	def jgdcbckye(self):
		self.delete_jgzb_row(u"机构低成本存款余额")
		sql=u"""
		select %s DATE_ID,third_org_code,'机构低成本存款余额' ZBLX,sum(f.credit_balance*0.01) je1,days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1 je2
from  v_jgc_jghz f
where subj_code in ('200100','20020101','20020102','20020103','200301','200302','20040101','20040102','20040103','20040201','20040301','20040401','20040701','20050101','2005010201','2005010202','2005010203','20050201','2005020201','2005020202','2005020203','2005020301','2005020401','2005020501')
  and f.credit_balance !=0  
  and f.date_id=%s
group by third_org_code,DATE_ID
with ur
		"""%(self.para['TJRQ'],self.para['TJRQ'],self.para['TJQSRQ'],self.para['TJRQ'])
		self.insert_jgzb_row(sql)

	def jgdgdkhs(self):
		self.delete_jgzb_row(u"机构对公贷款户数")
		sql=u"""
		select %s DATE_ID,third_org_code ,'机构对公贷款户数' ZBLX,count(1) je1,days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1 je2
from  M_CUST_BALANCE c
where   pe_flag =  '1'
  and c.date_id=%s
group by third_org_code
		"""%(self.para["TJRQ"],self.para["TJRQ"],self.para["TJQSRQ"],self.para["TJRQ"])
		self.insert_jgzb_row(sql)

	def jgdsdkhs(self):
		self.delete_jgzb_row(u"机构对私贷款户数")
		sql=u"""
		select %s DATE_ID,third_org_code,'机构对私贷款户数' ZBLX,count(1) je1,days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1 je2
from  M_CUST_BALANCE c
where   pe_flag =  '2'
  and c.date_id=%s
group by third_org_code
		"""%(self.para['TJRQ'],self.para["TJRQ"],self.para['TJQSRQ'],self.para['TJRQ'])
		self.insert_jgzb_row(sql)


	def jgwjblje(self):
		self.delete_jgzb_row(u"机构不良贷款余额")
		sql=u"""
		select  %s DATE_ID, third_org_code,'机构不良贷款余额' ZBLX,sum(balance)*0.01 je1,0 je2
from m_loan_five where date_id =%s  
and loan_five in ('可疑','损失','次级')
group by  third_org_code
		"""%(self.para['TJRQ'],self.para['TJRQ'])
		self.insert_jgzb_row(sql)

	def bnwbldk(self):
		self.delete_jgzb_row(u'表内外不良贷款')
		sql=u"""
		select  %s  DATE_ID, third_org_code,'表内外不良贷款' ZBLX,sum(debit_balance-(credit_balance)*-1) *0.01 je1,0 je2
from v_jgc_jghz  f 
where  account_classify='G'
        and f.date_id=%s 
        and subj_code in ('131','132','116')
group by third_org_code
order by 1

		"""%(self.para['TJRQ'],self.para['TJRQ'])#116无
		self.insert_jgzb_row(sql)
	

	def jgjnknkks(self):
		self.delete_jgzb_row(u'机构借记卡年开卡数')#20151231到20160216无借记卡开卡
		sql=u"""
		select %s DATE_ID,org_code ORG_CODE,'机构借记卡年开卡数' ZBLX,sum(num) je1,0 je2
from  m_jgc_card m
where  card_type='借记卡' and OWNER_FLAG='主卡' and ROW_STATUS='--'  and   OPEN_DATE<=%s 
and (CLOSE_DATE>%s  or CLOSE_DATE=0 or CLOSE_DATE=18991231) and OPEN_DATE>= %s 
and date_id = %s
group by org_code
with ur
		"""%(self.para['TJRQ'],self.para['TJRQ'],self.para['TJRQ'],self.para['TJQSRQ'],self.para['TJRQ'])
		self.insert_jgzb_row(sql)

	def jgydkclks(self):
		self.delete_jgzb_row(u'机构借记卡存量卡数')
		sql=u"""
		select %s DATE_ID,org_code ORG_CODE,'机构借记卡存量卡数' ZBLX,sum(num) je1,0 je2
from  m_jgc_card m
where  card_type='借记卡' and OWNER_FLAG='主卡' and m.ROW_STATUS ='--'
and date_id = %s
group by org_code
with ur
		"""%(self.para['TJRQ'],self.para['TJRQ'])
		self.insert_jgzb_row(sql)

	def yhkhkl(self):#银行卡活卡率
		sql1=u"""
		select org_code ,count(1)*1.0 card_num, %s  DATE_ID,'活卡率' ZBLX
from D_CONTRACT dc 
inner join f_contract f on dc.id = f.contract_id and date_id = %s
inner join d_contract_status ds on ds.id = f.contract_status_id and ds.ROW_STATUS = '--' and ds.owner_flag ='主卡' 
where dc.contract_classify = 'C'
group by org_code
		"""%(self.para['TJRQ'],self.para['TJRQ'])#活卡率
		sql2=u"""
select a.org_code,count(1)*1.0 live_card
from(
select  dc.main_account_no,dc.org_code,sum(TRAN_NUM) tran_num
from D_CONTRACT dc 
inner join  m_account_tran_num m on  m.contract_id= dc.id
where dc.contract_classify = 'C' and  dc.contract_status ='--' and dc.owner_flag ='主卡'
and m.date_id>=%s and  m.date_id<=%s
group by dc.org_code,dc.main_account_no
having sum(TRAN_NUM)>=4
) a
group by  a.org_code
		"""%(self.para['TJQSRQ'],self.para['TJRQ'])#机构活卡数
		sql=u"""
		select live_card,card_num,h.org_code,date_id,zblx 
		from (%s) as h 
		inner join (%s) as j
		on h.org_code=j.org_code
		"""%(sql1,sql2)#连接查询
		sql=sql.encode('gb2312')
		self.db.cursor.execute(sql)
		row=self.db.cursor.fetchone()
		rs=[]
		while row:
			je1=row[0]/row[1]
			je2=0
			rs.append((row[3],row[2],row[4],je1,je2))
			row=self.db.cursor.fetchone()
		self.insert_update_yhkhkl(rs)

	def insert_update_yhkhkl(self,rs):
		insert_1=[]
		update_1=[]
		sql=u"""
		select * from t_jgc_jgzb where date_id=? and org_code=? and zblx=?
		"""
		insert_sql=u"""
		insert into t_jgc_jgzb (date_id,org_code,zblx,je1,je2)
		values(?,?,?,?,?)
		"""
		update_sql=u"""
		update t_jgc_jgzb set je1=?,je2=? 
		where date_id=? and org_code=? and zblx=?
		"""
		for r in rs:
			self.db.cursor.execute(sql,r[0],r[1],r[2])
			row=self.db.cursor.fetchone()
			if row is None:
				insert_1.append(r)
			else:
				update_1.append((r[3],r[4],r[0],r[1],r[2]))
		if len(insert_1)>0:
			self.db.cursor.executemany(insert_sql,insert_1)
			self.db.conn.commit()
		if len(update_1)>0:
			self.db.cursor.executemany(update_sql,update_1)
			self.db.conn.commit()


	def delete_jgzb_row(self,zblx):
		sql="""
			delete from t_jgc_jgzb where zblx='%s' and date_id =%s  
			""" %(zblx.encode('gb2312'),self.para['TJRQ'])
		self.db.cursor.execute(sql)
		self.db.conn.commit()
		
	
	def insert_jgzb_row(self,sql2):
		sql=sql2.encode('gb2312')
		self.db.cursor.execute(sql)
		row= self.db.cursor.fetchone()
		rs=[]
		while row:
			rs.append((int(row[0]),str(row[1]),str(row[2]),float(str(row[3])),float(str(row[4]))))
			row=self.db.cursor.fetchone()
		insert_sql=""" 
		insert into t_jgc_jgzb (date_id,org_code,zblx,je1,je2)
		values (?,?,?,?,?)
		"""
		self.db.cursor.executemany(insert_sql,rs)
		self.db.conn.commit()

	 
	def run_jgsjhz(self):
		try :
			self.jgcknjs()#机构存款年积数
			
			self.jgckye()#机构存款余额
			self.jgdknjs()#机构贷款年积数
			self.jgdkye()#机构贷款余额
			self.jgdcbckye()#机构低成本存款余额 （应从业务总账中去找对应业务类型的存款）
			self.jgdgdkhs()#机构对公贷款户数
			self.jgdsdkhs()#机构对私贷款户数
			#self.cklxsr()#贷款利息收入 未写
			self.jgwjblje()#机构五级不良金额
			self.bnwbldk()#表内外不良贷款
			self.jgjnknkks()#机构借记卡年开卡数
			self.jgydkclks()#机构借记卡存量卡数
			self.yhkhkl()#银行卡活卡率
			self.db.conn.commit()

		finally :
			self.db.closeDB()
	
	def run(self):
		self.run_jgsjhz()
	






"""
机构数据汇总
"""
if __name__ == "__main__":
	arglen=len(sys.argv)
	if arglen  == 2:
		Datainstitutions(sys.argv[1]).run()
	else :
		print "please input python jgsjhz.py YYYYMMDD "




