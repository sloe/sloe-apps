
import logging
import optparse

import sloelib

class SloeApp:

  def enter(self):
  
    parser = optparse.OptionParser("usage: %prog [options] command")
    (self.options, self.args) = parser.parse_args()
    self.params = self.args[1:]
    logging.basicConfig()
    self.config = sloelib.SloeConfig()
    logging.info("Loading config file config.cfg")
    self.config.appendfile('config.cfg')
    loglevelstr = self.config.get("global", "loglevel")
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
    
    if self.loglevel <= logging.DEBUG:
      logging.info(self.config.dump())
    
    if len(self.args) == 0:
      parser.error("Please supply a command argument")
    else:
      valid_commands = ["generate_cfg"]
      command = self.args[0]
      if command not in valid_commands:
        parser.error("Command not valid - must be one of %s" % ", ".join(valid_commands))
      
      logging.info("Command: %s" % " ".join(self.args))      
      getattr(self, command)()
      
      
  def generate_cfg(self):
    pass 