# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
"""
员工基本信息维护
"""

class Query(ObjectQuery):

    def prepare_object(self):
        filterlist = ['org','SALE_CODE','WORK_STATUS','IS_VIRTUAL','STAFF_NAME','POSITION','MANAGE_TYPE','DEPARTMENT']
        filterstr,vlist = self.make_eq_filterstr(filterlist)
        sql ="""
        select ug.STARTDATE,fu.USER_NAME,fu.NAME,fu.ID_NUMBER,b.BRANCH_NAME,fu.IS_SAFE,fu.WORK_STATUS,gt.TYPE_NAME,g.GROUP_NAME,fu.ROLE_ID,ub.ID,ug.ID,fu.is_test,fu.is_virtual,ub.BRANCH_ID,fu.EDU,fu.IS_HEADMAN from F_USER fu
        left join USER_BRANCH ub on ub.USER_ID=fu.ROLE_ID
        left join BRANCH b on b.ROLE_ID=ub.BRANCH_ID
        left join USER_GROUP ug on ug.USER_ID=fu.ROLE_ID 
        left join "GROUP" g on g.ID=ug.GROUP_ID
        left join GROUP_TYPE gt on gt.TYPE_CODE=g.GROUP_TYPE_CODE
        where 1=1 %s 
        """%(filterstr)

       
        print sql
        rs={}
        row = self.engine.execute(sql,vlist).fetchall()
       
        for i in  row:
            if i[1] in rs:
                if i[7]==u'人员性质':
                    rs[i[1]][3]=i[8]
                    rs[i[1]][14]=i[11]
                if i[7]==u'部门':
                    rs[i[1]][6]=i[8]
                    rs[i[1]][15]=i[11]
                if i[7]==u'职务':
                    rs[i[1]][7]=i[8]
                    rs[i[1]][16]=i[11]
                    rs[i[1]][0]=i[0]
                if i[7]==u'等级':
                    rs[i[1]][8]=i[8]
                    rs[i[1]][17]=i[11]
                if i[7]==u'客户经理类别':
                    rs[i[1]][9]=i[8]
                    rs[i[1]][18]=i[11]
            else:
                temp=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                temp[1]=i[1]
                temp[2]=i[2]
                if i[7]==u'人员性质':
                    temp[3]=i[8]
                    temp[14]=i[11]
                temp[4]=i[3]
                temp[5]=i[4]
                if i[7]==u'部门':
                    temp[6]=i[8]
                    temp[15]=i[11]
                if i[7]==u'职务':
                    temp[7]=i[8]
                    temp[16]=i[11]
                    temp[0]=i[0]
                if i[7]==u'等级':
                    temp[8]=i[8]
                    temp[17]=i[11]
                if i[7]==u'客户经理类别':
                    temp[9]=i[8]
                    temp[18]=i[11]
                temp[10]=i[5]
                temp[11]=i[6]
                temp[12]=i[9]#f_user id
                temp[13]=i[10]#user_branch id
                temp.append(i[12])
                temp.append(i[13])
                temp.append(i[15])
                temp.append(i[16])

                rs[i[1]]=temp
        needtrans ={}
        rr=[]
        for key in rs:
            rr.append(list(rs[key]))
        rrr=[] 
        for i in rr:
            if ((self.mtyp!='') and (i[9]!=self.mtyp)):
                continue
            if ((self.pst!='') and (i[7]!=self.pst)):
                continue
            if ((self.dep!='') and (i[6]!=self.dep)):
                continue
            rrr.append(i)    
        return self.translate(rrr,needtrans)
    def make_eq_filterstr(self,filterlist):
        filterstr =""
        self.mtyp,self.pst,self.dep='','',''
        vlist = []
        global ymday
        for k,v in self.args.items():
            if k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" and b.branch_code in ( %s )"%bb

            if k == 'MANAGE_TYPE':
                self.mtyp = v;
            if k == 'POSITION':
                self.pst = v;
            if k == 'STAFF_NAME':
                filterstr = filterstr+" and fu.name like"+" '%'||"+"?"+"||'%'"
                vlist.append(v)
            if k=='org':
                vvv = self.dealfilterlist(v)
                filterstr = filterstr +" and b.branch_code in( %s ) "%(vvv)
            if k=='SALE_CODE':
                filterstr = filterstr+" and fu.USER_NAME = ? "
                vlist.append(v)
            if k=='IS_VIRTUAL':
                filterstr = filterstr+" and %s = ? "%k
                vlist.append(v)
            if k=='WORK_STATUS':
                filterstr = filterstr+" and %s = ? "%k
                vlist.append(v)
            if k=='DEPARTMENT':
                self.dep = v;
        return filterstr,vlist
    def column_header(self):
        return ["时间","员工号","员工名","人员性质","身份证号码","机构名","部门","职务","等级","客户经理类别","安全员标志","在职状态","试聘标志","虚拟柜员标志","学历","柜组长","操作"]
    @property
    def page_size(self):
        return 15
