import threading
import urllib2
import commonlib
import datetime
from BeautifulSoup import BeautifulSoup
import time




class Dropbucket(threading.Thread):

    def __init__(self,lib):
        threading.Thread.__init__(self)
        self.dropbucket_url = "http://dropbucket.org/snippets/new?page="
        self.basic_url = "http://dropbucket.org"
        self.lib = lib
        self.found = []


    def run(self):
        print "Starting Dropbucket Thread"
        while 1:
            try:
                self.dropbucket()
            except:
                print "**Error en dropbucket"
                time.sleep(60)
                pass
            time.sleep(10)
        print "Exiting Dropbucket Thread"



    def dropbucket(self):
        for i in range(10):
            can = True
            while can:
                try:
                    html=self.lib.request_url(self.dropbucket_url + str(i))
                    can = False
                except:
                    pass

            soup=BeautifulSoup(html)

            principaldiv = soup.find('div',{ "id" : "content-wrapper-inner" })
            ul = principaldiv.find('ul',{ "class" : "snippets-list clearfix" })
            h2 = ul.findAll('h2',{ "class" : "snippet-title" })


            for title in h2:
                try:
                    a =  title.find('a')
                    rawnum = 0
                    braw = True
                    while braw:
                        final_url = self.basic_url + a['href'] + "/raw/" + str(rawnum)
                        id = a['href'].split('/')[2]

                        try:
                            html=self.lib.request_url(final_url)
                        except:
                            braw = False
                            continue

                        rawnum += 1


                        try:
                            b = self.lib.search_regex(html)
                        except:
                            continue

                        if b and not id in self.found:
                            self.found.append(id)
                            print "La url: " + final_url + " coincide con alguna de las busquedas!"
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            self.lib.write_global_document(final_url)
                            self.lib.create_find_document(id,html,"Dropbucket")
                            self.lib.send_email(html,"Dropbucket",final_url)
                except:
                    continue
