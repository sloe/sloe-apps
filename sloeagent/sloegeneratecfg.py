
import json
import logging
import os
from pprint import pprint
import re
import subprocess

from sloeitem import SloeItem

class SloeGenerateCfg:
  def __init__(self, app):
    self.app = app

  def enter(self, trees):
    for tree in trees:
      self.process_tree(tree)
      
  def process_tree(self, tree):
    for worth, walkroot in self.app.get_primary_treepaths(tree).iteritems():
      logging.debug("generate_cfg walking tree directory %s" % walkroot)

      for root, dirs, files in os.walk(walkroot):
        for file in files:
          print file
          match = re.match(r"^(.*)\.(flv|mp4|f4v)$", file)
          if match:
            spec = {
              "name" : match.group(1),
              "tree" : tree,
              "subtree" : os.path.relpath(root, walkroot),
              "worth" : worth,
              "filepath" : os.path.join(root, file),
              "primacy" : "primary"
            }
            self.process_file(spec)
  
  def process_file(self, spec):
    logging.debug("Processing file with spec %s" % repr(spec))
      
    item = SloeItem()
    item.create_new(spec)
    self.detect_video_params(item)
    logging.debug(item.dump())
    item.savetofile()
    
  def detect_video_params(self, item):
    command = [
      self.app.get_global("ffprobe"),
      item.data["filepath"],
      "-print_format", "json", "-show_format", "-show_streams"]
      
    p = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    (json_out, stderr) = p.communicate()
    ffinfo = json.loads(json_out)
    for stream in ffinfo["streams"]:
      if stream["codec_type"] == "video":
        for name in ("codec_name", "width", "height", "pix_fmt", "level", "avg_frame_rate", "duration", "nb_frames"):
          if name in stream:
            item.data["video_" + name] = stream[name]
      elif stream["codec_type"] == "audio":
        for name in ("codec_name", "sample_fmt", "sample_rate", "channels", "duration", "nb_frames"):
          if name in stream:
            item.data["audio_" + name] = stream[name]
      else:
        logging.error("Unknown stream %s" % stream["codec_type"])
    for name in ("format_name", "format_long_name", "size", "bit_rate"):
      if name in ffinfo["format"]:
        item.data["video_" + name] = ffinfo["format"][name]
