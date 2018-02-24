# -*- coding:utf-8 -*-
#!/bin/python
import DB2
import etl.base.util as util
from etl.base.singleton import singleton


@singleton
class Common():
	def __init__(self):
		self.db = util.DBConnect()
	def get_strdate(self,date):
		date = str(date)
		return date[0:4]+'-'+date[4:6]+'-'+date[6:8]

	def get_insert_sql(self,col):
		cols = u""
		pars = u""
		for it in col['cols']:
			cols = cols + ',' + it
			pars = pars + ',?' 
		sql = u"""
			insert into %s(%s)
			values(%s)
		"""%(col['table'],cols[1:],pars[1:])
		return sql

	def get_up_sql(self,col):
		cols = u""
		pars = u""
		for it in col['cols']:
			cols = cols + '%s = ?,'% it
		for key in col['key']:
			pars = pars + '%s = ? and '% key 
		sql = u"""
			update %s set %s
			where %s
		"""%(col['table'],cols[:-1],pars[:-4])
		return sql

	def get_sel_sql(self,col):
		pars = u""
		for key in col['key']:
			pars = pars + '%s = ? and '% key 

		sql = u"""
			select 1 from %s where %s
		"""%(col['table'],pars[:-4])
		return sql
	
	def get_data(self,col,r):
		data =[]
		for it in col['cols']:
			data.append(r.get(it,None))
		fdata = []
		for key in col['key']:
			if not r.has_key(key):
				print "不允许key%s为空"%key
				raise Exception
			else:
				fdata.append(r[key])
		return (fdata,data)

	def insert_update(self,db,rs,col):
		insert_sql = self.get_insert_sql(col)
		up_sql = self.get_up_sql(col)
		sel_sql = self.get_sel_sql(col)

		insert_data = []
		up_data = []
		for r in rs:
			fdata,data =self.get_data(col,r)	
			db.cursor.execute(sel_sql,fdata)
			row = db.cursor.fetchone()
			if row is None:
				insert_data.append(data)
			else:
				up_data.append(data+fdata)
	
		if len(insert_data)>0:
			db.cursor.executemany(insert_sql,insert_data)
			db.conn.commit()
		if len(up_data)>0:
			db.cursor.executemany(up_sql,up_data)
			db.conn.commit()

	def list2dict(self,data,col):
		rs = []
		for item in data:
			d ={}
			if len(item)!=len(col['cols']):
				raise Exception
			for i in range(len(item)):
				d[col['cols'][i]]=item[i]
			rs.append(d)
		return rs

common = Common()		
	
if __name__ == '__main__':
	DBConnect().getConnect()
	
