# -*- coding:utf-8 -*-
u"""
可疑交易评估自动跑批测试
"""
from ..domain.aml_model import run_model_A0000
from .test_aml_database import ResetDB

"""
import logging, datetime
from .configure import Configure
with Configure() as cfg:
    #database = cfg.get_database("aml_database_for_test");
    database = cfg.get_database("aml_database");
"""


def test_auto_run_aml():
    run_model_A0000()
    

test_auto_run_aml.setup = ResetDB

