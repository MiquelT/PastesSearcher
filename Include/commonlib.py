from random import randrange
import urllib2
import datetime
import sys
import os
import re
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText



class Commonlib():
    def __init__(self,proxyBool,proxyList,path,regrexList,emailOptions):
        self.proxyBool = proxyBool
        self.proxyList = proxyList
        self.path = path
        self.regrexList = regrexList
        self.emailOptions = emailOptions

    def request_url(self,url):
        if self.proxyBool:
            proxy_num = randrange(len(self.proxyList))
            proxy_path = self.proxyList[proxy_num].split(' ')[0]
            protocol = self.proxyList[proxy_num].split(' ')[1]

            proxy_support = urllib2.ProxyHandler({protocol:protocol+"://"+proxy_path})
            opener = urllib2.build_opener(proxy_support)
            urllib2.install_opener(opener)

        html = urllib2.urlopen(url).read()
        return html


    def write_global_document(self,url):
        self.create_directory()
        date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).strip()
        f = open(self.path+"Globallist.txt", 'a')
        f.write(date + "\t" + url +"\n")
        f.close()

    def create_find_document(self,id,message,origin):
        self.create_directory()
        date = str(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")).strip()
        f = open(self.path +origin + "_" + date + "_" + id +".txt", 'w')
        for line in message.split("\n"):
            try:
                f.write(unicode(line)+"\n")
            except:
                continue
        f.close()


    def create_directory(self):
        if not os.path.isdir(self.path):
            os.makedirs(self.path)


    def search_regex(self,text):
        bool = False
        for regrex in self.regrexList:
            searchB = False
            includeB = True
            excludeB = True
            for key in regrex:
                what = regrex[key]
                if what == "search":
                    reg_s = re.search(key,text)
                    if reg_s: searchB = True
                elif what == "include":
                    reg_s = re.search(key,text)
                    if not reg_s: includeB = False
                elif what == "exclude":
                    reg_s = re.search(key,text)
                    if reg_s: excludeB = False

            if searchB and includeB and excludeB:
                bool = True

        return bool

    def send_email(self,content,lab,url):
        if self.emailOptions["activated"]:
            user = self.emailOptions["user"]
            password = self.emailOptions["password"]

            recipients = self.emailOptions["send"]


            msg = MIMEMultipart('alternative')
            msg['Subject'] = "PasteBinSearcher Alert"
            msg['From'] = user
            msg['To'] = ", ".join(recipients)


            html = """\
                    <html>
                    <head></head>
                    <body style="background:#EEE;">

                        <table style="background:#ACD; width:80%; "align="center">
                            <tr align="center">
                                <td style="background:#9BC;"><h1>PasteBinSearcher Alert!</h1></td>
                            </tr>
                            <tr align="center">
                                <td><h2>Origin: """+ lab +"""</h2></td>
                            </tr>
                            <tr>
                                <td>Url: <a href='""" + url + """'>""" + url + """</a></td>
                            </tr>
                            <tr>
                            </tr>
                            <tr>
                                <td style="background:#EEE; font-family:'Courier'; padding: 10px;">
                                """+ content +"""
                                </td>
                            </tr>
                        </table>
                    </body>
                </html>
                """

            part = MIMEText(html, 'html')

            msg.attach(part)


            server = smtplib.SMTP(self.emailOptions["smtp"])

            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(user, password)

            server.sendmail(user, recipients, msg.as_string())
            server.quit()

            print "Sended"







