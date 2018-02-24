#-*-coding:utf-8-*-
import datetime,xlrd
from flask import json, g,current_app
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all,aliased
from ..base import utils
from ..model import CustHook, User_ExtraScore, Branch,User,UserBranch,T_Para_Detail,UserLevel,T_Para_Header,T_Para_Type,TellerLevel,Group,UserGroup
from man_gradejdg import Man_gradejdgService
from userreport import UserReport
import datetime
from flask import current_app

msg = Man_gradejdgService()
ur = UserReport()
local_year,last_year,local_satrday,last_endday = ur.get_year_day()
class Teller_levelService():
    def calculate(self,**kwargs):
        try:
            rlist = self.get_rlist()
            for item in rlist:
                #current_app.logger.debug(item)
                syear = item[0][2]
                user_code = item[0][1]
                user = g.db_session.query(TellerLevel).filter(TellerLevel.syear == syear).filter(TellerLevel.user_code == user_code).first()
                
                if user:
                    g.db_session.query(TellerLevel).filter(TellerLevel.syear==syear).filter(TellerLevel.user_code==user_code).\
                    update({TellerLevel.syear:syear,TellerLevel.user_code:user_code,\
                    TellerLevel.count_rdata:item[1][1],TellerLevel.count_cscore:str(float(item[1][2])),TellerLevel.count_weight:str(float(item[1][3])),TellerLevel.count_score:str(float(item[1][0])),\
                    TellerLevel.level_rdata:item[2][1],TellerLevel.level_cscore:str(float(item[2][2])),TellerLevel.level_weight:str(float(item[2][3])),TellerLevel.level_score:str(float(item[2][0])),\
                    TellerLevel.civil_rdata:item[3][1],TellerLevel.civil_cscore:str(float(item[3][2])),TellerLevel.civil_weight:str(float(item[3][3])),TellerLevel.civil_score:str(float(item[3][0])),\
                    TellerLevel.error_rdata:item[4][1],TellerLevel.error_cscore:str(float(item[4][2])),TellerLevel.error_weight:str(float(item[4][3])),TellerLevel.error_score:str(float(item[4][0])),\
                    TellerLevel.satis_rdata:item[5][1],TellerLevel.satis_cscore:str(float(item[5][2])),TellerLevel.satis_weight:str(float(item[5][3])),TellerLevel.satis_score:str(float(item[5][0])),\
                    TellerLevel.wyear_rdata:item[6][1],TellerLevel.wyear_cscore:str(float(item[6][2])),TellerLevel.wyear_weight:str(float(item[6][3])),TellerLevel.wyear_score:str(float(item[6][0])),\
                    TellerLevel.edu_rdata:item[7][1],TellerLevel.edu_cscore:str(float(item[7][2])),TellerLevel.edu_weight:str(float(item[7][3])),TellerLevel.edu_score:str(float(item[7][0])),\
                    TellerLevel.byear_rdata:item[8][1],TellerLevel.byear_cscore:str(float(item[8][2])),TellerLevel.byear_weight:str(float(item[8][3])),TellerLevel.byear_score:str(float(item[8][0])),\
                    TellerLevel.extra_score:str(float(item[0][0])),TellerLevel.violate_score:str(float(item[9][0])),TellerLevel.total_score:str(float(item[10][0])),\
                    TellerLevel.sys_level:item[11][0],TellerLevel.last_level:item[11][0]})             
                else:
                    g.db_session.add(TellerLevel(syear=syear,user_code=user_code,count_rdata=item[1][1],count_cscore=str(float(item[1][2])),count_weight=str(float(item[1][3])),count_score=str(float(item[1][0])),\
                    level_rdata=item[2][1],level_cscore=str(float(item[2][2])),level_weight=str(float(item[2][3])),level_score=str(float(item[2][0])),\
                    civil_rdata=item[3][1],civil_cscore=str(float(item[3][2])),civil_weight=str(float(item[3][3])),civil_score=str(float(item[3][0])),\
                    error_rdata=item[4][1],error_cscore=str(float(item[4][2])),error_weight=str(float(item[4][3])),error_score=str(float(item[4][0])),\
                    satis_rdata=item[5][1],satis_cscore=str(float(item[5][2])),satis_weight=str(float(item[5][3])),satis_score=str(float(item[5][0])),\
                    wyear_rdata=item[6][1],wyear_cscore=str(float(item[6][2])),wyear_weight=str(float(item[6][3])),wyear_score=str(float(item[6][0])),\
                    edu_rdata=item[7][1],edu_cscore=str(float(item[7][2])),edu_weight=str(float(item[7][3])),edu_score=str(float(item[7][0])),\
                    byear_rdata=item[8][1],byear_cscore=str(float(item[8][2])),byear_weight=str(float(item[8][3])),byear_score=str(float(item[8][0])),\
                    extra_score=str(float(item[0][0])),violate_score=str(float(item[9][0])),total_score=str(float(item[10][0])),sys_level=item[11][0],last_level=item[11][0]))

                g.db_session.flush()
                edit_grade = g.db_session.query(TellerLevel.adj_level).filter(TellerLevel.syear==syear,TellerLevel.user_code==user_code).first()
                if not (edit_grade[0] is None):
                    g.db_session.query(TellerLevel).filter(TellerLevel.syear==syear,TellerLevel.user_code==user_code).update({TellerLevel.last_level:edit_grade[0]})
            return u'计算成功'
        except Exception,e:
            return u"计算失败"
    def affirm(self,**kwargs):
        row = g.db_session.query(TellerLevel.user_code,TellerLevel.last_level,TellerLevel.syear).order_by(TellerLevel.user_code,TellerLevel.syear).all()
        for item in row:
            date = local_satrday
            user_name = item[0]
            result = ur.check_update_his(last_endday,local_satrday,user_name,item[1])
        return result
    
    def get_rlist(self):
        row = g.db_session.query(UserLevel.syear,UserLevel.user_code,UserLevel.task_level,UserLevel.civilized_service,UserLevel.task_errorrate,UserLevel.cust_satisfaction,\
        UserLevel.work_year,User.edu,UserLevel.bankterm_year,UserLevel.violation_score).filter(User.user_name == UserLevel.user_code,UserLevel.syear == last_year).order_by(UserLevel.user_code).all()
        #扣分平均值
        lens = len(row)
        total = 0
        temp = 0
        #for r in row:
        #    current_app.logger.debug(len(r))
        for i in range(0,lens):
            if row[i][9]:
                temp = row[i][9]                 
            total += float(temp)
        avg = round(total/lens,2)

        alllist = []#存放各个员工的最终得分
        param1 = {'type_name':'员工附加分项参数','real_data':'','detail_key':'extra_code'}
        param2 = {'type_name':'柜员附加分最高值参数','detail_key':'Max_ExtraScore'}
        maxscore = self.getMaxScore(**param2)#附加分最大值
        weights = msg.get_weight(**{'type_name':'柜员等级指标权重参数','header_key':'GY_Weight'})
        i = 0
        tellernum = ur.teller_num(last_year)
        #current_app.logger.debug(tellernum)
        for item in row:
            syear = item[0]
            user_code = item[1]
            extra_row = g.db_session.query(User_ExtraScore.credential_code,User.is_headman).\
                            join(User,User.user_name == user_code).\
                            filter(User_ExtraScore.user_code == user_code).filter(User_ExtraScore.syear == syear).first()
            fscore = 0
            #用户附加分
            if extra_row:
                if not extra_row[0]:
                    fscore = 0
                else:
                    param1['real_data'] = extra_row[0]
                    fscore = msg.grade_param(**param1)      
                #用户是否是柜组长
                is_gleader = extra_row[1]
                if is_gleader == '是':
                    fscore = float(fscore) + 1
    
                if fscore > float(maxscore):
                    fscore = float(maxscore)      
            perlist = []
            result = (fscore,user_code,syear)
            perlist.append(result)
            alllist.append(perlist)           

            #业务量（笔）
            te_num = tellernum.get(item[1],(0,0))
            te_num = str(te_num[1])
            kw = {'real_data':te_num,'type_name':u'柜员等级指标标准值和等级值参数','min_header_key':'Min_YWScore','max_header_key':'Max_YWScore','header_name':'分值(分)','weight':weights[0][0]}
            self.get_fscores(alllist[i],**kw)
            #市办业务知识技能达标
            kw = {'real_data':item[2],'type_name':u'柜员等级指标标准值和等级值参数','detail_key':'DJScore','detail_value':u'市办业务知识技能达标','weight':weights[1][0]}
            self.get_fscores(alllist[i],**kw)
            #文明服务
            kw = {'real_data':item[3],'type_name':u'柜员等级指标标准值和等级值参数','min_header_key':'Min_FWScore','max_header_key':'Max_FWScore','header_name':'分值(分)','weight':weights[2][0]}
            self.get_fscores(alllist[i],**kw)
            #出错率
            kw = {'real_data':item[4],'type_name':u'柜员等级指标标准值和等级值参数','min_header_key':'Min_CCScore','max_header_key':'Max_CCScore','header_name':'分值(分)','weight':weights[3][0]}
            self.get_fscores(alllist[i],**kw)
            #满意度
            kw = {'real_data':item[5],'type_name':u'柜员等级指标标准值和等级值参数','min_header_key':'Min_MYScore','max_header_key':'Max_MYScore','header_name':'分值(分)','weight':weights[4][0]}
            self.get_fscores(alllist[i],**kw)
            #行龄
            kw = {'real_data':item[6],'type_name':u'柜员等级指标标准值和等级值参数','min_header_key':'Min_HL','max_header_key':'Max_HL','header_name':'分值(分)','weight':weights[5][0]}
            self.get_fscores(alllist[i],**kw)
            #文化程度
            kw = {'real_data':item[7],'type_name':u'柜员等级指标标准值和等级值参数','detail_key':'DJScore','detail_value':u'文化程度','weight':weights[6][0]}
            self.get_fscores(alllist[i],**kw)
            #临柜
            kw = {'real_data':item[8],'type_name':u'柜员等级指标标准值和等级值参数','min_header_key':'Min_LG','max_header_key':'Max_LG','header_name':'分值(分)','weight':weights[7][0]}
            self.get_fscores(alllist[i],**kw)
            #扣分
            real_data = (float(item[9])-avg)/avg*100

            kw = {'real_data':round(real_data,2),'type_name':u'员工违规积分附加分项参数','min_header_key':'Min_WScore','max_header_key':'Max_WScore','header_name':'扣分(分)'}
            self.get_fscores(alllist[i],**kw)
            #总分
            total = self.get_totalscore(alllist[i])
            alllist[i].append((total,0))                  
            #等级
            kw = {'real_data':alllist[i][10][0],'type_name':u'柜员等级划分参数','min_header_key':'Min_JScore','max_header_key':'Max_JScore','header_name':'等级'}
            self.get_fscores(alllist[i],**kw)
            #current_app.logger.debug(alllist[i])
            i += 1     
        return alllist

    def get_fscores(self,arr,**kwargs):
        real_data = kwargs.get('real_data')
        detail_value = kwargs.get('detail_value')
        weight = kwargs.get('weight')
        header_name = kwargs.get('header_name')
        cscore = 0
        if not real_data is None:
            if not detail_value:
                cscore = self.get_grade_param(**kwargs)
            else:
                cscore = msg.grade_param(**kwargs)
            if cscore == None:
                cscore = 0

            if header_name != '等级':
                cscore = float(cscore)
                if weight == None:
                    weight = 100
                weight = float(weight)
                fscore = cscore*weight/100
            else:
                fscore = cscore
        else:
            fscore = 0
        result = (fscore,real_data,cscore,weight)
        min_header_key = kwargs.get('min_header_key')
        #if min_header_key == 'Min_FWScore':
        #    current_app.logger.debug(result)
        #    current_app.logger.debug(fscore)
        #    current_app.logger.debug(cscore)
        arr.append(result)

    def getMaxScore(self,**kwargs):
        detail_key = kwargs.get("detail_key")
        score = g.db_session.query(T_Para_Detail.detail_value).filter(T_Para_Detail.detail_key ==detail_key).first()
        score = score[0]
        return score
    
    def get_grade_param(self, **kwargs):
        type_name = kwargs.get('type_name')
        min_header_key = kwargs.get('min_header_key')
        max_header_key = kwargs.get('max_header_key')
        real_data = kwargs.get('real_data')              # 实绩
        header_name = kwargs.get('header_name')          # 分值
        fscore = 0
        min_param = g.db_session.query(T_Para_Detail.detail_value).\
            join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
            join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
            filter(T_Para_Type.type_name == type_name).\
            filter(T_Para_Header.header_key == min_header_key).\
            order_by(T_Para_Detail.para_row_id).all()
        
        max_param = g.db_session.query(T_Para_Detail.detail_value).\
            join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
            join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
            filter(T_Para_Type.type_name == type_name).\
            filter(T_Para_Header.header_key == max_header_key).\
            order_by(T_Para_Detail.para_row_id).all()
       
        score = g.db_session.query(T_Para_Detail.detail_value).\
            join(T_Para_Header,T_Para_Header.id == T_Para_Detail.para_header_id).\
            join(T_Para_Type,T_Para_Type.id == T_Para_Header.para_type_id).\
            filter(T_Para_Type.type_name == type_name).\
            filter(T_Para_Header.header_name == header_name).\
            order_by(T_Para_Detail.para_row_id).all()

        if min_header_key in ['Min_FWScore','Min_CCScore','Min_LG','Min_HL','Min_MYScore','Min_YWScore','Min_WScore','Min_JScore']:
            for i in range(0,len(min_param)):
                if float(real_data) >= float(min_param[i][0]) and float(real_data) < float(max_param[i][0]):
                    fscore = score[i][0]
                    break
                else :
                    fscore = score[len(min_param)-1][0]
           #current_app.logger.debug(score)
        return fscore

    def get_totalscore(self,arr):
        total = 0
        for i in arr:
            i = float(i[0])
            total += i
        return round(total,2)
     
    def change_save(self,**kwargs):
        try:
            item_id = kwargs.get('item_id')
            adj_level = kwargs.get('adj_level')
            g.db_session.query(TellerLevel).filter(TellerLevel.id == item_id).update({TellerLevel.adj_level:adj_level,TellerLevel.last_level:adj_level})
            return u'调整等级成功'
        except Exception,e:
            return u'调整等级失败'
