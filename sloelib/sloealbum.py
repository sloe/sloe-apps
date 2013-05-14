
import logging
from pprint import pprint, pformat
import uuid

from sloeconfig import SloeConfig

class SloeAlbum:
    def __init__(self):
        self.contents = {}
