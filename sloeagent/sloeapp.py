
import logging
import optparse
import os
import sys
import sloelib

from sloedumptree import SloeDumpTree
from sloegeneratecfg import SloeGenerateCfg
from sloeverifytree import SloeVerifyTree

g_startup_log = []

try:
    import libg3
    from sloeupdateg3 import SloeUpdateG3
except ImportError, e:
    g_startup_log.append("libg3 import failed - disabling Gallery support (%s)" % str(e))


class SloeApp:

  def get_global(self, name):
    glb_cfg = sloelib.SloeConfig.get_global()
    return glb_cfg.get("global", name)


  def enter(self):
    glb_cfg = sloelib.SloeConfig.get_global()

    parser = optparse.OptionParser("usage: %prog [options] command")
    parser.add_option("-z", "--dryrun",
                  action="store_true", dest="dryrun", default=False,
                  help="perform functions but do not write files")
    parser.add_option("--final",
                  action="store_true", dest="final", default=False,
                  help="generate_cfg for final directory")
    (self.options, self.args) = parser.parse_args()
    self.params = self.args[1:]
    logging.basicConfig(format="#%(levelname)s:%(filename)s::%(funcName)s#%(lineno)d at %(asctime)s\n%(message)s")
    glb_cfg = sloelib.SloeConfig.get_global()
    g_startup_log.append("Loading global config file config.cfg")
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
    logging.debug("\n".join(g_startup_log))
    glb_cfg.set_options(self.options)

    if len(self.args) == 0:
      parser.error("Please supply a command argument")
    else:
      valid_commands = ("dump_tree", "generate_cfg", "update_g3", "verify_tree")
      command = self.args[0]
      if command not in valid_commands:
        parser.error("Command not valid - must be one of %s" % ", ".join(valid_commands))

      logging.info("Command: %s" % " ".join(self.args))
      getattr(self, command)()


  def dump_tree(self):
    handler = SloeDumpTree(self)
    handler.enter(self.params)


  def generate_cfg(self):
    handler = SloeGenerateCfg(self)
    handler.enter(self.params)


  def update_g3(self):
    handler = SloeUpdateG3(self)
    handler.enter(self.params)


  def verify_tree(self):
    handler = SloeVerifyTree(self)
    handler.enter(self.params)


