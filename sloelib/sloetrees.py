
import logging
import os
from pprint import pprint

from sloeconfig import SloeConfig
from sloetree import SloeTree

class SloeTrees:
  instance = None
  
  def __init__(self):
    self.trees = {}
    self.tree_uuids = {}
    
    
  @classmethod
  def inst(cls):
    if cls.instance is None:
      cls.instance = SloeTrees()
    return cls.instance

  
  def get_tree_key(self, tree_name):
    return "tree_" + tree_name
    
    
  def get_tree(self, tree_name):
    tree_uuid = self.tree_uuids.get(tree_name, None) or self.load_tree(tree_name)
    return self.trees[tree_uuid]
    
  
  def create_tree(self, tree_name):
    logging.debug("Loading tree %s" % tree_name)
    
    glb_cfg = SloeConfig.get_global()
    print glb_cfg.dump()
    tree_spec = glb_cfg.get_section(self.get_tree_key(tree_name))
    tree_spec["name"] = tree_name
    new_tree = SloeTree(tree_spec)
    self.trees[tree_spec["uuid"]] = new_tree
    self.tree_uuids[tree_spec["name"]] = tree_spec["uuid"]
    return new_tree
    
    
  def load_tree(self, tree_name):
    created_tree = self.create_tree(tree_name)
    created_tree.make()
    return created_tree.get_tree_uuid()
   
        