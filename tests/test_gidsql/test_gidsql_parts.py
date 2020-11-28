import pytest
from gidtools.gidfiles import pathmaker, writeit, readit, writebin, readbin, writejson, loadjson, linereadit, work_in, appendwriteit, pickleit, get_pickled
from gidtools.gidsql.script_handling import GidSqliteScriptProvider
import os

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


def test_script_handling(script_folder):
    script_handler = GidSqliteScriptProvider(script_folder)
    assert script_handler['query_script'] == readit(pathmaker(THIS_FILE_DIR, 'query_script.sql'))
    assert script_handler.get('query_script') == readit(pathmaker(THIS_FILE_DIR, 'query_script.sql'))
    assert script_handler.get('none_script') is None
    assert script_handler.get('missing_script', 'is_missing') == 'is_missing'
    script_handler['new_script'] = 'SELECT * FROM "everything"'
    assert 'new_script.sql' in os.listdir(script_folder)
    assert script_handler['new_script'] == 'SELECT * FROM "everything"'
    assert script_handler.setup_scripts == [readit(pathmaker(THIS_FILE_DIR, 'setup_test.sql'))]
