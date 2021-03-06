# region [Imports]

# * normal imports -->
import datetime
import os
import pickle
import shutil
from contextlib import contextmanager
from pprint import pformat
import configparser
import hashlib
import json
# * gid imports -->
import gidlogger as glog

# * Qt imports -->
# *Local Imports -->


# endregion [Imports]

__updated__ = '2020-09-14 20:03:35'

# region [Logging]

log = glog.aux_logger(__name__)
log.debug(glog.imported(__name__))

# endregion [Logging]


# region [Constants]


# endregion [Constants]


# region [Global_Functions]


# endregion [Global_Functions]


# region [Function_JSON]

def loadjson(in_file):
    with open(in_file, 'r') as jsonfile:
        _out = json.load(jsonfile)
    return _out


def writejson(in_object, in_file, sort_keys=True, indent=0):
    writeit(in_file, json.dumps(in_object, sort_keys=sort_keys, indent=indent))

# endregion [Function_JSON]

# region [Function_Hashes]


def hash_to_solidcfg(in_file, in_name=None, in_config_loc='default'):
    _cfg = configparser.ConfigParser()
    _cfg_loc = pathmaker('cwd', 'config', 'solid_config.ini') if in_config_loc == 'default' else in_config_loc
    _bin_file = readbin(in_file)
    _name = splitoff(in_file)[1].replace('.', '') if in_name is None else in_name
    _cfg.read(_cfg_loc)
    _hash = hashlib.md5(_bin_file).hexdigest()
    if _cfg.has_section('hashes') is False:
        log.info("section ['hashes'] does not exist in solid_config.ini, creating it now!")
        _cfg.add_section('hashes')
        log.info("section ['hashes'] added to solid_config.ini")
    _cfg.set('hashes', _name, _hash)
    log.info(f"added hash [{_hash}] to section ['hashes'] in solid_config.ini")
    with open(_cfg_loc, 'w') as configfile:
        _cfg.write(configfile)
        log.debug("saved new solid_config.ini at '{_cfg_loc}'")
    _cfg.read(_cfg_loc)
    if _cfg.get('hashes', _name) != _hash:
        raise configparser.Error("recently saved hash does not match the file hash")


def ishash_same(in_file, in_name=None, in_config_loc='default'):
    _cfg = configparser.ConfigParser()
    _cfg_loc = pathmaker('cwd', 'config', 'solid_config.ini') if in_config_loc == 'default' else in_config_loc
    _bin_file = readbin(in_file)
    _name = splitoff(in_file)[1].replace('.', '') if in_name is None else in_name
    _cfg.read(_cfg_loc)
    _hash = hashlib.md5(_bin_file).hexdigest()
    if _cfg.has_section('hashes') is True:
        if _cfg.has_option('hashes', _name):
            if _cfg.get('hashes', _name) != _hash:
                _out = False
                log.info("hashes are !NOT! the same")
            elif _cfg.get('hashes', _name) == _hash:
                _out = True
                log.info("hashes are the same")
        else:
            _out = False
            log.info('missing option')
    else:
        log.critical("section ['hashes'] is missing in solid_config.ini, it is absolutely needed")
        raise configparser.Error("section ['hashes'] does not exist!!")

    return _out


# endregion [Function_Hashes]

# region [Functions_Unsorted]


def absolute_listdir(in_dir, in_filter=None, in_filter_type=True):
    for files in os.listdir(in_dir):
        if in_filter is not None:
            if in_filter_type is True:
                if in_filter in files:
                    yield pathmaker(in_dir, files)
            elif in_filter_type is False:
                if in_filter not in files:
                    yield pathmaker(in_dir, files)
        else:
            yield pathmaker(in_dir, files)

# endregion [Functions_Unsorted]

# region [Functions_Delete]


# endregion [Functions_Delete]


# region [Functions_Read]

# -------------------------------------------------------------- readbin -------------------------------------------------------------- #
def readbin(in_file):
    # -------------------------------------------------------------- readbin -------------------------------------------------------------- #
    """
    Reads a binary file.

    Parameters
    ----------
    in_file : str
        A file path

    Returns
    -------
    str
        the decoded file as string
    """
    with open(pathmaker(in_file), 'rb') as binaryfile:
        return binaryfile.read()


