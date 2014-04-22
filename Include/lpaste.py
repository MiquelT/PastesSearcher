import threading
import urllib2
import commonlib
import datetime
from BeautifulSoup import BeautifulSoup
import time




class Lpaste(threading.Thread):

    def __init__(self,lib):
        threading.Thread.__init__(self)
        self.lpaste_url = "http://lpaste.net/browse?pastes_page="
        self.basic_url = "http://lpaste.net/raw"
        self.lib = lib


    def run(self):
        print "Starting Lpaste Thread"
        while 1:
            self.lpaste()
            time.sleep(10)
        print "Exiting Lpaste Thread"







    def lpaste(self):
        for i in range(1,5):
            can = True
            while can:
                try:
                    html=self.lib.request_url(self.lpaste_url + str(i))
                    # html = urllib2.urlopen("http://pastebin.com/archive").read()
                    can = False
                except:
                    pass

            soup=BeautifulSoup(html)

            table = soup.find('table',{ "class" : "latest-pastes" })
            aHref = table.findAll('a')


            for a in aHref:
                if not "/browse" in a['href']:
                    final_url = self.basic_url + a['href']
                    try:
                        html=self.lib.request_url(final_url)
                    except:
                        continue

                    try:
                        b = self.lib.search_regex(html)
                    except:
                        continue

                    if b:
                        print "La url: " + final_url + " coincide con alguna de las busquedas!"
                        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.lib.write_global_document(final_url)
                        self.lib.create_find_document(a['href'][1:],html,"Lpaste")
                        self.lib.send_email(html,"Lpaste",final_url)

