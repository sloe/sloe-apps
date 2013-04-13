
import logging
import os
from pprint import pprint

import sloelib

class SloeDumpTree:
  def __init__(self, app):
    self.app = app

  def enter(self, trees):
    for tree_name in trees:
      self.process_tree(tree_name)

  def process_tree(self, tree_name):
    logging.debug("Processing tree %s" % tree_name)
    tree = sloelib.SloeTrees.inst().get_tree(tree_name)
    pprint(tree)

