import threading
import urllib2
import commonlib
import datetime
from BeautifulSoup import BeautifulSoup
import time




class Codepad(threading.Thread):

    def __init__(self,lib):
        threading.Thread.__init__(self)
        self.codepad_url_recent = "http://codepad.org/recent"
        self.codepad_url = "http://codepad.org/"
        self.lib = lib
        self.found = []


    def run(self):
        print "Starting Codepad Thread"
        while 1:
            try:
                self.codepad()
            except:
                print "**Error in Codepad"
                time.sleep(60)
                pass
            time.sleep(10)
        print "Exiting Codepad Thread"




    def codepad(self):

        can = True
        while can:
            try:
                html=self.lib.request_url(self.codepad_url_recent)
                can = False
            except:
                pass

        soup=BeautifulSoup(html)

        sections = soup.findAll('div',{ "class" : "section" })


        for sec in sections:
            try:
                as1 = sec.findAll('a')
                for a1 in as1:
                    if "view" in a1:
                        final_url = a1["href"]
                        id = final_url.split('/')[1]
                        try:
                            html=self.lib.request_url(final_url)
                        except:
                            continue

                        soup=BeautifulSoup(html)
                        span = soup.findAll('span',{ "class" : "menu" })[5]
                        fa = span.findAll('a')

                        for a in fa:
                            if "raw code" in a.text:
                                try:
                                    html=self.lib.request_url(a["href"])
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
                                    self.lib.create_find_document(id,html,"codepad")
                                    self.lib.send_email(html,"codepad",final_url)

            except:
                continue