# -------------------------------------------------------------- readit -------------------------------------------------------------- #
def readit(in_file, per_lines=False, strip_n=False, in_encoding='utf-8', in_errors='strict'):
    # -------------------------------------------------------------- readit -------------------------------------------------------------- #
    """
    Reads a file.

    Parameters
    ----------
    in_file : str
        A file path
    per_lines : bool, optional
        If True, returns a list of all lines, by default False
    strip_n : bool, optional
        If True remove the newline marker from the string, by default False
    in_encoding : str, optional
        Sets the encoding, by default 'utf-8'
    in_errors : str, optional
        How to handle encoding errors, either 'strict' or 'ignore', by default 'strict'

    Returns
    -------
    str
        the read in file as string
    """
    _file = in_file
    _output_list = []
    with open(_file, 'r', encoding=in_encoding, errors=in_errors) as _rfile:
        if per_lines is True:
            _output_list.extend(_rfile.readlines())
            if strip_n is True:
                _output = [item.replace('\n', '') for item in _output_list]

            else:
                _output = _output_list

        elif per_lines is False:
            _output_string = _rfile.read()
            if strip_n is True:
                _output = _output_string.replace('\n', '')

            else:
                _output = _output_string

    return _output


def linereadit(in_file, in_encoding='utf-8', in_errors='strict'):
    with open(in_file, 'r', encoding=in_encoding, errors=in_errors) as lineread_file:
        _out = lineread_file.read().splitlines()
    return _out

# endregion [Functions_Read]


# region [Functions_Write]

def from_dict_to_file(in_out_file, in_dict_name, in_dict):
    appendwriteit(in_out_file, '\n\n')
    _dict_string = in_dict_name + ' = {' + pformat(in_dict) + '\n}'
    _dict_string = _dict_string.replace('{{', '{\n').replace('}}', '}').replace('}\n}', '\n}')
    appendwriteit(in_out_file, _dict_string)


# -------------------------------------------------------------- writebin -------------------------------------------------------------- #
def writebin(in_file, in_data):
    # -------------------------------------------------------------- writebin -------------------------------------------------------------- #
    """
    Writes a string to binary.

    Parameters
    ----------
    in_file : str
        The target file path
    in_data : str
        The data to write
    """
    if isinstance(in_file, (tuple, list)):
        _file = pathmaker(*in_file)
    elif isinstance(in_file, str):
        _file = pathmaker(in_file)
    with open(_file, 'wb') as outbinfile:
        outbinfile.write(in_data)


# -------------------------------------------------------------- writeit -------------------------------------------------------------- #
def writeit(in_file, in_data, append=False, in_encoding='utf-8'):
    # -------------------------------------------------------------- writeit -------------------------------------------------------------- #
    """
    Writes to a file.

    Parameters
    ----------
    in_file : str
        The target file path
    in_data : str
        The data to write
    append : bool, optional
        If True appends the data to the file, by default False
    in_encoding : str, optional
        Sets the encoding, by default 'utf-8'
    """
    if isinstance(in_file, (tuple, list)):
        _file = pathmaker(*in_file)
    elif isinstance(in_file, str):
        _file = pathmaker(in_file)
    _write_type = 'w' if append is False else 'a'
    _in_data = in_data
    with open(_file, _write_type, encoding=in_encoding) as _wfile:
        _wfile.write(_in_data)


def appendwriteit(in_file, in_data, in_encoding='utf-8'):
    with open(in_file, 'a', encoding=in_encoding) as appendwrite_file:
        appendwrite_file.write(in_data)


# -------------------------------------------------------------- clearit -------------------------------------------------------------- #
def clearit(in_file):
    # -------------------------------------------------------------- clearit -------------------------------------------------------------- #
    """
    Deletes the contents of a file.

    Parameters
    ----------
    in_file : str
        The target file path
    """
    writeit(pathmaker(in_file), '')
    log.debug(f"contents of file [{in_file}] was deleted")


# endregion [Functions_Write]


# region [Functions_Paths]

