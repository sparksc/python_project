# -*- coding:utf-8 -*-
import time
from flask.ext import excel
import pyexcel.ext.xls
import pyexcel.ext.xlsx
from querybase import QueryBase
from utils import *
import tempfile
import base64
import os


class ObjectQuery(QueryBase):

    def prepare_object(self):
        """查询接口 return a list object"""

    def do_query(self):
        self.build_header()
        ok, _ = self.cached_file()
        if not ok:
            self.conversation_id = self.cache_object()
            # print self.conversation_id

        self.target["rows"] = self.get_paged_data()
        self.target["actions"] = self.build_actions()

        if self.args:
            self.target["params"] = self.args

        return json.dumps(self.target)

    def do_excel_query(self):
        self.build_header()
        self.excle_header_len = len(self.target["header"])
        ok, _ = self.cached_file()
        if not ok:
            self.conversation_id = self.cache_object()
            # print self.conversation_id
        ltime=time.localtime()
        tstr = time.strftime("%Y%m%d%H%M%S", ltime)
        mstr = str(time.time()).replace('.','_')
        self.target["rows"] = self.get_all_data()
        outputlist = [self.target["header"][:self.excle_header_len]]+self.target["rows"]
        return excel.make_response_from_array(outputlist,"xlsx",200,"%s_%s"%(tstr,mstr))

   
    def get_all_data(self):
        data = []
        ok, file_name = self.cached_file()
        if ok:
            index = 0
            with open(file_name) as f:
                for line in f:
                    if index >= int(self.total_count):
                        break
                    index = index + 1
                    data.append(json.loads(line)[:self.excle_header_len])
        return data


    def get_paged_data(self):
        row_start = min(
            (self.page - 1) * self.page_size, int(self.total_count))
        row_end = min(self.page * self.page_size, int(self.total_count))
        self.row_count = row_end - row_start
        # print "page", self.page
        # print "page_size", self.page_size
        # print "total_count", self.total_count
        # print "row_count", self.row_count
        # print "row_start", row_start
        # print "row_end", row_end
        data = []
        ok, file_name = self.cached_file()
        if ok:
            index = 0
            with open(file_name) as f:
                for _ in xrange(row_start):
                    next(f)
                for line in f:
                    if index >= self.row_count:
                        break
                    index = index + 1
                    data.append(json.loads(line))
        return data

    @property
    def conversation_id(self):
        return self.args.get("conversation_id")

    @conversation_id.setter
    def conversation_id(self, value):
        return self.args.update({"conversation_id": base64.b64encode(value)})

    def cached_file(self):
        if self.conversation_id:
            file_name = base64.b64decode(self.conversation_id)
            return os.path.exists(file_name), file_name
        else:
            return False, None

    def object_to_json(self, src_object):
        """
        对象如果不能使用默认JSON序列化的方法，请覆盖此方法
        """
        return json.dumps(src_object)

    def cache_object(self):
        rows = self.prepare_object()
        self.total_count = len(rows)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            for obj in rows:
                f.write(self.object_to_json(obj) + '\n')
            f.flush()
            return f.name

    def translate(self,row,needtrans):
        self.transdict = self.get_dict_data(needtrans)
        rs=[]
        for item in row:
            tmp = list(item)
            for k,vdict in self.transdict.items():
                if vdict.has_key(str(tmp[k])):
                    tmp[k] = vdict[str(tmp[k])]
            rs.append(tmp)
        return rs

    def get_dict_data(self,needtrans):
        sql = """select dict_key,dict_value from  dict_data where dict_type =?"""
        rsdict ={}
        for idx,dict_type in needtrans.items():
            dict_data ={}
            rowdata = self.engine.execute(sql,dict_type).fetchall()
            for it in rowdata:
                dict_data[it[0]] =it[1]
            rsdict[idx] = dict_data
        return rsdict

