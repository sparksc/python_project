#-*- coding:utf-8 -*-
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

port = 1521
user = 'system'
pwd = 'system'
host = "192.168.30.144"
sid = 'xinchanwork'
#host = "192.168.112.184"
#sid = 'gzh'

#user = 'gzhms'
#pwd = 'gzhms'
#host = "10.10.1.43"
#sid = 'db3gbk1'

conn_str = 'oracle://%s:%s@%s:%d/%s' % (user, pwd, host, port, sid)
print conn_str

engine = create_engine(conn_str,pool_recycle=1)
Session = sessionmaker(bind=engine)
session = Session()
#r = session.execute("select * from t_jgc_jjzb_dkmx")
#print r.first()