# -------------------------------------------------------------- pathmaker -------------------------------------------------------------- #
def pathmaker(first_segment, *in_path_segments, rev=False):
    # -------------------------------------------------------------- pathmaker -------------------------------------------------------------- #
    """
    Normalizes input path or path fragments, replaces '\\\\' with '/' and combines fragments.

    Parameters
    ----------
    first_segment : str
        first path segment, if it is 'cwd' gets replaced by 'os.getcwd()'
    rev : bool, optional
        If 'True' reverts path back to Windows default, by default None

    Returns
    -------
    str
        New path from segments and normalized.
    """
    _first = os.getcwd() if first_segment == 'cwd' else first_segment
    _path = os.path.join(_first, *in_path_segments)
    _path = _path.replace('\\\\', '/')
    _path = _path.replace('\\', '/')
    if rev is True:
        _path = _path.replace('/', '\\')

    return _path.strip()


# -------------------------------------------------------------- work_in -------------------------------------------------------------- #
@contextmanager
def work_in(in_dir):
    # -------------------------------------------------------------- work_in -------------------------------------------------------------- #
    """
    A context manager which changes the working directory to the given path,
    and then changes it back to its previous value on exit.

    Parameters
    ----------
    in_dir : str
        A file directory path
    """
    prev_cwd = os.getcwd()
    os.chdir(in_dir)
    log.debug(f"starting to work in directory [{in_dir}]")
    yield
    log.debug(f"stopped to work in directory [{in_dir}] and returned to directory [{prev_cwd}]")


# -------------------------------------------------------------- path_part_remove -------------------------------------------------------------- #
def path_part_remove(in_file):
    # -------------------------------------------------------------- path_part_remove -------------------------------------------------------------- #
    """
    Removes last segment of path, to get parent path.

    Parameters
    ----------
    in_file : str
        A file path

    Returns
    -------
    str
        A new file path, parent path of input.
    """
    _file = pathmaker(in_file)
    _path = _file.split('/')
    _useless = _path.pop(-1)
    _first = _path.pop(0) + '/'
    _out = pathmaker(_first, *_path)
    log.debug(f"path segment [{_useless}] was removed from path [{_file}] to get [{_out}]")
    return _out


# -------------------------------------------------------------- dir_change -------------------------------------------------------------- #
def dir_change(*args, in_adress_home=False, ):
    # -------------------------------------------------------------- dir_change -------------------------------------------------------------- #
    """
    changes directory to script location or provided path.

    Parameters
    ----------
    in_adress_home : bool, optional
        'in_home_adress' if True defaults everything to location of current file and *args are ignored, by default False
    """
    if in_adress_home is True:
        _path_to_home = os.path.abspath(os.path.dirname(__file__))
    else:
        _path_to_home = pathmaker(*args)
    os.chdir(_path_to_home)
    log.debug('We are now in ' + _path_to_home)


# -------------------------------------------------------------- get_absolute_path -------------------------------------------------------------- #
def get_absolute_path(in_path='here', include_file=False):
    # -------------------------------------------------------------- get_absolute_path -------------------------------------------------------------- #
    """
    Generates absolute path from relative path, optional gives it out as folder, by removing the file segment.

    Parameters
    ----------
    in_path : str, optional
        A relative filepath, if 'here' gets replaced by current file, by default 'here'
    include_file : bool, optional
        if False doesn't include last segment of path, by default False

    Returns
    -------
    str
        An absolute file path
    """
    _rel_path = __file__ if in_path == 'here' else in_path
    _out = os.path.abspath(_rel_path)
    if include_file is False:
        _out = splitoff(_out)[0]
    return _out


# endregion [Functions_Paths]


# region [Functions_Names]

