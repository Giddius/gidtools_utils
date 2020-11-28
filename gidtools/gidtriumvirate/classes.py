# region [Imports]

# * Standard Library Imports -->
import shutil
import sqlite3
import configparser
from sqlite3 import Error
from contextlib import contextmanager

# * Gid Imports -->
import gidlogger as glog
import gidtools.gidfiles as gif

# endregion [Imports]

__updated__ = '2020-10-14 14:38:55'

# region [Logging]

log = glog.aux_logger(__name__)
log.debug(glog.imported(__name__))

# endregion [Logging]


class GidConfigMaster:
    # region [Class_GidConfigMaster]
    def __init__(self, config_name, config_loc, auto_convert_list=False, list_delim=', '):
        self.cfg_handle = configparser.ConfigParser()
        self.config_name = config_name
        self.config_location = gif.pathmaker('cwd', 'config') if config_loc == 'default' else gif.pathmaker(config_loc)
        self.config = gif.pathmaker(self.config_location, self.config_name)
        self.cfg_sections = self.read_config()
        self.convert_list = auto_convert_list
        self.list_delim = list_delim

    def read_config(self, in_section=None, in_key=None):
        self.cfg_handle.read(self.config)

        if in_section is None and in_key is None:
            _output = self.cfg_handle.sections()
        elif in_section is not None and in_key is None:
            _output = self.cfg_handle.options(in_section)
        elif in_section is not None and in_key is not None:
            _output = self.cfg_handle[in_section][in_key]
        return _output

    def sections_as_attributes(self):
        for section in self.cfg_sections:
            _temp_dict = {}
            if section == 'default_keys':
                for key in self.read_config(section):
                    if self.convert_list is True and self.list_delim in self.read_config(section, key):
                        _temp_dict[key] = self.read_config(section, key).split(self.list_delim)
                    else:
                        _temp_dict[key] = os.getcwd() if self.read_config(section, key) == 'cwd' else self.read_config(section, key)
            else:
                for key in self.read_config(section):
                    if key not in self.read_config('default_keys'):
                        if self.convert_list is True and self.list_delim in self.read_config(section, key):
                            _temp_dict[key] = self.read_config(section, key).split(self.list_delim)
                        else:
                            _temp_dict[key] = self.read_config(section, key)
            setattr(self, section, _temp_dict)

    @property
    def read(self):
        self.cfg_handle.read(self.config)

    def cfg_items(self, in_section):
        self.read
        return self.cfg_handle.items(in_section)

    def cfg_dict_wlist(self, in_section):
        _out = {}
        for key, value in getattr(self, in_section).items():
            _out[key] = value.replace(' ', '').split(',') if ',' in value else value
        return _out

    def get_value(self, in_section, in_key):
        self.read
        _out = self.cfg_handle[in_section][in_key]
        if self.convert_list is True and self.list_delim in _out:
            _out = _out.split(self.list_delim)
        return _out

    @classmethod
    def from_fullpath(cls, full_path):
        cfile = gif.pathmaker(full_path)
        cfile = gif.splitoff(cfile)[1]
        cpath = gif.pathmaker(full_path)
        cpath = gif.splitoff(cpath)[0]
        return cls(cfile, cpath)

# -------------------------------------- modify ini Section -------------------------------------- #
    def add_or_update_option(self, in_section, option_key, in_option_value):
        self.cfg_handle.read(self.config)
        self.cfg_handle.set(in_section, option_key, in_option_value)
        self.write_to_file(self.config)
        self.sections_as_attributes()
        log.debug(f"created or updated section in {self.config} --> [{in_section}], {option_key} with {in_option_value}")

    def remove_key_value(self, in_section, in_key):
        self.cfg_handle.read(self.config)
        self.cfg_handle.remove_option(in_section, in_key)
        self.write_to_file(self.config)
        log.debug(f"removed key in {self.config} --> [{in_section}], {in_key}")

    def config_object_clear(self):
        self.cfg_handle = ''
        self.cfg_handle = configparser.ConfigParser()
        log.debug(f"cleared {self.config}")

    def create_config_section(self, in_section, in_option_dict: dict):
        self.cfg_handle[in_section] = in_option_dict

    def write_to_file(self, in_config):
        with open(in_config, 'w') as new_config:
            self.cfg_handle.write(new_config)
