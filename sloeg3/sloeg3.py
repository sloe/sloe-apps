
import logging
from pprint import pprint, pformat
import types
import uuid

import libg3
import sloelib

class SloeEmptyLocalMovie(libg3.LocalMovie):
    def __init__(self, *args, **kwargs):
        libg3.LocalMovie.__init__(self, *args, **kwargs)
        self.contentType = "application/octet-stream"

    def getFileContents(self):
        logging.info("Returning empty file contents")
        return ""


class SloeGallery3(libg3.Gallery3):
    def __init__(self, *args, **kwargs):
        libg3.Gallery3.__init__(self, *args, **kwargs)

    def updateItem(self , item):
        """
        Updates a remote item's title and description

        item(BaseRemote)        : An item descended from BaseRemote

        returns(tuple(status , msg))    : Returns a tuple of a boolean status
                                          and a message if there is an error
        """
        if not item.can_edit:
            raise G3AuthError('You do not have permission to edit: %s' %
                item.title)
        try:
            self._isItemValid(item, libg3.G3Items.BaseRemote)
        except Exception , e:
            return (False , str(e))
        data = {
            'title': item.title,
            'description': item.description,
            'sloe_uuid': item.sloe_uuid,
        }
        req = libg3.Requests.PutRequest(item.url , self.apiKey , data)
        try:
            resp = self._openReq(req)
        except libg3.Errors.G3RequestError , e:
            return (False , str(e))
        return (True , '')


class SloeG3:
    def __init__(self):
        self.glb_cfg = sloelib.SloeConfig.get_global()


    def connect(self):
        apikey = self.glb_cfg.get("gallery3", "apikey")
        hostname = self.glb_cfg.get("gallery3", "hostname")
        g3base = self.glb_cfg.get("gallery3", "g3base")
        self.gal = SloeGallery3(hostname , apikey , g3Base=g3base)
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


    def sync_movie(self, movie, item):
        fields = []
        for dest, value in {
            "title": item.name
            }.iteritems():
            if getattr(movie, dest) != value:
                setattr(movie, dest, value)
                fields.append(dest)

        return fields


    def get_or_create_item(self, album, keys, item):
        movies = album.getMovies()
        remote_movie = None
        for movie in movies:
            if movie.sloe_uuid == item.uuid:
                remote_movie = movie
                break

        if remote_movie is None:
            logging.debug("Movie %s does not exist - creating" % item.leafname)
            g3item = SloeEmptyLocalMovie(item.get_filepath(), False)
            remote_movie = self.gal.addMovie(album, g3item, title="title", description="description", name=item.leafname)
            remote_movie.sloe_uuid = item.uuid

        fields = self.sync_movie(remote_movie, item)

        if len(fields) > 0:
            status, message = self.gal.updateMovie(remote_movie)

            if status:
                logging.info("Updated %s in item %s" % (", ".join(fields), item.name))
            else:
                logging.error("Failed to update g3 movie: %s" % message)


    def reconcile_to_g3tree(self, tree_name):
        def recurse_album(album, sloe_subtree, g3_album):
            for item in album.get_items():
                self.get_or_create_item(g3_album, sloe_subtree, item)

            for album in album.get_albums():
                sub_album = self.get_or_create_album(g3_album, album.name)
                recurse_album(album, sloe_subtree + [album.name], sub_album)

        recurse_album(self.sloe_tree.treedata.get_or_create_album("final"), [], self.g3root)


    def update_tree(self, tree_name):
        self.connect()
        self.sloe_tree = sloelib.SloeTrees.inst().get_tree(tree_name)
        self.reconcile_to_g3tree(tree_name)




