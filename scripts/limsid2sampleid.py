#!/usr/bin/python
#Script that connects to the MySQL database and parses data from an html table
#Import the mysql.connector library/module
import sys
import time
import glob
import re
import os
from limsaccess import *

if (len(sys.argv)>1):
  configfile = sys.argv[1]
else:
  configfile = 'None'
pars = readconfig(configfile)

with limsconnect(pars['apiuser'], pars['apipass'], pars['baseuri']) as lmc:
  
  entries = lmc.getroot()
  for node in entries:
    print node.tag
    for key in node.attrib:
      print key, node.attrib[key]
      
  hit = getentry('samples', 'SIB802A28')
  for node in hit:
    print node.tag
    for key in node.attrib:
      print key, node.attrib[key]
  
#  for entry in entries:
#    print entry 
