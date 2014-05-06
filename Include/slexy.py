import threading
import urllib2
import commonlib
import datetime
from BeautifulSoup import BeautifulSoup
import time




class Slexy(threading.Thread):

    def __init__(self,lib):
        threading.Thread.__init__(self)
        self.slexy_url = "http://slexy.org/slexy/recent/"
        self.basic_url = "http://slexy.org"
        self.lib = lib
        self.found = []


    def run(self):
        print "Starting Slexy Thread"
        while 1:
            try:
                self.slexy()
            except:
                print "**Error in Slexy"
                time.sleep(60)
                pass
            time.sleep(10)
        print "Exiting Slexy Thread"







    def slexy(self):
        for i in range(1,10):
            can = True
            while can:
                try:
                    html=self.lib.request_url(self.slexy_url + str(i))
                    can = False
                except:
                    pass

            soup=BeautifulSoup(html)

            maindiv = soup.find('div',{ "class" : "main" })

            table = maindiv.find("table")

            aHref = table.findAll('a')

            for a in aHref:
                try:
                    id = a['href'].split('/')[2]
                    final_url = self.basic_url+ a['href']

                    try:
                        html=self.lib.request_url(final_url)
                        soup=BeautifulSoup(html)
                        html = soup.find('div',{ "style" : "font-family:monospace;" }).text
                    except:
                        continue



                    try:
                        b = self.lib.search_regex(html)
                    except:
                        continue

                    if b and not id in self.found:
                        self.found.append(id)
                        print "La url: " + final_url + " coincide con alguna de las busquedas!"
                        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.lib.write_global_document(final_url)
                        self.lib.create_find_document(id,html,"Slexy")
                        self.lib.send_email(html,"Slexy",final_url)
                except:
                    continue