# -------------------------------------------------------------- file_name_time -------------------------------------------------------------- #
def file_name_time(var_sep='_', date_time_sep='-', box=('[', ']')):
    # -------------------------------------------------------------- file_name_time -------------------------------------------------------------- #
    """
    creates a name that is the date and time.

    Parameters
    ----------
    var_sep : str, optional
        specifies the symbol used to seperate the file name and the datetime, by default '_'
    date_time_sep : str, optional
        specifies the symbol used to seperate the date and time, by default '-'
    box : tuple, optional
        symbols used to frame the datetime, by default ('[', ']')

    Returns
    -------
    str
        New file name
    """
    whole_time = str(datetime.datetime.today()).split(' ')
    today_date_temp = whole_time[0].split('-')
    today_date = var_sep.join(today_date_temp)
    today_time_temp = whole_time[1].split('.')[0].split(':')
    today_time = '' + today_time_temp[0] + var_sep + today_time_temp[1]
    if box is not None:
        _output = box[0] + today_date + date_time_sep + today_time + box[1]
    else:
        _output = today_date + date_time_sep + today_time
    log.debug(f"created file name [{_output}]")
    return _output


# -------------------------------------------------------------- number_rename -------------------------------------------------------------- #
def number_rename(in_file_name, in_round=1):
    # -------------------------------------------------------------- number_rename -------------------------------------------------------------- #
    """
    Appends a number to a file name if it already exists, increases the number and checks again.

    Parameters
    ----------
    in_file_name : str
        [description]
    in_round : int, optional
        specifies the number to start on, by default 0

    Returns
    -------
    str
        new file name
    """
    _temp_path = in_file_name
    _temp_path = _temp_path.split('.')
    log.debug(f" Parts of rename: [0] = {_temp_path[0]}, [1] = {_temp_path[1]}")
    _output = _temp_path[0] + str(in_round) + '.' + _temp_path[1]
    log.debug(f"Setting name to {_output}")
    _new_round = int(in_round) + 1
    return _exist_handle(_output, _new_round, _temp_path[0] + '.' + _temp_path[1])


# -------------------------------------------------------------- cascade_rename -------------------------------------------------------------- #
# ! check which file it uses, so it doesnt add to back ~~~
def cascade_rename(in_file_name, in_folder, in_max_files=3):
    # -------------------------------------------------------------- cascade_rename -------------------------------------------------------------- #
    _temp_file_dict = {}
    _name = ext_splitter(in_file_name)
    _ext = ext_splitter(in_file_name, _out='ext')
    file_index = 1
    for files in os.listdir(in_folder):
        files = files.casefold()
        if _name in files:
            if any(letter.isdigit() for letter in files):
                _temp_file_dict[str(file_index)] = pathmaker(in_folder, files)
                file_index = int(file_index) + 1
            else:
                _temp_file_dict[str(0)] = pathmaker(in_folder, files)
    if file_index + 1 <= in_max_files:
        if file_index == 1:
            writeit(pathmaker(in_folder, _name + str(file_index) + '.' + _ext), ' ')
            _temp_file_dict[str(file_index)] = pathmaker(in_folder, _name + str(file_index) + '.' + _ext)
        else:
            writeit(pathmaker(in_folder, _name + str(file_index + 1) + '.' + _ext), ' ')
            _temp_file_dict[str(file_index + 1)] = pathmaker(in_folder, _name + str(file_index + 1) + '.' + _ext)
    for i in range(len(_temp_file_dict) - 1):
        if i != 0:
            shutil.copy(_temp_file_dict[str(i)], _temp_file_dict[str(i - 1)])
        else:
            os.remove(_temp_file_dict[str(0)])
    return pathmaker(in_folder, _temp_file_dict[str(0)])


# -------------------------------------------------------------- exist_handle -------------------------------------------------------------- #
def _exist_handle(in_path, in_round, original_path):
    # -------------------------------------------------------------- exist_handle -------------------------------------------------------------- #
    """
    internal use for the "number_rename" function.
    """
    if os.path.exists(in_path) is True:
        log.debug(f"{in_path} already exists")
        _new_path = number_rename(original_path, in_round)
        log.debug(f" variables for rename round {in_round} are: original_path = {original_path}, in_round = {in_round}")
    else:
        _new_path = in_path
        log.debug(
            f'{_new_path} does not exist, setting it to f"{in_path} does not exist, setting it to {_new_path}"'
        )

    return _new_path


