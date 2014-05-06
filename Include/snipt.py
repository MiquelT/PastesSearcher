import threading
import urllib2
import commonlib
import datetime
from BeautifulSoup import BeautifulSoup
import time




class Snipt(threading.Thread):

    def __init__(self,lib):
        threading.Thread.__init__(self)
        self.snipt_url = "https://snipt.net/public/?page="
        self.lib = lib
        self.found = []


    def run(self):
        print "Starting Snipt Thread"
        while 1:
            try:
                self.snipt()
            except:
                print "**Error in Snipt"
                time.sleep(60)
                pass
            time.sleep(10)
        print "Exiting Snipt Thread"



    def snipt(self):
        for i in range(1,25):
            can = True
            while can:
                try:
                    html=self.lib.request_url(self.snipt_url + str(i))
                    can = False
                except:
                    pass

            soup=BeautifulSoup(html)

            articles = soup.findAll('article')

            for article in articles:
                try:
                    foot = article.find('footer')

                    as1 = foot.findAll('a')
                    for a in as1:
                        if "Raw" in a.text and not "nice" in a["href"]:
                            id = a['href'].replace('/','_')
                            final_url = a['href']
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
                                self.lib.create_find_document(id,html,"Snipt")
                                self.lib.send_email(html,"Snipt",final_url)
                except:
                    continue

