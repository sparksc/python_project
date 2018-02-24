# -*- coding:utf-8 -*-
import logging
log = logging.getLogger()
import ibm_db
import datetime
class DB2:
    def db_conn(self):
        self.conn= ibm_db.connect('HOSTNAME=192.168.10.190;PORT=60000;DATABASE=creditdb;UID=whxd;PWD=pass;','','')
        #cur = conn.cursor()
        self.cols={}
        self.row=None
        self.result=None
        #server = ibm_db.server_info(self.conn)
        #print server
        #return conn

    def exesql(self,sql,tb):
        u'''
        
        '''
        #self.cols=[]
        self.cols={}
        col = ibm_db.columns(self.conn,None,None,tb) 
        el = ibm_db.fetch_both(col)
        index = 0
        while(el):
            self.cols[el['COLUMN_NAME']]=index;
            index = index + 1
            el = ibm_db.fetch_both(col) 
        self.result = ibm_db.exec_immediate(self.conn,sql) 
        self.row = ibm_db.fetch_tuple(self.result)
    def is_end(self):
        if (self.row):
            return False
        else:
            return True
    def get_byName(self,col_name):
        #print self.cols
        if self.row:
            value = self.row[self.cols[col_name]]
            if type(value) in [str,unicode]:
                  return value.strip()     
            else:
                  return value

    def get_next(self):
        rt = self.row
        if(self.row):
            self.row = ibm_db.fetch_tuple(self.result)
        return rt
    def close(self):
        ibm_db.close(self.conn)

def filterTables():
#    conn = ibm_db.connect('HOSTNAME=192.168.10.86;PORT=50000;DATABASE=QZ1109B;UID=administrator;PWD=pass;','','')
    conn = ibm_db.connect('HOSTNAME=192.168.10.190;PORT=60000;DATABASE=creditdb;UID=whxd;PWD=pass;','','')
    server = ibm_db.server_info( conn )
    print server
    col = ibm_db.columns(conn,None,None,"CUS_PER") 
    el = ibm_db.fetch_both(col)
    print el
    while(el):
        print '----------'
        print el['COLUMN_NAME'],
        print '----------'
        el = ibm_db.fetch_both(col) 

    result = ibm_db.exec_immediate(conn,"select name,type,creator from sysibm.systables where  type='T' and creator='WHXD'")
    row = ibm_db.fetch_tuple(result)
    tableName = []
    while ( row ):
        tableName.append(row[0]) #final = ", " + row[1] + ", " + row[2] + ", " + row[3] + ", , ";
        row = ibm_db.fetch_tuple(result)

    return tableName
def filterEmp(tableName):
#    conn = ibm_db.connect('HOSTNAME=192.168.10.86;PORT=50000;DATABASE=QZ1109B;UID=administrator;PWD=pass;','','')
    conn = ibm_db.connect('HOSTNAME=192.168.10.190;PORT=60000;DATABASE=creditdb;UID=whxd;PWD=pass;','','')
    server = ibm_db.server_info( conn )
    have = []
    no = []
    for tb in tableName:
        stmt = ibm_db.exec_immediate(conn, "SELECT count(*) FROM %s"%(tb,))
        res = ibm_db.fetch_tuple(stmt)
        rows = res[0]
#        print rows,
        if rows == 0:
            no.append(tb)
        else:
            have.append(tb)
    fl = open('tablename.txt','w')
    name = u'有数据的表%d张\n'%(len(have),)
#    print name
    fl.write(name.encode('utf-8'))
    for c in have:
        fl.write('[ '+c+' ] ')
    name = u'\n\n没有数据的表字段%d张\n'%(len(no),)
    fl.write(name.encode('utf-8'))
    for c in no:
        fl.write('[ '+c+' ] ')
    fl.close() 
#    print len(have),have
#    print len(no),no
    asd = open('asd.txt','r')
    text = asd.read()
    asd.close()
#    print '**'*20
    count = 0
    asd = text.split(',')
#    print len(asd)
    asdList = []
    for one in asd:
        if one.upper() in have:
#            print one.upper()
            have.remove(one.upper())        
            asdList.append(one.upper())
            count = count + 1
#    print asdList
#    count
#    print len(have),have
if __name__=='__main__':
    tableName = filterTables()
#    print len(tableName)
    filterEmp(tableName)
