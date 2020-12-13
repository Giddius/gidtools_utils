# region [Imports]

# * Standard Library Imports -->
import os
import sys
import shutil
from pprint import pformat
import logging
# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles.functions import readit, clearit, writeit, loadjson, pathmaker, writejson, linereadit, appendwriteit

# endregion [Imports]

__updated__ = '2020-12-03 05:15:53'


# region [Logging]

log = logging.getLogger('gidfiles')

glog.import_notification(log, __name__)

# endregion [Logging]


# region [Class_1]

class QuickFile:
    instance_list = []

    def __init__(self, always_clear=True):
        self.extension = 'txt'
        self.name = self._check_name()
        self.path = self._check_path()
        if always_clear is True:
            clearit(self.path)

    def _check_path(self):
        _folder = pathmaker('cwd', 'quick_files')
        if os.path.isdir(_folder) is False:
            os.makedirs(_folder)
        return pathmaker(_folder, self.name)

    def _check_name(self):
        _num = 1
        _name = 'quick_file_' + str(_num)
        while _name in self.instance_list:
            _num += 1
            _name = 'quick_file_' + str(_num)
        self.instance_list.append(_name)
        return _name + '.' + self.extension

    def write(self, data, pretty=False):
        _data = pformat(data) if pretty is True else data
        writeit(self.path, _data)

    def apwrite(self, data, pretty=False, add_newline=True):
        _data = pformat(data) if pretty is True else data
        _data = f"{_data}\n" if add_newline is True else _data
        appendwriteit(self.path, _data)

    def read(self):
        return readit(self.path)

    def lineread(self):
        return linereadit(self.path)

# endregion [Class_1]


# region [Main_Exec]
if __name__ == '__main__':
    pass

# endregion [Main_Exec]
