#!/usr/bin/python
__author__ = 'MiqueT'
# ProxyListCreator crea una lista de proxys. Por Miquel Tur (miquel.tur.m@gmail.com)

# Esta obra esta sujeta a la licencia Reconocimiento-NoComercial 4.0 Internacional de Creative Commons

# Usage example: python ProxyListCreator.py

import urllib2
import socket
import sys
from BeautifulSoup import BeautifulSoup

class ProxyListCreator():
    def __init__(self,proxyPath='/'):
        self.route = 'http://free-proxy-list.net/'
        self.path = proxyPath
        socket.setdefaulttimeout(2)

    def create_list(self,max=10):
        proxy_list = []

        html=urllib2.urlopen(self.route).read()


        soup=BeautifulSoup(html)

        table = soup.find('table',{ "id" : "proxylisttable" })


        trs = table.find('tbody').findAll('tr')

        for tr in trs[1:]:
            tds = tr.findAll('td')
            if len(tds) > 0:
                proxy = str(tds[0].text) + ":" + tds[1].text
                https = tds[6].text

                if(self.check_proxy(proxy)):
                    complet = {"proxy":proxy, "https":https}
                    proxy_list.append(complet)
                    if (len(proxy_list) >= max): break

        self.create_proxy_file_list(proxy_list)



    def check_proxy(self,proxy):
        try:
            proxy_handler = urllib2.ProxyHandler({'http': proxy})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib2.install_opener(opener)
            req=urllib2.Request('http://www.googles.com')  # change the URL to test here
            sock=urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            # print 'Error code: ', e.code
            return e.code
        except Exception, detail:
            # print "ERROR:", detail
            return False
        return True


    def create_proxy_file_list(self,list):
        if len(list)>1:
            f = None
            try:
                f = open(self.path, 'w')

            except:
                print "FAIL - impossible to open file: proxyList.conf"
                sys.exit(0)

            if f:
                for p in list:
                    httpsf = "https"
                    if 'no' in p["https"]: httpsf= "http"
                    f.write(p["proxy"] + " " + httpsf )
                    f.write("\n")

                f.close()
        else:
            print "No se ha podido crear la proxyList, vuelvalo a intentar mas tarde"
            sys.exit(0)






if __name__ == "__main__":
    plc = ProxyListCreator()
    plc.create_list()
