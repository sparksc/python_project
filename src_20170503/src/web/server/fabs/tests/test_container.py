from tornado import ioloop
from kazoo.client import KazooClient

class Container(object):
    def __init__(self, zk_url='localhost:2181'):
        self.zk=KazooClient(hosts=zk_url)
        self.servers={}
    #TODO: finish it!!! now just start zk
    def run(self):
        self.zk.start()
    #TODO: remove_server
    def add_server(self, server):
        if server.name in self.servers:
            raise Exception('server name exist %s'%server.name)
        self.servers[server.name]=server

    def start_server(self, name):
        self.servers['name'].start()

    def stop_server(self, name):
        self.servers['name'].stop()

    def start_all(self):
        for server in self.servers.values():
            server.start()
        ioloop.IOLoop.current().start()

    def stop_all(self):
        for server in self.servers.values():
            server.stop()


from ..server.admin import WebAdminServer
#TODO: run parameters?
def run():
    container=Container()
    container.run()
    #container.add_server(WebAdminServer())
    container.start_all()


from ..server.admin import admin_method
from multiprocessing import Process
from time import sleep
from ..server.admin import JSONRPCAdminClient
class test_run():
    def test_run_container(arg):
        @admin_method
        def do_things(arg):
            print 'arg:',arg
            return arg

        def run_server():
            run()

        def run_client():
            print JSONRPCAdminClient('http://localhost:9100/admin/jsonrpc/').call('do_things', 'this')
        p1=Process(target=run_server)
        p1.start()
        sleep(1)
        p2=Process(target=run_client)
        p2.start()
        p2.join()
        p1.terminate()
        p1.join()

#if __name__=='__main__':
#    test_run_container()
