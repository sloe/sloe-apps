
import logging
import os
from pprint import pprint

import sloelib
import sloeg3

class SloeUpdateG3:
  def __init__(self, app):
    self.app = app
    self.g3 = sloeg3.SloeG3()

  def enter(self, trees):
    for tree_name in trees:
      self.g3.update_tree(tree_name)

