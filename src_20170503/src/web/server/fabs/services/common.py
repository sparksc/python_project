# -*- coding: utf-8 -*-
"""
    yinsho.services.CommonService
    #####################

    yinsho CommonService module
"""

import hashlib, copy
from flask import json, g
from ..model.common import *
from ..model.customer import *
from ..model.party import *
from ..model.branch import *
from ..model.user import *
from .service import BaseService
from datetime import datetime
import time

class CommonService(BaseService):

    def query_industry(self,industry_d):
        indus = g.db_session.query(IndustryType).filter(IndustryType.industry_d.like(industry_d)).all()
        rtn = [{'industry_d':item.industry_d,'type_name':item.type_name} for item in indus]
        return rtn

    def query_industry_cust(self,party_id):
        party = g.db_session.query(Party).filter(Party.id == party_id).first()
        if party :
            if party.type_code =='company':
                rt = [party.industry_class,party.industry_large_class,party.industry_mid_class,party.industry_small_class]
                return rt
            else:
                cust = g.db_session.query(Customer).filter(Customer.party_id == party_id).first()
                if(cust.personal_card):
                    ids = cust.personal_card[0]
                    return [ids.industry_top,ids.industry_big,ids.industry_mid,ids.industry_small]
                else:
                    return []
        else :

            return []

    def create_person_level(self,cust_id,**kwagrs):

        cust = g.db_session.query(Customer).join(Party,Party.id==Customer.party_id).filter(Customer.cust_type=='person').filter(Party.id == cust_id).first();

        person_lev  = personLevel(customer=cust);
        g.db_session.add(person_lev);
        per_leve = g.db_session.query(personLevel)
        per_leve= per_leve.filter(personLevel.cust_id == cust.role_id).first()
        if per_leve:
            pass
        else:
            return
        items = per_leve.__dict__.keys()
        items.remove('_sa_instance_state')
        items.remove('cust_id')
        items.remove('id')
        targets = g.db_session.query(Target).filter(Target.code.in_(tuple(items))).all()
        return [ {'target':target.name,'attribute':target.attribute} for target in targets]

    def dealone(self,filename,tabObj):
        eles = g.db_session.query(CreateTable).filter(CreateTable.table_name == filename).order_by(CreateTable.id).all()

        kls=[]
        for ele in eles:
            kls.append(ele.element)
        fl = open('./fabs/tests/20160101/whmis_%s.unl'%(filename,),'r')
        while True:
            line = fl.readline()
            if not line:
                break;
            #print line
            vls = line.split(':')
            vls = vls[:-1]
            print len(vls)
            print len(kls)
            info={}
            for idx,k in enumerate(kls):
                info.update({k:vls[idx]})
            #print info
            tab = tabObj(**info)
            g.db_session.add(tab)
        g.db_session.commit()
        fl.close()
        return 'ok'

    def batch(self):
        #       filenames = [['fhdkfhz',u'贷款分户账'],['cdhpdjb',u'承兑汇票登记簿'],['djdkfdjs',u'贷款分段积数表(存量)'],['djtx',u'登记贴现'],['sxdkmx',u'授信贷款明细表（对私）'],['sxdkls',u'授信贷款流水表（对私）'],['sxdkmxn',u'授信贷款明细表（对公）'],['sxdklsn',u'授信贷款流水表(对公)'],['djajhkjhb',u'按揭还款计划表（村量）'],['sxdkqx',u'授信贷款欠息表（对私）'],['sxfdjs',u'授信贷款分段积数表'],['djajqkb',u'按揭欠款表（存量）'],['djajhkb',u'按揭还款表(增量)'],['fhdkmxz',u'贷款分户明细'],['dskhxxwj_contrast',u'对私客户信息对照文件'],['dkkhdzb',u'贷款卡号对照表'],['dgkhxxwj_contrast',u'对公客户信息对照文件']]
        filenames = [['fhdkfhz',FHDKFHZ],['cdhpdjb',CDHPDJB],['djdkfdjs',DJDKFDJS],['djtx',DJTX],['sxdkmx',SXDKMX],['sxdkls',SXDKLS],['sxdkmxn',SXDKMXN],['sxdklsn',SXDKLSN],['djajhkjhb',DJAJHKJHB],['sxdkqx',SXDKQX],['sxfdjs',SXFDJS],['djajqkb',DJAJQKB],['djajhkb',DJAJHKB],['fhdkmxz',FHDKMXZ]]
        #,['dskhxxwj_contrast',DSKHXXWJ_CONTRAST],['dkkhdzb',DKKHDZB],['dgkhxxwj_contrast',DGKHXXWJ_CONTRAST]]

        i = 1;
        print len(filenames)
        #filenames = [['fhdkfhz',FHDKFHZ] ]
        for fn in filenames:
            print fn[0]
            s = time.time()
            self.dealone(fn[0],fn[1])
            t = time.time()
            print t-s,i,'=============================================='
            i = i+1
        print 'Over',len(filenames)
        return 'ok'


