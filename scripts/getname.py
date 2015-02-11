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
  
  hit = lmc.gettag('samples', 'SIB802A28', 'name')
  print hit
