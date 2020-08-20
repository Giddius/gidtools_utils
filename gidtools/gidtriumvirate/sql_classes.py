# region [Imports]


# *NORMAL Imports -->
# from collections import namedtuple
from sqlite3.dbapi2 import Error
# from natsort import natsorted
# import argparse
# import datetime
# import lzma
import os
# import pyperclip
import shutil
import sqlite3 as sqlite
# import time
import configparser
# *GID Imports -->
from gidtools.gidfiles import cascade_rename, ext_splitter, pathmaker, readit, splitoff, writeit

import gidlogger as glog

# *QT Imports -->
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import QSize, Qt
# from PyQt5.QtGui import QIcon, QPixmap, QColor, QBrush, QCursor
# from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QTreeWidgetItem, QListWidgetItem, QHeaderView, QButtonGroup, QTreeWidgetItemIterator, QMenu

# *Local Imports -->
# endregion [Imports]

__updated__ = '2020-08-19 18:17:38'

# region [Localized_Imports]


# endregion [Localized_Imports]


# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


# region [Constants]


# endregion [Constants]


# region [Misc]


# endregion [Misc]


# region [Global_Functions]


# endregion [Global_Functions]


# region [Data_1]


# endregion [Data_1]


# region [Data_2]


# endregion [Data_2]


# region [Data_3]


# endregion [Data_3]


# region [Data_4]


# endregion [Data_4]


# region [Data_5]


# endregion [Data_5]


# region [Class_1]

class GidSQLiteExecutor:
    def __init__(self, in_db_loc, in_pragmas=None):
        self.db_loc = in_db_loc.casefold()
        self.pragmas = in_pragmas
        self.row_factory = None
        log.debug(glog.class_initiated(self.__class__))

    @property
    def exists(self):
        """
        checks if the db exist. logs if it is queryable

        Returns
        -------
        bool
            bool if the file exist or not
        """
        if os.path.isfile(self.db_loc):
            _out = True
            _test_query = self('SELECT name FROM sqlite_master WHERE type="table"')
            log.debug(f"test query resulted in {_test_query}")
            if _test_query != []:
                log.info(f"Database '{self.db_loc}' EXISTS as a file and IS queryable.")
            else:
                log.info(f"Database '{self.db_loc}' EXISTS as a file ,but !IS NOT! queryable")

        else:
            log.info(f"Database '{self.db_loc}' does !NOT EXISTS! as a file")
            _out = False
        return _out

    def execute_phrase(self, in_sql_phrase, in_variables, is_script, fetch):
        conn = sqlite.connect(self.db_loc, isolation_level=None)
        if self.row_factory is not None:
            conn.row_factory = self.row_factory
        cursor = conn.cursor()
        try:
            if self.pragmas is not None and self.pragmas != '':
                cursor.executescript(self.pragmas)
                log.debug(f"Executed pragmas '{self.pragmas}' successfully")
            if is_script is True:
                cursor.executescript(in_sql_phrase)
                log.debug(f"Executet sql script '{in_sql_phrase}' successfully")
            else:
                cursor.execute(in_sql_phrase, in_variables)
                log.debug(f"Executet sql phrase '{in_sql_phrase}' with args {str(in_variables)} successfully")
        except sqlite.Error as error:

            log.critical(str(error) + f' - with SQL --> {in_sql_phrase} and args[{str(in_variables)}]' + '\n\n')
            if 'syntax error' in str(error):
                raise SyntaxError(error)
        if fetch == 'all':
            _out = cursor.fetchall()
        elif fetch == 'one':
            _out = cursor.fetchone()
        else:
            raise Error('no fetch method specified')
        conn.close()
        return _out

    def __call__(self, in_sql_phrase, in_variables=None, is_script=False, fetch='all'):
        _variables = '' if in_variables is None else in_variables
        return self.execute_phrase(in_sql_phrase, _variables, is_script, fetch)

    def enable_row_factory(self, in_factory=sqlite.Row):
        self.row_factory = in_factory

    def disable_row_factory(self):
        self.row_factory = None

    def vacuum(self):
        self("VACUUM")
        log.info("finished VACUUM the DB")

    def __repr__(self):
        return f"{self.__class__} ('{self.db_loc}')"

# endregion [Class_1]


# region [Class_2]


# endregion [Class_2]


# region [Class_3]

