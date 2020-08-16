# region [Imports]

# * normal imports -->
# import argparse
# import contextlib
# import datetime
# import os
# import pickle
# import sys
# import jinja2
# import lzma
# import pyperclip
# import re
# import shutil
# import time
# from contextlib import contextmanager
# from pprint import *

# * gid imports -->
import gidlogger as glog
# import gidtools.gidfiles as gif
# * Qt imports -->
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import QSize
# from PyQt5.QtGui import QIcon, QPixmap
# from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QTreeWidgetItem, QListWidgetItem

# endregion [Imports]

__updated__ = '2020-07-15 03:23:00'

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


# region [Functions_1]

def give_std_repr(in_instance, *args):
    # _arg_string = "', '".join(args)
    return f"{in_instance.__class__.__name__}{str(args)}"

# endregion [Functions_1]


# region [Main_Exec]

if __name__ == '__main__':
    pass

# endregion [Main_Exec]