# ------------------------------------ end modify ini Section ------------------------------------ #

    def __repr__(self):
        return f"{self.__class__.__name__} '{self.config_name}' '{self.config_location}/' '{self.cfg_sections}'"

    def __str__(self):
        return f"Class {self.__class__.__name__} using {self.config_name} located at {self.config_location}/ containing:\nsections:\n\t\t\t\t{self.cfg_sections}\n\n"

# endregion [Class_GidConfigMaster]


class GiDataBaseMaster:
    # region [Class_GiDataBaseMaster]
    # --------------------------------------------- init --------------------------------------------- #
    def __init__(self, in_cwd, in_db_name, in_db_loc, in_sql_script_loc, in_pragma=None):
        self.db_name = in_db_name
        self.db_loc = gif.pathmaker(in_cwd, in_db_loc)
        self.db = gif.pathmaker(in_cwd, self.db_loc, self.db_name)
        self.pragma = () if in_pragma is None else in_pragma
        self.tables = []
        self.sql_script_loc = in_sql_script_loc
        self.db_status = ''

# ------------------------------------------- end init ------------------------------------------- #

# ------------------------------------ database contextmanager ----------------------------------- #
    @contextmanager
    def opendb(self, row_factory=None):
        conn = sqlite3.connect(self.db)
        for pragma in self.pragma:
            try:
                conn.execute(pragma)
                log.info(f"Executed PRAGMA [{pragma}] successfully")
            except Error as error:
                log.critical(str(error) + f' - with PRAGMA [{pragma}]' + '\n\n')
        if row_factory is not None:
            conn.row_factory = row_factory
        yield conn.cursor()
        conn.commit()
        conn.close()
# ---------------------------------- end database contextmanager --------------------------------- #

    def script_executer(self, in_script):
        with self.opendb() as conn:
            try:
                conn.executescript(in_script)
                _str = '\n'.join(in_script.split(';'))
                log.debug(f"Executed [{_str}] successfully")

            except Error as error:
                log.critical(str(error) + f' - with SQL [{in_script}]' + '\n\n')
        return None

# ---------------------------------------- phrase_executer --------------------------------------- #
    def phrase_executer(self, in_phrase, in_variables=None):
        with self.opendb() as conn:
            try:
                if in_variables is None:
                    conn.execute(in_phrase)
                    log.info(f"Executed [{in_phrase}]")
                else:
                    conn.execute(in_phrase, in_variables)
                    log.info(f"Executed [{in_phrase}] with variables[{in_variables}]")
            except Error as error:
                log.critical(str(error) + f' - with SQL [{in_phrase}]' + '\n\n')
# -------------------------------------- end phrase_executer ------------------------------------- #

# ---------------------------------------- query_executer ---------------------------------------- #
    def query_executer(self, in_phrase, in_variables=None, row_factory=None, mode='all'):
        # query Section
        with self.opendb(row_factory) as conn:
            try:
                if in_variables is None:
                    conn.execute(in_phrase)
                    log.info(f"Executed [{in_phrase}]")
                else:
                    conn.execute(in_phrase, in_variables)

            except Error as error:
                log.critical(str(error) + f' - with SQL [{in_phrase}]' + '\n\n')

            # assign to variable Section
            if mode == 'all':
                _results = conn.fetchall()
            elif mode == 'one':
                _results = conn.fetchone()

            # output Section
            return _results
# -------------------------------------- end query_executer -------------------------------------- #

