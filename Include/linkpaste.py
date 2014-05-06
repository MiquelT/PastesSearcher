import threading
import urllib2
import commonlib
import datetime
from BeautifulSoup import BeautifulSoup
import time




class Linkpaste(threading.Thread):

    def __init__(self,lib):
        threading.Thread.__init__(self)
        self.first_url = "http://www.linkpaste.com/last-pastes.html"
        self.lib = lib
        self.found = []


    def run(self):
        print "Starting linkpaste Thread"
        while 1:
            try:
                self.linkpaste()
            except:
                print "**Error in linkpaste"
                time.sleep(60)
                pass

            time.sleep(10)
        print "Exiting linkpaste Thread"







    def linkpaste(self):

        can = True
        while can:
            try:
                html=self.lib.request_url(self.first_url)
                can = False
            except:
                pass

        soup=BeautifulSoup(html)

        table = soup.findAll('table',{ "id" : "example" })[0]

        aHref = table.findAll('a')

        for a in aHref:
            try:
                if not "/user/" in a['href']:
                    final_url = a['href']
                    id = final_url.split('/')[1]
                    try:
                        html=self.lib.request_url(final_url)
                    except:
                        continue

                    soup=BeautifulSoup(html)
                    div = soup.findAll('div',{ "class" : "row pasteshere" })[0].text

                    try:
                        b = self.lib.search_regex(div)
                    except:
                        continue

                    if b and not id in self.found:
                        self.found.append(id)
                        print "La url: " + final_url + " coincide con alguna de las busquedas!"
                        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.lib.write_global_document(final_url)
                        self.lib.create_find_document(id,div,"linkpaste")
                        self.lib.send_email(html,"linkpaste",final_url)
            except:
                continue
