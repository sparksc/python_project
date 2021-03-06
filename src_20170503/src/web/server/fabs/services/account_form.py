#-*-coding:utf-8-*-
import datetime,xlrd
from flask import json, g, current_app
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all,aliased
from ..base import utils
from ..model import CustHook, User_ExtraScore, Account_Rank,Branch,User,UserBranch,T_Para_Detail,UserLevel,T_Para_Header,T_Para_Type,TellerLevel,AccountForm,Group,UserGroup
from man_gradejdg import Man_gradejdgService
from userreport import UserReport
import datetime

msg = Man_gradejdgService()
ur = UserReport()
local_year,last_year,local_startday,last_endday = ur.get_year_day()
class Account_formService():
    def calculate(self,**kwargs):
        rlist = self.get_rlist()
        for item in rlist:
            syear = item[0][2]
            user_code = item[0][1]
            user = g.db_session.query(AccountForm).filter(AccountForm.syear == syear).filter(AccountForm.user_code == user_code).first()

            if user:
                g.db_session.query(AccountForm).filter(AccountForm.syear==syear).filter(AccountForm.user_code==user_code).\
                update({AccountForm.syear:syear,AccountForm.user_code:user_code,\
                AccountForm.count_rdata:item[1][1],AccountForm.count_cscore:str(float(item[1][2])),AccountForm.count_weight:str(float(item[1][3])),AccountForm.count_score:str(float(item[1][0])),\
                AccountForm.mis_rdata:item[2][1],AccountForm.mis_cscore:str(float(item[2][2])),AccountForm.mis_weight:str(float(item[2][3])),AccountForm.mis_score:str(float(item[2][0])),\
                AccountForm.ball_rdata:item[3][1],AccountForm.ball_cscore:str(float(item[3][2])),AccountForm.ball_weight:str(float(item[3][3])),AccountForm.ball_score:str(float(item[3][0])),\
                AccountForm.basic_rdata:item[4][1],AccountForm.basic_cscore:str(float(item[4][2])),AccountForm.basic_weight:str(float(item[4][3])),AccountForm.basic_score:str(float(item[4][0])),\
                AccountForm.yrank_rdata:item[5][1],AccountForm.yrank_cscore:str(float(item[5][2])),AccountForm.yrank_weight:str(float(item[5][3])),AccountForm.yrank_score:str(float(item[5][0])),\
                AccountForm.wrong_rdata:item[6][1],AccountForm.wrong_cscore:str(float(item[6][2])),AccountForm.wrong_weight:str(float(item[6][3])),AccountForm.wrong_score:str(float(item[6][0])),\
                AccountForm.comp_rdata:item[7][1],AccountForm.comp_cscore:str(float(item[7][2])),AccountForm.comp_weight:str(float(item[7][3])),AccountForm.comp_score:str(float(item[7][0])),\
                AccountForm.skill_rdata:item[8][1],AccountForm.skill_cscore:str(float(item[8][2])),AccountForm.skill_weight:str(float(item[8][3])),AccountForm.skill_score:str(float(item[8][0])),\
                AccountForm.edu_rdata:item[9][1],AccountForm.edu_cscore:str(float(item[9][2])),AccountForm.edu_weight:str(float(item[9][3])),AccountForm.edu_score:str(float(item[9][0])),\
                AccountForm.exper_rdata:item[10][1],AccountForm.exper_cscore:str(float(item[10][2])),AccountForm.exper_weight:str(float(item[10][3])),AccountForm.exper_score:str(float(item[10][0])),\
                AccountForm.extra_score:str(float(item[0][0])),AccountForm.total_score:str(float(item[11][0])),\
                AccountForm.sys_level:item[12][0],AccountForm.last_level:item[12][0]})                
            else:
                g.db_session.add(AccountForm(syear=syear,user_code=user_code,count_rdata=item[1][1],count_cscore=str(float(item[1][2])),count_weight=str(float(item[1][3])),count_score=str(float(item[1][0])),\
                mis_rdata=item[2][1],mis_cscore=str(float(item[2][2])),mis_weight =str(float(item[2][3])),mis_score=str(float(item[2][0])),\
                ball_rdata=item[3][1],ball_cscore=str(float(item[3][2])),ball_weight=str(float(item[3][3])),ball_score=str(float(item[3][0])),\
                basic_rdata=item[4][1],basic_cscore=str(float(item[4][2])),basic_weight=str(float(item[4][3])),basic_score=str(float(item[4][0])),\
                yrank_rdata=item[5][1],yrank_cscore=str(float(item[5][2])),yrank_weight=str(float(item[5][3])),yrank_score=str(float(item[5][0])),\
                wrong_rdata=item[6][1],wrong_cscore=str(float(item[6][2])),wrong_weight=str(float(item[6][3])),wrong_score=str(float(item[6][0])),\
                comp_rdata=item[7][1],comp_cscore=str(float(item[7][2])),comp_weight=str(float(item[7][3])),comp_score=str(float(item[7][0])),\
                skill_rdata=item[8][1],skill_cscore=str(float(item[8][2])),skill_weight=str(float(item[8][3])),skill_score=str(float(item[8][0])),\
                edu_rdata=item[9][1],edu_cscore=str(float(item[9][2])),edu_weight=str(float(item[9][3])),edu_score=str(float(item[9][0])),\
                exper_rdata=item[10][1],exper_cscore=str(float(item[10][2])),exper_weight=str(float(item[10][3])),exper_score=str(float(item[10][0])),\
                extra_score=str(float(item[0][0])),total_score=str(float(item[11][0])),sys_level=item[12][0],last_level=item[12][0]))
            g.db_session.flush()
            edit_grade = g.db_session.query(AccountForm.adj_level).filter(AccountForm.syear==syear,AccountForm.user_code==user_code).first()
            if edit_grade[0] is not None:
                g.db_session.query(AccountForm).filter(AccountForm.syear==syear,AccountForm.user_code==user_code).update({AccountForm.last_level:edit_grade[0]})
        return u'??????'

    def affirm(self,**kwargs):
        row = g.db_session.query(AccountForm.user_code,AccountForm.last_level).order_by(AccountForm.user_code).all()
        for item in row:
            if item[1] == '??????????????????':
                rank = '??????'
            elif item[1] == '??????????????????':
                rank = '??????'
            elif item[1] == '??????????????????':
                rank = '??????'
            ur.check_update_his(last_endday,local_startday,item[0],rank)
            return "????????????????????????"
            """
            #??????user_id
            r_id = g.db_session.query(User.role_id).filter(User.user_name==item[0]).first()
            #??????group_id
            g_id = g.db_session.query(Group.id).filter(Group.group_name == item[1]).first()
            print g_id
            return u'OK'
            rg = g.db_session.query(UserGroup).filter(UserGroup.user_id==r_id[0]).first()
            if rg:
                g.db_session.query(UserGroup).filter(UserGroup.user_id==r_id[0]).update({UserGroup.user_id:r_id[0],UserGroup.group_id:g_id[0]})
            else:
                g.db_session.add(UserGroup(user_id=r_id[0],group_id=g_id[0]))
            """


    def get_rlist(self,**kwargs):
        row = g.db_session.query(Account_Rank.syear,Account_Rank.user_code,Account_Rank.mis_rank,Account_Rank.basic_rank,Account_Rank.ryear,Account_Rank.score_rank,Account_Rank.repleace_rank,Account_Rank.skill,User.edu,Account_Rank.experience,Account_Rank.org_code).filter(User.user_name==Account_Rank.user_code).filter(Account_Rank.syear == last_year).order_by(Account_Rank.user_code).all()
        alllist = []#?????????????????????????????????
        param1 = {'type_name':'????????????????????????','real_data':'','detail_key':'extra_code'}
        param2 = {'type_name':'??????????????????????????????','detail_key':'Max_ExtraScore'}
        maxscore = self.getMaxScore(**param2)
        weights = msg.get_weight(**{'type_name':'????????????????????????????????????','header_key':'weight'})
        i = 0
        for item in row:
            syear = item[0]
            user_code = item[1]
            branch_code = item[10]
            extra_row = g.db_session.query(User_ExtraScore.credential_code).join(User,User.user_name == user_code).filter(User_ExtraScore.user_code == user_code).filter(User_ExtraScore.syear <= syear).all()
            branch_num = ur.org_num(branch_code)
            ranking = ur.org_ranking(branch_code)
            fscore = 0
            cscore = 0
            for ta in range(0,len(extra_row)):
                if extra_row:
                    if not extra_row[ta][0]:
                        cscore = 0
                    else:
                        param1['real_data'] = extra_row[ta][0]
                        fscore = msg.grade_param(**param1)
                        cscore=cscore+float(fscore)

            if float(cscore) > float(maxscore):
                cscore = float(maxscore)       
           
            perlist = []
            result = (cscore,user_code,syear)
            perlist.append(result)
            alllist.append(perlist)
            print u'alllist:',alllist
           
            #??????????????????
            kw = {'real_data':branch_num,'type_name':u'???????????????????????????????????????????????????','min_header_key':'net_lownum','max_header_key':'net_highnum','header_name':'??????','weight':weights[0][0]}
            self.get_fscores(alllist[i],**kw)

            #?????????
            kw = {'real_data':item[2],'type_name':u'???????????????????????????????????????????????????','min_header_key':'mis_lowrank','max_header_key':'mis_highrank','header_name':'??????','weight':weights[1][0]}
            self.get_fscores(alllist[i],**kw)

            #????????????????????????
            kw = {'real_data':ranking,'type_name':u'???????????????????????????????????????????????????','min_header_key':'all_lowrank','max_header_key':'all_highrank','header_name':'??????','weight':weights[2][0]}
            self.get_fscores(alllist[i],**kw)

            #??????????????????????????????????????????
            kw = {'real_data':item[3],'type_name':u'???????????????????????????????????????????????????','detail_key':'score','detail_value':u'??????????????????????????????????????????','weight':weights[3][0]}
            self.get_fscores(alllist[i],**kw)

            #??????
            kw = {'real_data':item[4],'type_name':u'???????????????????????????????????????????????????','min_header_key':'lowyear','max_header_key':'highyear','header_name':'??????','weight':weights[4][0]}
            self.get_fscores(alllist[i],**kw)

            #????????????????????????
            kw = {'real_data':item[5],'type_name':u'???????????????????????????????????????????????????','min_header_key':'integration_lowrank','max_header_key':'integration_highrank','header_name':'??????','weight':weights[5][0]}
            self.get_fscores(alllist[i],**kw)

            #???????????????
            kw = {'real_data':item[6],'type_name':u'???????????????????????????????????????????????????','min_header_key':'etc_lowrank','max_header_key':'etc_highrank','header_name':'??????','weight':weights[6][0]}
            self.get_fscores(alllist[i],**kw)
            
            #???????????????????????????????????????????????????
            kw = {'real_data':item[7],'type_name':u'???????????????????????????????????????????????????','detail_key':'score','detail_value':u'???????????????????????????????????????????????????','weight':weights[7][0]}
            self.get_fscores(alllist[i],**kw)

            #????????????
            if item[8]=='??????': 
                a='???????????????'
                
                kw = {'real_data':a,'type_name':u'???????????????????????????????????????????????????','detail_key':'score','detail_value':u'????????????????????????','weight':weights[8][0]}
                self.get_fscores(alllist[i],**kw)

            elif item[8]=='???????????????':
                b='???????????????'
                
                kw = {'real_data':b,'type_name':u'???????????????????????????????????????????????????','detail_key':'score','detail_value':u'????????????????????????','weight':weights[8][0]}
                self.get_fscores(alllist[i],**kw)
            else:
                kw = {'real_data':item[8],'type_name':u'???????????????????????????????????????????????????','detail_key':'score','detail_value':u'????????????????????????','weight':weights[8][0]}
                self.get_fscores(alllist[i],**kw)
            
            #????????????       
            kw = {'real_data':item[9],'type_name':u'???????????????????????????????????????????????????','min_header_key':'low_experience','max_header_key':'high_experience','header_name':'??????','weight':weights[9][0]}
            self.get_fscores(alllist[i],**kw)
            
            #??????
            total = self.get_totalscore(alllist[i])
            alllist[i].append((total,0))            

            #??????
            kw = {'real_data':alllist[i][11][0],'type_name':u'??????????????????????????????','min_header_key':'low_integration','max_header_key':'high_integration','header_name':'??????'}
            self.get_fscores(alllist[i],**kw)
            print u'kw9',kw
            i += 1
            print  u'????????????',alllist,len(alllist)
        return alllist

    def get_fscores(self,arr,**kwargs):
        real_data = kwargs.get('real_data')
        detail_value = kwargs.get('detail_value')
        weight = kwargs.get('weight')
        header_name = kwargs.get('header_name')
        cscore=0
        if real_data:
            if not detail_value:
                cscore = self.get_grade_param(**kwargs)
            else:
                cscore = msg.grade_param(**kwargs)
            if cscore == None:
                cscore = 0

            if header_name != '??????':
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
        real_data = kwargs.get('real_data')              # ??????
        header_name = kwargs.get('header_name')          # ??????
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

        if min_header_key in ['net_lownum','mis_lowrank','all_lowrank','lowyear','integration_lowrank','etc_lowrank','low_experience','low_integration']:
            for i in range(0,len(min_param)):
                if float(real_data) >= float(min_param[i][0]) and float(real_data) < float(max_param[i][0]):
                    fscore = score[i][0]
        return fscore

    def get_totalscore(self,arr):
        total = 0
        for i in range(0,len(arr)-1):
            sco = float(arr[i][0])
            total = total + sco
        return round(total,2)

    def change_save(self,**kwargs):
        try:
            item_id = kwargs.get('item_id')
            adj_level = kwargs.get('adj_level')
            g.db_session.query(AccountForm).filter(AccountForm.id == item_id).update({AccountForm.adj_level:adj_level,AccountForm.last_level:adj_level})
            return u'??????????????????'
        except Exception,e:
            print type(e),Exception,'11111111111111111111111111111111111111'
            return u'??????????????????'


    def getNetsum():
        
        return netsum

    def getAllb():
        
        return allb
