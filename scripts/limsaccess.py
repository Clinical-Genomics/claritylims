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

def readconfig():
  configfile = os.getenv('HOME') + '/.scilifelabrc'
  params = {}
  with open(configfile, "r") as confs:
    for line in confs:
      if len(line) > 3 and not line[0] == "#":
        pv = line.rstrip().split(" ")
        arg = pv[0]
        pv.pop(0)
        params[arg] = ' '.join(pv)
  return params

class limsconnect(object):
  
  def __init__(self, User, Passwd, baseuri):
    self.user = User
    self.pwd = Passwd
    self.uri = baseuri
    self.entrypoints = { 'samples': 'limsid', 'artifacts': 'limsid' }

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    if exc_type:
      print '__exit__(%s, %s, %s)' % (exc_type, exc_val, exc_tb)
      
  def getroot(self):

    r = requests.get(self.uri, auth=(self.user, self.pwd))
    tree = ElementTree.fromstring(r.text)
    return tree.iter()

  def getentry(self, searchattribute, searchvalue):
    r = requests.get(self.uri + searchattribute + '/' + searchvalue, auth=(self.user, self.pwd))
    tree = ElementTree.fromstring(r.text)
    return tree.iter()
    
  def gettag(self, searchattribute, searchvalue, tag):
    r = requests.get(self.uri + searchattribute + '/' + searchvalue, auth=(self.user, self.pwd))
    tree = ElementTree.fromstring(r.text)
    hit = "No hit"
    for node in tree:
      if node.tag == tag:
        hit = node.text
    return hit

  def getlist(self, term):
    r = requests.get(self.uri + , auth=(self.user, self.pwd))
    uri = node.attrib.get('uri')
#          limsid = node.attrib.get('limsid')
#          if node.tag == 'sample':
#            counter += 1
#            internal_id = node.attrib['limsid']
#            suburi = node.attrib['uri']
#            rr = requests.get(suburi, auth=(user1, pass1))
#            subtree = ElementTree.fromstring(rr.text.encode('utf-8'))
#            name = subtree.find('name')
#            print counter, internal_id, name.text.encode('utf-8')
#          if node.tag == 'next-page':
#            baseurl = node.attrib.get('uri')
#          if node.tag == 'previous-page':
#            check = False

