import threading
import urllib2
import commonlib
import datetime
from BeautifulSoup import BeautifulSoup
import time




class Pasteru(threading.Thread):

    def __init__(self,lib):
        threading.Thread.__init__(self)
        self.basic_url = "http://paste.org.ru"
        self.lib = lib


    def run(self):
        print "Starting Paste.ru Thread"
        while 1:
            self.pasteru()
            time.sleep(10)
        print "Exiting Paste.ru Thread"




    def pasteru(self):

        can = True
        while can:
            try:
                html=self.lib.request_url(self.basic_url)
                # html = urllib2.urlopen("http://pastebin.com/archive").read()
                can = False
            except:
                pass

        soup=BeautifulSoup(html)

        td = soup.find('td',{ "id" : "left" })
        div = td.findAll('div')[0]


        aHref = div.findAll('a')



        for a in aHref:
            final_url = self.basic_url + a['href']
            try:
                html=self.lib.request_url(final_url)
            except:
                continue

            soup=BeautifulSoup(html)

            div = soup.find('textarea',{ "name" : "code" }).text

            try:
                b = self.lib.search_regex(div)
            except:
                continue

            if b:
                print "La url: " + final_url + " coincide con alguna de las busquedas!"
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.lib.write_global_document(final_url)
                self.lib.create_find_document(a['href'][1:],div,"paste.ru")
                self.lib.send_email(div,"paste.ru",final_url)

