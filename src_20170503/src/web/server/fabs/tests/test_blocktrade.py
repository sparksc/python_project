# -*- coding=utf-8 -*-
from ..domain.blocktrade import run_blocktrade_tran 

def test_query_blocktrade_tran():
    run_blocktrade_tran('20141215')

if __name__ == '__main__':
    test_query_blocktrade_tran()
