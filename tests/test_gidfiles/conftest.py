import pytest
import os
import json
import shutil

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def image_as_bin():
    with open(os.path.join(THIS_FILE_DIR, 'test_image.png'), 'rb') as bin_image_file:
        bin_data = bin_image_file.read()
    yield bin_data


@pytest.fixture
def multiline_string():
    yield """This is an multiline string!
    That will be used to test reading and writing multiline strings most likely.
    but can also be used for other tests, also here are some single word lines:
    alpha
    bravo
    charly

    delta
    """


@pytest.fixture
def simple_string():
    yield "This is a test string, to test reading in files!"


@pytest.fixture
def simple_dict():
    yield {'first_key': 'first_value', 'second_key': 'second_value', 'third_key': 3, 'fourth_key': True}


@pytest.fixture
def simple_json_dict_file(tmpdir, simple_dict):
    _path = tmpdir.join('simple_dict.json')
    with open(_path, 'w') as json_file:
        json.dump(simple_dict, json_file, sort_keys=False, indent=2)
    yield _path


@pytest.fixture
def simple_txt_file(tmpdir, simple_string):
    _path = tmpdir.join('simple_text.txt')
    with open(_path, 'w') as txt_file:
        txt_file.write(simple_string)
    yield _path


@pytest.fixture
def multiline_txt_file(tmpdir, multiline_string):
    _path = tmpdir.join('multiline_text.txt')
    with open(_path, 'w') as txt_file:
        txt_file.write(multiline_string)
    yield _path


@pytest.fixture
def simple_image_file(tmpdir, image_as_bin):
    _path = tmpdir.join('test_image.png')
    with open(_path, 'wb') as image_file:
        image_file.write(image_as_bin)
    yield _path
