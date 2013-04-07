
import os
from pprint import pprint, pformat

import ConfigParser
from sloeerror import SloeError

class SloeConfig:
  def __init__(self):
    self.reset()
    
  def reset(self):
    scriptroot = os.path.dirname(os.path.abspath(__file__))
    wsroot = os.path.dirname(os.path.dirname(scriptroot))
    defaults  = {
      '_scriptroot' : scriptroot,
      '_wsroot' : wsroot,
      '_wstopdir' : os.path.dirname(wsroot)
    }
    self.parser = ConfigParser.SafeConfigParser(defaults)
    self.data_valid = False
    
  def appendfile(self, filename):
    files = self.parser.read(filename)
    if not files:
      raise SloeError("Could not read config file %s" % filename)
    self.data_valid = False
    
  def remake_data(self):
    if not self.data_valid:
      self.data = {}
      for section in self.parser.sections():
        self.data[section] = {}
        for name, value in self.parser.items(section):
          if not name.startswith("_"):
            self.data[section][name] = value
      self.data_valid = True
  
  def get(self, section, name):
    if not self.data_valid:
      self.remake_data()
    return self.data[section][name]
  
  def dump(self):
    message = ""
    for section in ["DEFAULT"] + self.parser.sections():
      message += "[%s]\n" % section
      for name, value in self.parser.items(section):
        if not name.startswith("_"):
          message += "%s=%s\n" % (name, value)
    print "***"
    self.remake_data()
    message += pformat(self.data)
    return message
    