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

from gidtools.gidsql.db_writer import GidSQLiteWriter
from gidtools.gidsql.db_reader import GidSqliteReader
from gidtools.gidsql.script_handling import GidSqliteScriptProvider
# endregion[Imports]

__updated__ = '2020-11-22 10:35:46'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
# endregion[Constants]


class GidSqliteDatabase:
    def __init__(self, db_location, script_location, config=None):
        self.path = db_location
        self.config = config
        self.pragmas = None
        if self.config is not None:
            self.pragmas = self.config.getlist('general_settings', 'pragmas')
        self.writer = GidSQLiteWriter(db_location, self.pragmas)
        self.reader = GidSqliteReader(db_location, self.pragmas)
        self.scripter = GidSqliteScriptProvider(script_location)
        self.config = config

    def startup_db(self, overwrite=False):
        if os.path.exists(self.path) is True and overwrite is False:
            return None
        else:
            os.remove(self.path)
            for script in self.scripter.setup_scripts:
                self.writer.write(script)

# region[Main_Exec]


if __name__ == '__main__':
    # x = GidSqliteDatabase(pathmaker(THIS_FILE_DIR, "test_db.db"), r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils\tests\test_gidsql")
    # x.startup_db()
    # # x.writer.write('INSERT INTO "main_tbl" ("name", "info") VALUES (?,?)', ("first_name", "first_info"))
    # print(x.reader.query('SELECT * FROM main_tbl'))
    pass
# endregion[Main_Exec]
