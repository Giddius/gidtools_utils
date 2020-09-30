# region [Imports]

# *NORMAL Imports -->
# from benedict import benedict
# from collections import namedtuple
# from contextlib import contextmanager
# from natsort import natsorted
# from pprint import *
# import argparse
# import datetime
# import jinja2
# import lzma
# import os
# import pyperclip
# import re
# import shutil
# import sys
# import time
from enum import Enum, Flag, auto

# *GID Imports -->
# from gidqtutils.giddialogs import LittlePopuper
# from gidqtutils.gidgets import DragDropFileLineEdit, DragDropFileListWidget, OneComboInputPopup, OneLineInputPopup, get_icons, open_one_combo_dialog, open_one_line_dialog
# from gidqtutils.gidqtstuff import as_filedialog, buttongroup_factory, create_new_font, enable_widget_bool, fill_combo_from_db, make_icons, make_icons_stdpath, treewidgeter_simple
# from gidtools.gidfiles import absolute_listdir, appendwriteit, cascade_rename, clearit, dir_change, ext_splitter, file_name_modifier, file_name_time, file_walker, from_dict_to_file, get_absolute_path, get_pickled, hash_to_solidcfg, ishash_same, limit_amount_of_files, linereadit, number_rename, path_part_remove, pathmaker, pickleit, readbin, readit, splitoff, timenamemaker, work_in, writebin, writeit
# from gidtools.gidstuff import BaseToFile, CSVToDict, DictToCSVBase, DictToCSVKeyValueRow, DictToCSVValueList, InputError, ListToFile, RandomRGB, dict_selector, dict_to_attr, not_nempty, pydicterer, pylisterer, rec_dict_walker, sepI, sepvar, tab_spacer, time_log, underscore_maker
# from gidtools.gidtriumvirate import GiDataBase, GiDataBaseMaster, GiSolidConfig, GiUserConfig, GiVariousConfig, GidConfigMaster, GidSQLBuilder, GidSQLPhraser, GidSQLScripter, GidSQLiteDatabaser, GidSQLiteExecutor, RessourceSetUper, give_std_repr
import gidlogger as glog

# *QT Imports -->
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import QSize, Qt
# from PyQt5.QtGui import QIcon, QPixmap, QColor, QBrush, QCursor
# from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QTreeWidgetItem, QListWidgetItem, QHeaderView, QButtonGroup, QTreeWidgetItemIterator, QMenu

# *Local Imports -->

# endregion [Imports]

__updated__ = '2020-08-26 00:20:29'

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]

# region [Constants]


# endregion [Constants]


# region [Enums]

class sqltype(Enum):
    Text = 'TEXT'
    Integer = 'INTEGER'
    Blob = 'BLOB'
    Primkey = 'PRIMARY KEY'

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.data


class sqlspec(Enum):
    Unique = 'UNIQUE'
    NotNull = 'NOT NULL'
    Default = auto()

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.data

    def __add__(self, other):
        return str(self) + ' ' + str(other)

    def __radd__(self, other):
        return str(other) + ' ' + str(self)


# endregion [Enums]

# region [Global_Functions]

# endregion [Global_Functions]

# region [Factories]

# endregion [Factories]

# region [Paths]

# endregion [Paths]

# region [Singleton_Objects]

# endregion [Singleton_Objects]

# region [Support_Objects]

# endregion [Support_Objects]

# region [Functions_1]

# endregion [Functions_1]

# region [Functions_2]

# endregion [Functions_2]

# region [Functions_3]

# endregion [Functions_3]

# region [Functions_4]

# endregion [Functions_4]

# region [Functions_5]


def foreignkey(ref_table_name, ref_column):
    return f'REFERENCES "{ref_table_name}" ("{ref_column}")'

# endregion [Functions_5]

# region [Class_1]


class SQLPhraseGenerator:
    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = {}

    @property
    def create_table_phrase(self):
        _phrase = f'CREATE TABLE IF NOT EXISTS "{self.table_name}" ('
        for key, value in self.columns.items():
            _phrase += f'"{key}" {value}, '
        _phrase = _phrase.rstrip(', ') + ')'
        return _phrase

    def add_column(self, name, datatype, *flags, forkey=None):
        if datatype == sqltype.Primkey:
            self.columns[name] = 'INTEGER PRIMARY KEY'
        else:
            self.columns[name] = f'{str(datatype)}'
            for flag in flags:
                self.columns[name] += flag
            self.columns[name] = self.columns[name].strip()
            if forkey is not None:
                self.columns[name] += ' ' + forkey


# endregion [Class_1]


# region [Class_2]


# endregion [Class_2]


# region [Class_3]


# endregion [Class_3]


# region [Class_4]


# endregion [Class_4]


# region [Class_5]


# endregion [Class_5]


# region [Main_Exec]

if __name__ == '__main__':
    a = SQLPhraseGenerator('test_table')
    a.add_column('test_column', sqltype.Text, sqlspec.NotNull, sqlspec.Unique, forkey=foreignkey('wurst', 'wurst_id'))
    a.add_column('test2_column', sqltype.Primkey)
    print(a.create_table_phrase)


# endregion [Main_Exec]
