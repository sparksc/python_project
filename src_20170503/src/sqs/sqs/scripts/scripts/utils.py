# -*- coding:utf-8 -*-
import decimal
import simplejson as json


def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            v.decode('utf8')
        out_dict[k] = v
    return out_dict


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)


def db2_pagination(page=1, page_size=10, order_by=None):
    def pagination(func):
        def wrapper(*args, **kwargs):
            this = args[0]
            results = func(*args, **kwargs)
            if isinstance(results, tuple) and len(results) > 1:
                this.raw_sql = results[0]
                this.sql_params = results[1]
            else:
                this.raw_sql = results
                this.sql_params = None
            row_start = (this.page - 1) * this.page_size + 1
            row_end = this.page * this.page_size
            str_order_by = ""
            if this.order_by:
                str_order_by = u"order by %s" % this.order_by

            sql = u"select t_e_m_p.*,row_number() over(%s) RN from (%s) t_e_m_p" % \
                (str_order_by, this.raw_sql)
            sql = u"select * from (%s) where RN between %s and %s fetch first %s rows only" % (
                sql, row_start, row_end, this.page_size)
            return sql
        return wrapper
    return pagination
