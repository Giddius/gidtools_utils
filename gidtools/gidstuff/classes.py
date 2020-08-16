# region [Imports]

# * normal imports -->
import re
import random
# * gid imports -->
import gidlogger as glog
from gidtools.gidtriumvirate import give_std_repr
from gidtools.gidfiles import writeit, readit
# * Qt imports -->

# endregion [Imports]

__updated__ = '2020-08-12 13:45:14'

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


# region [Random_Class_RGB]

class RandomRGB:
    def __init__(self):
        self.name = 'rgb'
        self.last = {'r': 0, 'g': 0, 'b': 0}

    def __call__(self):
        _list = [50, 25, 10]
        _back_list = [256, 200, 150]
        random.shuffle(_list)
        random.shuffle(_back_list)
        r = random.randint(_list[0], _back_list[0])
        g = random.randint(_list[1], _back_list[1])
        b = random.randint(_list[2], _back_list[2])
        self.last = {'r': r, 'g': g, 'b': b}

        return (r, g, b, 0.25)

    def make_settings_region(self, in_settings, in_name_list):
        self.color_list = []
        for item in in_name_list:
            self.color_list.append(f'    "{item}": "{str(self)}",')
        col_reg_set_rex = re.compile('(?<="coloredRegions.namedColors": {\n).*?(?=},)', re.DOTALL)
        _out_str = '\n'.join(self.color_list) + '\n'
        _out_str += '    '
        writeit(in_settings, re.sub(col_reg_set_rex, _out_str, readit(in_settings)))

    def __repr__(self):
        return give_std_repr(self)

    def __str__(self):
        r, g, b, a = self.__call__()
        return f'rgb({str(r)}, {str(g)}, {str(b)}, {str(a)})'


# endregion [Random_Class_RGB]


# region [Class_1]


# endregion [Class_1]


# region [Class_2]


# endregion [Class_2]


# region [Class_3]


# endregion [Class_3]

# region [Class_4]


# endregion [Class_4]

# region [Class_5]


# endregion [Class_5]

# region [Class_6]


# endregion [Class_6]

# region [Class_7]

# endregion [Class_7]

# region [Class_8]

# endregion [Class_8]

# region [Class_9]

# endregion [Class_9]
# region [Main_Exec]
if __name__ == '__main__':
    pass


# endregion [Main_Exec]
