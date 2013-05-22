#!/usr/bin/env python

import optparse
import os
import sys

sys.path.append(os.path.abspath(".."))
try:
    import sloelib
except Exception, e:
    raise Exception("Failed to find sloelib in %s: %s" % (sys.path,str(e)))

from sloeapp import SloeApp

if __name__ == "__main__":
    SloeApp().enter()

