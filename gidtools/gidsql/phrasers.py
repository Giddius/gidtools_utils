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
from gidtools.gidsql.exceptions import GidSqliteColumnAlreadySetError, GidSqliteSemiColonError

# endregion[Imports]

__updated__ = '2020-11-12 14:32:23'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


def quoter(item):
    return f'"{item}"'


class GidSqliteInserter:
    def __init__(self, table, or_ignore=False):
        self.table = table
        self.or_ignore = or_ignore
        self.columns = {}
        if ';' in self.table:
            raise GidSqliteSemiColonError

    def add_column(self, column, value):
        if column in self.columns:
            raise GidSqliteColumnAlreadySetError(self.table, column)
        if ';' in column and ';' in value:
            raise GidSqliteSemiColonError
        self.columns[column] = value

    def sql_phrase(self):
        _columns = ', '.join(map(quoter, self.columns.keys()))
        _values = ', '.join([value for key, value in self.columns.items()])
        phrase = 'INSERT OR IGNORE INTO ' if self.or_ignore is True else 'INSERT INTO '
        phrase += f'"{self.table}" ' + f'({_columns}) VALUES ({_values})'

        return phrase

    @staticmethod
    def fk_select(table, output_column, input_column, condition='='):
        return f'(SELECT "{output_column}" FROM "{table}" WHERE "{input_column}"{condition}?)'

# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