# ------------------------------------------- start_db ------------------------------------------- #
    def start_db(self, overwrite=False, backup=True, in_num_backups=2):
        self.db_exist()
        log.info(f"starting to check database ['{self.db_name}']")
        if self.db_status == 'EXISTING' and overwrite is False:
            _out = True

        elif self.db_status == 'NOT_EXISTING' or overwrite is True:
            log.info(f"starting to create database ['{self.db_name}']")
            self.delete_db_if_exist(backup, in_num_backups)
            if self.pragma != ():
                self.add_pragma()
            self.create_std_init_tables()
            log.info(f"standard tables created for database ['{self.db_name}']")
            self.create_extra_init_tables()
            log.info(f"extra init tables created for database ['{self.db_name}']")
            self.db_exist()
            _out = False
        return _out
# ----------------------------------------- end start_db ----------------------------------------- #

# ------------------------------------------- fetch_toc ------------------------------------------ #
    def fetch_toc(self):
        pass
        # return self.query_executer(self.sql_init['que_toc'])
# ----------------------------------------- end fetch_toc ---------------------------------------- #

# -------------------------------------- delete_db_if_exist -------------------------------------- #
    def delete_db_if_exist(self, backup=False, in_num_backups=2):
        self.db_exist()
        if self.db_status == 'EXISTING':
            if backup is True:
                _archive_path = gif.pathmaker(self.default_keys['main_dir'], self.db_parameter['archive_loc'])
                _db_archive_loc = gif.pathmaker(_archive_path, self.db_name)
                gif.limit_amount_of_files(gif.ext_splitter(self.db_name), _archive_path, in_num_backups)
                if os.path.exists(_db_archive_loc) is True:
                    _round = 1
                    _db_archive_loc = gif.number_rename(gif.pathmaker(_db_archive_loc), _round)
                    log.debug(f" Backing up db as {_db_archive_loc}")

                shutil.copy(self.db, _db_archive_loc)

                log.info(f"copied db as backup to {_db_archive_loc}")

            os.remove(self.db)
            log.warning(f"removed {self.db_name}")

# ------------------------------------ end delete_db_if_exist ------------------------------------ #

# ------------------------------------ create_std_init_tables ------------------------------------ #
    def create_std_init_tables(self):
        # create toc_tbl
        self.phrase_executer(self.sql_init['cre_toc'])
        log.info("created toc")
        # create tablegroup_tbl
        self.phrase_executer(self.sql_init['cre_tablegroup_tbl'])
        log.info("created tablegroup_tbl")
# ---------------------------------- end create_std_init_tables ---------------------------------- #

# ----------------------------------- create_extra_init_tables ----------------------------------- #
    def create_extra_init_tables(self):
        for entries in self.read_config('sql_init_create'):
            if entries not in ['main_dir', 'project_name']:
                _sql = self.sql_init_create[entries]
                self.phrase_executer(_sql)
                self.insert_to_toc(entries, 'initial')
# --------------------------------- end create_extra_init_tables --------------------------------- #

# ----------------------------------------- insert_to_toc ---------------------------------------- #
    def insert_to_toc(self, tbl_name, in_tablegroup):
        _sql = self.sql_init['ins_toc']
        self.create_tablegroup(in_tablegroup)
        self.phrase_executer(_sql, (f'{tbl_name}', in_tablegroup))
# --------------------------------------- end insert_to_toc -------------------------------------- #

# --------------------------------------- create_tablegroup -------------------------------------- #
    def create_tablegroup(self, in_tablegroup):
        _sql = self.sql_init['ins_tablegroup_tbl']
        self.phrase_executer(_sql, (in_tablegroup, '-'))
# ------------------------------------- end create_tablegroup ------------------------------------ #

    def drop_table(self, in_table_name):
        _sql = 'DROP TABLE IF EXISTS "' + in_table_name + '"'
        self.phrase_executer(_sql)

    def delete_from_toc(self, in_table_name):
        _sql = 'DELETE FROM toc_tbl WHERE tbl_name='
        _sql += '"' + in_table_name + '"'
        self.phrase_executer(_sql)

# ------------------------------------------- db_exist ------------------------------------------- #
    def db_exist(self):
        self.db_status = 'EXISTING' if os.path.exists(self.db) is True else 'NOT_EXISTING'
        log.info(f"DB status is --> [{self.db_status}]")
        return self.db_status
