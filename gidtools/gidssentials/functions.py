# region [Imports]


# *NORMAL Imports -->
# from collections import namedtuple
# from contextlib import contextmanager
# from jinja2 import Environment, BaseLoader
# from natsort import natsorted
# from pprint import *
# import argparse
# import datetime
# import lzma
# import os
# import pyperclip
# import re
# import shutil
# import sqlite3 as sqlite
# import sys
# import time
import wmi
# *GID Imports -->
# from gidtools.gidfiles import pathmaker, writeit, readit, clearit, pickleit, get_pickled, ext_splitter, splitoff
# from gidtools.gidstuff import RandomRGB, not_nempty, time_log
# from gidtools.gidtriumvirate import GiUserConfig, GiSolidConfig, GiDataBase, give_std_repr
# import gidlogger as glog

# *QT Imports -->
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import QSize, Qt
# from PyQt5.QtGui import QIcon, QPixmap, QColor, QBrush, QCursor
# from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QTreeWidgetItem, QListWidgetItem, QHeaderView, QButtonGroup, QTreeWidgetItemIterator, QMenu

# endregion [Imports]

__updated__ = '2020-09-15 04:13:41'


# region [Logging]

# log = glog.aux_logger(__name__)
# log.info(glog.imported(__name__))

# endregion [Logging]


# region [Constants]


# endregion [Constants]


# region [Misc]


# endregion [Misc]


# region [Global_Functions]


# endregion [Global_Functions]


# region [Functions_1]

def get_drives():
    _out = []
    c = wmi.WMI()
    for drive in c.Win32_LogicalDisk():
        _out.append(drive.Caption)
    return _out


# endregion [Functions_1]


# region [Functions_2]


# endregion [Functions_2]


# region [Functions_3]


# endregion [Functions_3]


# region [Functions_4]


# endregion [Functions_4]


# region [Functions_5]


# endregion [Functions_5]


# region [Functions_6]


# endregion [Functions_6]


# region [Functions_7]


# endregion [Functions_7]


# region [Functions_8]


# endregion [Functions_8]


# region [Functions_9]


# endregion [Functions_9]


# region [Main_Exec]

if __name__ == '__main__':
    pass


# endregion [Main_Exec]
