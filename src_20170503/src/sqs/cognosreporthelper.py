#-*- coding:utf-8 -*-
from cognosreader import CognosReader
from cognosjsonparser import CognosJsonParser
from config import logger
import urllib
import utils

class CognosReportHelper():
    def __init__(self,report_conf={}):
        self.conf = report_conf
        # print report_conf

    def get_url(self,report_name, args={}):
        url_tail=""
        ip =self.conf.get("IP")
        cognos_para = self.conf.get("cognos_para")
        report = self.conf.get(report_name.strip())
        if report is None:
            logger.error( "no report config: %s  %s"%(str(report_name),str(type(report_name))))
            return None
        report_para= report.get(u"report_para")
        report_id = report.get(u"report_id")
        url_tail= cognos_para.format(report_id)
        args_has_value = {}
        for name in report_para:
            argv = args.get(name)
            if argv:
                args_has_value[name]=argv.strip()
        url_tail = url_tail + u"&" + urllib.urlencode(utils.encoded_dict(args_has_value))
        return u"http://{0}{1}".format(ip,url_tail)

    def get_convo_url(self,conversation_id,action):
        ip =self.conf.get("IP")
        conversation_url = self.conf.get(u"conversation_url")
        if conversation_url is None or conversation_id is None or action is None:
            return None
        return conversation_url.format(ip,conversation_id,action)

    def get_data(self,report_name, args={}):
        report_url =self.get_url(report_name,args)
        logger.info(u"get report"+unicode(report_name)+u" url: " +report_url)
        return self.get_data_by_url(report_url)
        
    def get_data_by_url(self,report_url):
        if report_url is None:
            return "{}"
        logger.info("get report by "+" url: " +report_url)
        reader = CognosReader()
        response = reader.context_request(report_url)
        parser = CognosJsonParser()
        result = parser.parse_response(response)
        return result


def get_report(report_name, args={},report_conf={}):
    report_helper = CognosReportHelper(report_conf)
    return report_helper.get_data(report_name, args)

def get_report_by_url(report_url,report_conf={}):
    report_helper = CognosReportHelper(report_conf)
    return report_helper.get_data_by_url(report_url)

def get_report_convo(conversation_id,action,report_conf={}):
    report_helper = CognosReportHelper(report_conf)
    report_url = report_helper.get_convo_url(conversation_id,action)
    return report_helper.get_data_by_url(report_url)