# ----------------------------------------- end db_exist ----------------------------------------- #

# -------------------------------------------- vacuum -------------------------------------------- #
    def vacuum(self):
        self.phrase_executer("VACUUM")
# ------------------------------------------ end vacuum ------------------------------------------ #

# -------------------------------------------- pragma -------------------------------------------- #
    def add_pragma(self):
        for pragma in self.pragma:
            self.phrase_executer(pragma)

# -------------------------------------------- dunder -------------------------------------------- #
    def __bool__(self):
        return os.path.exists(self.db)

    def __repr__(self):
        return f"{self.__class__.__name__} '{self.db_name}' '{self.db_loc}'"

    def __str__(self):
        _sql_phrase = "SELECT tbl_name FROM toc_tbl"
        _output = self.querista(_sql_phrase)
        _tbl_list = '\n'.join(_output)
        return f"Class {self.__class__.__name__} with tables: {_tbl_list}"
# ------------------------------------------ end dunder ------------------------------------------ #

# endregion [Class_GiDataBaseMaster]


class GiDataBase(GidConfigMaster, GiDataBaseMaster):
    # region [Class_GiDataBase]
    def __init__(self, in_config_loc='default', in_pragma=None, in_change_loc=False):
        GidConfigMaster.__init__(self, config_name='db_config.ini', config_loc=in_config_loc)
        self.change_loc = in_change_loc
        if self.change_loc is True:
            self.target_dir = gif.path_part_remove(self.config_location)
            with gif.work_in(self.target_dir):
                self.sections_as_attributes()
        else:
            self.sections_as_attributes()
        log.debug(f"cwd is [{self.default_keys['main_dir']}]")
        log.debug(f"database location is [{self.db_parameter['db_loc']}]")
        log.debug(f"database name  is [{self.db_parameter['db_name']}]")
        GiDataBaseMaster.__init__(self, self.default_keys['main_dir'], self.db_parameter['db_name'], self.db_parameter['db_loc'], gif.pathmaker(self.db_parameter['sql_script_folder']), in_pragma=in_pragma)


# endregion [Class_GiDataBase]


class GiUserConfig(GidConfigMaster):
    # region [Class_GiUserConfig]
    def __init__(self, in_config_loc='default', in_change_loc=False):
        super().__init__(config_name='user_config.ini', config_loc=in_config_loc)
        self.change_loc = in_change_loc
        if self.change_loc is True:
            self.target_dir = gif.path_part_remove(self.config_location)
            with gif.work_in(self.target_dir):
                self.sections_as_attributes()
        else:
            self.sections_as_attributes()

# endregion [Class_GiUserConfig]


class GiSolidConfig(GidConfigMaster):
    # region [Class_GiSolidConfig]
    def __init__(self, in_config_loc='default', in_change_loc=False):
        super().__init__(config_name='solid_config.ini', config_loc=in_config_loc)
        self.change_loc = in_change_loc
        if self.change_loc is True:
            self.target_dir = gif.path_part_remove(self.config_location)
            print(self.target_dir)
            with gif.work_in(self.target_dir):
                print(os.getcwd())
                self.sections_as_attributes()
        else:
            self.sections_as_attributes()

# endregion [Class_GiSolidConfig]

# region [Class_GiVariousConfig]


class GiVariousConfig(GidConfigMaster):
    def __init__(self, config_name, config_loc='default', in_change_loc=False):
        super().__init__(config_name, config_loc)
        self.change_loc = in_change_loc

        if self.change_loc is True:
            self.target_dir = gif.path_part_remove(self.config_location)
            with gif.work_in(self.target_dir):
                self.sections_as_attributes()
        else:
            self.sections_as_attributes()


# endregion [Class_GiVariousConfig]

# region [Class_1]


# endregion [Class_1]


# region [Main_Exec]
if __name__ == '__main__':
    pass


# endregion [Main_Exec]
