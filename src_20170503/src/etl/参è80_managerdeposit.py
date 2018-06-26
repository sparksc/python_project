# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
import DB2  

from etl.star.logger import info,debug,error
import etl.star.util as util
from etl.star.conf import Config
	

class Managerdeposit():
	def __init__(self,etldate=None):
		self.db =util.DBConnect()
		self.etldate=etldate
		self.stretldate =util.tostrdate(self.etldate) 
		self.para=util.get_common_parameter(self.db)
		if etldate is not None : self.para['TJRQ']=etldate
	def khjlrjck(self):
		sql=u"""
        select trim(o.user_name) YGGH,trim(o.branch_code) JGBH,trim(o.branch_name) JGMC,trim(o.name) YGXM
        from V_USER_GROUP g
        inner join V_USER_ORG o on  g.user_name = o.user_name
        where group_id   in (1)
        order by 1
        with ur
		"""
		staff_rs=util.get_select_row(self.db,sql)#客户经理员工工号
		sql1="""
		select trim(sale_code) YYGH, sum(balance) zy_cl_js
from m_jgc_khzb
where date_id>=%s and  date_id<=%s and relaction_type ='%s'
group by sale_code
		"""%(self.para['JZQSRQ'],self.para['JZZZRQ'],u'存款管理'.encode('gb2312'))
		zy_ck_cl_js=util.get_select_row(self.db,sql1)#自营存款存量积数
		if zy_ck_cl_js is  None : zy_ck_cl_js=[('1','1')]
	
		sql2="""
		select trim(sale_code) YYGH, sum(balance) zy_sd_js
from m_jgc_khzb
where date_id>=%s and  date_id<=%s and relaction_type ='%s'
group by sale_code
		"""%(self.para['TJQSRQ'],self.para['TJRQ'],u'存款管理'.encode('gb2312'))
	 	zy_ck_sd_js=util.get_select_row(self.db,sql2)#自营存款时点积数
		if zy_ck_sd_js is  None : zy_ck_sd_js=[('1','1')]


		sql3="""
		select trim(sale_code) yggh , sum(balance) fp_cl_js
from m_jgc_khzb
where date_id>=%s and  date_id<=%s and relaction_type = '%s'
group by sale_code

		"""%(self.para['JZQSRQ'],self.para['JZZZRQ'],u"存款管理分配".encode('gb2312'))
		fp_cl_js=util.get_select_row(self.db,sql3)#分配存款存量积数
		if fp_cl_js is None : fp_cl_js=[('1','1')]
		sql4="""
		select trim(sale_code) yggh , sum(balance) fp_sd_js
from m_jgc_khzb
where date_id>%s and  date_id<=%s and relaction_type = '%s'
group by sale_code
		"""%(self.para['JZZZRQ'],self.para['TJRQ'],u"存款管理分配".encode('gb2312'))
		fp_sd_js=util.get_select_row(self.db,sql4)#分配存款时点积数
		if fp_sd_js is None : fp_sd_js=[('1','1')]
		sql5="""
		select trim(sale_code) yggh , sum(balance) ps_cl_js
from m_jgc_khzb
where date_id>=%s and  date_id<=%s and relaction_type = '%s'
group by sale_code
		"""%(self.para['JZQSRQ'],self.para['JZZZRQ'],u"派生存款".encode('gb2312'))	
		ps_cl_js=util.get_select_row(self.db,sql5)#派生存量积数
		if ps_cl_js is None : ps_cl_js=[('1','1')]
		sql6="""
		select trim(sale_code) yggh , sum(balance) ps_sd_js
from m_jgc_khzb
where date_id>%s and  date_id<=%s and relaction_type = '%s'
group by sale_code
		"""%(self.para['JZZZRQ'],self.para['TJRQ'],u"派生存款".encode('gb2312'))
		ps_sd_js=util.get_select_row(self.db,sql6)
		if ps_sd_js is None : ps_sd_js=[('1','1')]	


		rs=[]
		if staff_rs is None : 
			info('staff_rs is None')
			return 
		for col in staff_rs:
			d={}
			d['YGGH']=col[0]
			d['JGBH']=col[1]
			d['JGMC']=col[2]
			d['YGXM']=col[3]
			rs.append(d)
		
		for r in rs:
			
			for col in zy_ck_cl_js:
				if r.get('YGGH')==col[0]:
					r['ZY_CL_JS']=col[1]#存量积数	
					break
				else :
					r['ZY_CL_JS']=0					
			for col2 in zy_ck_sd_js:
				if r.get('YGGH')==col2[0]:#时点积数
					r['ZY_SD_JS']=col2[1]	
					break
				else :
					r['ZY_SD_JS']=0
			for col3 in  fp_cl_js :
				if r.get('YGGH')==col3[0]:
					r['FP_CL_JS']=col3[1]#分配存量积数
					break
				else :
					r['FP_CL_JS']=0

			for col4 in fp_sd_js :# 分配时点积数
				if r.get('YGGH')==col4[0]:
					r['FP_SD_JS']=col4[1]
					break
				else :
					r['FP_SD_JS']=0

			for col5 in ps_cl_js :
				if r.get('YGGH')==col5[0]:#派生存量积数
					r['PS_CL_JS']=col5[1]	
					break
				else :
					r['PS_CL_JS']=0


			for col6 in ps_sd_js :#派生时点积数
				if r.get('YGGH')==col6[0]:
					r['PS_SD_JS']=col6[1]
					break
				else :
					r['PS_SD_JS']=0

		rs1=[]
		for r in rs :
			rs=self.rj_js(r)#日均计算
			rs1.append(rs)	
		self.update_insert_zb(rs1)#导入t_jgc_jxkh_zb_qm	
		rs2=self.get_ck_cl_jx_xc()
		if rs2 is None : 
			info('jxkh_cs is None')	
			return
		
		for  r in rs1 :#数据
			for  j in rs2 : #绩效指标
				if  r['RJCKCL']>=j[0] and r['RJCKCL']<j[1]:
					r['XX']=j[0]
					r['SX']=j[1]
					r['JE1']=j[2]
					r['JE2']=j[3]
					r['PARA_ID']=j[4]
					r['CSZD']=j[5]	
					break
				else :
					r['XX']=0
					r['SX']=0
					r['JE1']=0
					r['JE2']=0
					r['PARA_ID']=0
					r['CSZD']=0	
		
		sql7=u"""
		SELECT '1' AS CSZD,A.XX,A.SX,A.JE1 FROM T_JGC_JXKH_CS_QM A WHERE PARA_ID=5
		"""
		ck_zl_jx=util.get_select_row(self.db,sql7)#存款增量绩效
		sql8=u"""
		SELECT '1' AS CSZD,A.XX,A.SX ,A.JE1,A.JE2 FROM T_JGC_JXKH_CS_QM A WHERE PARA_ID=6
		"""
		ck_zl_jx300=util.get_select_row(self.db,sql8)#存款增量绩效300万以上
		for r in rs1 :
			r['ZL_XX_0']=ck_zl_jx[0][1]
			r['ZL_SX_0']=ck_zl_jx[0][2]
			r['ZL_CS_02']=ck_zl_jx[0][3]
			r['ZL_XX_3']=ck_zl_jx300[0][1]
			r['ZL_SX_3']=ck_zl_jx300[0][2]
			r['ZL_CS_31']=ck_zl_jx300[0][3]
			r['ZL_CS_32']=ck_zl_jx300[0][4]

		rs3=self.jx_js(rs1)
		self.update_insert_jx(rs3)
	

	def update_insert_jx(self,rs):
		update_l=[]
		insert_l=[]
		sql=u"""
		select * from T_JGC_JXKH_JX_QM where YGGH=? and TJRQ=? and TJZQ=? and JGBH=? and KHLX=?
		"""
		for r in rs :
			self.db.cursor.execute(sql,(r['YGGH'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX']))
			row = self.db.cursor.fetchone()
			if row is None :
				insert_l.append((r['YGGH'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX'],r['JGMC'],r['YGXM'],r['JE1'],r['JE2']))

			else :
				update_l.append((r['JGMC'],r['YGXM'],r['JE1'],r['JE2'],r['YGGH'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX']))

			
		if len(insert_l)>0:
			self.insert_jx_db(insert_l)
		if len(update_l)>0:
			self.update_jx_db(update_l)	


	def insert_jx_db(self,r):
		sql=u"""
		insert into T_JGC_JXKH_JX_QM (YGGH,TJRQ,TJZQ,JGBH,KHLX,JGMC,YGXM,JE1,JE2) values(?,?,?,?,?,?,?,?,?)
		"""
		self.db.cursor.executemany(sql,r)
		self.db.conn.commit()
	def update_jx_db(self,r):
		sql=u"""
		update T_JGC_JXKH_JX_QM set JGMC=?,YGXM=?,JE1=?,JE2=? where YGGH=? and TJRQ=? and TJZQ=? and JGBH=? and KHLX=?
		"""			
		self.db.cursor.executemany(sql,r)
		self.db.conn.commit()		
	
	def jx_js(self,rs):
		for r in rs :
			ckrj_cljx = 0
			if r['PARA_ID'] !=45:
			    ckrj_cljx = r['JE1']*10000*r['ZBTS']

			else :
			    ckrj_cljx = r['JE1']*10000+(r['RJCKCL']-r['XX'])*r['JE2']*r['ZBTS'];


			#增量部分
			zy_zl_jx = 0;
			flag = 1;
			if r['ZY_ZL_RJ']<0:
				flag = -1
			if r['ZY_ZL_RJ']/10000<r['ZL_SX_0'] and  r['ZY_ZL_RJ']>r['ZL_XX_0']:
				zy_zl_jx=((r['ZY_ZL_RJ']/10000)*r['ZL_CS_02']*r['ZBTS'])*flag
			elif r['ZY_ZL_RJ']/10000>=r['ZL_XX_3'] :
				zy_zl_jx=((r['ZL_XX_3']*r['ZL_CS_31']+(r['ZY_ZL_RJ']/10000-r['ZL_XX_3'])*r['ZL_CS_32']))*r['ZBTS']*flag

			fp_zl_jx=0
			flag = 1
			if r['FP_ZL_RJ']<0:
				flag = -1 
			if r['FP_ZL_RJ']/10000<r['ZL_SX_0'] and  r['FP_ZL_RJ']>r['ZL_XX_0'] :
				zy_zl_jx=((r['FP_ZL_RJ']/10000)*r['ZL_CS_02']/2*r['ZBTS'])*flag
			elif (r['FP_ZL_RJ']/10000)>=r['ZL_XX_3']:
				zy_zl_jx=((r['ZL_XX_3']*r['ZL_CS_31']+(r['FP_ZL_RJ']/10000-r['ZL_XX_3'])*r['ZL_CS_32'])/2)*r['ZBTS']*flag

			ps_zl_jx=0
			flag = 1
			if r['FP_ZL_RJ']<0 :
				flag = -1;
			if r['PS_ZL_RJ']/10000<r['ZL_SX_0'] and  r['PS_ZL_RJ']>r['ZL_XX_0'] :
				zy_zl_jx=((r['PS_ZL_RJ']/10000)*r['ZL_CS_02']/2)*r['ZBTS']*flag
			elif r['PS_ZL_RJ']/10000>=r['ZL_XX_3'] :
				zy_zl_jx=((r['ZL_XX_3']*r['ZL_CS_31']+(r['PS_ZL_RJ']/10000-r['ZL_XX_3'])*r['ZL_CS_32'])/2)*r['ZBTS']*flag

			ckrj_zljx=ps_zl_jx+zy_zl_jx+fp_zl_jx
			r['CKRJ_CLJX']=ckrj_cljx
			r['CKRJ_ZLJX']=ckrj_zljx			
		return rs				


	def get_ck_cl_jx_xc(self):
		sql=u"""
		SELECT XX,SX,JE1,JE2,PARA_ID,'1' as cszd FROM T_JGC_JXKH_CS_QM WHERE CSLX=01
		"""
		self.db.cursor.execute(sql)
		row= self.db.cursor.fetchone()
		if row is None : return None
		rs=[]
		while row:
			rs.append((row[0],row[1],row[2],row[3],row[4],row[5]))
			row = self.db.cursor.fetchone()
		return rs	


	def update_insert_zb(self,rs1):
		sql=u"""
		select *  from T_JGC_JXKH_ZB_QM where YGGH=? and TJRQ=?
		and TJZQ=? and JGBH=? and KHLX=?
		"""	
		update_l=[]
		insert_l=[]
			
		for r in rs1:
			self.db.cursor.execute(sql,(r['YGGH'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX']))
			row=self.db.cursor.fetchone()
			if row is None :
				insert_l.append((r['YGGH'],r['ZY_CL_RJ'],r['PS_ZL_RJ'],r['PS_CL_RJ'],r['ZY_ZL_RJ'],r['TJRQ'],r['ZY_SD_RJ'],r['TJZQ'],r['KHLX'],r['YGXM'],r['JGBH'],r['JGMC'],r['FP_SD_RJ'],r['FP_CL_RJ'],r['FP_ZL_RJ']))

			else :
				update_l.append((r['ZY_CL_RJ'],r['PS_ZL_RJ'],r['PS_CL_RJ'],r['ZY_ZL_RJ'],r['ZY_SD_RJ'],r['YGXM'],r['JGMC'],r['FP_SD_RJ'],r['FP_CL_RJ'],r['FP_ZL_RJ'],r['YGGH'],r['TJRQ'],r['TJZQ'],r['JGBH'],r['KHLX']))
		if len(insert_l)>0:
			self.insert_zb_db(insert_l)

		if len(update_l)>0:
			self.update_zb_db(update_l)
					
			
	

	def insert_zb_db(self,r):
		sql=u"""
		insert into T_JGC_JXKH_ZB_QM (YGGH,JE1,JE4,JE3,JE2,TJRQ,JE35,TJZQ,KHLX,YGXM,JGBH,JGMC,JE40,JE41,JE42) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
		"""
		self.db.cursor.executemany(sql,r)
		self.db.conn.commit()
	def update_zb_db(self,r):
		sql=u"""
		update T_JGC_JXKH_ZB_QM set JE1=?,JE4=?,JE3=?,JE2=?,JE35=?,YGXM=?,JGMC=?,JE40=?,JE41=?,JE42=? where YGGH =? and TJRQ=? and TJZQ=? and JGBH=? and KHLX=?
		"""
		self.db.cursor.executemany(sql,r)
                self.db.conn.commit()
	



	def rj_js(self,rs):#日均计算
		TJZQ='1'
		KHLX = str(self.para['TJRQ'])[0:4]#YYYY
		TJRQ = self.stretldate#YYYY-MM-DD
		cldays = util.date_diff_days(self.para['JZQSRQ'],self.para['JZZZRQ'])#存量天数
		ZY_CL_RJ =int(rs['ZY_CL_JS'])/cldays
		#if(KHLX=='2016')
		#      ZY_CL_RJ = 0
		FP_CL_RJ =int(rs['FP_CL_JS'])/cldays
		PS_CL_RJ =int(rs['PS_CL_JS'])/cldays
		zldays = util.date_diff_days(self.para['JZZZRQ'],self.para['TJRQ'])-1#增量天数
		ZY_SD_RJ = int(rs['ZY_SD_JS'])/zldays
		FP_SD_RJ = int(rs['FP_SD_JS'])/zldays
		PS_SD_RJ = int(rs['PS_SD_JS'])/zldays
		ZY_ZL_RJ = int(ZY_SD_RJ)-int(ZY_CL_RJ)
		FP_ZL_RJ = int(FP_SD_RJ)-int(FP_CL_RJ)
		PS_ZL_RJ = int(PS_SD_RJ)-int(PS_CL_RJ)
		RJCKCL=(ZY_CL_RJ+FP_CL_RJ+PS_CL_RJ)/10000
		ZBTS = zldays/int(self.para["JNTS"])		
		rs['TJZQ']=TJZQ
		rs['KHLX']=KHLX
		rs['TJRQ']=TJRQ
		rs['ZY_CL_RJ']=ZY_CL_RJ
		rs['FP_CL_RJ']=FP_CL_RJ
		rs['PS_CL_RJ']=PS_CL_RJ
		rs['ZY_SD_RJ']=ZY_SD_RJ
		rs['FP_SD_RJ']=FP_SD_RJ
		rs['PS_SD_RJ']=PS_SD_RJ
		rs['ZY_ZL_RJ']=ZY_ZL_RJ
		rs['FP_ZL_RJ']=FP_ZL_RJ
		rs['PS_ZL_RJ']=PS_ZL_RJ
		rs['RJCKCL']=RJCKCL
		rs['ZBTS']=ZBTS
		return rs


	def run_khjlrjckyjj(self):
		try :
			self.khjlrjck()#客户经理日均存款与计价
			self.db.conn.commit()

		finally :
			self.db.closeDB()
	
	def run(self):
		self.run_khjlrjckyjj()
	



"""
客户经理日均存款与计价
"""
if __name__ == "__main__":
	arglen=len(sys.argv)
	if arglen  == 2:
		Managerdeposit(sys.argv[1]).run()
	else :
		print "please input python khjlrqckyjj.py YYYYMMDD "




