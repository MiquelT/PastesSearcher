#!/usr/bin/python
__author__ = 'MiqueT'
# Pastes Searcher es un script para controlar los historiales de diversas fuentes de comparticion de texto o codigo, permitiendo la deteccion de strings o patrones en estos. Por Miquel Tur (miquel.tur.m@gmail.com)

# Esta obra esta sujeta a la licencia Reconocimiento-NoComercial 4.0 Internacional de Creative Commons

# Usage example: python main.py


from Include import ProxyListCreator
from Include.commonlib import Commonlib
from Include.pastebin import Pastebin
from Include.pastie import Pastie
from Include.linkpaste import Linkpaste
from Include.githubgist import Githubgist
from Include.ideone import Ideone
from Include.codepad import Codepad
from Include.snipt import Snipt
from Include.slexy import Slexy
from Include.dropbucket import Dropbucket
from Include.pasteru import Pasteru
from Include.pastelisp import Pastelisp
from Include.dzone import Dzone
from Include.lpaste import Lpaste
from Include.copytaste import Copytaste

import os
import sys
import xml.etree.ElementTree as ET
import time
import signal
import threading

path = "Data/"

emailOptions = {}

regrexPath = "Config/regrex.conf"
proxyPath = "Config/proxyList.conf"

activated = {}

proxyBool = False
CreateProxyList = False
regrexList = []


proxyList = []

def presentation():

    print "\n###############################################"
    print "############  PastesSearcher  #################"
    print "###############################################\n\n"



def usage():
    print "Usage:\n"
    print "$ python main.py [-c CONFIGFILE]\n\n"
    sys.exit(0)


def init_args():

    global path
    global proxyBool
    global CreateProxyList
    global proxyListUpdateTime

    global regrexPath
    global proxyPath

    global activated

    global emailOptions

    configpath = 'Config/config.xml'

    if len(sys.argv) > 2 and sys.argv[1] == '-c':
        configpathT = sys.argv[2]
        if os.path.isfile(configpathT):
            configpath = configpathT
    elif len(sys.argv) == 2 and  sys.argv[1] == '-h':
        usage()
    elif len(sys.argv) > 1:
        usage()



    tree = ET.parse(configpath)
    root = tree.getroot()

    regrexPath = root.find('regexFile').text
    proxyPath = root.find('proxysFile').text
    path = root.find('resultsPath').text

    proxyBool = int(root.find('proxy').text)
    CreateProxyList = int(root.find('CreateProxyList').text)
    proxyListUpdateTime = int(root.find('proxyListUpdateTime').text)

    if proxyListUpdateTime < 900: proxyListUpdateTime = 900

    emailB = int(root.find('email').attrib['active'])

    emailUser = root.find('email').find('user').text
    emailPassword = root.find('email').find('password').text
    smtp = root.find('email').find('smtp').text

    emailsX = root.find('email').findall('send')
    emails = []
    for e in emailsX:
        emails.append(e.text)

    emailOptions["user"] = emailUser
    emailOptions["password"] = emailPassword
    emailOptions["smtp"] = smtp
    emailOptions["send"] = emails
    emailOptions["activated"] = emailB

    sites = root.find('sites').findall('site')
    for site in sites:
        activated[site.attrib['name']] = int(site.text)


def init_config():

    global regrexList
    global proxyBool
    global proxyList

    tree = ET.parse(regrexPath)
    root = tree.getroot()
    regex = root.findall('regex')

    for r in regex:
        map = {}
        for atr in r:
            map[atr.text] = atr.tag
        regrexList.append(map)

    if proxyBool:
        f = open(proxyPath, 'r')
        for l in f:
            if l != "": proxyList.append(l)
        f.close()


def update_proxy_list():
    plc = ProxyListCreator.ProxyListCreator(proxyPath)
    plc.create_list()
    f = open(proxyPath, 'r')
    proxyList = []
    for l in f:
        if l != "": proxyList.append(l)
    f.close()


def start():
    global lock
    global emailLock
    lock = threading.Lock()
    emailLock = threading.Lock()
    lib = Commonlib(proxyBool,proxyList,path,regrexList,emailOptions,lock, emailLock)

    if activated["pastie"]:
        try:
            pastieT = Pastie(lib)
            pastieT.start()
        except:
            pass

    if activated["gist.github"]:
        try:
            githubgistT = Githubgist(lib)
            githubgistT.start()
        except:
            pass

    if activated["pastebin"]:
        try:
            pastebinT = Pastebin(lib)
            pastebinT.start()
        except:
            pass

    if activated["linkpaste"]:
        try:
            linkpasteT = Linkpaste(lib)
            linkpasteT.start()
        except:
            pass


    if activated["ideone"]:
        try:
            ideoneT = Ideone(lib)
            ideoneT.start()
        except:
            pass

    if activated["codepad"]:
        try:
            codepadT = Codepad(lib)
            codepadT.start()
        except:
            pass

    if activated["snipt"]:
        try:
            sniptT = Snipt(lib)
            sniptT.start()
        except:
            pass

    if activated["slexy"]:
        try:
            slexyT = Slexy(lib)
            slexyT.start()
        except:
            pass

    if activated["dropbucket"]:
        try:
            dropbucketT = Dropbucket(lib)
            dropbucketT.start()
        except:
            pass

    if activated["paste.ru"]:
        try:
            pasteruT = Pasteru(lib)
            pasteruT.start()
        except:
            pass

    if activated["paste.lisp"]:
        try:
            pastelispT = Pastelisp(lib)
            pastelispT.start()
        except:
            pass

    if activated["dzone"]:
        try:
            dzoneT = Dzone(lib)
            dzoneT.start()
        except:
            pass

    if activated["lpaste"]:
        try:
            lpasteT = Lpaste(lib)
            lpasteT.start()
        except:
            pass

    if activated["copytaste"]:
        try:
            copytasteT = Copytaste(lib)
            copytasteT.start()
        except:
            pass


    while 1:
        time.sleep(proxyListUpdateTime)
        if CreateProxyList:
            lock.acquire()
            print "\nUPDATING PROXY LIST\n"
            update_proxy_list()
            lock.release()


def signal_handler(signal, frame):
    print "\nYou pressed Ctrl+C"
    os._exit(0)


if __name__ == "__main__":
    presentation()
    init_args()

    if CreateProxyList:
        print "Creating the new ProxyList..."
        plc = ProxyListCreator.ProxyListCreator(proxyPath)
        plc.create_list()
        print "ProxyList Created!\n"


    init_config()

    # config Signal for exit
    signal.signal(signal.SIGINT, signal_handler)

    start()

    print "\nDone!\n"

