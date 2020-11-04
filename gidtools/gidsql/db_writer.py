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

from gidtools.gidsql.db_action_base import GidSqliteActionBase
# endregion [Imports]

__updated__ = '2020-11-03 03:28:37'


# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


# region [Class_1]

class GidSQLiteWriter(GidSqliteActionBase):
    def __init__(self, in_db_loc, in_pragmas=None):
        super().__init__(in_db_loc, in_pragmas)
        log.debug(glog.class_initiated(self.__class__))

    def write(self, sql_phrase: str, variables: Union[str, tuple, list] = None):
        conn = sqlite.connect(self.db_loc, isolation_level=None, detect_types=sqlite.PARSE_DECLTYPES)
        cursor = conn.cursor()
        try:
            self._execute_pragmas(cursor)
            if variables is not None:
                if isinstance(variables, str):
                    cursor.execute(sql_phrase, (variables,))
                    log.debug(f"Executed sql phrase '{sql_phrase}' with args {str(variables)} successfully")
                elif isinstance(variables, tuple):
                    cursor.execute(sql_phrase, variables)
                    log.debug(f"Executed sql phrase '{sql_phrase}' with args {str(variables)} successfully")
                elif isinstance(variables, list):
                    cursor.executemany(sql_phrase, variables)
                    log.debug(f"ExecutedMany sql phrase from '{sql_phrase}' with arg-iterable {pformat(variables)} successfully")
            else:
                cursor.executescript(sql_phrase)
                log.debug(f"ExecutedScript sql phrase '{sql_phrase}' successfully")
            conn.commit()
        except sqlite.Error as error:
            self._handle_error(error, sql_phrase, variables)
        finally:
            conn.close()

    def __repr__(self):
        return f"{self.__class__.__name__} ('{self.db_loc}')"

    def __str__(self):
        return self.__class__.__name__
# endregion [Class_1]


if __name__ == '__main__':
    pass
