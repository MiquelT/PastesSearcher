import threading
import urllib2
import commonlib
import datetime
from BeautifulSoup import BeautifulSoup
import time




class Pastie(threading.Thread):

    def __init__(self,lib):
        threading.Thread.__init__(self)

        self.pastie_id_digits = "0123456789"
        self.pastie_url_f = "http://pastie.org/pastes/"
        self.pastie_url_e = "/text"
        self.pastie_archive = "http://pastie.org/pastes/y/"#2014/4/page/1"


        self.lib = lib


    def run(self):
        print "Starting Pastie Thread"
        while 1:
            self.pastie()
            time.sleep(10)
        print "Exiting Pastebin Thread"







    def pastie(self):
        today = datetime.datetime.today()

        year = today.year
        month = today.month

        url = self.pastie_archive+ str(today.year) + "/" +str(today.month) +"/page/"

        next = True
        page = 0
        while next:
            page +=1
            url_now = url + str(page)
            try:
                html=self.lib.request_url(url_now)
            except:
                print "jar"
                continue

            soup=BeautifulSoup(html)

            divs = soup.findAll('div',{ "class" : "pastePreview" })
            for div in divs:
                a = div.find('a')
                final_url = a['href']
                try:
                    final_html=self.lib.request_url(final_url+"/text")
                except:
                    continue
                final_soup=BeautifulSoup(final_html)
                final_pre = final_soup.find('pre')
                pre = final_pre.text

                try:
                    b = self.lib.search_regex(pre)
                except:
                    continue

                if b:
                    print "La url: " + final_url + " coincide con alguna de las busquedas!"
                    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.lib.write_global_document(final_url)

                    url_spar = final_url.split("/")
                    id = url_spar[len(url_spar)-1]
                    self.lib.create_find_document(id,pre,"pastie")

                    self.lib.send_email(pre,"pastie",final_url)

            if len(divs) == 0:
                # break
                if month == 1:
                    month = 12
                    year -= 1
                else:
                    month -= 1

                url = self.pastie_archive + str(year) + "/" + str(month) +"/page/"
                page = 0
