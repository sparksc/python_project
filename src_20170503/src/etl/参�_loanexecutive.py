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
	


class  Loanexecutive():
	def __init__(self,etldate=None):
		self.db =util.DBConnect()
		self.etldate=etldate
		self.stretldate =util.tostrdate(self.etldate) 
		self.para=util.get_common_parameter(self.db)
		if etldate is not None : self.para['TJRQ']=etldate

	def lsdkzhhs(self):
		sql=u"""
		select sale_code,cust_no,sum(balance)*0.01 DK_CL_JS,1 je2
		from m_staff_loan
		where date_id =%s
		group by sale_code,cust_no
		order by 1
		"""%(self.para['JZZZRQ'])
		self.db.cursor.execute(sql)
		row = self.db.cursor.fetchone()
		if row is None : return 
		rs=[]
		while row:
			rj_sd = row[2]/row[3]
			f_hs0 = 0
			f_hs50 = 0
			if rj_sd <500000 and rj_sd>0:
				f_hs0 = 1
			elif rj_sd>=500000:
				f_hs50 = 1
			sjlx = u'年末时点'.encode('gb2312')
			rs.append((row[0],self.para['JZZZRQ'],f_hs0,f_hs50,sjlx))
			row = self.db.cursor.fetchone()
		d={}
		for i in rs :
			key = str(i[0])+'|'+str(i[1])+'|'+str(i[4])
			if  d.get(key) is None :
				d[key]={'f_hs0':i[2],'f_hs50':i[3]}
			else :
				d[key]['f_hs0']=d[key].get('f_hs0')+i[2]	
				d[key]['f_hs50']=d[key].get('f_hs50')+i[3]	
		sql2 =u"""
		select sale_code ,data_id,sjlx,hs0,hs50 from T_TMP_KHJL_DKHS
		""" 
		self.db.cursor.execute(sql2)
		old_row = self.db.cursor.fetchone()
		old_d={'1':'1'}
		while old_row:
			key=str(old_row[0])+'|'+str(old_row[1])+'|'+str(old_row[2])
			old_d[key]={'f_hs0':old_row[3],'f_hs50':old_row[4]}
			old_row=self.db.cursor.fetchone()
		for i in d:	
			
			if old_d.has_key(i):
				self.update_row(i,d)
			else :
				self.insert_row(i,d)						
		

	def get_cs(self,para_id):
		sql=u"""
		SELECT '1' AS CSZD,A.JE1,A.JE2 FROM T_JGC_JXKH_CS_QM A WHERE PARA_ID=%s
		"""%(para_id)
		self.db.cursor.execute(sql)
		row=self.db.cursor.fetchone()
		return row


