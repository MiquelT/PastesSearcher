import threading
import urllib2
import commonlib
import datetime
from BeautifulSoup import BeautifulSoup
import time




class Ideone(threading.Thread):

    def __init__(self,lib):
        threading.Thread.__init__(self)

        self.ideone_url_r = "http://ideone.com/recent/"
        self.ideone_url = "http://ideone.com/plain"

        self.lib = lib


    def run(self):
        print "Starting Ideone Thread"
        while 1:
            self.ideone()
            time.sleep(10)
        print "Exiting Ideone Thread"







    def ideone(self):
        for i in range(1,25):
            can = True
            while can:
                try:
                    html=self.lib.request_url(self.ideone_url_r + str(i))
                    can = False
                except:
                    pass

            soup=BeautifulSoup(html)
            divsv = soup.findAll('div',{"class" : "source-view"})

            for div in divsv:
                a = div.findAll('a')[0]
                final_url = self.ideone_url + a['href']
                try:
                    html=self.lib.request_url(final_url)
                except:
                    continue

                pre=BeautifulSoup(html).text

                try:
                    b = self.lib.search_regex(pre)
                except:
                    continue

                if b:
                    print "La url: " + final_url + " coincide con alguna de las busquedas!"
                    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.lib.write_global_document(final_url)
                    self.lib.create_find_document(a['href'][1:],pre,"Ideone")
                    self.lib.send_email(pre,"Ideone",final_url)