# -------------------------------------------------------------- splitoff -------------------------------------------------------------- #
def splitoff(in_file):
    # -------------------------------------------------------------- splitoff -------------------------------------------------------------- #
    """splitoff, wraps os.path.dirname and os.path.basename to return both as tuple.

    Args:
        in_file (str): the full file path

    Returns:
        tuple: where '[0]' is the dirname and '[1]' is the basename(filename)"""

    _file = pathmaker(in_file)
    return (os.path.dirname(_file), os.path.basename(_file))


# -------------------------------------------------------------- timenamemaker -------------------------------------------------------------- #
def timenamemaker(in_full_path):
    # -------------------------------------------------------------- timenamemaker -------------------------------------------------------------- #
    """
    Creates a filename, that has the time included.

    Parameters
    ----------
    in_full_path : str
        full path of the file name that is to be modified

    Returns
    -------
    str
        the new file name
    """
    _time = str(datetime.datetime.now()).rsplit('.', maxsplit=1)[0]
    log.debug(f"_time is [{_time}]")
    _file = splitoff(in_full_path)[1]
    _file_tup = os.path.splitext(_file)
    _new_file_name = _file_tup[0] + _time + _file_tup[1]
    _path = splitoff(in_full_path)[0]
    _out = pathmaker(_path, _new_file_name)
    log.debug(f"created file name [{_out}] from original name [{in_full_path}]")
    return _out


# -------------------------------------------------------------- ext_splitter -------------------------------------------------------------- #
def ext_splitter(in_file, _out='file'):
    # -------------------------------------------------------------- ext_splitter -------------------------------------------------------------- #
    """
    Splits a file name by the extension and returns either the name or the extension.

    Parameters
    ----------
    in_file : str
        a file name
    _out : str, optional
        the part to return either "file" or "ext", by default 'file'

    Returns
    -------
    str
        either the file name or the file extension
    """
    if '.' in in_file:
        _file = in_file.rsplit('.', maxsplit=1)[0]
        _ext = in_file.rsplit('.', maxsplit=1)[1]
    else:
        _file = in_file
        _ext = 'folder'
    if _out == 'file':
        _output = _file
    elif _out == 'ext':
        _output = _ext
    elif _out == 'both':
        _output = (_file, _ext)

    return _output


# -------------------------------------------------------------- file_name_modifier -------------------------------------------------------------- #
def file_name_modifier(in_path, in_string, pos='prefix', new_ext=None, seperator=None):
    # -------------------------------------------------------------- file_name_modifier -------------------------------------------------------------- #
    """
    changes a file name by inserting a string.

    Parameters
    ----------
    in_path : str
        the file path
    in_string : str
        the string inserted in the name
    pos : str, optional
        the position where to insert the string, either "prefix" or "postfix", by default 'prefix'
    new_ext : str, optional
        a new extension for th file name if not None, by default None
    seperator : str, optional
        the symbol that is used to seperate the old and new name, by default None

    Returns
    -------
    str
        the new file path

    Raises
    ------
    Exception
        checks the input for forbidden characters for filenames on Windows.
    """
    _forbiden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    if new_ext is not None and any(chars in new_ext for chars in _forbiden_chars):
        raise Exception(f"You can't use the following symbols in file names {str(_forbiden_chars)}")
    if seperator is not None and any(chars in seperator for chars in _forbiden_chars):
        raise Exception(f"You can't use the following symbols in file names {str(_forbiden_chars)}")
    if any(chars in in_string for chars in _forbiden_chars):
        raise Exception(f"You can't use the following symbols in file names {str(_forbiden_chars)}")
    _path, _file = splitoff(pathmaker(in_path))
    if new_ext is not None:
        _file = _file.rsplit('.', 1)[0] + new_ext if '.' in new_ext else _file.rsplit('.', 1)[0] + '.' + new_ext
    _file, _ext = _file.rsplit('.', 1)
    if seperator is None:
        _outfile = in_string + _file + '.' + _ext if pos == 'prefix' else _file + in_string + '.' + _ext
    else:
        _outfile = in_string + seperator + _file + '.' + _ext if pos == 'prefix' else _file + seperator + in_string + '.' + _ext
    _out = pathmaker(_path, _outfile)
    log.debug(f"created file name [{_out}] from original name [{in_path}]")
    return _out


