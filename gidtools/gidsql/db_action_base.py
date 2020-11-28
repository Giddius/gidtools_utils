# region [Imports]

# * Standard Library Imports -->
import gc
import os
import re
import sys
import json
import lzma
import time
import queue
import logging
import platform
import subprocess
from enum import Enum, Flag, auto
from time import sleep
from pprint import pprint, pformat
from typing import Union
from datetime import tzinfo, datetime, timezone, timedelta
from functools import wraps, lru_cache, singledispatch, total_ordering, partial
from contextlib import contextmanager
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import sqlite3 as sqlite
from sqlite3.dbapi2 import Error
# * Third Party Imports -->
# import requests
# import pyperclip
# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
# from github import Github, GithubException
# from jinja2 import BaseLoader, Environment
# from natsort import natsorted
# from fuzzywuzzy import fuzz, process

# * PyQt5 Imports -->

# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles import (QuickFile, readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
                               dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file)


# endregion[Imports]

__updated__ = '2020-11-26 17:04:37'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.debug(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class GidSqliteActionBase:
    def __init__(self, in_db_loc, in_pragmas=None):
        self.db_loc = in_db_loc
        self.pragmas = in_pragmas
        log.debug(glog.class_initiated(self))

    @property
    def exists(self):
        """
            checks if the db exist and logs it

            Returns
            -------
            bool
                bool if the file exist or not
            """
        if os.path.isfile(self.db_loc):
            log.info("database at %s, does EXIST", self.db_loc)
            return True
        else:
            log.info("databse at %s does NOT EXIST", self.db_loc)
            return False

    @staticmethod
    def _handle_error(error, sql_phrase, variables):
        log.critical(str(error) + f' - with SQL --> {sql_phrase} and args[{pformat(variables)}]')
        if 'syntax error' in str(error):
            raise SyntaxError(error)
        else:
            raise sqlite.Error(error)

    def _execute_pragmas(self, in_cursor):
        if self.pragmas is not None and self.pragmas != '':
            in_cursor.executescript(self.pragmas)
            log.debug(f"Executed pragmas '{self.pragmas}' successfully")

    def __repr__(self):
        return f"{self.__class__.__name__} ('{self.db_loc}')"

    def __str__(self):
        return self.__class__.__name__

# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
