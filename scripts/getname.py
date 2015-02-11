#!/usr/bin/python
#Script that connects to the MySQL database and parses data from an html table
#Import the mysql.connector library/module
import sys
import time
import glob
import re
import os
from limsaccess import *

limsid = sys.argv[1]

if (len(sys.argv)>2):
  configfile = sys.argv[2]
else:
  configfile = 'None'
pars = readconfig(configfile)

with limsconnect(pars['apiuser'], pars['apipass'], pars['baseuri']) as lmc:
  
  if os.path.isfile(limsid):
    with open(limsid) as f:
    lines = f.readlines()
    for line in lines:
      hit = lmc.gettag('samples', line, 'name')
      print line, hit
  else:
    lmc.gettag('samples', limsid, 'name')
    print hit
