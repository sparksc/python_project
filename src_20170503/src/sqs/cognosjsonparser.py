#-*- coding:utf-8 -*-

import json,utils

u"""
Parse Cognos's report JSON to custom JSON format.

e.g.
{
    "title":"Dumy Reprt",
    "header":["Column1","Column2"],
    "rows":[{"A1","B1"},{"A2","B2"}],
    "actions":[{"action": "NEXT",resource": "resource_url"},{"action": "PREV",resource": "resource_url"}]
}
    -------------------
          Dumy Reprt
    Column1    Column2
    A1         B1
    A2         B2
    -------------------

Cognos JSON format
http://www-01.ibm.com/support/knowledgecenter/SSEP7J_10.2.2/com.ibm.swg.ba.cognos.dg_cms.10.2.2.doc/r_rest_opt_fmt.html%23rest_opt_fmt?lang=en
"""
class CognosJsonParser():

    def __init__(self):
        self.target = {}
        self.content_url = ""
        self.obs_cols = [u"机构号",u"机构名称",u"员工号",u"员工姓名",u"客户号",u"客户名称",u"员工编号",u"员工名称",u"理财产品名称"]

    u"""
    parse JSON from httplib.HTTPResponse
    """
    def parse_response(self,response):
        self.content_url = response.geturl()
        if response.getcode() == 200 and "application/json" in response.headers.get("Content-Type"):
            document = json.load(response)
            self.get_operations(document)
            self.get_title(document)

            table = self.get_table(document)

            self.get_header(table)
            self.get_rows(table)
#            self.obs_data()
            return json.dumps(self.target)
        else:
            return json.dumps({})
    
    def obs_data(self):
        for idx,val in enumerate(self.target["header"]):
            if val in self.obs_cols:
                for row in self.target["rows"]:
                    row[idx] = "XXXXXXXXX"


    u"""
    Cognos报表标题
    """
    def get_title(self,document):
        """
        no title in format2
        """
        header = document["document"]["pages"][0]["page"].get("header")
        if header:
            title = header["item"][0]["blk"]["item"][0]["txt"]["val"]
            self.target["title"] = title


    u"""
    Cognos报表列标题
    """
    def get_header(self,tables):
        table = tables[0]
        if table and "format1" in tables[1]:
            lst = table["trow"][1]["tcell"][0]["item"][0].get("lst")
            if lst:
               header = lst["colTitle"]
            else:
               header = []
#            header = table["trow"][1]["tcell"][0]["item"][0]["lst"]["colTitle"]
        else:
            header = table["colTitle"]

        ths = [th["item"][0]["txt"]["val"] for th in header]
        self.target["header"] = ths


    u"""
    Cognos报表数据行
    """
    def get_rows(self,tables):
        table = tables[0]
        if table and "format1" in tables[1]:
            rows = {}
            lst = table["trow"][1]["tcell"][0]["item"][0].get("lst")
            if lst:
                rows = lst["group"]["row"]
            else:
                rows = {}
#            rows = table["trow"][1]["tcell"][0]["item"][0]["lst"]["group"]["row"]
            rows_obj = []
            for row in rows:
                tds = [td["item"][0]["txt"]["fmtVal"] if td["item"][0]["txt"].get("fmtVal") else td["item"][0]["txt"]["val"] for td in row["cell"]]
                rows_obj.append(tds)
            self.target["rows"] = rows_obj
        else:
            rows = table["group"]["row"]
            rows_obj = []
            for row in rows:
                tds = [td["item"][0]["txt"]["fmtVal"] if td["item"][0]["txt"].get("fmtVal") else td["item"][0]["txt"]["val"] for td in row["cell"]]
                rows_obj.append(tds)
            self.target["rows"] = rows_obj

    u"""
    Cognos报表表格
    """
    def get_table(self,document):
        table = document["document"]["pages"][0]["page"]["body"]["item"][0].get("tbl")
        if table:
            return (table,"format1")
        else: # format 2
            return (document["document"]["pages"][0]["page"]["body"]["item"][0].get("lst"),"format2")

    u"""
    Cognos报表分页等操作
    """
    def get_operations(self,document):
        actions = [{"action":op.get("value","").lower(),
                    "resource":"{0}/{1}".format(self.content_url,op.get("value","").lower()),
                    "conversation_id":utils.get_session_key(self.content_url)} for op in document["document"]["secondaryOperations"]]
        self.target["actions"] = actions
