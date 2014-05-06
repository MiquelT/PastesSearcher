import threading
import urllib2
import commonlib
import datetime
from BeautifulSoup import BeautifulSoup
import time




class Githubgist(threading.Thread):

    def __init__(self,lib):
        threading.Thread.__init__(self)
        self.githubgist_url = "https://gist.github.com/discover?page="
        self.basic_url = "https://gist.github.com"
        self.lib = lib
        self.found = []


    def run(self):
        print "Starting Githubgist Thread"
        while 1:
            try:
                self.githubgist()
            except:
                print "**Error in githubgist"
                time.sleep(60)
                pass
            time.sleep(10)
        print "Exiting Githubgist Thread"







    def githubgist(self):
        for i in range(100):
            can = True
            while can:
                try:
                    html=self.lib.request_url(self.githubgist_url + str(i))
                    # html = urllib2.urlopen("http://pastebin.com/archive").read()
                    can = False
                except:
                    pass

            soup=BeautifulSoup(html)

            aHref = soup.findAll('a',{ "class" : "link-overlay" })

            for a in aHref:
                try:
                    if not "archive/" in a['href']:
                        final_url = self.basic_url + a['href']
                        id = a['href'].replace('/','_')
                        try:
                            html=self.lib.request_url(final_url)
                        except:
                            continue

                        soup=BeautifulSoup(html)
                        div = soup.find('div',{ "class" : "column files" }).text

                        try:
                            b = self.lib.search_regex(div)
                        except:
                            continue

                        if b and not id in self.found:
                            self.found.append(id)
                            print "La url: " + final_url + " coincide con alguna de las busquedas!"
                            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            self.lib.write_global_document(final_url)
                            self.lib.create_find_document(id,div,"Githubgist")
                            self.lib.send_email(div,"Githubgist",final_url)
                except:
                    continue
