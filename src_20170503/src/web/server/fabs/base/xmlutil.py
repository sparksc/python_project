# -*- coding: utf-8 -*-
from xml.etree import ElementTree as ET
from xml.dom import minidom
import sys
reload(sys)                      # reload 才能调用 setdefaultencoding 方法  
sys.setdefaultencoding('utf-8')  # 设置 'utf-8'  

class xmlwrite:

    def __init__(self,xmlfile=''):
        self.xmlfile = xmlfile
        self.dom = minidom.getDOMImplementation('')

    def write_root(self,rootname,attributes={}):
        self.document = self.dom.createDocument(None, rootname, None)
        root = self.document.documentElement
        for key,value in attributes.items():
            root.setAttribute(key,value)
        return root

    def write_node_value(self,parentnode,nodename,attribute=None,value=None,CDATA=True):
        return self.write_node(parentnode,nodename,value,attribute,CDATA)

    def write_node(self,parentnode,nodename,attribute={},value=None,CDATA=True):
        node = self.document.createElement(nodename)
        if value:
            if CDATA:
                nodedata = self.document.createCDATASection(value)
            else:
                nodedata = self.document.createTextNode(value)
            node.appendChild(nodedata)
        if attribute and isinstance(attribute,dict):
            for key,values in attribute.items():
                node.setAttribute(key,values)
        parentnode.appendChild(node)
        return node

    def write_node_root(self):
        return self.write_root('Message',          \
                {'type':'Group' ,   \
                'xmlns:tns':'http://www.if-solutions.com/CbsMessageSchema' ,    \
                'xmlns:xsi':'http://www.w3.org/2001/XMLSchema-instance'} )


    def write_node_field(self,parentnode,name,value=None,type=1,CDATA=True):
        node = self.document.createElement('Field')
        if value:
            if CDATA:
                nodedata = self.document.createCDATASection(value)
            else:
                nodedata = self.document.createTextNode(value)
            node.appendChild(nodedata)
        attribute={
            1:{'type':'string'},
            2:{'type':'biginteger'},
            3:{'type':'date'},
            4:{'type':'bigdecimal','precision':'0'},
            5:{'type':'bigdecimal','precision':'2'},
            6:{'type':'bigdecimal','precision':'6'}
        }.get(type,1)
        attribute['name'] = name
        if attribute and isinstance(attribute,dict):
            for key,values in attribute.items():
                node.setAttribute(key,values)
        parentnode.appendChild(node)
        return node

    def write_node_head(self,parent_node,   \
                channel_name,channel_data,  \
                service_name,service_code,  \
                service_tran_name,\
                tran_code,  \
                final_flag, \
                teller_name,teller_code):
        head = self.write_node_head_tran(parent_node,   \
                channel_name,channel_data,  \
                service_name,service_code,  \
                service_tran_name,\
                tran_code,  \
                final_flag, \
                teller_name,teller_code)
        self.write_node(head, 'Author',  {'type':'List'})
        self.write_node(head, 'Auth', {'type':'List'})

    def write_node_head_tran(self,parent_node,  \
                channel_name,channel_data,  \
                service_name,service_code,  \
                service_tran_name, \
                tran_code,  \
                final_flag, \
                teller_name,teller_code):
        head = self.write_node(parent_node, 'Head', {'type':'Group'})
        self.write_node(head, 'Channel', {'type':'Field','name':channel_name}, channel_data, True)
        self.write_node(head, 'Service', {'type':'Field','timeOut':'0','name':service_name,'code':service_code}, service_code, True)
        self.write_node(head, 'ServiceName', {'type':'Field'}, service_tran_name, True)
        self.write_node(head, 'Tran', {'type':'Field'}, tran_code, True)
        self.write_node(head, 'Final', {'type':'Field'}, final_flag, True)
        self.write_node(head, 'Teller', {'type':'Field','name':teller_name,'code':teller_code}, teller_code, True)
        return head
        

    def save_xml(self):
        xmlfile = file(self.xmlfile, 'w')
        self.document.writexml(xmlfile, "\t", "\t", "\n", "UTF-8")
        xmlfile.close()
        

class xmlread():

    def __init__(self,xmlfile,expre=None):
        self.xmlfile = xmlfile
        xml = minidom.parseString(xmlfile)
        self.root = ET.fromstring(str(xml.toxml()))
        self.root_expre = (expre if expre else 'Group/Group' )
        self.root = self.root.findall(self.root_expre)


    def to_dict(self):
        category = {}
        for oneper in self.root:
            for child in oneper.getchildren():
                ctype = oneper.get('name')
                cdict = {child.get('name'):child.text}
                if category.has_key(ctype):
                    category.get(ctype).update(cdict)
                else:
                    category[oneper.get('name')] = cdict
        return category


if __name__ == '__main__':
    #print customer_xml().toxml()
    #print customer_xml()
    msg_head= str.strip('''
                <?xml version="1.0" encoding="UTF-8"?>
                <Group name="Message">
                <Group name="Response">
                <Group name="ResponseBodyData">
                <Field name="交易流水" type="biginteger"><![CDATA[1700003596]]></Field>
                </Group>
                <Group name="Status">
                <Field name="code" type="string"><![CDATA[0]]></Field>
                <Field name="reason" type="string"><![CDATA[交易成功]]></Field>
                </Group>
                </Group>
                </Group>
        ''')
    print msg_head

    cdict = xmlread(msg_head).to_dict()
        #cdict = xmlread('customer_add_suucess.xml').to_message_dict()
    print cdict.get('ResponseBodyData').get(u'交易流水')