class GidSQLiteDatabaser:

    def __init__(self, in_executor, in_scripter, in_backup_folder, in_startup_dict=None):
        self.backup_folder = pathmaker('cwd', in_backup_folder)
        self.executor = in_executor
        self.scripter = in_scripter
        self.startup_dict = {'overwrite': False, 'in_max_backup': 3} if in_startup_dict is None else in_startup_dict
        self.phrasers = {}

    def _backup_db(self, in_max_backup):
        if os.path.isdir(self.backup_folder) is False:
            os.makedirs(self.backup_folder)
        if os.path.isfile(self.executor.db_loc):
            _db_name = splitoff(self.executor.db_loc)[1]
            if os.path.isfile(pathmaker(self.backup_folder, _db_name)) is True:
                shutil.copy(self.executor.db_loc, cascade_rename(_db_name, self.backup_folder, in_max_backup))
            else:
                shutil.copy(self.executor.db_loc, self.backup_folder)
            log.info(f"Database backup from '{self.executor.db_loc}' to {self.backup_folder} was completed")

    def start_db(self):
        if self.executor.exists is False or self.startup_dict.get('overwrite', False) is True:
            if self.executor.exists is True and self.startup_dict.get('overwrite', False) is True:
                log.info(f"Overwriting Database at '{self.executor.db_loc}'")
                self._backup_db(self.startup_dict.get('in_max_backup', 3))
                os.remove(self.executor.db_loc)
                log.info(f"Database at {self.executor.db_loc} was deleted")
            log.info(f"creating Database at '{self.executor.db_loc}'")
            self._project_specific_init_sql()
            log.info("Database created!")
        else:
            log.info(f"Database at {self.executor.db_loc} exists and is ready")

    def _project_specific_init_sql(self):
        try:
            self.executor(self.scripter['extra_init'], is_script=True)
        except KeyError:
            log.debug(f"No extra init found at '{self.scripter.script_folder}'")


# endregion [Class_3]

# region [Class_4]


class GidSQLScripter:
    std_phrases = {
        'all_tables': "SELECT name FROM sqlite_master WHERE type='table'",
        'db_schema': "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
    }

    def __init__(self, in_script_folder):
        self.script_folder = in_script_folder
        self.scripts = {}
        self.get_scripts()

    def get_scripts(self):
        _orig_folder = os.getcwd()
        if os.path.isdir(self.script_folder) is False:
            os.makedirs(self.script_folder)
        os.chdir(self.script_folder)
        for script_files in os.listdir(self.script_folder):
            if '.sql' in script_files:
                self.scripts[ext_splitter(script_files).casefold()] = readit(script_files)
        os.chdir(_orig_folder)

    def write_scripts(self, in_script_file, in_phrase_name, in_sql_phrase, append=True):
        _orig_folder = os.getcwd()
        os.chdir(self.script_folder)
        writeit(in_script_file, f'{in_phrase_name}: {in_sql_phrase}\n', append=append)
        os.chdir(_orig_folder)

    def __getitem__(self, key):
        return self.scripts[key.casefold()]

    def __repr__(self):
        return f"{self.__class__} ('{self.script_folder}')"

# endregion [Class_4]

# region [Class_5]


class GidSQLBuilder:
    def __init__(self, in_cfg_loc='default', in_db_class=GidSQLiteDatabaser):
        self.cfg_loc = pathmaker('cwd', 'config/db_config.ini') if in_cfg_loc == 'default' else in_cfg_loc
        self.cfg_tool = configparser.ConfigParser()
        self.cfg_tool.read(self.cfg_loc)
        self.make_databaser(in_db_class)

    def make_databaser(self, in_db_class):
        _pragmas = self.cfg_tool.get('db_parameter', 'pragmas').replace(',', ';')
        _db_loc = pathmaker('cwd', self.cfg_tool.get('db_parameter', 'db_loc'))
        _backup_loc = self.cfg_tool.get('db_parameter', 'archive_loc')
        _script_folder = pathmaker('cwd', self.cfg_tool.get('db_parameter', 'sql_script_folder'))
        _executor = GidSQLiteExecutor(_db_loc, _pragmas)
        _scripter = GidSQLScripter(_script_folder)
        _startup_dict = {'overwrite': self.cfg_tool.getboolean('db_startup_parameter', 'overwrite'), 'in_max_backup': self.cfg_tool.getint('db_startup_parameter', 'max_backups')}
        self.databaser = in_db_class(_executor, _scripter, _backup_loc, _startup_dict)

    @classmethod
    def get_databaser(cls, in_cfg_loc='default', in_db_class=GidSQLiteDatabaser):
        _builder = GidSQLBuilder(in_cfg_loc, in_db_class)
        return _builder.databaser


# endregion [Class_5]

# region [Class_6]

# endregion [Class_6]

# region [Class_7]

# endregion [Class_7]

# region [Class_8]


# endregion [Class_8]

# region [Class_9]

# endregion [Class_9]

# region [Main_Exec]
if __name__ == '__main__':
    pass


# endregion [Main_Exec]
