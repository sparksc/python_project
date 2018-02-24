import string
import os,sys,codecs,re
def string_filter(filename):
    try:
        lines=open(filename,'r').readlines()
        flen=len(lines)
        for i in range(flen):
            #str=filter(lambda x:x in printable,lines[i])
            #lines[i]=filter(filter_detail,lines[i])

            #lines[i]=filter(filter_detail,lines[i])
            #a1 = re.compile('\x00')
            #a1 = re.compile('[\0\n]')
            a1 = re.compile('[\x00-\x09\x0b-\x1f\x7f]')
            lines[i]=a1.sub('',lines[i])
            #print lines[i]
        open('new'+filename,'w').writelines(lines)
    except Exception,e:
        print e

if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen==2:
        string_filter(sys.argv[1])
    else:
        print "please input python test_filter.py filename"
