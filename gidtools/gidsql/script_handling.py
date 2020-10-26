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

__updated__ = '2020-10-25 16:42:53'


# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]
