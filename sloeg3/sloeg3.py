
import logging
from pprint import pprint, pformat
import types
import uuid

import sloelib

try:
    import libg3
    g_libg3_present = True
except:
    g_libg3_present = False

class SloeG3:
    def __init__(self):
        if not g_libg3_present:
            raise sloelib.SloeError("Please install libg3 python bindings from https://github.com/"
                "gallery/gallery3-contrib/tree/master/<version>/client/Python/pylibgal3")
        self.glb_cfg = sloelib.SloeConfig.get_global()


    def connect(self):
        apikey = self.glb_cfg.get("gallery3", "apikey")
        hostname = self.glb_cfg.get("gallery3", "hostname")
        g3base = self.glb_cfg.get("gallery3", "g3base")
        self.gal = libg3.Gallery3(hostname , apikey , g3Base=g3base)
        if self.gal is None:
            raise sloelib.SloeError("Failed to connect to gallery3")
        try:
            self.g3root = self.gal.getRoot()
        except Exception, e:
            message = "Failed to connect to gallery3 (%s)" % str(e)
            logging.error(message)
            raise sloelib.SloeError(message)


    def get_or_create_album(self, parent_album, album_name):
        for album in parent_album.getAlbums():
            if album.name == album_name:
                logging.info("Found existing album %s" % album_name)
                return album
        logging.info("Creating new album %s" % album_name)
        return parent_album.addAlbum(album_name, album_name, album_name)


    def reconcile_to_g3tree(self, tree_name):
        def recurse_album(treedata, sloe_subtree, g3_album):
            for key in sorted(treedata.keys()):
                value = treedata[key]
                if isinstance(key, uuid.UUID):
                    pass
                    # logging.debug("Found item %s" % str(value))
                if isinstance(key, types.StringType) or isinstance(key, types.UnicodeType) :
                    sub_album = self.get_or_create_album(g3_album, key)
                    recurse_album(value, sloe_subtree + [key], sub_album)

        recurse_album(self.sloe_tree.treedata.get("final", {}), [], self.g3root)


    def update_tree(self, tree_name):
        self.connect()

        self.sloe_tree = sloelib.SloeTrees.inst().get_tree(tree_name)
        self.reconcile_to_g3tree(tree_name)




