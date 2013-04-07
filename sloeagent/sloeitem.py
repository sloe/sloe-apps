
from ConfigParser import ConfigParser
import logging
import os
from pprint import pprint, pformat
import uuid

class SloeItem:
  def __init__(self):
    self.data = {}
    
    
  def create_new(self, spec):
    for element in ("name", "tree", "subtree", "worth", "filepath"):
      self.data[element] = spec[element]
    self.data["uuid"] = uuid.uuid4()
 
 
  def get_key(self):
    return "item-%s" % str(self.data["uuid"])
  
    
  def get_ini_leafname(self):
    return "%s-%s.ini" % (self.data["name"], self.data["uuid"])
  
    
  def get_ini_filepath(self):
    treepath = os.path.dirname(self.data["filepath"])
    return os.path.join(treepath, self.get_ini_leafname());
  
    
  def savetofile(self):
    parser = ConfigParser()
    section = self.get_key()
    parser.add_section(section)
    for name, value in self.data.iteritems():
      parser.set(section, name, '"%s"' % str(value))
    
    logging.info("Path: %s" % self.get_ini_filepath())
    with open(self.get_ini_filepath(), "wb") as file:
      parser.write(file)
      
      
  def dump(self):
    return pformat(self.data)