
import ConfigParser
import logging
import os
import re
from pprint import pformat, pprint
import uuid

from sloeconfig import SloeConfig
from sloeerror import SloeError

class SloeTree:
  item_ini_regex = re.compile(r"(.*)-([0-9A-Fa-f-]{36})\.ini$")
  ini_regex = re.compile(r".*\.ini$")
  
  def __init__(self, spec):
    self.spec = spec
    self.loaded = False
    self.treedata = {}


  def get_tree_uuid(self):
    return self.spec["uuid"]


  def find_in_tree(self, test_fn):
    def recurse(candidate, found):
      for key, value in candidate.iteritems():
        if isinstance(key, uuid.UUID):
          if test_fn(value):
            return value
        else:
          found = recurse(value, found)
          if found:
            break
      return found
    return recurse(self.treedata, None)


  def get_item_from_name_subtree(self, name, subtree):
    def test(item_dict):
      # print "Testins %s = %s and %s = %s" % (item_dict["name"], name, item_dict["subtree"], subtree)
      return (item_dict["name"] == name and item_dict["subtree"] == subtree)
    return self.find_in_tree(test)
    
      
  def make(self):
    if not self.loaded:
      self.load()


  def load(self):
    logging.debug("Loading tree %s" % self.spec["name"])
    glb_cfg = SloeConfig.get_global()
    for stage in  glb_cfg.get("global", "stages").split(","):
      for worth in glb_cfg.get("global", "worths").split(","):
        subdir_path = os.path.join(self.spec["root_dir"], stage, worth, self.spec["name"])
        logging.debug("Walking path %s" % subdir_path)
        filecount = 0
        bytecount = 0
        for root, dirs, filenames in os.walk(subdir_path):
          for filename in filenames:
            match = self.item_ini_regex.match(filename)
            if match:
              name = match.group(1)
              filename_uuid = match.group(2)
              bytecount += self.add_from_ini(subdir_path, os.path.relpath(root, subdir_path), filename, name, filename_uuid)
              filecount += 1
            elif self.ini_regex.match(filename):
              logging.warning("Suspicious misnamed(?) .ini file %s" % os.path.join(root, filename))
        logging.info("Loaded %d item (%d MB) records from %s" % (filecount, bytecount / 2**20, subdir_path))       

  
  def add_from_ini(self, root, subtree, filename, name, filename_uuid):
    full_path = os.path.join(root, subtree, filename)
    parser = ConfigParser.RawConfigParser()
    parser.read(full_path)
    file_data = {}
    for section in parser.sections():
      file_data[section] = {}
      for item_name, value in parser.items(section):
        if value.startswith('"') and value.endswith('"'):
          value = value[1:-1]
        file_data[section][item_name] = value
    
    if len(file_data.keys()) != 1:
      raise SloeError("Only one section supported in .ini: %s" % full_path)
    
    for section, data in file_data.iteritems():
      # Verification
      if subtree != data["subtree"]:
        raise SloeError("subtree mismatch %s != %s in %s" %
          (subtree, data["subtree"], full_path))
      
      if section != "item-%s" % data["uuid"]:
        raise SloeError("in-file section/uuid mismatch %s != %s in %s" %
          (section, "item-%s" % data["uuid"], full_path))
        
      if data["uuid"] != filename_uuid: # Both are strings
        raise SloeError("filename/content uuid mismatch %s != %s in %s" %
          (data["uuid"], filename_uuid, full_path))

      filesize = 0
      filestat = os.stat(data["filepath"])
      if os.path.stat.S_ISREG(filestat.st_mode):
        filesize = filestat.st_size
      else:
        logging.warning("Missing file %s" % data["filepath"])

      target_dict = self.treedata
      for dir in data["subtree"].split("/"):
        if dir not in target_dict:
          target_dict[dir] = {}
        target_dict = target_dict[dir]
   
      id_uuid = uuid.UUID(data["uuid"])
      target_dict[id_uuid] = data

      return filesize
   
  def __repr__(self):
    return ("SloeTree.spec=" + pformat(self.spec) +
      "\nSloeTree.loaded=" + pformat(self.loaded) +
      "\nSloeTree.treedata=" + pformat(self.treedata))
      