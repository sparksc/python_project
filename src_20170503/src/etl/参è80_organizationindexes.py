# -*- coding:UTF-8 -*-
#!/bin/python
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random
from datetime import datetime,timedelta
from decimal import *

import etl.base.util as util
from etl.base.conf import Config
import DB2


"""
机构指标
"""
class Organizationindexes():
	def __init__(self,etldate=None):
                self.db =util.DBConnect()
                self.etldate=etldate
                self.stretldate =util.tostrdate(self.etldate)
                self.para=util.get_common_parameter(self.db)
                if etldate is not None : self.para['TJRQ']=etldate

	def select_jgzb(self):
		sql1=u"""
			select  trim(branch_code) JGBH,branch_NAME from BRANCH
		"""#t_cs_jg
		sql1=sql1.encode('gb2312')
		rs1=util.get_select_row(self.db,sql1)
		rsd1=[]
		for r in rs1:
			d={}
			d['JGBH']=r[0]
			d['ORG_NAME']=r[1]
			rsd1.append(d)
		#没有等级为3的机构
		sql2=u"""
			SELECT trim(ORG_CODE) JGBH ,JE1/JE2 as  ck_sd_rq
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='机构存款年积数' 
		"""%(int(self.para['TJRQ']))#存款本年积数
		sql2=sql2.encode('gb2312')
		rs2=util.get_select_row(self.db,sql2)
		rsd2=[]
		for r in rs2:
			d={}
			d['JGBH']=r[0]
			d['CK_SD_RQ']=r[1]
			rsd2.append(d)
		sql3=u"""
			SELECT trim(ORG_CODE) JGBH ,JE1/JE2 as  ck_cl_rq
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='机构存款年积数' 
		"""%(int(self.para['JZZZRQ']))#存款去年积数
		sql3=sql3.encode('gb2312')
		rs3=util.get_select_row(self.db,sql3)
		rsd3=[]
		if rs3 is None:
			d={}
			d['JGBH']='NULL'
			d['CK_CL_RQ']=0
			rsd3.append(d)
		else:
                	for r in rs3:
				d={}
                	        d['JGBH']=r[0]
                	        d['CK_CL_RQ']=r[1]
                	        rsd3.append(d)
		sql4=u"""
			SELECT trim(ORG_CODE) JGBH ,JE1/JE2 as  dk_sd_rq
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s   AND ZBLX='机构贷款年积数' 
                """%(int(self.para['TJRQ']))#贷款时点积数
		sql4=sql4.encode('gb2312')
                rs4=util.get_select_row(self.db,sql4)
                rsd4=[]
                for r in rs4:
			d={}
                        d['JGBH']=r[0]
                        d['DK_SD_RQ']=r[1]
                        rsd4.append(d)
		sql5=u"""
			SELECT trim(ORG_CODE) JGBH ,JE1/JE2 as  dk_cl_rq
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s  AND ZBLX='机构贷款年积数' 
                """%(int(self.para['JZZZRQ']))#贷款存量积数
		sql5=sql5.encode('gb2312')
                rs5=util.get_select_row(self.db,sql5)
                rsd5=[]
		if rs5 is None:
			d={}
			d['JGBH']='NULL'
                        d['DK_CL_RQ']=0
                        rsd5.append(d)
		else:
                	for r in rs5:
				d={}
                	        d['JGBH']=r[0]
                	        d['DK_CL_RQ']=r[1]
                	        rsd5.append(d)
		sql6=u"""
			SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='机构贷款余额' 
                """%(int(self.para['TJRQ']))#贷款时点余额
		sql6=sql6.encode('gb2312')
                rs6=util.get_select_row(self.db,sql6)
                rsd6=[]
		if rs6 is None:
                        d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd6.append(d)
                else:
                        for r in rs6:
                                d={}
                                d['JGBH']=r[0]
                                d['JE1']=r[1]
                                rsd6.append(d)
		sql7=u"""
			SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='机构存款余额'
                """%(int(self.para['TJRQ']))#存款时点余额
		sql7=sql7.encode('gb2312')
                rs7=util.get_select_row(self.db,sql7)
                rsd7=[]
		if rs7 is None:
                        d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd7.append(d)
                else:
                        for r in rs7:
                                d={}
                                d['JGBH']=r[0]
                                d['JE1']=r[1]
                                rsd7.append(d)
		sql8=u"""
			SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='机构对公贷款户数' 
                """%(int(self.para['TJRQ']))#对公贷款户数
		sql8=sql8.encode('gb2312')
                rs8=util.get_select_row(self.db,sql8)
                rsd8=[]
		if rs8 is None:
                        d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd8.append(d)
                else:
                        for r in rs8:
                                d={}
                                d['JGBH']=r[0]
                                d['JE1']=r[1]
                                rsd8.append(d)
		sql9=u"""
			SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='机构对私贷款户数' 
                """%(int(self.para['TJRQ']))#对私贷款户数
		sql9=sql9.encode('gb2312')
                rs9=util.get_select_row(self.db,sql9)
                rsd9=[]
		if rs9 is None:
                        d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd9.append(d)
                else:
                        for r in rs9:
                                d={}
                                d['JGBH']=r[0]
                                d['JE1']=r[1]
                                rsd9.append(d)
		sql10=u"""
			SELECT trim(ORG_CODE) JGBH ,je1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='机构不良贷款余额' 
		"""%(int(self.para['TJRQ']))#机构不良贷款余额
		sql10=sql10.encode('gb2312')
                rs10=util.get_select_row(self.db,sql10)
                rsd10=[]
		if rs10 is None:
                        d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd10.append(d)
                else:
                        for r in rs10:
                                d={}
                                d['JGBH']=r[0]
                                d['JE1']=r[1]
                                rsd10.append(d)
		sql11=u"""
        		SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='机构存款余额' 
                """%(int(self.para['JZZZRQ']))#存款上年余额
		sql11=sql11.encode('gb2312')
                rs11=util.get_select_row(self.db,sql11)
                rsd11=[]
		if rs11 is None:
			d={}
			d['JGBH']='NULL'
			d['JE1']=0
			rsd11.append(d)
		else:
                	for r in rs11:
				d={}
                	        d['JGBH']=r[0]
                	        d['JE1']=r[1]
                	        rsd11.append(d)
		sql12=u"""
        		SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='机构低成本存款余额' 
                """%(int(self.para['TJRQ']))#低成本存款
		sql12=sql12.encode('gb2312')
                rs12=util.get_select_row(self.db,sql12)
                rsd12=[]
		if rs12 is None:
			d={}
			d['JGBH']='NULL'
			d['JE1']=0
			rsd12.append(d)
                else:
			for r in rs12:
				d={}
                        	d['JGBH']=r[0]
                        	d['JE1']=r[1]
	                        rsd12.append(d)
		sql13=u"""
   	     		SELECT trim(t1.ORG_CODE) JGBH ,t1.JE1
			FROM t_jgc_jgzb T1
			WHERE T1.DATE_ID=%s AND t1.ZBLX='机构易贷卡存量卡数' 
		"""%(int(self.para['TJRQ']))#易贷卡增加数
		sql13=sql13.encode('gb2312')
                rs13=util.get_select_row(self.db,sql13)
                rsd13=[]
		if rs13 is None:
			d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd13.append(d)
                else:
                	for r in rs13:
				d={}
                        	d['JGBH']=r[0]
                        	d['JE1']=r[1]
                        	rsd13.append(d)
		sql14=u"""
        		SELECT trim(t1.ORG_CODE) JGBH ,t1.JE1
			FROM t_jgc_jgzb T1
			WHERE T1.DATE_ID=%s AND t1.ZBLX='机构易贷卡存量卡数' 
                """%(int(self.para['JZZZRQ']))#易贷卡上年
		sql14=sql14.encode('gb2312')
                rs14=util.get_select_row(self.db,sql14)
                rsd14=[]
		if rs14 is None:
			d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd14.append(d)
                else:
                	for r in rs14:
				d={}
                	        d['JGBH']=r[0]
                	        d['JE1']=r[1]
                	        rsd14.append(d)
		sql15=u"""
        		SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='机构金农卡年开卡数' 
                """%(int(self.para['TJRQ']))#金农卡
		sql15=sql15.encode('gb2312')
                rs15=util.get_select_row(self.db,sql15)
                rsd15=[]
		if rs15 is None:
			d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd15.append(d)
                else:
                	for r in rs15:
				d={}
                	        d['JGBH']=r[0]
                	        d['JE1']=r[1]
                	        rsd15.append(d)
		sql16=u"""
        		SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='企业网银户数' 
                """%(int(self.para['TJRQ']))#企业网银户数
		sql16=sql16.encode('gb2312')
                rs16=util.get_select_row(self.db,sql16)
                rsd16=[]
		if rs16 is None:
			d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd16.append(d)
                else:
                	for r in rs16:
				d={}
                	        d['JGBH']=r[0]
                	        d['JE1']=r[1]
                	        rsd16.append(d)
		sql17=u"""
        		SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='POS机商户数' 
                """%(int(self.para['TJRQ']))#POS机商户数
		sql17=sql17.encode('gb2312')
                rs17=util.get_select_row(self.db,sql17)
                rsd17=[]
		if rs17 is None:
			d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd17.append(d)
                else:
                	for r in rs17:
				d={}
                	        d['JGBH']=r[0]
                	        d['JE1']=r[1]
                	        rsd17.append(d)
		sql18=u"""
        		SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='手机银行户数' 
                """%(int(self.para['TJRQ']))#手机银行户数
		sql18=sql18.encode('gb2312')
                rs18=util.get_select_row(self.db,sql18)
                rsd18=[]
		if rs18 is None:
			d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd18.append(d)
                else:
                	for r in rs18:
				d={}
                	        d['JGBH']=r[0]
                	        d['JE1']=r[1]
                	        rsd18.append(d)
		sql19=u"""
        		SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='贷款利息收入' 
                """%(int(self.para['TJRQ']))#贷款利息收入
		sql19=sql19.encode('gb2312')
                rs19=util.get_select_row(self.db,sql19)
                rsd19=[]
		if rs19 is None:
			d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd19.append(d)
                else:
                	for r in rs19:
				d={}
                	        d['JGBH']=r[0]
                	        d['JE1']=r[1]
                        rsd19.append(d)
		sql20=u"""
        		SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='表内外不良贷款' 
                """%(int(self.para['TJRQ']))#表内外不良贷款
		sql20=sql20.encode('gb2312')
                rs20=util.get_select_row(self.db,sql20)
                rsd20=[]
		if rs20 is None:
			d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd20.append(d)
                else:
                	for r in rs20:
				d={}
                	        d['JGBH']=r[0]
                	        d['JE1']=r[1]
                	        rsd20.append(d)
		sql21=u"""
        		SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='机构贷款余额' 
                """%(int(self.para['JZZZRQ']))#贷款上年末余额
		sql21=sql21.encode('gb2312')
                rs21=util.get_select_row(self.db,sql21)
                rsd21=[]
		if rs21 is None:
			d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd21.append(d)
                else:
                	for r in rs21:
				d={}
                	        d['JGBH']=r[0]
                	        d['JE1']=r[1]
                	        rsd21.append(d)
		sql22=u"""
        		SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='活卡率' 
                """%(int(self.para['TJRQ']))#活卡率
		sql22=sql22.encode('gb2312')
                rs22=util.get_select_row(self.db,sql22)
                rsd22=[]
		if rs22 is None:
			d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd22.append(d)
                else:
                	for r in rs22:
				d={}
                	        d['JGBH']=r[0]
                	        d['JE1']=r[1]
                	        rsd22.append(d)
		sql23=u"""
        		SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='苹果手机动户率' 	
                """%(int(self.para['TJRQ']))#苹果手机动户率
		sql23=sql23.encode('gb2312')
                rs23=util.get_select_row(self.db,sql23)
                rsd23=[]
		if rs23 is None:
			d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd23.append(d)
                else:
                	for r in rs23:
				d={}
                	        d['JGBH']=r[0]
                	        d['JE1']=r[1]
                	        rsd23.append(d)
		sql24=u"""
                        SELECT trim(ORG_CODE) JGBH ,JE1
			FROM t_jgc_jgzb T
			WHERE T.DATE_ID=%s AND ZBLX='安卓手机动户率' 
                """%(int(self.para['TJRQ']))#安卓手机动户率
		sql24=sql24.encode('gb2312')
                rs24=util.get_select_row(self.db,sql24)
                rsd24=[]
		if rs24 is None:
			d={}
                        d['JGBH']='NULL'
                        d['JE1']=0
			rsd24.append(d)
                else:
                	for r in rs24:
				d={}
                	        d['JGBH']=r[0]
                	        d['JE1']=r[1]
                	        rsd24.append(d)

		rsx=[]
		for r1 in rsd1:
			dmax={}
			dmax['JGBH']=r1['JGBH']
			dmax['ORG_NAME']=r1['ORG_NAME']
			for r in rsd2:
				if r1['JGBH']==r['JGBH']:
					dmax['CK_SD_RQ']=r['CK_SD_RQ']
					break
				else:
					dmax['CK_SD_RQ']=0
			for r in rsd3:
				if r1['JGBH']==r['JGBH']:
					dmax['CK_CL_RQ']=r['CK_CL_RQ']
					break
				else:
					dmax['CK_CL_RQ']=0
			for r in rsd4:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['DK_SD_RQ']=r['DK_SD_RQ']
					break
				else:
					dmax['DK_SD_RQ']=0
			for r in rsd5:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['DK_CL_RQ']=r['DK_CL_RQ']
					break
				else:
					dmax['DK_CL_RQ']=0
			for r in rsd6:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['DK_SD']=r['JE1']
					break
				else:
					dmax['DK_SD']=0
			for r in rsd7:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['CK_SD']=r['JE1']
					break
				else:
					dmax['CK_SD']=0
			for r in rsd8:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['DG_HS']=r['JE1']
					break
				else:
					dmax['DG_HS']=0
			for r in rsd9:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['DS_HS']=r['JE1']
					break
				else:
					dmax['DS_HS']=0
			for r in rsd10:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['WJBL_SD']=r['JE1']
					break
				else:
					dmax['WJBL_SD']=0
			for r in rsd11:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['CK_SNM']=r['JE1']
					break
				else:
					dmax['CK_SNM']=0
			for r in rsd12:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['DCB']=int(r['JE1'])
					break
				else:
					dmax['DCB']=0
			for r in rsd13:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['YDKSNM']=r['JE1']
					break
				else:
					dmax['YDKSNM']=0
			for r in rsd14:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['YDKTJ']=r['JE1']
					break
				else:
					dmax['YDKTJ']=0
			for r in rsd15:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['JNK']=r['JE1']
					break
				else:
					dmax['JNK']=0
			for r in rsd16:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['QYWQHS']=r['JE1']
					break
				else:
					dmax['QYWQHS']=0
			for r in rsd17:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['POSHS']=r['JE1']
					break
				else:
					dmax['POSHS']=0
			for r in rsd18:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['M_HS']=r['JE1']
					break
				else:
					dmax['M_HS']=0
			for r in rsd19:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['LXSR']=r['JE1']
					break
				else:
					dmax['LXSR']=0
			for r in rsd20:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['BNWBLDK']=r['JE1']
					break
				else:
					dmax['BNWBLDK']=0
			for r in rsd21:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['DK_SNM']=r['JE1']
					break
				else:
					dmax['DK_SNM']=0
			for r in rsd22:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['HKL']=r['JE1']
					break
				else:
					dmax['HKL']=0
			for r in rsd23:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['APPLE']=r['JE1']
					break
				else:
					dmax['APPLE']=0
			for r in rsd24:
                                if r1['JGBH']==r['JGBH']:
                                        dmax['ANDROID']=r['JE1']
					break
				else:
					dmax['ANDROID']=0
			rsx.append(dmax)	

		rs=[]
		TJDT=self.para['TJRQ']
		TJRQ=self.stretldate
		for r in rsx:
			je1=r['CK_SD']
			je2=int(r['DK_SD'])
			je3=int(r['CK_SD'])-int(r['CK_CL_RQ'])
			je4=int(r['CK_SD_RQ'])-int(r['CK_CL_RQ'])
			je5=r['DCB']
			je6=r['DK_SD_RQ']-r['DK_CL_RQ']
			je7=r['DS_HS']
			je8=r['DG_HS']
			je9=1
			if (r['DK_SD']==None or r['DK_SD']==0):
				je9=0
			else:
				je9=int((r['WJBL_SD']/r['DK_SD'])*100)#五级不良率
			je10=0
			je11=r['YDKTJ']-r['YDKSNM']
			je12=r['JNK']
			je13=r['POSHS']
			je14=0
			je15=r['QYWQHS']
			je16=r['M_HS']
			je17=0
			je18=r['APPLE']
			je19=r['DK_SD']-r['DK_SNM']
			je20=r['LXSR']
			je21=r['BNWBLDK']
			HKL=r['HKL']
			sjyhdhl=r['ANDROID']
			rs.append((r['JGBH'],r['ORG_NAME'],TJRQ,je1,je2,je3,je4,je5,je6,je7,je8,je9,je10,je11,je12,je14,je14,je15,je16,je17,je18,je19,je20,je21,HKL,sjyhdhl))
		self.insert_update_jgzb(rs)
	def insert_update_jgzb(self,rs):
		insert_sql=u"""
			insert into T_JGC_JG_ZB_QM(JGBH,JGMC,TJRQ,JE1,JE2,JE3,JE4,JE5,JE6,JE7,JE8,JE9,JE10,JE11,JE12,JE13,JE14,JE15,JE16,JE17,JE18,JE19,JE20,JE21,HKL,sjyhdhl)
			values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
		"""
		update_sql=u"""
			update T_JGC_JG_ZB_QM set JGMC=?,JE1=?,JE2=?,JE3=?,JE4=?,JE5=?,JE6=?,JE7=?,JE8=?,JE9=?,JE10=?,JE11=?,JE12=?,JE13=?,JE14=?,JE15=?,JE16=?,JE17=?,JE18=?,JE19=?,JE20=?,JE21=?,HKL=?,sjyhdhl=? where JGBH=? and TJRQ=?
		"""
		sql=u"""
			select * from T_JGC_JG_ZB_QM where JGBH=? and TJRQ=?
		"""
		insert_1=[]
		update_1=[]
		for r in rs:
			self.db.cursor.execute(sql,r[0],r[2])
			row=self.db.cursor.fetchone()
			if row is None:
				insert_1.append(r)
			else:
				update_1.append((r[1],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13],r[14],r[15],r[16],r[17],r[18],r[19],r[20],r[21],r[22],r[23],r[24],r[25],r[0],r[2]))
		if len(insert_1)>0:
			self.db.cursor.executemany(insert_sql,insert_1)
			self.db.conn.commit()
		if len(update_1)>0:
			self.db.cursor.executemany(update_sql,update_1)
			self.db.conn.commit()
	
	def run_jgzb(self):
                try :
                        self.select_jgzb()
                        self.db.conn.commit()

                finally :
                        self.db.closeDB()
	def run(self):
		self.run_jgzb()
if __name__=="__main__":
	arglen=len(sys.argv)
        if arglen  == 2:
                Organizationindexes(sys.argv[1]).run()
        else :
                print "please input python khjlrqckyjj.py YYYYMMDD "
