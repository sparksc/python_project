# -*- coding:utf-8 -*-
#!/bin/python  

from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random,sys 
from datetime import datetime,timedelta
from decimal import *
import DB2  

from etl.base.conf import *
import etl.base.util as util

def sequence():
    util.fix_seq_id('D_MANAGE','D_MANAGE_SEQ')
    util.fix_seq_id('D_CUST_CONTRACT','D_CUST_CONTRACT_SEQ')
    util.fix_seq_id('D_ACCOUNT','D_ACCOUNT_SEQ_NEW')
    util.fix_seq_id('MENU','MENU_ID_SEQ')

if __name__=='__main__':
    util.fix_seq_id('D_MANAGE','D_MANAGE_SEQ')
    util.fix_seq_id('D_CUST_CONTRACT','D_CUST_CONTRACT_SEQ')
    util.fix_seq_id('D_ACCOUNT','D_ACCOUNT_SEQ_NEW')
    util.fix_seq_id('MENU','MENU_ID_SEQ')
