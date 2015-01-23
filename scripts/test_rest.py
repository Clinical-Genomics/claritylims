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

configfile = os.getenv('HOME') + '/.scilifelabrc'

if (len(sys.argv)>1):
  if os.path.isfile(sys.argv[1]):
    configfile = sys.argv[1]
    
params = {}
with open(configfile, "r") as confs:
  for line in confs:
    if len(line) > 5 and not line[0] == "#":
      line = line.rstrip()
      pv = line.split(" ")
#      if len(pv) > 1:
#        arg = pv[0]
#        pv.pop(0)
      params[pv[0]] = ' '.join(pv.pop(0))
#      else:
#        params[pv[0]] = pv[1]
#with open(configfile, "r") as confs:
#  for line in confs:
#    if len(line) > 5 and not line[0] == "#":
#      line = line.rstrip()
#      pv = line.split(" ")
#      params[pv[0]] = pv[1]

baseurl  = params['limsuri'] + 'api/v2/samples/'
user1 = params['apiuser']
pass1 = params['apipass']

r = requests.get(baseurl, auth=(user1, pass1))
tree = ElementTree.fromstring(r.text)

counter = 0
for node in tree.iter():
  uri = node.attrib.get('uri')
  limsid = node.attrib.get('limsid')
  if node.tag == 'sample':
    counter += 1
    internal_id = node.attrib['limsid']
    suburi = node.attrib['uri']
    rr = requests.get(suburi, auth=(user1, pass1))
    subtree = ElementTree.fromstring(rr.text.encode('utf-8'))
    name = subtree.find('name')
    print counter, internal_id, name.text.encode('utf-8')

exit
