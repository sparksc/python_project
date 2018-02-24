# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
参数类型查看
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.excle_header_len = len(self.target["header"])-1
        self.filterlist = ['row_status','para_type_id']
        self.vlist = []
        selstr,joinstr = self.make_str()
        filterstr = self.make_eq_filterstr() 
        sql ="""
            select %s,r.row_status,r.id
            from  t_para_row r
            %s
            where 1=1 %s
            order by r.row_num
	    """%(selstr,joinstr,filterstr)
        row = self.engine.execute(sql,self.vlist).fetchall()
        needtrans ={}
        self.target["para_header"] = self.para_header 
        #print sql, self.vlist
        return self.translate(row,needtrans)
    
    def make_str(self):
        selstr = ""
        joinstr = ""
        i= 0
        for item in self.para_header:
            i =i+1
            rename = 'd%s'%i
            selstr = selstr+",%s.detail_value"%rename
            joinstr = joinstr+"left join t_para_detail %s on %s.para_row_id = r.id and %s.para_header_id = ? "%(rename,rename,rename)
            self.vlist.append(item['para_header_id'])
        return selstr[1:],joinstr

    def make_eq_filterstr(self):
        filterstr =""
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ? "%k
                self.vlist.append(v)
        return filterstr

    def column_header(self):
        sql =u"""
            select header_name,header_key,id,header_type
            from t_para_header 
            where  header_status =? and  para_type_id=?
            order by header_order
        """
        rows = self.engine.execute(sql,'启用',self.args['para_type_id']).fetchall()
        self.para_header = []
        rs = []
        for row in rows:
            rs.append(row[0])
            data ={}
            data["header_name"] = row[0]
            data["header_key"] = row[1]
            data["para_header_id"] = row[2]
            data["header_type"] = row[3]
            self.para_header.append(data)
        rs.append("状态")
        rs.append("操作")
        return rs
        #return ["属性名","属性key","数据类型", "说明","属性顺序", "参数状态","操作"]

    @property
    def page_size(self):
        return 15
