#!/usr/bin/env python

import optparse
import os
import sys

sys.path.append(os.path.abspath(".."))
import sloelib

from sloeapp import SloeApp

if __name__ == "__main__":
  SloeApp().enter()

