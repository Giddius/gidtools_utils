import os
from gidtools.gidfiles import pathmaker, writeit


INDIR = r'D:\Dropbox\hobby\Modding\Ressources\Alphas'
replace_dict = {' ': '_',
                '-': '_',
                '/': '_',
                '\\': '_',
                '*': '',
                '{': '_',
                '}': '_',
                '[': '_',
                ']': '_',
                '(': '_',
                ')': '_',
                '>': '_',
                '<': '_',
                '#': '_',
                '&': '_',
                '+': '_',
                '$': '_',
                "'": '',
                '"': '', }

_list = []

for file in os.scandir(INDIR):
    if any(_rep in file.name for _rep in replace_dict) and '.' in file.name:
        _list.append('"' + file.name + '"')


writeit('test_data.txt', '\n'.join(_list))
