# -*- coding:utf-8 -*-
#!/bin/python  

from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random,sys 
from datetime import datetime,timedelta
from decimal import *
import DB2  

from etl.base.conf import *
import etl.base.util as util
from etl.star.dim import *
from etl.star.transformdict import *
from etl.base.singleton import singleton
     
from etl.base.logger import info


condecimal = getcontext()

class StarManage():
    def __init__(self, facts=1, dims=None):
        if dims is None:
            self.dims = []
        else:
            self.dims = dims
        self.dim_process = []
        self.fact_process = []
        self.fact_index = 0

        self.manager = multiprocessing.Manager()
        self.dim_queue = self.manager.Queue()
        self.fact_queue = []
        for x in range(facts):
            q = self.manager.Queue()
            self.fact_queue.append( q )

    def start_dim_process(self):
        pw1 = Process(target=queue2db, args=( self.dim_queue, ))
        self.dim_process.append( pw1 )

    def start_fact_process(self):
        for q in self.fact_queue:
            pw1 = Process(target=queue2db, args=( q, ))
            self.fact_process.append( pw1 )

    def setDimQueue(self):
        for dim in self.dims:
            dim.setQueue( self.dim_queue )

    def put_dim_data(self,data):
        if self.dim_queue is not None:
            self.dim_queue.put( data )

    def get_next_fact_queue(self):
        self.fact_index = self.fact_index + 1
        if self.fact_index >= len(self.fact_process):
            self.fact_index = 0
        return self.fact_queue[self.fact_index]

    def put_fact_data(self,data):
        q = self.get_next_fact_queue()
        q.put( data )

    def start(self):
        for p in self.fact_process:
            p.start()
        for p in self.dim_process:
            p.start()

    def restart_fact_process(self):
        for q in self.fact_queue:
            q.put(None)
        for p in self.fact_process:
            p.join()
        self.fact_process = []

        self.start_fact_process()
        for p in self.fact_process:
            p.start()

    def finish(self):

        self.dim_queue.put(None)
        for q in self.fact_queue:
            q.put(None)

        for p in self.dim_process:
            p.join()
        for p in self.fact_process:
            p.join()

@singleton
class StarBase():
    def __init__(self):
        pass

    def files2fact(self, ds, sm):
        d0 = datetime.now()
        factsqls = ds.fact_sql()
        factlen = len(factsqls)
        for row,flag in ds.to_fact_row() :     
            if flag == False: continue
            if row is None : break
            temp = ds.transfor_one_fact(row) 
            if temp is None : continue
            for i in range(factlen):
                rd = temp[i]
                if rd is None:
                    continue
                sm.put_fact_data( (factsqls[i], rd) )

    def files2fact2(self, ds, sm):
        d0 = datetime.now()
        factsqls = ds.fact_sql()
        factlen = len(factsqls)
        for row,flag in ds.to_fact_row2() :     
            if flag == False: continue
            if row is None : break
            temp = ds.transfor_one_fact(row) 
            if temp is None : continue
            for i in range(factlen):
                rd = temp[i]
                if rd is None:
                    continue
                sm.put_fact_data( (factsqls[i], rd) )
