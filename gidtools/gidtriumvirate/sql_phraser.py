# region [Imports]

# * Standard Library Imports -->
from enum import Enum, Flag, auto

# * Gid Imports -->
import gidlogger as glog

# endregion [Imports]

__updated__ = '2020-10-14 14:39:52'

# region [Logging]

log = glog.aux_logger(__name__)
log.debug(glog.imported(__name__))

# endregion [Logging]

# region [Constants]


# endregion [Constants]


# region [Enums]

class sqltype(Enum):
    Text = 'TEXT'
    Integer = 'INTEGER'
    Blob = 'BLOB'
    Primkey = 'PRIMARY KEY'

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.data


class sqlspec(Enum):
    Unique = 'UNIQUE'
    NotNull = 'NOT NULL'
    Default = auto()

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.data

    def __add__(self, other):
        return str(self) + ' ' + str(other)

    def __radd__(self, other):
        return str(other) + ' ' + str(self)


# endregion [Enums]

# region [Global_Functions]

# endregion [Global_Functions]

# region [Factories]

# endregion [Factories]

# region [Paths]

# endregion [Paths]

# region [Singleton_Objects]

# endregion [Singleton_Objects]

# region [Support_Objects]

# endregion [Support_Objects]

# region [Functions_1]

# endregion [Functions_1]

# region [Functions_2]

# endregion [Functions_2]

# region [Functions_3]

# endregion [Functions_3]

# region [Functions_4]

# endregion [Functions_4]

# region [Functions_5]


def foreignkey(ref_table_name, ref_column):
    return f'REFERENCES "{ref_table_name}" ("{ref_column}")'

# endregion [Functions_5]

# region [Class_1]


class SQLPhraseGenerator:
    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = {}

    @property
    def create_table_phrase(self):
        _phrase = f'CREATE TABLE IF NOT EXISTS "{self.table_name}" ('
        for key, value in self.columns.items():
            _phrase += f'"{key}" {value}, '
        _phrase = _phrase.rstrip(', ') + ')'
        return _phrase

    def add_column(self, name, datatype, *flags, forkey=None):
        if datatype == sqltype.Primkey:
            self.columns[name] = 'INTEGER PRIMARY KEY'
        else:
            self.columns[name] = f'{str(datatype)}'
            for flag in flags:
                self.columns[name] += flag
            self.columns[name] = self.columns[name].strip()
            if forkey is not None:
                self.columns[name] += ' ' + forkey


# endregion [Class_1]


# region [Class_2]


# endregion [Class_2]


# region [Class_3]


# endregion [Class_3]


# region [Class_4]


# endregion [Class_4]


# region [Class_5]


# endregion [Class_5]


# region [Main_Exec]

if __name__ == '__main__':
    a = SQLPhraseGenerator('test_table')
    a.add_column('test_column', sqltype.Text, sqlspec.NotNull, sqlspec.Unique, forkey=foreignkey('wurst', 'wurst_id'))
    a.add_column('test2_column', sqltype.Primkey)
    print(a.create_table_phrase)


# endregion [Main_Exec]
