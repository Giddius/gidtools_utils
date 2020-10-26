# region [Imports]

# * Gid Imports -->
import gidlogger as glog

# endregion [Imports]

__updated__ = '2020-10-14 14:39:03'

# region [Localized_Imports]


# endregion [Localized_Imports]


# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


# region [Constants]


# endregion [Constants]


# region [Misc]


# endregion [Misc]


# region [Global_Functions]


# endregion [Global_Functions]


# region [Data_1]

SOLID_CFG_STRING = """[DEFAULT]
main_dir: +cwd+
project_name: %PROJECT_NAME%

[specification]
is_gui:
is_db:

[locations]
ressources_folder: +cwd+ressources
data_folder: +cwd+ressources\data
icon_folder: +cwd+ressources\icons
archive_folder: +cwd+ressources\archive

[hashes]

"""


USER_CFG_STRING = """
[DEFAULT]
main_dir: cwd
project_name = PROJECT_NAME

[default_keys]

[from_user]
user_modified: no
;; possible options are: 'yes', 'no'

[locations]

"""


DB_CFG_STRING = """
[DEFAULT]
main_dir: cwd
project_name: PROJECT_NAME

[default_keys]

[db_parameter]
db_name: %(project_name)s.db
db_loc: ressources\%(db_name)s
archive_loc: ressources\archive
sql_script_folder: ressources\sql_procedures
pragmas: PRAGMA cache_size(-250000), PRAGMA synchronous(OFF)

[db_startup_parameter]
overwrite: True
max_backups: 1


[misc]

"""


EDITORCONFIG_STRING = """
root = true

[*]
indent_style = space
indent_size = 4
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true
"""


TODO_STRING = """
# TODO

---

---

## GUI

* [ ] misc


---

## FEATURES

* [ ] misc


---

## CODE

* [ ] misc


---

## DOC

* [ ] misc


---

---
"""


# endregion [Data_1]


# region [Data_2]


# endregion [Data_2]


# region [Data_3]


# endregion [Data_3]


# region [Data_4]


# endregion [Data_4]


# region [Data_5]


# endregion [Data_5]


# region [Dict_1]


# endregion [Dict_1]


# region [Dict_2]

SQL_JINJA_DICT = {
    'SELECT': 'SELECT {% if columns == "all" %}*{% else %}{% for column in columns %}"{{ column }}"{{ ", " if not loop.last }}{% endfor %}{% endif %} FROM "{{ table_name }}"',
    'SELECT_WHERE': 'SELECT {% if columns == "all" %}*{% else %}{% for column in columns %}"{{ column }}"{{ ", " if not loop.last }}{% endfor %}{% endif %} FROM "{{ table_name }}" WHERE {% for where in wheres %}"{{ where[0] }}" = "{{ where[1] }}"{{ " AND " if not loop.last }}{% endfor %}',
    'CREATE_TABLE': 'CREATE TABLE IF NOT EXISTS "{{ table_name }}" ({% for category in categories %}"{{ category[0] }}" {{ category[1] }} {{ category[2] }}{{ ", " if not loop.last }}{% endfor %}{% if unique %}, UNIQUE({% for unique in uniques %}"{{ unique }}"{{ ", " if not loop.last }}{% endfor %}){% endif %})',
    'UPDATE': 'UPDATE {{ table_name }} SET {% for column in columns %}"{{column[0]}}" = "{{ column[1] }}"{{ ", " if not loop.last }}{% endfor %} WHERE {% for where in wheres %}"{{ where[0] }}" = "{{ where[1] }}{{ " AND " if not loop.last }}{% endfor %}"',
    'DROP_TABLE': 'DROP TABLE {{ table_name }}',
    'INSERT': 'INSERT OR IGNORE INTO {{ table_name }} VALUES (NULL, {% for column in columns %}"{{ column }}"{{ ", " if not loop.last }}{% endfor %})',
}

# endregion [Dict_2]


# region [Dict_3]


# endregion [Dict_3]


# region [Dict_4]


# endregion [Dict_4]


# region [Dict_5]


# endregion [Dict_5]


# region [List_1]


# endregion [List_1]


# region [List_2]


# endregion [List_2]


# region [List_3]


# endregion [List_3]


# region [List_4]


# endregion [List_4]


# region [List_5]


# endregion [List_5]


# region [Main_Exec]

if __name__ == '__main__':
    pass


# endregion [Main_Exec]
