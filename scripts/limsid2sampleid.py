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

if (len(sys.argv) == 1):
  print "\n\tusage: $0 <LIMSID> <config-file:optional>\n"
  exit(0)
else:
  search = sys.argv[1]
    
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
        if sample.attrib['limsid'] == search:
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
          mybrain = 'intoxicated'
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

exit
