#!/usr/bin/env python

import optparse
import sys

sys.path.append("..")
import sloelib

from sloeapp import SloeApp

sloeapp = None
if __name__ == "__main__":
  sloeapp = SloeApp()
  sloeapp.enter()
  
