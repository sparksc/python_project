# -*- coding:utf-8 -*-
from  ..server import configure
from pika import BlockingConnection, ConnectionParameters
#from test_build import JJYTestCase

class process_test():

    def send_service_test(aa):
    #    connection=BlockingConnection(ConnectionParameters('localhost'))
    #    channel=connection.channel()
    #    channel.basic_publish(exchange='', routing_key='test_service', body='test ok')
        print 'test_process'
