
import logging
import optparse
import os

import sloelib

from sloegeneratecfg import SloeGenerateCfg
from sloeverifytree import SloeVerifyTree

class SloeApp:
  def get_treename(self, tree):
    return "tree_" + tree

  def get_primary_treepaths(self, tree):
    glb_cfg = sloelib.SloeConfig.get_global()
    root_dir = glb_cfg.get(self.get_treename(tree), "root_dir")
    name = glb_cfg.get(self.get_treename(tree), "name")
    retval = {}
    for worth in ("precious", "derived"):
      retval[worth] = os.path.join(root_dir, "primary", worth, name)
    return retval
      

  def get_global(self, name):
    glb_cfg = sloelib.SloeConfig.get_global()
    return glb_cfg.get("global", name)


  def enter(self):
    glb_cfg = sloelib.SloeConfig.get_global()
  
    parser = optparse.OptionParser("usage: %prog [options] command")
    (self.options, self.args) = parser.parse_args()
    self.params = self.args[1:]
    logging.basicConfig()
    glb_cfg = sloelib.SloeConfig.get_global()
    logging.info("Loading global config file config.cfg")
    glb_cfg.appendfile('config.cfg')
    loglevelstr = glb_cfg.get("global", "loglevel")
    if loglevelstr == 'DEBUG':
      self.loglevel = logging.DEBUG
    elif loglevelstr == 'INFO':
      self.loglevel = logging.INFO
    elif loglevelstr == 'WARNING':
      self.loglevel = logging.WARNING
    elif loglevelstr == 'ERROR':
      self.loglevel = logging.ERROR
    else:
      raise sloelib.SloeError("Invalid loglevel in config")
    logging.getLogger().setLevel(self.loglevel)
    
    logging.debug(glb_cfg.dump())
    
    if len(self.args) == 0:
      parser.error("Please supply a command argument")
    else:
      valid_commands = ("generate_cfg", "verify_tree")
      command = self.args[0]
      if command not in valid_commands:
        parser.error("Command not valid - must be one of %s" % ", ".join(valid_commands))
      
      logging.info("Command: %s" % " ".join(self.args))      
      getattr(self, command)()
      
      
  def generate_cfg(self):
    handler = SloeGenerateCfg(self)
    handler.enter(self.params)
    
  def verify_tree(self):
    handler = SloeVerifyTree(self)
    handler.enter(self.params)
    
    