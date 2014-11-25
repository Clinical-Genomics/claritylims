#!/usr/bin/python
#Script that connects to the MySQL database and parses data from an html table
#Import the mysql.connector library/module
import sys
import time
import glob
import re
import os
import requests
import elementtree.ElementTree as ET
import cElementTree as ET

configfile = "/home/hiseq.clinical/.scilifelabrc"
if (len(sys.argv)>2):
  if os.path.isfile(sys.argv[2]):
    configfile = sys.argv[2]

if (len(sys.argv)<2):
    print "usage: $0 <LIMSID> <config-file:optional>
    
params = {}
with open(configfile, "r") as confs:
  for line in confs:
    if len(line) > 5 and not line[0] == "#":
      line = line.rstrip()
      pv = line.split(" ")
      params[pv[0]] = pv[1]


baseurl  = 'https://clinical-lims-stage.scilifelab.se:8443/api/v2/'
user1 = params['apiuser']
pass1 = params['apipass']

r = requests.get(baseurl, auth=(user1, pass1))
#print r.status_code
#print r.headers['content-type']
#print r.encoding
#print r.text

tree = ET.ElementTree(ET.fromstring(r.text))
root = tree.getroot()

#for child in root:
#  print child.tag, child.attrib
  
# get samples

LIMSID = ''
SAMPLEID = ''
COUNTER = 0

URL = baseurl+'samples/'
previous = URL
smpls = requests.get(URL, auth=(user1, pass1))
stree = ET.ElementTree(ET.fromstring(smpls.text))
rsmpl = stree.getroot()
mybrain = 'empty'
while mybrain == 'empty':
  if previous == URL:
    for sample in rsmpl:
      if sample.tag == "sample":
        LIMSID = sample.attrib['limsid']
        singlev = requests.get(sample.attrib['uri'], auth=(user1, pass1), 
            headers={'content-type': 'application/xml', 'accept': 'application/xml'})
        svt = ET.ElementTree(ET.fromstring(singlev.text.encode('utf-8')))
        elem = svt.getroot()
        for element in elem:
          if element.tag == 'name':
            SAMPLEID = element.text
            COUNTER += 1
        print str(COUNTER) + "     LIMSID " + LIMSID + "     SAMPLEID " + SAMPLEID 
      else:
        if sample.tag == "next-page":
          URL = sample.attrib['uri']
          previous = URL
          smpls = requests.get(URL, auth=(user1, pass1))
          stree = ET.ElementTree(ET.fromstring(smpls.text))
          rsmpl = stree.getroot()
        if sample.tag == "previous-page":
          smpls = ""
          stree = ""
          rsmpl = []
          mybrain = 'delirious'
        print URL
        print sample.tag


#for sample in rsmpl:
#  print sample.tag, sample.attrib, sample.keys()
#  print sample.tag
#  print '  in limsid:', sample.attrib['limsid']
#  LIMSID = sample.attrib['limsid']
#  print '  in uri   :', sample.attrib['uri']
#  singlev = requests.get(sample.attrib['uri'], auth=(user1, pass1), 
#            headers={'content-type': 'application/xml', 'accept': 'application/xml'})
#  svt = ET.ElementTree(ET.fromstring(singlev.text))
#  print singlev.text
#  svt = ET.ElementTree(ET.fromstring(singlev.text.encode('utf-8')))
#  elem = svt.getroot()
#  print elem.attrib.get("name")

#  for element in elem:
#      if element.tag == 'name':
#        SAMPLEID = element.text

#        print element.tag, element.text
#  print ET.iselement(elem), ET.iselement(stree), ET.iselement(rsmpl)
#  name = ET.SubElement(elem, "name")
#  print name.text
#  print "LIMSID " + LIMSID + "     SAMPLEID " + SAMPLEID
  
exit
