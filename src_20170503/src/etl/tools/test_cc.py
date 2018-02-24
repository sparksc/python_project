# -*- coding:utf-8 -*-
#!/bin/python 
import os, time, random,sys
from datetime import datetime,timedelta

def daycalc(etldate,days):
    if etldate == 0:
        return 0
    s=str(etldate)
    d1=datetime(int(s[0:4]),int(s[4:6]),int(s[6:8])) + timedelta(days)
    s=str(d1.strftime('%Y%m%d'))
    return s

if __name__=='__main__':
   arglen=len(sys.argv)
   date = sys.argv[1]
   days = int(sys.argv[2])
   print days
   #day = daycalc(date,days)
   s = datetime.now()
   ss = str(s)[0:4]+str(s)[5:7]+str(s)[8:10]
   print "***:",ss
   i = '-1'
   #print "****:",i
   day = daycalc(ss,-1)
   days = day[0:4]+'-'+day[4:6]+'-'+day[6:8]
   print days
