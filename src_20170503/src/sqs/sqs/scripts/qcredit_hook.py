# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
import calendar
"""
信用卡不良
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist, date_id = self.make_eq_filterstr()
        sql ="""select MTHS_ODUE, STM_BALFRE, STM_BALINT, STM_BALMP, BAL_FREE, BAL_INT, BAL_MP, MP_REM_PPL,STMBALINT_FLAG, BAL_INT_FLAG from f_credit_bad
            """%(filterstr)
        year, month, day = self.get_date_year_month_day(date_id) 
        ##计算年度初始日期到当前的月份差,天数差
        month_dif, day_dif = self.get_month_day_dif(date_id)
        ##取公司贷款余额/户数折算比例
        rate_month_balance, rate_month_number, rate_add_number, rate_add_balance, rate_day_balance = self.get_man_loan_rewards_rate_para()
        ##取根据不良率及4个上浮比例金额计算参数
        (min_percent1, max_percent1, min_items1, up_percent1, money1, min_percent2, max_percent2, min_items2, up_percent2, money2) =  self.get_man_loan_rewards_money_para()
        ##取当天客户经理人数
        manager_count = self.get_manager_counts(date_id)
        ##取月均责任管贷余额平均值
        all_avg_balance = self.get_all_month_avg_balance(rate_month_balance, month_dif, manager_count, date_id, year)
        ##取管贷户数平均值
        all_avg_number = self.get_all_month_avg_number(rate_month_number, month_dif, manager_count, date_id, year)
        ##取新增管贷户数平均值
        add_avg_number = self.get_add_month_avg_number(rate_add_number, manager_count, date_id)
        ##取新增责任管贷余额平均值
        add_avg_balance = self.get_add_month_avg_balance(rate_add_balance, manager_count, date_id)
        ##取日均责任管贷余额平均值
        day_avg_balance = self.get_day_avg_balance(rate_day_balance, day_dif, manager_count, date_id, year)
        vlist.append(date_id)
        vlist.append(month_dif)
        vlist.append(month_dif)
        vlist.append(month_dif)
        vlist.append(rate_month_balance)
        vlist.append(month_dif)
        vlist.append(rate_month_balance)
        vlist.append(month_dif)
        vlist.append(all_avg_balance)
        vlist.append(all_avg_balance)
        vlist.append(year)
        vlist.append(date_id)
        vlist.append(month_dif)
        vlist.append(month_dif)
        vlist.append(month_dif)
        vlist.append(rate_month_number)
        vlist.append(month_dif)
        vlist.append(rate_month_number)
        vlist.append(month_dif)
        vlist.append(all_avg_number)
        vlist.append(all_avg_number)
        vlist.append(year)
        vlist.append(date_id)
        vlist.append(add_avg_number)
        vlist.append(add_avg_number)
        vlist.append(rate_add_number)
        vlist.append(date_id)
        vlist.append(rate_add_number)
        vlist.append(date_id)
        vlist.append(add_avg_balance)
        vlist.append(add_avg_balance)
        vlist.append(rate_add_balance)
        vlist.append(date_id)
        vlist.append(rate_add_balance)
        vlist.append(date_id)
        vlist.append(day_dif)
        vlist.append(day_dif)
        vlist.append(day_dif)
        vlist.append(rate_day_balance)
        vlist.append(day_dif)
        vlist.append(rate_day_balance)
        vlist.append(day_dif)
        vlist.append(day_avg_balance)
        vlist.append(day_avg_balance)
        vlist.append(date_id)
        vlist.append(year)
        vlist.append(date_id)
        vlist.append(date_id)
        print vlist
        print sql
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        rowlist=[]
        tt=[5, 6, 7, 8, 20, 21, 22, 23, 26, 27, 28, 29, 31, 32]
        for i in row:
            t=list(i[0:5])
            for j in i[5:]:
                if j is None:j=0
                if list(i).index(j) in tt:
                    j=self.amount_trans_dec(j)
                else:
                    j=j
                t.append(j)
            ##这里补足平均值
            t.insert(9, self.amount_trans_dec(all_avg_balance/100))
            t.insert(15, all_avg_number)
            t.insert(21, add_avg_number)
            t.insert(27, self.amount_trans_dec(add_avg_balance/100))
            ##这里进行判断是否满足奖励条件
            ##1. 不良率 0-0.3(含) 4个上浮比率有2个达到30, 3000元
            flag1, count1 = self.get_first_rewards(t, min_percent1, max_percent1, up_percent1, min_items1)
            flag2, count2 = self.get_secend_rewards(t, min_percent2, max_percent2, up_percent2, min_items2)

            t.insert(29, count1)
            if flag1:
                t.insert(31, self.amount_trans_dec(money1))
            else:
                t.insert(31, self.amount_trans_dec(0))

            ##2. 不良率 0.3-0.5(含) 4个上浮比率有2个达到20, 2000元
            t[30] =  count2
            if flag2:
                t[31] =  self.amount_trans_dec(money2)
            else:
                if not flag1:
                    t[31] =  self.amount_trans_dec(0)

            t.insert(36, self.amount_trans_dec(day_avg_balance/100))

            ##3. 无不良,无新增应收利息,无经济案件笔数, 2000元
            flag3, count3 = self.get_third_rewards(t)
            if flag3:
                t.insert(41, self.amount_trans_dec(int(2000)))
            else:
                t.insert(41, self.amount_trans_dec(int(0)))

            t.insert(42, self.amount_trans_dec(  int(float(t[31].replace(',', ''))) + int(float(t[41].replace(',', ''))) ) )
            rowlist.append(t) 
        return self.translate(rowlist, needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            print k,v
            if k == 'login_teller_no':
                if self.deal_teller_query_auth(v) == True:
                    filterstr = filterstr+" and SALE_CODE = '%s'"%v
            elif k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" and ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)

                if k == 'DATE_ID':
                   date_id = v
        return filterstr,vlist, date_id

    def get_man_loan_rewards_rate_para(self):
        sql = """ 
            select row_id,
            max(case  when HEADER_NAME='考察项' then DETAIL_VALUE else '' end) as 考察项,
            max(case when a.HEADER_NAME = '折算类型' then DETAIL_VALUE else '' end) as 折算类型,
            max(case when  a.HEADER_NAME = '折算值' then DETAIL_VALUE else '' end) as 折算值
            from
            (select r.id as row_id,HEADER_NAME, d.DETAIL_VALUE from  t_para_type t, t_para_header h, t_para_row r, t_para_detail d
            where t.id = h.PARA_TYPE_ID and t.id = r.PARA_TYPE_ID and h.id = d.PARA_HEADER_ID and r.id = d.PARA_ROW_ID and t.TYPE_NAME = '客户经理贷款奖励折算参数' )a
            group by row_id 
            """
        row = self.engine.execute(sql, []).fetchall()
        for i in row:
            if i[1] == u'月均责任管贷余额':
                rate_month_balance = float(i[3]) 
            elif i[1] == u'管带户数':
                rate_month_number = float(i[3]) 
            elif i[1] == u'当年新增户数':
                rate_add_number = float(i[3]) 
            elif i[1] == u'当年新增责任贷款余额':
                rate_add_balance = float(i[3]) 
            elif i[1] == u'当年日均责任贷款余额':
                rate_day_balance = float(i[3]) 
        return (rate_month_balance, rate_month_number, rate_add_number, rate_add_balance, rate_day_balance)

    def get_man_loan_rewards_money_para(self):
        sql = """ 
            select row_id,
            max(case  when HEADER_NAME='不良贷款最小占比' then DETAIL_VALUE else '' end) as 不良贷款最小占比,
            max(case  when HEADER_NAME='不良贷款最大占比' then DETAIL_VALUE else '' end) as 不良贷款最大占比,
            max(case  when HEADER_NAME='考察项' then DETAIL_VALUE else '' end) as 考察项,
            max(case when a.HEADER_NAME = '最小考察项目数量' then DETAIL_VALUE else '' end) as 最小考察项目数量,
            max(case when  a.HEADER_NAME = '在全行平均数上浮比例' then DETAIL_VALUE else '' end) as 在全行平均数上浮比例,
            max(case when  a.HEADER_NAME = '奖励金额' then DETAIL_VALUE else '' end) as 奖励金额
            from
            (select r.id as row_id,HEADER_NAME, d.DETAIL_VALUE from  t_para_type t, t_para_header h, t_para_row r, t_para_detail d
            where t.id = h.PARA_TYPE_ID and t.id = r.PARA_TYPE_ID and h.id = d.PARA_HEADER_ID and r.id = d.PARA_ROW_ID and t.TYPE_NAME = '客户经理贷款奖励金额参数' )a
            group by row_id order by 不良贷款最小占比 asc
            """
        row = self.engine.execute(sql, []).fetchall()
        min_percent1 = float(row[0][1]) 
        max_percent1 = float(row[0][2]) 
        min_items1 = int(row[0][4]) 
        up_percent1 = float(row[0][5]) 
        money1 = float(row[0][6]) 

        min_percent2 = float(row[1][1]) 
        max_percent2 = float(row[1][2]) 
        min_items2 = int(row[1][4]) 
        up_percent2 = float(row[1][5]) 
        money2 = float(row[1][6]) 
        return (min_percent1, max_percent1, min_items1, up_percent1, money1, min_percent2, max_percent2, min_items2, up_percent2, money2)

    def get_manager_counts(self, date_id):
        #sql = """SELECT count(SALE_CODE) FROM REPORT_MANAGER_LOAN WHERE DATE_ID = ? and length(SALE_CODE) = 7 """
        sql = """ select count(*) from f_user f, group_type gt, group g, user_group ug where f.role_id = ug.user_id and f.WORK_STATUS = '在职' and f.is_virtual = '否'
                and ug.enddate is null and g.id = ug.group_id and g.group_type_code = gt.type_code and gt.type_name = '客户经理类别' and g.group_name = '客户经理'
              """
        manager_count = self.engine.execute(sql, []).fetchall()[0]
        return int(manager_count[0])

    def get_all_month_avg_balance(self, rate, month_dif, manager_count, date_id, year):
        sql = """ SELECT bigint( nvl((sum(nvl(DSZRYE,0))+sum(nvl(DGZRYE, 0) * ? / 100))/? / ?, 0) ) FROM YDW.REPORT_MANAGER_LOAN  
                  WHERE DATE_ID in(SELECT distinct MONTHEND_ID FROM D_DATE WHERE YEAR = ? AND ID <= ? order by MONTHEND_ID asc) and length(sale_code) = 7 and (DGZRYE <> 0 or DSZRYE<> 0) """
        avg_balance = self.engine.execute(sql, [rate, month_dif, manager_count, year, date_id]).fetchall()[0]
        return float(avg_balance[0])

    def get_all_month_avg_number(self, rate, month_dif, manager_count, date_id, year):
        sql = """ SELECT nvl((sum(nvl(PRI_THIS_STANDARD_NUM,0))+sum(nvl(PUB_THIS_STANDARD_NUM, 0) * ?)) / ? / ?, 0) FROM YDW.REPORT_MANAGER_LOAN
                  WHERE date_id in(SELECT distinct MONTHEND_ID FROM D_DATE WHERE YEAR = ? AND ID <= ? order by MONTHEND_ID asc) 
                  and (PRI_THIS_STANDARD_NUM > 0 or PUB_THIS_STANDARD_NUM > 0)
              """
        avg_number = self.engine.execute(sql, [rate, month_dif, manager_count, year, date_id]).fetchall()[0]
        return float(avg_number[0])

    def get_add_month_avg_number(self, rate, manager_count, date_id):
        sql = """ 
                SELECT  
                    nvl(sum(nvl(AA.当前合计折算后 - BB.上年合计折算后, 0)) / ?, 0)
                FROM
                    (SELECT  SALE_CODE, SALE_NAME, sum(nvl(PUB_THIS_STANDARD_NUM,0)) 当前公司户数, sum(nvl(PRI_THIS_STANDARD_NUM,0)) 当前个人户数, sum(nvl(PRI_THIS_STANDARD_NUM,0))+sum(nvl(PUB_THIS_STANDARD_NUM,0)) 当前合计折算前, sum(nvl(PRI_THIS_STANDARD_NUM,0))+sum(nvl(PUB_THIS_STANDARD_NUM, 0) * ?) 当前合计折算后 FROM YDW.REPORT_MANAGER_LOAN
                    WHERE date_id = ? and (PRI_THIS_STANDARD_NUM > 0 or PUB_THIS_STANDARD_NUM > 0)
                    group by  SALE_CODE, SALE_NAME)AA
                LEFT JOIN
                    (SELECT  SALE_CODE, SALE_NAME, sum(nvl(PUB_THIS_STANDARD_NUM,0)) 上年公司户数, sum(nvl(PRI_THIS_STANDARD_NUM,0)) 上年个人户数, sum(nvl(PRI_THIS_STANDARD_NUM,0))+sum(nvl(PUB_THIS_STANDARD_NUM,0)) 上年合计折算前, sum(nvl(PRI_THIS_STANDARD_NUM,0))+sum(nvl(PUB_THIS_STANDARD_NUM, 0) * ?) 上年合计折算后 FROM YDW.REPORT_MANAGER_LOAN
                    WHERE date_id in (SELECT L_YEAREND_ID FROM D_DATE WHERE ID = ?) and (PRI_THIS_STANDARD_NUM > 0 or PUB_THIS_STANDARD_NUM > 0)
                    group by  SALE_CODE, SALE_NAME)BB 
                ON AA.SALE_CODE = BB.SALE_CODE
              """
        avg_number = self.engine.execute(sql, [manager_count, rate, date_id, rate, date_id]).fetchall()[0]
        return float(avg_number[0])

    def get_add_month_avg_balance(self, rate, manager_count, date_id):
        sql = """ 
                SELECT
                    nvl(sum((nvl(AB.当前合计折算后, 0) - nvl(BA.上年合计折算后, 0))) / ?, 0)
                FROM
                    (SELECT  SALE_CODE, SALE_NAME, sum(nvl(DGZRYE,0)) 当前公司余额, sum(nvl(DSZRYE,0)) 当前个人余额, (sum(nvl(DSZRYE,0))+sum(nvl(DGZRYE,0))) 当前合计折算前, (sum(nvl(DSZRYE,0))+sum(nvl(DGZRYE, 0) * ? / 100)) 当前合计折算后   FROM YDW.REPORT_MANAGER_LOAN
                    WHERE date_id = ? and (DSZRYE > 0 or DGZRYE > 0) and length(SALE_CODE) = 7
                    group by  SALE_CODE, SALE_NAME)AB
                LEFT JOIN
                    (SELECT  SALE_CODE, SALE_NAME, sum(nvl(DGZRYE,0))  上年公司余额, sum(nvl(DSZRYE,0)) 上年个人余额, (sum(nvl(DSZRYE,0))+sum(nvl(DGZRYE,0))) 上年合计折算前, (sum(nvl(DSZRYE,0))+sum(nvl(DGZRYE, 0) * ? / 100)) 上年合计折算后   FROM YDW.REPORT_MANAGER_LOAN
                    WHERE date_id in (SELECT L_YEAREND_ID FROM D_DATE WHERE ID = ?) and (DSZRYE > 0 or DGZRYE > 0) and length(SALE_CODE) = 7
                    group by  SALE_CODE, SALE_NAME)BA
                ON AB.SALE_CODE = BA.SALE_CODE
              """
        avg_balance = self.engine.execute(sql, [manager_count, rate, date_id, rate, date_id]).fetchall()[0]
        return float(avg_balance[0])

    def get_day_avg_balance(self, rate, day_dif, manager_count, date_id, year):
        sql = """
                SELECT  bigint( nvl(sum((nvl(DSZRYE,0) + nvl(DGZRYE, 0) * ? / 100) / ?) / ?, 0) )   from YDW.REPORT_MANAGER_LOAN
                WHERE date_id in ( SELECT ID FROM D_DATE WHERE YEAR = ? AND ID <= ? ) and (DSZRYE > 0 or DGZRYE > 0) and length(SALE_CODE) = 7"""
        avg_balance = self.engine.execute(sql, [rate, day_dif, manager_count, year, date_id]).fetchall()[0]
        return float(avg_balance[0])

    def get_month_day_dif(self, date_id):
        sql = """ SELECT MONTH, BEG_YEAR_DAYS ID FROM D_DATE WHERE ID = ?"""
        row = self.engine.execute(sql, [date_id]).fetchall()[0]
        return int(row[0]),  int(row[1])

    def get_date_year_month_day(self, date_id):
        year = int(date_id[0:4])
        month = int(date_id[4:6])
        day = int(date_id[6:8])
        return year, month, day

    def get_first_rewards(self, t, min_percent, max_percent, up_percent, min_items):
        count = 0
        ratelist = [t[10], t[16], t[22], t[28], t[37]]
        if t[4] >= Decimal(min_percent) and t[4] <= Decimal(max_percent):
            for v in ratelist:
                if v >= Decimal(up_percent):
                    count = count + 1
        if count >= int(min_items):
            return True, count
        else:
            return False, count

    def get_secend_rewards(self, t, min_percent, max_percent, up_percent, min_items):
        count = 0
        ratelist = [t[10], t[16], t[22], t[28], t[37]]
        if t[4] > Decimal(min_percent) and t[4] <= Decimal(max_percent):
            for v in ratelist:
                if v >= Decimal(up_percent):
                    count = count + 1
        if count >= int(min_items):
            return True, count
        else:
            return False, count

    def get_third_rewards(self, t):
        count = 0
        ratelist = [t[38], t[39], t[40]]
        for v in ratelist:
            v = int(float(str(v).replace(',', '')))
            if v == 0:
                count = count + 1

        if count >= 3:
            return True, count
        else:
            return False, count

    def column_header(self):
        return ["机构编号", "机构名称", "客户经理员工号", "员工姓名", "总卡数", "不良卡数", "不良余额"]

    @property
    def page_size(self):
        return  15 
