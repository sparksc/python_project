# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
import DB2  
import csv

import etl.base.util as util
from etl.base.conf import Config
     
condecimal = getcontext()
"""
    更新D_CUST_CONTRACT表上的CST_NO字段，
"""
def update_cst_no():
    try :
        db = util.DBConnect()
        m_sql ="""
            update D_CUST_CONTRACT c set c.CST_NO=(select CST_NO from D_CREDIT_CARD where CARD_NO=c.CARD_NO) where c.BUSI_TYPE='ETC' and substr(c.CST_NO,1,1)<>'8'
        """
        """
        跑完datastage之后可能会把第三方存管内码重新变成空，需要重新更新第三方存管的内码
        """
        sql0=u"""
        UPDATE   D_CUST_CONTRACT  D SET CST_NO=(  SELECT A.CST_NO FROM ( SELECT DISTINCT D.ACCT_NO,C.CST_NO,MIN(D.ID) AS ID   FROM D_CUST_CONTRACT D
        JOIN D_ACCOUNT C ON D.ACCT_NO=C.ACCOUNT_NO   
        WHERE D.BUSI_TYPE='第三方存管'   GROUP BY D.ACCT_NO,C.CST_NO  ) A  WHERE D.ACCT_NO=A.ACCT_NO  AND D.ID =A.ID FETCH FIRST 1 ROWS ONLY)  WHERE D.BUSI_TYPE='第三方存管'
        """
        """更新完内码后，没有的内码会变成空，在更新manageid时会报错，要把空更新成‘无’"""
        sql1=u"""
        update d_cust_contract set CST_NO='无' where BUSI_TYPE='第三方存管' and cst_no is  null
        """
        sql2=u"""
        update   D_CUST_CONTRACT  D set CST_NO=(  select A.CST_NO from ( select distinct d.ACCT_NO,c.CST_NO,min(d.id) as id   from D_CUST_CONTRACT D
        join D_ACCOUNT C on D.ACCT_NO=C.ACCOUNT_NO   
        where d.BUSI_TYPE='手机银行' and d.CST_NO is null  group by d.ACCT_NO,c.CST_NO  ) A  where D.ACCT_NO=A.ACCT_NO  and d.id =A.id fetch first 1 rows only)  where d.BUSI_TYPE='手机银行' and d.cst_no is null
        """
        sql3=u"""
        MERGE INTO D_CUST_CONTRACT A 
        USING (SELECT C.CUST_NO,D.ID FROM D_CUST_INFO C JOIN D_CUST_CONTRACT D ON C.CUST_LONG_NO=D.CST_NO
         WHERE C.ID IN(SELECT MAX(I.ID) AS CID FROM D_CUST_CONTRACT D JOIN D_CUST_INFO I ON D.CST_NO = I.CUST_LONG_NO
         WHERE LENGTH(TRIM(D.CST_NO)) != 11 AND D.BUSI_TYPE = '支付宝卡通' AND D.CST_NO !='' GROUP BY  I.CUST_LONG_NO ) )  B ON A.ID=B.ID
        WHEN MATCHED THEN UPDATE SET A.CST_NO=B.CUST_NO
        """
        sql4=u"""
        MERGE INTO D_CUST_CONTRACT A
        USING (SELECT D.ID,MAX(C.CUST_NO) AS CUST_NO FROM D_CUST_CONTRACT D 
         JOIN D_CUST_INFO C ON C.CUST_LONG_NO='101'||(D.ID_NUMBER)
         WHERE D.BUSI_TYPE='第三方存管' AND D.CST_NO='无' GROUP BY D.ID) B ON A.ID=B.ID
        WHEN MATCHED THEN UPDATE SET A.CST_NO=B.CUST_NO
        """
        sql5=u"""
        MERGE INTO D_CUST_CONTRACT A
        USING (SELECT D.ID,MAX(C.CUST_NO) AS CUST_NO FROM D_CUST_CONTRACT D 
         JOIN D_CUST_INFO C ON C.CUST_LONG_NO='1'||CCRD15TO18(D.ID_NUMBER)
         WHERE D.BUSI_TYPE='第三方存管' AND D.CST_NO='无' GROUP BY D.ID) B ON A.ID=B.ID
        WHEN MATCHED THEN UPDATE SET A.CST_NO=B.CUST_NO
        """
        db.cursor.execute(m_sql)
        db.cursor.execute(sql0.encode('utf-8'))
        db.cursor.execute(sql1.encode('utf-8'))
        db.cursor.execute(sql2.encode('utf-8'))
        db.cursor.execute(sql3.encode('utf-8'))
        db.cursor.execute(sql4.encode('utf-8'))
        db.cursor.execute(sql5.encode('utf-8'))
        db.conn.commit()
    finally :
        db.closeDB()

if __name__=='__main__':
    update_cst_no()
