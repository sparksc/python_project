# -*- coding:utf-8 -*-
from proc_template import *

class Report():
    def __init__(self, code, args, report_conf={}):
        self.conf = report_conf
        self.code = code
        self.args = args
        self.module = self.import_module(self.code)
    def get_list_data(self):
        query = self.module.Query(self.code, self.args, self.conf)
        return query.prepare_object()

    def get_data(self):
        query = self.module.Query(self.code, self.args, self.conf)
        return query.do_query()

    def get_report_by_url(self, report_url):
        return '{}'

    def get_convo_url(self, conversation_id, action):
        return '{}'

    def get_module(self, code):
        return "sqs.scripts.q" + code

    def import_module(self, code):
        return __import__(self.get_module(code), fromlist=["scripts"])


def get_report(report_name, args={}, report_conf={}):
    report_helper = Report(report_conf)
    return report_helper.get_data(report_name, args)


def get_report_by_url(report_url, report_conf={}):
    report_helper = Report(report_conf)
    return report_helper.get_data_by_url(report_url)


def get_report_convo(conversation_id, action, report_conf={}):
    report_helper = Report(report_conf)
    report_url = report_helper.get_convo_url(conversation_id, action)
    return report_helper.get_data_by_url(report_url)
