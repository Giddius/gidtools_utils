# region [Imports]

# * Standard Library Imports -->
import os
import sys
import shutil
from pprint import pformat

# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles.functions import readit, clearit, writeit, loadjson, pathmaker, writejson, linereadit, appendwriteit

# endregion [Imports]

__updated__ = '2020-10-14 14:36:29'


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


# region [Class_2]


# endregion [Class_2]


# region [Class_3]


# endregion [Class_3]


# region [Class_4]


# endregion [Class_4]


# region [Class_5]


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
