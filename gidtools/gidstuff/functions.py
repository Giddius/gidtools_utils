# region [Imports]

# * normal imports -->
# import argparse
# import contextlib
# import datetime
# import jinja2
# import lzma
# import pyperclip
# import re
# import shutil
from gidtools.gidfiles.functions import readit, writeit
import time
import timeit
import matplotlib.pyplot as plt
import statistics
# import os
# import sys
# from contextlib import contextmanager
# from jinja2 import Environment, BaseLoaderimport configparser
# from pprint import *

# * gid imports -->
import gidlogger as glog
from gidtools.gidfiles import pathmaker

# * Qt imports -->
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import QSize
# from PyQt5.QtGui import QIcon, QPixmap
# from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QTreeWidgetItem, QListWidgetItem

# endregion [Imports]

__updated__ = '2020-09-14 21:37:31'

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


# region [Constants]


# endregion [Constants]


# region [Global_Functionss]


# endregion [Global_Functionss]


# region [Functions_1]

def sepvar(in_str):
    _num = len(in_str) / 2
    _amount = 20 - int(_num)
    if _amount < 0:
        _amount = _amount * -1
    _liner = '-' * _amount
    return '#' + _liner + ' ' + in_str + ' ' + _liner + '#'


def sepI():
    return '-' * 10

# endregion [Functions_1]


# region [Functions_2]

def underscore_maker(*in_args):
    _out_string = ''
    for items in list(in_args):
        _out_string += '_' + items
    _out_string = _out_string.lstrip('_')
    return _out_string

# endregion [Functions_2]


# region [Functions_3]

# ------------------------------------------------------------- dict_selector ------------------------------------------------------------ #
def dict_selector(in_name, in_dict):
    # ------------------------------------------------------------- dict_selector ------------------------------------------------------------ #
    """dict_selector, returns value of a key in the in_dict, that is matching the name.

    used to get rid of too high amount if statements.

    Args:
        in_name (str): the argument you received
        in_dict (dict): the dictionary with the available arguments and resulting actions/strings/whatever

    Returns:
        [value]: returns whatever the value is, returns empty string  if not matches, plus prints warning
        """
    for key, value in in_dict.items():
        if in_name == key:
            _out = value
    if _out not in ['', [], (), {}]:
        return _out
    else:
        print('Warning, no matching key')
        return ''

# endregion [Functions_3]


# region [Functions_4]

def dict_to_attr(in_object, in_dict):
    for key, value in in_dict.items():
        setattr(in_object, key, value)

# endregion [Functions_4]


# region [Functions_5]

def tab_spacer(in_multi: int):
    return ' ' * (4 * in_multi)

# endregion [Functions_5]


# region [Functions_6]

def time_log(in_t0, in_logger, in_message):
    _minutes = (time.time() - in_t0) // 60
    in_logger.critical(f"{in_message} time: [{_minutes}]")

# endregion [Functions_6]


# region [Functions_7]

def not_nempty(in_put):
    # Todo: Check if you would rather use 'bool()' and if it works in every situation
    _out = False
    if in_put is not None:
        if isinstance(in_put, str):
            if in_put != '':
                _out = True
        elif isinstance(in_put, list):
            if in_put != []:
                _out = True
        elif isinstance(in_put, dict):
            if in_put != {}:
                _out = True
    return _out


# endregion [Functions_7]


# region [Functions_8]

def pydicterer(in_file, in_dict_name='DICT_1', in_out_file='default'):
    _output = pathmaker(r"D:\Dropbox\hobby\Modding\Ressources\assorted\pyDicterer_output.py") if in_out_file == 'default' else in_out_file
    _lines = readit(in_file, per_lines=True, strip_n=True)
    writeit(_output, f"\n\n{in_dict_name.upper()} = " + "{\n", append=True)
    for line in _lines:
        try:
            key, value = line.split(';')
            writeit(_output, f"        '{key}': '{str(value)}',\n", append=True)
        except ValueError:
            log.debug(f"ValueError with line '{line}")
    writeit(_output, "    }\n\n", append=True)

    # endregion [Functions_8]

    # region [Functions_9]


def pylisterer(in_file, in_list_name='LIST_1', in_out_file='default'):
    _output = pathmaker(r"D:\Dropbox\hobby\Modding\Ressources\assorted\pyListerer_output.py") if in_out_file == 'default' else in_out_file
    _lines = readit(in_file, per_lines=True, strip_n=True)
    writeit(_output, f"\n\n{in_list_name.upper()} = " + "[\n", append=True)
    for line in _lines:
        writeit(_output, f"        '{line}',\n", append=True)
    writeit(_output, "    ]\n\n", append=True)

# endregion [Functions_9]


def nesteddictvalues(d):
    for v in d.values():
        if isinstance(v, dict):
            yield from nesteddictvalues(v)
        else:
            yield v

# region [Functions_10]


def rec_dict_walker(value, key=None):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from rec_dict_walker(v, k)
    else:
        if key is None:
            yield value
        else:
            yield key, value

# endregion [Functions_10]


def timeit_runner(func, repeat=1, graph='scatter'):
    _graph_data = []
    _value_list = []
    timeit_object = timeit.Timer(func)
    for index, i in enumerate(range(repeat)):
        _time = timeit_object.timeit(number=1)
        _graph_data.append((index, _time))
        _value_list.append(_time)
    print(f"Mean: {round(statistics.mean(_value_list),2)}")
    print(f"Median: {round(statistics.median(_value_list),2)}")
    print(f"Std Dev: {round(statistics.stdev(_value_list),2)}")
    x, y = zip(*_graph_data)
    if graph == 'scatter':
        plt.scatter(x, y)
    elif graph == 'plot':
        plt.plot(x, y)
    plt.show()


# region [Main_Exec]
if __name__ == '__main__':
    pass


# endregion [Main_Exec]
