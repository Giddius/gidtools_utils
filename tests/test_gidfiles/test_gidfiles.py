from gidtools.gidfiles.functions import (pathmaker, path_part_remove, loadjson, writejson, readit, readbin,
                                         linereadit, writebin, writeit, clearit, work_in, ext_splitter, file_name_modifier, create_folder)
import pytest
import json
import os
import sys


@ pytest.mark.skipif(sys.platform not in ['win32', 'linux'], reason="paths are specific to windows and linux")
def test_pathmaker():
    assert pathmaker('bin', 'folder') == 'bin/folder'
    assert pathmaker(r"C:\Users\name\file") == 'C:/Users/name/file'
    assert pathmaker(r"C:\\Users\\name\\file") == 'C:/Users/name/file'
    assert pathmaker(r'C:/Users/name/file', rev=True) == r'C:\Users\name\file'
    assert pathmaker(r'C:/Users/name', '../other_name') == r'C:/Users/other_name'


@ pytest.mark.skipif(sys.platform not in ['win32', 'linux'], reason="paths are specific to windows and linux")
def test_path_part_remove():
    assert path_part_remove('C:/Users/name/file') == 'C:/Users/name'
    assert path_part_remove(r"C:\\Users\\name\\file") == 'C:/Users/name'
    assert path_part_remove(r"C:\Users\name\file") == 'C:/Users/name'
    assert path_part_remove('c:/') == 'c:/'
    with pytest.raises(IndexError):
        assert path_part_remove('whatever')


def test_loadjson(simple_json_dict_file, simple_dict):
    json_data = loadjson(simple_json_dict_file)
    assert json_data == simple_dict


def test_writejson(tmpdir, simple_dict):
    _path_unsorted = tmpdir.join('write_test_json_unsorted.json')
    writejson(simple_dict, _path_unsorted, sort_keys=False, indent=2)
    with open(_path_unsorted, 'r') as json_file_unsorted:
        _read_json_data_unsorted = json.load(json_file_unsorted)
    assert _read_json_data_unsorted == simple_dict

    _path_sorted = tmpdir.join('write_test_json_sorted.json')
    writejson(simple_dict, _path_sorted, sort_keys=True, indent=2)
    with open(_path_sorted, 'r') as json_file_sorted:
        _read_json_data_sorted = json.load(json_file_sorted)
    assert _read_json_data_sorted == simple_dict


def test_readit(simple_txt_file, simple_string):
    file_content = readit(simple_txt_file)
    assert file_content == simple_string


def test_readbin(simple_image_file, image_as_bin):
    _bin_data = readbin(simple_image_file)
    assert _bin_data == image_as_bin


def test_linereadit(multiline_txt_file, multiline_string):
    line_content = linereadit(multiline_txt_file)
    assert line_content == multiline_string.splitlines()
    assert line_content[2] == multiline_string.splitlines()[2]


def test_work_in(tmpdir):
    _dir = tmpdir.mkdir('test_folder')
    assert os.getcwd() != _dir
    assert os.path.basename(os.getcwd()) != 'test_folder'
    with work_in(_dir):
        assert os.getcwd() == _dir
        assert os.path.basename(os.getcwd()) == 'test_folder'
    assert os.getcwd() != _dir
    assert os.path.basename(os.getcwd()) != 'test_folder'


def test_ext_splitter(tmpdir):
    _file = str(tmpdir.join('test_file.txt'))
    _file_wo_ext = str(tmpdir.join('test_file'))
    _folder = str(tmpdir.mkdir('test_folder'))
    assert ext_splitter(_file, _out='file') == _file_wo_ext
    assert ext_splitter(_file, _out='ext') == 'txt'
    assert ext_splitter(_file, _out='both') == (_file_wo_ext, 'txt')
    assert ext_splitter(_folder, _out='file') == _folder
    assert ext_splitter(_folder, _out='ext') == 'folder'
    assert ext_splitter(_folder, _out='both') == (_folder, 'folder')


def test_file_name_modifier(tmpdir):
    _file = str(tmpdir.join('test_file.txt'))
    _mod_file = str(tmpdir.join('modified_test_file.txt')).replace('\\', '/')
    _mod_file_2 = str(tmpdir.join('test_file_modified.txt')).replace('\\', '/')
    _mod_file_3 = str(tmpdir.join('modifiedtest_file.txt')).replace('\\', '/')
    new_path = file_name_modifier(_file, 'modified', seperator='_')
    assert new_path == _mod_file

    new_path = file_name_modifier(_file, 'modified', seperator='_', pos='postfix')
    assert new_path == _mod_file_2

    new_path = file_name_modifier(_file, 'modified', seperator='_', new_ext="jpg")
    assert new_path == _mod_file.split('.')[0] + '.jpg'

    new_path = file_name_modifier(_file, 'modified')
    assert new_path == _mod_file_3

    with pytest.raises(Exception):
        new_path = file_name_modifier(_file, 'modi/fied', seperator='_')
    with pytest.raises(Exception):
        new_path = file_name_modifier(_file, 'modified', seperator=':')
    with pytest.raises(Exception):
        new_path = file_name_modifier(_file, 'modified', seperator='_', new_ext='dd:a')


def test_clearit(simple_txt_file):
    clearit(simple_txt_file)
    with open(simple_txt_file, 'r') as txt_file:
        _content = txt_file.read()
    assert _content == ''


def test_creat_folder(tmpdir):
    _dir = tmpdir.mkdir('test_folder')
    _target_folder = os.path.join(_dir, 'new_folder')
    assert os.path.exists(_target_folder) is False
    create_folder(_target_folder)
    assert os.path.exists(_target_folder) is True
