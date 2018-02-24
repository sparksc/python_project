#encoding=utf-8
import unittest
import httplib, urllib
import logging



class TestSMS(unittest.TestCase):


    def test_sms(self):
        httpClient = None
        try:
            params = urllib.urlencode({'userId': 'JC2280', 'password': '366620' \
                    , 'pszMobis':'18602198412', 'pszMsg':'ceshi', 'iMobiCount':'1','pszSubPort':'*' })
            headers = {"Content-type": "application/x-www-form-urlencoded" \
                            , "Accept": "text/plain"}

            httpClient = httplib.HTTPConnection("61.145.229.29", 9003, timeout=30)
            httpClient.request("POST", "/MWGate/wmgw.asmx/MongateCsSpSendSmsNew", params, headers)

            response = httpClient.getresponse()
            logging.debug(response.status)
            logging.debug(response.reason)
            logging.debug(response.read())
            logging.debug(response.getheaders())
        except Exception, e:
            logging.debug(e)
        finally:
            if httpClient:
                httpClient.close()
