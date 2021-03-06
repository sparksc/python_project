# -*- coding: utf-8-*-
from collections import Iterable
import tempfile
import json
from decimal import  *

def object_to_json(src_object):
    return json.dumps(src_object)

class groupby(object):
    '''
       对数据按照指定的列进行分组
    '''
    def __init__(self, iterable, groups,  maxgroups):
        '''
            iterable : 分组的数据
            groups: 分组列
            maxgoups: 最大分组列
        '''
        self.groups = groups
        self.gps = groups
        self.maxgroups = maxgroups
        if groups is None:
            key = lambda x: x
        else:
            key  = lambda item:[ item[x] for x in groups ]
        self.keyfunc = key
        self.it = iter(iterable)
        self.tgtkey = self.currkey = self.currvalue = object()

    def __iter__(self):
        return self

    def next(self):
        while self.currkey == self.tgtkey:
            self.currvalue = next(self.it)    # Exit on StopIteration
            self.currkey = self.keyfunc(self.currvalue)
        self.tgtkey = self.currkey
        if len(self.groups) < len(self.maxgroups) :
            return ((self.currkey,self.gps), groupby(self._grouper(self.tgtkey), self.maxgroups[0:len(self.groups)+1], self.maxgroups))
            return (self.currkey, groupby(self._grouper(self.tgtkey), self.maxgroups[0:len(self.groups)+1], self.maxgroups))
        else:
            return ( (self.currkey, self.gps), self._grouper(self.tgtkey) )
            return ( self.currkey, self._grouper(self.tgtkey) )

    def _grouper(self, tgtkey):
        while self.currkey == tgtkey:
            yield self.currvalue 
            self.currvalue = next(self.it)    # Exit on StopIteration
            self.currkey = self.keyfunc(self.currvalue)
            self.gps = self.groups




