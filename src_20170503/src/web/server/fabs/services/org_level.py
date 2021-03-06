#-*-coding:utf-8-*-
import datetime,xlrd
from flask import json, g,current_app
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all,aliased
from ..base import utils
from ..model import CustHook, User_ExtraScore, Branch,User,UserBranch,T_Para_Detail,UserLevel,T_Para_Header,T_Para_Type,TellerLevel,Group,UserGroup,OrgLevel,BranchGroup,Hand_Maintain,OrgPeopleCount
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
                syear = item[8][1]
                org_code = item[8][2]
                branch = g.db_session.query(OrgLevel).filter(OrgLevel.syear == syear).filter(OrgLevel.org_code == org_code).first()
                
                if branch:
                    g.db_session.query(OrgLevel).filter(OrgLevel.syear==syear).filter(OrgLevel.org_code==org_code).\
                        update({OrgLevel.syear:syear,OrgLevel.org_code:org_code,\
                        OrgLevel.yjc_rdata:str(float(item[0][1])),OrgLevel.yjc_cscore:int(float(item[0][2])),OrgLevel.yjc_weight:str(float(item[0][3])),\
                        OrgLevel.yjc_score:str(float(item[0][0])),\
                        OrgLevel.rjc_rdata:str(float(item[1][1])),OrgLevel.rjc_cscore:int(float(item[1][2])),OrgLevel.rjc_weight:str(float(item[1][3])),\
                        OrgLevel.rjc_score:str(float(item[1][0])),\
                        OrgLevel.yjd_rdata:str(float(item[2][1])),OrgLevel.yjd_cscore:int(float(item[2][2])),OrgLevel.yjd_weight:str(float(item[2][3])),\
                        OrgLevel.yjd_score:str(float(item[2][0])),\
                        OrgLevel.ebc_rdata:str(item[3][1]),OrgLevel.ebc_cscore:int(float(item[3][2])),OrgLevel.ebc_weight:str(float(item[3][3])),OrgLevel.ebc_score:str(float(item[3][0])),\
                        OrgLevel.ebr_rdata:str(item[4][1]),OrgLevel.ebr_cscore:int(float(item[4][2])),OrgLevel.ebr_weight:str(float(item[4][3])),OrgLevel.ebr_score:str(float(item[4][0])),\
                        OrgLevel.dkc_rdata:str(item[5][1]),OrgLevel.dkc_cscore:int(float(item[5][2])),OrgLevel.dkc_weight:str(float(item[5][3])),OrgLevel.dkc_score:str(float(item[5][0])),\
                        OrgLevel.wdg_rdata:str(item[6][1]),OrgLevel.wdg_cscore:int(float(item[6][2])),OrgLevel.wdg_weight:str(float(item[6][3])),OrgLevel.wdg_score:str(float(item[6][0])),\
                        OrgLevel.sbl_rdata:str(item[7][1]),OrgLevel.sbl_cscore:int(float(item[7][2])),OrgLevel.sbl_weight:str(float(item[7][3])),OrgLevel.sbl_score:str(float(item[7][0])),\
                        OrgLevel.total_score:str(float(item[8][0])),OrgLevel.sys_level:item[9][0],OrgLevel.last_level:item[9][0]})
                else:
                    g.db_session.add(OrgLevel(syear=syear,org_code=org_code,
                        yjc_rdata=str(float(item[0][1])),yjc_cscore=int(float(item[0][2])),yjc_weight=str(float(item[0][3])),yjc_score=str(float(item[0][0])),\
                        rjc_rdata=str(float(item[1][1])),rjc_cscore=int(float(item[1][2])),rjc_weight=str(float(item[1][3])),rjc_score=str(float(item[1][0])),\
                        yjd_rdata=str(float(item[2][1])),yjd_cscore=int(float(item[2][2])),yjd_weight=str(float(item[2][3])),yjd_score=str(float(item[2][0])),\
                        ebc_rdata=str(item[3][1]),ebc_cscore=int(float(item[3][2])),ebc_weight=str(float(item[3][3])),ebc_score=str(float(item[3][0])),\
                        ebr_rdata=str(item[4][1]),ebr_cscore=int(float(item[4][2])),ebr_weight=str(float(item[4][3])),ebr_score=str(float(item[4][0])),\
                        dkc_rdata=str(item[5][1]),dkc_cscore=int(float(item[5][2])),dkc_weight=str(float(item[5][3])),dkc_score=str(float(item[5][0])),\
                        wdg_rdata=str(item[6][1]),wdg_cscore=int(float(item[6][2])),wdg_weight=str(float(item[6][3])),wdg_score=str(float(item[6][0])),\
                        sbl_rdata=str(float(item[7][1])),sbl_cscore=str(float(item[7][2])),sbl_weight=str(float(item[7][3])),sbl_score=str(float(item[7][0])),\
                        total_score=str(float(item[8][0])),sys_level=item[9][0],last_level=item[9][0]))

                g.db_session.flush()
                edit_grade = g.db_session.query(OrgLevel.adj_level).filter(OrgLevel.syear==syear,OrgLevel.org_code==org_code).first()
                if not (edit_grade[0] is None):
                    g.db_session.query(OrgLevel).filter(OrgLevel.syear==syear,OrgLevel.org_code==org_code).update({OrgLevel.last_level:edit_grade[0]})
            return u'????????????'
        except Exception,e:
            print type(e)
            return u"????????????"+str(e)
    
    def affirm(self,**kwargs):
        row = g.db_session.query(OrgLevel.org_code,OrgLevel.last_level).filter(OrgLevel.syear==last_year).order_by(OrgLevel.org_code).all()
        for item in row:
            result = ur.update_org_grade(item[0],item[1])
        return result
    
    def get_rlist(self,**kwargs):
        #??????????????????
        row = g.db_session.query(OrgPeopleCount.kyear,OrgPeopleCount.org_no,OrgPeopleCount.peo_count).filter(OrgPeopleCount.kyear == last_year).order_by(OrgPeopleCount.org_no).all()
        aslist = []#?????????????????????????????????
        for r in row:
            slist = []#?????????????????????????????????
            #????????????????????????
            yrc_count = ur.dep_avg_all(r[0],r[1])
            slist.append(round(yrc_count/10000000000.00,2))
            #????????????????????????
            rrc_count = float(yrc_count)/float(r[2])
            slist.append(round(rrc_count/1000000.00,2))
            #????????????????????????
            yrd_count = ur.loan_avg_all(r[0],r[1])
            slist.append(round(float(yrd_count/10000000000.00),2))
            #?????????????????????
            ebh_count = ur.ebank_num(r[0],r[1])
            slist.append(ebh_count)
            #?????????????????????
            eb_rate = ur.ebank_percent(r[0],r[1]) 
            slist.append(eb_rate)
            #????????????
            loan_count =  ur.loan_num(r[0],r[1])
            slist.append(loan_count)
            #????????????????????????????????????
            wd_rate = ur.avg_dep_loan_percent(r[0],r[1])
            slist.append(wd_rate)
            #???????????????
            bl_rate = ur.bad_bal_percent(r[0],r[1])
            slist.append(bl_rate)
            #??????????????????
            slist.append(r[0])
            slist.append(r[1])

            aslist.append(slist)
        row2 = aslist
        alllist = []#?????????????????????????????????
        typenames=[u'???????????????????????????????????????????????????????????????',u'??????????????????????????????????????????']
        weights = msg.get_weight(**{'type_name':'??????????????????????????????????????????','header_key':'WD_GWeight'})
        fs = 0
        i=0
        for item in row2:
            perlist = []
            alllist.append(perlist)           
            #????????????????????????
            kw = {'real_data':item[0],'type_name':typenames[0],'min_header_key':'YCK_MinTotal','max_header_key':'YCK_MaxTotal','header_name':'?????????','weight':weights[0][0]}
            self.get_fscores(alllist[i],**kw)
            #?????????????????????
            kw = {'real_data':item[1],'type_name':typenames[0],'min_header_key':'RJCK_Min','max_header_key':'RJCK_Max','header_name':'?????????','weight':weights[1][0]}
            self.get_fscores(alllist[i],**kw)
            #????????????????????????
            kw = {'real_data':item[2],'type_name':typenames[0],'min_header_key':'YDK_MinTotal','max_header_key':'YDK_MaxTotal','header_name':'?????????','weight':weights[2][0]}
            self.get_fscores(alllist[i],**kw)
            #?????????????????????
            kw = {'real_data':item[3],'type_name':typenames[0],'min_header_key':'DZBank_MinCount','max_header_key':'DZBank_MaxCount','header_name':'?????????','weight':weights[3][0]}
            self.get_fscores(alllist[i],**kw)
            #?????????????????????
            kw = {'real_data':item[4],'type_name':typenames[0],'min_header_key':'DZBank_MinRate','max_header_key':'DZBank_MaxRate','header_name':'?????????','weight':weights[4][0]}
            self.get_fscores(alllist[i],**kw)
            #????????????
            kw = {'real_data':item[5],'type_name':typenames[0],'min_header_key':'DK_MinCount','max_header_key':'DK_MaxCount','header_name':'?????????','weight':weights[5][0]}
            self.get_fscores(alllist[i],**kw)
            #????????????????????????????????????
            kw = {'real_data':item[6],'type_name':typenames[0],'min_header_key':'RJCK_MinRate','max_header_key':'RJCK_MaxRate','header_name':'?????????','weight':weights[6][0]}
            self.get_fscores(alllist[i],**kw)
            #???????????????
            kw = {'real_data':item[7],'type_name':typenames[0],'min_header_key':'SJBL_MinRate','max_header_key':'SJBL_MaxRate','header_name':'?????????','weight':weights[7][0]}
            self.get_fscores(alllist[i],**kw)
            #??????
            total = self.get_totalscore(alllist[i])
            alllist[i].append((total,item[8],item[9]))      
            #??????
            kw = {'real_data':alllist[i][8][0],'type_name':typenames[1],'min_header_key':'WD_MinScore','max_header_key':'WD_MaxScore','header_name':'??????'}
            self.get_fscores(alllist[i],**kw)
            i += 1
        return alllist

    def get_fscores(self,arr,**kwargs):
        real_data = kwargs.get('real_data')
        detail_value = kwargs.get('detail_value')
        weight = kwargs.get('weight')
        header_name = kwargs.get('header_name')
        min_header_key = kwargs.get('min_header_key')
        cscore = 0
        fscore = 0
        if not real_data is None:
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
        result = (fscore,real_data,cscore,weight)
        arr.append(result)

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
        if min_header_key in ['YCK_MinTotal','RJCK_Min','YDK_MinTotal','DZBank_MinCount','DZBank_MinRate','DK_MinCount','RJCK_MinRate','WD_MinScore']:
            if float(real_data) > float(min_param[0][0]):
                fscore = score[0][0]
            for i in range(1,len(min_param)):
                if float(real_data) > float(min_param[i][0]) and float(real_data) <= float(max_param[i][0]):
                    fscore = score[i][0]
            if float(real_data) <= 0:
                fscore = score[len(min_param)-1][0]
        #????????????
        if min_header_key in ['SJBL_MinRate']:
           for i in range(1,len(min_param)):
               if float(real_data) > float(min_param[i][0]) and float(real_data) <= float(max_param[i][0]):
                   fscore = score[i][0]
           if float(real_data) <= 0:
               fscore = score[1][0]
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
            g.db_session.query(OrgLevel).filter(OrgLevel.id == item_id).update({OrgLevel.adj_level:adj_level,OrgLevel.last_level:adj_level})
            return u'??????????????????'
        except Exception,e:
            return u'??????????????????'


    def count_save(self, **kwargs):
        try:
            kyear = kwargs.get('kyear')
            org_no = kwargs.get('org_no')
            org_name = kwargs.get('org_name')
            peo_count= kwargs.get('peo_count')
            remarks = kwargs.get('remarks')
            if float(peo_count)<0:
                return "??????????????????"
 
            fx = g.db_session.query(Branch).filter(Branch.branch_code==org_no).first()
            fy = g.db_session.query(OrgPeopleCount).filter(OrgPeopleCount.org_no==org_no,OrgPeopleCount.kyear==kyear).first()
            if not fx:
                return u'?????????????????????'
            if fy:
                return u'?????????????????????'

            g.db_session.add(OrgPeopleCount(kyear=kyear, org_no=org_no, peo_count=peo_count, remarks=remarks))
            return u'???????????????'
        except Exception,e:
            print type(e),Exception,'OrgPeopleCount:count_save'
            return str(e)
 

    def count_edit_save(self, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            kyear = kwargs.get('kyear')
            org_no = kwargs.get('org_no')
            org_name = kwargs.get('org_name')
            peo_count= kwargs.get('peo_count')
            remarks = kwargs.get('remarks')
            if float(peo_count)<0:
                return "??????????????????"

            g.db_session.query(OrgPeopleCount).filter(OrgPeopleCount.id == item_id).update({OrgPeopleCount.kyear:kyear, OrgPeopleCount.org_no:org_no,  OrgPeopleCount.peo_count:peo_count, OrgPeopleCount.remarks:remarks})
            return u'???????????????'
        except Exception, e:
            return str(e)

    def conunt_del(sel, **kwargs):
        try:
            row_id = kwargs.get('row_id')

            g.db_session.query(OrgPeopleCount).filter(OrgPeopleCount.id == row_id).delete()

            return u'???????????????'
        except Exception, e:
            return u'???????????????'

    def count_upload(self, filepath, filename):
        """
            ????????????
        """
        print '????????????'
        try:
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)

            nrows = sheet.nrows
            if nrows in [0, 1]:
                raise Exception(u"??????:????????????")
            bill_type_sign = ""
            list = []
        except Exception, e:
            return str(e)
        all_msg = []
        souser = []
        for r in range(1, nrows):
            try:
                kyear = str(int(sheet.cell(r, 0).value))
                org_no = str(int(sheet.cell(r, 1).value))
                org_name = str(sheet.cell(r,2).value)
                peo_count = str(float(sheet.cell(r,3).value))
                remarks = str(sheet.cell(r, 4).value)
                kyear = kyear[0:4]
                if len(kyear)<4:
                    e = u'???'+str(r+1)+u'??????????????????????????????'
                    raise Exception(e)
                if len(org_no) < 6 or len(org_no) > 7:
                    e = u'???'+str(r+1)+u'??????????????????????????????'
                    raise Exception(e)
                if float(peo_count) < 0:
                    e = u'???'+str(r+1)+u'?????????????????????'
                    raise Exception(e)
                
                temp = {'kyear': kyear[0:4],
                        'org_no': org_no,
                        'peo_count': peo_count,
                        'remarks': remarks,
                }
                fx = g.db_session.query(Branch).filter(Branch.branch_code==org_no).first()
                fy = g.db_session.query(OrgPeopleCount).filter(OrgPeopleCount.org_no==org_no,OrgPeopleCount.kyear==kyear).first()
                if not fx:
                    return u'???'+str(r+1)+u'???,??????'+u'?????????????????????'
                if fy:
                    return u'???'+str(r+1)+u'???,??????'+str(org_no)+u'???'+str(kyear)+u'??????????????????'
                all_msg.append(temp)
                key = str(kyear)+str(org_no)
                if key in souser:
                    return u'???'+str(r+1)+u'???????????????????????????????????????'
                else:
                    souser.append(key)
            except ValueError, e:
                g.db_session.rollback()
                return u'???'+str(r + 1) + u'????????????'+str(e)+u"?????????????????????????????????????????????,??????????????????????????????"
            except IndexError,e:
                g.db_session.rollback()
                return u'???'+str(r+1)+u'????????????,???????????????'
            except Exception, e:
                g.db_session.rollback()
                print Exception, ':', e
                return u'???'+str(r+1)+u'????????????:'+str(e)
        for i in range(0,len(all_msg)):
            g.db_session.add(OrgPeopleCount(**all_msg[i]))
        return u'????????????'
