# region [Imports]

# * Standard Library Imports -->
import os
import shutil
import sqlite3 as sqlite
import configparser
from sqlite3.dbapi2 import Error
from typing import Union
import enum
# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles import readit, writeit, splitoff, pathmaker, ext_splitter, cascade_rename
from pprint import pformat
# endregion [Imports]

__updated__ = '2020-10-25 17:38:40'


# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


class Fetch(enum.Enum):
    'All' = enum.auto()
    'One' = enum.auto()


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

    def _handle_error(self, error, sql_phrase, variables):
        log.critical(str(error) + f' - with SQL --> {sql_phrase} and args[{pformat(variables)}]' + '\n\n')
        if 'syntax error' in str(error):
            raise SyntaxError(error)
        else:
            raise sqlite.Error(error)

    def _execute_pragmas(self, in_cursor):
        if self.pragmas is not None and self.pragmas != '':
            in_cursor.executescript(self.pragmas)
            log.debug(f"Executed pragmas '{self.pragmas}' successfully")

    def write(self, sql_phrase: str, variables: Union[tuple, list] = None):
        conn = sqlite.connect(self.db_loc, isolation_level=None, detect_types=sqlite.PARSE_DECLTYPES)
        cursor = conn.cursor()
        try:
            self._execute_pragmas(cursor)
            if variables is not None:
                if isinstance(variables, tuple):
                    cursor.execute(sql_phrase, variables)
                    log.debug(f"Executed sql phrase '{sql_phrase}' with args {str(variables)} successfully")
                elif isinstance(variables, list):
                    cursor.executemany(sql_phrase, variables)
                    log.debug(f"ExecutedMany sql phrase from '{sql_phrase}' with arg-iterable {pformat(variables)} successfully")
            else:
                cursor.executescript(sql_phrase)
                log.debug(f"ExecutedScript sql phrase '{sql_phrase}' successfully")
        except sqlite.Error as error:
            self._handle_error(error, sql_phrase, variables)
        finally:
            conn.close()

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

    def dump_sql(self):  # sourcery skip: list-comprehension
        _out = []
        con = sqlite.connect(self.db_loc, isolation_level=None, detect_types=sqlite.PARSE_DECLTYPES)
        for line in con.iterdump():
            _out.append(line)
        con.close()
        return _out

    def vacuum(self):
        self("VACUUM")
        log.info("finished VACUUM the DB")

    def __repr__(self):
        return f"{self.__class__.__name__} ('{self.db_loc}')"

    def __str__(self):
        return self.__class__.__name__
# endregion [Class_1]
