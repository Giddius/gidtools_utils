import os
import base64

FILE = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils\test\test_image.png"
OUT_FILE = 'bin_something_output.py'


def create_varname():
    return os.path.basename(FILE).replace('.', '__').upper()


def read_as_bin():
    with open(FILE, 'rb') as bin_file:
        _content = base64.b64encode(bin_file.read())
    return _content


def bin_it():
    _varname = create_varname()
    _bin_data = read_as_bin()
    with open(OUT_FILE, 'w') as out_bin_file:
        out_bin_file.write(f"{_varname} = {_bin_data}")


if __name__ == '__main__':
    bin_it()
