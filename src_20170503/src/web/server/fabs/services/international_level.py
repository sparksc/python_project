#-*-coding:utf-8-*-
import datetime,xlrd
from flask import json, g,current_app
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all,aliased
from ..base import utils
from ..model import CustHook, User_ExtraScore, Branch,User,UserBranch,T_Para_Detail,UserLevel,T_Para_Header,T_Para_Type,TellerLevel,Group,UserGroup,InternationalLevel,Burank,BranchGroup
from man_gradejdg import Man_gradejdgService
from userreport import UserReport
import datetime

msg = Man_gradejdgService()
ur = UserReport()
local_year,last_year,local_satrday,last_endday = ur.get_year_day()
class Org_levelService():
    def calculate(self,**kwargs):
        try:
            rlist = self.get_rlist()
            for item in rlist:
                #current_app.logger.debug(item)
                syear = item[1]
                org_code = '966220'
                branch = g.db_session.query(InternationalLevel).filter(InternationalLevel.syear == syear).filter(InternationalLevel.org_code == org_code).first()
                
                if branch:
                    g.db_session.query(InternationalLevel).filter(InternationalLevel.syear==syear).filter(InternationalLevel.org_code==org_code).\
                        update({InternationalLevel.syear:syear,InternationalLevel.org_code:org_code,\
                        InternationalLevel.ranking:str(int(item[2])),\
                        InternationalLevel.sys_level:item[3],InternationalLevel.last_level:item[3]})
                else:
                    g.db_session.add(InternationalLevel(syear=syear,org_code=org_code,
                        ranking=str(int(item[2])),\
                        sys_level=item[3],last_level=item[3]))

                g.db_session.flush()
                edit_grade = g.db_session.query(InternationalLevel.adj_level).filter(InternationalLevel.syear==syear,InternationalLevel.org_code==org_code).first()
                if not (edit_grade[0] is None):
                    g.db_session.query(InternationalLevel).filter(InternationalLevel.syear==syear,InternationalLevel.org_code==org_code).update({InternationalLevel.last_level:edit_grade[0]})
            return u'计算成功'
        except Exception,e:
            print type(e)
            return u"计算失败"+str(e)
    
    def affirm(self,**kwargs):
        row = g.db_session.query(InternationalLevel.org_code,InternationalLevel.last_level).filter(InternationalLevel.syear==last_year).order_by(InternationalLevel.org_code).all()
        for item in row:
            result = ur.update_org_grade(item[0],item[1],True)
        return result
    
    def get_rlist(self,**kwargs):
        #获取年份和排名
        row = g.db_session.query(Burank.syear,Burank.srank,InternationalLevel.last_level,InternationalLevel.adj_level).outerjoin(InternationalLevel,InternationalLevel.syear==Burank.syear).order_by(Burank.syear).all()
        aslist = []
        for i in range(0,len(row)):
            slist = []#存放每年升降名次
            if i == 0:
                ranking = 0 
            else:
                ranking = int(row[i][1]) - int(row[(i-1)][1])
            slist.append(ranking)
            slist.append(row[i][0])
            slist.append(row[i][1])
            slist.append(row[i][2])
            slist.append(row[i][3])

            aslist.append(slist)
        row2 = aslist
        typenames=[u'国际业务部全省排名上升参数',u'支行（部）业务经营管理等级划分参数']
        alllist = []
        kw = {'type_name':typenames[0],'type_name2':typenames[1],'header_key':'add_grade','header_key2':'branch_grade'}
        all_garde = self.get_fscores(row2,**kw)
        return all_garde 

    def get_fscores(self,arr,**kwargs):
        type_name = kwargs.get('type_name')
        type_name2 = kwargs.get('type_name2')
        header_key = kwargs.get('header_key')
        header_key2 = kwargs.get('header_key2')
        cscore = 0
        fscore = 0
        #获取等级上升参数
        rank = g.db_session.query(T_Para_Detail.detail_value).\
                 join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
                 join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
                 filter(T_Para_Type.type_name == type_name).\
                 filter(T_Para_Header.header_key == header_key).\
                 order_by(T_Para_Detail.para_row_id).all()
        #获取等级得分
        grade = g.db_session.query(T_Para_Detail.detail_value).\
                 join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
                 join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
                 filter(T_Para_Type.type_name == type_name2).\
                 filter(T_Para_Header.header_key == header_key2).\
                 order_by(T_Para_Detail.para_row_id).all()
        max_garde = grade[2][0] #取最高等级 二级
        thd_garde = grade[3][0]
        fir_garde = grade[4][0]
        min_garde = grade[5][0] #取最低等级 五级

        #计算从2014年开始,2014排名为13,等级为三级,2015排名11,等级为二级,其他年份为开始则为二级
        if arr[0][3] == None:
            if int(arr[0][1]) == 2014 and int(arr[0][2]) == 13:
                arr[0][3] = thd_garde
            elif int(arr[0][1]) == 2015 and int(arr[0][2]) == 11:
                arr[0][3] = max_garde
            elif int(arr[0][1]) == 2016 and int(arr[0][2]) == 12:
                arr[0][3] = max_garde
            else:
                arr[0][3] = max_garde
        #current_app.logger.debug(arr[0][3]) 
        for i in range(1,len(arr)):
            if arr[i-1][4] is not None:
                socre = self.get_score(arr[i-1][4]) 
            else:
                socre = self.get_score(arr[i-1][3]) 
            if int(arr[i][0]) >= 0:
                ra = int(arr[i][0]) / int(rank[0][0])
            else :
                ra = - (int(abs(arr[i][0])) / int(rank[0][0]) )
            ra = socre + ra
            if ra < 2:
                ra = 2
            if ra >5:
                ra = 5

            arr[i][3]=self.get_garde(ra)
            #current_app.logger.debug(str(arr[i][3])+str(arr[i][1]))
        return arr


    def get_score(self, garde):
        if garde == u'二级':
            return 2
        elif garde == u'三级':
            return 3
        elif garde == u'四级':
            return 4
        elif garde == u'五级':
            return 5
            
    def get_garde(self, socre):
        if socre == 2:
            return u'二级'
        elif socre == 3:
            return u'三级'
        elif socre == 4:
            return u'四级'
        elif socre == 5:
            return u'五级'
     
    def change_save(self,**kwargs):
        try:
            item_id = kwargs.get('item_id')
            adj_level = kwargs.get('adj_level')
            g.db_session.query(InternationalLevel).filter(InternationalLevel.id == item_id).update({InternationalLevel.adj_level:adj_level,InternationalLevel.last_level:adj_level})
            return u'调整等级成功'
        except Exception,e:
            return u'调整等级失败'