#TODO 逻辑有错，可能需要修改
	def dkzhhs(self):
		sql =u"""
		select m.sale_code,m.cust_no,sum(m.balance)*0.01 DK_SD_JS,days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1 je2,'1' CSZD ,old_cust.DK_CL_JS
from m_staff_loan m
left join (
select cust_no,sum(balance) DK_CL_JS
                from m_staff_loan
                where date_id<=%s and date_id>%s
                group by cust_no
                order by 1) old_cust 
on m.cust_no =old_cust.cust_no

where m.date_id<=%s and m.date_id>=%s 
group by m.sale_code,m.cust_no,old_cust.DK_CL_JS
order by 1
		"""%(self.para['TJRQ'],self.para['TJQSRQ'],self.para['JZZZRQ'],self.para['JZQSRQ'],self.para['TJRQ'],self.para['TJQSRQ'])	
		self.db.cursor.execute(sql)
		row = self.db.cursor.fetchone()
		if row is None : return 
		rs=[]
		while row :
			rj_sd=row[2]/row[3]
			new_hs0=0
			new_hs50=0
			old_hs0=0
			old_hs50=0
			if rj_sd<500000 and rj_sd>0:
				if row[5] is not None and  row[5]>0:
					old_hs0=1
				else:
					new_hs0=1
			if rj_sd>=500000:
				if row[5] is not None and row[5]>0:
					old_hs50=1
				else:
					new_hs50=1
								
			sjlx=u"日均贷款管户数".encode('gb2312')
			rs.append((str(row[0]).strip(),str(row[1]).strip(),row[2],row[3],row[4],row[5],old_hs0,old_hs50,new_hs0,new_hs50,sjlx,self.para['TJRQ'],self.para['JNTS']))#贷款时点积数
			row=self.db.cursor.fetchone()
		
		d={}
		for i in rs :
			key = str(i[0])+'|'+str(i[11])+'|'+str(i[10])+'|'+str(i[4])+'|'+str(i[12])#客户经理|统计日期|数据类型|CSZD|年天数
			if  d.get(key) is None :
				d[key]={'old_hs0':i[6],'old_hs50':i[7],'new_hs0':i[8],'new_hs50':i[9]}
			else :
				d[key]['old_hs0']=d[key].get('old_hs0')+i[6]	
				d[key]['old_hs50']=d[key].get('old_hs50')+i[7]	
				d[key]['new_hs0']=d[key].get('new_hs0')+i[8]	
				d[key]['new_hs50']=d[key].get('new_hs50')+i[9]	

		sql2="""
			select sale_code,hs0 nmhs0,hs50 nmhs50
from T_TMP_KHJL_DKHS
where data_id=%s and sjlx ='%s'
order by 1
		"""%(self.para['JZZZRQ'],u'年末时点'.encode('gb2312'))	
		self.db.cursor.execute(sql2)
		row2=self.db.cursor.fetchone()
		rs2=[]
		if row2 is None : 
			rs2=[('1','1')]
		else :
			while row2:
				rs2.append((str(row2[0]).strip(),row2[1],row2[2]))
				row2=self.db.cursor.fetchone()
		
	
		for k in d:
			for r in rs2:
				sale_code=k.split('|')[0]
				if sale_code==r[0]:
					d[k]['nmhs0']=r[1]
					d[k]['nmhs50']=r[2]
				else :
					d[k]['nmhs0']=0
					d[k]['nmhs50']=0
		rs3=self.get_cs(7)#获得50万以下参数
		rs4=self.get_cs(8)#获得50万以上参数
		for k in d:
			d[k]['clxs0']=rs3[1]
			d[k]['zlxs0']=rs3[2]
			d[k]['clxs50']=rs4[1]
			d[k]['zlxs50']=rs4[2]
	
		for k in d:
			a=d[k]['old_hs0']-d[k]['nmhs0']
			b=d[k]['old_hs50']-d[k]['nmhs50']	
			jxxc=0
			if a<0:
				jxxc=(d[k]['new_hs0']+a)*d[k]['zlxs0']+d[k]['nmhs0']*d[k]['clxs0']
			else:
				jxxc=d[k]['new_hs0']*d[k]['zlxs0']+d[k]['old_hs0']*d[k]['clxs0']
			jxxc=jxxc/int(k.split('|')[4])
			jxxc2=0
			if(b<0):
				jxxc2=(d[k]['new_hs50']+b)*d[k]['clxs50']+d[k]['nmhs50']*d[k]['zlxs50']
			else :
				jxxc2=d[k]['new_hs50']*d[k]['clxs50']+d[k]['old_hs50']*d[k]['zlxs50']
			jxxc2=jxxc2/int(k.split('|')[4])
			d[k]['jxxc']=jxxc
			d[k]['jxxc2']=jxxc2
			#
			d[k]['sale_code']=k.split('|')[0]
			d[k]['tjrq']=k.split('|')[1]
			d[k]['sjlx']=k.split('|')[2]

		sql3 =u"""
		select sale_code ,data_id,sjlx,old_hs0,old_hs50,new_hs0,new_hs50,jxxc,jxxc2 from T_TMP_KHJL_DKHS
		""" 
		self.db.cursor.execute(sql3)
		old_row = self.db.cursor.fetchone()
		old_d={'1':'1'}
		while old_row:
			key=str(old_row[0])+'|'+str(old_row[1])+'|'+str(old_row[2])
			old_d[key]={
				'old_hs0':old_row[3],
				'old_hs50':old_row[4],
				'new_hs0':old_row[5],
				'new_hs50':old_row[6],
				'jxxc':old_row[7],
				'jxxc2':old_row[8]
				}
			old_row=self.db.cursor.fetchone()
		h={}
		for i in d :
			key = i.split('|')[0]+'|'+i.split('|')[1]+'|'+i.split('|')[2]
			h[key]=d[i]		

		for i in h:	
			
			if old_d.has_key(i):
				self.update_row2(i,h)
			else :
				self.insert_row2(i,h)					

			
	def update_row(self,key,d):
		l = key.split('|')
		sql='''
		update T_TMP_KHJL_DKHS set hs0=%s,hs50=%s where sale_code='%s' and data_id=%s and sjlx='%s'		
		'''%(d[key].get('f_hs0'),d[key].get('f_hs50'),l[0],l[1],l[2])		
		
		self.db.cursor.execute(sql)
		self.db.conn.commit()
		
	def update_row2(self,key,d):
		l = key.split('|')
		sql='''
		update T_TMP_KHJL_DKHS set old_hs0=%s,old_hs50=%s, new_hs0=%s,new_hs50=%s ,jxxc=%s,jxxc2=%s  where sale_code='%s' and data_id=%s and sjlx='%s'		
		'''%(d[key].get('old_hs0'),d[key].get('old_hs50'),d[key].get('new_hs0'),d[key].get('new_hs50'),d[key].get('jxxc'),d[key].get('jxxc2'),l[0],l[1],l[2])		
		
		self.db.cursor.execute(sql)
		self.db.conn.commit()
	

	def insert_row(self,key,d):
		l = key.split('|')
		sql="""
		insert into T_TMP_KHJL_DKHS (sale_code,data_id,sjlx,hs0,hs50) values('%s',%s,'%s',%s,%s)
		"""%(l[0],l[1],l[2],d[key].get('f_hs0'),d[key].get('f_hs50'))	
		self.db.cursor.execute(sql)
		self.db.conn.commit()
			 
			
	def insert_row2(self,key,d):
		l = key.split('|')
		sql="""
		insert into T_TMP_KHJL_DKHS (sale_code,data_id,sjlx,old_hs0,old_hs50,new_hs0,new_hs50,jxxc,jxxc2) values('%s',%s,'%s',%s,%s,%s,%s,%s,%s)
		"""%(l[0],l[1],l[2],d[key].get('old_hs0'),d[key].get('old_hs50'),d[key].get('new_hs0'),d[key].get('new_hs50'),d[key].get('jxxc'),d[key].get('jxxc2'))	
		self.db.cursor.execute(sql)
		self.db.conn.commit()
		
	def run_dkzhhs(self):
		try :
			self.lsdkzhhs()#历史贷款增户户数
			self.dkzhhs()#贷款增户户数	
			
			self.db.conn.commit()

		finally :
			self.db.closeDB()
	
	def run(self):
		self.run_dkzhhs()
	





"""
贷款增户户数统计`
"""
if __name__ == "__main__":
	arglen=len(sys.argv)
	if arglen  == 2:
		Loanexecutive(sys.argv[1]).run()
	else :
		print "please input python dkzhhs.py YYYYMMDD "




