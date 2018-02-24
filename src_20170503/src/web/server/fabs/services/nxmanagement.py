# -*- coding: utf-8 -*-
"""
    yinsho.services.ManagementService
    #####################

    yinsho ManagementService module
"""

from ..model.nxmanagement import *
from ..base import utils
from flask import json, g

class ManagementService():
    __model__ = NXBranch


class NXBranchService():

    def all(self):
        return g.db_session.query(NXBranch).all()

    def get(self,id):
        return g.db_session.query(NXBranch).filter(NXBranch.id==id).first()

    def add(self, **kwargs):
        nxbranch = NXBranch(**kwargs)
        g.db_session.add(nxbranch)
        g.db_session.commit()
        return nxbranch

    def update(self,id,**kwargs):
        status_code = 200
        nxbranch = self.get_nxbranch(id,**kwargs)
        if nxbranch is None:
            nxbranch = NXBranch(**kwargs)
            nxbranch.id = id
            g.db_session.add(nxbranch)
            status_code = 201
        g.db_session.commit()
        return nxbranch,status_code

    def get_nxbranch(self,id,**kwargs):
        if id:
            nxbranch = g.db_session.query(NXBranch).filter(NXBranch.id==id).first()
        if nxbranch:
            if kwargs.has_key("name"):
                nxbranch.name = kwargs.get("name")
            if kwargs.has_key("address"):
                nxbranch.address = kwargs.get("address")
            if kwargs.has_key("phone"):
                nxbranch.phone = kwargs.get("phone")
        return nxbranch

    def update_exists(self,id,**kwargs):
        nxbranch = self.get_nxbranch(id,**kwargs)
        if nxbranch:
            g.db_session.commit()
        return nxbranch

    def delete(self,id):
        if id:
            nxbranch = g.db_session.query(NXBranch).filter(NXBranch.id==id).delete()
            g.db_session.commit()
        return {"result":True}
