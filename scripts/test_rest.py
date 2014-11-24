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

print 'hello'

baseurl  = 'https://clinical-lims-stage.scilifelab.se:8443/api/v2/'
user1 = "apiuser"
pass1 = "rushverbpureking"

r = requests.get(baseurl, auth=(user1, pass1))
print r.status_code
print r.headers['content-type']
print r.encoding
print r.text

doc = ET.ElementTree(r.text)
print doc.root

exit
