#!/usr/bin/python
__author__ = 'MiqueT'
# RegexIncluder.py es un script para agregar regex o strings al XML de busquedas. Por Miquel Tur (miquel.tur.m@gmail.com)

# Esta obra esta sujeta a la licencia Reconocimiento-NoComercial 4.0 Internacional de Creative Commons

import sys
import os
import xml.etree.ElementTree as ET

fname = None
do = None


def usage():
    print "python RegexInclude.py (-a|-n) FILE"
    print "-a --append \tappend to regex file."
    print "-n --new \tnew regex file."
    print "\nFILE \tFile path with new regex strings."


def init_args():
    if len(sys.argv) != 3:
        print "\nAdd file path\n"
        sys.exit()
    else:
        global do
        global fname
        do = sys.argv[1]
        fname = sys.argv[2]

def create_xml():
    xml = ET.Element("config")
    return xml


def indent(elem, level=1):
      i = "\n" + level*"  "
      if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
      else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


if __name__ == "__main__":
    init_args()

    list = []

    with open(fname) as f:
        content = f.readlines()
        for line in content:
            if line.strip() != "":
                list.append(line.strip())

    tree = ET.parse('Config/config.xml')
    root = tree.getroot()

    regrexPath = root.find('regexFile').text

    if not os.path.exists(regrexPath) or do == '-n' or do == '--new':
        f = open(regrexPath, "w")
        f.write("<?xml version='1.0'?>\n<config>\n</config>")
        f.close()


    tree2 = ET.parse(regrexPath)
    xml = tree2.getroot()

    if do == '-n' or do == '--new':
        print "new regex file"
        for child in xml:
            xml.remove(child)

    elif do == '-a' or do == '--append':
        print "append to regex file"
    else:
        usage()

    for word in list:
        regexString = ET.SubElement(xml,"regex" )
        searchString = ET.SubElement(regexString,"search")
        searchString.text = word

    indent(xml)
    tree3 = ET.ElementTree(xml)
    tree3.write(regrexPath, xml_declaration=True, encoding='utf-8', method="xml")
