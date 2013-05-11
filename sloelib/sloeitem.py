
import ConfigParser
import logging
import os
import sys
from pprint import pprint, pformat
import uuid

from sloeconfig import SloeConfig


class SloeItem:
    MANDATORY_ELEMENTS = ("leafname", "name", "primacy", "tree", "subtree", "worth")

    def __init__(self):
        self.data = {}

    def create_new(self, existing_item, spec):
        self.data = {}

        if existing_item:
            # Preserve UUID of item
            self.data["uuid"] = existing_item.data["uuid"]
        else:
            # No pre-existing item, so take all info from passed-in spec
            self.data["uuid"] = uuid.uuid4()

        for element in self.MANDATORY_ELEMENTS:
            if existing_item is not None and existing_item.data[element] != spec[element]:
                logging.error("Mismatched original item: element %s new %s !=  old %s" % (
                    element, spec[element], existing_item[element]))
            # print "%s %s" % (pformat(spec), pformat(existing_item))
            self.data[element] = spec[element]


    def create_from_ini_file(self, ini_filepath, error_info):
        with open(ini_filepath, "rb") as ini_fp:
            self._create_from_ini_fp(ini_fp, error_info)


    @classmethod
    def new_from_ini_file(cls, ini_filepath, error_info):
        item = SloeItem()
        item.create_from_ini_file(ini_filepath, error_info)
        return item


    def _create_from_ini_fp(self, ini_fp, error_info):
        self.data = {}
        parser = ConfigParser.RawConfigParser()
        parser.readfp(ini_fp)
        file_data = {}
        for section in parser.sections():
            file_data[section] = {}
            for item_name, value in parser.items(section):
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                file_data[section][item_name] = value


        # Verification
        if len(file_data.keys()) != 1:
            raise SloeError("Only one section supported in .ini: %s" % error_info)

        for section, section_data in file_data.iteritems():
            data = file_data[file_data.keys()[0]]
            if section != "item" and section != "item-%s" % data["uuid"]:
                raise SloeError("in-file section/uuid mismatch %s != %s in %s" %
                    (section, "item-%s" % data["uuid"], full_path))

        missing_elements = []
        for element in self.MANDATORY_ELEMENTS:
            if element not in data:
                missing_elements.append(element)

        if len(missing_elements) > 0:
            raise SloeError("Missing elements %s in .ini: %s" % (", ".join(missing_elements), error_info))

        self.data = data


    def get_file_dir(self):
        root_dir = SloeConfig.get_global().get_tree_root_dir(self.data["tree"])
        return os.path.join(root_dir, self.data["primacy"], self.data["worth"], self.data["tree"], self.data["subtree"])


    def get_filepath(self):
        return os.path.join(self.get_file_dir(), self.data["leafname"])


    def get_key(self):
        return "item-%s" % str(self.data["uuid"])


    def get_ini_leafname(self):
        return "%s-%s.ini" % (self.data["name"], self.data["uuid"])


    def get_ini_filepath(self):
        treepath = os.path.dirname(self.get_filepath())
        return os.path.join(treepath, self.get_ini_leafname());


    def savetofile(self):
        parser = ConfigParser.ConfigParser()
        section = self.get_key()
        parser.add_section(section)
        for name, value in self.data.iteritems():
            parser.set(section, name, '"%s"' % str(value))

        with open(self.get_ini_filepath(), "wb") as file:
            parser.write(file)


    def dump(self):
      return pformat(self.data)
