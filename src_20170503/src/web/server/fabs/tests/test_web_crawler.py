# -*- coding:utf-8 -*-
u"""
网络爬虫
"""
import logging, datetime,os,re,xlrd,urllib,urllib2,sys
from bs4 import BeautifulSoup
from .configure import Configure
from ..domain.model import *
from ..web_crawler import *

    
def test_insertDB():
    search_civil_servant2()
    search_civil_servant3()
    search_biz_manager()
    search_gov_manager()
    search_sch_manager()
     
if __name__=="__main__":
    test_insertDB()

