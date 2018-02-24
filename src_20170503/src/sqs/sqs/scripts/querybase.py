# -*- coding:utf-8 -*-


from sqlalchemy import create_engine
import simplejson as json
import urllib
from utils import *
import math
import decimal


class QueryBase(object):
    def __init__(self, code, args, conf, echo=False):
        self.code = code
        self.args = args
        self.conf = conf
        self.engine = None
        self.echo = echo
        self.create_engine()
        self.target = {}
        self.row_count = 0
        self.raw_sql = None
        self.total_count
        self.top_branch_no = '966000'

        #system_cal = self.engine.execute("select * from system_calendar").fetchone()
        #self.system_date = system_cal[1]

    def create_engine(self):
        DB_URI = self.conf.get("DB_URI")
        if DB_URI:
            self.engine = create_engine(DB_URI, echo=self.echo)

    @property
    def page(self):
        page = self.args.get("page")
        if page:
            return int(page)
        return 1

    @property
    def total_count(self):
        total_count = self.args.get("total_count")
        if total_count:
            return int(total_count)
        else:
            return 0

    @total_count.setter
    def total_count(self, value):
        return self.args.update({"total_count": value})

    @property
    def page_size(self):
        page_size = self.args.get("page_size")
        if page_size:
            return int(page_size)
        else:
            return 10

    @property
    def order_by(self):
        return None

    def column_header(self):
        """ 查询接口列标题 """

    def prepare_sql(self):
        """ 查询接口SQL """

    def do_query(self):
        self.build_header()

        sql = self.prepare_sql()
        self.count_rows()
        rows = self.engine.execute(sql,self.sql_params).fetchall()
        self.target["rows"] = []
        self.target["actions"] = []
        if rows:
            self.row_count = len(rows)
            self.target["rows"] = [list(row) for row in rows]
            self.target["actions"] = self.build_actions()

        if self.args:
            self.target["params"] = self.args

        return json.dumps(self.target)

    def count_rows(self):
        """call this function before prepare_sql()"""
        count_sql = u"SELECT count(1) AS count_1 FROM ({0}) AS anon_1".format(self.raw_sql)  
        self.total_count = self.engine.execute(count_sql,self.sql_params).scalar()

    def build_header(self):
        header = self.column_header()
        if header:
            self.target["header"] = list(header)
        else:
            self.target["header"] = []

    def build_actions(self):
        acts = ["first", "next", "previous", "last", "release"]
        actions = [self.build_page_url(act) for act in acts]

        return [action for action in actions if action]

    def build_page_url(self, act):
        action = {"action": act}
        params = self.args.copy()
        if act == "first":
            if self.page > 1:
                params.update({"page": 1})
            else:
                return None

        if act == "next":
            if self.row_count == self.page_size:
                params.update({"page": self.page + 1})
            else:
                return None

        if act == "previous":
            if self.page > 1:
                params.update({"page": self.page - 1})
            else:
                return None

        if act == "last":
            if self.row_count == self.page_size:
                params.update(
                    {"page": int(math.ceil(decimal.Decimal(self.total_count) / self.page_size))})
            else:
                return None

        action["conversation_id"] = u"{0}?{1}".format(
            self.code, urllib.urlencode(encoded_dict(params)))

        return action
