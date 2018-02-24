# -*- coding:utf-8 -*-

import unittest
from ..database import simple_session, Base
from ..model.branch import Branch
from ..model.user import *
import xlrd
import logging
from os import *

log = logging.getLogger()
class TestBranch(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()

    def init_branch(self):
        # Branch.__table__.create(self.session.bind)
        init_branch_data(self.session)

    def query_branchs(self):
        branch = self.session.query(Branch).filter(Branch.branch_code=='047303').first()
        log.debug(branch.__dict__)
        log.debug(branch.parent.__dict__ if branch.parent else None)
        log.debug(branch.children)
        for child in branch.children:
            log.debug(child.__dict__)
            log.debug(child.parent.__dict__)
        log.debug('####################################')

        '''
        for branch in branchs:
            log.debug('####################################')
            log.debug(branch.__dict__)
            log.debug(branch.parent.__dict__ if branch.parent else None)
            log.debug(branch.children)
            for child in branch.children:
                log.debug(child.__dict__)
                log.debug(child.parent.__dict__)
            log.debug('####################################')
        '''

    def tearDown(self):
        logging.debug("finish!!!")

 
    def test_init_branch_data(self):
        self.session.query(UserBranch).delete()
        self.session.query(Branch).delete()
        self.session.query(Role).filter(Role.type_code == 'branch').delete()

        #  机构
        data = xlrd.open_workbook(environ['HOME'] + u'/src/doc/机构表.xls')
        sheet = data.sheet_by_index(0)
        nrows = sheet.nrows
        for r in range(1,nrows):
            if not sheet.cell(r,0).value.strip():
                continue
            branch = Branch(branch_code=sheet.cell(r,0).value,branch_name=sheet.cell(r,1).value,branch_level=sheet.cell(r,3).value)
            top_branch_code = sheet.cell(r,2).value.strip()
            print sheet.cell(r,0).value.strip(), top_branch_code
            if top_branch_code is not None and len(top_branch_code) > 0:
                top_branch = self.session.query(Branch).filter(Branch.branch_code == top_branch_code).first()
                branch.parent_id = top_branch.role_id
            self.session.flush()
            self.session.add(branch)
        self.session.commit()
