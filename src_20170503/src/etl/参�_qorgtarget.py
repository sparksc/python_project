# -*- coding:utf-8 -*-

from objectquery import ObjectQuery


class Query(ObjectQuery):

    def prepare_object(self):
        self.para = self.get_common_parameter()
        self.datadict = self.init_org_dict()
        self.data_func() 
        for data in self.datalist:
            if data.has_key("func"):
                func = data["func"]
                parafun = data.get("paralist",self.renone)
                drs = func(data["sql"],parafun())
                for code,value in drs.items():
                    if self.datadict.has_key(code):self.datadict[code][data["name"]] = value
        for org_code,org_data in self.datadict.items():
            
            org_data["机构日均存款净增"] = org_data.get("机构本日日均存款",0)-org_data.get("机构上年末日均存款",0)
            org_data["机构日均贷款净增"] = org_data.get("机构本日日均贷款",0)-org_data.get("机构上年末日均贷款",0)
            card_num = org_data.get("机构卡数")
            if card_num is None:
                org_data["机构活卡率"] = "0.00%"
            else:
                org_data["机构活卡率"] = "%s%%"%str("%.2f"%((org_data.get("机构活卡数",0)/card_num)*100))
        rowdata=[]
        for org_code,org_data in self.datadict.items():
            rs=[]
            for header in self.lheader:
                rs.append(org_data.get(header,0))
            rowdata.append(rs)
        return rowdata

    def init_org_dict(self):
        sql = u"select  trim(branch_code) JGBH,branch_NAME from BRANCH"
        d ={}
        rows = self.engine.execute(sql).fetchall()
        for row in rows:
            item={}
            item["机构号"]=row[0]
            item["机构名"] = row[1]
            d[row[0]] = item
        return d

    def renone(self):
        return []
    """
        需要计算的指标的配置
    """
    def data_func(self):
        self.datalist = [
            {
                "name":"机构本日日均存款",
                "func":self.simple_org_data,
                "sql" :u"""
                        select third_org_code,sum(f.credit_balance*0.01)/(days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1) je
                        from v_jgc_jghz f
                        where f.account_classify='G'  
                        and subj_code in ('2001','2002','2003','2004','2005','2006','2007','2011','2014','2017')
                        and f.credit_balance !=0  
                        and f.date_id>=%s
                        and f.date_id<=%s
                        group by third_org_code 
                      """%(self.para['TJRQ'],self.para['TJQSRQ'],self.para['TJQSRQ'],self.para['TJRQ'])

            },
            {
                "name":"机构上年末日均存款",
                "func":self.simple_org_data,
                "sql":u"""
                        select third_org_code,sum(f.credit_balance*0.01)/(days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1) je
                        from v_jgc_jghz f
                        where f.account_classify='G'  
                        and subj_code in ('2001','2002','2003','2004','2005','2006','2007','2011','2014','2017')
                        and f.credit_balance !=0  
                        and f.date_id>=%s
                        and f.date_id<=%s
                        group by third_org_code 
                    """%(self.para['JZZZRQ'],self.para['JZQSRQ'],self.para['JZQSRQ'],self.para['JZZZRQ'])
            },
            {   
                "name":"机构存款余额",
                "func":self.simple_org_data,
                "sql":"""
		            select third_org_code,sum(f.credit_balance)*0.01 je1
                    from v_jgc_jghz f
                    where date_id=? 
                    and f.account_classify='G'
                    and subj_code in ('2001','2002','2003','2004','2005','2006','2007','2011','2014','2017')
                    and (f.credit_balance!=0)
                    group by f.third_org_code
                """,
                "paralist":self.get_tjrq,
            },
            {
                "name":"机构贷款余额",
                "func":self.simple_org_data,
                "sql":"""
		            select third_org_code,sum(f.debit_balance-(f.credit_balance)*-1)*0.01 je1
                    from v_jgc_jghz f
                    where date_id=? 
                    and f.account_classify='G'
                    and f.subj_code in ('1301','1302','1303','1304','1305','1306')
                    and (f.credit_balance!=0 or f.debit_balance!=0)
                    group by f.third_org_code
                """,
                "paralist":self.get_tjrq,
            },
            {
                "name":"机构本日日均贷款",
                "func":self.simple_org_data,
                "sql" :u"""
                        select third_org_code,sum(f.credit_balance-(f.credit_balance))*0.01/(days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1) je
                        from v_jgc_jghz f
                        where f.account_classify='G'  
                        and f.subj_code in ('1301','1302','1303','1304','1305','1306')
                        and (f.credit_balance!=0 or f.debit_balance!=0)
                        and f.date_id>=%s
                        and f.date_id<=%s
                        group by third_org_code 
                      """%(self.para['TJRQ'],self.para['TJQSRQ'],self.para['TJQSRQ'],self.para['TJRQ'])

            },
            {
                "name":"机构上年末日均贷款",
                "func":self.simple_org_data,
                "sql":u"""
                        select third_org_code,sum(f.credit_balance-(f.credit_balance))*0.01/(days(to_date(%s,'yyyyMMdd') ) - days(to_date(%s,'yyyyMMdd') )+1) je
                        from v_jgc_jghz f
                        where f.account_classify='G'  
                        and f.subj_code in ('1301','1302','1303','1304','1305','1306')
                        and (f.credit_balance!=0 or f.debit_balance!=0)
                        and f.date_id>=%s
                        and f.date_id<=%s
                        group by third_org_code 
                    """%(self.para['JZZZRQ'],self.para['JZQSRQ'],self.para['JZQSRQ'],self.para['JZZZRQ'])
            },
            {   
                "name":"机构低成本存款余额",
                "func":self.simple_org_data,
                "sql":u"""
		            select third_org_code,sum(f.credit_balance)*0.01 je1
                    from v_jgc_jghz f
                    where date_id=? 
                    and f.account_classify='G'
                    and subj_code in ('200100','20020101','20020102','20020103','200301','200302','20040101','20040102','20040103','20040201','20040301','20040401','20040701','20050101','2005010201','2005010202','2005010203','20050201','2005020201','2005020202','2005020203','2005020301','2005020401','2005020501')
                    and (f.credit_balance!=0)
                    group by f.third_org_code
                """,
                "paralist":self.get_tjrq,
            },
            {
                "name":"机构对公贷款户数",
                "func":self.simple_org_data,
                "sql":u"""
                    select third_org_code ,count(1) je1
                    from  M_CUST_BALANCE c
                    where   pe_flag =  '1'
                    and c.date_id=?
                    group by third_org_code
                """,
                "paralist":self.get_tjrq,
            },
            {
                "name":"机构对私贷款户数",
                "func":self.simple_org_data,
                "sql":u"""
                    select third_org_code ,count(1) je1
                    from  M_CUST_BALANCE c
                    where   pe_flag =  '2'
                    and c.date_id=?
                    group by third_org_code
                """,
                "paralist":self.get_tjrq,
            },
            {
                "name":"机构不良贷款余额",
                "func":self.simple_org_data,
                "sql":u"""
                    select third_org_code ,count(1) je1
                    from m_loan_five c
                    where   c.loan_five in (?,?,?) 
                    and c.date_id=?
                    group by third_org_code
                """,
                "paralist":self.get_five,
            },
            {   
                "name":"表内外不良贷款",
                "func":self.simple_org_data,
                "sql":u"""
		            select third_org_code,sum(debit_balance-(credit_balance)*-1) *0.01 je1
                    from v_jgc_jghz f
                    where date_id=? 
                    and f.account_classify='G'
                    and subj_code in ('131','132','116')
                    group by f.third_org_code
                """,
                "paralist":self.get_tjrq,
            },
            {
                "name":"机构借记卡年开卡数",
                "func":self.simple_org_data,
                "sql":u"""
		            select org_code ORG_CODE,sum(num) je1
                    from  m_jgc_card m
                    where date_id = ? 
                    and card_type=? and OWNER_FLAG=? and ROW_STATUS='--'  and   OPEN_DATE<=%s
                    and (CLOSE_DATE>%s  or CLOSE_DATE=0 or CLOSE_DATE=18991231) and OPEN_DATE>= %s 
                    group by org_code
                    with ur
		        """%(self.para['TJRQ'],self.para['TJRQ'],self.para['TJQSRQ']),
                "paralist":self.get_card_num,
            },
             {   
                "name":"机构借记卡存量卡数",
                "func":self.simple_org_data,
                "sql":u"""
		            select org_code,sum(num) je1
                    from m_jgc_card m 
                    where date_id=? 
                    and card_type=? and OWNER_FLAG=? and m.ROW_STATUS ='--' 
                    group by org_code
                    with ur
                """,
                "paralist":self.get_card_num,
            },
            { 
                "name":"机构活卡数",
                "func":self.simple_org_data,
                "sql":u"""
                    select a.org_code,count(1)*1.0 live_card
                    from(
                        select  dc.main_account_no,dc.org_code,sum(TRAN_NUM) tran_num
                        from D_CONTRACT dc 
                        inner join  m_account_tran_num m on  m.contract_id= dc.id
                        where dc.contract_classify = 'C' and  dc.contract_status ='--'
                        and m.date_id>=%s and  m.date_id<=? and  dc.owner_flag =?
                        group by dc.org_code,dc.main_account_no
                        having sum(TRAN_NUM)>=4
                    ) a
                    group by  a.org_code
		        """%(self.para['TJQSRQ']),
                "paralist":self.get_card_type,
            },
            {   
                "name":"机构卡数",
                "func":self.simple_org_data,
                "sql":u"""
		            select org_code ,count(1)*1.0 card_num
                    from D_CONTRACT dc 
                    inner join f_contract f on dc.id = f.contract_id and date_id = ?
                    inner join d_contract_status ds on ds.id = f.contract_status_id and ds.ROW_STATUS = '--' and ds.owner_flag =? 
                    where dc.contract_classify = 'C'
                    group by org_code
                    with ur
                """,
                "paralist":self.get_card_type,
            },
        ]

    def get_tjrq(self):
        return self.para["TJRQ"]
    def get_five(self):
        return ['可疑','损失','次级',self.para["TJRQ"]]
    def get_card_num(self):
        return [self.para["TJRQ"],'借记卡','主卡']
    def get_card_type(self):
        return [self.para["TJRQ"],'主卡']
    """
        简单查询
    """
    def simple_org_data(self,sql,paralist):
        rows = self.engine.execute(sql.encode('gb2312'),paralist).fetchall() 
        rsdict = {}
        for row in rows:
            rsdict[row[0]] = row[1]
        return rsdict
    """
        统计日期参数，之后可能根据上传的值计算
    """
    def get_common_parameter(self):
        sql = u"""
            select TJRQ,TJQSRQ,JZQSRQ, JZZZRQ,JNTS from T_COMMON_PARAMETER 
        """
        row = self.engine.execute(sql.encode('gb2312')).fetchone() 
        d={}
        d['TJRQ']=str(row[0])
        d['TJQSRQ']=str(row[1])
        d['JZQSRQ']=str(row[2])
        d['JZZZRQ']=str(row[3])
        d['JNTS']=str(row[4])
        return d

    @property
    def page_size(self):
        return 10

    def column_header(self):
        self.lheader = ["机构号","机构名","机构日均存款净增","机构存款余额","机构日均存款净增","机构贷款余额","机构低成本存款余额","机构对公贷款户数","机构对私贷款户数","机构不良贷款余额","表内外不良贷款","机构借记卡年开卡数","机构借记卡存量卡数","机构活卡率"]
        return self.lheader
    def object_to_json(self, src_object):
        """
        对象如果不能使用默认JSON序列化的方法，请覆盖此方法
        """
        return ObjectQuery.object_to_json(self, src_object)