# endregion [Functions_Names]


# region [Functions_Pickle]

# -------------------------------------------------------------- pickleit -------------------------------------------------------------- #
def pickleit(obj, in_path):
    # -------------------------------------------------------------- pickleit -------------------------------------------------------------- #
    """
    saves an object as pickle file.

    Parameters
    ----------
    obj : object
        the object to save
    in_name : str
        the name to use for the pickled file
    in_dir : str
        the path to the directory to use
    """
    with open(pathmaker(in_path), 'wb') as filetopickle:
        log.debug(f"saved object [{str(obj)}] as pickle file [{in_path}]")
        pickle.dump(obj, filetopickle, pickle.HIGHEST_PROTOCOL)


# -------------------------------------------------------------- get_pickled -------------------------------------------------------------- #
def get_pickled(in_path):
    # -------------------------------------------------------------- get_pickled -------------------------------------------------------------- #
    """
    loads a pickled file.

    Parameters
    ----------
    in_path : str
        the file path to the pickle file

    Returns
    -------
    object
        the pickled object
    """
    with open(pathmaker(in_path), 'rb') as pickletoretrieve:
        log.debug(f"loaded pickle file [{in_path}]")
        return pickle.load(pickletoretrieve)

# endregion [Functions_Pickle]


# region [Functions_Search]

# -------------------------------------------------------------- file_walker -------------------------------------------------------------- #
def file_walker(in_path, in_with_folders=False):
    # -------------------------------------------------------------- file_walker -------------------------------------------------------------- #
    """
    walks recursively through a file system and returns a list of file paths.

    Parameters
    ----------
    in_path : str
        the path to the directory from where to start

    Returns
    -------
    list
        a list of all files found as file paths.
    """
    _out_list = []
    log.debug(f"start to walk and find all files in [{in_path}]")
    for root, _, filelist in os.walk(in_path):
        for files in filelist:
            _out = os.path.join(root, files)
            _out_list.append(_out)
        if in_with_folders is True and root != in_path:
            _out_list.append(root)
    log.debug(f"finished walking [{in_path}]")
    return _out_list

# endregion [Functions_Search]


# region [Functions_Misc]

# -------------------------------------------------------------- limit_amount_of_files -------------------------------------------------------------- #
def limit_amount_of_files(in_basename, in_directory, in_amount_max):
    # -------------------------------------------------------------- limit_amount_of_files -------------------------------------------------------------- #
    """
    limits the amount of files in a folder that have a certain basename,

    if needed deletes the oldest and renames every file to move up namewise.

    (second oldest gets named to the oldest,...)

    Parameters
    ----------
    in_basename : str
        the common string all file names that should be affected share.
    in_directory : str
        path of the directory to affect
    in_amount_max : int
        the max amount of files allowed
    """
    log.debug(f"checking amount of files with name [{in_basename}] in [{in_directory}], if more than [{in_amount_max}]")
    _existing_file_list = []
    for files in os.listdir(pathmaker(in_directory)):
        if in_basename in files:
            _existing_file_list.append(pathmaker(in_directory, files))
    if len(_existing_file_list) > in_amount_max:
        log.debug(f"files are exceding max amount by [{len(_existing_file_list)-in_amount_max}]")
        _existing_file_list.sort(key=os.path.getmtime)
        for index, files in enumerate(_existing_file_list):
            _rename_index = index - 1
            if index == 0:
                os.remove(files)
                log.debug(f"removing oldest file [{files}]")
            elif index > in_amount_max:
                break
            else:
                os.rename(files, _existing_file_list[_rename_index])
                log.debug(f"renaming file [{files}] to [{_existing_file_list[_rename_index]}]")


def create_folder(in_path):
    if os.path.isdir(in_path) is False:
        log.error(f"Folder '{in_path}' does **NOT** exist!")
        os.makedirs(in_path)
        log.info("Created Folder '{in_path}'")
    else:
        log.info(f"Folder '{in_path}' does exist!")

# endregion [Functions_Misc]


# region [Main_Exec]
# sourcery skip: remove-redundant-if
if __name__ == '__main__':
    pass


# endregion [Main_Exec]
