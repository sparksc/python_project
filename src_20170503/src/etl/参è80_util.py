# -*- coding:utf-8 -*-
#!/bin/python
import DB2
from riskconf import RiskConfig
import etl.star.util as util
from etl.star.singleton import singleton


class DBConnect():
	__connect_num__=0
	def __init__(self):
		DBConnect.__connect_num__=DBConnect.__connect_num__+1
		self.conn = self.getConnect()
		self.cursor = self.conn.cursor()
	def closeDB(self):
		try:
			self.cursor.close()
                        self.cursor=None
                        self.conn.close()
                        self.conn=None
                        DBConnect.__connect_num__=DBConnect.__connect_num__-1
		except Exception, e:
			pass
		finally:
			pass
	def getConnect(self):
		DSN = RiskConfig().DSN
		USER = RiskConfig().USER
		PASSWD = RiskConfig().PASSWD
        	return  DB2.connect(DSN,USER,PASSWD)
@singleton
class Common():
	def __init__(self):
		self.db = DBConnect()
		self.cust = self.get_cust()
	def getloandata(self,*arg):
		sql="""
		
		"""
	def get_strdate(self,date):
		date = str(date)
		return date[0:4]+'-'+date[4:6]+'-'+date[6:8]

	"""
	   取得所需参数类型
	"""
	def get_risk_cs(self,db,risktype):
		sql =u"""
			select SUBTYPE, PARA1
 			from T_RISK_PARA
  			where riskname =?
		"""
		db.cursor.execute(sql,risktype)
		row = db.cursor.fetchone()
		data = {}
		while row :
			data[row[0]] = row[1]
			row = db.cursor.fetchone() 
		return data
	"""
		删除历史数据跑出来
	"""
	def delete_today_risk(self,db,strdate,rtype):
		d_sql = u"""
			delete from t_jgc_czfx where tjrq=? and gnbh = ? and spbz is null
		""" 
		db.cursor.execute( d_sql,strdate,rtype)
        	db.conn.commit()

	def get_msg(self,rtype,args,tablename):
                sql = 'select *  from %s where gldxbh =?'%tablename
		decsql = "select * from %s where 1!=1"%tablename
		self.db.cursor.execute(decsql)
		self.desc = self.db.cursor.description
                self.db.cursor.execute(sql,rtype)
                row = self.db.cursor.fetchone()
                data = {}
                while row:
			for key,value in args.items():
				idx = util.get_colname_index(self.desc,value)
				data[key] = row[idx]
                	row = self.db.cursor.fetchone()
                return data

	"""
	key:作为主键的字段，l_value:需要的比对的字段，d_filter:筛选条件
	得到历史的风险
	"""	
	def get_risk_his(self,l_key,l_value,d_filter):
		k_str = ""
		for i in l_key:
			k_str = k_str+","+i
		k_str = k_str[1:]
		s_str = ""
		for i in l_value:
			s_str = s_str+","+i
		s_str = s_str[1:]
		filter_str = ""
		d=[]
		for k,v in d_filter.items():
			filter_str = filter_str+" and %s = ?"%k
			d.append(v)
		filter_str = filter_str[4:]
		sql = u"""
			select %s,%s from t_jgc_czfx where %s
		"""%(k_str,s_str,filter_str)
		self.db.cursor.execute( sql,d)
		row = self.db.cursor.fetchone()
                data = {}
		while row:
			data_key = self.rowtovalue(row[0:len(l_key)])
			data[data_key] = self.rowtovalue(row[len(l_key):])
                	row = self.db.cursor.fetchone()
                return data
	
	def rowtovalue(self,row):
		key = None
		for i in range(len(row)):
                        val = row[i]
                        if val is None :
                                val = "--"
                        if isinstance(val, unicode) :
                                val=val.strip()
                        elif isinstance(val, str) :
                                val=val.strip()
                        else :
                                val=str(val)
                        if key is None :
                                key = val
                        else:
                                key=key+"|"+val
                return key	


	
	def get_risk_flag(self,rtype,args,tablename,etldate):
		sql = 'select *  from %s where gnbh =? and tjrq = ?'%tablename
                decsql = "select * from %s where 1!=1"%tablename
                self.db.cursor.execute(decsql)
                self.desc = self.db.cursor.description
                self.db.cursor.execute(sql,rtype,etldate)
                row = self.db.cursor.fetchone()
                data = {}
		datalist = []
                while row:
                        for key,value in args.items():
                                idx = util.get_colname_index(self.desc,value)
                                data[key] = row[idx]
			datalist.append(data)
                        row = self.db.cursor.fetchone()
                return datalist
	def get_cust(self):
		sql ="select distinct cust_no,cust_name from d_cust where  cust_no!='--' and cust_no!=''"
		self.db.cursor.execute(sql)
		row = self.db.cursor.fetchone()
                data = {}
		while row:
			data[row[0]] = row[1]
                	row = self.db.cursor.fetchone()
                return data
	""" 插入风险表
	"""
	def insert2db(self,rs,insert_sql):
        	self.db.cursor.executemany (insert_sql, rs )
        	self.db.conn.commit()

	def simple_db2dict(self,sql,f_list= None):
		if f_list is None:
			self.db.cursor.execute(sql)
		else:
			self.db.cursor.execute(sql,f_list)
		data = {}
		row = self.db.cursor.fetchone() 
		while row :
			data[row[0].strip()] = row
			row = self.db.cursor.fetchone() 
		return data
		
	def get_insrt_flag(self,data1,data2):
                for item in data1:
                        flag = True
                        for key1,value1 in item.items():
                                if data2[key1] != value1:
                                        flag = False
                        if flag:
                                return True
                return False
	

common = Common()		
	
if __name__ == '__main__':
	DBConnect().getConnect()
	data=Common().get_risk_msg('TSZYJYJK_DKLJY_016',{'CDBH':'DXBH','DXMC':'DXBH'})
	
