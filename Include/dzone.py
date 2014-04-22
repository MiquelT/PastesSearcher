import threading
import urllib2
import commonlib
import datetime
from BeautifulSoup import BeautifulSoup
import time




class Dzone(threading.Thread):

    def __init__(self,lib):
        threading.Thread.__init__(self)
        self.basic_url = "http://www.dzone.com"
        self.lib = lib


    def run(self):
        print "Starting Dzone Thread"
        while 1:
            self.dzone()
            time.sleep(10)
        print "Exiting Dzone Thread"




    def dzone(self):

        can = True
        while can:
            try:
                html=self.lib.request_url(self.basic_url+"/snippets")
                # html = urllib2.urlopen("http://pastebin.com/archive").read()
                can = False
            except:
                pass

        soup=BeautifulSoup(html)

        principalDiv = soup.find('div',{ "id" : "recent_snippets" })



        h3s = principalDiv.findAll('h3')



        for h3 in h3s:

            a = h3.find('a')

            final_url = self.basic_url+a['href']

            id = final_url.split('/')[2]

            try:
                html=self.lib.request_url(final_url)
            except:
                continue

            soup=BeautifulSoup(html)

            div = soup.find('div',{ "id" : "articleText" }).find('pre').text

            try:
                b = self.lib.search_regex(div)
            except:
                continue

            if b:
                print "La url: " + final_url + " coincide con alguna de las busquedas!"
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.lib.write_global_document(final_url)
                self.lib.create_find_document(id,div,"Dzone")
                self.lib.send_email(div,"Dzone",final_url)

