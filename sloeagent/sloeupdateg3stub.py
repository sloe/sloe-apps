
import logging

class SloeUpdateG3:
    def __init__(self, app):
        pass

    def enter(self, trees):
        raise sloelib.SloeError("Gallery3 support unavailable.  Please install libg3 python bindings from "
            "https://github.com/gallery/gallery3-contrib/tree/master/<version>/client/Python/pylibgal3")
