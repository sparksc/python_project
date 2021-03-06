# -*- coding:utf-8 -*-


from querybase import QueryBase
from utils import *
import tempfile
import base64
import os
from decimal import Decimal
from groupby import *
from flask import current_app
import base64
import json
import decimal
def read_style(name):
    f = open(name)
    mg = None
    for row in f:
        mg = json.loads(row)
    f.close()
    return mg

class ObjectQuery(QueryBase):

    def prepare_object(self):
        """查询接口 return a list object"""

    def exp_str(self):
        '''
         返回 excel 写入表达式
        '''
        pass
    def cancal_merge(self):
        '''
        是否取消合并只添加小计
        '''
        pass

    def do_query(self):
        current_app.logger.debug(self)
        self.build_header()
        self.merge_file = None
        current_app.logger.debug(self)
        ok, _ ,_= self.cached_file()
        if not ok:
            self.conversation_id = self.cache_object()
            #if ":" in self.conversation_id:
            #    self.merge_file = base64.b64decode(self.conversation_id.split(":")[1])
            # print self.conversation_id
        self.target["rows"] = self.get_paged_data()
        self.target["actions"] = self.build_actions()
        if self.args:
            self.target["params"] = self.args
        if ":" in  self.conversation_id: #访问2个文件，一个是数据，一个是样式合并信息
            sname = self.conversation_id.split(":")[1]
            sname = base64.b64decode(sname)
            mg = read_style(sname)
            self.target["merge_style"]=  mg            
            gb = self.group_by()
            merge_cols = gb[0]
            m=[0]
            if len(gb) >= 3:
                self.target["sub"]=gb[2]
                for value in gb[2].values():
                    merge_cols.extend(value)
                '''
                for _,sub in 
                m.extend(for _,x in]
                '''
            self.target["cancalMerge"]=self.cancal_merge()
            merge_cols.sort()
            self.target["merge_cols"] = merge_cols
        if self.exp_str() is not None:
            self.target["exps"]= self.exp_str()
        print self
        return json.dumps(self.target)
    def get_paged_data(self):
        print "***",self.merge_file
        page_size = self.page_size
        if self.args.has_key("export"):
            page_size = self.total_count
        row_start = min(
            (self.page - 1) * page_size, int(self.total_count))
        row_end = min(self.page * page_size, int(self.total_count))
        self.row_count = row_end - row_start
        # print "page", self.page
        # print "page_size", page_size
        # print "total_count", self.total_count
        # print "row_count", self.row_count
        # print "row_start", row_start
        # print "row_end", row_end
        data = []
        ok, file_name, merge_file = self.cached_file()
        if ok:
            index = 0
            with open(file_name) as f:
                for _ in xrange(row_start):
                    next(f)
                for line in f:
                    if index >= self.row_count:
                        break
                    index = index + 1
                    data.append(self.json_to_object(line))
        return data

    @property
    def conversation_id(self):
        return self.args.get("conversation_id")

    @conversation_id.setter
    def conversation_id(self, value):
        #return self.args.update({"conversation_id": base64.b64encode(value)})
        return self.args.update({"conversation_id": value})

    def cached_file(self):
        if self.conversation_id:
            cid = self.conversation_id
            if ":" in cid:
                cids = cid.split(":")
                self.merge_file  = base64.b64decode(cids[1])
                file_name = base64.b64decode( cids[0] )
            else:
                print self.conversation_id ,"*****************"
                file_name = base64.b64decode( self.conversation_id )
            return os.path.exists(file_name), file_name, self.merge_file
        else:
            return False, None,None
    

    def json_encode_decimal(self, obj):
        if isinstance(obj,decimal.Decimal):
            return float(obj)
        raise TypeError(repr(obj),"is not JSON serializable")

    def object_to_json(self, src_object):
        """
        对象如果不能使用默认JSON序列化的方法，请覆盖此方法
        """
        return json.dumps(src_object, default=self.json_encode_decimal)


    def json_to_object(self, str_json):
        """
        对象如果不能使用默认JSON反序列化的方法，请覆盖此方法
        """
        return json.loads(str_json)

    def group_by(self):
        '''
        return  分组，汇总
        '''

    def cache_object(self):
        rows = self.prepare_object()
        self.total_count = len(rows)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            gb = self.group_by()
            #print len(gb),type(gb),'******************************',gb
            if gb is None:
                for obj in rows:
                    f.write(self.object_to_json(obj) + '\n')
                f.flush()
                return  base64.b64encode(f.name)
            else:
                cols = gb[0]
                sums = gb[1]
                dg = DataGroup(rows, cols, sums, True)
                result_file = tempfile.NamedTemporaryFile(delete=False)
                dg.group_by_cols_to_file(result_file, object_to_json )

                merge_file = tempfile.NamedTemporaryFile(delete=False)
                dg.to_merge_file( merge_file )
                merge_file.close()
                result_file.close()
                self.total_count = dg.total_count
                return base64.b64encode(result_file.name) + ":" + base64.b64encode(merge_file.name)
			
    def translate(self,row,needtrans):
        "翻译"
        self.transdict = self.get_dict_data(needtrans)
        current_app.logger.debug("zhihang")
        rs=[]
        for item in row:
            tmp = list(item)
            for k,vdict in self.transdict.items():
                if vdict.has_key(str(tmp[k])):
                    tmp[k] = vdict[str(tmp[k])]
                elif needtrans.has_key("defalut"):
                    tmp[k] = needtrans["defalut"]
            rs.append(tmp)
        return rs

    def dealfilterlist(self, filterlist):
        vv = filterlist.split(',')
        vvv = ""
        for tt in vv:
            ttt = "'" + tt + "'" 
            vvv = vvv + ttt + ','
        vvv = vvv[:-1]
        return vvv

    def deal_teller_query_auth(self, login_teller_no):
        """
        查询权限控制,前端送上当前登录柜员,在没有选择查询柜员的前提下
        1、总行查询全行
        2、支行管理行(M)查询下属机构
        3、网点指定岗位查选全网点
        4、客户经理、柜员查询个人
        """

        login_teller = self.engine.execute("select gr.group_name from f_user fu, user_group ug, group gr where ug.user_id = fu.role_id and ug.group_id = gr.id and gr.group_type_code = '5000' and fu.user_name = '%s'"%(login_teller_no)).fetchone()
        if login_teller[0] in [u'总行管理组', u'系统管理组', u'支行管理组', u'支行营业部及网点管理组', u'支行系统管理组', u'支行非审批管理组']:
            return False
        else:
            return True

    def deal_teller_transfer_auth(self, login_teller_no):
        """
        查询权限控制,前端送上当前登录柜员,在没有选择查询柜员的前提下
        和deal_teller_query_auth唯一的不同就是网点指定岗位查选全网点，但是不可以移交
        """

        login_teller = self.engine.execute("select gr.group_name from f_user fu, user_group ug, group gr where ug.user_id = fu.role_id and ug.group_id = gr.id and gr.group_type_code = '5000' and fu.user_name = '%s'"%(login_teller_no)).fetchone()
        if login_teller[0] in [u'总行管理组', u'支行管理组', u'支行系统管理组', u'支行非审批管理组']:
            return False
        else:
            return True

    def deal_branch_query_auth(self, login_branch_no):
        """
        查询权限控制,前端送上当前登录机构,在没有选择机构的前提下:
        1、总行查询全行
        2、支行管理行(M)查询下属机构
        """

        if login_branch_no == self.top_branch_no:
            return False
        else:
            branch_codes = self.engine.execute("select branch_code from branch where parent_id in (select role_id from branch where branch_code='%s')"%(login_branch_no)).fetchall()
            bb = "'" + login_branch_no + "'," 
            for b in branch_codes:
                tt = "'" + b[0] + "'" 
                bb = bb + tt + ','
            bb = bb[:-1]
            if len(bb) < 1:
                bb = "'" + login_branch_no + "'" 
            return bb

    def get_dict_data(self,needtrans):
        rs={}
        sql = u"select dict_key,DICT_VALUE from dict_data where dict_type = ?"
        for k,v in needtrans.items():
            if not isinstance(k,int): continue
            row = self.engine.execute(sql,v).fetchall()
            rs[k] = {}
            for item in row:
                rs[k][item[0]] = item[1]
        return rs

    def get_paradetail(self,keylist):
        "得到参数"
        if not keylist:
            return []
        status = u"正常"
        selstr = ""
        joinstr = ""
        v =[]
        for key in keylist:
            selstr = selstr+",%s.value "%key
            joinstr = joinstr+ """
                inner join t_para_detail %s on  %s.PARA_ROW_ID = r.ID and %s.detail_key = ?
            """%(key,key,key)
            v.append(key)
        sql = u"""
            select %s from  t_para_row r  %s where r.ROW_STATUS = ?
        """%(selstr[1:],joinstr)
        v.append[status]
        row = self.engine.execute(sql,v).fetchall()
        rs=[]
        for item in row:
            rs.append(dict(zip(keylist,item)))
        return rs
    def get_auth_sql(self,data_type,sale_code,org_code,dep_name):
        "调用时传入机构号和员工号的，数据库字段"
        print "login_teller_no:", self.args.get("login_teller_no")
        print "login_branch_no:", self.args.get("login_branch_no")

        if not self.args.has_key('login_teller_no'):
            return "1=1"

        auth_type,value_list = self.get_teller_query_auth(data_type)    #查询数据的权限模板类型
        print "auth_type:", auth_type
        print "value_list:", value_list
        if auth_type=='0' or auth_type=='101':    #总行,无
            return value_list
        elif auth_type=='100' and sale_code:      #个人
            return "%s in ('%s')"%(sale_code,value_list)
        elif auth_type in "2,1" and org_code:   #支行,网点
            return "%s in (%s)"%(org_code,value_list)
        elif auth_type in "5" and dep_name:   #部门
            return "%s in (%s)"%(dep_name,value_list)
        else:
            return "1=1"
         

    def get_teller_query_auth(self,data_type):
        """
            查询权限控制，前端送上登录员工号，脚本中传入数据模块名(dict_data中的data_type类型),查询该员工岗位对应的权限(越小权限越大)
        """

        teller_no = self.args.get('login_teller_no')
        print "get_teller_query_auth:", teller_no, data_type
        #机构
        teller_branch = self.engine.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(teller_no)).fetchone()
        #部门
        teller_dep = self.engine.execute("select gr.id from f_user fu, user_group ug, group gr where ug.user_id = fu.role_id and ug.group_id = gr.id and gr.group_type_code = '3000' and ug.enddate is null and fu.user_name = '%s'"%(teller_no)).fetchone()

        auth_type = '100'#默认查询本人
        l_branch = '无'
        l_dep = '无'

        l_branch = []
        if teller_branch is not None:
            l_branch.append(teller_branch[0])
        if teller_dep is not None:
            l_dep = teller_dep[0]

        #权限
        auth_type_sql = """
            select gd.auth_type from f_user fu, user_group ug, group gr, group_data gd where 
            ug.user_id = fu.role_id and ug.group_id = gr.id 
            and gr.group_type_code = '5000' 
            and ug.enddate is null and gd.group_id = gr.id 
            and fu.user_name = ? and gd.data_type = ?
        """
        auth_type_row = self.engine.execute(auth_type_sql,[teller_no,data_type]).fetchall()
        for it in auth_type_row:
            auth_type = str(min(int(auth_type), int(it[0])))
        print "get_teller_query_auth:", teller_no, auth_type

        return auth_type,self.auth_value(auth_type,l_branch,l_dep, teller_no)
    def auth_value(self,auth_type,l_branch,l_dep,teller_no):
        """
            根据权限级别，返回不同的查询字段值
        """
        auth_func={
            '0':u'1=1',
            '1':self.br_value,
            '2':self.dot_value,
            '100':teller_no,
            '101':u"1!=1",
            '5':self.dep_value,
        }
        func = auth_func.get(auth_type)
        if hasattr(func,'__call__'):
            return func(l_branch, l_dep)
        else:
            return func

    def dep_value(self, l_branch, l_dep):
        "部门权限，实际应该拼接本部门所有的柜员号, 暂时未考虑只有总行部室"

        sql = u"""
            select fu.* from f_user fu
            join user_group ug on ug.user_id = fu.role_id and ug.enddate is null
            join group gr on gr.id = ug.group_id and gr.group_type_code = '3000'
            join user_branch ub on ub.user_id = fu.role_id
            join branch b on b.role_id = ub.branch_id and b.branch_code = ?
            where gr.id = ?
            """
        print sql
        tellers = self.engine.execute(sql, [self.top_branch_no, l_dep]).fetchall()

        str=""
        for b in tellers:
            str="%s,'%s'"%(str,b[1])

        if len(str)<1:
            return None
        else:
            return str[1:] 
 
    def dot_value(self,l_branch, l_dep):
        "网点权限，就是本身网点号"
        str = ""
        for branch_code in l_branch:
            str=",'%s'"%branch_code
        return str[1:]

    def br_value(self,l_branch, l_dep):
        "支行权限，是所有有相同上级机构的网点"
        print "br_value:",l_branch 
        str_branch_code = self.dot_value(l_branch, l_dep)
        print "br_value:", str_branch_code, str_branch_code[1]
        if str_branch_code[1] == 'M':
            sql = """
                select branch_code 
                from branch 
                where parent_id in (
                    select role_id from branch bb where bb.branch_code in (%s)
                    )
                """%(str_branch_code)
        else:
            sql = """
                select branch_code 
                from branch
                where parent_id in (
                 select distinct b1.parent_id
                 from branch b1
                 where b1.branch_code in (%s)
                )
            """%(str_branch_code)
        branch_codes = self.engine.execute(sql).fetchall()
        str=""
        for b in branch_codes:
            str="%s,'%s'"%(str,b[0])
        if len(str)<1:
            return str_branch_code
        else:
            return str[1:] 

    def amount_trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        mon = '{:,}'.format(tmp)
        return mon
