# -*- coding:utf-8 -*-

#DSN="driver={IBM DB2 ODBC DRIVER };database=%s;hostname=%s;port=%s;protocol=tcpip;"%("dwedb","127.0.0.1","50000")
DSN="dwedb"
USER="ydw"
PASSWD="qwe123"

from etl.base.singleton import singleton

@singleton
class Config():
    def __init__(self):
        self.fact_execute_num=10
        self.data_path = u"/data/mis_src"
        self.branch_code =u'966'
Config().etldate=None
Config().etldateotr=None
Config().stretldate=None 
Config().accountid=[]
Config().firstrun=False

Config().target_data = "/data/mis_src"
