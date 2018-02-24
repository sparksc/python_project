#-*- coding:utf-8 -*-

# from cognosreporthelper import CognosReportHelper
from cognosreader import CognosReader
from cognosjsonparser import CognosJsonParser
import json
from config import report_conf
import cognosreporthelper as report



if __name__== "__main__":
    # t = cognosreporthelper.CognosReportHelper(report_conf)

    result = report.get_report(report_name="test",args={},report_conf=report_conf)

    # print result
    result_obj = json.loads(result)

    next_page_url = result_obj["actions"][0]["resource"]

    # print report.get_report_by_url(next_page_url,report_conf=report_conf)

    result = report.get_report(report_name="test2",args={"p_BRANCH_CODE":"000000","p_FLAG":"待处理","p_OP_TYPE":"<NULL>"},report_conf=report_conf)

    result_obj = json.loads(result)
    convo_id = result_obj["actions"][0]["conversation_id"]
    action = result_obj["actions"][0]["action"]
    print convo_id,action
    result = report.get_report_convo(convo_id,action,report_conf=report_conf)
    print result
    # cr = CognosReader()
    # # content = cr.context_request("http://192.168.100.39/ibmcognos/cgi-bin/cognos.cgi/rds/pagedReportData/report/i7496927BE1F4454BB591FFA1527C1288?fmt=JSON&p_BRANCH_CODE=000000&p_FLAG=待处理&p_OP_TYPE=<NULL>")
    # content = cr.context_request("http://192.168.100.39/ibmcognos/cgi-bin/cognos.cgi/rds/pagedReportData/report/i5FF079E606B342E6A28AEB094B9C395B?fmt=JSON")

    # parser = CognosJsonParser()
    # result = parser.parse_response(content)

    # result_obj = json.loads(result)

    # print result
    # # print result_obj

    # next_page_url = result_obj["actions"][0]["resource"]
    # cr = CognosReader()
    # content = cr.context_request(next_page_url)
    # result = parser.parse_response(content)
    # print result