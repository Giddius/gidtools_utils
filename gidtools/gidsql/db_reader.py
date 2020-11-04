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
import enum
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
# from PyQt5.QtGui import QFont, QIcon, QBrush, QColor, QCursor, QPixmap, QStandardItem, QRegExpValidator
# from PyQt5.QtCore import (Qt, QRect, QSize, QObject, QRegExp, QThread, QMetaObject, QCoreApplication,
#                           QFileSystemWatcher, QPropertyAnimation, QAbstractTableModel, pyqtSlot, pyqtSignal)
# from PyQt5.QtWidgets import (QMenu, QFrame, QLabel, QDialog, QLayout, QWidget, QWizard, QMenuBar, QSpinBox, QCheckBox, QComboBox,
#                              QGroupBox, QLineEdit, QListView, QCompleter, QStatusBar, QTableView, QTabWidget, QDockWidget, QFileDialog,
#                              QFormLayout, QGridLayout, QHBoxLayout, QHeaderView, QListWidget, QMainWindow, QMessageBox, QPushButton,
#                              QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWizardPage, QApplication, QButtonGroup, QRadioButton,
#                              QFontComboBox, QStackedWidget, QListWidgetItem, QTreeWidgetItem, QDialogButtonBox, QAbstractItemView,
#                              QCommandLinkButton, QAbstractScrollArea, QGraphicsOpacityEffect, QTreeWidgetItemIterator, QAction, QSystemTrayIcon)
# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles import (QuickFile, readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
                               dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file)

from gidtools.gidsql.db_action_base import GidSqliteActionBase
# endregion[Imports]

__updated__ = '2020-11-03 03:30:05'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class Fetch(enum.Enum):
    All = enum.auto()
    One = enum.auto()


class GidSqliteReader(GidSqliteActionBase):
    def __init__(self, in_db_loc, in_pragmas=None):
        super().__init__(in_db_loc, in_pragmas)
        self.row_factory = None
        log.debug(glog.class_initiated(self.__class__))

    def query(self, sql_phrase, variables: tuple = None, fetch: Fetch = Fetch.All):
        conn = sqlite.connect(self.db_loc, isolation_level=None, detect_types=sqlite.PARSE_DECLTYPES)
        if self.row_factory is not None:
            conn.row_factory = self.row_factory
        cursor = conn.cursor()
        try:
            self._execute_pragmas(cursor)
            if variables is not None:
                cursor.execute(sql_phrase, variables)
                log.debug(f"Queried sql phrase '{sql_phrase}' with args {str(variables)} successfully")
            else:
                cursor.executescript(sql_phrase)
                log.debug(f"QueriedScript sql phrase '{sql_phrase}' successfully")
            _out = cursor.fetchone() if fetch is Fetch.One else cursor.fetchall()
        except sqlite.Error as error:
            self._handle_error(error, sql_phrase, variables)
        finally:
            conn.close()
        return _out

    def enable_row_factory(self, in_factory=sqlite.Row):
        self.row_factory = in_factory

    def disable_row_factory(self):
        self.row_factory = None
# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
