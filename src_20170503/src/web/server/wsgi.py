# -*- coding: utf-8 -*-
"""
    wsgi
    ##########
    yinsho wsgi module
"""
BASEPATH = '/Users/zxzhao'
ALLDIRS = [BASEPATH + '/lib/python2.7/site-packages']
activate_this = BASEPATH + '/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
import os
import site

sys.stdout = sys.stderr
# Remember original sys.path.
prev_sys_path = list(sys.path)
# Add each new site-packages directory.
for directory in ALLDIRS:
        site.addsitedir(directory)
# Reorder sys.path so new directories at the front.
new_sys_path = []
for item in list(sys.path):
        if item not in prev_sys_path:
                new_sys_path.append(item)
                sys.path.remove(item)
sys.path[:0] = new_sys_path


sys.path.insert(0, '/Users/zxzhao/Documents/workspace/Python/')
sys.path.insert(0, '/Users/zxzhao/Documents/workspace/Python/clown/')
sys.path.insert(1, '/Users/zxzhao/Documents/workspace/Python/etl/')
os.environ['PYTHON_EGG_CACHE'] = BASEPATH + '/.python-eggs'

from yinsho.views import app
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
