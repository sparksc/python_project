#-*- coding:utf-8 -*-

import logging,sys
import json


HOME_PATH = ''
logging.basicConfig(stream=sys.stdout,format="%(asctime)-15s %(process)d %(levelname)s : %(message)s", level=logging.INFO)
from logging.handlers import RotatingFileHandler
from logging import Formatter
filename=HOME_PATH + "./cognos_report.log"
filehandler = RotatingFileHandler(filename, maxBytes=100*1024*1024)
filehandler.setFormatter(Formatter("%(asctime)-15s %(process)d %(levelname)s : %(message)s"))
logger=logging.getLogger("audit")
logger.addHandler(filehandler)

config_report = open("config_report.json")
report_conf = json.load(config_report)
