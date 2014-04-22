import threading
import urllib2
import commonlib
import datetime
from BeautifulSoup import BeautifulSoup
import time




class Pastelisp(threading.Thread):

    def __init__(self,lib):
        threading.Thread.__init__(self)
        self.basic_url = "http://paste.lisp.org"
        self.lib = lib


    def run(self):
        print "Starting pastelisp Thread"
        while 1:
            self.pastelisp()
            time.sleep(10)
        print "Exiting pastelisp Thread"




    def pastelisp(self):

        can = True
        while can:
            try:
                html=self.lib.request_url(self.basic_url+"/list")
                # html = urllib2.urlopen("http://pastebin.com/archive").read()
                can = False
            except:
                pass

        soup=BeautifulSoup(html)

        table = soup.find('table',{ "class" : "detailed-paste-list" })



        aHref = table.findAll('a')



        for a in aHref:
            final_url = a['href']

            splited = final_url.split('/')
            lent = len(splited)
            id = splited[lent-1]

            try:
                html=self.lib.request_url(final_url+"/raw")
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
                self.lib.create_find_document(id,html,"pastelisp")
                self.lib.send_email(html,"pastelisp",final_url)

