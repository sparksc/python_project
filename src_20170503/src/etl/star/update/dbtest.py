# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
import DB2  

import etl.base.util as util
from etl.base.conf import Config
import ibm_db
	 

dsn = "DSN=PDB2;DRIVER={IBM DB2 ODBC DRIVER};DATABASE=qm_dwedb;HOSTNAME=192.168.100.14;PORT=50000;PROTOCOL=TCPIP;UID=ydw;PWD=qwe123;"


if __name__=='__main__':
	db = util.DBConnect("dwedb14","ydw","qwe123")
	print db
