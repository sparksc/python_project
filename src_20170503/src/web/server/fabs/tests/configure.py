# -*- coding:utf-8 -*-
u"""
测试用的配置
"""
import tempfile
import shutil
import os.path
import os
from ..configure import PythonConfigure
from ..model.database import Database
import logging

class Configure(PythonConfigure):
    def __init__(self):
        super(Configure, self).__init__()
        self.root_path=tempfile.mkdtemp(prefix='guangning', dir="/tmp/") #TODO:如何删除这个临时目录
        self.etc_path=os.path.join(self.root_path, "etc")
        os.mkdir(self.etc_path)
        self.configure_file=os.path.join(self.etc_path, "guangning.cfg")
        self['root_path']=self.root_path

        self.install_sample_cfg(os.path.join(os.path.dirname(__file__),"./sample.cfg"))
        self.read()
        self.get_database()

    def install_sample_cfg(self, path):
        u"""
        安装测试使用的配置文件到测试用的目录
        """
        return shutil.copyfile(path, self.configure_file)
    def read(self):
        u"""
        读取测试的配置文件，返回配置对象
        """
        return super(Configure, self).read(self.configure_file)

    def get_database(self, name="test_database"):
        logging.debug("configure:%s"%str(self))
        self.database=Database(self, name)
        return self.database

    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.close()
        logging.debug("args:%s"%str(args))
    def close(self):
        shutil.rmtree(self.root_path)
