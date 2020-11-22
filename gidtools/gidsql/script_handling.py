# region [Imports]

# * Standard Library Imports -->
import os
import shutil
import sqlite3 as sqlite
import configparser
from sqlite3.dbapi2 import Error

# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles import readit, writeit, splitoff, pathmaker, ext_splitter, cascade_rename

# endregion [Imports]

__updated__ = '2020-11-21 20:12:30'


# region [Logging]
log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


class GidSqliteScriptProvider:
    def __init__(self, script_folder):
        self.script_folder = script_folder
        self.setup_prefix = 'setup'

    @property
    def scripts(self):
        _out_dict = {}
        for _file in os.scandir(self.script_folder):
            if os.path.isfile(_file.path) is True and _file.name.endswith('.sql') and not _file.name.startswith(self.setup_prefix):
                _bare_name = _file.name.split('.')[0]
                _out_dict[_bare_name] = _file.path
        return _out_dict

    @property
    def setup_scripts(self):
        # sourcery skip: inline-immediately-returned-variable, list-comprehension
        setup_scripts = []
        for _file in os.scandir(self.script_folder):
            if os.path.isfile(_file.path) is True and _file.name.endswith('.sql') and _file.name.startswith(self.setup_prefix):
                setup_scripts.append(readit(_file.path))
        return setup_scripts

    def __getitem__(self, key):
        _file = self.scripts.get(key, None)
        if _file:
            return readit(_file)


if __name__ == '__main__':
    pass
