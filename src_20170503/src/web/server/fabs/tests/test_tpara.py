# -*- coding:utf-8 -*-

import unittest
from sqlalchemy.orm import joinedload_all
from ..base import utils
import datetime

import csv
import logging

from ..model.t_para import *
log = logging.getLogger()

class TestPara(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()
        logging.debug("finish!!!")
        init_para(self.session) 
    
    def tearDown(self):
        logging.debug("finish!!!")

def init_para(session):
    logging.debug("init tpara")
   
    for k,v in tdict.items():
        rs = init_para_file(k,v)
        if k =='T_PARA_TYPE':
            for data in rs:
                session.add(T_Para_Type(**data))
        if k =='T_PARA_DETAIL':
            for data in rs:
                session.add(T_Para_Detail(**data))
        if k =='T_PARA_ROW':
            for data in rs:
                session.add(T_Para_Row(**data))
        if k =='T_PARA_HEADER':
            for data in rs:
                session.add(T_Para_Header(**data))

    session.commit()

tdict = {
    'T_PARA_TYPE':["ID","TYPE_STATUS","TYPE_NAME", "TYPE_MODULE","TYPE_KEY" ,"TYPE_DETAIL" ],
    'T_PARA_ROW':["ID" ,"PARA_TYPE_ID" ,"ROW_NUM", "ROW_STATUS" ,"ROW_START_DATE","ROW_END_DATE"],
    'T_PARA_HEADER':["ID","PARA_TYPE_ID","HEADER_NAME"   ,"HEADER_KEY"    ,"HEADER_ORDER" ,"HEADER_DETAIL" ,"HEADER_TYPE"  ,"HEADER_STATUS"  ],
    'T_PARA_DETAIL':["ID","PARA_HEADER_ID" ,"PARA_ROW_ID","DETAIL_VALUE","DETAIL_KEY"]
}

def init_para_file(type,fildlist):
    path = "%s.del"%type
    csv_reader = csv.reader(path)
    rs =[]
    for row in csv_reader:
        data={}
        i = 0
        for item in row:
            data[fildlist[i]] = item
    return rs
