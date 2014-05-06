import threading
import urllib2
import commonlib
import datetime
from BeautifulSoup import BeautifulSoup
import time




class Pastebin(threading.Thread):

    def __init__(self,lib):
        threading.Thread.__init__(self)
        self.pastebin_url = "http://pastebin.com/raw.php?i="
        self.lib = lib
        self.found = []


    def run(self):
        print "Starting Pastebin Thread"
        while 1:
            try:
                self.pastebin()
            except:
                print "**Error in Pastebin"
                time.sleep(60)
                pass
            time.sleep(10)
        print "Exiting Pastebin Thread"







    def pastebin(self):

        can = True
        while can:
            try:
                html=self.lib.request_url("http://pastebin.com/archive")
                can = False
            except:
                pass

        soup=BeautifulSoup(html)

        table = soup.findAll('table',{ "class" : "maintable" })[0]

        aHref = table.findAll('a')



        for a in aHref:
            try:
                if not "archive/" in a['href']:
                    id = a['href'][1:]
                    final_url = "http://pastebin.com/raw.php?i=" + id

                    try:
                        html=self.lib.request_url(final_url)
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
                        self.lib.create_find_document(id,html,"pastebin")
                        self.lib.send_email(html,"pastebin",final_url)
            except:
                continue
