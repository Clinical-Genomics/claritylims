#!/usr/bin/python
#Script that connects to the MySQL database and parses data from an html table
#Import the mysql.connector library/module
import sys
import time
import glob
import re
import os
import requests
from xml.etree import ElementTree

configfile = "/home/hiseq.clinical/.scilifelabrc"
if (len(sys.argv)>1):
  if os.path.isfile(sys.argv[1]):
    configfile = sys.argv[1]
    
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

tree = ElementTree.fromstring(r.text)

for node in tree.findall('sample'):
  print node.tag
  uri = node.attrib.get('uri')
  limsid = node.attrib.get('limsid')
  if uri and limsid:
    print '  %s :: %s' % (limsid, uri)
  else:
    print 'None'


for elem in r.text:
  print elem.text
#URL = baseurl+'samples/'
#previous = URL
#smpls = requests.get(URL, auth=(user1, pass1))
#stree = ET.ElementTree(ET.fromstring(smpls.text))
#rsmpl = stree.getroot()
#mybrain = 'empty'
#while mybrain == 'empty':
#  if previous == URL:
#    for sample in rsmpl:
#      if sample.tag == "sample":
#        LIMSID = sample.attrib['limsid']
#        singlev = requests.get(sample.attrib['uri'], auth=(user1, pass1), 
#            headers={'content-type': 'application/xml', 'accept': 'application/xml'})
#        svt = ET.ElementTree(ET.fromstring(singlev.text.encode('utf-8')))
#        elem = svt.getroot()
#        for element in elem:
#          if element.tag == 'name':
#            SAMPLEID = element.text
#            COUNTER += 1
#        print str(COUNTER) + "     LIMSID " + LIMSID + "     SAMPLEID " + SAMPLEID 
#      else:
#        if sample.tag == "next-page":
#          URL = sample.attrib['uri']
#          previous = URL
#          smpls = requests.get(URL, auth=(user1, pass1))
#          stree = ET.ElementTree(ET.fromstring(smpls.text))
#          rsmpl = stree.getroot()
#        if sample.tag == "previous-page":
#          smpls = ""
#          stree = ""
#          rsmpl = []
#          mybrain = 'delirious'
#        print URL
#        print sample.tag

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
