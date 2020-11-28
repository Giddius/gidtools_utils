import pytest
import os
import shutil
from gidtools.gidsql.facade import GidSqliteDatabase

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def simple_db(tmpdir):
    _scriptfolder = tmpdir.mkdir('scripts')
    _db_loc = tmpdir.join('test_db.db')
    for _file in os.scandir(THIS_FILE_DIR):
        if _file.name.endswith('.sql'):
            shutil.copyfile(_file.path, os.path.join(_scriptfolder, _file.name))
    db = GidSqliteDatabase(_db_loc, _scriptfolder)
    yield db


@pytest.fixture
def script_folder(tmpdir):
    _scriptfolder = tmpdir.mkdir('scripts')
    for _file in os.scandir(THIS_FILE_DIR):
        if _file.name.endswith('.sql'):
            shutil.copyfile(_file.path, os.path.join(_scriptfolder, _file.name))
    yield _scriptfolder