class DataGroup():
    '''
        对分组后的数据遍历(打印或者输出到指定文件)
        同时按照分组后的数据增加小计,总计数据
    '''
    def __init__(self, data, groups, sumcols, totalflag):
        '''
            data:分组数据
            groups:分组列
            sumcols:汇总列
            totalflag:是否总计
        '''
        self.cols_merge = {}
        self.data = data
        self.groups = groups
        self.sumcols = sumcols
        self.totalflag = totalflag
        self.object_to_json_fun = object_to_json
        self.result_file  = None
        self.merge_file  = None
        min_sum_cols = -1
        for x in sumcols:
            if x > min_sum_cols: 
                min_sum_cols = x
                break
        self.min_sum_cols = min_sum_cols
        self.total_count = 0
        pass

    def print_csv(self, idx, row):
        if self.result_file is None:
            for x in row:
                print x,",",
            print idx
        else:
            self.result_file.write(self.object_to_json_fun(row) + '\n')

    def data_group_by(self):
        if self.groups is None or len(self.groups) == 0:
            return groupby(self.data, [], [])
        else:
            return groupby(self.data, [self.groups[0]], self.groups)
    
    def amount_trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        mon = '{:,}'.format(tmp)
        return mon

    def to_decimal(self,num):
        if isinstance(num,str) or isinstance(num,unicode):
            return Decimal(num.replace(",",""))
        else:
            return num

    def sum_row(self, sum, row):
        if sum is None:
            return  row
        else:
            for c in self.sumcols:
                am1 = self.to_decimal(sum[c])
                am2 = self.to_decimal(row[c])
                sum[c] = self.amount_trans_dec(self.to_decimal(sum[c]) + self.to_decimal(row[c]))
        return sum
    
    def merge_row(self, ridx, row,cnt = "小计"):
        if row is None:
            return None
        col_num = len(row)
        min = None
        max = None
        for i in range(col_num):
            if row[i] is None:
                if min is None : min = i
                if (max is None or i > max) and i < self.min_sum_cols : max = i
        if max is None: max  = min
        if min != 0 and min is not None:
            min = min - 1
            #self.cols_merge[ ridx,(min,max) ] = cnt
            self.cols_merge[ str(ridx) ] = (min,max)
            return (min,cnt)
        else:
            self.cols_merge[ str(ridx) ] = (0,max)
            return (0,cnt)

    def set_row_none(self, row, key):
        if row is None: return None
        col_num = len(row)
        for i in range(col_num):
            if i in key or i in self.sumcols:
                pass
            else:
                row[i] =  None
        return row

    def iter_rows(self, key, iter_data, ridx, first, tsum):
        sum = None
        fidx =  ridx
        for  row in iter_data:
            t = type(row[1])
            if len(row) == 2 and ( isinstance(row[1], groupby) or isinstance(row[1], Iterable) ) :
                bridx  = ridx
                sum0,ridx = self.iter_rows(row[0], row[1], ridx,False, tsum)
                sum = self.sum_row(sum, sum0)
                col_num = len(sum0)
                sum0 = self.set_row_none(sum0, key[1])
                k = key[1][ len(key[1]) -1 ] + 1
            else:
                self.print_csv(ridx,row)
                sum = self.sum_row(sum, row)
                sum = self.set_row_none(sum, key[1])
                ridx  = ridx + 1
        if first:
            sum = self.set_row_none(sum, [])
            if len(key) <=1 or len(key[1]) <= 0 :
                pass
            else:
                k = key[1][ len(key[1]) -1 ] 
                self.cols_merge[ str(ridx-1) + "-" + str(k) ]  =  (fidx,ridx-1)
                (min, cnt) = self.merge_row(ridx,sum)
                sum[min] = cnt
                self.print_csv(ridx, sum)
                ridx  = ridx + 1
        else:
            k = key[1][ len(key[1]) -1 ] #+ 1
            self.cols_merge[ str(ridx-1) + "-" + str(k) ]  =  (fidx,ridx-1)
            #sum[k] = '小计'
            (min,cnt) = self.merge_row(ridx,sum)
            sum[min] = cnt
            self.print_csv(ridx, sum)
            ridx  = ridx + 1
        return (sum,ridx)

    def group_by_cols_to_file(self, result_file = None, object_to_json_fun=None):
        self.result_file = result_file
        if object_to_json_fun is not None:
            self.object_to_json_fun = object_to_json_fun
        group_result = self.data_group_by()
        ridx = 0
        sum0 = None
        ts = None
        for g in group_result:
            sum1,ridx = self.iter_rows(g[0], g[1], ridx, True, sum0)
            ts = self.sum_row(ts, sum1)
        if ts is not None:
            (min,cnt) = self.merge_row(ridx,ts,"总计")
            self.total_count = ridx + 1
            ts[min] = cnt
            self.print_csv(ridx, ts)

    def to_merge_file(self, merge_file):
        self.merge_file = merge_file
        self.merge_file.write( self.object_to_json_fun(self.cols_merge) )

    def print_merge(self):
        for k in self.cols_merge:
            print k,self.cols_merge[k]

def to_html(f1,f2):
    f = open(f1)
    mg = None
    for row in f:
        mg = json.loads(row)
    f.close()

    f = open(f2)
    mg = None
    idx = 0
    for row in f:
        nrow  = json.loads(row)
        for x in nrow:
            print x,",",
        print idx
        idx = idx + 1
    f.close()

    #def print_merge(self):
    #    #self.result_file = tempfile.NamedTemporaryFile(delete=False)
    #    for k in self.cols_merge:
    #        print k ,self.cols_merge[k]


if __name__ == "__main__":
    data = [
        ["A1","B1","C1",1,2,5.1],
        ["A1","B1","C2",1,2,6.2],
        ["A1","B2","C3",1,2,7.3],
        ["A1","B2","C4",1,2,3],
        ["A2","B2","C3",1,2,3],
        ["A2","B2","C4",1,2,3],
    ]
    cols = [0,1]
    dg = DataGroup(data,cols,[3,4,5],True)
    #result_file = tempfile.NamedTemporaryFile(delete=False)
    #dg.group_by_cols_to_file( result_file, object_to_json )
   
    dg.group_by_cols_to_file( )
    #dg.to_merge_file()
    #print dg.merge_file.name
    #to_html(dg.merge_file.name, dg.result_file.name)
    #dg.print_merge()
