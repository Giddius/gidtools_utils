from gidtools.gidfiles.functions import pathmaker, path_part_remove
import pytest


def test_pathmaker():
    assert pathmaker('bin', 'folder') == 'bin/folder'
    assert pathmaker(r"C:\Users\name\file") == 'c:/users/name/file'
    assert pathmaker(r"C:\\Users\\name\\file") == 'c:/users/name/file'
    assert pathmaker(r'c:/users/name/file', rev=True) == r'c:\users\name\file'


def test_path_part_remove():
    assert path_part_remove('c:/users/name/file') == 'c:/users/name'
    assert path_part_remove(r"C:\\Users\\name\\file") == 'c:/users/name'
    assert path_part_remove(r"C:\Users\name\file") == 'c:/users/name'
    assert path_part_remove('c:/') == 'c:/'
    with pytest.raises(IndexError):
        assert path_part_remove('whatever')
